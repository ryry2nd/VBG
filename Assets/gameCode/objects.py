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
                jobs.put((len(self.chunks)-1, len(self.chunks[-1])-1, x, z))
        
        if self.chunkThreads > 1 and self.tLength*self.tWidth > 1:
            for i in range(self.chunkThreads):
                t = Thread(target=self.loadChunkThread, args=(jobs, ))
                t.start()
            jobs.join()
        else:
            self.loadChunkThread(jobs)

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
                    if y != 0:
                        self.blocks[x][z][y].bottom.visible = False
                        self.blocks[x][z][y].bottom.enabled = False
                    if y != maxY-1:
                        self.blocks[x][z][y].top.visible = False
                        self.blocks[x][z][y].top.enabled = False
                    if x != maxX-1 and len(self.blocks[x+1][z])-1 >= y:
                        self.blocks[x][z][y].left.visible = False
                        self.blocks[x][z][y].left.enabled = False
                    if x != 0 and len(self.blocks[x-1][z])-1 >= y:
                        self.blocks[x][z][y].right.visible = False
                        self.blocks[x][z][y].right.enabled = False
                    if z != maxZ-1 and len(self.blocks[x][z+1])-1 >= y:
                        self.blocks[x][z][y].front.visible = False
                        self.blocks[x][z][y].front.enabled = False
                    if z != 0 and len(self.blocks[x][z-1])-1 >= y:
                        self.blocks[x][z][y].back.visible = False
                        self.blocks[x][z][y].back.enabled = False

class Voxel:
    def __init__(self, position:tuple, texture:tuple, truePos:tuple, chunk:Chunk):
        self.position = position
        x, y, z = position

        self.top = Face((x, y+0.5, z), Vec3(90, 0, 0), texture[0], self)
        self.bottom = Face((x, y-0.5, z), Vec3(-90, 0, 0), texture[1], self)
        self.right = Face((x-0.5, y, z), Vec3(0, 90, 0), texture[2], self)
        self.left = Face((x+0.5, y, z), Vec3(0, -90, 0), texture[3], self)
        self.front = Face((x, y, z+0.5), Vec3(0, -180, 0), texture[4], self)
        self.back = Face((x, y, z-0.5), Vec3(0, 0, 0), texture[5], self)

        self.chunk = chunk
        self.truePos = truePos

    def updateVisible(self):
        x, z, y = self.truePos

        maxX = len(self.chunk.blocks)
        maxZ = len(self.chunk.blocks[x])
        maxY = len(self.chunk.blocks[x][z])

        if x < maxX and y <= len(self.chunk.blocks[x+1][z])-1 and self.chunk.blocks[x+1][z][y] != None:
            self.chunk.blocks[x+1][z][y].visible = True
            self.chunk.blocks[x+1][z][y].enabled = True
        if x > 0 and y <= len(self.chunk.blocks[x-1][z])-1 and self.chunk.blocks[x-1][z][y] != None:
            self.chunk.blocks[x-1][z][y].visible = True
            self.chunk.blocks[x-1][z][y].enabled = True
        if z < maxZ and y <= len(self.chunk.blocks[x][z+1])-1 and self.chunk.blocks[x][z+1][y] != None:
            self.chunk.blocks[x][z+1][y].visible = True
            self.chunk.blocks[x][z+1][y].enabled = True
        if z > 0 and y <= len(self.chunk.blocks[x][z-1])-1 and self.chunk.blocks[x][z-1][y] != None:
            self.chunk.blocks[x][z-1][y].visible = True
            self.chunk.blocks[x][z-1][y].enabled = True
        if y < maxY and self.chunk.blocks[x][z][y+1]!= None:
            self.chunk.blocks[x][z][y+1].visible = True
            self.chunk.blocks[x][z][y+1].enabled = True
        if y > 0 and self.chunk.blocks[x][z][y-1]!= None:
            self.chunk.blocks[x][z][y-1].visible = True
            self.chunk.blocks[x][z][y-1].enabled = True

    def breakBlock(self):
        x, z, y = self.truePos

        #self.updateVisible()

        self.chunk.blocks[x][z][y] = None

        destroy(self.top)
        destroy(self.bottom)
        destroy(self.left)
        destroy(self.right)
        destroy(self.front)
        destroy(self.back)

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
        highlight_color = color.white
        )

    def input(self, key):
        if self.hovered and mouse.normal:
            pos = self.position + mouse.normal
            if distance(pos, player) < 7:
                if key == 'right mouse down':
                    self.place(pos)
                elif key == 'left mouse down':
                    self.block.breakBlock()

    def place(self, pos):
        rp = pos-self.position
        rx, ry, rz = rp.x, rp.y, rp.z
        x, z, y = self.truePos
        
        nx, ny, nz = int(rx+x), int(ry+y), int(rz+z)

        maxX, maxY, maxZ = len(self.chunk.blocks)-1, len(self.chunk.blocks[nx])-1, len(self.chunk.blocks[nx][nz])-1

        if nx>maxX and ny>maxY and nz>maxZ and self.chunk.blocks[nx][nz][ny] == None:
            self.chunk.blocks[nx][nz].pop(ny)

        if player.selected == 1:
            self.chunk.blocks[nx][nz].insert(ny, Grass_block(pos, (nx, nz, ny), self.chunk))
        elif player.selected == 2:
            Dirt_block(pos)
        elif player.selected == 3:
            Stone_block(pos)
        elif player.selected == 4:
            Bedrock_block(pos)

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