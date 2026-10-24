#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
if [ -f ".venv/bin/activate" ]; then
  source .venv/bin/activate
fi
python -c "import flask" >/dev/null 2>&1 || {
  echo "[!] Flask library is missing. Run: bash setup_kali.sh"
  exit 1
}
echo "[✓] Starting ShadowFoot..."
echo "Open browser: http://127.0.0.1:5000"
exec python app.py
