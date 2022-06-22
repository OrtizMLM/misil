import random
import pygame
import numpy
import math

from GUI import *
from Asterisco import *

aleatorio = True

#tamaños
width=800
height=600
x=0
y=50

(ancho, alto)=(800 , 600)


#matriz tablero
global matrizTablero
matrizTablero=[]


# cargar img del suelo
sueloimg = []

# cargar img obtaculo
obsimg = []

global fantasmasimgx, fantasmasimgy, fantasmasimgrect, fantasmasimg
#fantasmas
fantasmasimg = []
fantasmasimgrect = []
fantasmasimgx=[]
fantasmasimgy=[]

cantidadfantasmas=3

player = pygame.image.load("./imgs/fantasma.png")
player = pygame.transform.scale(player, (50, 50))


#lugarllave
filallave=(alto // 50)-1
columnallave=(ancho // 50)-1

#lugarpuerta
filapuerta=(alto // 50) - 1
columnapuerta=0

# inicio del juego
def main(dimension, aleatorio, matrizPersonalizada, anchoPersonalizado, altoPersonalizado):
    if aleatorio == True:
        if dimension == "800 x 600":
            ancho = 800
            alto =600

        if dimension == "600 x 400":
            ancho = 600
            alto =400

        if dimension == "400 x 200":
            ancho = 400
            alto = 200
    else:
        ancho = anchoPersonalizado // 2
        alto = altoPersonalizado  // 2

    pygame.init()

    #Suelo
    suelo = pygame.image.load("./imgs/piso.png")
    obstaculo = pygame.image.load("./imgs/obstaculo.png")

    #Personaje Link
    link = pygame.image.load("./imgs/link1.png")
    link_x = random.randint(0, 2)
    link_y = random.randint(0, 2)
    i=0

    #LLave

    llave = pygame.image.load("./imgs/key.png")
    llave_x = random.randint(2, 7)
    llave_y = random.randint(2, 7)

    meta_x = llave_x
    meta_y = llave_y

    #Puerta

    puerta = pygame.image.load("./imgs/puerta.png")
    puerta_x = math.ceil(ancho/2)-50
    puerta_y = 0
    pygame.display.set_caption("Zelda")
    icon = pygame.image.load("./imgs/icon.png")
    pygame.display.set_icon(icon)


    screen = pygame.display.set_mode((ancho, alto))


    #para matriz
    filas = alto // 50
    columnas = ancho // 50


    #Loop principal
    running = True
    crearTablero = False
    crearfantasmas = False
    moverenemigos = True
    valorAnterior = 0

    busqueda1 = True
    global screenshot,fantasmasimgrect,fantasmasimg,cantidadfantasmas


    while running:

        #Crear mapa
        if crearTablero == False:
            global matrizTablero

            if aleatorio == True:
                matrizTablero = tablero(screen, ancho, alto)


                #Asignacion posicion puerta

                posPuerta = asignacion(matrizTablero, puerta_x, 0)
                puerta_x = posPuerta[0]
                puerta_y = 0

                #Asignacion posicion llave y puerta
                posLlave = asignacion(matrizTablero, llave_x, llave_y)
                llave_x = posLlave[0]
                llave_y = posLlave[1]

                screen.blit(llave, ((llave_x*50)+5, (llave_y*50)+5))
                screen.blit(puerta, (puerta_x-25 , puerta_y-9))

                #Asignacion posicion link

                posLink = asignacion(matrizTablero, link_x, link_y)
                link_x = posLink[0]
                llave_y = posLink[1]



                #Tomar fondo del juego
                screenshot = screen.copy()
                screen.blit(screenshot, (0, 0))


                screen.blit(link, (link_x * 50, link_y * 50))
                matrizTablero[link_y][link_x] = 2
                matrizTablero[llave_y][llave_x] = 4

                #Asignacion posici
                # on puerta

                matrizTablero[math.ceil(puerta_y*2/100)][math.ceil(puerta_x*2/100)] = 5

                #gasto de cada movimiento
                matrizGasto = numpy.zeros((len(matrizTablero),len(matrizTablero[0])))

                #Creacion de fantasmas
                CrearFantasmas(screenshot, matrizTablero, ancho,alto, cantidadfantasmas)



            else:
                matrizTablero = matrizPersonalizada
                matrizGasto = numpy.zeros((len(matrizTablero),len(matrizTablero[0])))
                personalizado = tableroPersonalizado(matrizPersonalizada, screen, suelo, obstaculo, llave, puerta, link, player)
                #CrearFantasmasPersonalizados( matrizTablero, ancho,alto)

                link_x = personalizado[0]
                link_y = personalizado[1]
                meta_x = personalizado[2]
                meta_y = personalizado[3]
                puerta_x = personalizado[4] * 50
                puerta_y = personalizado[5] * 50
                fantasmasimgx = personalizado[6]
                fantasmasimgy = personalizado[7]
                fantasmasimgrect = personalizado[8]
                cantidadfantasmas = personalizado[9]
                fantasmasimg = personalizado[10]

                screenshot = screen.copy()
                screen.blit(screenshot, (0, 0))
                screen.blit(link, (link_x, link_y))

        if link_x == meta_x and link_y == meta_y:
            matrizGasto = numpy.zeros((len(matrizTablero),len(matrizTablero[0])))
            meta_x = math.ceil(puerta_x/50)
            meta_y = math.ceil(puerta_y/50)
            #suelo1 = pygame.transform.scale(suelo, (97, 100))
            #screen.blit(suelo1, (link_x-24, link_y-24.8))
            #screenshot = screen.copy()
            #screen.blit(screenshot, (0, 0))


    #Actulizacion de matrices
        matrizGasto = matrizUpdate(matrizTablero, matrizGasto)
        matrizCopia = matrizGasto.copy()

        #Llamado a algorimto de busqueda Link
        global mov



        asterisco = Asterisco(matrizCopia, link_x, link_y, meta_x, meta_y)

        print (link_x)
        print (link_y)
        asterisco = Asterisco(matrizGasto, link_x, link_y, meta_x, meta_y)


        mov = asterisco.mov

        #Evento para cierre de ventana
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False


        #Movimientos de link

        if(mov == []):
            mov = [None]
            moverenemigos=False
        if crearTablero == True:
            movimiento = moverLink(mov[0], link_x, link_y, matrizTablero, matrizGasto, valorAnterior)
            link_x = movimiento[0]
            link_y = movimiento[1]
            matrizTablero = movimiento[2]
            matrizGasto = movimiento[3]
            valorAnterior = movimiento[4]
            screen.blit(screenshot, (0, 0))
            screen.blit(link, (link_x * 50, link_y * 50))


            # mover y pintar fantasmas
            #print(matrizTablero)
        print(matrizTablero)
        #print("cantidad fantasmas es : "+ str(cantidadfantasmas))

        if moverenemigos == True:
            for p in range(0, cantidadfantasmas):
                (fantasmasimgrect[p], a) = \
                    Profundidadsinciclos(fantasmasimgrect[p], matrizTablero, ancho, alto, link_y, link_x, llave_y,
                                         llave_x,puerta_y, puerta_x)
                screen.blit(fantasmasimg[p], fantasmasimgrect[p])



        crearTablero = True
        moverenemigos= True
        pygame.time.delay(500)
        pygame.display.update()

# tablero del juego
def tablero (screen, ancho, alto):
    # ciclo para suelo
    for j in range(0, (math.ceil(alto / 100)) * 2):
        for i in range(0, (math.ceil(ancho / 100)) * 2):
            sueloimg.append(pygame.image.load("./imgs/piso.png"))
            screen.blit(sueloimg[i], (i * 50 - 24, j * 50 - 25))

    # ciclo para obstaculos
    matrizObstaculos = numpy.zeros(((math.ceil(alto / 100)) * 2,
                                    (math.ceil(ancho / 100)) * 2), dtype=int)

    for x in range(0, math.ceil(alto / 100)):
        for z in range(0, (math.ceil(ancho / 100))):
            posicionX = random.randint(0, (math.ceil(ancho / 100)) * 2) * 50
            posicionY = random.randint(0, (math.ceil(ancho / 100)) * 2) * 50
            if posicionX <= ancho-50 and posicionY <= alto-50:
                matrizObstaculos[math.floor(posicionY * 2 / 100)][math.floor(posicionX * 2 / 100)] = 1
            obsimg.append(pygame.image.load("./imgs/obstaculo.png"))
            screen.blit(obsimg[z], (posicionX, posicionY))
    return matrizObstaculos

def matarFantasma(matriz, link_x, link_y, fantasmasimgrect, cantidadfantasmas):
    if matrizTablero[link_y//50][link_x//50] == 3 and cantidadfantasmas > 1:
        for i in range (0, cantidadfantasmas-1):
            if link_x//50 == fantasmasimgrect[i][0]//50 and link_y//50 == fantasmasimgrect[i][1]//50:
                fantasmasimgrect.remove(fantasmasimgrect[i])
                fantasmasimg.remove(fantasmasimg[i])

        cantidadfantasmas -= 1

#Movimientos de link
def moverLink(movimiento, link_x, link_y, matrizTablero, matrizGasto, valorAnterior):
        link_x *= 50
        link_y *= 50

        if movimiento == "l":
            if link_x >= 50:
                matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)] = valorAnterior
                valorAnterior = matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)-1]
                matarFantasma(matrizTablero, link_x-50, link_y,fantasmasimgrect, cantidadfantasmas)
                link_x -= 50
                matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)] = 2
                matrizGasto[math.ceil(link_y/50)][math.ceil(link_x/50)+1] +=1

        if movimiento == "r":
            if link_x <= ancho-100:
                matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)] = valorAnterior
                valorAnterior = matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)+1]
                matarFantasma(matrizTablero, link_x + 50, link_y,fantasmasimgrect, cantidadfantasmas)
                link_x += 50
                matrizGasto[math.ceil(link_y/50)][math.ceil(link_x/50)-1]+=1
                matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)] = 2


        if movimiento == "u":
            if link_y >= 50:
                matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)] = valorAnterior
                valorAnterior = matrizTablero[math.ceil(link_y/50)-1][math.ceil(link_x/50)]
                matarFantasma(matrizTablero, link_x,link_y-50,fantasmasimgrect, cantidadfantasmas)
                link_y -= 50
                matrizGasto[math.ceil(link_y/50)+1][math.ceil(link_x/50)] += 1
                matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)] = 2


        if movimiento == "d":
            if link_y <= alto-100:
                matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)] = valorAnterior
                valorAnterior = matrizTablero[math.ceil(link_y/50)+1][math.ceil(link_x/50)]
                matarFantasma(matrizTablero, link_x ,link_y+50 ,fantasmasimgrect, cantidadfantasmas)
                link_y += 50
                matrizGasto[math.ceil(link_y/50)-1][math.ceil(link_x/50)] += 1
                matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)] = 2

        #print(matrizTablero)
        return math.ceil(link_x/50), math.ceil(link_y/50), matrizTablero, matrizGasto, valorAnterior

