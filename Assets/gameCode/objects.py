from perlin_noise import PerlinNoise
from ursina import *
from Assets.gameCode.vars import *
from Assets.gameCode.threadingWithRet import ThreadWRet
from queue import Queue

class Voxel(Button):
    def __init__(self, texture, position, truePos, chunk, model="Assets/models/block"):
        super().__init__(
        parent = scene,
        position = position,
        model = model,
        origin_y = 0.5,
        texture = texture,
        color = color.color(0, 0, 2),
        scale = 0.5,
        highlight_color = color.white
        )

        self.chunk = chunk
        self.truePos = truePos

    def place(self, pos):
        if player.selected == 1:
            Grass_block(pos)
        elif player.selected == 2:
            Dirt_block(pos)
        elif player.selected == 3:
            Stone_block(pos)
        elif player.selected == 4:
            Bedrock_block(pos)
    
    def breakBlock(self):
        x, z, y = self.truePos

        self.updateVisible()

        self.chunk[x][z][y] = None
        destroy(self)

    def input(self, key):
        if self.hovered and mouse.normal:
            pos = self.position + mouse.normal
            if distance(pos, player) < 7:
                if key == 'right mouse down':
                    self.place(pos)
                elif key == 'left mouse down':
                    self.breakBlock()

    def updateVisible(self):
        x, z, y = self.truePos

        maxX = len(self.chunk)-1
        maxZ = len(self.chunk[x])-1
        maxY = len(self.chunk[x][z])-1

        if x != maxX and y <= len(self.chunk[x+1][z])-1 and self.chunk[x+1][z][y]!= None:
            self.chunk[x+1][z][y].visible = True
            self.chunk[x+1][z][y].enabled = True
            self.chunk[x+1][z][y].parent = self.chunk
        if x != 0 and y <= len(self.chunk[x-1][z])-1 and self.chunk[x-1][z][y]!= None:
            self.chunk[x-1][z][y].visible = True
            self.chunk[x-1][z][y].enabled = True
            self.chunk[x-1][z][y].parent = self.chunk
        if z != maxZ and y <= len(self.chunk[x][z+1])-1 and self.chunk[x][z+1][y]!= None:
            self.chunk[x][z+1][y].visible = True
            self.chunk[x][z+1][y].enabled = True
            self.chunk[x][z+1][y].parent = self.chunk
        if z != 0 and y <= len(self.chunk[x][z-1])-1 and self.chunk[x][z-1][y]!= None:
            self.chunk[x][z-1][y].visible = True
            self.chunk[x][z-1][y].enabled = True
            self.chunk[x][z-1][y].parent = self.chunk
        if y != maxY and self.chunk[x][z][y+1]!= None:
            self.chunk[x][z][y+1].visible = True
            self.chunk[x][z][y+1].enabled = True
            self.chunk[x][z][y+1].parent = self.chunk
        if y != 0 and self.chunk[x][z][y-1]!= None:
            self.chunk[x][z][y-1].visible = True
            self.chunk[x][z][y-1].enabled = True
            self.chunk[x][z][y-1].parent = self.chunk

class Grass_block(Voxel):
    def __init__(self, position, truePos, chunk):
        super().__init__(grass_texture, position, truePos, chunk)

class Dirt_block(Voxel):
    def __init__(self, position, truePos, chunk):
        super().__init__(dirt_texture, position, truePos, chunk)

class Stone_block(Voxel):
    def __init__(self, position, truePos, chunk):
         super().__init__(stone_texture, position, truePos, chunk)

class Bedrock_block(Voxel):
    def __init__(self, position, truePos, chunk):
        super().__init__(bedrock_texture, position, truePos, chunk)

    def breakBlock(self):
        pass

class GameSky(Entity):
	def __init__(self):
    		super().__init__(
			parent = scene,
			model = "sphere",
			texture = sky_texture,
			scale = 10000,
			double_sided = True,
            collision = False
            )

class Chunk:
    blocks = []

    def __init__(self, position, height, noise, freq, amp):
        self.position = position
        self.height = height
        self.noise = noise
        self.freq = freq
        self.amp = amp
        self.generate_chunk()
        self.optimize()

    def generateZAxises(self, x, zPos, trueXPos):
        zAxises = []

        for z in range(zPos, zPos+16):
            zAxises.append([])
            ty = round(self.noise([x/self.freq,z/self.freq])*self.amp)
            maxY = ty+self.height
            for y in range(maxY):
                ry = (maxY)-y-1
                if ry == maxY-1:
                    zAxises[-1].append(Bedrock_block((x, y, z), None, self.blocks))
                    zAxises[-1][-1].truePos = (trueXPos, len(zAxises)-1, len(zAxises[-1])-1)
                elif ry > 2:
                    zAxises[-1].append(Stone_block((x, y, z), None, self.blocks))
                    zAxises[-1][-1].truePos = (trueXPos, len(zAxises)-1, len(zAxises[-1])-1)
                elif ry > 0:
                    zAxises[-1].append(Dirt_block((x, y, z), None, self.blocks))
                    zAxises[-1][-1].truePos = (trueXPos, len(zAxises)-1, len(zAxises[-1])-1)
                else:
                    zAxises[-1].append(Grass_block((x, y, z), None, self.blocks))
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
                    if not(
                        (y == maxY-1) or
                        (x != maxX-1 and y > len(self.blocks[x+1][z])-1) or
                        (x != 0 and y > len(self.blocks[x-1][z])-1) or
                        (z != maxZ-1 and y > len(self.blocks[x][z+1])-1) or
                        (z != 0 and y > len(self.blocks[x][z-1])-1)
                        ):

                        self.blocks[x][z][y].visible = False
                        self.blocks[x][z][y].enabled = False

class Terrain:
    chunks = []
    def __init__(self, terrainSize, terrainHeight=64, seed=time.time(), amp=6, freq=24, octaves=4, chunkThreads=2):
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
            self.chunks[trueX].insert(trueY, Chunk((x*16-16, z*16-16), self.tHeight, self.noise, self.freq, self.amp))
            q.task_done()

    def generateTerrain(self):
        jobs = Queue()

        for x in range(1, self.tLength+1):
            self.chunks.append([])
            for z in range(1, self.tWidth+1):
                self.chunks[-1].append(None)
                jobs.put((len(self.chunks)-1, len(self.chunks[-1])-1, x, z))
        
        for i in range(self.chunkThreads):
            t = ThreadWRet(target=self.loadChunkThread, args=(jobs, ))
            t.start()
        
        jobs.join()
            

__all__ = ["GameSky", "Terrain"]