__author__ = 'neil'

import pyglet, random

class Pill():
    def __init__(self,x,y,batch):
        print("creating a pill with coords " ,x,y)
        self.size = 6
        self.vel = [0,0]
        self.x = x
        self.y = y
        r = random.randrange(255)
        g = random.randrange(255)
        b = random.randrange(255)
        vertices = [self.x,self.y,self.x,self.y,self.x + self.size,self.y,self.x - self.size/2,self.y + self.size,self.x + self.size/2,self.y + self.size,self.x + self.size/2,self.y + self.size]
        #vertices = [self.x,self.y,self.x +self.size,self.y,self.x +self.size*2,self.y +self.size,self.x+self.size,self.y+self.size*2,self.x,self.y+self.size*2,self.x-self.size,self.y+self.size,self.x,self.y]
        colours = [r,g,b,r,g,b,r,g,b,r,g,b,r,g,b,r,g,b]
        self.position_on_map_x = x
        self.position_on_map_y = y
        self.rotation = 0
        #self.vertex_list = pyglet.graphics.vertex_list(7,("v2f",vertices),("c3b",colours))
        self.vertex_list = batch.add(6,pyglet.gl.GL_TRIANGLE_STRIP,None,("v2f",vertices),("c3b",colours))


    #def draw(self):
        #self.vertex_list.draw(pyglet.gl.GL_POLYGON)

    def get_list(self):
        return self.vertex_list

    def change_position(self,pos):
        if self.position_on_map_x - pos[0] > -10 :
            #print(pos)
            self.x = self.position_on_map_x - pos[0]
            vertices = [self.x,self.y,self.x,self.y,self.x + self.size,self.y,self.x - self.size/2,self.y + self.size,self.x + self.size/2,self.y + self.size,self.x + self.size/2,self.y + self.size]
            self.vertex_list.vertices = vertices
        else:
            self.x = -1000
        if self.position_on_map_y - pos[1] > -10 :
            self.y = self.position_on_map_y - pos[1]
            vertices = [self.x,self.y,self.x,self.y,self.x + self.size,self.y,self.x - self.size/2,self.y + self.size,self.x + self.size/2,self.y + self.size,self.x + self.size/2,self.y + self.size]
            self.vertex_list.vertices = vertices
        else:
            self.y = -1000

print((-16 % 30))