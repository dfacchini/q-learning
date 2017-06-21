# -*- coding: utf-8 -*-
import random
from itertools import groupby

# TODO
# Criar estrutura para as recompensas
# Criar o caminho aleatoriamente


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
    aprendizagem = trecho.destino.razao + 0.5 * (max(trecho.destino.trechos, key=lambda x: x.recompensa).recompensa)
    trecho.recompensa = aprendizagem   

def escolhe_trecho_otimo(celula):
    return max(celula.trechos, key=lambda x: x.recompensa).destino

def escolhe_trecho(celula, promissores=False):

    if promissores:
        trecho_promissor = max(celula.trechos, key=lambda x: x.recompensa)
        trechos_iguais = [trecho for trecho in celula.trechos if trecho.recompensa == trecho_promissor.recompensa]
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

    # print u'\n Quantidade de passos: %s \n' % cont
    # print [t.endereco for t in trajetoria]

def inicia_trajetoria_otimo(celula_robo, celula_objetivo):
    trajetoria = []
    while True: 
        trajetoria.append(celula_robo)
        celula_robo = escolhe_trecho_otimo(celula_robo)

        # print u'%s = ' % celula_robo.endereco  

        if celula_robo == celula_objetivo:
            return trajetoria
            break

def main():
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

            [celula_inicial, Celula(10, -100), Celula(11, -100), Celula(20, -100),
             Celula(21, -100), Celula(30, -100), Celula(31, -100),
             Celula(40, -100), Celula(41, -100), celula_final]]

    criar_trechos(mapa)    

    print '\n'
    for areas in mapa:
        area = ''
        for celula in areas:
            area += '%s ' % celula.endereco
        print area + '\n'
    print '\n'

    for i in range(0, 100):
        inicia_trajetoria(celula_inicial, celula_final)

    from IPython import embed; embed()
    trajetoria = inicia_trajetoria_otimo(celula_inicial, celula_final)
    print [t.endereco for t in trajetoria]
    #from IPython import embed; embed()


main()
