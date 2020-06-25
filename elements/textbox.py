import pygame

pygame.font.init()
fontMedium = pygame.font.Font('resources/fonts/medium.ttf', 30)
fontThin = pygame.font.Font('resources/fonts/thin.ttf', 24)

class Textbox():

	def __init__(self, width, margin=20):
		self.margin = margin
		self.width = width
		self.screens1 = []
		self.screens2 = []

	@staticmethod
	def appendSurfaces(surface1, surface2, fontHeight):
		SURFACE = pygame.Surface((surface1.get_width(), surface1.get_height() + fontHeight))
		SURFACE.blit(surface1, (0, 0))
		SURFACE.blit(surface2, (0, surface1.get_height()))
		return SURFACE

	@staticmethod
	def textwrap(string:str, font:pygame.font.Font, limit, margin):
		words = string.split()
		i = 0
		before = 0
		newline = ''
		out = []
		while i < len(words):
			word = words[i]
			after = before + font.size(word)[0]
			if after < margin:
				newline += word + ' '
				before = after + font.size(' ')[0]
			else:
				if before > limit:
					i -= 1
				else:
					for j in range(len(word)):
						if before + font.size(word[:j])[0] > margin:
							newline += word[:j-1] + '-'
							words.insert(i + 1, word[j-1:])
							break
				out.append(newline)
				before = 0
				newline = ''
			i += 1
		out.append(newline)
		return out

	def setstr1(self, str1:str):
		self.string1 = str1
		self.screens1 = [fontMedium.render(line, True, (255, 255, 255)) for line in self.textwrap(str1, fontMedium, self.width - 3 * self.margin, self.width - 2 * self.margin)]

	def setstr2(self, str2:str):
		self.string2 = str2
		self.screens2 = [fontThin.render(line, True, (255, 255, 255)) for line in self.textwrap(str2, fontThin, self.width - 4 * self.margin, self.width - 2 * self.margin)]

	def getSurface(self):
		SCREEN = pygame.Surface((self.width, fontMedium.get_linesize()))
		SCREEN.blit(self.screens1[0], (0, 0))
		for scr in self.screens1[1:]:
			SCREEN = self.appendSurfaces(SCREEN, scr, fontMedium.get_linesize())
		for scr in self.screens2:
			SCREEN = self.appendSurfaces(SCREEN, scr, fontThin.get_linesize())
		return SCREEN
