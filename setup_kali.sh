#!/usr/bin/env bash
set -e

echo "========================================"
echo " ShadowFoot OSINT - Kali Linux"
echo "========================================"

if ! command -v python3 >/dev/null 2>&1; then
  echo "[!] Python 3 is not installed. Install it using your distro package manager."
  exit 1
fi

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -c "import flask; print('Flask import OK')"

echo
echo "[✓] Setup complete. Run: bash run_kali.sh"
