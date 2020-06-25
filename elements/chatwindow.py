import pygame
from pygame.locals import MOUSEWHEEL
from .textbox import Textbox

class ChatWindow():
	def __init__(self, dimensions, position):
		self.width, self.height = dimensions
		self.position = position
		self.screens = [pygame.Surface(dimensions)]
		pygame.draw.circle(self.screens[0], (0, 255, 0), (self.width // 2, self.height // 2), 30)
		self.scrollLimit = 0
		self.scrollPosition = 0

	def eventHandler(self, events:pygame.event.EventType):
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				x, y = pygame.mouse.get_pos()
				x -= self.position[0]
				y -= self.position[1]
				if x > 0 and x < self.width:
					if y > 0 and y < self.height: 		
						if event.button == 4:
							self.scrollPosition -= 5
						if event.button == 5:
							self.scrollPosition += 5
						self.scrollPosition = self.scrollPosition if self.scrollPosition < self.scrollLimit else self.scrollLimit
						self.scrollPosition = self.scrollPosition if self.scrollPosition > 0 else 0

	def addScreen(self, screen:pygame.Surface):
		oldHeight = self.screens[-1].get_height()
		self.scrollLimit += oldHeight if oldHeight < self.height else self.height
		if screen.get_height() > self.height:
			self.scrollLimit += (screen.get_height() - self.height)
		self.screens.append(screen)

	def removeScreen(self):
		pass

	def getSurface(self):
		SCREEN = pygame.Surface((self.width, self.height))
		accumulator = -self.scrollPosition
		for screen in self.screens:
			bottomLoc = accumulator + screen.get_height()
			if (accumulator > 0 or bottomLoc > 0) and (accumulator < self.height or bottomLoc < self.height):
				SCREEN.blit(screen, (0, accumulator))
			accumulator = bottomLoc
		return

