#!/usr/bin/env python3

import os, socket, time
from dotenv import load_dotenv
from pynput.mouse import Button, Controller
from signal import signal, SIGINT
from multiprocessing import Process

load_dotenv()

width, height = 2560, 1440
MAX = 10000

def handler(signal_received, frame):
    global run_code
    # Handle any cleanup here
    if signal_received == SIGINT:
        print('SIGINT or CTRL-C detected. Exiting gracefully')
        run_code = False

def Main(s):
    controller = Controller() 
    pressed = 0
    timeout = 5 # timeout for touch reset.
    timestamp = time.time()

    while True:
        # make sure timeout for reset touch is not reached.
        if timestamp + timeout < time.time():
            touch = 0
            controller.release(Button.left)
            pressed = touch

        # reveive data from socket connection
        data, addr = s.recvfrom(1024)
        data = data.decode('utf-8')
        event = tuple(map(int, data.split(',')))
        print("Raw data", data)
        print("Message from: " + str(addr))
        print("From connected client: " + str(event))

        touch = event[0]
        posX = int(width / MAX * event[2])
        posY = int(height / MAX * event[3])
        controller.position = (posX, posY)
        if pressed != touch and touch == 1:
            controller.press(Button.left)
            pressed = touch
        elif pressed != touch and touch == 0:
            controller.release(Button.left)
            pressed = touch

        timestamp = time.time()
        
        # if touch == 0:
        #     # on touchup (release)
        #     controller.click(mouse.Button.left, 1)

if __name__=='__main__':
    run_code = True
    host = os.environ.get("HOST_IP", '') #Server ip
    port = int(os.environ.get("HOST_PORT", 4000))

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
    program.terminate()
    s.close()
