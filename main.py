import os
import logging
import random
from flask import Flask, request
from collections import namedtuple
from functools import cmp_to_key
import random


PlayerState = namedtuple('PlayerState', 'x y')
PlayerState.__eq__ = lambda source, target: source.x == target.x and source.y == target.y

DIRECTION_MAP = {
    "N":1,
    "E":2,
    "S":3,
    "W":4
}

def turn_left(vector: int):
    result = vector - 1
    if result < 0:
        result = 4
    return result

def turn_right(vector: int):
    result = vector + 1
    if result > 4:
        result = 1
    return result


def move_down(direction: str):
    moves = {
        "N":"R",
        "E":"R",
        "S":"F",
        "W":"L"
    }
    return moves.get(direction,"F")

def move_up(direction: str):
    moves = {
        "N":"F",
        "E":"L",
        "S":"R",
        "W":"R"
    }
    return moves.get(direction,"F")

def move_right(direction: str):
    moves = {
        "N":"R",
        "E":"F",
        "S":"L",
        "W":"R"
    }
    return moves.get(direction,"F")

def move_left(direction: str):
    moves = {
        "N":"L",
        "E":"R",
        "S":"R",
        "W":"F"
    }
    return moves.get(direction,"F")

def get_line(bot_state, vector):
    line = [PlayerState(1,1)] * 3
    if vector == 1:
        line[0] = PlayerState(bot_state.get("x"),bot_state.get("y") - 1)
        line[1] = PlayerState(bot_state.get("x"),bot_state.get("y") - 2)
        line[2] = PlayerState(bot_state.get("x"),bot_state.get("y") - 3)
    if vector == 2:
        line[0] = PlayerState(bot_state.get("x"),bot_state.get("y") + 1)
        line[1] = PlayerState(bot_state.get("x"),bot_state.get("y") + 2)
        line[2] = PlayerState(bot_state.get("x"),bot_state.get("y") + 3)
    if vector == 3:
        line[0] = PlayerState(bot_state.get("x") + 1,bot_state.get("y"))
        line[1] = PlayerState(bot_state.get("x") + 2,bot_state.get("y"))
        line[2] = PlayerState(bot_state.get("x") + 3,bot_state.get("y"))
    if vector == 4:
        line[0] = PlayerState(bot_state.get("x") - 1,bot_state.get("y"))
        line[1] = PlayerState(bot_state.get("x") - 2,bot_state.get("y"))
        line[2] = PlayerState(bot_state.get("x") - 3,bot_state.get("y"))
    return line
    


def find_bots_in_range(bot_state, arena, vector):
    line = get_line(bot_state, vector)
    n_line_bots = 0
    player_states = [PlayerState(player_state.get("x"),player_state.get("y")) for player_state in arena.get("arena").get("state").values()]
    for l in line:
        n_line_bots += len(list(filter(lambda player_state: player_state == l,player_states)))
    return n_line_bots

def find_closest_bot(bot_state, arena):
    def sort(player1 ,player2):
        d1 = abs(bot_state.get("x") - player1.x) + abs(bot_state.get("y") -  player1.y)
        d2 = abs(bot_state.get("x") - player2.x) + abs(bot_state.get("y") -  player2.y)
        if d1 < d2:
          return -1
        elif d1 > d2:
          return 1
        else:
          return 0

    player_states = [PlayerState(player_state.get("x"),player_state.get("y")) for player_state in arena.get("arena").get("state").values()]
    players = list(filter(lambda player: player != PlayerState(bot_state.get("x"), bot_state.get("y")),player_states))
    players.sort(key=cmp_to_key(sort))
    if len(players) > 0:
        return players[0]
    else:
        return random.choice(player_states)


    



def make_a_move(arena):
    bot = arena.get("_links").get("self").get("href")
    bot_state = arena.get("arena").get("state").get(bot)
    vector = DIRECTION_MAP.get(bot_state.get("direction"),1)
    result_cmd = "T"
    
    max_bots_in_range = 0
    bots_in_range = find_bots_in_range(bot_state, arena, vector)
    if max_bots_in_range < bots_in_range:
        max_bots_in_range = bots_in_range
    
    left_bots_in_range = find_bots_in_range(bot_state, arena, turn_left(vector))
    if max_bots_in_range < left_bots_in_range:
        max_bots_in_range = left_bots_in_range
    
    right_bots_in_range = find_bots_in_range(bot_state, arena, turn_right(vector))
    if max_bots_in_range < right_bots_in_range:
        max_bots_in_range = right_bots_in_range
    
    back_bots_in_range = find_bots_in_range(bot_state, arena, turn_left(turn_left(vector)))
    if max_bots_in_range < back_bots_in_range:
        max_bots_in_range = back_bots_in_range
    
    
    if max_bots_in_range >= 0:
        if max_bots_in_range == bots_in_range:
            result_cmd = "T"
        elif max_bots_in_range == left_bots_in_range:
            result_cmd = "L"
        elif max_bots_in_range == right_bots_in_range:
            result_cmd = "R"
        else:
            result_cmd = "L"
    
    
    else:
        close_bot = find_closest_bot(bot_state, arena)
        delta_x = bot_state.get("x") - close_bot.x
        delta_y = bot_state.get("y") - close_bot.y
        bot_direction = bot_state.get("direction")
        if delta_y == 0:
            if delta_x > 3:
                result_cmd = move_right(bot_direction)
            else:
                result_cmd = move_left(bot_direction)
        elif delta_x == 0:
            if delta_y > 3:
                result_cmd = move_down(bot_direction)
            else:
                result_cmd = move_up(bot_direction)
        elif delta_x < delta_y:
            if delta_x > 3:
                result_cmd = move_right(bot_direction)        
            else:
                result_cmd = move_left(bot_direction)
        else:
            if delta_y > 3:
                result_cmd = move_down(bot_direction)
            else:
                result_cmd = move_up(bot_direction)

    return result_cmd

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/", methods=['POST'])
def move():
    data = request.json
    bot_move = make_a_move(arena=data)
    

    return bot_move

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))