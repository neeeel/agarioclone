__author__ = 'neil'


import threading,time,pyglet,clientsocket,struct,time,json,constants
from collections import deque



class Player(threading.Thread):
    def __init__(self):
        super(Player, self).__init__()
        #self.img = img
        self.tick_value = (1000/constants.TICK_VALUE)
        self.last_tick = 0
        self.lock = threading.Lock()
        self.frames = deque([])
        self.position_queue = []
        self.pos = [-1,-1]
        self.diff = [0,0]
        self.vel = []
        self.start_time = 0
        self.current_frame_no = 0
        self.last_frame_received = 0
        self.initialized = False
        #self.sprite = pyglet.sprite.Sprite(img,200,200)
        #self.sprite.scale  = 0.05
        self.clientsocket = clientsocket.ClientSocket()
        self.clientsocket.connect()
        t = threading.Thread(target = self.update_position )
        t.start()
        t.join(0.01)


    def get_pos(self):
        return self.pos
        #print("in get_pos")
        if len(self.position_queue) >0:
            temp = self.position_queue[0]
            self.position_queue.remove(0)
            #print("position queue is " , self.position_queue)
           # print("temp is ",temp)
            return temp
        else:
            return None


    def get_dif(self):
        return self.diff

    def add_frame(self,frame):
        if self.initialized == False:
            return
        #print("ADDING FRAME")
        self.lock.acquire()
        if self.start_time  == 0:
            self.start_time = time.time()
            print("setting start time to ",self.start_time)
        self.current_frame_no +=1
        self.frames.append([self.current_frame_no,frame])
        for f in list(self.frames):
            if f[0] <= self.last_frame_received:
                self.frames.popleft()
        self.lock.release()
        self.send_frames()

    def send_frames(self):
        #print (self.frames)
        #print("sending frames ", self.frames)
        self.clientsocket.send(list(self.frames))

    def update_position(self):
        while True:
            #print("in updateposition")
            t = time.time()
            if  (t - self.start_time) * 1000 < 1000:
                print("buffering,size of received frames is ",self.position_queue)
                #return
            else:
                #print("here now")
                if (t - self.last_tick)*1000 >= self.tick_value:
                    #print("updating player position, length of position queue is ",len(self.position_queue))
                    #print("time since last update is ",(t - self.last_tick)*1000 )
                    self.last_tick = t
                    if len(self.position_queue)> 10:
                        next_pos =self.position_queue.pop(0)
                        #print("popped next position of player : ",next_pos)
                        temp = self.pos
                        self.pos = next_pos
                        self.diff = [self.pos[0]- temp[0] ,self.pos[1] - temp[1] ]
            time.sleep(0.001)


    def test_change_position(self,pos):
        #pos here is velocity
        temp = self.pos
        self.pos = [pos[0] + self.pos[0],pos[1] + self.pos[1]]
        self.diff = [temp[0] - self.pos[0],temp[1] -self.pos[1]]
        #print(" diff between last position and new position is ",self.diff)
        #print("received velocity " , pos)
        #print ("new player position is " ,self.pos)

    def run(self):
        while True:
            try:
                #print("in player thread")
                unpacker = struct.Struct("L")
                msg =self.clientsocket.recv(4)
                if len(msg ) <4:
                    return
                length = unpacker.unpack(msg)
            except ConnectionResetError as e:
                print("connection forcibly closed by client")
                return
            except ConnectionAbortedError as e:
                return
            MSGLEN = int(length[0])            
            chunks = []
            received = 0
            while received < MSGLEN:
                try:
                    chunk  = str(self.clientsocket.recv(min(MSGLEN - received, 2048)).decode())
                except ConnectionResetError as e:
                    print("connection forcibly closed by client")
                    return
                except ConnectionAbortedError as e:
                    return
                if chunk == '':
                    return
                chunks.append(chunk)
                received +=  len(chunk)
            data = "".join(chunks)
            msg = json.loads(data)
            #print("in player module,message rceived from server is," ,msg)
            if msg[0] == constants.NEXT_POSITION:
                if self.pos == [-1,-1] :
                    self.pos = msg[1]
                else:
                    #temp = self.pos
                    #self.pos = msg[1]
                    #self.diff = [self.pos[0]- temp[0] ,self.pos[1] - temp[1] ]
                    #msg[1] here is the actual position after velocity has been calculated and dt been applied
                    #print("received position " , msg[1])
                    self.position_queue.append( msg[1])
                    #print("position queue is ",self.position_queue)
            if msg[0] == constants.LAST_FRAME_RECEIVED:
                self.last_frame_received = msg[1]
                self.lock.acquire()
                #print("run acquired lock")
                temp = list(self.frames)
                for f in temp:
                    if f[0] <= self.last_frame_received:
                        temp.remove(f)
                self.frames = deque(temp)
                #print("length of self.frames is ",len(self.frames))
                self.lock.release()
                #print("run released lock")
                #print("after receiving data from server, no of frames left is ",len(self.frames))
                #print("first frame is " ,self.frames[0][0])
            if msg[0] == constants.INITIALISE:
                self.pos = msg[1]
                #print("received initialisation data",msg[1])
                #print("self.ois is " ,self.pos)
                self.position_queue.append(msg[1])
                self.initialized = True
            time.sleep(0.01)




