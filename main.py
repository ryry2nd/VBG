from ursina import *
from Assets import *

SIZE = (3, 3)
HEIGHT = 16
CHUNK_THREADS = 4
SEED = random.randint(0, 1000000000000000000000000000)

window.fullscreen = True
window.exit_button.visible = False
window.vsync = True
window.title = 'Voxel Based Block Game'

terrain = Terrain(terrainSize=SIZE, terrainHeight=HEIGHT, chunkThreads=CHUNK_THREADS, seed=SEED)

xChunk = len(terrain.chunks)//2
yChunk = len(terrain.chunks[xChunk])//2
xBlock = len(terrain.chunks[xChunk][yChunk].blocks)//2
yBlock = len(terrain.chunks[xChunk][yChunk].blocks[xBlock])//2

player.startPos.y = len(terrain.chunks[xChunk][yChunk].blocks[xBlock][yBlock])
player.position = player.startPos

if __name__ == '__main__':
    app.run()