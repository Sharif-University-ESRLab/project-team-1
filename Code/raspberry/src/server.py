import socketserver
from http.server import BaseHTTPRequestHandler
import json


# todo
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/get-locations':
            self.__send_locations()
        elif self.path == '/get-speeds':
            self.__send_speeds()
        elif self.path == '/get-signs':
            self.__send_signs()
        elif self.path == '/speed-limits':
            self.__send_speed_limits()

    def __send_locations(self):
        pass

    def __send_speeds(self):
        pass

    def __send_signs(self):
        pass

    def __send_speed_limits(self):
        pass

    def do_POST(self):
        return
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
