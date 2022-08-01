from Assets import *
import random

SIZE = (3, 3)
HEIGHT = 16
CHUNK_THREADS = 4
SEED = random.randint(0, 1000000000000000000000000000)

terrain = Terrain(terrainSize=SIZE, terrainHeight=HEIGHT, chunkThreads=CHUNK_THREADS, seed=SEED)

player.startPos.y = len(terrain.chunks[SIZE[0]//2][SIZE[1]//2].blocks[8][8])
player.position = player.startPos

if __name__ == '__main__':
    app.run()