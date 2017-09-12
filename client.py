__author__ = 'neil'

import time,json,clientsocket,struct,threading,constants
from collections import deque

FULL_MAP_WIDTH = 2000
FULL_MAP_HEIGHT = 2000

class Client():
    def __init__(self,x,y,x1,y1,img,c,tick_value):
        self.tick_value = tick_value
        self.frames = {}
        self.outgoing_queue  = []
        self.pos = [x,y]
        self.vel = []
        self.img = img
        self.start_time = 0
        self.current_frame = 0
        self.last_frame_received = 0
        self.connected_socket = c
        t = threading.Thread(target = self.deal_with_incoming)
        t.start()
        t.join(0.01)
        t = threading.Thread(target = self.deal_with_outgoing)
        #print("in client, thread for dealing with outgoing is ",t.name)
        t.start()
        t.join (0.01)

    def update(self):
        next_frame = self.current_frame + 1
        if len(self.frames) >0:
            if int(next_frame) in self.frames:
                vel = self.frames[int(next_frame)]
                self.pos[0] += vel[0] * self.tick_value/1000
                self.pos[1] += vel[1] * self.tick_value/1000
                if self.pos[0] > FULL_MAP_HEIGHT:
                    self.pos[0] = FULL_MAP_HEIGHT
                if self.pos[0] <0:
                    self.pos[0] = 0
                if self.pos[1] > FULL_MAP_WIDTH:
                    self.pos[1] = FULL_MAP_WIDTH
                if self.pos[1] <0:
                    self.pos[1] = 0
                del self.frames[int(next_frame)]
                self.current_frame += 1
                self.outgoing_queue.append((constants.NEXT_POSITION,self.pos))

                #print("processing frame " ,next_frame)
                #print ("frame was ",vel)
                #print ("new calculated position ", self.pos)

    def deal_with_outgoing(self):
        while True:
            if len(self.outgoing_queue) > 0:
                msg = self.outgoing_queue.pop(0)
                #print(" in client, deal with outgoing, sending msg " ,msg)
                msg = json.dumps(msg)
                try:
                    packer = struct.Struct("L")
                    packed_data = packer.pack(len(msg))
                    self.connected_socket.send(packed_data)
                except Exception as e:
                    print("failed to send length string ", type(e))
                    print (str(e))
                    return
                try:
                    self.connected_socket.send(msg.encode())
                except Exception as e:
                    print("failed to send length string ", type(e))
                    print (str(e))
                    return

    def add_to_outgoing_queue(self,msg):
        self.outgoing_queue.append(msg)

    def add_frames(self,received_frames):
        frames = json.loads(received_frames)
        #print(frames)
        if len(self.frames) == 0:
            self.start_time = time.time()
        #print("last frame received was ",self.last_frame_received)
        for f in frames:
            frame_no = int(f[0])
            #print ("processing frame no ",frame_no)
            if frame_no > self.last_frame_received:
                self.frames[frame_no] = f[1]
                self.last_frame_received = frame_no
        #print ("after adding frames, self.frames is " ,self.frames)
        return self.last_frame_received



    def deal_with_incoming(self):
        while True:
            try:
                unpacker = struct.Struct("L")
                msg =self.connected_socket.recv(4)
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
                    chunk  = str(self.connected_socket.recv(min(MSGLEN - received, 2048)).decode())
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
           #print("received frame ",data)
            last_received  = self.add_frames(data)
            self.outgoing_queue.append((constants.LAST_FRAME_RECEIVED,last_received))
        self.connected_socket.close()
        print("connection closed")


temp = [1, [-118.69275020882506, -91.71712516136482, 150]]
temp2 = [0,[0.0,0.0,0]]
print (len(temp))
t1 = json.dumps(temp).encode()
t2 = json.dumps(temp2).encode()
print(len(t1))
print(len(t2))