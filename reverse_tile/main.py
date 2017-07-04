# -*- coding: utf8 -*-
import kivy
kivy.require('1.0.6') # replace with your current kivy version !
from kivy.app import App
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.clock import Clock
from math import fabs
from copy import deepcopy
from functools import partial
from os import sep
import random
import main


# -*- coding: utf-8 -*-
import random
from itertools import groupby


class Celula():
    def __init__(self, endereco, razao=-1):
        self.endereco = endereco
        self.trechos = []
        self.razao = razao

    def __unicode__(self):
        return self.endereco


class Trecho():
    def __init__(self, origem, destino):
        self.destino = destino
        self.origem = origem
        self.recompensa = 0


def criar_trechos(mapa):
    for x in range(0, len(mapa)):
        for y in range(0, len(mapa[x])):
            if y < len(mapa[x]) - 1:
                mapa[x][y].trechos.append(Trecho(mapa[x][y], mapa[x][y + 1]))
                mapa[x][y+1].trechos.append(Trecho(mapa[x][y+1], mapa[x][y]))

            if x < len(mapa) - 1:
                mapa[x][y].trechos.append(Trecho(mapa[x][y], mapa[x+1][y]))
                mapa[x+1][y].trechos.append(Trecho(mapa[x+1][y], mapa[x][y]))


def aprendizagem(trecho):
    ''' Aplica o calculo para propagação do conhecimento '''
    aprendizagem = trecho.destino.razao + 0.5 * (
        max(trecho.destino.trechos, key=lambda x: x.recompensa).recompensa)
    trecho.recompensa = aprendizagem


def escolhe_trecho_otimo(celula):
    return max(celula.trechos, key=lambda x: x.recompensa).destino


def escolhe_trecho(celula, promissores=False):

    if promissores:
        trecho_promissor = max(celula.trechos, key=lambda x: x.recompensa)
        trechos_iguais = [
            trecho for trecho in celula.trechos
            if trecho.recompensa == trecho_promissor.recompensa
        ]
        trecho_escolhido = random.choice(trechos_iguais)
        aprendizagem(trecho_escolhido)
        return trecho_escolhido.destino
    else:
        trecho_escolhido = random.choice(celula.trechos)
        aprendizagem(trecho_escolhido)
        return trecho_escolhido.destino


def inicia_trajetoria(celula_robo, celula_objetivo):

    trajetoria = []
    while True:
        chance = random.random()

        trajetoria.append(celula_robo)
        celula_robo = escolhe_trecho(celula_robo, chance < 0.7)

        # print u'%s = ' % celula_robo.endereco

        if celula_robo == celula_objetivo:
            return trajetoria
            break


def inicia_trajetoria_otimo(celula_robo, celula_objetivo):
    trajetoria = []
    while True:
        trajetoria.append(celula_robo)
        celula_robo = escolhe_trecho_otimo(celula_robo)

        if celula_robo == celula_objetivo:
            return trajetoria
            break


def main(*args, **kwargs):
    celula_inicial = Celula(1)
    celula_final = Celula(50, 100)
    mapa = [[Celula(5), Celula(6), Celula(15), Celula(16), Celula(25),
             Celula(26), Celula(35), Celula(36), Celula(45), Celula(46)],

            [Celula(4), Celula(7), Celula(14), Celula(17), Celula(24),
             Celula(27), Celula(34), Celula(37), Celula(44), Celula(47)],

            [Celula(3), Celula(8), Celula(13), Celula(18), Celula(23),
             Celula(28), Celula(33), Celula(38), Celula(43), Celula(48)],

            [Celula(2), Celula(9), Celula(12), Celula(19), Celula(22),
             Celula(29), Celula(32), Celula(39), Celula(42), Celula(49)],

            [celula_inicial, Celula(10, -100), Celula(11, -100),
             Celula(20, -100), Celula(21, -100), Celula(30, -100),
             Celula(31, -100), Celula(40, -100), Celula(41, -100),
             celula_final]]

    criar_trechos(mapa)

    print '\n'
    for areas in mapa:
        area = ''
        for celula in areas:
            area += '%s ' % celula.endereco
        print area + '\n'
    print '\n'

    for episodio in range(0, 100):
        inicia_trajetoria(celula_inicial, celula_final)

    for areas in mapa:
        for celula in areas:
            for trecho in celula.trechos:
                label = Label(text='%s - %s = %s' % (
                    trecho.origem, trecho.destino, trecho.recompensa))
                args[0].parent.parent.layout_2.add_widget(label)


    from IPython import embed; embed()

    trajetoria = inicia_trajetoria_otimo(celula_inicial, celula_final)
    print [t.endereco for t in trajetoria]


# main()



#todo : better locking, lock when it is flipping and when is computer turn
#todo : flip sound
#todo : show hint
#todo : check if resume game not faulty

Window.size=(800, 600)

TEXTURES = {}
TEXTURES['empty'] = Image(source="image%sempty.png" % sep).texture
for i in range(0,6):
    TEXTURES['black%i' % i] = Image(source="image%sblack%i.png" % (sep,i) ).texture
    TEXTURES['white%i' % i] = Image(source="image%swhite%i.png" % (sep,i) ).texture


