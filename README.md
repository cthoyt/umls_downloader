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
    <a href="https://github.com/cthoyt/cookiecutter-python-package">
        <img alt="Cookiecutter template from @cthoyt" src="https://img.shields.io/badge/Cookiecutter-python--package-yellow" /> 
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
    <a href='https://umls_downloader.readthedocs.io/en/latest/?badge=latest'>
        <img src='https://readthedocs.org/projects/umls_downloader/badge/?version=latest' alt='Documentation Status' />
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

## 👐 Contributing

Contributions, whether filing an issue, making a pull request, or forking, are
appreciated. See
[CONTRIBUTING.rst](https://github.com/cthoyt/umls_downloader/blob/master/CONTRIBUTING.rst)
for more information on getting involved.

## 👋 Attribution

### ⚖️ License

The code in this package is licensed under the MIT License.

<!--
### 📖 Citation

Citation goes here!
-->

<!--
### 🎁 Support

This project has been supported by the following organizations (in alphabetical order):

- [Harvard Program in Therapeutic Science - Laboratory of Systems Pharmacology](https://hits.harvard.edu/the-program/laboratory-of-systems-pharmacology/)

-->

<!--
### 💰 Funding

This project has been supported by the following grants:

| Funding Body                                             | Program                                                                                                                       | Grant           |
|----------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|-----------------|
| DARPA                                                    | [Automating Scientific Knowledge Extraction (ASKE)](https://www.darpa.mil/program/automating-scientific-knowledge-extraction) | HR00111990009   |
-->

### 🍪 Cookiecutter

This package was created
with [@audreyfeldroy](https://github.com/audreyfeldroy)'s
[cookiecutter](https://github.com/cookiecutter/cookiecutter) package
using [@cthoyt](https://github.com/cthoyt)'s
[cookiecutter-snekpack](https://github.com/cthoyt/cookiecutter-snekpack)
template.

## 🛠️ For Developers

<details>
  <summary>See developer instrutions</summary>


The final section of the README is for if you want to get involved by making a
code contribution.

### ❓ Testing

After cloning the repository and installing `tox` with `pip install tox`, the
unit tests in the `tests/` folder can be run reproducibly with:

```shell
$ tox
```

Additionally, these tests are automatically re-run with each commit in
a [GitHub Action](https://github.com/cthoyt/umls_downloader/actions?query=workflow%3ATests)
.

### 📦 Making a Release

After installing the package in development mode and installing
`tox` with `pip install tox`, the commands for making a new release are
contained within the `finish` environment in `tox.ini`. Run the following from
the shell:

```shell
$ tox -e finish
```

This script does the following:

1. Uses BumpVersion to switch the version number in the `setup.cfg` and
   `src/umls_downloader/version.py` to not have the `-dev` suffix
2. Packages the code in both a tar archive and a wheel
3. Uploads to PyPI using `twine`. Be sure to have a `.pypirc` file configured to
   avoid the need for manual input at this step
4. Push to GitHub. You'll need to make a release going with the commit where the
   version was bumped.
5. Bump the version to the next patch. If you made big changes and want to bump
   the version by minor, you can use `tox -e bumpversion minor` after.

</details>
