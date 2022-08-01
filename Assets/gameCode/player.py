from Assets.gameCode.vars import *
from Assets.gameCode.objects.gameSky import *
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

sky = GameSky()

player = FirstPersonController()
player.jump_height = 1.5
player.selected = 1
player.startPos = Vec3(0, 0, 0)
player.height = 2

def input(key):
    if key == 'escape':
        exit()
    elif key == 'r':
        player.position = player.startPos
        player.air_time = 0
    
    if key == '1':
        player.selected = 1
    elif key == '2':
        player.selected = 2
    elif key == '3':
        player.selected = 3

def update():
    sky.position = player.position

    if held_keys['left control']:
        player.speed = 10
    else:
        player.speed = 5

__all__ = ["sky", "player", "input", "update"]