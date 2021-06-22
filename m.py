import mouse
#import pyautogui
import socket 
import time


def left_mouse():
    pos = mouse.get_position()
    message = str(pos[0]) + "," + str(pos[1])
    print(message.encode('utf-8'), server)
    s.sendto(message.encode('utf-8'), server)

def Main():
    global s, server
    myHostname = socket.gethostname()
    print("Name of the localhost is {}".format(myHostname))

    host = '192.168.69.112'
    port = 4005

    server = ('192.168.69.121', 4000)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    mouse.on_click(left_mouse)


    while True:
        #run forever
        
        time.sleep(.1)

        #print(mouse.get_position())
        #mouse.move(100, 100, absolute=True, duration=0.2)
        #mouse.click('right')

if __name__ == '__main__':
    Main()
