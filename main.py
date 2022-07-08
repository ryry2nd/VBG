from ursina import *
from Assets import *

window.fullscreen = True
window.exit_button.visible = False
window.vsync = True

def input(key):
    if key == 'escape':
        exit()
    elif key == 'r':
        player.position = (0, 100, 0)

def update():
    global sky, player

    sky.position = player.position

    if held_keys['1']:
        player.selected = 1
    elif held_keys['2']:
        player.selected = 2
    elif held_keys['3']:
        player.selected = 3
    elif held_keys['4']:
        player.selected = 4

terrain = Terrain((1, 1), 16)

if __name__ == '__main__':
    app.run()
    

"""
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
from numpy import floor
app = Ursina()

class Voxel(Button):
    def __init__(self, model, color, chunk):
        super().__init__(model=model, color=color)
        self.parent = chunk

class Terrain(Entity):
    def __init__(self):
        super().__init__(model=None, collider=None)
        self.generate()
        self.combine()
        self.collider = 'mesh'
        self.texture = 'white_cube'
    
    def generate(self):
        noise = PerlinNoise(octaves=2, seed=100)
        freq = 24
        amp = 5

        terrain_width = 16
        for i in range(terrain_width*terrain_width):
            block = Voxel(model='cube', color=color.green, chunk=self)
            block.x = floor(i/terrain_width)
            block.z = floor(i%terrain_width)
            block.y = floor(noise([block.x/freq, block.z/freq]) * amp)

terrain = Terrain()

FirstPersonController()

app.run()"""