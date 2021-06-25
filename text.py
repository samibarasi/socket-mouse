import pygame
import sys


pygame.init()
info = pygame.display.Info()
SIZE = WIDTH, HEIGHT = info.current_w, info.current_h
print(WIDTH, HEIGHT)
flags = pygame.NOFRAME | pygame.FULLSCREEN
mainsurface = pygame.display.set_mode(SIZE, flags)
screen = pygame.Surface((800, 600))
screen.fill((10, 200, 255))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 72)
text = "Hello World in a Full screen"
rt = font.render(text, 1, pygame.Color("White"))

while True:
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
	screen.blit(rt, (0, 0))
	mainsurface.blit(
		pygame.transform.scale(screen, (WIDTH, HEIGHT)), # scale to full
		(0, 0)) # the position of the scaled screen
	pygame.display.update()
