__author__ = 'neil'


import socket
import threading
import win32com.client
import decimal
import pythoncom,pyglet
import time,client,random,json,struct,constants


class myServerSocket(socket.socket):
    def __init__(self):
        pythoncom.CoInitialize()
        self.clients = []
        self.players = {}
        super(myServerSocket, self).__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.last_tick = time.time() * 1000
        self.tick_value = constants.TICK_VALUE
        print("starting server with tick rate of ",self.tick_value)
        t = threading.Thread(target= self.update)
        t.start()
        t.join(0.01)


    def update(self):
        while True:
            t = time.time() *1000
            tick = t - self.last_tick
            self.last_tick = t
            print("time since last tick ",tick)
            t = time.time() * 1000
            for c in self.clients:
                c.update()
            #print("update of clients took ",time.time() * 1000 -t)
            time.sleep(1/constants.TICK_VALUE)

    def listen(self, max):
        super(myServerSocket, self).listen(max)
        while 1:
            try:
                clientsocket, address = self.accept()
            except Exception as e:
                break
            print("new connection made, no of active connections ",len(self.clients))
            x =random.randrange(2000)
            y = random.randrange(2000)
            c = client.Client(x,y,3,3,"1up.png",clientsocket,self.tick_value)
            self.clients.append(c)
            c.add_to_outgoing_queue([constants.INITIALISE,[x,y]])
            #t = threading.Thread(target=self.deal_with_client,args=(clientsocket,c))
            #t.start()
            #t.join(0.1)


    def close_connection(self):
        for c in self.clients:
            c.close()
        self.close()

    def deal_with_client(self,clientsocket,client):
        while True:
            print("op")
            try:
                unpacker = struct.Struct("L")
                msg =clientsocket.recv(4)
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
                    chunk  = str(clientsocket.recv(min(MSGLEN - received, 2048)).decode())
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
            #print( "in server, received ",data)
            last_received  = client.add_frames(data)
            packer = struct.Struct("L")
            packed_data = packer.pack(last_received)
            try:
                #print(temp)
                clientsocket.send(packed_data)
            except Exception as e:
                print("failed to send  , ", type(e))
                print (str(e))
        clientsocket.close()
        print("connection closed")

def server():
    global serversocket
    serversocket.bind(('', 5554))
    print("listening")
    serversocket.listen(5)



serversocket = myServerSocket()
t = threading.Thread(target = server)
t.start()
#t.join (0.1)
#tt = threading.Timer(0.1,update)
#tt.start()
