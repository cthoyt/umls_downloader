# -*- coding: utf-8 -*-

"""Command line interface for :mod:`umls_downloader`.

Why does this file exist, and why not put this in ``__main__``? You might be tempted to import things from ``__main__``
later, but that will cause problems--the code will get executed twice:

- When you run ``python3 -m umls_downloader`` python will execute``__main__.py`` as a script.
  That means there won't be any ``umls_downloader.__main__`` in ``sys.modules``.
- When you import __main__ it will get executed again (as a module) because
  there's no ``umls_downloader.__main__`` in ``sys.modules``.

.. seealso:: https://click.palletsprojects.com/en/7.x/setuptools/#setuptools-integration
"""

import logging
from typing import Optional

import click
from more_click import verbose_option

from .api import download_tgt, download_umls

__all__ = [
    "main",
]

logger = logging.getLogger(__name__)


@click.command()
@verbose_option
@click.option("--version")
@click.option("--url")
@click.option("--output")
def main(version: Optional[str], url: Optional[str], output: Optional[str]):
    """Download the given version of the UMLS or another UMLS-controlled
    resource via a custom URL."""
    if url and output:
        download_tgt(url=url, path=output)
    download_umls(version=version)


if __name__ == "__main__":
    main()
