__author__ = 'neil'

import pyglet,time,math, constants, threading

class myWindow(pyglet.window.Window):
    #

    def __init__(self, refreshrate,batch1,batch2):
        self.mag = 0
        self.START_OF_GRID   = [0,0]
        self.BOTTOM_RIGHT_OF_SCREEN = [100,0]
        self.vertex_list = []
        self.create_vertex_list()
        self.batch1 = batch1
        self.batch2 = batch2
        super(myWindow, self).__init__(vsync = False)
        self.set_size(400,400)
        self.frames = 0
        self.velocity = [0,0]
        self.player_pos = [-1,-1]
        self.diff = [0,0]
        self.framerate = pyglet.text.Label(text='Unknown', font_name='Verdana', font_size=8, x=10, y=10, color=(100,200,100,200))
        self.last = time.time()
        self.alive = 1
        self.last_draw = 0
        self.refreshrate = refreshrate
        pyglet.gl.glClearColor(0, 1, 0, 0.5)


    def update_player_position(self,new_pos):
        if self.player_pos == [-1,-1]:
            print("initialising new position as ",new_pos)
            self.player_pos = new_pos
            self.diff = [0,0]
        else:
            temp = self.player_pos
            self.player_pos = new_pos
            self.diff = [temp[0] - self.player_pos[0],temp[1] -self.player_pos[1]]
            #print (" new player position is ",self.player_pos)

    def update(self):#
        self.BOTTOM_RIGHT_OF_SCREEN[0] = self.player_pos[0] - 200
        self.BOTTOM_RIGHT_OF_SCREEN[1] = self.player_pos[1] - 200
        #print(player_pos,diff,START_OF_GRID)
        self.START_OF_GRID[0] += self.diff[0]
        self.START_OF_GRID[1] += self.diff[1]
        #print("after adjustment, start of grid is ",START_OF_GRID)
        if self.BOTTOM_RIGHT_OF_SCREEN[0]<= -200:
            self.BOTTOM_RIGHT_OF_SCREEN[0] =-200
        if self.BOTTOM_RIGHT_OF_SCREEN[0]>=constants.FULL_MAP_WIDTH:
            self.BOTTOM_RIGHT_OF_SCREEN[0] =constants.FULL_MAP_WIDTH
        if self.BOTTOM_RIGHT_OF_SCREEN[1]>=constants.FULL_MAP_WIDTH:
            self.BOTTOM_RIGHT_OF_SCREEN[1] =constants.FULL_MAP_WIDTH
        if self.BOTTOM_RIGHT_OF_SCREEN[1]<= -200:
                self.BOTTOM_RIGHT_OF_SCREEN[1] =-200
        if self.START_OF_GRID[0] >=constants.GRID_WIDTH:
            self.START_OF_GRID[0] = self.START_OF_GRID[0] % constants.GRID_WIDTH
        if self.START_OF_GRID[0] <0:
                self.START_OF_GRID[0] = (self.START_OF_GRID[0]%constants.GRID_WIDTH) #+ GRID_WIDTH
        if self.START_OF_GRID[1] <=0:
                #print("phphph")
                self.START_OF_GRID[1] = (self.START_OF_GRID[1]%constants.GRID_WIDTH)#+ GRID_WIDTH
        if self.START_OF_GRID[1] >=constants.GRID_WIDTH:
                self.START_OF_GRID[1] = self.START_OF_GRID[1] % constants.GRID_WIDTH
        vertices = []
        for i in range(int(self.START_OF_GRID[0]),401+int(self.START_OF_GRID[0]),constants.GRID_WIDTH):
            vertices.append(i)
            vertices.append(0)
            vertices.append(i)
            vertices.append(400)
        for i in range(int(self.START_OF_GRID[1]),401+int(self.START_OF_GRID[1]),constants.GRID_WIDTH):
            vertices.append(0)
            vertices.append(i)
            vertices.append(400)
            vertices.append(i)
        self.vertex_list.vertices = vertices

    def create_vertex_list(self):
        vertices = []
        colours = []
        for i in range(0,401,constants.GRID_WIDTH):
            vertices.append(i)
            vertices.append(0)
            vertices.append(i)
            vertices.append(400)
            vertices.append(0)
            vertices.append(i)
            vertices.append(400)
            vertices.append(i)
            colours.append(205)
            colours.append(201)
            colours.append(201)
            colours.append(205)
            colours.append(201)
            colours.append(201)
            colours.append(205)
            colours.append(201)
            colours.append(201)
            colours.append(205)
            colours.append(201)
            colours.append(201)
            self.vertex_list = pyglet.graphics.vertex_list(int(len(vertices)/2), ('v2i', vertices),('c3B', colours))
            self.vertex_list.vertices = vertices
            self.vertex_list.colours  = colours

    def on_draw(self):
        self.render()

    def render(self):
        if self.last_draw == 0:
            self.last_draw = time.time()*1000
        temp = time.time() * 1000
        temp = temp -self.last_draw
        #print("drawing ",temp)
        #print (self.player_pos)
        self.last_draw = time.time() * 1000
        new_pos = [0,0]
        #print("updting, velocity is ",self.velocity)
        #new_pos[0] = self.player_pos[0] + (self.velocity[0] * 1/self.refreshrate)
        #new_pos[1] = self.player_pos[1] + (self.velocity[1] * 1/self.refreshrate)
        #print("after updating, new position is ",new_pos)
        #self.update_player_position(new_pos)
        self.update()
        self.clear()
        if time.time() - self.last >= 1:
            self.framerate.text = str(self.frames)
            self.frames = 0
            self.last = time.time()
        else:
            self.frames += 1
            #print("frames " ,self.frames)
        self.framerate.draw()
        self.vertex_list.draw(pyglet.gl.GL_LINES)
        self.batch1.draw()
        self.batch2.draw()
        self.flip()
        self.dispatch_events()


    def on_close(self):
        self.alive = 0

    def on_key_release(self, symbol, modkey):
            print(symbol, modkey)

    def on_mouse_motion(self,x, y, dx, dy):
        #print('Mouse from:',x,y,'moved:',dx,dy)
        global velocity,clientsocket,mag
        self.velocity = [x -200,y-200]
        self.mag = math.sqrt(self.velocity[0]**2+self.velocity[1]**2)
        if math.fabs(self.mag) >constants.MAX_MAGNITUDE:
            self.velocity[0] = self.velocity[0] * (constants.MAX_MAGNITUDE/math.fabs(self.mag))
            self.velocity[1] = self.velocity[1] * (constants.MAX_MAGNITUDE/math.fabs(self.mag))
            mag = constants.MAX_MAGNITUDE
        self.dispatch_events()

    def get_velocity(self):
        return [self.velocity[0],self.velocity[1],self.mag]

    def run(self):
        while self.alive:
            self.render()
            event = self.dispatch_events() # <-- This is the event queue
           # self.dispatch_event('on_draw')
            time.sleep(1.0/self.refreshrate)


