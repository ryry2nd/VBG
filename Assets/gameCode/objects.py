from perlin_noise import PerlinNoise
from ursina import *
from threading import Thread
from Assets.gameCode.vars import *
from queue import Queue

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

class Terrain:
    def __init__(self, terrainSize, terrainHeight=64, seed=time.time(), amp=6, freq=24, octaves=4, chunkThreads=1):
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

    def generateZAxises(self, x, zPos, trueXPos):
        zAxises = []

        for z in range(zPos, zPos+16):
            zAxises.append([])
            ty = round(self.noise([x/self.freq,z/self.freq])*self.amp)
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

class Voxel:
    def __init__(self, position:tuple, texture:tuple, truePos:tuple, chunk:Chunk):
        self.position = position
        self.texture = texture

        self.top = None
        self.bottom = None
        self.left = None
        self.right = None
        self.front = None
        self.back = None

        self.chunk = chunk
        self.truePos = truePos

    def toggleTopFace(self):
        x, y, z = self.position
        if self.top == None:
            self.top = Face((x, y+0.5, z), Vec3(90, 0, 0), self.texture[0], self)
        else:
            destroy(self.top)
            self.top = None
    
    def toggleBottomFace(self):
        x, y, z = self.position
        if self.bottom == None:
            self.bottom = Face((x, y-0.5, z), Vec3(-90, 0, 0), self.texture[1], self)
        else:
            destroy(self.bottom)
            self.bottom = None
    
    def toggleLeftFace(self):
        x, y, z = self.position
        if self.left == None:
            self.left = Face((x+0.5, y, z), Vec3(0, -90, 0), self.texture[3], self)
        else:
            destroy(self.left)
            self.left = None
    
    def toggleRightFace(self):
        x, y, z = self.position
        if self.right == None:
            self.right = Face((x-0.5, y, z), Vec3(0, 90, 0), self.texture[2], self)
        else:
            destroy(self.right)
            self.right = None
    
    def toggleFrontFace(self):
        x, y, z = self.position
        if self.front == None:
            self.front = Face((x, y, z+0.5), Vec3(0, -180, 0), self.texture[4], self)
        else:
            destroy(self.front)
            self.front = None

    def toggleBackFace(self):
        x, y, z = self.position
        if self.back == None:
            self.back = Face((x, y, z-0.5), Vec3(0, 0, 0), self.texture[5], self)
        else:
            destroy(self.back)
            self.back = None
    
    def toggleAllFaces(self):
        self.toggleTopFace()
        self.toggleBottomFace()
        self.toggleLeftFace()
        self.toggleRightFace()
        self.toggleFrontFace()
        self.toggleBackFace()

    def updateVisible(self):
        x, z, y = self.truePos

        maxX = len(self.chunk.blocks)
        maxZ = len(self.chunk.blocks[x])
        maxY = len(self.chunk.blocks[x][z])

        if y != maxY-1 and self.chunk.blocks[x][z][y+1] != None:
            self.chunk.blocks[x][z][y+1].toggleBottomFace()
        if y != 0 and self.chunk.blocks[x][z][y-1]!= None:
            self.chunk.blocks[x][z][y-1].toggleTopFace()
        if x != maxX-1 and y <= len(self.chunk.blocks[x+1][z])-1 and self.chunk.blocks[x+1][z][y] != None:
            self.chunk.blocks[x+1][z][y].toggleRightFace()
        if x != 0 and y <= len(self.chunk.blocks[x-1][z])-1 and self.chunk.blocks[x-1][z][y] != None:
            self.chunk.blocks[x-1][z][y].toggleLeftFace()
        if z != maxZ-1 and y <= len(self.chunk.blocks[x][z+1])-1 and self.chunk.blocks[x][z+1][y] != None:
            self.chunk.blocks[x][z+1][y].toggleBackFace()
        if z != 0 and y <= len(self.chunk.blocks[x][z-1])-1 and self.chunk.blocks[x][z-1][y] != None:
            self.chunk.blocks[x][z-1][y].toggleFrontFace()

    def breakBlock(self):
        x, z, y = self.truePos

        self.updateVisible()

        self.chunk.blocks[x][z][y] = None

        destroy(self.top)
        destroy(self.bottom)
        destroy(self.left)
        destroy(self.right)
        destroy(self.front)
        destroy(self.back)
    
    def place(self, pos):
        x, y, z = (None, None, None)

        maxX, maxZ, maxY = len(self.chunk.blocks), len(self.chunk.blocks[x]), len(self.chunk.blocks[x][z])

        if x>maxX-1 and y>maxY-1 and z>maxZ-1 and self.chunk.blocks[x][z][y] == None:
            self.chunk.blocks[x][z].pop(y)

        if player.selected == 1:
            self.chunk.blocks[x][z].insert(y, Grass_block(pos, (x, z, y), self.chunk))
        elif player.selected == 2:
            self.chunk.blocks[x][z].insert(y, Dirt_block(pos, (x, z, y), self.chunk))
        elif player.selected == 3:
            self.chunk.blocks[x][z].insert(y, Stone_block(pos, (x, z, y), self.chunk))
        elif player.selected == 4:
            Bedrock_block(pos)
        
        self.chunk.blocks[x][z][y].toggleTopFace()
        
        maxX, maxZ, maxY = len(self.chunk.blocks), len(self.chunk.blocks[x]), len(self.chunk.blocks[x][z])

        if y != maxY-1 and self.chunk.blocks[x][z][y+1] != None:
            self.chunk.blocks[x][z][y+1].toggleBottomFace()
        if y != 0 and self.chunk.blocks[x][z][y-1]!= None:
            self.chunk.blocks[x][z][y-1].toggleTopFace()
        if x != maxX-1 and y <= len(self.chunk.blocks[x+1][z])-1 and self.chunk.blocks[x+1][z][y] != None:
            self.chunk.blocks[x+1][z][y].toggleRightFace()
        if x != 0 and y <= len(self.chunk.blocks[x-1][z])-1 and self.chunk.blocks[x-1][z][y] != None:
            self.chunk.blocks[x-1][z][y].toggleLeftFace()
        if z != maxZ-1 and y <= len(self.chunk.blocks[x][z+1])-1 and self.chunk.blocks[x][z+1][y] != None:
            self.chunk.blocks[x][z+1][y].toggleBackFace()
        if z != 0 and y <= len(self.chunk.blocks[x][z-1])-1 and self.chunk.blocks[x][z-1][y] != None:
            self.chunk.blocks[x][z-1][y].toggleFrontFace()

class Face(Button):
    def __init__(self, position, rotation, texture, block):
        self.block = block
        super().__init__(
        parent = scene,
        position = position,
        rotation = rotation,
        model = "quad",
        texture = texture,
        color = color.color(0, 0, 2),
        highlight_color = color.gray
        )

    def input(self, key):
        if self.hovered and mouse.normal:
            pos = self.position + mouse.normal
            if distance(pos, player) < 7:
                if key == 'right mouse down':
                    self.block.place(pos)
                elif key == 'left mouse down':
                    self.block.breakBlock()

class Grass_block(Voxel):
    def __init__(self, position, truePos, chunk):
        super().__init__(position, grass_texture, truePos, chunk)

class Dirt_block(Voxel):
    def __init__(self, position, truePos, chunk):
        super().__init__(position, dirt_texture, truePos, chunk)

class Stone_block(Voxel):
    def __init__(self, position, truePos, chunk):
         super().__init__(position, stone_texture, truePos, chunk)

class Bedrock_block(Voxel):
    def __init__(self, position, truePos, chunk):
        super().__init__(position, bedrock_texture, truePos, chunk)

    def breakBlock(self):
        pass

__all__ = ["GameSky", "Terrain"]