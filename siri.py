import pygame
import threading

from elements.dock import Dock
from elements.textbox import Textbox
from elements.chatwindow import ChatWindow

from modules.recognizer import Recognizer
from modules.modelchatbot import ChatBot

pygame.init()
SCREEN = pygame.display.set_mode((375, 667))
pygame.display.set_caption('u/siri')

done = False
clock = pygame.time.Clock()
FRAME_RATE = 120

dock = Dock((375, 100))
chatwindow = ChatWindow((20, 20), (335, 580))
recognizer = Recognizer()
chatbot = ChatBot()

def chatThread():
	global recognizer, dock, chatwindow, chatbot, thread

	recognizer.record()
	dock.stopListening()
	text, stopLoading = recognizer.decode()

	tb = Textbox(325, 20)
	tb.setstr1(text)
	chatwindow.addScreen(tb.getSurface())
	chatwindow.setRemoveKey()

	if stopLoading:
		dock.stopLoading()
		thread = threading.Thread(target=chatThread)
		return

	tb = tb.copy()
	tb.setstr2(chatbot.query(text))
	dock.stopLoading()
	chatwindow.addScreen(tb.getSurface())

	thread = threading.Thread(target=chatThread)
	return

thread = threading.Thread(target=chatThread)

while not done:
	SCREEN.fill((0, 0, 0))

	SCREEN.blit(dock.getSurface(), (0, 580))
	SCREEN.blit(chatwindow.getSurface(), (20, 20))

	events = pygame.event.get()
	chatwindow.eventHandler(events)
	dockResponse = dock.eventHandler(events)
	if dockResponse == 'listen' and not thread.is_alive():
		thread.start()

	for event in events:
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q:
				exit()
			if event.key == pygame.K_v:
				dock.stopListening()
			if event.key == pygame.K_r:
				dock.stopLoading()
			if event.key == pygame.K_t:
				dock.stopTyping()
	pygame.display.flip()
	clock.tick(FRAME_RATE)
