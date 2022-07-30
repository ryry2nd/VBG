from Assets.gameCode.vars import *
from Assets.gameCode.objects.blocks import *
from ursina import *

class Voxel:
    def __init__(self, position:tuple, texture:tuple, truePos:tuple, chunk):
        self.position = position
        self.texture = texture

        self.top = None
        self.bottom = None
        self.left = None
        self.right = None
        self.front = None
        self.back = None

        self.chunk = chunk
        self.truePos = truePos

    def toggleTopFace(self):
        x, y, z = self.position
        if self.top == None:
            self.top = Face((x, y+0.5, z), Vec3(90, 0, 0), self.texture[0], self)
        else:
            destroy(self.top)
            self.top = None
    
    def toggleBottomFace(self):
        x, y, z = self.position
        if self.bottom == None:
            self.bottom = Face((x, y-0.5, z), Vec3(-90, 0, 0), self.texture[1], self)
        else:
            destroy(self.bottom)
            self.bottom = None
    
    def toggleLeftFace(self):
        x, y, z = self.position
        if self.left == None:
            self.left = Face((x+0.5, y, z), Vec3(0, -90, 0), self.texture[3], self)
        else:
            destroy(self.left)
            self.left = None
    
    def toggleRightFace(self):
        x, y, z = self.position
        if self.right == None:
            self.right = Face((x-0.5, y, z), Vec3(0, 90, 0), self.texture[2], self)
        else:
            destroy(self.right)
            self.right = None
    
    def toggleFrontFace(self):
        x, y, z = self.position
        if self.front == None:
            self.front = Face((x, y, z+0.5), Vec3(0, -180, 0), self.texture[4], self)
        else:
            destroy(self.front)
            self.front = None

    def toggleBackFace(self):
        x, y, z = self.position
        if self.back == None:
            self.back = Face((x, y, z-0.5), Vec3(0, 0, 0), self.texture[5], self)
        else:
            destroy(self.back)
            self.back = None
    
    def toggleAllFaces(self):
        self.toggleTopFace()
        self.toggleBottomFace()
        self.toggleLeftFace()
        self.toggleRightFace()
        self.toggleFrontFace()
        self.toggleBackFace()

    def updateVisible(self):
        x, z, y = self.truePos

        maxX = len(self.chunk.blocks)
        maxZ = len(self.chunk.blocks[x])
        maxY = len(self.chunk.blocks[x][z])

        if y != maxY-1 and self.chunk.blocks[x][z][y+1] != None:
            self.chunk.blocks[x][z][y+1].toggleBottomFace()
        if y != 0 and self.chunk.blocks[x][z][y-1]!= None:
            self.chunk.blocks[x][z][y-1].toggleTopFace()
        if x != maxX-1 and y <= len(self.chunk.blocks[x+1][z])-1 and self.chunk.blocks[x+1][z][y] != None:
            self.chunk.blocks[x+1][z][y].toggleRightFace()
        if x != 0 and y <= len(self.chunk.blocks[x-1][z])-1 and self.chunk.blocks[x-1][z][y] != None:
            self.chunk.blocks[x-1][z][y].toggleLeftFace()
        if z != maxZ-1 and y <= len(self.chunk.blocks[x][z+1])-1 and self.chunk.blocks[x][z+1][y] != None:
            self.chunk.blocks[x][z+1][y].toggleBackFace()
        if z != 0 and y <= len(self.chunk.blocks[x][z-1])-1 and self.chunk.blocks[x][z-1][y] != None:
            self.chunk.blocks[x][z-1][y].toggleFrontFace()

    def breakBlock(self):
        x, z, y = self.truePos

        self.updateVisible()

        self.chunk.blocks[x][z][y] = None

        destroy(self.top)
        destroy(self.bottom)
        destroy(self.left)
        destroy(self.right)
        destroy(self.front)
        destroy(self.back)
    
    def place(self, pos):
        x, y, z = (None, None, None)

        maxX, maxZ, maxY = len(self.chunk.blocks), len(self.chunk.blocks[x]), len(self.chunk.blocks[x][z])

        if x>maxX-1 and y>maxY-1 and z>maxZ-1 and self.chunk.blocks[x][z][y] == None:
            self.chunk.blocks[x][z].pop(y)

        if player.selected == 1:
            self.chunk.blocks[x][z].insert(y, Grass_block(pos, (x, z, y), self.chunk))
        elif player.selected == 2:
            self.chunk.blocks[x][z].insert(y, Dirt_block(pos, (x, z, y), self.chunk))
        elif player.selected == 3:
            self.chunk.blocks[x][z].insert(y, Stone_block(pos, (x, z, y), self.chunk))
        elif player.selected == 4:
            Bedrock_block(pos)
        
        self.chunk.blocks[x][z][y].toggleTopFace()
        
        maxX, maxZ, maxY = len(self.chunk.blocks), len(self.chunk.blocks[x]), len(self.chunk.blocks[x][z])

        if y != maxY-1 and self.chunk.blocks[x][z][y+1] != None:
            self.chunk.blocks[x][z][y+1].toggleBottomFace()
        if y != 0 and self.chunk.blocks[x][z][y-1]!= None:
            self.chunk.blocks[x][z][y-1].toggleTopFace()
        if x != maxX-1 and y <= len(self.chunk.blocks[x+1][z])-1 and self.chunk.blocks[x+1][z][y] != None:
            self.chunk.blocks[x+1][z][y].toggleRightFace()
        if x != 0 and y <= len(self.chunk.blocks[x-1][z])-1 and self.chunk.blocks[x-1][z][y] != None:
            self.chunk.blocks[x-1][z][y].toggleLeftFace()
        if z != maxZ-1 and y <= len(self.chunk.blocks[x][z+1])-1 and self.chunk.blocks[x][z+1][y] != None:
            self.chunk.blocks[x][z+1][y].toggleBackFace()
        if z != 0 and y <= len(self.chunk.blocks[x][z-1])-1 and self.chunk.blocks[x][z-1][y] != None:
            self.chunk.blocks[x][z-1][y].toggleFrontFace()

class Face(Button):
    def __init__(self, position, rotation, texture, block):
        self.block = block
        super().__init__(
        parent = scene,
        position = position,
        rotation = rotation,
        model = "quad",
        texture = texture,
        color = color.color(0, 0, 2),
        highlight_color = color.gray
        )

    def input(self, key):
        if self.hovered and mouse.normal:
            pos = self.position + mouse.normal
            if distance(pos, player) < 7:
                if key == 'right mouse down':
                    self.block.place(pos)
                elif key == 'left mouse down':
                    self.block.breakBlock()

__all__ = ["Voxel", "Face"]