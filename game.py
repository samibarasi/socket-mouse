import sys, pygame
pygame.init()
size = width, height = 1280,800
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


while 1:
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT: sys.exit()
        #or event.type == pygame.MOUSEMOTION
        if event.type == pygame.MOUSEBUTTONDOWN :
            pos = event.pos
            text = font.render(str(pos[0]) + ', ' + str(pos[1]) , True, green, blue)
            print(event.type, pygame.MOUSEBUTTONDOWN, pos)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            if screen.get_flags() & pygame.FULLSCREEN:
                pygame.display.set_mode(size)
            else:
                pygame.display.set_mode(size, pygame.FULLSCREEN) 


    screen.fill(black)

    screen.blit(text, textRect)
    pygame.display.flip()
