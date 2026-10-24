#!/data/data/com.termux/files/usr/bin/bash
set -e

echo
echo "========================================"
echo " ShadowFoot OSINT - Android / Termux"
echo "========================================"
echo

if ! command -v pkg >/dev/null 2>&1; then
  echo "[!] Termux package manager not found."
  echo "    On Kali/Linux use: bash setup_kali.sh"
  exit 1
fi

echo "[1/4] Updating Termux packages..."
pkg update -y
pkg install -y python

echo "[2/4] Checking pip..."
python -m ensurepip --upgrade >/dev/null 2>&1 || true
python -m pip install --upgrade pip

echo "[3/4] Installing project dependencies..."
python -m pip install -r requirements.txt

echo "[4/4] Checking Flask import..."
python -c "import flask; print('Flask OK:', flask.__version__)"

echo
echo "[✓] Setup complete."
echo "Start the app with: bash run_android.sh"
