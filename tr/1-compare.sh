#!/bin/bash

set -euo pipefail

cd "$(dirname "$0")/.."

COMPARE_BASE="${1:-none}"

mkdir -p tmp

logwarn() {
    echo -e "\033[33m$1\033[0m" 1>&2
}

loginfo() {
    echo -e "\033[32m$1\033[0m" 1>&2
}

if [ "${COMPARE_BASE}" = "none" ]; then
    logwarn "No compare base provided, will not be able to detect the changes since the last commit"
    rm -f tmp/desc.en.hocon.base
else
    git show "${COMPARE_BASE}:desc.en.hocon" > tmp/desc.en.hocon.base
fi

# compare base may not have the file in flattened format
# so we need to flatten it just to make sure the comparison is correct
if [ -f tmp/desc.en.hocon.base ]; then
    ./scripts/hocon.sh flatten tmp/desc.en.hocon.base > tmp/desc.en.hocon.base.flat
fi

# delete the keys from desc.zh.hocon that are not found in desc.en.hocon
./tr/delete-stale-tr.py desc.en.hocon desc.zh.hocon > tmp/desc.zh.hocon
mv tmp/desc.zh.hocon desc.zh.hocon

./tr/do-compare.py desc.en.hocon desc.zh.hocon tmp/desc.en.hocon.base.flat $COMPARE_BASE > tmp/desc.diff.hocon

if [ -s tmp/desc.diff.hocon ]; then
    loginfo "Generated 'tmp/desc.diff.hocon' for review & translation."
    loginfo "You can now either manually review/translate it in-place,"
    loginfo "or run './tr/2-translate.py' to do the translation by ChatGPT."
    loginfo "After everything is done, run './tr/3-commit.sh'"
    loginfo "to write the fixed translations back to 'desc.zh.hocon' and commit it."
    if [ "${DEBUG:-}" = "true" ]; then
        echo "DEBUG: tmp/desc.diff.hocon:"
        cat tmp/desc.diff.hocon
    fi
else
    loginfo "All translations are up to date, no need to review and translate"
fi
