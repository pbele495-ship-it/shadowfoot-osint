#!/data/data/com.termux/files/usr/bin/bash
set -e
cd "$(dirname "$0")"
python -c "import flask" >/dev/null 2>&1 || {
  echo "[!] Flask library is missing. Run: bash setup_android.sh"
  exit 1
}
echo "[✓] Starting ShadowFoot on this Android device..."
echo "Open Chrome: http://127.0.0.1:5000"
exec python app.py
