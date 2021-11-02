import pygame as pg
import sys,random,time
import os
from pygame.locals import *
import PySimpleGUI as sg
import line
import sheet
import planeXY
import visualize

class Engbook:
    def __init__(self):

        self.line = line.Line()
        self.buttons_name = ['PENCIL', 'MOVE', 'punto', 'vector', 'circulo', 'arco']
        self.screensize = sg.Window.get_screen_size()

        self.visualize = visualize.View()

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
        self.plane = planeXY.Plane((400,300))

        while True:
            event, value = window.read(timeout=10)

            if event == sg.WIN_CLOSED:
                break

            if event in self.buttons_name:
                for k in self.buttons_name:
                    window[k].update(button_color=sg.theme_button_color())
                window[event].update(button_color=('white', 'red'))
                button_act = event

            #MOUSE
            for evento in pg.event.get():
                if evento.type == QUIT:
                    pass

                elif evento.type == MOUSEBUTTONDOWN:
                    if evento.button == 1:

                        if button_act == 'PENCIL':
                            self.line.start_line()

                        elif button_act == 'MOVE':
                            self.sheet.move_sheet(self.line.lines_register)


                elif evento.type == MOUSEBUTTONUP:
                    if evento.button == 1:

                        if button_act == 'PENCIL':
                            self.line.end_line()

                        elif button_act == 'MOVE':
                            self.sheet.stop_sheet()

            screen.fill((255, 255, 255))


            """self.plane.plane(self.sheet.center,'R1',{'X': {'separation':10},
                                   'Y': {'separation':10},
                                   'color': (180, 180, 180)})"""

            self.plane.plane(self.sheet.center,'R2',{'X': {'separation': 50},
                                   'Y': {'separation': 50},
                                   'color': (100, 100, 100)})

            self.sheet.show(screen,[self.plane.plane_register,
                                    self.line.lines_register])
            #self.plane.data_mouse(screen)

            pg.draw.circle(screen, (200, 0, 0), self.sheet.center, 10, 1)
            pg.draw.circle(screen, (0, 200, 0), self.sheet.origin, 10)


            self.visualize.view(screen,{'pantalla':window['-GRAPH-'].get_size(),
                                        'mouse':pg.mouse.get_pos(),
                                        'center':self.sheet.center})

            #pg.draw.line(screen, (10,10,10),(10, 10),vxy, 3)

            #print(f'rel :{pg.mouse.get_rel()[0],}')

            #BUTTONS GUI
            if button_act == 'PENCIL':
                self.line.draw_line(screen)

            elif button_act == 'MOVE':
                self.sheet.update(self.line.lines_register)


            pg.display.update()


        pg.quit()
        window.close()

def main():
    Engbook().show()
main()


