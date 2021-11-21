<!--
<p align="center">
  <img src="https://github.com/cthoyt/umls_downloader/raw/main/docs/source/logo.png" height="150">
</p>
-->

<h1 align="center">
  UMLS Downloader
</h1>

<p align="center">
    <a href="https://github.com/cthoyt/umls_downloader/actions?query=workflow%3ATests">
        <img alt="Tests" src="https://github.com/cthoyt/umls_downloader/workflows/Tests/badge.svg" />
    </a>
    <a href="https://pypi.org/project/umls_downloader">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/umls_downloader" />
    </a>
    <a href="https://pypi.org/project/umls_downloader">
        <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/umls_downloader" />
    </a>
    <a href="https://github.com/cthoyt/umls_downloader/blob/main/LICENSE">
        <img alt="PyPI - License" src="https://img.shields.io/pypi/l/umls_downloader" />
    </a>
    <a href='https://github.com/psf/black'>
        <img src='https://img.shields.io/badge/code%20style-black-000000.svg' alt='Code style: black' />
    </a>
</p>

Don't worry about UMLS licensing and distribution rules - just use
`umls_downloader` to write code that knows how to download it and use it
automatically.

## Installation

```bash
$ pip install umls_downloader
```

## Download A Specific Version

```python
import os
from umls_downloader import download_umls

# Get this from https://uts.nlm.nih.gov/uts/edit-profile
api_key = ...

path = download_umls(version="2021AB", api_key=api_key)

# This is where it gets downloaded: ~/.data/bio/umls/2021AB/umls-2021AB-mrconso.zip
expected_path = os.path.join(
    os.path.expanduser("~"), ".data", "umls", "2021AB",
    "umls-2021AB-mrconso.zip",
)
assert expected_path == path.as_posix()
```

After it's been downloaded once, it's smart and doesn't need to download again.
It gets stored using [`pystow`](https://github.com/cthoyt/pystow) automatically
in the `~/.data/umls`
directory.

## Automating Configuration of UMLS Credentials

There are two ways to automatically set the username and password so you don't
have to worry about getting it and passing it around in your python code:

1. Set `UMLS_API_KEY` in the environment
2. Create `~/.config/umls.ini` and set in the `[umls]` section a `api_key` key.

```python
from umls_downloader import download_umls

# Same path as before
path = download_umls(version="2021AB")
```

## Download the Latest Version

First, you'll have to
install [`bioversions`](https://github.com/cthoyt/bioversions)
with `pip install bioversions`, whose job it is to look up the latest version of
many databases. Then, you can modify the previous code slightly by omitting
the `version` keyword argument:

```python
from umls_downloader import download_umls

# Same path as before (as of November 21st, 2021)
path = download_umls()
```

## Download and open the file

The UMLS file is zipped, so it's usually accompanied with the following
boilerplate code:

```python
import zipfile
from umls_downloader import download_umls
path = download_umls()
with zipfile.ZipFile(path) as zip_file:
    with zip_file.open("MRCONSO.RRF", mode="r") as file:
        for line in file:
            ...
```

This exact code is wrapped with the `open_umls()` using Python's context
manager so it can more simply be written as:

```python
from umls_downloader import open_umls

with open_umls() as file:
    for line in file:
        ...
```

The `version` and `api_key` arguments also apply here.

## Why not an API?

The UMLS provides an [API](https://documentation.uts.nlm.nih.gov/rest/home.html)
for access to tiny bits of data at a time. There are even two recent (last 5
years) packages [`umls-api`](https://pypi.org/project/umls-api)
[`connect-umls`](https://pypi.org/project/connect-umls) that provide a wrapper
around them. However, API access is generally rate limited, difficult to use in
bulk, and slow. For working with UMLS (or any other database, for that matter)in
bulk, it's necessary to download full database dumps.

## 👋 Attribution

### ⚖️ License

The code in this package is licensed under the MIT License.

### 🍪 Cookiecutter

This package was created
with [@audreyfeldroy](https://github.com/audreyfeldroy)'s
[cookiecutter](https://github.com/cookiecutter/cookiecutter) package
using [@cthoyt](https://github.com/cthoyt)'s
[cookiecutter-snekpack](https://github.com/cthoyt/cookiecutter-snekpack)
template.
