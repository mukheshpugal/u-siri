import pygame
from pygame import gfxdraw
import numpy as np
import random

class Wave():
	def __init__(self, amplitude, color, width):
		self.amplitude = amplitude
		self.color = color
		self.width = width
		self.points = np.zeros(width)

	@staticmethod
	def get_gaussian(x_shift, y_amplitude, x_scale):
		return lambda x : y_amplitude * np.exp(-(x_scale * (x - x_shift))**2)

	@staticmethod
	def linearMap(x, a, b, c, d):
		return c + (x - a) * (d - c) / (b - a)

	def getSurface(self, trim=True):
		SCREEN = pygame.Surface((self.width, 2*self.amplitude))
		poly = pygame.Surface((self.width, self.amplitude))

		points = self.amplitude * self.points
		if trim:
			points += np.ones_like(self.points)
			points *= self.get_gaussian(self.width / 2., 1, 4 / self.width)(np.arange(self.width))

		for x in range(self.width):
			y = points[x]
			gfxdraw.pixel(poly, x, int(y), self.color + (int(255 * (y - int(y))),))
			if y >= 1:
				gfxdraw.vline(poly, x, 0, int(y) - 1, self.color + (255,))

		SCREEN.blit(pygame.transform.flip(poly, False, True), (0, 0))
		SCREEN.blit(poly, (0, self.amplitude))
		return SCREEN

	def update(self, damp):
		self.points *= damp

	def load(self, amplitude, position, isRight):
		offset = self.amplitude * amplitude
		pixelPosition = int(position * (self.width - 2 * offset) + offset)
		dist = self.width * np.sin(np.pi * pixelPosition / self.width) / 3
		self.points[:pixelPosition] = amplitude * (1 + (np.arange(pixelPosition) - pixelPosition) / (dist if isRight else  offset))
		self.points[pixelPosition:] = amplitude * (1 - np.arange(self.width - pixelPosition) / (offset if isRight else dist))

		self.points *= self.points > 0

	def shift(self, amplitude, position):
		'''
		Position goes from 0.5 to 1
		amp goes from amp to 1 linearly
		xwidth goes from 100/width to 4/width
		'''
		x_width = self.linearMap(position, 0.5, 1, 100 / self.width, 4 / self.width)
		amp = self.linearMap(position, 0.5, 1, amplitude, 1 / self.amplitude)
		self.points = self.get_gaussian(self.width // 2, amp, x_width)(np.arange(self.width))

	def induce(self, factor):
		randx = self.width / 8 + 3 * random.random() * self.width / 4
		randy = factor * (.5 + .5 * random.random())
		self.points += self.get_gaussian(randx, randy, 10 / self.width)(np.arange(self.width))
