# -*- coding: utf-8 -*-

"""Automate downloading UMLS data."""

from .api import download_tgt, download_umls, open_umls  # noqa:F401
from .semmeddb import (  # noqa:F401
    download_semmeddb_citations,
    download_semmeddb_concept,
    download_semmeddb_entity,
    download_semmeddb_predication,
    download_semmeddb_predication_aux,
    download_semmeddb_sentence,
)
