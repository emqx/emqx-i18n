#! /bin/bash

set -euo pipefail

cd "$(dirname "$0")/.."

# Default values
EMQX_REPO_BRANCH_OR_TAG=""
THIS_REPO_TRANSLATION_COMPARE_BASE=""
DRYRUN_OPT=""
MODEL_OPT=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --emqx-ref)
            EMQX_REPO_BRANCH_OR_TAG="$2"
            shift 2
            ;;
        --compare-base)
            THIS_REPO_TRANSLATION_COMPARE_BASE="$2"
            shift 2
            ;;
        --dryrun)
            DRYRUN_OPT="--dryrun"
            shift
            ;;
        --model)
            MODEL_OPT="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Check required arguments
if [ -z "$EMQX_REPO_BRANCH_OR_TAG" ] || [ -z "$THIS_REPO_TRANSLATION_COMPARE_BASE" ]; then
    echo "Usage: $0 --emqx-ref <emqx-ref> --compare-base <compare-base> [--model <openai-model>] [--dryrun]"
    exit 1
fi

./tr/0-sync-en.sh "${EMQX_REPO_BRANCH_OR_TAG}"
./tr/1-compare.sh "${THIS_REPO_TRANSLATION_COMPARE_BASE}"
if [ -n "${MODEL_OPT}" ]; then
    ./tr/2-translate.py --model "${MODEL_OPT}"
else
    ./tr/2-translate.py
fi
./tr/3-commit.sh --compare-base "${THIS_REPO_TRANSLATION_COMPARE_BASE}" ${DRYRUN_OPT}
