<!-- General Information -->
[![License](https://img.shields.io/github/license/davidbrownell/uvRepoTemplate?color=dark-green)](https://github.com/davidbrownell/uvRepoTemplate/blob/master/LICENSE)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/9353/badge)](https://www.bestpractices.dev/projects/9353)

<!-- Package Information -->
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/uvRepoTemplate?color=dark-green)](https://pypi.org/project/uvRepoTemplate/)
[![PyPI - Version](https://img.shields.io/pypi/v/uvRepoTemplate?color=dark-green)](https://pypi.org/project/uvRepoTemplate/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/uvrepotemplate)](https://pypistats.org/packages/uvrepotemplate)

<!-- Development Information -->
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![CI](https://github.com/davidbrownell/UvRepoTemplate/actions/workflows/CI.yml/badge.svg)](https://github.com/davidbrownell/UvRepoTemplate/actions/workflows/CI.yml)
[![Code Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/davidbrownell/48391b195dedd43fcaa87d77130c3987/raw/UvRepoTemplate_code_coverage.json)](https://github.com/davidbrownell/uvRepoTemplate/actions)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/y/davidbrownell/uvRepoTemplate?color=dark-green)](https://github.com/davidbrownell/uvRepoTemplate/commits/main/)

## Contents
- [Overview](#overview)
- [Installation](#installation)
- [Development](#development)
- [Additional Information](#additional-information)
- [License](#license)

<a name="overview"></a>
## Overview
TODO: Complete this section

### How to use uvRepoTemplate
TODO: Complete this section

<a name="installation"></a>
## Installation

| Installation Method | Command |
| --- | --- |
| Via [uv](https://github.com/astral-sh/uv) | `uv add uvrepotemplate` |
| Via [pip](https://pip.pypa.io/en/stable/) | `pip install uvrepotemplate` |

### Verifying Signed Artifacts
Artifacts are signed and validated using [py-minisign](https://github.com/x13a/py-minisign) using the public key `\nRWREcaTucMl3IhymqTtoRV4joxXzNf71yqGWnU+/BL9MTAYQIKgOfkpM`.

To verify that an artifact is valid, visit [the latest releases](https://github.com/gt-sse-center/RepoAuditor/releases/latest) and download the `.minisign` signature file that corresponds to the artifact. Then run the following command, replacing `<filename>` with the name of the artifact to be verified:

`uv run --with py-minisign python -c "import minisign; minisign.PublicKey.from_bytes(b'\nRWREcaTucMl3IhymqTtoRV4joxXzNf71yqGWnU+/BL9MTAYQIKgOfkpM').verify_file('<filename>')"`

<a name="development"></a>
## Development
Please visit [Contributing](https://github.com/davidbrownell/uvRepoTemplate/blob/main/CONTRIBUTING.md) and [Development](https://github.com/davidbrownell/uvRepoTemplate/blob/main/DEVELOPMENT.md) for information on contributing to this project.

<a name="additional-information"></a>
## Additional Information
Additional information can be found at these locations.

| Title | Document | Description |
| --- | --- | --- |
| Code of Conduct | [CODE_OF_CONDUCT.md](https://github.com/davidbrownell/uvRepoTemplate/blob/main/CODE_OF_CONDUCT.md) | Information about the norms, rules, and responsibilities we adhere to when participating in this open source community. |
| Contributing | [CONTRIBUTING.md](https://github.com/davidbrownell/uvRepoTemplate/blob/main/CONTRIBUTING.md) | BugBug |
| Development | [DEVELOPMENT.md](https://github.com/davidbrownell/uvRepoTemplate/blob/main/DEVELOPMENT.md) | Information about development activities involved in making changes to this project. |
| Governance | [GOVERNANCE.md](https://github.com/davidbrownell/uvRepoTemplate/blob/main/GOVERNANCE.md) | Information about how this project is governed. |
| Maintainers | [MAINTAINERS.md](https://github.com/davidbrownell/uvRepoTemplate/blob/main/MAINTAINERS.md) | Information about individuals who maintain this project. |
| Security | [SECURITY.md](https://github.com/davidbrownell/uvRepoTemplate/blob/main/SECURITY.md) | Information about how to privately report security issues associated with this project. |

<a name="license"></a>
## License
uvRepoTemplate is licensed under the <a href="https://choosealicense.com/licenses/mit/" target="_blank">MIT</a> license.
