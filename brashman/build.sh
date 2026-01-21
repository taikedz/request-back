#!/usr/bin/env bash

THIS="$(realpath "$0")"
HEREDIR="$(dirname "$THIS")"
SCRIPT="$(basename "$0")"

set -euo pipefail

main() {
    name="$1"; shift

    cd "$HEREDIR"

    go build -trimpath -o "$name.exe" "$name.go"
}

main "$@"
