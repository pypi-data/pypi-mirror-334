import os
import socket
import pathlib
from unittest.mock import patch
from typing import Optional, Generator

import pytest

from .mock_slurm import mock_slurm_clients


def pytest_addoption(parser):
    parser.addoption(
        "--slurm-root-directory",
        action="store",
        default=None,
        help="Specify the SLURM root directory for logs and data.",
    )
    parser.addoption(
        "--slurm-api-version",
        action="store",
        default=None,
        help="Specify the SLURM API version.",
    )


@pytest.fixture(scope="session")
def slurm_root_directory(tmp_path_factory, request):
    path = request.config.getoption("--slurm-root-directory")
    if path:
        return pathlib.Path(path)
    return tmp_path_factory.mktemp("slurm_root")


@pytest.fixture(scope="session", params=["mock", "production"])
def slurm_parameters(request) -> dict:
    api_version = request.config.getoption("--slurm-api-version")

    if request.param == "mock":
        return {
            "mock": True,
            "url": "mockurl",
            "token": "mocktoken",
            "user_name": "mockuser",
            "api_version": api_version,
        }

    if request.param == "production":
        url = os.environ.get("SLURM_URL")
        if not url:
            pytest.skip("SLURM_URL environment variable required")

        token = os.environ.get("SLURM_TOKEN")
        if not token:
            pytest.skip("SLURM_TOKEN environment variable required")

        user_name = os.environ.get("SLURM_USER")
        if not user_name:
            pytest.skip("SLURM_USER environment variable required")

        slurm_root_directory = request.config.getoption("--slurm-root-directory")
        if not slurm_root_directory:
            pytest.skip("--slurm-root-directory pytest argument is required")

        api_version = os.environ.get("SLURM_API_VERSION", api_version)

        return {
            "mock": False,
            "url": url,
            "token": token,
            "user_name": user_name,
            "api_version": api_version,
        }

    raise ValueError(request.param)


@pytest.fixture(scope="session")
def slurm_log_directory(
    slurm_root_directory, tmp_path_factory, slurm_parameters
) -> Optional[str]:
    if slurm_parameters["mock"]:
        return tmp_path_factory.mktemp("slurm_logs")
    if slurm_root_directory:
        return slurm_root_directory / slurm_parameters["user_name"] / "slurm_logs"


@pytest.fixture(scope="session")
def slurm_data_directory(
    slurm_root_directory, tmp_path_factory, slurm_parameters
) -> Optional[str]:
    if slurm_parameters["mock"]:
        return tmp_path_factory.mktemp("slurm_data")
    if slurm_root_directory:
        return slurm_root_directory / slurm_parameters["user_name"] / "slurm_data"


@pytest.fixture(scope="session")
def mock_job_name():
    job_name = f"pyslurmutils.unittest.{socket.gethostname()}"
    with patch("pyslurmutils.client.defaults.JOB_NAME", job_name):
        yield job_name


@pytest.fixture(scope="session")
def slurm_client_kwargs(
    slurm_log_directory, tmp_path_factory, slurm_parameters, mock_job_name
) -> Generator[dict, None, None]:
    # This must remain a session scope fixture for third-party libraries
    params = dict(slurm_parameters)
    _ = params.pop("mock")
    params["log_directory"] = slurm_log_directory
    if slurm_parameters["mock"]:
        tmp_path = tmp_path_factory.mktemp("slurm_mock")
        with mock_slurm_clients(tmp_path, slurm_parameters):
            yield params
    else:
        yield params
