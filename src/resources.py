"""
HTTP Resources
"""
import asyncio
import datetime as dt
import logging
import os
import subprocess
import uuid
from typing import List

from aiohttp import web
from aiohttp.client_exceptions import ClientError
import pymonads as pm
from pymonads import either
from pymonads.utils import identity


from my_types import Job, Uploaded
import helpers as hf
from redis_connection import ReJson

logging.basicConfig(level=logging.INFO)

ROUTES = web.RouteTableDef()

redis = ReJson(os.getenv("REDIS_HOST", "localhost"), os.getenv("REDIS_PORT", 6379))


@ROUTES.view("/v1/jobs")
class Jobs(web.View):

    async def post(self) -> web.Response:
        """Post a job"""
        req = await self.request.json()
        urls = req.get("urls", None)
        if urls is None:
            msg = "Bad Request. No `urls` field."
            return web.Response(status=400, reason=msg)
        job_id = str(uuid.uuid4())
        self._submit_job(job_id, urls)
        return web.json_response(job_id, status=201)

    def _submit_job(self, job_id: str, urls: List[str]) -> Job:
        valid, invalid = hf.partition(hf.is_valid_url, urls)
        job = Job(job_id, Uploaded(pending=list(valid), failed=list(invalid)))
        redis.post(job_id, job.to_dict())
        asyncio.create_task(self._handle_job(job))
        return job

    async def _handle_job(self, job: Job) -> None:
        job_id = job.job_id
        redis.update(job.job_id, 'status', 'In-Progress')
        images = await asyncio.gather(
            *[self._handle_download(job_id, url) for url in job.uploaded.pending]
        )
        results = await asyncio.gather(*[self._upload(image) for image in images])
        redis.update(job_id, 'finished', dt.datetime.utcnow().isoformat())
        redis.update(job_id, 'status', "complete")

    @staticmethod
    async def _handle_download(job_id: str, url: str) -> pm.Either[str]:
        try:
            image = await hf.download_image(url)
        except (ClientError, IOError) as exc:
            logging.info("Failed: %s", url)
            redis.append(job_id, 'uploaded.failed', url)
            redis.remove(job_id, 'uploaded.pending', url)
            return pm.Left(str(exc))

        logging.info("Success: %s", url)
        redis.append(job_id, 'uploaded.completed', url)
        redis.remove(job_id, 'uploaded.pending', url)
        return pm.Right(image)

    async def _upload(self, image: pm.Either[str]) -> pm.Either[str]:
        return either.either(identity, identity, image)


@ROUTES.view("/v1/jobs/{job_id}")
class SingleJob(web.View):
    async def get(self) -> web.Response:
        """Check job status"""
        job_id = self.request.match_info.get("job_id", None)
        job = redis.get(job_id)
        if job is None:
            return web.json_response(
                {"error": f"Job {job_id} was not found."}, status=404
            )
        return web.json_response(job)


@ROUTES.view("/v1/images")
class Images(web.View):
    async def get(self) -> web.Response:
        """Get list of uploaded images"""
        result = subprocess.run(
            "hostname", shell=True, stdout=subprocess.PIPE, check=True
        )
        return web.Response(text=result.stdout.decode())
