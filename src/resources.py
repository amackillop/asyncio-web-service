"""
HTTP Resources
"""
import asyncio
import datetime as dt
import logging
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

logging.basicConfig(level=logging.INFO)

ROUTES = web.RouteTableDef()


@ROUTES.view("/v1/jobs")
class Jobs(web.View):
    async def get(self) -> web.Response:
        """Get a list of all submitted jobs"""
        return web.json_response(list(self.request.app.get("jobs", {}).keys()))

    async def post(self) -> web.Response:
        """Post a job"""
        req = await self.request.json()
        urls = req.get("urls", None)
        if urls is None:
            msg = "Bad Request. No `urls` field."
            return web.Response(status=400, reason=msg)
        job_id = str(uuid.uuid4())
        self.request.app["jobs"][job_id] = self._submit_job(job_id, urls)
        return web.json_response(job_id, status=201)

    def _submit_job(self, job_id: str, urls: List[str]) -> Job:
        valid, invalid = hf.partition(hf.is_valid_url, urls)
        job = Job(job_id, Uploaded(pending=list(valid), failed=list(invalid)))
        asyncio.create_task(self._handle_job(job))
        return job

    async def _handle_job(self, job: Job) -> None:
        job.status = "in-progress"
        images = await asyncio.gather(
            *[self._handle_download(job, url) for url in job.uploaded.pending]
        )
        results = await asyncio.gather(*[self._upload(image) for image in images])
        job.finished = dt.datetime.utcnow().isoformat()
        job.status = "complete"

    @staticmethod
    async def _handle_download(job: Job, url: str) -> pm.Either[str]:
        try:
            image = await hf.download_image(url)
        except (ClientError, IOError) as exc:
            logging.info("Failed: %s", url)
            job.uploaded.failed.append(url)
            job.uploaded.pending.remove(url)
            return pm.Left(str(exc))

        logging.info("Success: %s", url)
        job.uploaded.completed.append(url)
        job.uploaded.pending.remove(url)
        return pm.Right(image)

    async def _upload(self, image: pm.Either[str]) -> pm.Either[str]:
        return either.either(identity, identity, image)


@ROUTES.view("/v1/jobs/{job_id}")
class SingleJob(web.View):
    async def get(self) -> web.Response:
        """Check job status"""
        job_id = self.request.match_info.get("job_id", None)
        job = self.request.app["jobs"].get(job_id, None)
        if job is None:
            return web.json_response(
                {"error": f"Job {job_id} was not found."}, status=404
            )
        return web.json_response(job.to_dict())


@ROUTES.view("/v1/images")
class Images(web.View):
    async def get(self) -> web.Response:
        """Get list of uploaded images"""
        result = subprocess.run(
            "hostname", shell=True, stdout=subprocess.PIPE, check=True
        )
        return web.Response(text=result.stdout.decode())
