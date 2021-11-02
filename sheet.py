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

	def ruler(self):
		pass

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

	def move_sheet(self,register):
		self.move = True
		mx, my = pg.mouse.get_pos()
		self.domx = mx - self.ox
		self.domy = my - self.oy
		for key in register:
			START = register[key]['LINE']['START']
			END = register[key]['LINE']['END']
			dpmstart = (mx - START[0], my - START[1]) #distacia punto al mouse comienzo
			dpmend = (mx - END[0], my - END[1])# ""          "" final
			self.register_dpm[key] = {"dpmSTART": dpmstart, "dpmEND": dpmend}


	def stop_sheet(self):
		self.move=False

	def update(self,register):
		if self.move:
			mx, my = pg.mouse.get_pos()
			self.ox = mx - self.domx
			self.oy = my - self.domy
			self.origin = (self.ox, self.oy)
			self.center = (int(self.ox + self.vax), int(self.oy + self.vay))

			if (self.center[0] > (self.size[0])):
				self.vax = self.vax - self.size[0]

			elif (self.center[0] < 0):
				self.vax = self.vax + self.size[0]

			elif (self.center[1] > (self.size[1])):
				self.vay = self.vay - self.size[1]

			elif (self.center[1] < 0):
				self.vay = self.vay + self.size[1]

			else:
				pass

			for key in register.keys():
				dmpstart = self.register_dpm[key]['dpmSTART']
				dmpend = self.register_dpm[key]['dpmEND']

				START = (mx - dmpstart[0], my - dmpstart[1])
				END = (mx - dmpend[0], my - dmpend[1])

				register[key] = {'LINE': {'START': START, 'END': END},
													   'W': 3,
													   'C': (15, 15, 15)}

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