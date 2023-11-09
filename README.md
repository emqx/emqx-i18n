# EMQX Config Documentation and Dashboard Internationalization

This repository contains multi-language translations for EMQX document generation and EMQX Dashboard.

EMQX Dashboard includes translations in JSON or HOCON format within the package.
This package is downloaded and built as part of EMQX's release package.


## Workflow

The primary language is English, which originates from [emqx.git](https://github.com/emqx/emqx).
Translations are stored in this repository.

To make changes, follow these steps:

1. Update English descriptions in the [upstream repository](https://github.com/emqx/emqx/tree/master/rel).
2. Periodically sync the updated English description file to this repository.
  - In `emqx` proejct, build the file with `make i18n`.
  - Copy the dumped file `_build/docgen/desc.en.hocon` to this repo.
  - Send a pull request for review.
3. Translators should review changes in the English version and apply corresponding updates to their translations.
4. Run `jq --sort-keys . desc.zh.hocon` to ensure the keys are sorted.
