import math
import numpy

class Asterisco:

    def __init__(self, matriz, link_x, link_y, meta_x, meta_y):
        mov_disp = []
        movimiento = []

        while True:

            if link_x == meta_x and link_y == meta_y:
                self.mov = [None]
                break

            if link_y-1 >= 0:
                up = matriz[link_y-1][link_x] + Asterisco.calulo_manhatan(link_x, link_y-1, meta_x, meta_y)
                mov_disp+=[up]

            else:
                up = None

            if link_y + 1 <= len(matriz)-1:
                down = matriz[link_y+1][link_x] + Asterisco.calulo_manhatan(link_x, link_y+1, meta_x, meta_y)
                mov_disp+=[down]

            else:
                down = None

            if link_x + 1 <= len(matriz[0])-1:
                rigth = matriz[link_y][link_x+1] + Asterisco.calulo_manhatan(link_x+1, link_y, meta_x, meta_y)
                mov_disp+=[rigth]

            else:
                rigth = None

            if link_x - 1 >= 0 :
                left = matriz[link_y][link_x-1] + Asterisco.calulo_manhatan(link_x-1, link_y, meta_x, meta_y)
                mov_disp+=[left]
            else:
                left = None


            #Diccionario con movimientos disponibles
            movements = {left : "l", down : "d", rigth: "r", up : "u"}

            #Ordenar matriz de posibles movimientos
            a = numpy.array([mov_disp])
            a.sort(axis=1)
            mov_ordenados = a[0]
            movimiento += movements.get(mov_ordenados[0])

            a = []
            mov_disp = []

            #Actualizar posocion link
            if movements.get(mov_ordenados[0]) == "l":
                matriz[link_y][link_x] += 1
                link_x -= 1
            if movements.get(mov_ordenados[0]) == "d":
                matriz[link_y][link_x] += 1
                link_y += 1
            if movements.get(mov_ordenados[0]) == "r":
                matriz[link_y][link_x] += 1
                link_x += 1
            if movements.get(mov_ordenados[0]) == "u":
                matriz[link_y][link_x] += 1
                link_y -= 1
            mov_ordenados = []

        self.mov = movimiento



    def calulo_manhatan(link_x, link_y, meta_x, meta_y):
        manhatan=math.ceil(math.fabs(link_x - meta_x)) + math.ceil(math.fabs(link_y - meta_y))
        return manhatan


