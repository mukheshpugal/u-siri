import pygame

class textbox():

	def setstr1(self, str1:str):
		self.string1 = str1

	def setstr2(self, str2:str):
		self.string2 = str2

	def show(self, screen:pygame.Surface):

		self.string1