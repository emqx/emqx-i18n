# EMQX Config Documentation and Dashboard Internationalization

This repository contains multi-language translations for EMQX document generation and EMQX Dashboard.

## How the files are used

- During EMQX build, it downloads the `desc.zh.hocon` file to dump `zh` flafor schema doc (which is then used to generate markdown docs).
  EMQX does NOT download `desc.en.hocon` because `en` being the source of truth always resides in [upstream repository](https://github.com/emqx/emqx/tree/master/rel).

- EMQX dashboard current builds their own dictionary, but will consider taking this repo as the source of truth in the future.

## Why named hocon while they are JSON

This is because older version EMQX may need to download the `.hocon` file.

## Branches

- main: EMQX before 5.3.2 downaloads from this branch
- v53: EMQX since 5.3.2 (before 5.4) downloads from this branch

## Workflow

The primary language is English, which originates from [emqx.git](https://github.com/emqx/emqx).
Translations are stored in this repository.

To make changes, follow these steps:

- Update English descriptions in the [upstream repository](https://github.com/emqx/emqx/tree/master/rel).

- Periodically sync the updated English description file to this repository.

  - In `emqx` proejct, build the file with `make i18n`.

  - Copy the dumped file `_build/docgen/desc.en.json` to this repo.

  - Send a pull request for review.

- Translators should review changes in the English version and apply corresponding updates to their translations.

- Run `jq --sort-keys . desc.zh.json` to ensure the keys are sorted.
