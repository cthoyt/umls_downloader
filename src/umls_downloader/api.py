# -*- coding: utf-8 -*-

"""Download functionality for the UMLS ticket granting system."""

import logging
from pathlib import Path
from typing import Callable, Optional, Union

import bs4
import pystow
import pystow.utils
import requests
from pystow.utils import name_from_url

__all__ = [
    "download_tgt",
    "download_tgt_versioned",
]

logger = logging.getLogger(__name__)

MODULE = pystow.module("bio", "umls")
TGT_URL = "https://utslogin.nlm.nih.gov/cas/v1/api-key"


def download_tgt(
    url: str, path: Union[str, Path], *, api_key: Optional[str] = None, force: bool = False
) -> None:
    """Download a file via the UMLS ticket granting system.

    This implementation is based on the instructions listed at
    https://documentation.uts.nlm.nih.gov/automating-downloads.html.

    :param url: The URL of the file to download, like
        ``https://download.nlm.nih.gov/umls/kss/2021AB/umls-2021AB-mrconso.zip``
    :param path: The local file path where the file should be downloaded
    :param api_key: An API key. If not given, is looked up using
        :func:`pystow.get_config` with the ``umls`` module and ``api_key`` key.
    :param force: Should the file be re-downloaded?
    """
    path = Path(path).resolve()
    if path.is_file() and not force:
        return

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


def download_tgt_versioned(
    url_fmt: str,
    version: Optional[str] = None,
    *,
    module_key: str,
    version_key: str,
    api_key: Optional[str] = None,
    force: bool = False,
    version_transform: Optional[Callable[[str], str]] = None,
) -> Path:
    """Download a file via the UMLS ticket granting system.

    :param url_fmt: The URL format of the file to download where ``{version}`` is
        used as a placeholder (potentially multiple times), like in
        ``https://download.nlm.nih.gov/umls/kss/{version}/umls-{version}-mrconso.zip``
    :param version: The version of the file to download
    :param module_key: The key for the pystow submodule of "bio"
    :param version_key: The key to look up the version via :mod:`bioversions`
        if the ``version`` parameter is not given explicitly.
    :param api_key: An API key. If not given, is looked up using
        :func:`pystow.get_config` with the ``umls`` module and ``api_key`` key.
    :param force: Should the file be re-downloaded?
    :param version_transform: A string transformation function, in case the version
        needs to be reformatted
    :returns: The local path to the downloaded versioned file
    :raises ValueError: if the URL format string doesn't have a ``{version}`` substring
    :raises RuntimeError: if no version is given and none can be looked up
    """
    if "{version}" not in url_fmt:
        raise ValueError("URL string can't format in a version")
    if version is None:
        import bioversions

        version = bioversions.get_version(version_key)
    if version is None:
        raise RuntimeError(f"Could not get version for {version_key}")
    if version_transform:
        version = version_transform(version)
    url = url_fmt.format(version=version)
    path = pystow.join("bio", module_key, version, name=name_from_url(url))
    download_tgt(url, path, api_key=api_key, force=force)
    return path
