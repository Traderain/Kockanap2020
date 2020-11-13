
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
import game_state
import requests

def send_response(data, ip):
    print('Calculating response...')
    json_d = json.loads(data)
    print('-- GAME STATE --')
    #print(json.dumps(json_d, indent=2))
    gs = game_state.GameState(json_d)
    for p in gs.perceptions:
        print('\t' + p.to_string(gs.unit_ids))
    print('--- END GAME ---')
    print('Sending response')
    ret = gs.handle_response(ip)
    print('-- CURRENT LOOP DONE --')
    return ret

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
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        resp_data = send_response(post_data, 'http://' + self.client_address[0])        
        self.wfile.write(resp_data).encode('utf-8')

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        logging.info('Httpd server is up!')
        httpd.serve_forever()
    except KeyboardInterrupt:
        logging.error('Stopping server...')
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

def main():
    print('---- STARTING Félévmentésch HTTP Server for kockanap ----')
    run(port=6969)



if __name__ == '__main__':
    main()