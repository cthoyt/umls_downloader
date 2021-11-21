# -*- coding: utf-8 -*-

"""Download functionality for UMLS."""

import logging
import zipfile
from contextlib import contextmanager
from pathlib import Path
from typing import Optional, Union

import bs4
import pystow
import pystow.utils
import requests

__all__ = [
    "download_tgt",
    "download_umls",
    "open_umls",
]

logger = logging.getLogger(__name__)

MODULE = pystow.module("bio", "umls")
TGT_URL = "https://utslogin.nlm.nih.gov/cas/v1/api-key"


def download_tgt(url: str, path: Union[str, Path], *, api_key: Optional[str] = None) -> None:
    """Download a file via the UMLS ticket granting system.

    This implementation is based on the instructions listed at
    https://documentation.uts.nlm.nih.gov/automating-downloads.html.

    :param url: The URL of the file to download, like
        ``https://download.nlm.nih.gov/umls/kss/2021AB/umls-2021AB-mrconso.zip``
    :param path: The local file path where the file should be downloaded
    :param api_key: An API key. If not given, is looked up using
        :func:`pystow.get_config` with the ``umls`` module and ``api_key`` key.
    """
    api_key = pystow.get_config("umls", "api_key", passthrough=api_key, raise_on_missing=True)

    # Step 1: get a link to the ticket granting system (TGT)
    auth_res = requests.post(TGT_URL, data={"apikey": api_key})
    #  for some reason, this API returns HTML. This needs to be parsed,
    #  and there will be a form whose action is the next thing to POST to
    soup = bs4.BeautifulSoup(auth_res.text, features="html.parser")
    action_url = soup.find("form").attrs["action"]
    logger.info("[umls] got TGT url: %s", action_url)

    # Step 2: get a service ticket for the file you want to download
    #  by POSTing to the action URL with the name of the URL you actually
    #  want to download inside the form data
    key_res = requests.post(action_url, data={"service": url})
    # luckily this one just returns the text you need
    service_ticket = key_res.text
    logger.info("[umls] got service ticket: %s", service_ticket)

    # Step 3: actually try downloading the file you want, using the
    # service ticket issued in the last step as a query parameter
    pystow.utils.download(
        url=url,
        path=path,
        backend="requests",
        params={"ticket": service_ticket},
    )


def download_umls(
    version: Optional[str] = None, *, api_key: Optional[str] = None, force: bool = False
) -> Path:
    """Ensure the given version of the UMLS MRCONSO.RRF file.

    :param version: The version of UMLS to ensure. If not given, is looked up
        with :mod:`bioversions`.
    :param api_key: An API key. If not given, is looked up using
        :func:`pystow.get_config` with the ``umls`` module and ``api_key`` key.
    :param force: Should the file be re-downloaded, even if it already exists?
    :return: The path of the file for the given version of UMLS.
    """
    if version is None:
        import bioversions

        version = bioversions.get_version("umls")
    url = f"https://download.nlm.nih.gov/umls/kss/{version}/umls-{version}-mrconso.zip"
    path = MODULE.join(version, name=f"umls-{version}-mrconso.zip")
    if path.is_file() and not force:
        return path
    download_tgt(url, path, api_key=api_key)
    return path


@contextmanager
def open_umls(version: Optional[str] = None, *, api_key: Optional[str] = None, force: bool = False):
    """Ensure and open the UMLS MRCONSO.RRF file from the given version.

    :param version: The version of UMLS to ensure. If not given, is looked up
        with :mod:`bioversions`.
    :param api_key: An API key. If not given, is looked up using
        :func:`pystow.get_config` with the ``umls`` module and ``api_key`` key.
    :param force: Should the file be re-downloaded, even if it already exists?
    :yields: The file, which is used in the context manager.
    """
    path = download_umls(version=version, api_key=api_key, force=force)
    with zipfile.ZipFile(path) as zip_file:
        with zip_file.open("MRCONSO.RRF", mode="r") as file:
            yield file
