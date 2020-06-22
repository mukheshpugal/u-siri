import pygame
import sys
from elements.waveform import Wave
from elements.textbox import Textbox

pygame.init()
window_name = '.'.join(sys.argv[0].split('.')[:-1])
pygame.display.set_caption(window_name if window_name != '' else 'pygame')
SCREEN = pygame.display.set_mode((375, 667))
done = False
clock = pygame.time.Clock()
FRAME_RATE = 120

waves = []
waves.append(Wave(50, (255, 0, 0), 375))
waves.append(Wave(50, (0, 255, 0), 375))
waves.append(Wave(50, (0, 0, 255), 375))

tb = Textbox(375)
tb.setstr1("Hello")
tb.setstr2("Hi there! What can I do for you? brrrrr")

while not done:
	SCREEN.fill((0, 0, 0))
	# pygame.dra
	for wave in waves:
		wave.update(0.83)
		wave.show(SCREEN, 540)
	tb.show(SCREEN, 20)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				for wave in waves:
					wave.induce(0.5)
			if event.key == pygame.K_q:
				done = True
	pygame.display.flip()
	clock.tick(FRAME_RATE)
