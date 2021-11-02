import pygame as pg
import sys
from pygame.locals import *

class Punto:
	def __init__(self,superficie):
		self.superficie=superficie
		self.coorX=""
		self.coorY=""
		self.variable1=""
		self.memoria_punto=[]

		

	def coordenadas(self):
		tupla_coor=(self.coorX,self.coorY)
		return tupla_coor

	def crear_punto(self):
		self.variable1=True
		x,y=pg.mouse.get_pos()
		self.coorX,self.coorY=x,y
		self.memoria_punto.append((self.coorX,self.coorY))

	def dibujar_punto(self):
		if self.variable1==True:
			pg.draw.circle(self.superficie,(11,15,15),(self.coorX,self.coorY),10,1)
			self.variable1=False

	def memoria_puntos(self):
		valor=0
		for i in self.memoria_punto:
			coorXY=self.memoria_punto[valor]
			pg.draw.circle(self.superficie,(11,15,15),coorXY,10,1)
			valor=valor+1

	def lista_puntos(self):
		memoria=self.memoria_punto
		return memoria
				
	def borrar_punto(self):
		pass

	def crear_superficie(self):
		pass		 
