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
from pathlib import Path
from typing import Optional

import click
from more_click import force_option, verbose_option

from umls_downloader import download_umls

from .api import download_tgt
from .rxnorm import download_rxnorm

__all__ = [
    "main",
]

logger = logging.getLogger(__name__)

api_option = click.option(
    "--api-key",
    help="The API key for the UMLS ticket granting system. If not given, uses pystow to load."
    " Get one at https://uts.nlm.nih.gov/uts/edit-profile.",
)

version_option = click.option(
    "--version",
    help="The version to download. If none specified, looks up the latest with bioversions",
)


@click.group()
def main():
    """Download files from the UMLS Terminology Service."""


@main.command()
@verbose_option
@api_option
@force_option
@click.option(
    "--url",
    help="The URL for a file to be downloaded through the UMLS ticket granting system.",
    required=True,
)
@click.option("-o", "--output", help="The local file path to download a file to", required=True)
def custom(url: str, output: str, api_key: Optional[str], force: bool):
    """Download a file via a custom URL."""
    path = Path(output).expanduser().resolve()
    download_tgt(url=url, path=path, api_key=api_key, force=force)
    click.secho(str(path))


@main.command()
@verbose_option
@version_option
@force_option
@api_option
def umls(version: Optional[str], force: bool, api_key: Optional[str]):
    """Download the UMLS data and print the path to stdout."""
    path = download_umls(api_key=api_key, force=force, version=version)
    click.secho(str(path))


@main.command()
@verbose_option
@version_option
@force_option
@api_option
def rxnorm(version: Optional[str], force: bool, api_key: Optional[str]):
    """Download the RxNorm data and print the path to stdout."""
    path = download_rxnorm(api_key=api_key, force=force, version=version)
    click.secho(str(path))


if __name__ == "__main__":
    main()
