#!/bin/bash

set -euo pipefail

cd "$(dirname "$0")/.."

DRYRUN="false"
REF=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --dryrun)
            DRYRUN="true"
            shift
            ;;
        --ref)
            REF="$2"
            shift 2
            ;;
        *)
            logerr "Unknown option: $1"
            exit 1
            ;;
    esac
done

loginfo() {
    echo -e "\033[32m$@\033[0m"
}

logerr() {
    echo -e "\033[31m$@\033[0m"
}

TR_FILE="tmp/desc.tr.hocon"

if [ ! -s "$TR_FILE" ]; then
    loginfo "Nothing to commit"
    exit 0
fi

# check if the new file is the same as the original file
if ! ./scripts/hocon.sh flatten "$TR_FILE" > /dev/null; then
    logerr "Error: $TR_FILE is not a valid hocon file"
    exit 1
fi

# parse the diff file to desc.zh.hocon format
./tr/parse-tr.py "$TR_FILE" > "$TR_FILE.parsed"

# merge the parsed diff into desc.zh.hocon
cat desc.zh.hocon "$TR_FILE.parsed" > "$TR_FILE.all"

# flatten the new file
./scripts/hocon.sh flatten "$TR_FILE.all" > desc.zh.hocon

if [ "$DRYRUN" = "true" ]; then
    loginfo "Dry run, not committing"
else
    git add desc.en.hocon
    git add desc.zh.hocon
    if git diff --quiet HEAD desc.en.hocon desc.zh.hocon; then
        loginfo "No changes to commit"
        exit 0
    fi
    compare_base_msg=""
    if [ -n "$REF" ]; then
        compare_base_msg=", translation compare base: ${REF}"
    fi
    git commit -m "docs: sync and update translations${compare_base_msg}"
fi
