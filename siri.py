import pygame
import sys
from elements.dock import Dock
from elements.textbox import Textbox

pygame.init()
window_name = '.'.join(sys.argv[0].split('.')[:-1])
pygame.display.set_caption(window_name if window_name != '' else 'pygame')
pygame.display.set_icon(pygame.image.load('resources/images/mic.png'))
SCREEN = pygame.display.set_mode((375, 667))
done = False
clock = pygame.time.Clock()
FRAME_RATE = 120

dock = Dock((375, 100))

tb = Textbox(375)
tb.setstr1("Hello")
tb.setstr2("Hi there! What can I do for you? brrrrr")

while not done:
	SCREEN.fill((0, 0, 0))
	dock.update()
	SCREEN.blit(dock.show(), (0, 580))
	tb.show(SCREEN, 20)
	# pygame.draw.rect(SCREEN, (0, 255, 0), (325, 615, 30, 30))
	events = pygame.event.get()
	dock.eventHandler(events)
	for event in events:
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.KEYDOWN:
			# if event.key == pygame.K_SPACE:
			# 	for wave in waves:
			# 		wave.induce(0.5)
			if event.key == pygame.K_q:
				done = True
	pygame.display.flip()
	clock.tick(FRAME_RATE)
