from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hello DevOps - Version 5")

server = HTTPServer(("0.0.0.0", 8080), Handler)
print("Server running on port 8080 - Version 5")
server.serve_forever()
