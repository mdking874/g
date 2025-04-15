from wingo_predictor import run_bot

if __name__ == "__main__":
    run_bot()
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

class Ping(BaseHTTPRequestHandler):
    def do_GET(self): self.send_response(200); self.end_headers()
threading.Thread(target=lambda: HTTPServer(('0.0.0.0', 8000), Ping).serve_forever(), daemon=True).start()
