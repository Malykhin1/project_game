from pynput import keyboard
from map import Map
import time
import os
from helicopter import Helicopter as helico
from clouds import Clouds
import json

TICK_SLEEP = 0.05
TREE_UPDATE = 50
CLOUDS_UPDATE = 150
FIRE_UPDATE = 100
MAP_W, MAP_H = 20, 20

tmp = Map(MAP_W, MAP_H)
clouds = Clouds(MAP_W, MAP_H)
helico = helico(MAP_W, MAP_H)
tick = 1

MOVES = {'w': (-1, 0), 'd': (0, 1), 's': (1, 0), 'a': (0, -1)}
def process_key(key):
    global helico, tick, clouds, tmp
    c = key.char
    if c in MOVES.keys():
        dx, dy = MOVES[c][0], MOVES[c][1]
        helico.move(dx, dy)
    elif c == 'f':
        data = {'helicopter': helico.export_data(), 
                'clouds': clouds.export_data(), 
                'tmp': tmp.export_data(),
                'tick': tick}
        with open('level.json', 'w') as lvl:
            json.dump(data, lvl)
    elif c == 'g':
        with open('level.json', 'r') as lvl:
            data = json.load(lvl)
            tick = data['tick'] or 1
            helico.import_data(data['helicopter']) 
            tmp.import_data(data['tmp'])
            clouds.import_data(data['clouds'])

    
listener = keyboard.Listener(
    on_press=None,
    on_release=process_key, )
listener.start()

while True:
    os.system('cls')
    tmp.process_helicopter(helico, clouds)
    helico.print_stats()
    tmp.print_map(helico, clouds)
    print('TICK', tick)
    tick += 1
    time.sleep(TICK_SLEEP)
    if (tick % TREE_UPDATE == 0):
        tmp.generate_tree()
    if (tick % FIRE_UPDATE == 0):
        tmp.update_fires()
    if (tick % CLOUDS_UPDATE == 0):
        clouds.update()
 