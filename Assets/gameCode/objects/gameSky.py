from Assets.gameCode.vars import *
from ursina import *

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

__all__ = ["GameSky"]