import pygame
import win32gui
import win32con
import win32api
import ctypes
import sys

pygame.init()
window_name = '.'.join(sys.argv[0].split('.')[:-1])
pygame.display.set_caption(window_name if window_name != '' else 'pygame')
pygame.display.set_icon(pygame.image.load('resources/images/mic.png'))
SCREEN = pygame.display.set_mode((400, 400), pygame.NOFRAME)
done = False
clock = pygame.time.Clock()
FRAME_RATE = 120

hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 0), 200, win32con.LWA_ALPHA)

dwm = ctypes.windll.dwmapi

class attrData(ctypes.Structure):
	_fields_ = [("AccentState", ctypes.c_double),
				("AccentFlags", ctypes.c_double),
				("GradientColor", ctypes.c_double),
				("AnimationId", ctypes.c_double)
				]

accent = attrData(4, 2, 0x01<<24, 0)
print(ctypes.sizeof(accent))
dwm.DwmSetWindowAttribute(hwnd, 0x13, ctypes.byref(accent), ctypes.sizeof(accent))

while not done:
	SCREEN.fill((0, 0, 0))
	pygame.draw.rect(SCREEN, (0, 255, 0), (50, 50, 20, 20))
	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q:
				done = True
	pygame.display.flip()
	clock.tick(FRAME_RATE)