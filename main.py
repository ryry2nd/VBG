from ursina import *
from Assets import *
import time

window.fullscreen = True
window.exit_button.visible = False
seed = time.time()

def input(key):
    if key == 'escape':
        exit()

def update():
    global sky, player

    sky.position = player.position

    if held_keys['1']:
        player.selected = 1
    elif held_keys['2']:
        player.selected = 2
    elif held_keys['3']:
        player.selected = 3

Terrain((1, 1, 4), seed)

if __name__ == '__main__':
    app.run()