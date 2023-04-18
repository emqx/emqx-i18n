#!/usr/bin/env bash

set -euo pipefail

THIS_DIR="$(cd "$(dirname "$(readlink "$0" || echo "$0")")"; pwd -P)"

usage() {
    echo "Usage: $0 path/to/input path/to/output"
    echo "Or:    $0 https://url.to.file path/to/output"
}

input="${1:-}"
if [ -z "$input" ]; then
    usage
    exit 1
fi

output="${2:-}"
if [ -z "$output" ]; then
    usage
    exit 1
fi

if [ -z "${HOCON_IMAGE:-}" ]; then
    # build docker image
    cd "$THIS_DIR"/hocon-in-docker
    make
    cd -
    HOCON_IMAGE='hocon'
fi


if [ -f "$input" ]; then
    file="$(realpath "$input")"
    docker run --rm -it -v "$file":'/input' "$HOCON_IMAGE" to-json '/input' > "$output"
else
    docker run --rm -it "$HOCON_IMAGE" to-json "$input" > "$output"
fi
