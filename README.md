# ShadowFoot OSINT Workbench

A standalone, mobile-responsive OSINT dashboard. This is a demo app inspired by OSINT workbenches, **not SpiderFoot**, and it does not perform external lookups. The scan endpoint creates clearly labeled sample events.

## Android / Termux setup

Extract the ZIP in Termux's Download folder, then:

```bash
cd ~/storage/downloads/shadowfoot_osint
bash setup_android.sh
bash run_android.sh
```

If `termux-setup-storage` has not been run yet, do that first and grant file access when prompted:

```bash
termux-setup-storage
```

Open Chrome on the same phone and visit:

`http://127.0.0.1:5000`

Keep Termux open while using the website. Stop the server with `Ctrl+C`.

If the folder name differs after unzipping, use `ls` and `cd` into the actual extracted folder.

## Kali Linux setup

```bash
cd shadowfoot_osint
bash setup_kali.sh
bash run_kali.sh
```

Then open `http://127.0.0.1:5000`.

## If installation still fails

Run this in the project folder and copy the full error output:

```bash
python -m pip install -r requirements.txt
python -c "import flask; print('Flask import OK')"
```

On Kali, use the included virtual environment setup (`bash setup_kali.sh`) rather than installing packages globally. On Termux, use `pkg install python` and `python -m pip`.

## Features
- Responsive dark cybersecurity dashboard
- Domain, IPv4 and email target input validation
- Demo profiles: Passive, Footprint, Investigate
- Sample results table and filter
- JSON and CSV export
- JSON API

## API
- `GET /api/health`
- `GET /api/scans`
- `POST /api/scans` with JSON `{"target":"example.com","scanType":"passive"}`
- `GET /api/scans/<SCAN_ID>`
- `GET /api/scans/<SCAN_ID>/export?format=json` (or `csv`)

## Important notes
- Scans are stored in memory and disappear when the server stops.
- The server binds to `127.0.0.1` by default, so it is accessible only on the local device.
- The app does not query DNS, websites, certificate transparency, WHOIS, IP reputation services, or SpiderFoot.
- Only investigate targets you own or have explicit permission to assess.
- Google Fonts are loaded from an external CDN. For offline UI, remove the `@import` line at the top of `static/style.css`.
