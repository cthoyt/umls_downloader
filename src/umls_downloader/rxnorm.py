from pathlib import Path
from typing import Optional

import pystow.utils
from pystow.utils import name_from_url

from .api import download_tgt_versioned

__all__ = [
    "download_rxnorm",
    "download_rxnorm_prescribable",
]

MODULE = pystow.module("bio", "rxnorm")


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
    url = f"https://download.nlm.nih.gov/umls/kss/rxnorm/RxNorm_full_{version}.zip"
    return download_tgt_versioned(
        url=url,
        version=version,
        api_key=api_key,
        force=force,
        version_key="rxnorm",
        module_key="rxnorm",
    )


def download_rxnorm_prescribable(version: Optional[str] = None, *, force: bool = False) -> Path:
    """Ensure the given version of the RxNorm prescribable content file.

    :param version: The version of RxNorm to ensure. If not given, is looked up
        with :mod:`bioversions`.
    :param force: Should the file be re-downloaded, even if it already exists?
    :return: The path of the file for the given version of RxNorm.
    """
    if version is None:
        import bioversions

        version = bioversions.get_version("rxnorm")
    url = f"https://download.nlm.nih.gov/rxnorm/RxNorm_full_prescribe_{version}.zip"
    return MODULE.ensure(version, url=url, name=name_from_url(url), force=force)
