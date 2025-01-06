from http.server import BaseHTTPRequestHandler, HTTPServer

from log_parser import parse_log
from metrics_converter import MetricsConverter

ENCODING = "utf-8"
PORT = 9100


def start_server():
    web_server = HTTPServer(("", PORT), _RequestHandler)
    print(f"Server started http://localhost:{PORT}/metrics")
    web_server.serve_forever()


class _RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self._send_homepage()
        elif self.path == "/metrics":
            try:
                goaccess_metrics = parse_log()
                prometheus_metrics = MetricsConverter(goaccess_metrics).convert()
                self._send_metrics(prometheus_metrics)
            except Exception as error:
                self._send_error(500, "Internal Server Error", str(error))
        else:
            self._send_error(404, "Not Found", "Supported endpoint:<a href=\"/metrics\">/metrics</a>")

    def _send_homepage(self):
        title = "GoAccess Prometheus Exporter"
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(bytes(f"<html><head><title>{title}</title></head>", ENCODING))
        self.wfile.write(bytes("<body>", ENCODING))
        self.wfile.write(bytes(f"<h1>{title}</h1>", ENCODING))
        self.wfile.write(bytes(f'<a href="/metrics">Metrics</a>', ENCODING))
        self.wfile.write(bytes("</body></html>", ENCODING))

    def _send_metrics(self, metrics):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; version=0.0.4; charset=utf-8")
        self.end_headers()
        self.wfile.write(bytes(metrics, ENCODING))

    def _send_error(self, response_code, title, message):
        self.send_response(response_code)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(bytes(f"<html><head><title>{title}</title></head>", ENCODING))
        self.wfile.write(bytes("<body>", ENCODING))
        self.wfile.write(bytes(f"<h1>{title}</h1>", ENCODING))
        self.wfile.write(bytes(f"<p>{message}</p>", ENCODING))
        self.wfile.write(bytes("</body></html>", ENCODING))
