#!/usr/bin/env bash
set -euo pipefail
if [[ "${1:-}" == --help || "${1:-}" == -h ]]; then
    echo 'Usage: scripts/install-tools.sh [--native]'
    echo 'Install uv, PostgreSQL 17 and Mailpit with Homebrew; --native adds geckodriver.'
    echo 'Install Chrome and Firefox separately for native browser tests.'
    exit 0
fi
[[ $# -eq 0 || ( $# -eq 1 && "$1" == --native ) ]] || { echo 'Expected --native or no arguments.' >&2; exit 1; }
command -v brew >/dev/null 2>&1 || { echo 'Homebrew is required for this optional installer. Otherwise install uv, PostgreSQL 17 and Mailpit with your package manager.' >&2; exit 1; }
tools=(uv postgresql@17 mailpit)
if [[ "${1:-}" == --native ]]; then tools+=(geckodriver); fi
exec brew install "${tools[@]}"
