from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

class GamePlayer(FirstPersonController):
    selected = 1

app = Ursina()
player = GamePlayer(position=(0, 100, 0), jump_height=1.5)

grass_texture = (
                load_texture("Assets/textures/grass/top.png"), 
                load_texture("Assets/textures/grass/bottom.png"), 
                load_texture("Assets/textures/grass/side.png"), 
                load_texture("Assets/textures/grass/side.png"), 
                load_texture("Assets/textures/grass/side.png"), 
                load_texture("Assets/textures/grass/side.png")
                )
dirt_texture = (
                load_texture("Assets/textures/dirt/dirt.png"), 
                load_texture("Assets/textures/dirt/dirt.png"), 
                load_texture("Assets/textures/dirt/dirt.png"), 
                load_texture("Assets/textures/dirt/dirt.png"), 
                load_texture("Assets/textures/dirt/dirt.png"), 
                load_texture("Assets/textures/dirt/dirt.png")
                )
stone_texture = (
                load_texture("Assets/textures/stone/stone.png"), 
                load_texture("Assets/textures/stone/stone.png"), 
                load_texture("Assets/textures/stone/stone.png"), 
                load_texture("Assets/textures/stone/stone.png"), 
                load_texture("Assets/textures/stone/stone.png"), 
                load_texture("Assets/textures/stone/stone.png")
                )
bedrock_texture = (
                load_texture("Assets/textures/bedrock/bedrock.png"), 
                load_texture("Assets/textures/bedrock/bedrock.png"), 
                load_texture("Assets/textures/bedrock/bedrock.png"), 
                load_texture("Assets/textures/bedrock/bedrock.png"), 
                load_texture("Assets/textures/bedrock/bedrock.png"), 
                load_texture("Assets/textures/bedrock/bedrock.png")
                )

sky_texture = load_texture("Assets/textures/skybox.png")

__all__ = ["app", "player", "grass_texture", "dirt_texture", "stone_texture", "sky_texture", "bedrock_texture"]