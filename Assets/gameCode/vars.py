from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

class GamePlayer(FirstPersonController):
    selected = 1

app = Ursina()
player = GamePlayer(position=(0, 100, 0))

grass_texture = load_texture("Assets/textures/grass_block.png")
dirt_texture = load_texture("Assets/textures/dirt_block.png")
stone_texture = load_texture("Assets/textures/stone_block.png")
bedrock_texture = load_texture("Assets/textures/bedrock_block.png")
sky_texture = load_texture("Assets/textures/skybox.png")

__all__ = ["app", "player", "grass_texture", "dirt_texture", "stone_texture", "sky_texture", "bedrock_texture"]