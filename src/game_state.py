import json
import requests
import random as rand
import numpy as np
import math
import cv2

class GameState:
    team_id = -1
    perceptions = []
    unit_ids = []
    simple_movements = ["MoveN", "MoveS", "MoveE", "MoveW"]
    advanced_movements = ["MoveNW", "MoveNE", "MoveSW", "MoveSE"]
    all_movement_points = 50
    max_ammo = 10
    max_hp = 10
    width = 700
    height = 1000
    wall = np.zeros((700, 1000, 1), dtype = "uint8")
    movement = np.zeros((700, 1000, 1), dtype = "uint8")
    movement_history = {}

    def __init__(self, jsondata):
        self.all_movement_points = GameState.all_movement_points
        self.perceptions = []
        self.team_id = jsondata['you_are']
        self.unit_ids = jsondata['your_units']
        for perception in jsondata['you_see']:
            pos_x = perception['X']
            pos_y = perception['Y']
            item_id = perception['ItemId']
            ammo = None
            hp = None
            for unitdata in jsondata['your_unitdatas']:
                if item_id == unitdata['UnitId']:
                    ammo = unitdata['Ammo']
                    hp = unitdata['HealthPoint']
            self.perceptions.append(Item(pos_x, pos_y, item_id, ammo, hp))
    
    def get_units(self):
        ret = []
        for p in self.perceptions:
            if p.item_id in self.unit_ids and not any([r.item_id == p.item_id for r in ret]):
                ret.append(p)
        return ret

    def get_enemies(self):
        ret = []
        for p in self.perceptions:
            if p.item_id not in self.unit_ids and p.item_id > 10 and p.item_id < 200 and not any([r.item_id == p.item_id for r in ret]):
                ret.append(p)
        return ret
    
    def get_ammos(self):
        ret = []
        for p in self.perceptions:
            if p.item_id == 2 and not any([r.pos_x == p.pos_x and r.pos_y == p.pos_y for r in ret]):
                ret.append(p)
        return ret
    
    def get_healths(self):
        ret = []
        for p in self.perceptions:
            if p.item_id == 3 and not any([r.pos_x == p.pos_x and r.pos_y == p.pos_y for r in ret]):
                ret.append(p)
        return ret

    def handle_response(self, url):
        res = Response(target=url, gamestate=self)
        # TODO: Figure out what to send!
        GameState.movement = np.zeros((GameState.width, GameState.height, 1), dtype = "uint8")
        units = self.get_units()
        if len(GameState.movement_history) == 0:
            for unit in units:
                GameState.movement_history[unit.item_id] = np.zeros((GameState.width, GameState.height, 1), dtype = "uint8")
        while self.all_movement_points >= 2:
            total_cost = 0
            for unit in units:
                #self.all_movement_points -= res.shoot_closest(unit, self.all_movement_points)
                cost = res.move_raytracing(unit, self.all_movement_points)
                total_cost += cost
                self.all_movement_points -= cost
            if total_cost == 0:
                break
                #if unit.ammo < GameState.max_hp - 5:
                #    self.all_movement_points -= res.pickup_health_closest(unit, self.all_movement_points)
                #if unit.ammo < GameState.max_ammo - 3:
                #    self.all_movement_points -= res.pickup_ammo_closest(unit, self.all_movement_points)
        return res.get_response_data()


