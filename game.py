import sys, pygame
pygame.init()
clock = pygame.time.Clock()
size = width, height = 640,480 
speed = [2, 2]
black = 0, 0, 0
friction = 5

screen = pygame.display.set_mode(size)

ball = pygame.image.load("intro_ball.gif")
ballrect = ball.get_rect()

while 1:
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT: sys.exit()
        #or event.type == pygame.MOUSEMOTION
        if event.type == pygame.MOUSEBUTTONDOWN :
            pos = event.pos
            print(event.type, pygame.MOUSEBUTTONDOWN, pos)
            deltaX = (pos[0] - ballrect.x) / friction
            deltaY = (pos[1] - ballrect.y) / friction
            ballrect = ballrect.move(deltaX, deltaY)
    #if ballrect.left < 0 or ballrect.right > width:
    #    speed[0] = -speed[0]
    #if ballrect.top < 0 or ballrect.bottom > height:
    #    speed[1] = -speed[1]

    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()
    clock.tick(60)
