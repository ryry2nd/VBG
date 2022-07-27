from ursina import *
from Assets import *

SIZE = (2, 2)
HEIGHT = 16
CHUNK_THREADS = 4
ROW_THREADS = 0

window.fullscreen = True
window.exit_button.visible = False
window.vsync = True

def input(key):
    if key == 'escape':
        exit()
    elif key == 'r':
        player.position = (0, 100, 0)

def update():
    global sky, player

    sky.position = player.position

    if held_keys['1']:
        player.selected = 1
    elif held_keys['2']:
        player.selected = 2
    elif held_keys['3']:
        player.selected = 3
    elif held_keys['4']:
        player.selected = 4

terrain = Terrain(terrainSize=SIZE, terrainHeight=HEIGHT, chunkThreads=CHUNK_THREADS)

if __name__ == '__main__':
    app.run()