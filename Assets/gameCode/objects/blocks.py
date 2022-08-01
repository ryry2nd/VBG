from Assets.gameCode.objects.voxel import Voxel
from Assets.gameCode.vars import *

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

class Water(Voxel):
    def __init__(self, position, truePos, chunk):
        super().__init__(position, water_texture, truePos, chunk, collider=None)

__all__ = ["Grass_block", "Dirt_block", "Stone_block", "Bedrock_block", "Water"]