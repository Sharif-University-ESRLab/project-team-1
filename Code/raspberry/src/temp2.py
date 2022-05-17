import socketserver
from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

locations = [(1, 0), (4, 1), (4, 2), (8, 3), (12, 4)]

# todo
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.__parse_get_params()
        print(self.params)
        print(self.path)
        if self.path.startswith('/get-locations'):
            self.__send_locations()
        elif self.path.startswith('/get-speeds'):
            self.__send_speeds()
        elif self.path.startswith('/get-signs'):
            self.__send_signs()
        elif self.path.startswith('/speed-limits'):
            self.__send_speed_limits()
        else:
            assert 1 == 2

    def __parse_get_params(self):
        self.params = parse_qs(urlparse(self.path).query)

    def __send_locations(self):
        print('hi')
        timestamp = int(self.params['timestamp'][0])
        index = self.__find_timestamp_index(timestamp, locations)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(json.dumps(locations[index+1:len(locations)]).encode())
        # self.wfile.write('hello world!'.encode())

    def __send_speeds(self):
        pass

    def __send_signs(self):
        pass

    def __send_speed_limits(self):
        pass

    # Returns the index of the first cell with the timestamp greater or equal to TIMESTAMP in ARR
    def __find_timestamp_index(self, timestamp: int, arr: [tuple]):
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

    def log_message(self, format, *args):
        pass


def run_server(port):
    i = 0
    while True:
        try:
            httpd = socketserver.ThreadingTCPServer(("", port+i), MyHandler)
        except:
            i += 1
            continue
        break
    print(f'Server running on port {port+i}...')
    httpd.serve_forever()

run_server(8000)