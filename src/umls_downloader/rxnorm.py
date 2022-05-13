# -*- coding: utf-8 -*-

"""Download RxNorm content through the UMLS Terminology Services."""

from pathlib import Path
from typing import Optional

import pystow.utils

from .api import download_tgt_versioned

__all__ = [
    "download_rxnorm",
    "download_rxnorm_prescribable",
]

MODULE = pystow.module("bio", "rxnorm")
RXNORM_URL_FMT = "https://download.nlm.nih.gov/umls/kss/rxnorm/RxNorm_full_{version}.zip"


def _fix_rxnorm_version(rxnorm_version: str) -> str:
    if "-" not in rxnorm_version:
        return rxnorm_version
    year, month, day = rxnorm_version.split("-")
    return f"{month}{day}{year}"


def download_rxnorm(
    version: Optional[str] = None, *, api_key: Optional[str] = None, force: bool = False
) -> Path:
    """Ensure the given version of the RxNorm monthly file.

    :param version: The version of RxNorm to ensure. If not given, is looked up
        with :mod:`bioversions`.
    :param api_key: An API key. If not given, is looked up using
        :func:`pystow.get_config` with the ``umls`` module and ``api_key`` key.
    :param force: Should the file be re-downloaded, even if it already exists?
    :return: The path of the file for the given version of RxNorm.
    """
    return download_tgt_versioned(
        url_fmt=RXNORM_URL_FMT,
        version=version,
        api_key=api_key,
        force=force,
        version_key="rxnorm",
        module_key="rxnorm",
        version_transform=_fix_rxnorm_version,
    )


def download_rxnorm_prescribable(version: Optional[str] = None, *, force: bool = False) -> Path:
    """Ensure the given version of the RxNorm prescribable content file.

    :param version: The version of RxNorm to ensure. If not given, is looked up
        with :mod:`bioversions`.
    :param force: Should the file be re-downloaded, even if it already exists?
    :return: The path of the file for the given version of RxNorm.
    :raises RuntimeError: if no version is given and none can be looked up
    """
    if version is None:
        import bioversions

        version = bioversions.get_version("rxnorm")
    if version is None:
        raise RuntimeError("Could not get version for RxNorm")
    version = _fix_rxnorm_version(version)
    url = f"https://download.nlm.nih.gov/rxnorm/RxNorm_full_prescribe_{version}.zip"
    return MODULE.ensure(version, url=url, force=force)
