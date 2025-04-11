#!/usr/bin/env bash

set -euo pipefail

THIS_DIR="$(cd "$(dirname "$(readlink "$0" || echo "$0")")"; pwd -P)"

usage() {
    echo "Usage: $0 [COMMAND] path/to/input path/to/output"
    echo "Or:    $0 [COMMAND] https://url.to.file path/to/output"
    echo "COMMANDS:"
    echo "  to-json : Convert HOCON to JSON"
    echo "  flatten : Flatten the HOCON file"
}

command="${1:-}"
if [ -z "$command" ]; then
    echo "Error: Command is required"
    usage
    exit 1
fi

input="${2:-}"
if [ -z "$input" ]; then
    echo "Error: Input file is required"
    exit 1
fi

output="${3:-}"
if [ -z "$output" ]; then
    echo "Error: Output file is required"
    exit 1
fi

if [ -z "${HOCON_IMAGE:-}" ]; then
    # build docker image
    cd "$THIS_DIR"/hocon-in-docker
    make
    cd -
    HOCON_IMAGE='hocon'
fi

docker_run_opts=()
docker_input="$input"

if [ -f "$input" ]; then
    docker_run_opts+=("-v" "$(realpath "$input"):/input")
    docker_input="/input"
fi

case "$command" in
    "to-json")
        docker run --rm -it "${docker_run_opts[@]}" "$HOCON_IMAGE" do to-json "$docker_input" > "$output"
        ;;
    "flatten")
        docker run --rm -it "${docker_run_opts[@]}" "$HOCON_IMAGE" do flatten "$docker_input" > "$output"
        ;;
    *)
        usage
        exit 1
        ;;
esac
