import pygame as pg
import numpy as np
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
		self.axis_plane = {}
		#self.plane(self.origin, 'R1', self.zoom)
		self.axis_register = {}
		self.axis()
		self.xz = 0
		self.yz = 0
		self.zoom_xy = (self.xz,self.yz)

	def axis(self):

		D = {'U':{'dis':self.origin[1]},
			 'D':{'dis':self.size[1] - self.origin[1]},
			 'R':{'dis':self.size[0] - self.origin[0]},
			 'L':{'dis':self.origin[0]}}
		G = {
			 'X':{'O': 0,
				  'lim':self.size[0],
				  'dir': {'R': 1,
						  'L':-1}
			 	  },
			 'Y':{'O': 1,
				  'lim':self.size[1],
				  'dir': {'U':-1,
						  'D': 1}
				  }
			 }
		dicc = {}
		for AXIS in G:
			for d in G[AXIS]['dir']:
				if D[d]['dis'] > 0:
					dicc2 = {}
					ol = list(self.origin)
					for k in range(1, round((D[d]['dis'] / self.zoom) + 1)):
						ol[G[AXIS]['O']] = self.origin[G[AXIS]['O']]
						ol[G[AXIS]['O']] = ol[G[AXIS]['O']] + (k * self.zoom * G[AXIS]['dir'][d])
						dicc2[k * self.zoom] = tuple(ol)
					dicc[d] = dicc2

				else:
					print(D[d]['dis'])
			self.axis_register[AXIS] = dicc
			dicc = {}
		print(self.axis_register)


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
					    'end': {'x':600, 'y': o[1]},
					      'M': (0, 1),
					      'var': o[1],
						'limit': 600
					  },
				'Y': {
					  'start': {'x': o[0], 'y': 0},
					    'end': {'x': o[0], 'y': 600},
					      'M': (1, 0),
					      'var': o[0],
					    'limit':600

				      }
				     }
		index_for = {'X':1,'Y':0}
		dicc = {}
		for axis in line:
			# >= 0
			while (line[axis]['var'] - S * num) >= 125 and (line[axis]['var'] + S * num) <= 625 :
				sn = S * num
				START = (line[axis]['start']['x'] - line[axis]['M'][0] * sn,
						 line[axis]['start']['y'] - line[axis]['M'][1] * sn)

				END = (line[axis]['end']['x'] - line[axis]['M'][0] * sn,
					   line[axis]['end']['y'] - line[axis]['M'][1] * sn)

				self.plane_register[f'{name}{axis}_N{num}'] = {'LINE': {'START':START, 'END':END},
														  'W': 1,
														  'C': C}
				dicc[line[axis]["M"][index_for[axis]] * sn] = ( o[0] + (line[axis]["M"][0] * sn) , o[1] + (line[axis]["M"][1] * sn) )
				num += 1
			num = 0
			#line[axis]['limit']
			while (line[axis]['var'] - S * num) >= 125 and (line[axis]['var'] + S * num) <= 625:
				sn = S * num
				START = (line[axis]['start']['x'] + line[axis]['M'][0] * sn,
						 line[axis]['start']['y'] + line[axis]['M'][1] * sn)

				END = (line[axis]['end']['x'] + line[axis]['M'][0] * sn,
					   line[axis]['end']['y'] + line[axis]['M'][1] * sn)

				self.plane_register[f'{name}{axis}_P{num}'] = {'LINE': {'START': START, 'END': END},
																'W': 1,
													            'C': C}
				dicc[-1*line[axis]["M"][index_for[axis]] * sn] = ( o[0] + (-1*line[axis]["M"][0] * sn) , o[1] + (-1*line[axis]["M"][1] * sn) )
				num += 1
			num = 0
			self.axis_plane[axis] = dicc
			dicc = {}
			#print(self.axis_plane)

	def zoom_plane(self,z):
		if self.zoom < 200 and self.zoom > 50:
			mx, my = pg.mouse.get_pos()
			ndomx = -1 * (mx - self.ox)
			ndomy = -1 * (my - self.oy)
			dis = round(np.linalg.norm([ndomx, ndomy]), 2)
			self.xz = round((z*2) * (ndomx/dis))
			self.yz = round((z*2) * (ndomy/dis))
			self.zoom_xy = (self.xz, self.yz)
			self.ox = self.ox + self.xz
			self.oy = self.oy + self.yz
			self.origin = (self.ox, self.oy)

			self.zoom += z
			self.axis()
		else:
			self.zoom = 100
			self.axis()

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
		#self.plane(self.origin, 'R1', self.zoom)
		self.axis()

	def update(self,list_register):
		if self.move:
			mx, my = pg.mouse.get_pos()
			self.ox = mx - self.domx
			self.oy = my - self.domy
			self.origin = (self.ox, self.oy)
			self.center = (int(self.ox + self.vax), int(self.oy + self.vay))

			#self.plane_register = {}
			#self.plane(self.origin, 'R1', self.zoom)
			self.axis()

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

	def show_point(self,surface,register):
		for dicc in register:
			for key in dicc.keys():
				reg = dicc[key]
				pg.draw.circle(surface, reg['C'],reg['POINT'], reg['W'])

	@property
	def list_ID(self):
		return [l for l in self.draw.keys()]


	"""						if (line[axis]['limit'] - S * (num + 1)) < 0:
							self.plane_register[f'{name}{axis}{i}T'] = {'LINE': {'START': START, 'END': END},
																			'W': 2,
																			'C': (200, 10, 10)}"""