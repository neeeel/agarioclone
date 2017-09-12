__author__ = 'neil'

import socket,json,threading,struct

class ClientSocket(socket.socket):
    def __init__(self):
        super(ClientSocket, self).__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.send_thread = threading.Thread()
        self.listen_thread = threading.Thread()
        self.last_received =0
        self.send_queue= []

    def connect(self):
        try:
            print("trying to connect to " )
            super(ClientSocket, self).connect(("localhost", 5554))
        except Exception as e:
            # print(e.__class__)
            # print(type(e))
            print("failed", type(e))
        print ("connected")

    def test(self):
        return "pop"

    def send(self,msg):
        #print(type(msg))
        temp= json.dumps(msg)
        value = len(temp)
        packer = struct.Struct("L")
        packed_data = packer.pack(value)
        try:
            #print("in clientsocket, trying to send ",msg)
            super(ClientSocket, self).send(packed_data)
        except Exception as e:
            print("failed to send length string ", type(e))
            print (str(e))
        try:
            super(ClientSocket, self).send(temp.encode())
        except Exception as e:
            print("failed to send length string ", type(e))
            print (str(e))


    def receive(self):
        pass