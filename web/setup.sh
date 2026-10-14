#!/usr/bin/env bash
set -euo pipefail
project_root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$project_root"
python3 -m venv --system-site-packages web/.venv
web/.venv/bin/python -m pip install --cache-dir "$project_root/web/.cache/pip" -r web/requirements-dev.txt
cd web/frontend
npm --cache "$project_root/web/.cache/npm" ci --no-audit --no-fund
npm run build
