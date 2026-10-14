#!/usr/bin/env bash
set -euo pipefail
project_root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$project_root"
python_bin="${GRAUWASSER_PYTHON:-$project_root/web/.venv/bin/python}"
if [[ ! -x "$python_bin" ]]; then
  printf '%s\n' 'Zuerst bash web/setup.sh ausführen oder GRAUWASSER_PYTHON setzen.' >&2
  exit 1
fi
if [[ ! -f web/frontend/dist/index.html ]]; then
  printf '%s\n' 'Frontend fehlt. Zuerst bash web/setup.sh ausführen.' >&2
  exit 1
fi
exec "$python_bin" -m uvicorn web.backend.app:app --host "${GRAUWASSER_HOST:-0.0.0.0}" --port "${GRAUWASSER_PORT:-8000}"
