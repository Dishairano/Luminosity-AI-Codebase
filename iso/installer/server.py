#!/usr/bin/env python3
"""Luminosity Installer — lokale install-server.

Draait in de live-ISO als root. Serveert de installer-UI (web/) en biedt een
kleine API waarmee de UI de echte installatie aanstuurt:

    GET  /api/disks    -> lijst van schijven (lsblk)
    POST /api/install  -> start install.sh met de gekozen config; streamt
                          voortgang terug als Server-Sent Events (data: {...})
    POST /api/reboot   -> herstart de computer

Alleen bereikbaar op localhost; de kiosk-browser opent http://127.0.0.1:8723/.
Bewust klein gehouden: enkel de Python-stdlib, geen externe pakketten.
"""

import json
import os
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HIER = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(HIER, "web")
INSTALL_SH = os.path.join(HIER, "install.sh")
PORT = int(os.environ.get("LUM_INSTALLER_PORT", "8723"))

MIME = {".html": "text/html", ".css": "text/css", ".js": "application/javascript",
        ".svg": "image/svg+xml", ".png": "image/png", ".json": "application/json"}


def lijst_schijven():
    """Geeft de echte schijven terug via lsblk (alleen type 'disk')."""
    try:
        uit = subprocess.run(
            ["lsblk", "-dn", "-b", "-o", "NAME,SIZE,MODEL,TYPE"],
            capture_output=True, text=True, check=True).stdout
    except Exception:
        return []
    schijven = []
    for regel in uit.splitlines():
        velden = regel.split(None, 3)
        if len(velden) < 4 or velden[-1] != "disk":
            continue
        naam, bytes_, model = velden[0], int(velden[1]), (velden[2] if len(velden) > 3 else "")
        gb = bytes_ / 1e9
        grootte = f"{gb:.0f} GB" if gb >= 1 else f"{bytes_/1e6:.0f} MB"
        schijven.append({"name": naam, "size": grootte, "model": model.strip()})
    return schijven


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):  # stil
        pass

    def _send(self, code, body=b"", ctype="application/json"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if body:
            self.wfile.write(body if isinstance(body, bytes) else body.encode())

    def do_GET(self):
        pad = self.path.split("?", 1)[0]
        if pad == "/api/disks":
            self._send(200, json.dumps({"disks": lijst_schijven()}))
            return
        # statische bestanden
        rel = "index.html" if pad in ("/", "") else pad.lstrip("/")
        bestand = os.path.normpath(os.path.join(WEB, rel))
        if not bestand.startswith(WEB) or not os.path.isfile(bestand):
            self._send(404, b"not found", "text/plain")
            return
        ext = os.path.splitext(bestand)[1]
        with open(bestand, "rb") as f:
            self._send(200, f.read(), MIME.get(ext, "application/octet-stream"))

    def do_POST(self):
        if self.path == "/api/reboot":
            self._send(200, json.dumps({"ok": True}))
            subprocess.Popen(["systemctl", "reboot"])
            return
        if self.path != "/api/install":
            self._send(404, b"not found", "text/plain")
            return

        lengte = int(self.headers.get("Content-Length", "0"))
        try:
            cfg = json.loads(self.rfile.read(lengte) or "{}")
        except Exception:
            self._send(400, json.dumps({"error": "ongeldige config"}))
            return

        # Stream Server-Sent Events terug.
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self._run_install(cfg)

    def _event(self, obj):
        try:
            self.wfile.write(f"data: {json.dumps(obj, ensure_ascii=False)}\n".encode())
            self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            raise

    def _run_install(self, cfg):
        # install.sh leest de config als JSON op stdin en print regels:
        #   PROGRESS <pct>     -> voortgang
        #   <vrije tekst>      -> logregel
        #   DONE / ERROR <msg> -> einde
        proc = subprocess.Popen(
            ["bash", INSTALL_SH], stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        proc.stdin.write(json.dumps(cfg))
        proc.stdin.close()
        try:
            for regel in proc.stdout:
                regel = regel.rstrip("\n")
                if regel.startswith("PROGRESS "):
                    self._event({"type": "progress", "pct": float(regel.split()[1])})
                elif regel == "DONE":
                    self._event({"type": "done"})
                elif regel.startswith("ERROR "):
                    self._event({"type": "error", "msg": regel[6:]})
                elif regel:
                    self._event({"type": "log", "msg": regel})
        except (BrokenPipeError, ConnectionResetError):
            proc.kill()
            return
        proc.wait()


def main():
    os.chdir(HIER)
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Luminosity installer-server op http://127.0.0.1:{PORT}/", file=sys.stderr)
    srv.serve_forever()


if __name__ == "__main__":
    main()
