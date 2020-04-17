""""""
import pytest
import re
import requests
import subprocess as sp


def test_submit_job_returns_uuid_on_success(capsys):
    match_uuid = re.compile(
        r"[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"
    )
    res = requests.post(
            "http://localhost:8080/v1/jobs",
            data='{"urls":["https://www.dummyimage.com/80x80", "https://www.dumimage.com/40x40"]}',
            headers={"Content-Type": "application/json"},
        )
    try:
        res.raise_for_status()
    except requests.HTTPError as exc:
        pytest.fail(exc)
    assert match_uuid.match(res.json())

