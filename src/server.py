import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

CONFIG_PATH = '/config/config.json'

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    return {"server_port": 8080, "debug_mode": False}

class MinimalWebserver(BaseHTTPRequestHandler):
    def do_GET(self):
        config = load_config()
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        
        response = {
            "status": "online",
            "message": "PlayniteNASync running from GitHub image.",
            "debug_enabled": config.get("debug_mode", False)
        }
        self.wfile.write(bytes(json.dumps(response), "utf-8"))

if __name__ == "__main__":
    config = load_config()
    port = config.get("server_port", 8080)
    server = HTTPServer(("0.0.0.0", port), MinimalWebserver)
    print(f"Starting webserver on port {port}...")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()