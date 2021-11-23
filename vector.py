import numpy as np

class Vector:
    def __init__(self):
        self.register_vertors = {}
        self.num_vector = 0
        self.coor = {}

    def ID_vector(self):
        self.num_vector += 1
        return f'V{self.num_lines}'

    def add_vector(self,distance,START,angle):
        x = round(distance * np.cos(angle))
        y = round(distance * np.sin(angle))
        END = (START[0]+x,START[1]+y)
        self.coor = {'START':START,'END':END}

    def coor_vector(self):
        return self.coor

