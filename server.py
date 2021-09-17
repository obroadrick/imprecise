from http.server import BaseHTTPRequestHandler, HTTPServer

port = 8000
def run_scheduler_tasks(schedule):
    schedule.run_tasks()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        message = "GET RESPONSE"
        self.wfile.write(bytes(message, "utf8"))

with HTTPServer(('', port), handler) as server:
    server.serve_forever()
