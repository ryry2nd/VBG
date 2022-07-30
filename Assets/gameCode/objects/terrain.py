from perlin_noise import PerlinNoise
from queue import Queue
from threading import Thread
from Assets.gameCode.objects.blocks import *
import time, random

class Terrain:
    def __init__(self, terrainSize, terrainHeight=64, seed=random.randint(0, 1000000000000000000000000000), amp=[6, 24], freq=[24, 48], octaves=4, chunkThreads=1):
        self.chunks = []
        self.tLength, self.tWidth = terrainSize
        self.tHeight = terrainHeight
        self.seed = seed
        self.amp = amp
        self.freq = freq
        self.octaves = octaves
        self.noise = PerlinNoise(octaves=octaves, seed=seed)
        self.chunkThreads = chunkThreads
        self.generateTerrain()

    def loadChunkThread(self, q:Queue):
        while not q.empty():
            trueX, trueY, x, z = q.get()
            self.chunks[trueX].insert(trueY, Chunk((x*16-(self.tLength*16)//2, z*16-(self.tLength*16)//2), (trueX, trueY), self.tHeight, self.noise, self.freq, self.amp))
            q.task_done()

    def generateTerrain(self):
        jobs = Queue()

        for x in range(self.tLength):
            self.chunks.append([])
            for z in range(self.tWidth):
                jobs.put((len(self.chunks)-1, len(self.chunks[-1])-1, x, z))
        
        if self.chunkThreads > 1 and self.tLength*self.tWidth > 1:
            for i in range(self.chunkThreads):
                t = Thread(target=self.loadChunkThread, args=(jobs, ))
                t.start()
            jobs.join()
        else:
            self.loadChunkThread(jobs)

class Chunk:
    def __init__(self, position, truePos, height, noise, freq, amp):
        self.blocks = []
        self.position = position
        self.truePos = truePos
        self.height = height
        self.noise = noise
        self.freq = freq
        self.amp = amp
        self.generate_chunk()
        self.optimize()
    
    def generateNoise(self, x, z):
        lowNoise = self.noise([x / self.freq[0], z / self.freq[0]]) * self.amp[0]
        highNoise = self.noise([x / self.freq[1], z / self.freq[1]]) * self.amp[1]

        return (lowNoise + highNoise) / 2

    def generateZAxises(self, x, zPos, trueXPos):
        zAxises = []

        for z in range(zPos, zPos+16):
            zAxises.append([])
            ty = round(self.generateNoise(x, z))
            maxY = ty+self.height

            zAxises[-1].append(Bedrock_block((x, 0, z), None, self))
            zAxises[-1][-1].truePos = (trueXPos, len(zAxises)-1, len(zAxises[-1])-1)

            for y in range(maxY):
                ry = (maxY)-y-1
                if ry == maxY-1:
                    pass
                elif ry > 2:
                    zAxises[-1].append(Stone_block((x, y, z), None, self))
                    zAxises[-1][-1].truePos = (trueXPos, len(zAxises)-1, len(zAxises[-1])-1)
                elif ry > 0:
                    zAxises[-1].append(Dirt_block((x, y, z), None, self))
                    zAxises[-1][-1].truePos = (trueXPos, len(zAxises)-1, len(zAxises[-1])-1)
                else:
                    zAxises[-1].append(Grass_block((x, y, z), None, self))
                    zAxises[-1][-1].truePos = (trueXPos, len(zAxises)-1, len(zAxises[-1])-1)
        return zAxises

    def generate_chunk(self):
        xPos, zPos = self.position
        idx = 0

        for x in range(xPos, xPos+16):
            self.blocks.append(self.generateZAxises(x, zPos, idx))
            idx += 1

    def optimize(self):
        maxX = len(self.blocks)
        for x in range(maxX):
            maxZ = len(self.blocks[x])
            for z in range(maxZ):
                maxY = len(self.blocks[x][z])
                for y in range(maxY):
                    if y == 0:
                        self.blocks[x][z][y].toggleBottomFace()
                    if y == maxY-1:
                        self.blocks[x][z][y].toggleTopFace()
                    if x != maxX-1 and len(self.blocks[x+1][z])-1 < y:
                        self.blocks[x][z][y].toggleLeftFace()
                    if x != 0 and len(self.blocks[x-1][z])-1 < y:
                        self.blocks[x][z][y].toggleRightFace()
                    if z != maxZ-1 and len(self.blocks[x][z+1])-1 < y:
                        self.blocks[x][z][y].toggleFrontFace()
                    if z != 0 and len(self.blocks[x][z-1])-1 < y:
                        self.blocks[x][z][y].toggleBackFace()

__all__ = ["Terrain", "Chunk"]