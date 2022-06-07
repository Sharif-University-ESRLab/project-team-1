import socketserver
from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

from modules import lock as data_lock
from modules import locations, speeds, signs, speed_limits


# HTTP request handler class
class MyHandler(BaseHTTPRequestHandler):
    # Main request handler function
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

    # Parses GET request parameters.
    def __parse_get_params(self):
        self.params = parse_qs(urlparse(self.path).query)

    # Sends response to android app.
    def __send_response(self, arr):
        timestamp = int(self.params['timestamp'][0])
        data_lock.acquire()
        if timestamp == -1: # First request from android app will have TIMESTAMP equal to -1.
            index = -1
        else:   # Other requests will set TIMESTAMP equal to the timestamp of the last cell they have gotten.
            index = self.__find_timestamp_index(timestamp, arr)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(json.dumps(arr[index+1:len(arr)]).encode())
        data_lock.release()

    # Sends 400 bad request. It's used when url path is wrong.
    def __send_400_response(self):
        self.send_response(400)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    # Returns the index of the first cell with the timestamp greater or equal to TIMESTAMP in ARR.
    # Uses binary search algorithm for better performance.
    def __find_timestamp_index(timestamp: int, arr: [tuple]):
        # Will find TIMESTAMP in ARR using bin search.
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


# Start server on port number PORT
def run_server(port):
    httpd = socketserver.ThreadingTCPServer(("", port), MyHandler)
    print('Server running ...')
    httpd.serve_forever()
