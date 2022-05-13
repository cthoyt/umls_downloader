# -*- coding: utf-8 -*-

"""Automate downloading UMLS data."""

from .api import (  # noqa:F401
    download_tgt,
    download_tgt_versioned,
    download_umls,
    download_umls_metathesaurus,
    open_umls,
)
from .rxnorm import download_rxnorm, download_rxnorm_prescribable  # noqa:F401
from .semmeddb import (  # noqa:F401
    download_semmeddb_citations,
    download_semmeddb_concept,
    download_semmeddb_entity,
    download_semmeddb_predication,
    download_semmeddb_predication_aux,
    download_semmeddb_sentence,
)
