import socket
import os
from dotenv import load_dotenv
from pynput import mouse
from signal import signal, SIGINT
from sys import exit
from multiprocessing import Process

load_dotenv()

def handler(signal_received, frame):
    global run_code
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    run_code = False


def Main(s):
    controller = mouse.Controller()    

    while True:
        data, addr = s.recvfrom(1024)
        data = data.decode('utf-8')
        pos = tuple(map(int, data.split(',')))
        print("Message from: " + str(addr))
        print("From connected client: " + str(pos))
        controller.position = (pos[0], pos[1])

if __name__=='__main__':
    run_code = True
    host = os.environ.get("MY_IP") #Server ip
    port = int(os.environ.get("HOST_PORT"))

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    
    program = Process(target=Main, args=(s,))
    # Tell Python to run the handler() function when SIGINT is recieved
    signal(SIGINT, handler)
    print('Running. Press CTRL-C to exit.')

    # Start Main
    program.start()
    print("Server start listening on {0} and port {1}".format(host, port))

    while run_code:
        # run forever
        pass
    
    # Clean up
    s.close()
    program.terminate();
