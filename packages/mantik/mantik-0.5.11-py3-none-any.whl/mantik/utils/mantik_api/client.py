import json
import logging
import typing as t

import requests

import mantik.utils as utils
import mantik.utils.mantik_api.credentials as credentials

_MANTIK_API_URL_ENV_VAR = "MANTIK_API_URL"
_MANTIK_API_SUBDOMAIN = "api"
_DEFAULT_MANTIK_API_URL = f"https://{_MANTIK_API_SUBDOMAIN}.cloud.mantik.ai"

_TOKENS_API_PATH_PREFIX = "/mantik/tokens"
MANTIK_API_CREATE_TOKEN_API_PATH = f"{_TOKENS_API_PATH_PREFIX}/create"
MANTIK_API_REFRESH_TOKEN_API_PATH = f"{_TOKENS_API_PATH_PREFIX}/refresh"

logger = logging.getLogger(__name__)


def create_tokens(
    access_credentials: t.Optional[credentials.Credentials] = None,
) -> t.Dict:
    """Get tokens from the Mantik API."""
    if access_credentials is None:
        access_credentials = credentials.Credentials.from_env()
    response = send_request_to_mantik_api(
        method="POST",
        data=access_credentials.to_dict(),
        url_endpoint=MANTIK_API_CREATE_TOKEN_API_PATH,
    )
    return response.json()


def refresh_tokens(
    refresh_token: str,
    access_credentials: t.Optional[credentials.Credentials] = None,
) -> t.Dict:
    """Get tokens from the Mantik API."""
    if access_credentials is None:
        access_credentials = credentials.Credentials.from_env()
    data = {
        **access_credentials.to_dict(include_password=False),
        "refresh_token": refresh_token,
    }
    response = send_request_to_mantik_api(
        method="POST", data=data, url_endpoint=MANTIK_API_REFRESH_TOKEN_API_PATH
    )
    return response.json()


def send_request_to_mantik_api(
    method: str,
    data: t.Union[dict, str],
    url_endpoint: str,
    token: t.Optional[str] = None,
    query_params: t.Optional[dict] = None,
) -> requests.Response:
    url = _create_url(url_endpoint)
    header = (
        {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }
        if token
        else None
    )
    request = {
        "url": url,
        "json": data,
        "headers": header,
        "params": query_params,
    }
    try:
        response = requests.request(method, **request)
        response.raise_for_status()
    except requests.HTTPError as e:
        logger.exception(
            "Call to Mantik API %s with data %s failed",
            url,
            data,
            exc_info=True,
        )
        try:
            message = e.response.json()["detail"]
        except (KeyError, json.decoder.JSONDecodeError):
            message = e.response.text
        raise requests.exceptions.HTTPError(
            f"Request to Mantik API failed: {message}",
            response=e.response,
        ) from e
    else:
        return response


def _create_url(endpoint: str) -> str:
    url = _get_base_url()
    url = utils.urls.remove_double_slashes_from_path(
        f"{url}{endpoint}", ensure_https=False
    )
    return url


def _get_base_url() -> str:
    """Gets the base URL for the mantik API.

    Notes
    -----
    Tries to get the base URL from (in order)
    `MANTIK_API_URL` env var

    Defaults to `https://api.cloud.mantik.ai`


    """
    mantik_api_url = utils.env.get_optional_env_var(_MANTIK_API_URL_ENV_VAR)
    if mantik_api_url is not None:
        logger.debug("Base URL for mantik API is set to %s", mantik_api_url)
        return mantik_api_url

    logger.debug(
        "Base URL for mantik API is set to %s", _DEFAULT_MANTIK_API_URL
    )
    return _DEFAULT_MANTIK_API_URL
