import socket
import os
from dotenv import load_dotenv
from pynput import mouse 

load_dotenv()

def Main():

    controller = mouse.Controller()
   
    host = os.environ.get("HOST_IP") #Server ip
    port = int(os.environ.get("HOST_PORT"))

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    print("Server Started")
    while True:
        data, addr = s.recvfrom(1024)
        data = data.decode('utf-8')
        pos = tuple(map(int, data.split(',')))
        print("Message from: " + str(addr))
        print("From connected client: " + str(pos))
        controller.position = (pos[0], pos[1])
    c.close()

if __name__=='__main__':
    Main()
