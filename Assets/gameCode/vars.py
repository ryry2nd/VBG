from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

class GamePlayer(FirstPersonController):
    selected = 1

app = Ursina()
player = GamePlayer()

__all__ = ["app", "player"]