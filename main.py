import socket
from http.server import SimpleHTTPRequestHandler, HTTPServer

PORT = 8000

class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        elif self.path == '/message':
            self.path = '/message.html'
        elif self.path.startswith('/static/'):
            self.path = self.path
        else:
            self.path = '/error.html'

        return super().do_GET()

    def do_POST(self):
        if self.path == '/message':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('socket_server', 5000))
                s.sendall(post_data)

            self.send_response(302)  
            self.send_header('Location', '/')
            self.end_headers()

def run(server_class=HTTPServer, handler_class=MyHTTPRequestHandler):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    print(f'Starting HTTP server on port {PORT}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()