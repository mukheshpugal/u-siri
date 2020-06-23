import pygame
import pyaudio
import numpy as np
from .waveform import Wave
from webbrowser import open as wOpen

pygame.font.init()
typing = pygame.font.Font('resources/fonts/thin.ttf', 28).render('typing...', True, (255, 255, 255))
imageMic = pygame.transform.smoothscale(pygame.image.load('resources/images/mic.png'), (30, 30))
imageKBoard = pygame.transform.smoothscale(pygame.image.load('resources/images/keyboard.png'), (30, 30))
imageHelp = pygame.transform.smoothscale(pygame.image.load('resources/images/help.png'), (24, 24))

class Dock():

	def __init__(self, dimensions):
		self.mode = 'listening'
		self.dimensions = dimensions
		width, height = dimensions
		self.mic = pyaudio.PyAudio().open(format=pyaudio.paFloat32, channels=1, rate=44100, input=True, frames_per_buffer=1024)

		self.waves = []
		self.waves.append(Wave(height / 2, (255, 0, 0), width))
		self.waves.append(Wave(height / 2, (0, 255, 0), width))
		self.waves.append(Wave(height / 2, (0, 0, 255), width))

	def eventHandler(self, events:pygame.event.EventType):
		if self.mode == 'idle':
			for event in events:
				if event.type == pygame.MOUSEBUTTONDOWN:
					x, y = pygame.mouse.get_pos()
					if y > 615 and y < 645:
						if x > 25 and x < 49:
							wOpen('https://github.com/mukheshpugal/u-siri')
						if x > 168 and x < 198:
							pass
						if x > 325 and x < 355:
							pass
		if self.mode == 'listening':
			for event in events:
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						for wave in self.waves:
							wave.induce(0.5)

		if self.mode == 'typing':
			pass

	def update(self):
		if self.mode == 'listening':
			samples = self.mic.read(1024, exception_on_overflow=False)
			samples = np.frombuffer(samples, dtype=np.float32)[::2]
			volume = np.sum(samples**2)/len(samples)
			volume = volume**0.5/2
			for wave in self.waves:
				wave.induce(2*volume)
				wave.update(0.834)

	def show(self):
		SCREEN = pygame.Surface(self.dimensions)
		if self.mode == 'listening':
			for wave in self.waves:
				wave.show(SCREEN)
		if self.mode == 'idle':
			SCREEN.blit(imageMic, [x / 2 - 15 for x in self.dimensions])
			SCREEN.blit(imageKBoard, (self.dimensions[0] - 50, self.dimensions[1] / 2 - 15))
			SCREEN.blit(imageHelp, (25, self.dimensions[1] / 2 - 12))
		if self.mode == 'typing':
			SCREEN.blit(typing, (20, self.dimensions[1] / 2 - typing.get_height() / 2))
		return SCREEN
