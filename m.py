import mouse
import socket 
import time


def left_mouse():
    print('LEFT ', mouse.get_position())

def Main():
    myHostname = socket.gethostname()
    print("Name of the localhost is {}".format(myHostname))

    host = myHostname
    port = 4005

    server ('192.168.69.121', 4000)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    

#mouse.on_click(left_mouse)


#vid=0x046d 
#pid=0xc068

#with hid.Device(vid, pid) as h:
#   print(h.manufacturer)
#    print(h.product)
#    print(h.serial)
#    print(h)
    #h.set_raw_data_handler(readData)

    while True:
        #run forever
        
        time.sleep(.1)

        #print(mouse.get_position())
        #mouse.move(100, 100, absolute=True, duration=0.2)
        #mouse.click('right')

if __name__ == '__main__':
    Main()
