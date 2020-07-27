class textInput():
	def __init__(self):
		self.string = ''
		self.cursor = 0
		self.charSpecial = {
			'`' : '~',
			'1' : '!',
			'2' : '@',
			'3' : '#',
			'4' : '$',
			'5' : '%',
			'6' : '^',
			'7' : '&',
			'8' : '*',
			'9' : '(',
			'0' : ')',
			'-' : '_',
			'=' : '+',
			'[' : '{',
			']' : '}',
			'\\' : '|',
			';' : ':',
			'\'' : '"',
			',' : '<',
			'.' : '>',
			'/' : '?'
			}

	def insert(self, string):
		self.string = self.string[:self.cursor] + string + self.string[self.cursor:]
		self.cursor += 1

	def eventHandler(self, events):
		for event in events:
			if event.type == pygame.KEYDOWN:
				key = event.key
				if key >= 97 and key <= 122:
					mods = pygame.key.get_mods()
					shift = bool(mods & pygame.KMOD_SHIFT)
					caps = bool(mods & pygame.KMOD_CAPS)
					if shift ^ caps : key -= 32
					self.insert(chr(key))

				if key == 32 : self.insert(chr(key))

				if key in [ord(k) for k in self.charSpecial.keys()]:
					char = chr(key)
					mods = pygame.key.get_mods()
					if mods & pygame.KMOD_SHIFT:
						char = self.charSpecial[char]
					self.insert(char)

				if key == pygame.K_BACKSPACE:
					if self.cursor == 0: return
					self.string = self.string[:self.cursor-1] + self.string[self.cursor:]
					self.cursor -= 1

				if key == pygame.K_DELETE:
					if self.cursor == len(self.string): return
					self.string = self.string[:self.cursor] + self.string[self.cursor+1:]

				if key == pygame.K_LEFT:
					self.cursor -= 1
					if self.cursor < 0: self.cursor = 0

				if key == pygame.K_RIGHT:
					self.cursor += 1
					if self.cursor > len(self.string): self.cursor = len(self.string)

				if key == pygame.K_HOME: self.cursor = 0
				if key == pygame.K_END: self.cursor = len(self.string)
				print(self.string)

	def show(self):
		print(self.string)


import pygame

pygame.init()
SCREEN = pygame.display.set_mode((375, 100))

done = False
clock = pygame.time.Clock()
FRAME_RATE = 120
box = textInput()

while not done:
	SCREEN.fill((0, 0, 0))
	box.eventHandler(pygame.event.get())
	# for event in pygame.event.get():
	# 	if event.type == pygame.KEYDOWN:
	# 		print(event.key)
	# 		print(pygame.K_END)
	pygame.display.flip()
	clock.tick(FRAME_RATE)