import logging
import tempfile
import uuid
import zipfile

import mantik.cli.utils as utils
import mantik.utils.mantik_api as mantik_api
import mantik.utils.urls

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def download_artifacts(
    project_id: uuid.UUID,
    run_id: uuid.UUID,
    target_dir: str,
    unzip: bool,
):
    artifacts_url = mantik_api.run.get_download_artifact_url(
        project_id=project_id,
        run_id=run_id,
        token=utils.access_token_from_env_vars(),
    )
    artifacts_path = mantik.utils.urls.get_local_path_from_url(
        target_dir=target_dir, url=artifacts_url, filetype=".zip"
    )
    if unzip:
        download_and_unzip_file_from_internet(
            artifacts_path=artifacts_path,
            artifacts_url=artifacts_url,
            target_dir=target_dir,
        )
    else:
        mantik.utils.urls.download_from_url(
            url=artifacts_url, target_path=artifacts_path
        )
        logger.info(f"Successfully downloaded at {artifacts_path}`")


def download_and_unzip_file_from_internet(
    artifacts_path: str,
    artifacts_url: str,
    target_dir: str,
):
    with tempfile.TemporaryDirectory() as temp_dir_name:
        temp_file = temp_dir_name + "/" + artifacts_path.split("/")[-1]
        mantik.utils.urls.download_from_url(
            url=artifacts_url, target_path=temp_file
        )
        with zipfile.ZipFile(temp_file, "r") as zip_ref:
            zip_ref.extractall(target_dir)
    logger.info(f"Artifacts successfully downloaded at {target_dir}`")
