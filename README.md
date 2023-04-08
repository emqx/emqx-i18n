# EMQX Dashboard Internationalization

This repository contains multi-language translations for the EMQX Dashboard.

The translation files are currently in HOCON format, but they may be refactored to better suit available tooling.

EMQX Dashboard includes translations in JSON or HOCON format within the package.
This package is downloaded and built as part of EMQX's release package.


## Workflow

The primary language is English, which originates from [emqx.git](https://github.com/emqx/emqx).
Translations are stored in this repository.

To make changes, follow these steps:

1. Update English descriptions in the [upstream repository](https://github.com/emqx/emqx/tree/master/rel).
2. Periodically sync the updated English description files with this repository.
3. Translators should review changes in the English version and apply corresponding updates to their translations.

