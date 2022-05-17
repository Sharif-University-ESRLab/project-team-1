import socketserver
from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

from modules import lock as data_lock
from modules import locations, speeds, signs, speed_limits


# HTTP request handler class
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.__parse_get_params()
        if self.path.startswith('/get-locations'):
            self.__send_response(locations)
        elif self.path.startswith('/get-speeds'):
            self.__send_response(speeds)
        elif self.path.startswith('/get-signs'):
            self.__send_response(signs)
        elif self.path.startswith('/speed-limits'):
            self.__send_response(speed_limits)
        else:
            self.__send_400_response()

    def __parse_get_params(self):
        self.params = parse_qs(urlparse(self.path).query)

    def __send_response(self, arr):
        timestamp = int(self.params['timestamp'][0])
        data_lock.acquire()
        index = self.__find_timestamp_index(timestamp, arr)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(json.dumps(arr[index+1:len(arr)]).encode())
        data_lock.release()

    def __send_400_response(self):
        self.send_response(400)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    # Returns the index of the first cell with the timestamp greater or equal to TIMESTAMP in ARR
    def __find_timestamp_index(timestamp: int, arr: [tuple]):
        def bin_search(start, end):
            if start == end:
                return start
            mid = (start + end) // 2
            mid_timestamp = arr[mid][0]
            if mid_timestamp < timestamp:
                return bin_search(mid+1, end)
            else:
                return bin_search(start, mid)

        return bin_search(0, len(arr)-1)

    # todo: delete?
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
    def __get_post_params(self, raw_data):
        pdict = dict()
        for pair in raw_data.split('&'):
            index = pair.find('=')
            pdict[pair[0:index]] = pair[index+1:len(pair)]
        return pdict

    # todo: delete?
    def log_message(self, format, *args):
        pass


def run_server(port):
    httpd = socketserver.ThreadingTCPServer(("", port), MyHandler)
    print('Server running ...')
    httpd.serve_forever()
