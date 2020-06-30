import pygame
from pygame.locals import MOUSEWHEEL
from .textbox import Textbox

class ChatWindow():
	def __init__(self, position, dimensions):
		self.width, self.height = dimensions
		self.position = position
		self.screens = [pygame.Surface(dimensions)]
		pygame.draw.circle(self.screens[0], (0, 0, 255), (self.width // 2, self.height // 2), 30)
		textSurace = pygame.font.Font('resources/fonts/thin.ttf', 56).render('u/Siri', True, (255, 255, 255))
		textRect = textSurace.get_rect()
		textRect.center = (self.width // 2, self.height // 3)
		self.screens[0].blit(textSurace, textRect)
		self.screens[0].blit(pygame.image.load('resources/images/bottom.png'), (0, 512))
		self.scrollLimit = 0
		self.scrollPosition = 0
		self.removeBeforePosting = False
		self.mode = 'idle'

	def eventHandler(self, events:pygame.event.EventType):
		if self.mode == 'idle':
			for event in events:
				if event.type == MOUSEWHEEL:
					x, y = pygame.mouse.get_pos()
					x -= self.position[0]
					y -= self.position[1]
					if x > 0 and x < self.width:
						if y > 0 and y < self.height:
							self.scrollPosition -= 20 * event.y
							self.scrollPosition = self.scrollPosition if self.scrollPosition < self.scrollLimit else self.scrollLimit
							self.scrollPosition = self.scrollPosition if self.scrollPosition > 0 else 0
		if self.mode == 'newPanel':
			self.scrollPosition += 20
			if self.scrollPosition >= self.scrollLimit:
				self.scrollPosition = self.scrollLimit
				self.mode = 'idle'

	def addScreen(self, screen:pygame.Surface):
		if self.removeBeforePosting:
			self.removeScreen()
			self.removeBeforePosting = False
		oldHeight = self.screens[-1].get_height()
		self.scrollLimit += oldHeight if oldHeight < self.height else self.height
		if screen.get_height() > self.height:
			self.scrollLimit += (screen.get_height() - self.height)
		self.screens.append(screen)
		if self.scrollLimit - self.scrollPosition > 400:
			self.scrollPosition = self.scrollLimit - 400
			self.mode = 'newPanel'
		else:
			self.scrollPosition = self.scrollLimit

	def setRemoveKey(self):
		self.removeBeforePosting = True

	def removeScreen(self):
		if len(self.screens) < 2: return
		height = self.screens[-2].get_height()
		self.scrollLimit -= height if height < self.height else self.height
		return self.screens.pop(-1)

	def getSurface(self):
		SCREEN = pygame.Surface((self.width, self.height))
		accumulator = -self.scrollPosition
		for screen in self.screens:
			bottomLoc = accumulator + screen.get_height()
			if (accumulator > 0 or bottomLoc > 0) and (accumulator < self.height or bottomLoc < self.height):
				SCREEN.blit(screen, (0, accumulator))
			accumulator = bottomLoc
		return SCREEN
