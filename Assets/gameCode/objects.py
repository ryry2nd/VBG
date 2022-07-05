from perlin_noise import PerlinNoise
from ursina import *
from Assets.gameCode.vars import *

class Voxel(Button):
    def __init__(self, texture, position, model='Assets/models/block'):
        super().__init__()
        self.parent = scene
        self.position = position
        self.model = model
        self.origin_y = 0.5
        self.texture = texture
        self.color = color.color(0, 0, 2)
        self.scale = 0.5
        self.highlight_color = color.white

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
                elif key == 'left mouse down':
                    destroy(self)

class Grass_block(Voxel):
    def __init__(self, position):
        super().__init__(grass_texture, position)

class Dirt_block(Voxel):
    def __init__(self, position):
        super().__init__(dirt_texture, position)

class Stone_block(Voxel):
    def __init__(self, position):
         super().__init__(stone_texture, position)

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

    def generate_chunk(self):
        xPos, zPos = self.position

        for x in range(xPos, xPos+16):
            self.blocks.append([])
            for z in range(zPos, zPos+16):
                self.blocks[-1].append([])
                ty = round(self.noise([x/self.freq,z/self.freq])*self.amp)
                for y in range(ty+self.height):
                    ry = (ty+self.height)-y-1
                    if ry > 2:
                        self.blocks[-1][-1].append(Stone_block((x, y, z)))
                    elif ry > 0:
                        self.blocks[-1][-1].append(Dirt_block((x, y, z)))
                    else:
                        self.blocks[-1][-1].append(Grass_block((x, y, z)))
    
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