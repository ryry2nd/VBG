from ursina import *
from Assets import *

SIZE = (3, 3)
HEIGHT = 16
CHUNK_THREADS = 4
SEED = time.time()

window.fullscreen = True
window.exit_button.visible = False
window.vsync = True

startPos = (0, 0, 0)

def input(key):
    if key == 'escape':
        exit()
    elif key == 'r':
        player.position = startPos
        player.air_time = 0

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

xChunk = len(terrain.chunks)//2
yChunk = len(terrain.chunks[xChunk])//2
xBlock = len(terrain.chunks[xChunk][yChunk].blocks)//2
yBlock = len(terrain.chunks[xChunk][yChunk].blocks[xBlock])//2

startPos = (0, len(terrain.chunks[xChunk][yChunk].blocks[xBlock][yBlock]), 0)
player.position = startPos

if __name__ == '__main__':
    app.run()