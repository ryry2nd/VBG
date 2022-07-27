from ursina import *
from Assets import *
from Assets.gameCode.objects import Grass_block

SIZE = (1, 1)
HEIGHT = 3
CHUNK_THREADS = 4
ROW_THREADS = 4

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
Grass_block((1, 5, 0), (), None)

if __name__ == '__main__':
    app.run()