def asignacion(matriz, posX, posY):
    obstaculo = 0
    try:
        if matriz [posY][posX] == 1:
            obstaculo += 3

        if matriz [posY-1][posX] == 1:
            obstaculo += 1

        if matriz [posY+1][posX] == 1:
            obstaculo += 1

        if matriz [posY][posX-1] == 1:
            obstaculo += 1

        if matriz [posY][posX+1] == 1:
            obstaculo += 1
    except:
        pass
    if obstaculo < 3:
        return posX, posY
    else:
        for x in range(0, len(matriz)):
         for z in range(0, len(matriz[0])):
             if matriz[x][z] == 0:
                 if matriz [x-1][z] != 1:
                     obstaculo -= 1

                 if matriz [x+1][z] != 1:
                    obstaculo -= 1

                 if matriz [x][z-1] != 1:
                    obstaculo -= 1

                 if matriz [x][z+1] != 1:
                    obstaculo -= 1

                 if obstaculo < 2:
                     posX = z
                     posY = x
                     return  posX, posY
                     break




#Para matriz personalizada
def tableroPersonalizado(matriz, screen, suelo, obstaculo ,llave, puerta, link, fantasma):
    fantasmasimgx = []
    fantasmasimgy = []
    # agregar 0s a arrays de posiciones de fantasmas
    #fantasmasimgx = numpy.zeros((cantidadfantasmas), dtype=int)
    #fantasmasimgy = numpy.zeros((cantidadfantasmas), dtype=int)
    contadorfantasma=0
    fantasmasimgrect = []
    fantasmasimgx = []

    puerta_x = 0
    puerta_y = 0

    for x in range(0, len(matriz)):
        for z in range(0, len(matriz[0])):
            if matriz[x][z] == 0:
                screen.blit(suelo, (z*50-25, x*50-25))

            if matriz[x][z] == 1:
                screen.blit(obstaculo, (z*50, x*50))

            if matriz[x][z] == 2:
                screen.blit(suelo, (z*50-25, x*50-25))
                #screen.blit(link, (z*50, x*50))
                link_x = z
                link_y = x

            if matriz[x][z] == 3:

                screen.blit(suelo, (z*50-25, x*50-25))
                #screen.blit(fantasma, (z*50, x*50))
                fantasmasimgx+=[z*50]
                fantasmasimgy +=[x*50]
                newfantas = pygame.image.load("./imgs/fantasma.png")
                newfantas = pygame.transform.scale(player, (50, 50))
                fantasmasimg.append(newfantas)
                rect = fantasmasimg[contadorfantasma].get_rect()
                fantasmasimgrect.append(rect)
                rect.left = fantasmasimgx[contadorfantasma]
                rect.top = fantasmasimgy[contadorfantasma]
                contadorfantasma+=1


            if matriz[x][z] == 4:
                screen.blit(suelo, (z*50-25, x*50-25))
                screen.blit(llave, (z*50+5, x*50+5))
                llave_x = z
                llave_y = x

            if matriz[x][z] == 5:
                screen.blit(suelo, (z*50-25, x*50-25))
                screen.blit(puerta, (z*50-25 , x*50-9))
                puerta_x = z
                puerta_y = x

    print("los fantasmas son estos : "+ str(contadorfantasma))
    cantidadfantasmas=contadorfantasma
    return link_x, link_y, llave_x, llave_y, puerta_x, puerta_y,\
           fantasmasimgx, fantasmasimgy,fantasmasimgrect,cantidadfantasmas,fantasmasimg

