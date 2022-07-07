from ursina import *
from Assets import *
from threading import Thread
import time

st = time.time()
t1 = Thread(target=Terrain, args=((1, 1), 16, ) )
t1.start()

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

t1.join()
print(time.time()-st)

if __name__ == '__main__':
    app.run()