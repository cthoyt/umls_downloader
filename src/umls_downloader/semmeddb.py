# -*- coding: utf-8 -*-

"""Download functionality for SemMedDB."""

from pathlib import Path
from typing import Optional

import pystow
from pystow.utils import name_from_url

from .api import download_tgt

__all__ = [
    "download_semmeddb_citations",
    "download_semmeddb_entity",
    "download_semmeddb_concept",
    "download_semmeddb_predication",
    "download_semmeddb_predication_aux",
    "download_semmeddb_sentence",
]

MODULE = pystow.module("bio", "semmeddb")

SEMMEDDB_VERSION = "43"
SEMMEDDB_BASE = "https://data.lhncbc.nlm.nih.gov/umls-restricted/ii/tools/SemRep_SemMedDB_SKR"
SEMMEDDB_CITATIONS = f"{SEMMEDDB_BASE}/semmedVER43_2021_R_CITATIONS.csv.gz"
SEMMEDDB_ENTITY = f"{SEMMEDDB_BASE}/semmedVER43_2021_R_ENTITY.csv.gz"
SEMMEDDB_CONCEPT = f"{SEMMEDDB_BASE}/semmedVER43_2021_R_GENERIC_CONCEPT.csv.gz"
SEMMEDDB_PREDICATION = f"{SEMMEDDB_BASE}/semmedVER43_2021_R_PREDICATION.csv.gz"
SEMMEDDB_PREDICATION_AUX = f"{SEMMEDDB_BASE}/semmedVER43_2021_R_PREDICATION_AUX.csv.gz"
SEMMEDDB_SENTENCE = f"{SEMMEDDB_BASE}/semmedVER43_2021_R_SENTENCE.csv.gz"


def download_semmeddb_citations(**kwargs) -> Path:
    """Download the SemMedDB citations file."""
    return _download_semmeddb_helper(SEMMEDDB_CITATIONS, **kwargs)


def download_semmeddb_entity(**kwargs) -> Path:
    """Download the SemMedDB entities file."""
    return _download_semmeddb_helper(SEMMEDDB_ENTITY, **kwargs)


def download_semmeddb_concept(**kwargs) -> Path:
    """Download the SemMedDB generic concepts file."""
    return _download_semmeddb_helper(SEMMEDDB_CONCEPT, **kwargs)


def download_semmeddb_predication(**kwargs) -> Path:
    """Download the SemMedDB predication file."""
    return _download_semmeddb_helper(SEMMEDDB_PREDICATION, **kwargs)


def download_semmeddb_predication_aux(**kwargs) -> Path:
    """Download the SemMedDB predication (aux) file."""
    return _download_semmeddb_helper(SEMMEDDB_PREDICATION_AUX, **kwargs)


def download_semmeddb_sentence(**kwargs) -> Path:
    """Download the SemMedDB sentence file."""
    return _download_semmeddb_helper(SEMMEDDB_SENTENCE, **kwargs)


def _download_semmeddb_helper(
    url: str, *, api_key: Optional[str] = None, force: bool = False
) -> Path:
    path = MODULE.join(SEMMEDDB_VERSION, name=name_from_url(url))
    if path.is_file() and not force:
        return path
    download_tgt(url, path, api_key=api_key)
    return path
