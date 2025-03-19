---
hide:
  - toc
---

# gcil

<!-- markdownlint-disable no-inline-html -->

[![Release](https://img.shields.io/pypi/v/gitlabci-local?color=blue)](https://pypi.org/project/gitlabci-local)
[![Python](https://img.shields.io/pypi/pyversions/gitlabci-local?color=blue)](https://pypi.org/project/gitlabci-local)
[![Downloads](https://img.shields.io/pypi/dm/gitlabci-local?color=blue)](https://pypi.org/project/gitlabci-local)
[![License](https://img.shields.io/gitlab/license/RadianDevCore/tools/gcil?color=blue)](https://gitlab.com/RadianDevCore/tools/gcil/-/blob/main/LICENSE)
<br />
[![Build](https://gitlab.com/RadianDevCore/tools/gcil/badges/main/pipeline.svg)](https://gitlab.com/RadianDevCore/tools/gcil/-/commits/main/)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=RadianDevCore_gcil&metric=bugs)](https://sonarcloud.io/dashboard?id=RadianDevCore_gcil)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=RadianDevCore_gcil&metric=code_smells)](https://sonarcloud.io/dashboard?id=RadianDevCore_gcil)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=RadianDevCore_gcil&metric=coverage)](https://sonarcloud.io/dashboard?id=RadianDevCore_gcil)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=RadianDevCore_gcil&metric=ncloc)](https://sonarcloud.io/dashboard?id=RadianDevCore_gcil)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=RadianDevCore_gcil&metric=alert_status)](https://sonarcloud.io/dashboard?id=RadianDevCore_gcil)
<br />
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Commitizen friendly](https://img.shields.io/badge/commitizen-friendly-brightgreen.svg)](https://commitizen-tools.github.io/commitizen/)
[![gcil](https://img.shields.io/badge/gcil-enabled-brightgreen?logo=gitlab)](https://radiandevcore.gitlab.io/tools/gcil)
[![pre-commit-crocodile](https://img.shields.io/badge/pre--commit--crocodile-enabled-brightgreen?logo=gitlab)](https://radiandevcore.gitlab.io/tools/pre-commit-crocodile)

Launch .gitlab-ci.yml jobs locally, wrapped inside the specific images,  
with inplace project volume mounts and adaptive user selections.

---

## Deprecated features

- Since version `11.0.0`, the following `.local:` configurations are deprecated:
    - `.local: network`: Use `CI_LOCAL_NETWORK` variable globally or per job, [documented in issue #286](https://gitlab.com/RadianDevCore/tools/gcil/-/issues/286)

- Versions before `10.0.0` were named `gitlabci-local` and not `gcil` yet,  
  the tool's backwards compatibility remains, however settings have changed too,  
  use the `--settings` parameter to see the file and redo your changes

- Versions before `4.6.0` used the now deprecated `PyInquirer` dependency,  
  and due to its own old dependency to the `prompt-toolkit` package,  
  you shoud uninstall both packages first before updating
