#!/usr/bin/env python3

###########################################
# FP2021/2022 @ IST                       #
# Projeto 2 - O Prado                     #
# Alberto Abad                            #
# Graphic version                         #
###########################################

import sys
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import importlib.util


class PradoSimulator(tk.Frame):
    def __init__(self, master=None, config_filename=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.mapa = proj2.parse_config(config_filename)
        self.num_gen = 0 

        # Graphics dimensions
        self.mapa_size = proj2.obter_tamanho_x(self.mapa), proj2.obter_tamanho_y(self.mapa)
        self.cellsize =min((50, 600//max(self.mapa_size)))
        self.boxscoresize = 50

        # Load icon images
        self.icon_imgs = {"predador": "fox.png", "presa": "rabbit.png", "monte": "mountain.png"}
        self.load_icons()

        # Create widgets
        self.create_widgets()


    def load_icons(self):

        icons = dict()
        
        # Associate Icon Image to key
        for key in self.icon_imgs:
            img = Image.open(self.icon_imgs[key])
            icons[key] = {'img': ImageTk.PhotoImage(img.resize((self.cellsize, self.cellsize), Image.ANTIALIAS)),
                         'img_big': ImageTk.PhotoImage(img.resize((self.boxscoresize, self.boxscoresize), Image.ANTIALIAS))}
        
        self.icons = icons

    def create_widgets(self):
        
        # Board/map widget creation and drawing
        self.board = tk.Canvas(self,
                           width=self.mapa_size[0] * self.cellsize,
                           height=self.mapa_size[1] * self.cellsize)
        self.board.pack(side='left')
        self.draw_map()

        # Frame widget for the additional elements (boxscore and turn button)
        right_frame = tk.Frame(self)
        right_frame.pack(side=tk.RIGHT)

        # Create boxscore widget and draw it
        self.boxscore = tk.Canvas(right_frame,
                           width=4*self.boxscoresize,
                           height=5*self.boxscoresize)
        self.boxscore.pack(fill=tk.X, pady=10)
        self.draw_boxscore()

        # Create next turn butto widget and associate with callback function next_turn
        self.turn_button = tk.Button(right_frame, text="NEXT", font="Times 20 bold",
                              command=self.next_turn)
        self.turn_button.pack(fill=tk.X, pady=10)


    def draw_map(self):
        x, y = 0, 0
        for char in proj2.prado_para_str(self.mapa):
            if char == '\n':
                x, y = 0, y + 1
            else:
                if char in '+-|@':
                    char = "monte"
                    self.board.create_image(x * self.cellsize, y * self.cellsize,
                                            anchor=tk.NW, image=self.icons[char]['img'])
                    self.board.create_rectangle(x * self.cellsize, y * self.cellsize,
                                                (x + 1) * self.cellsize, (y + 1) * self.cellsize,
                                                fill="")
                elif char == '.':
                    self.board.create_rectangle(x * self.cellsize, y * self.cellsize,
                                                (x + 1) * self.cellsize, (y + 1) * self.cellsize,
                                                fill="white")
                else:
                    char = "predador" if char.isupper() else "presa"
                    self.board.create_image(x * self.cellsize, y * self.cellsize,
                                            anchor=tk.NW, image=self.icons[char]['img'])
                    self.board.create_rectangle(x * self.cellsize, y * self.cellsize,
                                                (x + 1) * self.cellsize, (y + 1) * self.cellsize,
                                                fill="")
                x = x + 1

    def draw_boxscore(self):
        self.boxscore.delete("all")

        pos_y = 0
        keys = "predador", "presa"
        scores = proj2.obter_numero_predadores(self.mapa), proj2.obter_numero_presas(self.mapa)
        
        self.boxscore.create_text(self.boxscoresize/4, pos_y, anchor=tk.NW, font="Times 40 italic bold", text="GEN. #{}".format(self.num_gen))
        pos_y += 1.5*self.boxscoresize

        for key, score in zip(keys, scores):
            self.boxscore.create_image(self.boxscoresize / 4, pos_y, anchor=tk.NW, image=self.icons[key]['img_big'])
            self.boxscore.create_text(2*self.boxscoresize, pos_y + self.boxscoresize/4,
                                      anchor=tk.NW, font="Times 40 italic bold",
                                      text=str(score))
            pos_y += self.boxscoresize
            self.boxscore.create_text(self.boxscoresize/4, pos_y, anchor=tk.NW, font="Times 20 italic bold", text=key)
            pos_y += self.boxscoresize

    def next_turn(self):
        # mapa_old = cria_copia_mapa(self.mapa)
        proj2.geracao(self.mapa)
        self.num_gen += 1
        self.draw_map()
        self.draw_boxscore()



if __name__ == '__main__':

    usage = '''    O Prado GUI - FP2021/2022 @ IST, Alberto Abad, 2021   
    Inteface gráfica simples para o segundo projeto de FP basedo em Tkinter.
    '''

    usage += '''
    ATENÇÃO: A solução do projeto, para além de todas as funções do enunciado,
             precisa de conter a função parse_config: str --> prado, que recebe
             o nome de um ficheiro de configuração e devolve o prado correspondente.
    
    '''
    usage += 'Usage: ' + sys.argv[0] + ' codigo_projeto config_file\n'


    if len(sys.argv) != 3:
        print(usage)
        exit()

    # Load Project
    proj2_spec = importlib.util.spec_from_loader("proj2", loader=None)
    proj2 = importlib.util.module_from_spec(proj2_spec)
    exec(open(sys.argv[1], encoding="utf-8").read(), proj2.__dict__)

    if 'parse_config' not in proj2.__dict__:
        print(usage)
        exit()

    root = tk.Tk()
    root.title("O Prado - FP2021/2022 @ IST, Alberto Abad, 2021")
    app = PradoSimulator(master=root, config_filename=sys.argv[2])
    app.mainloop()

