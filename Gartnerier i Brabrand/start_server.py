#!/usr/bin/env python3
"""
Simple lokale webserver til at åbne Gartnerier i Brabrand
"""
import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

# Indstillinger
PORT = 8000
LOCALHOST = "127.0.0.1"

# Det aktuelle script-direktori (hvor index.html ligger)
current_dir = Path(__file__).parent
os.chdir(current_dir)

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Simpel HTTP handler"""
    def end_headers(self):
        # Tilføj cache-kontrol headers
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

# Start server
try:
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        url = f"http://{LOCALHOST}:{PORT}/index.html"
        print(f"🌍 Server kører på: {url}")
        print("Tryk Ctrl+C for at stoppe serveren")
        print()
        
        # Åbn automatisk i browser
        webbrowser.open(url)
        
        # Hold serveren kørende
        httpd.serve_forever()
        
except KeyboardInterrupt:
    print("\n✓ Server stoppet")
    sys.exit(0)
except OSError as e:
    print(f"❌ Fejl: {e}")
    print(f"Port {PORT} er måske allerede i brug. Prøv at lukkede andre programmer.")
    sys.exit(1)
