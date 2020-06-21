import pygame
import sys
from waveform import Wave

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

while not done:
	SCREEN.fill((0, 0, 0))
	for wave in waves:
		wave.update(0.9)
		wave.show(SCREEN, 540)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				for wave in waves:
					wave.induce(0.5)
	pygame.display.flip()
	clock.tick(FRAME_RATE)
