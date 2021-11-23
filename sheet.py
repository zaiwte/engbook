import pygame as pg
import sys
from pygame.locals import *
#from typing import Dict,Tuple

class Sheet:
	def __init__(self,size):
		self.size = size
		self.ox = int(self.size[0] / 2)
		self.oy = int(self.size[1] / 2)
		self.origin = (self.ox, self.oy)
		self.move = False
		self.domx = 0  # DISTANCIA DEL ORIGEN A LA POSICION DEL MOUSE EN X
		self.domy = 0  # DISTANCIA DEL ORIGEN A LA POSICION DEL MOUSE EN Y
		self.vax = 0  #
		self.vay = 0  #
		self.center = (int(self.ox + self.vax), int(self.oy + self.vay))
		self.draw:dict = {}
		self.register_dpm: dict = {}
		self.plane_register: dict = {}
		self.zoom = 100
		self.plane(self.origin, 'R1', self.zoom)

	def plane(self,o,name,S,C=(100,100,100)):
		""""
			name = 'name'
			conf = {'x':{'separation':npixel},
				    'y':{'separation':npixel},
				    'color':(r,g,b)
				    'jumpL':[n,(r,g,b)]}
		"""
		num = 0
		line = {
			    'X': {
					  'start': {'x': 0, 'y': o[1]},
					    'end': {'x':self.size[0], 'y': o[1]},
					      'M': (0, 1),
					      'var': o[1],
						'limit': self.size[1]
					  },
				'Y': {
					  'start': {'x': o[0], 'y': 0},
					    'end': {'x': o[0], 'y': self.size[1]},
					      'M': (1, 0),
					      'var': o[0],
					    'limit':self.size[0]

				      }
				     }

		for axis in line:
			while (line[axis]['var'] - S * num) >= 0:
				sn = S * num
				START = (line[axis]['start']['x'] - line[axis]['M'][0] * sn,
						 line[axis]['start']['y'] - line[axis]['M'][1] * sn)

				END = (line[axis]['end']['x'] - line[axis]['M'][0] * sn,
					   line[axis]['end']['y'] - line[axis]['M'][1] * sn)

				self.plane_register[f'{name}{axis}_N{num}'] = {'LINE': {'START':START, 'END':END},
														  'W': 1,
														  'C': C}
				num += 1
			num = 0
			while (line[axis]['var'] + S * num) <= line[axis]['limit']:
				sn = S * num
				START = (line[axis]['start']['x'] + line[axis]['M'][0] * sn,
						 line[axis]['start']['y'] + line[axis]['M'][1] * sn)

				END = (line[axis]['end']['x'] + line[axis]['M'][0] * sn,
					   line[axis]['end']['y'] + line[axis]['M'][1] * sn)

				self.plane_register[f'{name}{axis}_P{num}'] = {'LINE': {'START': START, 'END': END},
																'W': 1,
																'C': C}
				num += 1
			num = 0

	def zoom_plane(self,z):
		if self.zoom < 200 and self.zoom > 50:
			mx, my = pg.mouse.get_pos()
			domx = -1 * (mx - self.ox)
			domy = -1 * (my - self.oy)
			self.zoom += z
			#self.origin = (self.ox + domx + self.zoom, self.oy + domy + self.zoom,)
			self.plane_register = {}
			self.plane(self.origin, 'R1', self.zoom)
		else:
			self.zoom = 100
			self.plane_register = {}
			self.plane(self.origin, 'R1', self.zoom)


	def clear(self,ID):
		del self.register[ID]

	def get(self,ID):
		if ID in self.draw.keys():
			return self.register[ID]
	#('ID',{'LINE':{'START':(x,y),'END':(x,y)},'W':1})
	#('ID',{'POINT':(x,y)})

	def pencil(self,ID,newPoint):
		if ID not in self.draw.keys():
			self.draw[ID] = newPoint

	def move_sheet(self,list_registers):
		self.move = True
		mx, my = pg.mouse.get_pos()
		self.domx = mx - self.ox
		self.domy = my - self.oy

		for register in list_registers:
			for key in register:
				START = register[key]['LINE']['START']
				END = register[key]['LINE']['END']
				dpmstart = (mx - START[0], my - START[1]) #distacia punto al mouse comienzo
				dpmend = (mx - END[0], my - END[1])# ""          "" final
				self.register_dpm[key] = {"dpmSTART": dpmstart, "dpmEND": dpmend}

	def stop_sheet(self):
		self.move=False
		#self.plane_register = {}
		self.plane(self.origin, 'R1', self.zoom)

	def update(self,list_register):
		if self.move:
			mx, my = pg.mouse.get_pos()
			self.ox = mx - self.domx
			self.oy = my - self.domy
			self.origin = (self.ox, self.oy)
			self.center = (int(self.ox + self.vax), int(self.oy + self.vay))

			self.plane_register = {}
			self.plane(self.origin, 'R1', self.zoom)

			for register in list_register:
				for key in register:
					dmpstart = self.register_dpm[key]['dpmSTART']
					dmpend = self.register_dpm[key]['dpmEND']

					START = (mx - dmpstart[0], my - dmpstart[1])
					END = (mx - dmpend[0], my - dmpend[1])

					W = register[key]['W']
					C = register[key]['C']
					register[key] = {'LINE': {'START': START, 'END': END},
														   'W': W,
														   'C': C}

	def show(self,surface,register):
		#self.register: dict = {'draw':self.draw}
		for dicc in register:
			for key in dicc.keys():
				reg = dicc[key]
				#print(reg)
				pg.draw.line( surface,
							 reg['C'],
							 reg['LINE']['START'],
							 reg['LINE']['END'],
							 reg['W'])

	@property
	def list_ID(self):
		return [l for l in self.draw.keys()]


	"""						if (line[axis]['limit'] - S * (num + 1)) < 0:
							self.plane_register[f'{name}{axis}{i}T'] = {'LINE': {'START': START, 'END': END},
																			'W': 2,
																			'C': (200, 10, 10)}"""