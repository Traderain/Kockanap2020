
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
import game_state
import requests
import numpy as np
import cv2
import random
import math
from collections import defaultdict

def send_response(data, ip):
    print('Calculating response...')
    json_d = json.loads(data)
    preview_map(json_d)
    print('-- GAME STATE --')
    #print(json.dumps(json_d, indent=2))
    gs = game_state.GameState(json_d)
    for p in gs.perceptions:
        #print('\t' + p.to_string(gs.unit_ids))
        if p.item_id == 1:
            game_state.GameState.wall[p.pos_y][p.pos_x] = 1
    print('--- END GAME ---')
    print('Sending response')
    ret = gs.handle_response(ip)
    print('-- CURRENT LOOP DONE --')
    return ret

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        #logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        print('[Post request recieved]')
        length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(length)
        resp_data = send_response(post_data, 'http://' + self.client_address[0]).encode('utf-8')     
        self.send_response(200) #create header
        self.send_header("Content-Length", str(len(resp_data)))
        self.end_headers()
        self.wfile.write(resp_data)

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

def preview_map(json_data):    
    gamestate = game_state.GameState(json_data)
    mat = np.zeros((700, 1000, 3), dtype = "uint8")
    cv2.bitwise_not(mat, mat, mask=game_state.GameState.wall)
    for p in gamestate.perceptions:
        color = (0, 0, 0)
        if p.item_id == 1: # This is a wall
            color = (255, 255, 255)
        if p.item_id == 2:
            color = (255, 165, 0)
        if p.item_id == 2:
            color = (165, 42, 42)
        mat[p.pos_y, p.pos_x, :] = color
    for unit in gamestate.get_units():
        cv2.drawMarker(mat, (unit.pos_x, unit.pos_y), (0, 255, 0), markerType=cv2.MARKER_CROSS)
        cv2.putText(mat, str(unit.hp), (unit.pos_x, unit.pos_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        cv2.putText(mat, str(unit.ammo), (unit.pos_x, unit.pos_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
    for unit in gamestate.get_enemies():
        cv2.drawMarker(mat, (unit.pos_x, unit.pos_y), (255, 0, 0), markerType=cv2.MARKER_CROSS)
    for unit in gamestate.get_ammos():
        cv2.drawMarker(mat, (unit.pos_x, unit.pos_y), (255, 255, 0), markerType=cv2.MARKER_DIAMOND)
    for unit in gamestate.get_healths():
        cv2.drawMarker(mat, (unit.pos_x, unit.pos_y), (255, 0, 255), markerType=cv2.MARKER_DIAMOND)
    cv2.imshow('[OE Kockanap] - Perception preview', mat)
    cv2.waitKey(1)



MODE = 1 # 1 for server 2 for parsing json data

def main():
    if MODE == 1:
        print('---- STARTING Félévmentésch HTTP Server for kockanap ----')
        run(port=6971)
    elif MODE == 2:
        print('Loading json...')
        data = ''
        with open('.\\data\\example_json.json', 'r') as f:
            data = f.read()
        d = json.loads(data)
        preview_map(d)
    else:
        print('Unknown play mode! Error!')



if __name__ == '__main__':
    main()