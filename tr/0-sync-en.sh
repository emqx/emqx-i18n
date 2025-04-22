#! /bin/bash

set -euo pipefail

cd "$(dirname "$0")/.."

BRANCH="${1:-}"

if [ -z "$BRANCH" ]; then
    echo "Usage: $0 <emqx.git-branch-or-tag>"
    exit 1
fi

BUILDER='ghcr.io/emqx/emqx-builder/5.5-1:1.17.3-27.2-2-ubuntu24.04'

WORKDIR="tmp/emqx-$BRANCH"
trap 'rm -rf "$WORKDIR"' EXIT
mkdir -p "$WORKDIR"

git clone --depth 1 --branch "$BRANCH" https://github.com/emqx/emqx.git "$WORKDIR"

# concatenate all the .hocon files in $WORKDIR/rel/i18n/

TMP_FILE="tmp/docs.en.all.hocon"
# Find all .hocon files in rel/i18n/ and concatenate them
find "$WORKDIR/rel/i18n/" -name "*.hocon" -type f -exec cat {} + > "$TMP_FILE"

# Flatten the file
./scripts/hocon.sh flatten "$TMP_FILE" > desc.en.hocon
