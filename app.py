from flask import Flask, render_template, request, jsonify, Response
from datetime import datetime, timezone
import csv, io, json, re, uuid

app = Flask(__name__)
SCANS = {}

def valid_target(target):
    target = (target or "").strip()
    if not target or len(target) > 253:
        return False
    # Accept domains, IPv4 addresses, and email addresses for a demo UI.
    domain = re.fullmatch(r"(?=.{1,253}$)(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)(?:\.(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?))+", target)
    ipv4 = re.fullmatch(r"(?:\d{1,3}\.){3}\d{1,3}", target)
    email = re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", target)
    return bool(domain or ipv4 or email)

def demo_events(target, scan_type):
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return [
        {"type":"SCAN_NOTE","severity":"info","data":"Demo mode enabled — no external lookups were performed.","source":"ShadowFoot demo engine","time":now},
        {"type":"TARGET","severity":"info","data":target,"source":"User input","time":now},
        {"type":"SCAN_PROFILE","severity":"info","data":scan_type.title(),"source":"Local configuration","time":now},
        {"type":"DOMAIN_METADATA","severity":"low","data":"Example metadata record (illustrative only)","source":"Sample dataset","time":now},
        {"type":"PUBLIC_CONTACT","severity":"medium","data":"No real contact data collected in demo mode","source":"Sample dataset","time":now},
    ]

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/api/health")
def health():
    return jsonify({"ok": True, "mode": "demo", "engine": "ShadowFoot standalone"})

@app.get("/api/scans")
def list_scans():
    return jsonify(sorted(SCANS.values(), key=lambda s: s["created"], reverse=True))

@app.post("/api/scans")
def create_scan():
    payload = request.get_json(silent=True) or {}
    target = str(payload.get("target", "")).strip()
    scan_type = str(payload.get("scanType", "passive")).lower()
    if not valid_target(target):
        return jsonify({"error": "Enter a valid domain, IPv4 address, or email address."}), 400
    if scan_type not in {"passive", "footprint", "investigate"}:
        return jsonify({"error": "Choose a supported demo scan profile."}), 400
    scan_id = uuid.uuid4().hex[:10].upper()
    scan = {
        "id": scan_id,
        "target": target,
        "scanType": scan_type,
        "status": "DEMO COMPLETE",
        "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "mode": "demo",
        "events": demo_events(target, scan_type)
    }
    SCANS[scan_id] = scan
    return jsonify(scan), 201

@app.get("/api/scans/<scan_id>")
def get_scan(scan_id):
    scan = SCANS.get(scan_id.upper())
    if not scan:
        return jsonify({"error": "Scan not found in this server session."}), 404
    return jsonify(scan)

@app.get("/api/scans/<scan_id>/export")
def export_scan(scan_id):
    scan = SCANS.get(scan_id.upper())
    if not scan:
        return jsonify({"error": "Scan not found."}), 404
    fmt = request.args.get("format", "json").lower()
    if fmt == "csv":
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=["type", "severity", "data", "source", "time"])
        writer.writeheader()
        writer.writerows(scan["events"])
        return Response(output.getvalue(), mimetype="text/csv",
                        headers={"Content-Disposition": f'attachment; filename="scan-{scan_id}.csv"'})
    return Response(json.dumps(scan, indent=2), mimetype="application/json",
                    headers={"Content-Disposition": f'attachment; filename="scan-{scan_id}.json"'})

if __name__ == "__main__":
    # Local-only by default; change host deliberately if you know your network setup.
    app.run(host="127.0.0.1", port=5000, debug=False)
