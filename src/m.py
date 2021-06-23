#import mouse
#import pyautogui
from pynput import mouse
import os
import socket 
import time
from dotenv import load_dotenv

load_dotenv()

def left_mouse():
    #pos = mouse.get_position()
    controller = mouse.Controller()
    pos = controller.position
    message = str(pos[0]) + "," + str(pos[1])
    print(message.encode('utf-8'), server)
    s.sendto(message.encode('utf-8'), server)

def on_click(x, y, button, pressed):
    #print('{0} at {1}'.format(
    #    'Pressed' if pressed else 'Released',
    #    (x, y)))
    if pressed:
        message = "{:d},{:d}".format(int(x), int(y))
        print(message.encode('utf-8'), server)
        s.sendto(message.encode('utf-8'), server)

def Main():
    global s, server
    myHostname = socket.gethostname()
    print("Name of the localhost is {}".format(myHostname))

    host = os.environ.get("MY_IP")
    port = 4005

    server = (os.environ.get("HOST_IP"), int(os.environ.get("HOST_PORT")))

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    #mouse.on_click(left_mouse)

    # Collect events until released
    with mouse.Listener(
            on_click=on_click) as listener:
        listener.join()


    while True:
        #run forever
        
        time.sleep(.1)

        #print(mouse.get_position())
        #mouse.move(100, 100, absolute=True, duration=0.2)
        #mouse.click('right')

if __name__ == '__main__':
    Main()