#Crear fantasmas
def CrearFantasmas(screen, a, ancho,alto,cantidadfantasmas):


    # agregar 0s a arrays de posiciones de fantasmas
    fantasmasimgx = numpy.zeros((cantidadfantasmas), dtype=int)
    fantasmasimgy = numpy.zeros((cantidadfantasmas), dtype=int)

    # crear fantasmas
    for f in range(0, cantidadfantasmas):
        newfantas = pygame.image.load("./imgs/fantasma.png")
        newfantas = pygame.transform.scale(player, (50, 50))
        fantasmasimg.append(newfantas)
        (fantasmasimgy[f], fantasmasimgx[f]) = Buscar(a, ancho, alto)
        #screen.blit(fantasmasimg[f], (fantasmasimgx[f], fantasmasimgy[f]))
        rect = fantasmasimg[f].get_rect()
        fantasmasimgrect.append(rect)
        rect.left = fantasmasimgx[f]
        rect.top = fantasmasimgy[f]
        a[fantasmasimgy[f] // 50][fantasmasimgx[f] // 50] = 3


#crea arbolpor profundidad sin ciclos
def Libres(posf,posc,hentrante, matrixobst, ancho , alto, arbol, linkf, linkc):

    # para escoger una direccion disponible
    (arr, aba, der, izq) = (True, True, True, True)

    # para mirar si esta en un borde del mapa
    (bordearr, bordeaba, bordeder, bordeizq) = (False, False, False, False)

    # opciones de movimiento disponibles
    opciones = []

    libres = arbol
    posicionf=0
    posicionc=0

    #para obtener posicion en fila y columna del hijo entrante
    #forma [(1,2)]
    if hentrante.__len__() == 5:
        #print("forma [(1,2)]")
        posicionf = int(hentrante[1:2])
        posicionc = int(hentrante[3:4])

    #forma [(1,23)] o [(12,3)]
    elif hentrante.__len__() == 6:
        # forma [(1,23)]
        if hentrante[2] == ",":
            #print("forma [(1,23)]")
            posicionf = int(hentrante[1:2])
            posicionc = int(hentrante[3:5])
        # forma [(12,3)]
        elif hentrante[3] == ",":
            #print("forma [(12,3)]")
            posicionf = int(hentrante[1:3])
            posicionc = int(hentrante[4:5])

    elif hentrante.__len__() == 7:
        #print("forma [(12,34)]")
        posicionf = int(hentrante[1:3])
        posicionc = int(hentrante[4:6])



    # Miro si esta en un limite del mapa
    # Esta arriba Max, no se puede mover hacia arriba
    if posicionf == 0:
        # print("Esta Arriba")
        arr = False
        bordearr = True

    # Esta abajo Max, no se puede mover hacia abajo
    if posicionf == (alto // 50) - 1:
        # print("Esta Abajo")
        aba = False
        bordeaba = True

    # Esta izquierda Max, no se puede mover hacia la izquierda
    if posicionc == 0:
        # print("Esta a la Izquierda")
        izq = False
        bordeizq = True

    # Esta Derecha Max, no se puede mover hacia la derecha
    if posicionc == (ancho // 50) - 1:
        # print("Esta a la Derecha")
        der = False
        bordeder = True

    # Miro si tiene obstaculos al rededor
    # a la izquierda
    if bordeizq == False:
        if matrixobst[posicionf][posicionc - 1] == 1:
            izq = False
        else:
            izq: True

    # a la derecha
    if bordeder == False:
        if matrixobst[posicionf][posicionc + 1] == 1:
            der = False
        else:
            der = True

    # arriba
    if bordearr == False:
        if matrixobst[posicionf - 1][posicionc] == 1:
            arr = False
        else:
            arr = True

    # abajo
    if bordeaba == False:
        if matrixobst[posicionf + 1][posicionc] == 1:
            aba = False
        else:
            aba = True


    #arbol de forma matricial
    arbolmatrix=""

    #ultimos hijos
    ultimoshijos=""

    #numero de hermanos del ultimo
    numultimoshijos=0

    #hijo a expandir
    hijo = ""

    #posicion donde estoy
    posicionactual = arbolmatrix.__len__()-1

    #raiz y meta
    raiz = "(" + str(posf) + ","+ str(posc) + ")"
    meta = "(" + str(linkf) + ","+ str(linkc) + ")"

    # hijo entrante , valor entrante
    hijoentrante = hentrante

    #variables boleanas
    soyancestro = False
    soyraiz = False
    soymeta = False

    #para agregar hijos a la lista, expandir
    expandir= False

    #arbol en forma de lista para enviar nuevamente a este metodo
    arbolenviar=""


#####capturo valores para trabajar
    if arbol != "" :
        arbolmatrix = arbol.splitlines()
        ultimoshijos = (arbolmatrix[arbolmatrix.__len__()-1])
        #hijo = ultimoshijos[1:6]
        numultimoshijos = ultimoshijos.__len__()



#####validar si es ancestro
    if arbol != "" :
        for x in range(0, arbolmatrix.__len__()-1):
            filahijos = (arbolmatrix[x])

            #onehijo = filahijos[1:6]

            # miro de que forma es el primer hijo
            # si es de la forma (a,b)
            if filahijos[5] == ")":
                # selecciono el hijo a enviar
                onehijo = filahijos[1:6]

            # si es de la forma (a,bc) o (ab,c)
            elif filahijos[6] == ")":
                # selecciono el hijo a enviar
                onehijo = filahijos[1:7]

            # si es de la forma (ab,cd)
            elif filahijos[7] == ")":
                # selecciono el hijo a enviar
                onehijo = filahijos[1:8]


            if hijoentrante == onehijo:
                soyancestro = True




##### validar si la opción que llega es meta
    if hijoentrante == meta:

        if hijoentrante == meta and arbol == "":
            print("yo soy la meta, me devuelvo yo misma : " + hijoentrante)
            return hijoentrante
        else :

            filahijos = (arbolmatrix[1])

            # miro de que forma es el primer hijo
            # si es de la forma (a,b)
            if filahijos[5] == ")":
                # selecciono el hijo a enviar
                onehijo = filahijos[1:6]

            # si es de la forma (a,bc) o (ab,c)
            elif filahijos[6] == ")":
                # selecciono el hijo a enviar
                onehijo = filahijos[1:7]

            # si es de la forma (ab,cd)
            elif filahijos[7] == ")":
                # selecciono el hijo a enviar
                onehijo = filahijos[1:8]

            soymeta = True
            print("llegamos a la meta, devuelve el primer valor del primer hijo de la raiz , que es:   " + onehijo)
            print("la mejor opcion es : " + onehijo)
            return onehijo


##### Validar si es Raiz
    elif arbol == "" :
        arbolenviar = "[" + hijoentrante + "]\n"
        expandir = True
        soyraiz = True

        #print("Soy la Raiz, me pongo, pongo mis hijos y mando mi primer hijo para repetir este metodo y seguir creando el arbol ")


    #validar si ya estoy de ancestro.
    elif soyancestro == True:
        #print("YA ESTA REPETIDO , me quito de la lista y envio la lista y a mi hermano.")
        #me quito
        sinquitar =  ultimoshijos[ultimoshijos.__len__() - 1]
        ultimoshijos = ultimoshijos[6:ultimoshijos.__len__() - 1]
        twohijo=""
        hijosanteriores=""

        abuelosunicos=False
        todosunicos = False

        #ver si todos somos hijos unicos, si alguno no es hijo unico se rompe
        for x in range(arbolmatrix.__len__()):
            if arbolmatrix[x].__len__() <= 9:
                todosunicos = True
            elif arbolmatrix[x].__len__() > 9:
                todosunicos=False
                break



        #ver si mis abuelos son hijos unicos
        if arbolmatrix[arbolmatrix.__len__()-2].__len__() <= 9:
            abuelosunicos=True


        # si es hijo unico, y todos tambien son hijos unicos
        # se quitan todos y se envia el primer hijo de la raiz
        # se envia los niveles arriba y se envia el segundo de hijo del que este en ese nivel arriba
        if numultimoshijos <= 9 and todosunicos == True:
            filahijos = (arbolmatrix[1])

            # miro de que forma es el primer hijo
            # si es de la forma (a,b)
            if filahijos[5] == ")":
                # selecciono el hijo a enviar
                onehijo = filahijos[1:6]

            # si es de la forma (a,bc) o (ab,c)
            elif filahijos[6] == ")":
                # selecciono el hijo a enviar
                onehijo = filahijos[1:7]

            # si es de la forma (ab,cd)
            elif filahijos[7] == ")":
                # selecciono el hijo a enviar
                onehijo = filahijos[1:8]

            soymeta = True
            #print("llegamos a la meta, devuelve el primer valor del primer hijo de la raiz , que es:   " + onehijo)
            #print("la mejor opcion es : " + onehijo)
            return onehijo




        #si es hijo unico, y el nivel anterior tambien es hijo unico
        #se quita este que ingresa, tambien se quita el hijo unico del nivel anterior
        # se envia los niveles arriba y se envia el segundo de hijo del que este en ese nivel arriba
        if numultimoshijos <= 9 and abuelosunicos == True:

            #capturo el abuelo que tenga varios hijos
            contador = 0
            posicionabuelo=0
            for x in range(arbolmatrix.__len__() - 1, -1, -1):
                contador += 1
                if arbolmatrix[x].__len__()  > 9:
                    posicionabuelo = x
                    break


            #capturo los hijos de dos niveles anteriores
            hijosanteriores = (arbolmatrix[posicionabuelo])

            #capturo al segundo hermano

            # si el 1ro es de la forma (a,b)
            if hijosanteriores[5] == ")":
            #pregunto de que forma es el segundo hijo de 2 niveles anteriores
                #si segundo es de la forma (a,b)
                if hijosanteriores[10] == ")":
                    # selecciono el siguiente hijo a enviar
                    twohijo = hijosanteriores[6:11]

                #si segundo es de la forma (a,bc) o (ab,c)
                elif hijosanteriores[11] == ")":
                    # selecciono el siguiente hijo a enviar
                    twohijo = hijosanteriores[6:12]

                #si el segundo es de la forma (ab,cd)
                elif hijosanteriores[12] == ")":
                    # selecciono el siguiente hijo a enviar
                    twohijo = hijosanteriores[6:13]

                # me quito
                ultimoshijos = hijosanteriores[6:hijosanteriores.__len__() - 1]
                libres = "[" + ultimoshijos + "]"


            # si el 1ro es de la forma (a,bc) o (ab,c)
            elif hijosanteriores[6] == ")":
            # pregunto de que forma es el segundo hijo del nivel anterior
                # si segundo es de la forma (a,b)
                if hijosanteriores[11] == ")":
                    # selecciono el siguiente hijo a enviar
                    twohijo = hijosanteriores[7:12]

                # si segundo es de la forma (a,bc) o (ab,c)
                elif hijosanteriores[12] == ")":
                    # selecciono el siguiente hijo a enviar
                    twohijo = hijosanteriores[7:13]

                # si el segundo es de la forma (ab,cd)
                elif hijosanteriores[13] == ")":
                    # selecciono el siguiente hijo a enviar
                    twohijo = hijosanteriores[7:14]

                # me quito
                ultimoshijos = hijosanteriores[7:hijosanteriores.__len__() - 1]
                libres = "[" + ultimoshijos + "]"


            # si el 1ro es de la forma (ab,cd)
            elif hijosanteriores[7] == ")":
            # pregunto de que forma es el segundo hijo del nivel anterior
                # si segundo es de la forma (a,b)
                if hijosanteriores[12] == ")":
                    # selecciono el siguiente hijo a enviar
                    twohijo = hijosanteriores[8:13]

                # si segundo es de la forma (a,bc) o (ab,c)
                elif hijosanteriores[13] == ")":
                    # selecciono el siguiente hijo a enviar
                    twohijo = hijosanteriores[8:14]

                # si el segundo es de la forma (ab,cd)
                elif hijosanteriores[14] == ")":
                    # selecciono el siguiente hijo a enviar
                    twohijo = hijosanteriores[8:15]

                # me quito
                ultimoshijos = hijosanteriores[8:hijosanteriores.__len__() - 1]
                libres = "[" + ultimoshijos + "]"



            arbolmatrix[posicionabuelo] = libres

            #arbolenviar = MatrizaLista(arbolmatrix, False)
            #arbolenviar = MatrizaLista(arbolenviar.splitlines(), False)

            for x in range(contador-1):
                arbolenviar = MatrizaLista(arbolmatrix,False)

            """print("todos : ")
            print(arbol)
            print("  sin el repetido : ")
            print(arbolenviar)
            print(" El siguiente a enviar es : " + twohijo)"""

            return Libres(posf,posc,twohijo,matrixobst,ancho,alto,arbolenviar,linkf,linkc)


        #si es hijo unico , y el nivel anterior tiene varios hijos
        # se quita, y se envia la lista hasta el nivel anterior, y ese nivel anterior envia al segundo hermano.
        #y la lista desde ahi desde ese 2do hermano
        #si es hijo unico
        if numultimoshijos <= 9 :
            #capturo  el nivel anterior o los hijos anteriores
            hijosanteriores = (arbolmatrix[arbolmatrix.__len__() - 2])

            #capturo al segundo hermano

            # si el 1ro es de la forma (a,b)
            if hijosanteriores[5] == ")":
            #pregunto de que forma es el segundo hijo del nivel anterior
                #si segundo es de la forma (a,b)
                if hijosanteriores[10] == ")":
                    # selecciono el siguiente hijo a enviar
                    twohijo = hijosanteriores[6:11]

                #si segundo es de la forma (a,bc) o (ab,c)
                elif hijosanteriores[11] == ")":
                    # selecciono el siguiente hijo a enviar
                    twohijo = hijosanteriores[6:12]

                #si el segundo es de la forma (ab,cd)
                elif hijosanteriores[12] == ")":
                    # selecciono el siguiente hijo a enviar
                    twohijo = hijosanteriores[6:13]

                # me quito
                ultimoshijos = hijosanteriores[6:hijosanteriores.__len__() - 1]
                libres = "[" + ultimoshijos + "]"


            # si el 1ro es de la forma (a,bc) o (ab,c)
            elif hijosanteriores[6] == ")":
            # pregunto de que forma es el segundo hijo del nivel anterior
                # si segundo es de la forma (a,b)
                if hijosanteriores[11] == ")":
                    # selecciono el siguiente hijo a enviar
                    twohijo = hijosanteriores[7:12]

                # si segundo es de la forma (a,bc) o (ab,c)
                elif hijosanteriores[12] == ")":
                    # selecciono el siguiente hijo a enviar
                    twohijo = hijosanteriores[7:13]

                # si el segundo es de la forma (ab,cd)
                elif hijosanteriores[13] == ")":
                    # selecciono el siguiente hijo a enviar
                    twohijo = hijosanteriores[7:14]

                # me quito
                ultimoshijos = hijosanteriores[7:hijosanteriores.__len__() - 1]
                libres = "[" + ultimoshijos + "]"


            # si el 1ro es de la forma (ab,cd)
            elif hijosanteriores[7] == ")":
            # pregunto de que forma es el segundo hijo del nivel anterior
                # si segundo es de la forma (a,b)
                if hijosanteriores[12] == ")":
                    # selecciono el siguiente hijo a enviar
                    twohijo = hijosanteriores[8:13]

                # si segundo es de la forma (a,bc) o (ab,c)
                elif hijosanteriores[13] == ")":
                    # selecciono el siguiente hijo a enviar
                    twohijo = hijosanteriores[8:14]

                # si el segundo es de la forma (ab,cd)
                elif hijosanteriores[14] == ")":
                    # selecciono el siguiente hijo a enviar
                    twohijo = hijosanteriores[8:15]

                # me quito
                ultimoshijos = hijosanteriores[8:hijosanteriores.__len__() - 1]
                libres = "[" + ultimoshijos + "]"



            arbolmatrix[arbolmatrix.__len__() - 2] = libres
            arbolenviar = MatrizaLista(arbolmatrix, False)

            """print("todos : ")
            print(arbol)
            print("  sin el repetido : ")
            print(arbolenviar)
            print(" El siguiente a enviar es : " + twohijo)"""

            return Libres(posf,posc,twohijo,matrixobst,ancho,alto,arbolenviar,linkf,linkc)


        #si tengo mas hermanos
        elif numultimoshijos > 9 :
            # capturo  el nivel actual o los hijos actuales
            ultimoshijos = (arbolmatrix[arbolmatrix.__len__() - 1])

        #miro de que forma es el primer hijo
            #si es de la forma (a,b)
            if ultimoshijos[5] == ")":
                # me quito
                ultimoshijos = ultimoshijos[6:ultimoshijos.__len__() - 1]
                libres = "[" + ultimoshijos + "]"


                # selecciono el siguiente hijo a enviar
                #twohijo = libres[1:6]


            #si es de la forma (a,bc) o (ab,c)
            elif ultimoshijos[6] == ")":
                # me quito
                ultimoshijos = ultimoshijos[7:ultimoshijos.__len__() - 1]
                libres = "[" + ultimoshijos + "]"
                # selecciono el siguiente hijo a enviar
                #twohijo = libres[1:7]

            #si es de la forma (ab,cd)
            elif ultimoshijos[7] == ")":
                # me quito
                ultimoshijos = ultimoshijos[8:ultimoshijos.__len__() - 1]
                libres = "[" + ultimoshijos + "]"
                # selecciono el siguiente hijo a enviar
                #twohijo = libres[1:8]



            # miro de que forma es el primer hijo de estos que quedaron
            # si es de la forma (a,b)
            if libres[5] == ")":
                # selecciono el hijo a enviar
                twohijo = libres[1:6]

            # si es de la forma (a,bc) o (ab,c)
            elif libres[6] == ")":
                # selecciono el hijo a enviar
                twohijo = libres[1:7]

            # si es de la forma (ab,cd)
            elif libres[7] == ")":
                # selecciono el hijo a enviar
                twohijo = libres[1:8]


            arbolmatrix[arbolmatrix.__len__() - 1] = libres
            arbolenviar = MatrizaLista(arbolmatrix, True)

            """print("todos : ")
            print(arbol)
            print("  sin el repetido : ")
            print(arbolenviar)
            print(" El hermano siguiente es : " + twohijo)"""

            return Libres(posf, posc, twohijo, matrixobst, ancho, alto, arbolenviar, linkf, linkc)


    if soyraiz == True or (soymeta == False and soyancestro == False and soyraiz == False):

        if soyraiz == True:

            #print("ENTRAMOOOS")


            libres += "["
            # Agrego opciones de movimientos al array y a libres
            if arr == True:
                opciones.append(4)
                libres += "(" + str(posicionf - 1) + "," + str(posicionc) + ")"

            if der == True:
                opciones.append(1)
                libres += "(" + str(posicionf) + "," + str(posicionc + 1) + ")"

            if aba == True:
                opciones.append(2)
                libres += "(" + str(posicionf + 1) + "," + str(posicionc) + ")"

            if izq == True:
                opciones.append(3)
                libres += "(" + str(posicionf) + "," + str(posicionc - 1) + ")"

            libres += "]"

            arbolenviar += libres

            # miro de que forma es el primer hijo de la raiz
            # si es de la forma (a,b)
            if libres[5] == ")":
                # selecciono el hijo a enviar
                onehijo = libres[1:6]

            # si es de la forma (a,bc) o (ab,c)
            elif libres[6] == ")":
                # selecciono el hijo a enviar
                onehijo = libres[1:7]

            # si es de la forma (ab,cd)
            elif libres[7] == ")":
                # selecciono el hijo a enviar
                onehijo = libres[1:8]



            """print("agregar hijos de la raiz y enviar el primer hijo")
            print("arbol que se genero es : ")
            print(arbolenviar)
            print(" primer hijo es : ")
            print( onehijo)"""

            return Libres(posf, posc, onehijo, matrixobst, ancho, alto, arbolenviar, linkf, linkc)

        elif (soymeta == False and soyancestro == False and soyraiz == False):
            #print("Agregar hijos del que llego al final del arbol, y enviar al primer hijo de esta ultima rama")

            libres = "["
            # Agrego opciones de movimientos al array y a libres
            if arr == True:
                opciones.append(4)
                libres += "(" + str(posicionf - 1) + "," + str(posicionc) + ")"

            if der == True:
                opciones.append(1)
                libres += "(" + str(posicionf) + "," + str(posicionc + 1) + ")"

            if aba == True:
                opciones.append(2)
                libres += "(" + str(posicionf + 1) + "," + str(posicionc) + ")"

            if izq == True:
                opciones.append(3)
                libres += "(" + str(posicionf) + "," + str(posicionc - 1) + ")"

            libres += "]"



            arbolenviar = MatrizaLista(arbolmatrix, True)
            arbolenviar += "\n"
            arbolenviar += libres

            # miro de que forma es el primer hijo
            # si es de la forma (a,b)
            if libres[5] == ")":
                # selecciono el hijo a enviar
                onehijo = libres[1:6]

            # si es de la forma (a,bc) o (ab,c)
            elif libres[6] == ")":
                # selecciono el hijo a enviar
                onehijo = libres[1:7]

            # si es de la forma (ab,cd)
            elif libres[7] == ")":
                # selecciono el hijo a enviar
                onehijo = libres[1:8]

            """print("agregar hijos del que llego:")
            print("arbol que se genero es : ")
            print(arbolenviar)
            print(" primer hijo de la ultima rama ees : ")
            print(onehijo)"""

            return Libres(posf, posc, onehijo, matrixobst, ancho, alto, arbolenviar, linkf, linkc)

#combierte una matriz en lista
def MatrizaLista(array, cuantos):
    lista = ""
    todos = cuantos

    if todos == True:
        for x in range(0, array.__len__()):
            if x == (array.__len__()-1):
                lista += array[x]
            else:
                lista += array[x] + "\n"
    elif todos == False:
        for x in range(0, array.__len__()-1):
            if x == (array.__len__()-2):
                lista += array[x]
            else:
                lista += array[x] + "\n"



    return lista

#Busqueda de movimiento para fantasma mediante profundidad sin ciclos
def Profundidadsinciclos(fantasma, matrixobst, ancho , alto, linkf,linkc, llavef,llavec, puertaf,puertac):
    #reglas: arriba, derecha, abajo ,izquierda

    (filallave, columnallave, filapuerta, columnapuerta)=(llavef,llavec,puertaf,puertac)

    # Capturo posicion fantasma
    posicionc = fantasma.left // 50
    posicionf = fantasma.top // 50
    # quedan como posiciones anteriores
    posicioncvieja = posicionc
    posicionfvieja = posicionf


    #hijo a enviar, posicion actual, raiz
    onehijo = "(" + str(posicionf) + ","+ str(posicionc) + ")"

    opcion = Libres(posicionf, posicionc, onehijo, matrixobst, ancho, alto, "", linkf, linkc)
    valorescogido = 0

    #valido la posicion que llego para saber hacia que lado se mueve el fantasma
    #miro si es arriba
    if opcion == "(" + str(posicionf-1) + ","+ str(posicionc) + ")" :
        valorescogido = 1
    elif opcion == "(" + str(posicionf) + ","+ str(posicionc+1) + ")" :
        valorescogido = 2
    elif opcion == "(" + str(posicionf+1) + ","+ str(posicionc) + ")" :
        valorescogido = 3
    elif opcion == "(" + str(posicionf) + ","+ str(posicionc-1) + ")" :
        valorescogido = 4


    #opcion que llega de Libres
    elegido = valorescogido

    # movimiento despues de elegir el lado a donde se va a mover
        # mover arriba
    if elegido == 1 and fantasma.top >= 50:
        fantasma.top += -50
    # mover derecha
    if elegido == 2 and fantasma.left <= ancho - 100:
        fantasma.left += 50
        # mover abajo
    if elegido == 3 and fantasma.top <= alto - 100:
        fantasma.top += 50
        # mover izquierda
    if elegido == 4 and fantasma.left >= 50:
        fantasma.left += -50

    # capturo posiciones nuevas
    posicioncnueva = fantasma.left // 50
    posicionfnueva = fantasma.top // 50

    # modifico posiciones viejas con 0 = vacio, o con 4 = llave , o 5 = puerta
    # print("nueva")
    # print(posicionfnueva, posicioncnueva)

    # actualizo si estaba la llave en la posicion vieja
    if (filallave == posicionfvieja and columnallave == posicioncvieja) or (
            filapuerta == posicionfvieja and columnapuerta == posicioncvieja):
        if (filallave == posicionfvieja and columnallave == posicioncvieja):
            matrixobst[posicionfvieja][posicioncvieja] = 4
        elif (filapuerta == posicionfvieja and columnapuerta == posicioncvieja):
            matrixobst[posicionfvieja][posicioncvieja] = 5
    else:
        matrixobst[posicionfvieja][posicioncvieja] = 0

    # si me muevo a la llave o a la puerta dejo la matrix como estaba con la llave o puerta
    if matrixobst[posicionfnueva][posicioncnueva] == 4 or matrixobst[posicionfnueva][posicioncnueva] == 5:
        if matrixobst[posicionfnueva][posicioncnueva] == 4:
            #print("pase por la llave")
            matrixobst[posicionfnueva][posicioncnueva] = 4
            # (filallave,columnallave)=(posicionfnueva,posicioncnueva)

        elif matrixobst[posicionfnueva][posicioncnueva] == 5:
            #gprint("pase por la puerta")
            matrixobst[posicionfnueva][posicioncnueva] = 5
            (filapuerta, columnapuerta) = (posicionfnueva, posicioncnueva)
    else:
        matrixobst[posicionfnueva][posicioncnueva] = 3

    return fantasma, matrixobst


#Actualizar matriz gastos
def matrizUpdate(tablero, gastos):
    try:
        for x in range(0, len(tablero)):
            for i in range(0, len(tablero[0])):
             if tablero[x][i] == 3:
                gastos[x][i] = 3
             if tablero[x][i] == 1:
                gastos[x][i] = None
             if tablero[x][i] == 0 and gastos[x][i] == 3 and \
                     (tablero[x-1][i] != 2 or tablero[x+1][i] != 2 or tablero[x][i-1] != 2 or tablero[x][i+1] != 2):
                gastos[x][i] = 0
    except :
        pass
    return gastos
#Busca valores (x,y) para un nuevo fantasma
def Buscar(matrix, ancho,alto):

    #valores iniciales
    valorfila=random.randint(0, (alto // 50)-1)
    valorcolum=random.randint(0, (ancho // 50)-1)

    # valores finales
    (filaescogida, columnaescogida) = (0, 0)

    #si encontro el numero adecuado
    encontrado=False
    #si se cumple la distancia de link
    lejos=False

    # para mirar si esta en un borde del mapa
    (bordearr, bordeaba, bordeder, bordeizq) = (False, False, False, False)


#mirar si esta en un borde del mapa
    # Esta arriba max
    if valorfila == 0:
        bordearr = True

    # Esta abajo Max
    if valorfila == (alto // 50) - 1:
        bordeaba = True

    # Esta izquierda Max
    if valorcolum == 0:
        bordeizq = True

    # Esta Derecha Max
    if valorcolum == (ancho // 50) - 1:
        bordeder = True


#mirar si esta en dos bordes al mismo tiempo
    #arriba y a un lado
    if (bordearr == True and bordeder == True) or (bordearr == True and bordeizq == True):
        if bordearr == True and bordeder == True:
            #print("arriba y a la derecha")
            if (matrix[0][valorcolum-1] != 2) and (matrix[1][valorcolum-1] != 2) and (matrix[1][valorcolum] != 2) :
                #print("si esta lejos link")
                lejos=True
        elif bordearr == True and bordeizq == True:
            #print("arriba y a la izquierda")
            if (matrix[0][1] != 2) and (matrix[1][1] != 2) and (matrix[1][0] != 2) :
                #print("si esta lejos link")
                lejos=True

    #abajo y a un lado
    if (bordeaba == True and bordeder == True) or (bordeaba == True and bordeizq == True):
        if bordeaba == True and bordeder == True:
            #print("abajo y a la derecha")
            if (matrix[valorfila][valorcolum-1] != 2) and (matrix[valorfila-1][valorcolum-1] != 2) and (matrix[valorfila-1][valorcolum] != 2) :
                #print("si esta lejos link")
                lejos=True
        elif bordeaba == True and bordeizq == True:
            #print("abajo y a la izquierda")
            if (matrix[valorfila][1] != 2) and (matrix[valorfila-1][1] != 2) and (matrix[valorfila-1][0] != 2) :
                #print("si esta lejos link")
                lejos=True

#mirar si esta solo en un borde
    # si esta arriba solamente
    if bordearr == True and bordeaba == False and bordeder == False and bordeizq == False:
        #print("solamente arriba")
        if (matrix[0][valorcolum - 1] != 2) and (matrix[0][valorcolum + 1] != 2) and (matrix[1][valorcolum-1] != 2) \
                and (matrix[1][valorcolum] != 2) and (matrix[1][valorcolum+1] != 2):
            #print("si esta lejos link")
            lejos = True

    # si esta abajo solamente
    if bordeaba == True and bordearr == False and bordeder == False and bordeizq == False:
        #print("solamente abajo")
        if (matrix[valorfila][valorcolum-1] != 2) and (matrix[valorfila][valorcolum+1] != 2) \
                and (matrix[valorfila - 1][valorcolum-1] != 2) and (matrix[valorfila - 1][valorcolum] != 2) and (matrix[valorfila - 1][valorcolum+1] != 2):
            #print("si esta lejos link")
            lejos = True


    # si esta a la izquierda solamente
    if bordeizq == True and bordeaba == False and bordeder == False and bordearr == False:
        #print("solamente izquierda")
        if (matrix[valorfila-1][0] != 2) and (matrix[valorfila+1][0] != 2) and (matrix[valorfila - 1][valorcolum + 1] != 2)\
                and (matrix[valorfila][valorcolum+1] != 2) and (matrix[valorfila + 1][valorcolum + 1] != 2):
            #print("si esta lejos link")
            lejos = True

    # si esta a la derecha solamente
    if bordeder == True and bordeaba == False and bordearr == False and bordeizq == False:
        #print("solamente derecha")
        if (matrix[valorfila-1][valorcolum] != 2) and (matrix[valorfila+1][valorcolum] != 2) and (matrix[valorfila - 1][valorcolum - 1] != 2)\
                and (matrix[valorfila][valorcolum-1] != 2) and (matrix[valorfila + 1][valorcolum - 1] != 2):
            #print("si esta lejos link")
            lejos = True

#mirar si no esta en ningun borde
    if bordeder == False and bordeaba == False and bordearr == False and bordeizq == False:
        #print("no esta en ningun borde ")
        if (matrix[valorfila-1][valorcolum-1] != 2) and (matrix[valorfila-1][valorcolum] != 2) and (matrix[valorfila - 1][valorcolum + 1] != 2)\
                and (matrix[valorfila][valorcolum+1] != 2) and (matrix[valorfila ][valorcolum - 1] != 2) and (matrix[valorfila+1][valorcolum-1] != 2) \
                and (matrix[valorfila+1][valorcolum] != 2) and (matrix[valorfila + 1][valorcolum + 1] != 2):
            #print("si esta lejos link")
            lejos = True



    #pasar valores a #*50
    valorfila = valorfila * 50
    valorcolum = valorcolum * 50

    if valorfila == alto:
        valorfila = valorfila - 50

    if valorcolum == ancho:
        valorcolum = valorcolum - 50

    if matrix[valorfila//50][valorcolum//50] == 0:
        encontrado=True
    elif matrix[valorfila//50][valorcolum//50] != 0:
        encontrado=False
    else:
        encontrado=False



    if encontrado == True and lejos == True:
        (filaescogida, columnaescogida) = (valorfila, valorcolum)
        return filaescogida,columnaescogida
    elif encontrado == False or lejos == False:
        return Buscar(matrix, ancho , alto)


#fantasmas

#mover fantasmas aleatoriamente con la posicion de cada uno , la matriz del mapa, el ancho y alto de la ventana
def MoverFantasma(fantasma, matrixobst, ancho , alto):
    global filallave,columnallave,filapuerta,columnapuerta
    #capturar si paso por llave o puerta
    (hayllave,haypuerta)=(False,False)

    #opciones de movimiento disponibles
    opciones = []

    #para escoger una direccion disponible
    (arr, aba, der, izq) = (True, True, True, True)

    #para mirar si esta en un borde del mapa
    (bordearr, bordeaba, bordeder, bordeizq) = (False, False, False, False)

#Capturo posicion fantasma
    posicionc=fantasma.left//50
    posicionf=fantasma.top//50
#quedan como posiciones anteriores
    posicioncvieja=posicionc
    posicionfvieja=posicionf

    #si paso por llave
    #if matrixobst[posicionf][posicionc]==4:
     #   print("paso por la llave")
      #  pg.quit()






#Miro si esta en un limite del mapa
    #Esta arriba Max, no se puede mover hacia arriba
    if posicionf == 0 :
        #print("Esta Arriba")
        arr=False
        bordearr=True

    # Esta abajo Max, no se puede mover hacia abajo
    if posicionf == (alto//50)-1:
        #print("Esta Abajo")
        aba=False
        bordeaba=True

    # Esta izquierda Max, no se puede mover hacia la izquierda
    if posicionc == 0:
        #print("Esta a la Izquierda")
        izq=False
        bordeizq=True

    # Esta Derecha Max, no se puede mover hacia la derecha
    if posicionc == (ancho // 50) - 1:
        #print("Esta a la Derecha")
        der=False
        bordeder=True

#Miro si tiene obstaculos al rededor
    #a la izquierda
    if bordeizq == False :
        if matrixobst[posicionf][posicionc-1] == 1 :
            izq=False
        else:
            izq=True

    #a la derecha
    if bordeder == False :
        if matrixobst[posicionf][posicionc+1] == 1 :
            der=False
        else:
            der=True

    #arriba
    if bordearr == False :
        if matrixobst[posicionf-1][posicionc] == 1 :
            arr=False
        else:
            arr=True

    #abajo
    if bordeaba == False :
        if matrixobst[posicionf+1][posicionc] == 1 :
            aba=False
        else:
            aba=True

#Agrego opciones de movimientos al array
    if der == True:
        opciones.append(1)
    if aba == True:
        opciones.append(2)
    if izq == True:
        opciones.append(3)
    if arr == True:
        opciones.append(4)

    valor = random.randint(0, opciones.__len__()-1)
    elegido=opciones[valor]
    #print(opciones)

    # movimiento despues de elegir el lado a donde se va a mover
    # mover derecha
    if elegido == 1 and fantasma.left <= ancho - 100:
        fantasma.left += 50
        # mover abajo
    if elegido == 2 and fantasma.top <= alto - 100:
        fantasma.top += 50
        # mover izquierda
    if elegido == 3 and fantasma.left >= 50:
        fantasma.left += -50
        # mover arriba
    if elegido == 4 and fantasma.top >= 50:
        fantasma.top += -50

#capturo posiciones nuevas
    posicioncnueva = fantasma.left // 50
    posicionfnueva = fantasma.top // 50

#modifico posiciones viejas con 0 = vacio, o con 4 = llave , o 5 = puerta
    #print("nueva")
    #print(posicionfnueva, posicioncnueva)

    #actualizo si estaba la llave en la posicion vieja
    if (filallave == posicionfvieja and columnallave == posicioncvieja) or (filapuerta == posicionfvieja and columnapuerta == posicioncvieja) :
        if (filallave == posicionfvieja and columnallave == posicioncvieja):
            matrixobst[posicionfvieja][posicioncvieja] = 4
        elif (filapuerta == posicionfvieja and columnapuerta == posicioncvieja):
            matrixobst[posicionfvieja][posicioncvieja] = 5
    else :
        matrixobst[posicionfvieja][posicioncvieja] = 0

    #si me muevo a la llave o a la puerta dejo la matrix como estaba con la llave o puerta
    if matrixobst[posicionfnueva][posicioncnueva] == 4 or matrixobst[posicionfnueva][posicioncnueva] == 5:
        if matrixobst[posicionfnueva][posicioncnueva] == 4:
            #print("pase por la llave")
            matrixobst[posicionfnueva][posicioncnueva] = 4
            #(filallave,columnallave)=(posicionfnueva,posicioncnueva)

        elif matrixobst[posicionfnueva][posicioncnueva] == 5:
            #print("pase por la puerta")
            matrixobst[posicionfnueva][posicioncnueva] = 5
            (filapuerta, columnapuerta) = (posicionfnueva, posicioncnueva)
    else:
        matrixobst[posicionfnueva][posicioncnueva] = 3


    return fantasma, matrixobst



if __name__ == '__main__':

    gui = GUI()
    #main("600 x 400", True, [], 0, 0)
