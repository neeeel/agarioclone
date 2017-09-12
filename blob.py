__author__ = 'neil'

import math,pill,random,socket,json,clientsocket,mywindow, threading

import pyglet,physicalobject,player, constants, time,repeatedtimer



BOTTOM_RIGHT_OF_SCREEN = [100,0]
START_OF_GRID   = [0,0]
GRID_WIDTH = 30
LEFT = False
RIGHT = False
UP = False
DOWN = False

velocity = [20,20]
mag = 0.0
total_moved = 0
SPEED = 30
current_frame = 0
window = None


def update():
    global window,player
    while True:
        if window != None:
            temp = player.get_pos()
            #print("in blob update, player pos is ",temp)
            if temp != None:
                window.update_player_position(temp)
                temp = window.get_velocity() #[velocity[0] ,velocity[1],mag]
                player.add_frame(temp)
        time.sleep(1/constants.FRAME_RATE)
    #player.send_frames()


def start_client():
    global clientsocket, ip_address
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print("trying to connect to " )
        clientsocket.connect(("localhost", 5554))
    except Exception as e:
        # print(e.__class__)
        # print(type(e))
        print("failed", type(e))
    print ("connected")

batch = pyglet.graphics.Batch()
batch2 = pyglet.graphics.Batch()
player_img = pyglet.image.load('blue flag.png')
things = []
pills = []
player_sprite = pyglet.sprite.Sprite(player_img,200,200,batch = batch)
player_sprite.scale = 0.55
for i in range(0,constants.NUM_PILLS):
    my_pill = pill.Pill(random.randrange(1200),random.randrange(1200),batch2)
    pills.append(my_pill)
player = player.Player()
player.start()
#print("player thread started")
player.join(0.1)
pyglet.gl.glClearColor(0, 1, 1, 1)
t = threading.Thread(target = update)
t.start()
print("now here")
window =mywindow.myWindow(constants.FRAME_RATE,batch,batch2)
window.run()
