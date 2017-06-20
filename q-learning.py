# -*- coding: utf-8 -*-

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


def main():
    mapa = [[Celula(5), Celula(6), Celula(15), Celula(16), Celula(25),
             Celula(26), Celula(35), Celula(36), Celula(45), Celula(46)],

            [Celula(4), Celula(7), Celula(14), Celula(17), Celula(24),
             Celula(27), Celula(34), Celula(37), Celula(44), Celula(47)],

            [Celula(3), Celula(8), Celula(13), Celula(18), Celula(23),
             Celula(28), Celula(33), Celula(38), Celula(43), Celula(48)],

            [Celula(2), Celula(9), Celula(12), Celula(19), Celula(22),
             Celula(29), Celula(32), Celula(39), Celula(42), Celula(49)],

            [Celula(1), Celula(10, -100), Celula(11, -100), Celula(20, -100),
             Celula(21, -100), Celula(30, -100), Celula(31, -100),
             Celula(40, -100), Celula(41, -100), Celula(50, 100)]]

    criar_trechos(mapa)
    # Teste

    print '\n'
    for areas in mapa:
        area = ''
        for celula in areas:
            area += '%s ' % celula.endereco
        print area + '\n'
    print '\n'

    from IPython import embed; embed()


main()
