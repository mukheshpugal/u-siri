import pygame
import sys
from elements.dock import Dock
from elements.textbox import Textbox
from elements.chatwindow import ChatWindow
import win32gui
import win32api
import win32con
from pygame.locals import MOUSEWHEEL

pygame.init()
window_name = '.'.join(sys.argv[0].split('.')[:-1])
pygame.display.set_caption(window_name if window_name != '' else 'pygame')
pygame.display.set_icon(pygame.image.load('resources/images/mic.png'))
SCREEN = pygame.display.set_mode((375, 667))
done = False
clock = pygame.time.Clock()
FRAME_RATE = 120
dock = Dock((375, 100))
cw = ChatWindow((20, 20), (335, 570))
tb = Textbox(335, 20)
tb.setstr1("HHH")
tb.setstr2("Hi there! What can I do for you? brrrrr")

while not done:
	SCREEN.fill((0, 0, 0))
	dock.update()
	SCREEN.blit(dock.getSurface(), (0, 580))
	# SCREEN.blit(tb.getSurface(), (20, 20))
	SCREEN.blit(cw.getSurface(), (20, 20))
	# SCREEN.blit(tb.getSurface(), (20, 300))
	# pygame.draw.rect(SCREEN, (0, 255, 0), (20, 20, 335, 570))
	events = pygame.event.get()
	dock.eventHandler(events)
	cw.eventHandler(events)
	for event in events:
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q:
				done = True
			if event.key == pygame.K_v:
				dock.stopListening()
			if event.key == pygame.K_r:
				dock.stopLoading()
			if event.key == pygame.K_t:
				dock.stopTyping()
			if event.key == pygame.K_s:
				cw.addScreen(tb.getSurface().copy())
			if event.key == pygame.K_a:
				cw.removeScreen()
	pygame.display.flip()
	clock.tick(FRAME_RATE)
