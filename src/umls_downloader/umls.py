# -*- coding: utf-8 -*-

"""Download content."""

import zipfile
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

from .api import download_tgt_versioned

__all__ = [
    "download_umls",
    "download_umls_full",
    "download_umls_metathesaurus",
    "open_umls",
    "open_umls_full",
    "open_umls_semantic_types",
    "open_umls_hierarchy",
]

UMLS_URL_FMT = "https://download.nlm.nih.gov/umls/kss/{version}/umls-{version}-mrconso.zip"
UMLS_METATHESAURUS_URL_FMT = (
    "https://download.nlm.nih.gov/umls/kss/{version}/umls-{version}-metathesaurus.zip"
)
UMLS_METATHESAURUS_FULL_FMT = (
    "https://download.nlm.nih.gov/umls/kss/{version}/umls-{version}-metathesaurus-full.zip"
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


def download_umls_full(
    version: Optional[str] = None, *, api_key: Optional[str] = None, force: bool = False
) -> Path:
    """Ensure the given version of the UMLS MRSTY.RRF file.

    :param version: The version of UMLS to ensure. If not given, is looked up
        with :mod:`bioversions`.
    :param api_key: An API key. If not given, is looked up using
        :func:`pystow.get_config` with the ``umls`` module and ``api_key`` key.
    :param force: Should the file be re-downloaded, even if it already exists?
    :return: The path of the file for the given version of UMLS.
    """
    return _download_umls(
        url_fmt=UMLS_METATHESAURUS_FULL_FMT, version=version, api_key=api_key, force=force
    )


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
        # In the 2023AB release, they added an intermediate META directory,
        # which means we have to go searching for the file by name
        for zip_info in zip_file.infolist():
            if "MRCONSO.RRF" in zip_info.filename:
                with zip_file.open(zip_info, mode="r") as file:
                    yield file
                break


@contextmanager
def open_umls_full(
    name: str, version: Optional[str] = None, *, api_key: Optional[str] = None, force: bool = False
):
    """Ensure and open a UMLS file from the given version.

    :param name: The name of the file, like ``MRSTY.RRF``
    :param version: The version of UMLS to ensure. If not given, is looked up
        with :mod:`bioversions`.
    :param api_key: An API key. If not given, is looked up using
        :func:`pystow.get_config` with the ``umls`` module and ``api_key`` key.
    :param force: Should the file be re-downloaded, even if it already exists?
    :yields: The file, which is used in the context manager.
    """
    path = download_umls_full(version=version, api_key=api_key, force=force)
    with zipfile.ZipFile(path) as zip_file:
        # In the 2023AB release, they added an intermediate META directory,
        # which means we have to go searching for the file by name
        for zip_info in zip_file.infolist():
            if name in zip_info.filename:
                with zip_file.open(zip_info, mode="r") as file:
                    yield file
                break


@contextmanager
def open_umls_semantic_types(
    version: Optional[str] = None, *, api_key: Optional[str] = None, force: bool = False
):
    """Ensure and open a UMLS file from the given version.

    :param version: The version of UMLS to ensure. If not given, is looked up
        with :mod:`bioversions`.
    :param api_key: An API key. If not given, is looked up using
        :func:`pystow.get_config` with the ``umls`` module and ``api_key`` key.
    :param force: Should the file be re-downloaded, even if it already exists?
    :yields: The file, which is used in the context manager.

    This file contains the following columns:

    ===   ========================================================================
    CUI   Unique identifier of concept
    TUI   Unique identifier of Semantic Type
    STN   Semantic Type tree number
    STY   Semantic Type. The valid values are defined in the Semantic Network.
    ATUI  Unique identifier for attribute
    CVF   Content View Flag. Bit field used to flag rows included in Content View.
    ===   ========================================================================

    .. seealso:: https://www.ncbi.nlm.nih.gov/books/NBK9685/table/ch03.Tf/
    """
    with open_umls_full(name="MRSTY.RRF", version=version, api_key=api_key, force=force) as file:
        yield file


@contextmanager
def open_umls_hierarchy(
    version: Optional[str] = None, *, api_key: Optional[str] = None, force: bool = False
):
    """Ensure and open a UMLS file from the given version.

    :param version: The version of UMLS to ensure. If not given, is looked up
        with :mod:`bioversions`.
    :param api_key: An API key. If not given, is looked up using
        :func:`pystow.get_config` with the ``umls`` module and ``api_key`` key.
    :param force: Should the file be re-downloaded, even if it already exists?
    :yields: The file, which is used in the context manager.

    This file contains the following columns:

    ===   ==========================================================================
    CUI   Unique identifier of concept
    AUI   Unique identifier of atom - variable length field, 8 or 9 characters
    CXN   Context number (e.g., 1, 2, 3)
    PAUI  Unique identifier of atom's immediate parent within this context
    SAB   Abbreviated source name (SAB) of the source of atom
    RELA  Relationship of atom to its immediate parent
    PTR   Path to the top or root of the hierarchical context from this atom.
    HCD   Source asserted hierarchical number or code for this atom in this context.
    CVF   Content View Flag. Bit field used to flag rows included in Content View.
    ===   ==========================================================================

    .. seealso:: https://www.ncbi.nlm.nih.gov/books/NBK9685/table/ch03.T.computable_hierarchies_file_mrhie
    """
    with open_umls_full(name="MRHIER.RRF", version=version, api_key=api_key, force=force) as file:
        yield file
