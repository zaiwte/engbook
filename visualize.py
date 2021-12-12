import pygame as pg
import sys
from pygame.locals import *

class View:
	def __init__(self):
		self.size = (0,0)


	def view_inf(self,surface,dicc_data,s=100,o=(25,25)):
		#up down left right
		'''{  UP:{name1:d1,name2:d2,name3:d3},
		    DOWN:{name1:d1,name2:d2,name3:d3},
		    LEFT:{name1:d1,name2:d2,name3:d3},
		   RIGHT:{name1:d1,name2:d2,name3:d3}}'''
		posy = o[1]
		font = pg.font.Font(None, 30)
		for d in dicc_data:
			view = font.render(f'{d} : {dicc_data[d]}',0,(10,10,10))
			pos = [o[0],posy]
			surface.blit(view,pos)
			posy = posy + s

	def view_axis(self,surface,dicc_data):
		font = pg.font.Font(None, 30)
		for AXIS in dicc_data:
			for D in dicc_data[AXIS]:
				for V in dicc_data[AXIS][D]:
					view = font.render(f'{V}',0,(40,40,40))
					surface.blit(view,dicc_data[AXIS][D][V])


	def data_mouse(self,surface):
		font = pg.font.Font(None, 30)
		o = font.render("mouse:"+str(pg.mouse.get_rel()), 0, (10, 10, 10))
		surface.blit(o, (10,10))
		return pg.mouse.get_rel()

	"""line = {
		'X': {
			'start': {'x': 0, 'y': o[1]},
			'end': {'x': self.size[0] / 2, 'y': o[1]},
			'M': (0, 1),
			'var': o[1],
			'limit': self.size[1] / 2
		},
		'Y': {
			'start': {'x': o[0], 'y': 0},
			'end': {'x': o[0], 'y': self.size[1] / 2},
			'M': (1, 0),
			'var': o[0],
			'limit': self.size[0] / 2

		}
	}"""