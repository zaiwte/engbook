import pygame as pg
import sys
from pygame.locals import *
import sheet

class Line:
	def __init__(self):
		self.START = ()
		self.END = ()
		self.VAR = None
		self.MOVE = False
		self.lines_register = {}
		self.num_lines = 0

	def ID_line(self):
		self.num_lines += 1
		return f'L{self.num_lines}'

	def start_line(self):
		self.VAR = True
		self.START = pg.mouse.get_pos()

	def end_line(self):
		self.VAR = False
		self.END = pg.mouse.get_pos()
		self.lines_register[self.ID_line()] = {'LINE': {'START': self.START,'END': self.END},
										    'W': 3,
										    'C': (15, 15, 15)}

	def draw_line(self,surface):
		if self.VAR:
			pg.draw.line(surface,(15,15,255),self.START, pg.mouse.get_pos(), 3)