class Item:
    pos_x = 0
    pos_y = 0
    item_id = 0
    ammo = 0
    hp = 0

    def __init__(self, x, y, id, ammo, hp):
        self.pos_x = x
        self.pos_y = y
        self.item_id = id
        self.ammo = ammo
        self.hp = hp

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

    def __init__(self, target, gamestate):
        self.commands = []
        self.url = target
        self.gamestate = gamestate

    def append_command(self, obj):
        self.commands.append(obj)

    def get_response_data(self):
        return json.dumps(self.commands)
    
    def calculate_cost(self, id, moveStr, all_movement_points, cost):
        if all_movement_points - cost >= 0:
            self.commands.append({"UnitId": int(id), "Action": moveStr})
            return cost
        return 0
    
    def get_distance(self, x1, y1, x2, y2):
        return math.sqrt((x1-x2)**2 + (y1-y2)**2)

    def get_closest(self, items, checked_item):
        min_dist = 99999
        min_item = None
        for item in items:
            dist = self.get_distance(item.pos_x, item.pos_y, checked_item.pos_x, checked_item.pos_y)
            if dist < min_dist:
                min_dist = dist
                min_item = item
        return min_item

    def move_to_closest_item(self, all_movement_points, item, closest_item):
        total_cost = 0
        if closest_item is not None:
            new_commands = []
            curr_pos_x = item.pos_x
            curr_pos_y = item.pos_y
            finished = False
            while not finished:
                finished = True
                if closest_item.pos_x > item.pos_x:
                    if closest_item.pos_x - curr_pos_x > -10:
                        total_cost += 2
                        new_commands.append({"UnitId": int(item.item_id), "Action": "MoveE"})
                        curr_pos_x += 10
                        finished = False
                else:
                    if curr_pos_x - closest_item.pos_x > -10:
                        total_cost += 2
                        new_commands.append({"UnitId": int(item.item_id), "Action": "MoveW"})
                        curr_pos_x -= 10
                        finished = False
                if closest_item.pos_y > item.pos_y:
                    if closest_item.pos_y - curr_pos_y > -10:
                        total_cost += 2
                        new_commands.append({"UnitId": int(item.item_id), "Action": "MoveS"})
                        curr_pos_y += 10
                        finished = False
                else:
                    if curr_pos_y - closest_item.pos_y > -10:
                        total_cost += 2
                        new_commands.append({"UnitId": int(item.item_id), "Action": "MoveN"})
                        curr_pos_y -= 10
                        finished = False
            if all_movement_points - total_cost > 0 and len(new_commands) > 0:
                self.commands.extend(new_commands)
                return total_cost
        return total_cost

    def simple_move(self, item, moveStr, all_movement_points):
        cost = 2
        return self.calculate_cost(item.item_id, moveStr, all_movement_points, cost)
    
    def advanced_move(self, item, moveStr, all_movement_points):
        cost = 3
        return self.calculate_cost(item.item_id, moveStr, all_movement_points, cost)
    
    def find_ray(self, x, y, x_modifier, y_modifier, item):
        while x > 0 and y > 0 and x < GameState.height - 1 and y < GameState.width - 1:
            off = False
            range_num = 3
            lower_x_range = -range_num
            upper_x_range = range_num
            lower_y_range = -range_num
            upper_y_range = range_num
            if x_modifier < 0:
                upper_x_range = 0
            if x_modifier > 0:
                lower_x_range = 0
            if y_modifier < 0:
                lower_y_range = 0
            if y_modifier > 0:
                upper_y_range = 0
            for i in range(lower_y_range, upper_y_range):
                for j in range(lower_x_range, upper_x_range):
                    if y + i >= 0 and x + j >= 0 and x + j < GameState.height and y + i < GameState.width and (GameState.wall[y + i][x + j] == 1 or GameState.movement[y + i][x + j] == 1):
                        off = True
                        break
                if off:
                    break
            if off:
                break
            x += x_modifier
            y += y_modifier
        return (x, y)

    def move_raytracing(self, item, all_movement_points):
        curr_pos_x = item.pos_x
        curr_pos_y = item.pos_y
        total_cost = 0
        moved_w = 0
        moved_e = 0
        moved_n = 0
        moved_s = 0
        while True:
            x = curr_pos_x
            y = curr_pos_y
            max_x, _ = self.find_ray(x, y, 1, 0, item)
            min_x, _ = self.find_ray(x, y, -1, 0, item)
            _, max_y = self.find_ray(x, y, 0, 1, item)
            _, min_y = self.find_ray(x, y, 0, -1, item)
            if min_x == max_x and min_y == max_y:
                return 0
            x_max_var = abs(max_x - x) if abs(max_x - x) > abs(x - min_x) else abs(x - min_x)
            y_max_var = abs(max_y - y) if abs(max_y - y) > abs(y - min_y) else abs(y - min_y)
            if all_movement_points - total_cost - 2 < 0:
                return total_cost
            if x_max_var > y_max_var:
                if abs(max_x - x) > abs(x - min_x):
                    total_cost += 2
                    new_command = {"UnitId": int(item.item_id), "Action": "MoveE"}
                    curr_pos_x += 10
                    moved_e += 10
                else:
                    total_cost += 2
                    new_command = {"UnitId": int(item.item_id), "Action": "MoveW"}
                    curr_pos_x -= 10
                    moved_w += 10
            else:
                if abs(max_y - y) > abs(y - min_y):
                    total_cost += 2
                    new_command = {"UnitId": int(item.item_id), "Action": "MoveS"}
                    curr_pos_y += 10
                    moved_s += 10
                else:
                    total_cost += 2
                    new_command = {"UnitId": int(item.item_id), "Action": "MoveN"}
                    curr_pos_y -= 10
                    moved_n += 10
            cv2.line(GameState.movement, (x, y), (curr_pos_x, curr_pos_y), 1, 1)
            cv2.line(GameState.movement_history[item.item_id], (x, y), (curr_pos_x, curr_pos_y), 1, 1)
            self.commands.append(new_command)
        return 0
    
    def lie_down(self, item, all_movement_points):
        cost = 8
        return self.calculate_cost(item.item_id, "LieDown", all_movement_points, cost)
    
    def crouch(self, item, all_movement_points):
        cost = 4
        return self.calculate_cost(item.item_id, "Crouch", all_movement_points, cost)

    def stand_up(self, item, all_movement_points):
        cost = 4
        return self.calculate_cost(item.item_id, "StandUp", all_movement_points, cost)
    
    def shoot_closest(self, item, all_movement_points):
        enemies = self.gamestate.get_enemies()
        closest_enemy = self.get_closest(enemies, item)
        if closest_enemy is not None:
            cost = 2
            if all_movement_points - cost >= 0:
                self.commands.append({"UnitId": int(item.item_id), "Action": "Shoot", "TargetId": closest_enemy.item_id})
                return cost
        return 0
    
    def pickup_health_closest(self, item, all_movement_points):
        healths = self.gamestate.get_healths()
        closest_health = self.get_closest(healths, item)
        return self.move_to_closest_item(all_movement_points, item, closest_health)
    
    def pickup_ammo_closest(self, item, all_movement_points):
        ammos = self.gamestate.get_ammos()
        closest_ammo = self.get_closest(ammos, item)
        return self.move_to_closest_item(all_movement_points, item, closest_ammo)
