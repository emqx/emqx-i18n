#!/usr/bin/env bash

set -euo pipefail

THIS_DIR="$(cd "$(dirname "$(readlink "$0" || echo "$0")")"; pwd -P)"

logerr() {
    echo "$@" >&2
}

usage() {
    logerr "Usage: $0 [COMMAND] path/to/input"
    logerr "Or:    $0 [COMMAND] https://url.to.file"
    logerr "COMMANDS:"
    logerr "  to-json : Convert HOCON to JSON"
    logerr "  flatten : Flatten the HOCON file"
}

command="${1:-}"
if [ -z "$command" ]; then
    logerr "Error: Command is required"
    usage
    exit 1
fi

input="${2:-}"
if [ -z "$input" ]; then
    logerr "Error: Input file is required"
    exit 1
fi

if [ -z "${HOCON_IMAGE:-}" ]; then
    # build docker image
    cd "$THIS_DIR"/hocon-in-docker
    make >/dev/null
    cd - >/dev/null
    HOCON_IMAGE='hocon'
fi

docker_run_opts=()

if [ -f "$input" ]; then
    input=$(realpath "$input")
    docker_run_opts+=("-v" "$input:$input")
fi

case "$command" in
    "to-json")
        docker run --rm "${docker_run_opts[@]}" "$HOCON_IMAGE" do to-json "$input"
        ;;
    "flatten")
        docker run --rm "${docker_run_opts[@]}" "$HOCON_IMAGE" do flatten "$input"
        ;;
    *)
        usage
        exit 1
        ;;
esac
