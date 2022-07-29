from ursina import *
from Assets import *

SIZE = (3, 3)
HEIGHT = 16
CHUNK_THREADS = 4
SEED = 0

window.fullscreen = True
window.exit_button.visible = False
window.vsync = True

startPos = (0, 0, 0)

def input(key):
    if key == 'escape':
        exit()
    elif key == 'r':
        player.position = startPos

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

terrain = Terrain(terrainSize=SIZE, terrainHeight=HEIGHT, chunkThreads=CHUNK_THREADS, seed=SEED)

startPos = (0, len(terrain.chunks[0][0].blocks[0][0]), 0)
player.position = startPos

if __name__ == '__main__':
    app.run()