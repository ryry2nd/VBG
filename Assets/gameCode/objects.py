from ursina import *
from Assets.gameCode.vars import *

class Voxel(Button):
    def __init__(self, texture, position, model='Assets/models/block'):
        super().__init__(
            parent = scene,
			position = position,
			model = model,
			origin_y = 0.5,
			texture = texture,
            color = color.color(0, 0, random.uniform(1.9,1)),
			scale = 0.5
        )
    def input(self, key):
        if self.hovered:
            pos = self.position + mouse.normal
            if distance(pos, player) < 7:
                if key == 'right mouse down':
                    if player.selected == 1:
                        Grass_block(pos)
                    elif player.selected == 2:
                        Dirt_block(pos)
                elif key == 'left mouse down':
                    destroy(self)

class Grass_block(Voxel):
    def __init__(self, position):
        super().__init__("Assets/textures/grass_block.png", position)

class Dirt_block(Voxel):
    def __init__(self, position):
        super().__init__("Assets/textures/dirt_block.png", position)

class GameSky(Entity):
	def __init__(self):
    		super().__init__(
			parent = scene,
			model = 'sphere',
			texture = 'Assets/textures/skybox.png',
			scale = 10000,
			double_sided = True,
            collision = False
            )

__all__ = ["Grass_block", "Dirt_block", "GameSky"]