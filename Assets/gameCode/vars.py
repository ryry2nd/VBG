from ursina import *

app = Ursina()

window.fullscreen = True
window.exit_button.visible = False
window.vsync = True

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
water_texture = (
                load_texture("Assets/textures/water/water.png"), 
                load_texture("Assets/textures/water/water.png"), 
                load_texture("Assets/textures/water/water.png"), 
                load_texture("Assets/textures/water/water.png"), 
                load_texture("Assets/textures/water/water.png"), 
                load_texture("Assets/textures/water/water.png")
                )

sky_texture = load_texture("Assets/textures/skybox.png")

__all__ = ["app", "sky_texture", "water_texture", "bedrock_texture", "stone_texture", "dirt_texture", "grass_texture"]