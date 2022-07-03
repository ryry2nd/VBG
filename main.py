from ursina import *
from Assets import *

def update():
    global sky, player

    sky.position = player.position
    
    if held_keys['1']:
        player.selected = 1
    if held_keys['2']:
        player.selected = 2

for z in range(20):
    for x in range(20):
        Grass_block((x, 0, z))

if __name__ == '__main__':
    app.run()