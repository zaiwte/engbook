import numpy as np
import pygame as pg

class Vector:
    def __init__(self):
        self.register_vertors = {}
        self.num_vector = 0
        self.coor = {}

    def ID_vector(self):
        self.num_vector += 1
        return f'V{self.num_lines}'

    def add_vector(self,distance,START,angle):
        v = pg.math.Vector2().from_polar((int(distance),int(angle)))
        x = round(distance * np.cos(-1 * angle * (np.pi/180)))
        y = round(distance * np.sin(-1 * angle * (np.pi/180)))
        END = (START[0]+x,START[1]+y)
        self.coor = {'START':START,'END':END}

    def get_angle(self,END1,END2,START):
        n = (END1[0]-START[0], START[1]-END1[1])
        m = (END2[0]-START[0], START[1]-END2[1])
        n_norm = round(np.linalg.norm([n[0], n[1]]), 2)
        m_norm = round(np.linalg.norm([m[0], m[1]]), 2)
        nxm = np.dot(n,m)
        angle = np.arccos((nxm/(n_norm * m_norm)))
        if n[1] < 0:
            return round(360 - (angle * (180/np.pi)),2)
        else:
            return round(angle * (180 / np.pi),2)

    def coor_vector(self):
        return self.coor

