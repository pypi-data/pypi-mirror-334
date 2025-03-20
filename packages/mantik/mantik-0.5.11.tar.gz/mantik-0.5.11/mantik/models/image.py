import logging
import uuid

import mantik.cli.utils as utils
import mantik.utils.mantik_api.models
import mantik.utils.urls

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def download_container(
    project_id: uuid.UUID,
    model_id: uuid.UUID,
    target_dir: str,
    image_type: str,
    load: bool,
):
    if image_type.lower() == "docker":
        image_url = mantik.utils.mantik_api.models.get_image_url(
            project_id=project_id,
            model_id=model_id,
            token=utils.access_token_from_env_vars(),
        )

        image_path = mantik.utils.urls.get_local_path_from_url(
            target_dir=target_dir, url=image_url, filetype=".tar.gz"
        )
        _save_image(image_path=image_path, image_url=image_url)

        if load:
            _load_to_docker(image_path=image_path)
        else:
            logger.info(
                "In order to load the image into docker, "
                f"you can run `docker load < {image_path}`"
            )
    else:
        logger.error(f"We are sorry, {image_type} is not supported yet!")
        raise NotImplementedError


def _save_image(image_path: str, image_url: str):
    logger.info(
        f"Downloading image: {image_path}. This can take a few minutes..."
    )
    mantik.utils.urls.download_from_url(url=image_url, target_path=image_path)
    logger.info(f"Image saved as zipped tarball at {image_path}")


def _load_to_docker(image_path: str):
    try:
        import docker
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Install supported 'docker' version "
            "(`pip install mantik[docker]`)"
            "or any desired 'docker' python package version"
        ) from exc
    logger.info(
        "Unzipping and loading into docker. This can take a few minutes..."
    )

    client = docker.from_env()

    with open(image_path, "rb") as f:
        client.images.load(f)

    filename = image_path.split("/")[-1][:-7]
    logger.info(
        "Run 'docker images', an image named " f"{filename} should be present."
    )

    logger.info(
        f"Run 'docker run -p 8080:8080 {filename}` "
        "to serve the model image for inference."
    )
