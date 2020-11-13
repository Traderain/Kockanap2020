import json
import requests
import random as rand

class GameState:
    team_id = -1
    perceptions = []
    unit_ids = []
    simple_movements = ["MoveN", "MoveS", "MoveE", "MoveW"]
    advanced_movements = ["MoveNW", "MoveNE", "MoveSW", "MoveSE"]
    all_movement_points = 50

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
            if p.item_id not in self.unit_ids and p.item_id > 10 and p.item_id < 200:
                ret.append(p)
        return ret

    def handle_response(self, url):
        res = Response(target=url)
        # TODO: Figure out what to send!
        units = self.get_units()
        move_actions = [res.simple_move, res.advanced_move]
        actions = [res.lie_down, res.crouch, res.stand_up, res.shoot]
        #while self.all_movement_points >= 2:
        for unit in units:
            idx = rand.randint(0, len(self.simple_movements) - 1)
            self.all_movement_points -= res.simple_move(unit.item_id, self.simple_movements[idx], self.all_movement_points)
            #idx = rand.randint(0, len(self.advanced_movements) - 1)
            #self.all_movement_points -= res.advanced_move(unit.item_id, self.advanced_movements[idx], self.all_movement_points)
            #for action in actions:
            #    self.all_movement_points -= action(unit.item_id, self.all_movement_points)
        return str(res.get_response_data()).encode('utf-8')


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
                return('[ENEMEY UNIT] @ X: ' + str(self.pos_x) + ' Y: ' + str(self.pos_y))
        else:
            return('[ERROR]  Something is wrong id:' + str(self.item_id))

class Response:
    url = ''

    commands = []

    def __init__(self, target):
        self.url = target

    def append_command(self, obj):
        self.commands.append(obj)

    def get_response_data(self):
        return json.dumps(self.commands)
    
    def calculate_cost(self, id, moveStr, all_movement_points, cost):
        if all_movement_points - cost >= 0:
            self.commands.append({"UnitId": id, "Action": moveStr})
            return cost
        return 0

    def simple_move(self, id, moveStr, all_movement_points):
        cost = 2
        return self.calculate_cost(id, moveStr, all_movement_points, cost)
    
    def advanced_move(self, id, moveStr, all_movement_points):
        cost = 3
        return self.calculate_cost(id, moveStr, all_movement_points, cost)
    
    def lie_down(self, id, all_movement_points):
        cost = 8
        return self.calculate_cost(id, "LieDown", all_movement_points, cost)
    
    def crouch(self, id, all_movement_points):
        cost = 4
        return self.calculate_cost(id, "Crouch", all_movement_points, cost)

    def stand_up(self, id, all_movement_points):
        cost = 4
        return self.calculate_cost(id, "StandUp", all_movement_points, cost)
    
    def shoot(self, id, all_movement_points):
        cost = 2
        return self.calculate_cost(id, "Shoot", all_movement_points, cost)
        
        
        




