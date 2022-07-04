from ursina import *
from Assets import *
from numpy import floor
from perlin_noise import PerlinNoise
import time

noise = PerlinNoise(octaves=4, seed=time.time())
amp = 6
freq = 24

def input(key):
    if key == 'escape':
        exit()

def update():
    global sky, player

    sky.position = player.position

    if held_keys['1']:
        player.selected = 1
    if held_keys['2']:
        player.selected = 2

tWidth = 20
tLength = 20
tHeight = 3

for x in range(tWidth):
    for ty in range(tHeight):
        for z in range(tLength):
            y = floor((noise([x/freq,z/freq]))*amp)-ty
            if ty > 0:
                Dirt_block((x, y, z))
            else:
                Grass_block((x, y, z))

if __name__ == '__main__':
    app.run()