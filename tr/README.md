# Scripts to translate from desc.en.hocon to desc.zh.hocon

This dir is a collection of scripts to help translate `desc.en.hocon` to `desc.zh.hocon`.

## Steps

- Run `0-sync-en.sh` to sync the en docs from emqx.git.
- Run `1-compare.sh` to run a 3-way compare between `desc.en.hocon`, `desc.zh.hocon` and `desc.base.hocon`.
  The diff is saved into `tmp/desc.diff.hocon`.
  The diff rules are:
  - If a doc changed from `desc.base.hocon` to `desc.en.hocon`, a comment `#NEED_TRANSLATION: CHANGED_SINCE <old_version>` is added,
    followed by the old version doc, the new version doc and the new version doc in zh.
  - If a doc is missing in `desc.zh.hocon`, a the doc content is added as `DOC_ID = NEED_TRANSLATION`.
- Run `2-translate.py` to translate the diff file.

- `2-translate.py` uses OpenAI Responses API and defaults to model `gpt-5.3-codex`. Model precedence is: `--model` > `OPENAI_MODEL` > default.
- Run `3-commit.sh` to concatenate the translated diff into `desc.zh.hocon`, then re-format the file and commit it into git.

## Automation

The steps can be run in one go in CI.

```
./tr/run.sh --emqx-ref <emqx.git-branch-or-tag> --compare-base <this-repo-translation-compare-base> [--model <openai-model>] [--dryrun]
```

Example:

```
./tr/run.sh --emqx-ref master --compare-base v5.9.0 --model gpt-5.3-codex
```
