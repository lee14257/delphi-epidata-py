# Delphi Epidata Python Client

[![License: MIT][mit-image]][mit-url] [![Github Actions][github-actions-image]][github-actions-url] [![PyPi][pypi-image]][pypi-url] [![Read the Docs][docs-image]][docs-url]

## Install

Install from PyPi:

```sh
pip install delphi-epidata
```

latest version

```sh
pip install -e "git+https://github.com/cmu-delphi/delphi-epidata-py.git#egg=delphi_epidata"
```

## Usage

TODO

## Development Environment

This project requires a recent version of gnu/make and docker or an installed Python version

### Local Python version

besides the docker variant a local Python instance can be used.

Prepare virtual environment and install dependencies

```sh
python -m venv venv
source ./venv/bin/activate
pip install --use-feature=2020-resolver -r requirements.txt -r requirements-dev.txt
```

### Common Commands

```sh
source ./venv/bin/activate
inv format   # format code
inv lint     # check linting
inv docs     # build docs
inv test     # run unit tests
inv coverage # run unit tests with coverage
inv clean    # clean build artifacts
inv dist     # build distribution packages
inv release  # upload the current version to pypi
```

## Release Process

The release consists of multiple steps which can be all done via the GitHub website:

1. Go to [create_release GitHub Action](https://github.com/cmu-delphi/delphi-epidata-py/actions/workflows/create_release.yml) and click the `Run workflow` button. Enter the next version number or one of the magic keywords (patch, minor, major) and hit the green `Run workflow` button.
1. The action will prepare a new release and will end up with a new [Pull Request](https://github.com/cmu-delphi/delphi-epidata-py/pulls)
1. Let the code owner review the PR and its changes and let the CI check whether everything builds successfully
1. Once approved and merged, another GitHub action job starts which automatically will
   1. create a git tag
   1. create another [Pull Request](https://github.com/cmu-delphi/delphi-epidata-py/pulls) to merge the changes back to the `dev` branch
   1. create a [GitHub release](https://github.com/cmu-delphi/delphi-epidata-py/releases) with automatically derived release notes
   1. create docker image and the production system will be notified to pull this update
1. Once the jobs are completed the new release should be available at https://delphi.cmu.edu within minutes.
1. Done

[mit-image]: https://img.shields.io/badge/License-MIT-yellow.svg
[mit-url]: https://opensource.org/licenses/MIT
[github-actions-image]: https://github.com/cmu-delphi/delphi-epidata-py/workflows/ci/badge.svg
[github-actions-url]: https://github.com/cmu-delphi/delphi-epidata-py/actions
[pypi-image]: https://pypip.in/version/delphi-epidata/badge.svg
[pypi-url]: https://pypi.python.org/pypi/delphi-epidata/
[docs-image]: https://readthedocs.org/projects/delphi-epidata/badge/?version=latest
[docs-url]: https://delphi-epidata.readthedocs.io/en/latest/?badge=latest
