import re
import urllib.parse

import requests


def remove_double_slashes_from_path(url: str, ensure_https: bool = True) -> str:
    """Ensure that a URL uses HTTPS and does not contain `//` in its path."""
    u = urllib.parse.urlparse(url)
    path = u.path.replace("//", "/")
    url = f"{u.netloc}{path}".replace("//", "/")
    if ensure_https:
        return f"https://{url}"
    return f"{u.scheme}://{url}"


def replace_first_subdomain(url: str, replace_with: str) -> str:
    regex = re.compile(r"^https?:\/\/(www\.)?(.*?)(\..*)$")
    return regex.sub(rf"https://\1{replace_with}\3", url)


def download_from_url(url: str, target_path: str):
    """
    Download artifacts stored at a certain url and saves them in target path.
    """
    file = requests.get(url, stream=True)

    with open(target_path, "wb") as f:
        for chunk in file:
            f.write(chunk)


def get_local_path_from_url(url: str, target_dir: str, filetype: str) -> str:
    filename = url.split("/")[-1].split(filetype)[0] + filetype
    if not target_dir[-1] == "/":
        target_dir += "/"
    return target_dir + filename
