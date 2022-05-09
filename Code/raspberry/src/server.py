import socketserver
from http.server import BaseHTTPRequestHandler
import json


# welcome_html = open('./welcome.html', 'r').read()


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/hello':
            print('GET')
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(welcome_html.encode())

    def do_POST(self):
        if self.path == '/sum':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            data = self.rfile.read(
                int(self.headers['Content-length'])).decode('utf-8')
            pdict = self._get_post_params(data)
            num1 = int(pdict['num1'])
            num2 = int(pdict['num2'])
            print(pdict)
            self.wfile.write(json.dumps({'res': num1+num2}).encode())

    # todo: replace it something built-in?
    def _get_post_params(self, raw_data):
        pdict = dict()
        for pair in raw_data.split('&'):
            index = pair.find('=')
            pdict[pair[0:index]] = pair[index+1:len(pair)]
        return pdict

    def log_message(self, format, *args):
        pass


def run_server(port):
    httpd = socketserver.ThreadingTCPServer(("", port), MyHandler)
    print('Server running ...')
    httpd.serve_forever()