def swap(s1, s2):
    return s2, s1

class tile(Image):
    current_flipping=0
    def __init__(self,**kwargs):
        self.rev_x = kwargs['rev_x']
        self.rev_y = kwargs['rev_y']
        self.caller_instance = kwargs['rev_caller']
        super(Image, self).__init__(**kwargs)
        self.toggle_texture(kwargs['rev_content'],' ')

    def on_touch_down(self,touch):
        if self.caller_instance.b_wait:
            return True

        if self.collide_point(*touch.pos):
            self.caller_instance.play(int(self.rev_x),int(self.rev_y))
            return True

    def my_callback(self,dt):
        if len(self.fip_seq) == self.flip_state:
            self.flip_state -=1
        self.texture = TEXTURES[self.fip_seq[self.flip_state]]

        self.flip_state += 1
        if len(self.fip_seq) == self.flip_state:
            tile.current_flipping -=1
            return False        #end the scheduling


    def toggle_texture(self,s_texture,s_previous_texture):
        if s_previous_texture == ' ':
            if s_texture == 'O':
                self.texture = TEXTURES['white0']
            elif s_texture =='X':
                self.texture = TEXTURES['black0']
            else:
                self.texture = TEXTURES['empty']

def divide_screen():
    x = Window.width
    y = Window.height

    if x>y:
        x,y = swap(x,y)

    grid_width = x
    menu_width = y-x
    return grid_width,menu_width


class Play_ground(Widget):
    b_wait = False

    def __init__(self, **kwargs):
        super(Play_ground, self).__init__(**kwargs) #constructeur du parent
        self.caller_instance = kwargs['caller_instance']
        self.resume = ''

        self.new_grid()

    def new_game(self,instance):
        self.resume = ''
        self.new_grid()

    def new_grid(self):
        grid_width,menu_width = divide_screen()

        self.player ='O'

        self.grid = [[' ' for x in xrange(50)] for x in xrange(50)]
        self.grid[1][4]='X'
        self.grid[2][4]='X'
        self.grid[3][4]='X'
        self.grid[4][4]='X'
        self.grid[5][4]='X'
        self.grid[6][4]='X'
        self.grid[7][4]='X'
        self.grid[8][4]='X'

        # self.grid[4][4]='O'
        # self.grid[3][4]='X'
        # self.grid[4][3]='X'

        # if self.resume == '':
        #     self.grid[3][3]='O'
        #     self.grid[4][4]='O'
        #     self.grid[3][4]='X'
        #     self.grid[4][3]='X'
        # else:
        #     idx = 0
        #     for y in range(0,8):
        #         for x in range(0,8):
        #             self.grid[y][x]=self.resume[idx]
        #             idx += 1
        self.previous_grid = deepcopy(self.grid)

        self.label_score = Label(text='Tabela Q')

        # graphic grid
        self.clear_widgets()
        self.graphical_grid = GridLayout(
            cols=10, size=(grid_width, grid_width/2), x=0+10, y=grid_width/2-10)
        for y in range(0,5):
            for x in range(0,10):
                tiloun = tile(rev_x = x, rev_y =y, rev_caller = self,
                              rev_content = self.grid[x][y])
                self.graphical_grid.add_widget(tiloun)


        # from IPython import embed; embed()

        self.add_widget(self.graphical_grid)
        #control panel
        self.layout = BoxLayout(orientation='vertical',
                  x=grid_width+15,y=grid_width-50,width = menu_width-30, height=40
                           )

        self.layout_2 = BoxLayout(orientation='horizontal',
                  x=0,y=300-100, width = Window.width
                           )

        btn1 = Button(text='Iniciar', size=(50,50))
        btn1.bind(on_press=main)
        self.layout.add_widget(btn1)
        self.layout_2.add_widget(self.label_score)
        self.add_widget(self.layout)
        self.add_widget(self.layout_2)

    def display(self):
        for child in self.graphical_grid.children:
            if self.grid[int(child.rev_x)][int(child.rev_y)] != self.previous_grid[int(child.rev_x)][int(child.rev_y)]:
                child.toggle_texture(self.grid[int(child.rev_x)][int(child.rev_y)],self.previous_grid[int(child.rev_x)][int(child.rev_y)])

    def in_grid_boundary(self,x,y):
        if x<0 or x>7 or y<0 or y>7:
            return False
        return True

    def reverse(self,x,y):

        self.previous_grid = deepcopy(self.grid)
        self.grid[x][y] = self.player

    def play(self,x,y):

        if  self.in_grid_boundary(x,y) == False or self.grid[x][y] <>' ':
            return False

        #update logical grid
        self.reverse(x,y)

        #display logical grid
        self.display()


class MyApp(App):
    # def build_config(self, config):
    #     config.setdefaults('section1', {'difficulty': 'easy','resume':''})

    # def on_stop(self):
    #     resume = ''
    #     for y in range(0,8):
    #         for x in range(0,8):
    #             resume += self.game.grid[y][x]
    #     resume = resume.replace(' ','_')
    #     self.config.set('section1', 'resume', resume)
    #     self.config.write()



    def build(self):
        self.game = Play_ground(caller_instance= self)
        return self.game

if __name__ in ( '__main__'):
    MyApp().run()
