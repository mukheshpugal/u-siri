import pygame
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((640,480))
clock = pygame.time.Clock()

def main():
   while True:
      for event_var in pygame.event.get():
      		if event_var.type == QUIT:
      			pygame.quit()
      			return
      		if event_var.type == MOUSEWHEEL:
      			print(event_var) # can access properties with prop notation
                                # (ex: event_var.y)
   clock.tick(60)

# Execute game:
main()