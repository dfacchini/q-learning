# -*- coding: utf-8 -*-
import random
import datetime


class Estado():
    def __init__(self, endereco, razao=-1):
        self.endereco = endereco
        self.acoes = []
        self.razao = razao

    def __unicode__(self):
        return self.endereco


class Acao():
    def __init__(self, origem, destino):
        self.destino = destino
        self.origem = origem
        self.recompensa = 0


def criar_acoes(mapa):
    for x in range(0, len(mapa)):
        for y in range(0, len(mapa[x])):
            if y < len(mapa[x]) - 1:
                mapa[x][y].acoes.append(Acao(mapa[x][y], mapa[x][y + 1]))
                mapa[x][y+1].acoes.append(Acao(mapa[x][y+1], mapa[x][y]))

            if x < len(mapa) - 1:
                mapa[x][y].acoes.append(Acao(mapa[x][y], mapa[x+1][y]))
                mapa[x+1][y].acoes.append(Acao(mapa[x+1][y], mapa[x][y]))


def aprendizagem(acao):
    ''' Aplica o calculo para propagação do conhecimento '''
    aprendizagem = acao.destino.razao + 0.5 * (
        max(acao.destino.acoes, key=lambda x: x.recompensa).recompensa)
    acao.recompensa = aprendizagem


def escolhe_acao_otima(estado):
    return max(estado.acoes, key=lambda x: x.recompensa).destino


def escolhe_acao(estado, promissores=False):

    if promissores:
        acao_promissora = max(estado.acoes, key=lambda x: x.recompensa)
        acoes_iguais = [
            acao for acao in estado.acoes
            if acao.recompensa == acao_promissora.recompensa
        ]
        acao_escolhida = random.choice(acoes_iguais)
        aprendizagem(acao_escolhida)
        return acao_escolhida.destino
    else:
        acao_escolhida = random.choice(estado.acoes)
        aprendizagem(acao_escolhida)
        return acao_escolhida.destino


def inicia_trajetoria(estado_robo, estado_objetivo):

    trajetoria = []
    while True:
        chance = random.random()

        trajetoria.append(estado_robo)
        estado_robo = escolhe_acao(estado_robo, chance < 0.7)

        if estado_robo == estado_objetivo:
            return trajetoria
            break


def inicia_trajetoria_otima(estado_robo, estado_objetivo):
    trajetoria = []
    while True:
        trajetoria.append(estado_robo)
        estado_robo = escolhe_acao_otima(estado_robo)

        if estado_robo == estado_objetivo:
            trajetoria.append(estado_objetivo)
            return trajetoria
            break


def main():
    estado_inicial = Estado(1)
    estado_final = Estado(50, 100)
    mapa = [[Estado(5), Estado(6), Estado(15), Estado(16), Estado(25),
             Estado(26), Estado(35), Estado(36), Estado(45), Estado(46)],

            [Estado(4), Estado(7), Estado(14), Estado(17), Estado(24),
             Estado(27), Estado(34), Estado(37), Estado(44), Estado(47)],

            [Estado(3), Estado(8), Estado(13), Estado(18), Estado(23),
             Estado(28), Estado(33), Estado(38), Estado(43), Estado(48)],

            [Estado(2), Estado(9), Estado(12), Estado(19), Estado(22),
             Estado(29), Estado(32), Estado(39), Estado(42), Estado(49)],

            [estado_inicial, Estado(10, -100), Estado(11, -100),
             Estado(20, -100), Estado(21, -100), Estado(30, -100),
             Estado(31, -100), Estado(40, -100), Estado(41, -100),
             estado_final]]

    criar_acoes(mapa)

    print '\n'
    for areas in mapa:
        area = ''
        for estado in areas:
            if len(str(estado.endereco)) == 2:
                area += '%s ' % estado.endereco
            else:
                area += '%s  ' % estado.endereco
        print area + '\n'
    print '\n'

    t = datetime.datetime.now()
    arquivo = open("result_%s.txt" % t, "wb")

    for episodio in range(0, 50):
        trajetoria = inicia_trajetoria(estado_inicial, estado_final)
        print 'Passos ep. %s' % len(trajetoria)

    arquivo.write('\n Tabela Q \n\n')
    print '\n Tabela Q(Ações) \n\n'

    for areas in mapa:
        for estado in areas:
            for acao in estado.acoes:
                if len(str(acao.origem.endereco)) == 2:
                    origem = 'Origem(%s) ' % acao.origem.endereco
                else:
                    origem = 'Origem(%s)  ' % acao.origem.endereco

                if len(str(acao.destino.endereco)) == 2:
                    destino = 'Destino(%s) ' % acao.destino.endereco
                else:
                    destino = 'Destino(%s)  ' % acao.destino.endereco

                resultado = '%s| %s = %s\n' % (
                    origem,
                    destino,
                    acao.recompensa)
                print resultado
                arquivo.write(resultado)

    arquivo.close()

    trajetoria = inicia_trajetoria_otima(estado_inicial, estado_final)

    print u'\n\n Política Ótima(Conjunto de estados) \n'
    print [tr.endereco for tr in trajetoria]

    print '\n'
    for areas in mapa:
        area = ''
        for estado in areas:
            if estado in trajetoria:
                area += 'x  '
            else:
                if len(str(estado.endereco)) == 2:
                    area += '%s ' % estado.endereco
                else:
                    area += '%s  ' % estado.endereco
        print area + '\n'
    print '\n'


main()
