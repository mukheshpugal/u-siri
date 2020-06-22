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
	def get_gaussian(x_a, y_a, x_f):
		return lambda x : y_a * np.exp(-(x_f * (x - x_a))**2)

	@staticmethod
	def aa_point(screen, x, y, color):
		gfxdraw.pixel(screen, x, int(y), color + (int(255*(y - np.floor(y))),))
		gfxdraw.pixel(screen, x, int(y) + 1, color + (int(255*(np.ceil(y) - y)),))
		pass

	def show(self, screen : pygame.Surface):
		poly = pygame.Surface((self.width, self.amplitude))
		points = self.amplitude * self.points + np.ones_like(self.points)
		points *= self.get_gaussian(self.width / 2., 1, 4 / self.width)(np.arange(self.width))

		for x in range(self.width):
			y = points[x]
			gfxdraw.pixel(poly, x, int(y), self.color + (int(255 * (y - int(y))),))
			if y >= 1:
				gfxdraw.vline(poly, x, 0, int(y) - 1, self.color)

		screen.blit(pygame.transform.flip(poly, False, True), (0, 0), special_flags=pygame.BLEND_ADD)
		screen.blit(poly, (0, self.amplitude), special_flags=pygame.BLEND_ADD)

	def update(self, damp):
		self.points *= damp
		# self.points[self.points < 0.02] = 0.

	def induce(self, factor):
		randx = self.width / 8 + 3 * random.random() * self.width / 4
		randy = factor * (.5 + .5 * random.random())
		self.points += self.get_gaussian(randx, randy, 10 / self.width)(np.arange(self.width))
