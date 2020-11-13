
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
import requests

def use_recieved_data(data):
    print('Parsing game info...')
    return data

def send_response(data):
    print('Calculating response...')
    json_d = json.loads(data)
    print('-- GAME STATE --')
    print(json.dumps(json_d, indent=2))
    print('--- END GAME ---')
    print('Sending response')
    url = 'https://www.w3schools.com/python/demopage.php'
    myobj = {'somekey': 'somevalue'}
    x = requests.post(url, data = myobj)
    print('-- CURRENT LOOP DONE --')

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        #logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        print('[Post request recieved]')
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
       # logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
        #        str(self.path), str(self.headers), post_data.decode('utf-8'))
        #jsondata = post_data.decode('utf-8')
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        send_response(post_data)        

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

def main():
    print('---- STARTING Félévmentésch HTTP Server for kockanap ----')
    run(port=6969)



if __name__ == '__main__':
    main()