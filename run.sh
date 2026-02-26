#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$HOME/to-doodle-ranch"
APP_FILE="app.py"
PYTHON_BIN="python3.11"

cd "$APP_DIR"

git fetch --all
git reset --hard origin/main

# Create venv if missing OR if it's not using Python 3.11
if [ ! -x ".venv/bin/python" ]; then
  "$PYTHON_BIN" -m venv .venv
else
  VENV_VER=$(.venv/bin/python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
  if [ "$VENV_VER" != "3.11" ]; then
    echo "Venv is Python $VENV_VER, rebuilding with $PYTHON_BIN..."
    rm -rf .venv
    "$PYTHON_BIN" -m venv .venv
  fi
fi

PY="$APP_DIR/.venv/bin/python"

"$PY" -m pip install -U pip
"$PY" -m pip install -r requirements.txt

# Stop previous process
pkill -f "$PY $APP_FILE" || true

nohup "$PY" "$APP_FILE" > log.txt 2>&1 &

echo "Started. Tail logs with: tail -n 200 -f $APP_DIR/log.txt"