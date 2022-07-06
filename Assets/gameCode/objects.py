from perlin_noise import PerlinNoise
from ursina import *
from Assets.gameCode.vars import *

class Voxel(Button):
    def __init__(self, texture, position, truePos, chunk, model="Assets/models/block"):
        super().__init__()
        self.parent = scene
        self.position = position
        self.truePos = truePos
        self.model = model
        self.origin_y = 0.5
        self.texture = texture
        self.color = color.color(0, 0, 2)
        self.scale = 0.5
        self.highlight_color = color.white
        self.chunk = chunk

    def input(self, key):
        if self.hovered:
            pos = self.position + mouse.normal
            if distance(pos, player) < 7:
                if key == 'right mouse down':
                    if player.selected == 1:
                        Grass_block(pos)
                    elif player.selected == 2:
                        Dirt_block(pos)
                    elif player.selected == 3:
                        Stone_block(pos)
                    elif player.selected == 4:
                        Bedrock_block(pos)
                elif key == 'left mouse down':
                    x, z, y = self.truePos

                    maxX = len(self.chunk.blocks)
                    maxZ = len(self.chunk.blocks[x])
                    maxY = len(self.chunk.blocks[x][z])

                    if x != maxX-1 and y <= len(self.chunk.blocks[x+1][z])-1 and self.chunk.blocks[x+1][z][y]!= None:
                        self.chunk.blocks[x+1][z][y].visible = True
                        self.chunk.blocks[x+1][z][y].enabled = True
                    if x != 0 and y <= len(self.chunk.blocks[x-1][z])-1 and self.chunk.blocks[x-1][z][y]!= None:
                        self.chunk.blocks[x-1][z][y].visible = True
                        self.chunk.blocks[x-1][z][y].enabled = True
                    if z != maxZ-1 and y <= len(self.chunk.blocks[x][z+1])-1 and self.chunk.blocks[x][z+1][y]!= None:
                        self.chunk.blocks[x][z+1][y].visible = True
                        self.chunk.blocks[x][z+1][y].enabled = True
                    if z != 0 and y <= len(self.chunk.blocks[x][z-1])-1 and self.chunk.blocks[x][z-1][y]!= None:
                        self.chunk.blocks[x][z-1][y].visible = True
                        self.chunk.blocks[x][z-1][y].enabled = True
                    if y != maxY-1 and self.chunk.blocks[x][z][y+1]!= None:
                        self.chunk.blocks[x][z][y+1].visible = True
                        self.chunk.blocks[x][z][y+1].enabled = True
                    if y != 0 and self.chunk.blocks[x][z][y-1]!= None:
                        self.chunk.blocks[x][z][y-1].visible = True
                        self.chunk.blocks[x][z][y-1].enabled = True

                    self.chunk.blocks[x][z][y] = None
                    destroy(self)

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

class GameSky(Entity):
	def __init__(self):
    		super().__init__(
			parent = scene,
			model = 'sphere',
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

    def generate_chunk(self):
        xPos, zPos = self.position

        for x in range(xPos, xPos+16):
            self.blocks.append([])
            for z in range(zPos, zPos+16):
                self.blocks[-1].append([])
                ty = round(self.noise([x/self.freq,z/self.freq])*self.amp)
                maxY = ty+self.height
                for y in range(maxY):
                    ry = (maxY)-y-1
                    if ry == maxY-1:
                        self.blocks[-1][-1].append(Bedrock_block((x, y, z), None, self))
                        self.blocks[-1][-1][-1].truePos = (len(self.blocks)-1, len(self.blocks[-1])-1, len(self.blocks[-1][-1])-1)
                    elif ry > 2:
                        self.blocks[-1][-1].append(Stone_block((x, y, z), None, self))
                        self.blocks[-1][-1][-1].truePos = (len(self.blocks)-1, len(self.blocks[-1])-1, len(self.blocks[-1][-1])-1)
                    elif ry > 0:
                        self.blocks[-1][-1].append(Dirt_block((x, y, z), None, self))
                        self.blocks[-1][-1][-1].truePos = (len(self.blocks)-1, len(self.blocks[-1])-1, len(self.blocks[-1][-1])-1)
                    else:
                        self.blocks[-1][-1].append(Grass_block((x, y, z), None, self))
                        self.blocks[-1][-1][-1].truePos = (len(self.blocks)-1, len(self.blocks[-1])-1, len(self.blocks[-1][-1])-1)
        
    def optimize(self):
        maxX = len(self.blocks)
        for x in range(maxX):
            maxZ = len(self.blocks[x])
            for z in range(maxZ):
                maxY = len(self.blocks[x][z])
                for y in range(maxY):
                    self.blocks[x][z][y].visible = False
                    self.blocks[x][z][y].enabled = False

                    if y == maxY-1:
                        self.blocks[x][z][y].visible = True
                        self.blocks[x][z][y].enabled = True
                    elif x != maxX-1 and y > len(self.blocks[x+1][z])-1:
                        self.blocks[x][z][y].visible = True
                        self.blocks[x][z][y].enabled = True
                    elif x != 0 and y > len(self.blocks[x-1][z])-1:
                        self.blocks[x][z][y].visible = True
                        self.blocks[x][z][y].enabled = True
                    elif z != maxZ-1 and y > len(self.blocks[x][z+1])-1:
                        self.blocks[x][z][y].visible = True
                        self.blocks[x][z][y].enabled = True
                    elif z != 0 and y > len(self.blocks[x][z-1])-1:
                        self.blocks[x][z][y].visible = True
                        self.blocks[x][z][y].enabled = True
                    elif x == 0 or z == 0:
                        self.blocks[x][z][y].visible = True
                        self.blocks[x][z][y].enabled = True
                    elif x == maxX-1 or z == maxZ-1:
                        self.blocks[x][z][y].visible = True
                        self.blocks[x][z][y].enabled = True
    
class Terrain:
    chunks = []
    def __init__(self, terrainSize, seed=time.time(), amp=6, freq=24, octaves=4):
        self.tLength, self.tWidth, self.tHeight = terrainSize
        self.seed = seed
        self.amp = amp
        self.freq = freq
        self.octaves = octaves
        self.noise = PerlinNoise(octaves=octaves, seed=seed)
        self.generateTerrain()

    def generateTerrain(self):
        for x in range(1, self.tLength+1):
            self.chunks.append([])
            for z in range(1, self.tWidth+1):
                self.chunks[-1].append(Chunk((x*16-16, z*16-16), self.tHeight, self.noise, self.freq, self.amp))

__all__ = ["GameSky", "Terrain"]