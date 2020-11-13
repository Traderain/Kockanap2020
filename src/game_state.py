import json
import requests

class GameState:
    team_id = -1
    perceptions = []
    unit_ids = []

    def __init__(self, jsondata):
        self.team_id = jsondata['you_are']
        self.unit_ids = jsondata['your_units']
        for perception in jsondata['you_see']:
            pos_x = perception['X']
            pos_y = perception['Y']
            item_id = perception['ItemId']
            self.perceptions.append(Item(pos_x, pos_y, item_id))
    
    def get_units(self):
        ret = []
        for p in self.perceptions:
            if p.item_id in self.unit_ids:
                ret.append(p)
        return ret

    def get_enemies(self):
        ret = []
        for p in self.perceptions:
            if p.item_id not in self.unit_ids:
                ret.append(p)
        return ret

    def handle_response(self, url):
        res = Response(target=url)
        # TODO: Figure out what to send!
        return res.get_response_data()


class Item:
    pos_x = 0
    pos_y = 0
    item_id = 0

    def __init__(self, x, y, id):
        self.pos_x = x
        self.pos_y = y
        self.item_id = id

    def to_string(self, unit_ids):
        if self.item_id == 1:
            return('[WALL] @ X: ' + str(self.pos_x) + ' Y: ' + str(self.pos_y))
        elif self.item_id == 2:
            return('[BONUS +5 AMMO] @ X: ' + str(self.pos_x) + ' Y: ' + str(self.pos_y))
        elif self.item_id == 3:
            return('[BONUS +10 HEALTH] @ X: ' + str(self.pos_x) + ' Y: ' + str(self.pos_y))
        elif self.item_id > 10 and self.item_id < 200:
            if self.item_id in unit_ids:
                return('[FRIENDLY UNIT] @ X: ' + str(self.pos_x) + ' Y: ' + str(self.pos_y))
            else:
                return('[ENEMEY UNIT] @ X: ' + str(self.pos_x) + ' Y: ' + str(elf.pos_y))
        else:
            return('[ERROR]  Something is wrong id:' + str(self.item_id))

class Response:
    url = 'https://www.youtube.com/watch?v=4yVHD2qvEEk'

    commands = []

    def __init__(self, target):
        self.url = target

    def append_command(self, obj):
        self.commands.append(obj)

    def get_response_data(self):
        return json.dumps(self.commands)
        
        
        




