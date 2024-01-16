# EMQX Config Documentation and Dashboard Internationalization

This repository contains multi-language translations for EMQX document generation and EMQX Dashboard.

## How the files are used

- During EMQX build, it downloads the `desc.zh.hocon` file to dump `zh` flafor schema doc (which is then used to generate markdown docs).
  EMQX does NOT download `desc.en.hocon` because `en` being the source of truth always resides in [upstream repository](https://github.com/emqx/emqx/tree/master/rel).

- EMQX dashboard current builds their own dictionary, but will consider taking this repo as the source of truth in the future.

## Workflow

Assuming the content of `desc.en.hocon` is the most complete, two operations need to be performed:

1. Find the newly added fields in `desc.en.hocon`:

  ```bash
  ./scripts/tools.py diff > diff.json
  ```

2. Find the content to be translated. Some proper nouns that do not need to be translated are recorded in the `./scripts/no-translate-dict.txt` file:

  ```bash
  ./scripts/tools.py UT > diff.json
  ```

3. Manually modify the `diff.json` file and translate the file into English.

4. Merge the translated fields with `desc.zh.hocon` and output to `desc.zh.hocon.new.json`:

  ```bash
  ./scripts/tools.py merge desc.zh.hocon diff.json > desc.zh.hocon.new.json
  ```

5. After checking for errors, copy the contents of `desc.zh.hocon.new.json` into `desc.zh.hocon`.

When necessary, also check whether there are untranslated fields in `desc.zh.hocon`:

  ```bash
  ./scripts/tools.py UT > diff.json
  ```

Manually translate the fields in `diff.json` and merge the translated fields with `desc.zh.hocon` according to step 4.

## Why named hocon while they are JSON

!!! DO NOT ATTEMPT to change naming convention of the files for below reasons:

1. HOCON is a super-set of JSON, so JSON IS technically also HOCON.
2. The `en` flavor files in upstream (emqx project) are HOCON format, and even after they are merged, it's just one HOCON file concatenated.
3. The file suffix `.hocon` is used by emqx when it tries to build the dictionary cache.

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

  - Copy the dumped file `_build/docgen/desc.en.hocon` to this repo.

  - Send a pull request for review.

- Translators should review changes in the English version and apply corresponding updates to their translations.

- Run `jq --sort-keys . desc.zh.hocon` to ensure the keys are sorted.
