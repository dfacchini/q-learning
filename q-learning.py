# -*- coding: utf-8 -*-
import random
import datetime
from itertools import groupby


class Celula():
    def __init__(self, endereco, razao=-1):
        self.endereco = endereco
        self.estados = []
        self.razao = razao

    def __unicode__(self):
        return self.endereco


class Estado():
    def __init__(self, origem, destino):
        self.destino = destino
        self.origem = origem
        self.recompensa = 0


def criar_estados(mapa):
    for x in range(0, len(mapa)):
        for y in range(0, len(mapa[x])):
            if y < len(mapa[x]) - 1:
                mapa[x][y].estados.append(Estado(mapa[x][y], mapa[x][y + 1]))
                mapa[x][y+1].estados.append(Estado(mapa[x][y+1], mapa[x][y]))

            if x < len(mapa) - 1:
                mapa[x][y].estados.append(Estado(mapa[x][y], mapa[x+1][y]))
                mapa[x+1][y].estados.append(Estado(mapa[x+1][y], mapa[x][y]))


def aprendizagem(estado):
    ''' Aplica o calculo para propagação do conhecimento '''
    aprendizagem = estado.destino.razao + 0.5 * (
        max(estado.destino.estados, key=lambda x: x.recompensa).recompensa)
    estado.recompensa = aprendizagem


def escolhe_estado_otimo(celula):
    return max(celula.estados, key=lambda x: x.recompensa).destino


def escolhe_estado(celula, promissores=False):

    if promissores:
        estado_promissor = max(celula.estados, key=lambda x: x.recompensa)
        estados_iguais = [
            estado for estado in celula.estados
            if estado.recompensa == estado_promissor.recompensa
        ]
        estado_escolhido = random.choice(estados_iguais)
        aprendizagem(estado_escolhido)
        return estado_escolhido.destino
    else:
        estado_escolhido = random.choice(celula.estados)
        aprendizagem(estado_escolhido)
        return estado_escolhido.destino


def inicia_trajetoria(celula_robo, celula_objetivo):

    trajetoria = []
    while True:
        chance = random.random()

        trajetoria.append(celula_robo)
        celula_robo = escolhe_estado(celula_robo, chance < 0.7)

        # print u'%s = ' % celula_robo.endereco

        if celula_robo == celula_objetivo:
            return trajetoria
            break


def inicia_trajetoria_otimo(celula_robo, celula_objetivo):
    trajetoria = []
    while True:
        trajetoria.append(celula_robo)
        celula_robo = escolhe_estado_otimo(celula_robo)

        if celula_robo == celula_objetivo:
            trajetoria.append(celula_objetivo)
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

            [celula_inicial, Celula(10, -100), Celula(11, -100),
             Celula(20, -100), Celula(21, -100), Celula(30, -100),
             Celula(31, -100), Celula(40, -100), Celula(41, -100),
             celula_final]]

    criar_estados(mapa)

    print '\n'
    for areas in mapa:
        area = ''
        for celula in areas:
            if len(str(celula.endereco)) == 2:
                area += '%s ' % celula.endereco
            else:
                area += '%s  ' % celula.endereco
        print area + '\n'
    print '\n'

    t = datetime.datetime.now()
    arquivo = open("result_%s.txt" % t, "wb")

    for episodio in range(0, 50):
        trajetoria = inicia_trajetoria(celula_inicial, celula_final)
	print 'Passos ep. %s' % len(trajetoria)
    #arquivo.write(str([t.endereco for t in trajetoria]))

    arquivo.write('\n Tabela Q \n\n')
    print '\n Tabela Q \n\n'
    for areas in mapa:
        for celula in areas:
            for estado in celula.estados:
                if len(str(estado.origem.endereco)) == 2:
                    origem = 'Origem(%s) ' % estado.origem.endereco
                else:
                    origem = 'Origem(%s)  ' % estado.origem.endereco

                resultado = '%s| Razão(%s) = %s\n' % (
                    origem,
                    estado.destino.endereco,
                    estado.recompensa)
                print resultado
                arquivo.write(resultado);

    arquivo.close()

    trajetoria = inicia_trajetoria_otimo(celula_inicial, celula_final)
    print [t.endereco for t in trajetoria]

    print '\n'
    for areas in mapa:
        area = ''
        for celula in areas:
            if celula in trajetoria:
                area += 'x  '
            else:
                if len(str(celula.endereco)) == 2:
                    area += '%s ' % celula.endereco
                else:
                    area += '%s  ' % celula.endereco
        print area + '\n'
    print '\n'


main()
