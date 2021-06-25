import sys, pygame, socket, os, json
from dotenv import load_dotenv
load_dotenv()

# GUI
pygame.init()
size = width, height = 1280,800
# Can't use pygame.OPENGL because it is not supported in virtualbox
flags = pygame.NOFRAME | pygame.FULLSCREEN
black = 0, 0, 0
screen = pygame.display.set_mode((0,0), flags)
pos = (0, 0)
green = (0, 255, 0)
blue = (0, 0, 128)
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('Hello World', True, green, blue)
textRect = text.get_rect()
textRect.center = (width // 2, height // 2) 

# Socket
host = os.environ.get("HOST_IP")
port = int(os.environ.get("HOST_PORT"))
server = (host, port)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(server)
print("Connected to host: {0} on port {1}".format(host, port))
print("My IP addresse is {}".format(s.getsockname()[0]))

# Main
while 1:
    
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT: 
            s.close()
            sys.exit()
        #or event.type == pygame.MOUSEMOTION
        # TODO: add Mouse Motion
        # TODO: add Mouse Button Up
        # TODO: add Double Click 
        # TODO: add Mouse Motion with Button Down  
        if event.type == pygame.MOUSEBUTTONDOWN :
            posX, posY = event.pos
            text = font.render(str(posX) + ', ' + str(posY) , True, green, blue)
            #print("{:d},({:d},{:d})".format(event.type, posX, posY))
            message = {
            	"type": event.type,
            	"X": posX,
            	"Y": posY
            }
            jsonStr = json.dumps(message)
            print(jsonStr)
            #message = "{:d},{:d},{:d}".format(event.type, posX, posY)
            
            s.sendto(jsonStr.encode('utf-8'), server)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
               s.close()
               pygame.quit()
               sys.exit()
            if event.key == pygame.K_f:
                if screen.get_flags() & pygame.FULLSCREEN:
                    pygame.display.set_mode(size)
                else:
                    pygame.display.set_mode(size, pygame.FULLSCREEN) 


    screen.fill(black)

    screen.blit(text, textRect)
    pygame.display.flip()
