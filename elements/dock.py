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
		self.mode = 'idle'
		self.dimensions = dimensions
		width, height = dimensions
		self.mic = pyaudio.PyAudio().open(format=pyaudio.paFloat32, channels=1, rate=44100, input=True, frames_per_buffer=1024)

		self.waves = []
		self.waves.append(Wave(height / 2, (255, 0, 0), width))
		self.waves.append(Wave(height / 2, (0, 255, 0), width))
		self.waves.append(Wave(height / 2, (0, 0, 255), width))

		self.loadWave = Wave(height / 2, (255, 255, 255), width)
		self.loaderLocation = 0.5
		self.loaderDirection = True # Right if true

	def eventHandler(self, events:pygame.event.EventType):
		if self.mode == 'idle':
			for event in events:
				if event.type == pygame.MOUSEBUTTONDOWN:
					x, y = pygame.mouse.get_pos()
					if y > 615 and y < 645:
						if x > 25 and x < 49:
							# Info
							wOpen('https://github.com/mukheshpugal/u-siri')
						if x > 168 and x < 198:
							# Mic
							# pass
							self.mode = 'toListen'
							return 'listen'
						if x > 325 and x < 355:
							# Keyboard
							self.mode = 'typing'
							return 'keyboard'
		elif self.mode == 'listening':
			'''
			Press to terminate listening
			'''
			pass

	def stopListening(self):
		if self.mode == 'listening':
			self.mode = 'loading'

	def stopLoading(self):
		if self.mode == 'loading':
			self.mode = 'stopLoading'

	def stopTyping(self):
		if self.mode == 'typing':
			self.mode = 'idle'

	def update(self):
		if self.mode == 'listening':
			samples = self.mic.read(1024, exception_on_overflow=False)
			samples = np.frombuffer(samples, dtype=np.float32)[::2]
			volume = np.sum(samples**2)/len(samples)
			volume = 0. if volume < 0.005 else volume**0.2/5
			for wave in self.waves:
				wave.induce(volume)
				wave.update(0.85)
		if self.mode in ('loading', 'stopLoading'):
			velocity = 0.02 * (np.sin(self.loaderLocation * np.pi) + 0.1) * (1 if self.loaderDirection else -1)
			self.loaderLocation += velocity

			if self.loaderLocation >= 1:
				self.loaderDirection = not self.loaderDirection
				self.loaderLocation = 1.
			if self.loaderLocation <= 0:
				self.loaderDirection = not self.loaderDirection
				self.loaderLocation = 0.

			self.loadWave.load(2 * np.abs(velocity) + 0.01, self.loaderLocation, self.loaderDirection)

			if self.mode == 'stopLoading' and np.abs(velocity) > 0.02:
				self.mode = 'idle'
				self.loaderLocation = 0.5
				self.loaderDirection = True

		if self.mode == 'toListen':
			self.loaderLocation += 0.05
			self.loadWave.shift(0.5, self.loaderLocation)
			if self.loaderLocation >= 1:
				self.loaderLocation = 0.5
				self.mode = 'listening'

	def getSurface(self):
		SCREEN = pygame.Surface(self.dimensions)
		if self.mode == 'listening':
			for wave in self.waves:
				SCREEN.blit(wave.getSurface(), (0, 0), special_flags=pygame.BLEND_ADD)
		if self.mode in ('loading', 'toListen', 'stopLoading'):
			SCREEN.blit(self.loadWave.getSurface(False), (0, 0))
		if self.mode == 'idle':
			SCREEN.blit(imageMic, [x / 2 - 15 for x in self.dimensions])
			SCREEN.blit(imageKBoard, (self.dimensions[0] - 50, self.dimensions[1] / 2 - 15))
			SCREEN.blit(imageHelp, (25, self.dimensions[1] / 2 - 12))
		if self.mode == 'typing':
			SCREEN.blit(typing, (20, self.dimensions[1] / 2 - typing.get_height() / 2))
		return SCREEN
