# -*- coding: utf-8 -*-

"""Download content."""

import zipfile
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

from .api import download_tgt_versioned

__all__ = [
    "download_umls",
    "download_umls_metathesaurus",
    "open_umls",
]

UMLS_URL_FMT = "https://download.nlm.nih.gov/umls/kss/{version}/umls-{version}-mrconso.zip"
UMLS_METATHESAURUS_URL_FMT = (
    "https://download.nlm.nih.gov/umls/kss/{version}/umls-{version}-metathesaurus.zip"
)


def _download_umls(
    url_fmt: str,
    version: Optional[str] = None,
    *,
    api_key: Optional[str] = None,
    force: bool = False,
) -> Path:
    return download_tgt_versioned(
        url_fmt=url_fmt,
        version=version,
        version_key="umls",
        module_key="umls",
        api_key=api_key,
        force=force,
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
    return _download_umls(url_fmt=UMLS_URL_FMT, version=version, api_key=api_key, force=force)


def download_umls_metathesaurus(
    version: Optional[str] = None, *, api_key: Optional[str] = None, force: bool = False
) -> Path:
    """Ensure the given version of the UMLS metathesaurus zip archive.

    :param version: The version of UMLS to ensure. If not given, is looked up
        with :mod:`bioversions`.
    :param api_key: An API key. If not given, is looked up using
        :func:`pystow.get_config` with the ``umls`` module and ``api_key`` key.
    :param force: Should the file be re-downloaded, even if it already exists?
    :return: The path of the file for the given version of UMLS.
    """
    return _download_umls(
        url_fmt=UMLS_METATHESAURUS_URL_FMT, version=version, api_key=api_key, force=force
    )


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
