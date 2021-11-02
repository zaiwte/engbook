import pygame as pg
import sys
from pygame.locals import *

class Plane:
	def __init__(self,size):
		self.size=size
		self.ox=self.size[0]/2
		self.oy=self.size[1]/2
		self.domx=0 #DISTANCIA DEL ORIGEN A LA POSICION DEL MOUSE EN X
		self.domy=0 #DISTANCIA DEL ORIGEN A LA POSICION DEL MOUSE EN Y
		self.origin=(self.ox,self.oy)
		self.move=False
		self.vax=0 #
		self.vay=0 #
		self.center=((self.ox+self.vax),(self.oy+self.vay))
		self.plane_register:dict = {}

	def plane(self,o,name,conf):
		""""

			name = 'name'
			conf = {'x':{'separation':npixel},
				    'y':{'separation':npixel},
				    'color':(r,g,b)
				    'jumpL':[n,(r,g,b)]}

			if not num%jnum:
				color = conf['jumpL'][1]
			else:
				color = conf['color']
		"""
		num = 0
		line = { 'X':{'start':{'x':o[0] - self.size[0],'y':o[1]},
					  'end':{'x':o[0] + self.size[0],'y':o[1]},'M':(0,1)},
		         'Y':{'start':{'x':o[0],'y':o[1] - self.size[1]},
					  'end':{'x':o[0],'y':o[1] + self.size[1]},'M':(1,0)}}
		interv = {'A': 1, 'B': -1}
		limit = {'X':(o[1] ,o[1] + self.size[1]),
				 'Y':(o[0] ,o[0] + self.size[0])}

		for axis in line:
			while True:
				if (limit[axis][0] + (conf[axis]['separation']*num))>(limit[axis][1]):
					break
				for i in interv:

					sn = conf[axis]['separation'] * num * interv[i]
					START = (line[axis]['start']['x'] + line[axis]['M'][0] * sn,
							 line[axis]['start']['y'] + line[axis]['M'][1] * sn)

					END  =  (line[axis]['end']['x'] + line[axis]['M'][0] * sn,
							 line[axis]['end']['y'] + line[axis]['M'][1] * sn)

					self.plane_register[f'{name}{axis}{i}{num}'] = {'LINE': {'START':START, 'END':END},
													          'W': 1,
													          'C': conf['color']}
				num += 1
			num = 0


	def ver_ejes_XY(self):
		miFuente=pg.font.Font(None,23)
		R=self._rejillas_C( (self.centro[0], self.centro[1]), (self._ancho, self._alto)  )
		# cada regilla debe tener centro con coordenada para fijar posicion de ellos en la pantalla
		o=miFuente.render(str(self.origen) + " origen",0,(105,5,5))
		self._superficie.blit(o,self.centro)

	def move_plane(self):
		self.move=True
		mx,my=pg.mouse.get_pos()
		#distancia origen moues xy--->domx, domy
		self.domx=mx-self.ox
		self.domy=my-self.oy

	def stop_plane(self):
		self.move=False

	def draw_plane(self):
		if self.move:
			#miFuente=pg.font.Font(None,25)
			mx,my=pg.mouse.get_pos()
			self.ox=mx-self.domx
			self.oy=my-self.domy
			self.origin=(self.ox,self.oy)
			self.center=((self.ox+self.vax), (self.oy+self.vay))

			if (self.center[0]>(self.size[0])):
				self.vax=self.vax-self.size[0]

			elif (self.center[0]<0):
				self.vax=self.vax+self.size[0]

			elif (self.center[1]>(self.size[1])):
				self.vay=self.vay-self.size[1]

			elif (self.center[1]<0):
				self.vay=self.vay+self.size[1]

			else:
				pass

			#o2=miFuente.render(str((self.vax,self.vay))+ ": vaxy",0,(5,100,5))
			#self._superficie.blit(o2,(0,0))

	def data_mouse(self,surface):
		font = pg.font.Font(None, 30)
		o = font.render("mouse:"+str(pg.mouse.get_rel()), 0, (10, 10, 10))
		surface.blit(o, (10,10))
		return pg.mouse.get_rel()

