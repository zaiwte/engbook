import pygame as pg
import numpy as np
import sys,random,time
import os
from pygame.locals import *
import PySimpleGUI as sg
import line
import sheet
import planeXY
import visualize
import vector

class Engbook:
    def __init__(self):

        self.line = line.Line()
        self.buttons_name = ['PENCIL', 'MOVE', 'punto', 'vector', 'circulo', 'arco']
        self.screensize = sg.Window.get_screen_size()
        self.visualize = visualize.View()
        self.vector = vector.Vector()

    def printDicct(self,dic):
        for d in dic:
            print(d)

    def gui(self):
        layout = [
            [sg.Button('PENCIL'), sg.Button('MOVE'), sg.Button('punto'), sg.Button('vector'), sg.Button('circulo'),
             sg.Button('arco')],
            [sg.Graph((self.screensize[0], self.screensize[1]), (0, 0), (200, 200), background_color="black", key='-GRAPH-')]
                ]
        return layout

    def show(self):
        button_act = None

        window = sg.Window('engbook', self.gui(), finalize=True, resizable=True)

        graph = window['-GRAPH-']
        embed = graph.TKCanvas
        os.environ['SDL_WINDOWID'] = str(embed.winfo_id())

        pg.init()
        screen = pg.display.set_mode((self.screensize[0], self.screensize[1]))
        screen.fill((255, 255, 255))

        #self.plane.size = window['-GRAPH-'].get_size()
        #self.sheet.size = window['-GRAPH-'].get_size()
        self.sheet = sheet.Sheet(window['-GRAPH-'].get_size())


        while True:
            event, value = window.read(timeout=10)

            if event == sg.WIN_CLOSED:
                #self.printDicct(self.sheet.plane_register)
                break

            if event in self.buttons_name:
                for k in self.buttons_name:
                    window[k].update(button_color=sg.theme_button_color())
                window[event].update(button_color=('white', 'red'))
                button_act = event

            #PYGAME
            for evento in pg.event.get():
                if evento.type == QUIT:
                    pass

                elif evento.type == MOUSEBUTTONDOWN:
                    if evento.button == 1:

                        if button_act == 'PENCIL':
                            self.line.start_line()

                        elif button_act == 'MOVE':
                            self.sheet.move_sheet([self.line.lines_register])
                            #self.sheet.plane_register,

                    elif evento.button == 4:
                        self.sheet.zoom_plane(10)

                    elif evento.button == 5:
                        self.sheet.zoom_plane(-10)

                elif evento.type == MOUSEBUTTONUP:
                    if evento.button == 1:

                        if button_act == 'PENCIL':
                            self.line.end_line()

                        elif button_act == 'MOVE':
                            self.sheet.stop_sheet()



            screen.fill((255, 255, 255))

            self.sheet.show(screen,[self.sheet.plane_register,
                                    self.line.lines_register])

            pg.draw.circle(screen, (200, 0, 0), self.sheet.center, 10, 1)
            pg.draw.circle(screen, (0, 200, 0), self.sheet.origin, 10)

            mx, my = pg.mouse.get_pos()
            domx = mx - self.sheet.ox
            domy = my - self.sheet.oy
            ndomx = -1*(mx - self.sheet.ox)
            ndomy = -1*(my - self.sheet.oy)
            #x = ndomx + self.sheet.ox + self.sheet.zoom
            x =self.sheet.ox + ndomx
            y = np.interp(x,[self.sheet.ox, self.sheet.ox + ndomx],[self.sheet.oy, self.sheet.oy + ndomy])

            pg.draw.circle(screen, (0, 200, 0), (ndomx + self.sheet.ox,ndomy + self.sheet.oy), 10)
            #pg.draw.circle(screen, (0, 200, 200), (self.sheet.ox + x,self.sheet.oy + round(y)), 8)

            self.vector.add_vector(np.linalg.norm([domx,domy]),self.sheet.origin,np.pi)
            pg.draw.circle(screen, (0, 200, 200), self.vector.coor_vector()['END'], 8)
            self.visualize.view(screen,{'pantalla':window['-GRAPH-'].get_size(),
                                        'mouse':pg.mouse.get_pos(),
                                        'center':self.sheet.origin,
                                        'zoom':self.sheet.zoom,
                                        'dom':(domx,domy),
                                        'VEC':self.vector.coor_vector()['END'],
                                        'distance':np.linalg.norm([domx,domy])},s=50)

            #BUTTONS GUI
            if button_act == 'PENCIL':
                self.line.draw_line(screen)

            elif button_act == 'MOVE':
                self.sheet.update([self.line.lines_register])

            pg.display.update()


        pg.quit()
        window.close()

def main():
    Engbook().show()
main()


