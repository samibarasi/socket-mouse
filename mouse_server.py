import socket
#import mouse

def Main():
   
    host = '192.168.69.121' #Server ip
    port = 4000

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    print("Server Started")
    while True:
        data, addr = s.recvfrom(1024)
        data = data.decode('utf-8')
        pos = tuple(map(int, data.split(',')))
        print("Message from: " + str(addr))
        print("From connected client: " + str(pos))
#        mouse.move(pos[0], pos[1])
    c.close()

if __name__=='__main__':
    Main()
