#PROGRAMA JUEGO DE LA VIDA
#AUTOR: BRAYAN ALFONSO, basado en canal Dot CSV

#Se importan las librerías necesarias

import pygame
import time, os
import numpy as np
from tkinter import *
from tkinter import messagebox as MessageBox

print('Bienvenido al juego de la vida -- Versión Clásica')
MessageBox.showinfo("Juego de la Vida - Información General", "Bienvenido,\nlas reglas son las siguientes: \n" + " \nRegla 1: Una célula muerta con exactamente 3 células vecinas vivas nace, es decir, al próximo turno estará viva. \n" + "\nRegla 2: Una célula viva con 2 o 3 células vecinas vivas sigue viva, en otro caso muere (por soledad o superpoblación).\n" + "\nInstrucciones: \n" + "\n1. El juego inicia pausado. \n" + "\n2. Con clic derecho se puede cambiar el estado de las celdas. \n" + "\n3. Con la tecla 'R' se borra el contador de población, generación y se limpia la pantalla. \n" + "\n4. Con la tecla 'ESC' se cierra el juego. \n" + "\n5. Con cualquier otra tecla que no haya sido mencionada se pausa y despausa el juego. \n")


# Hago que la ventana aparezca centrada en Windows
os.environ["SDL_VIDEO_CENTERED"] = "1"

pygame.init()

# Establezco el título de la ventana:
pygame.display.set_caption("Juego de la vida -- Brayan Alfonso")

# Carga el icono si existe
iconPath = "./icono.ico"

if os.path.exists(iconPath):

    icono = pygame.image.load(iconPath)

    # Establece el icono de la ventana
    pygame.display.set_icon(icono)

# Defino ancho y alto de la ventana
width, height = 600, 600

# Creación de la ventana
screen = pygame.display.set_mode((height, width))

# Color de fondo, casi negro
bg = 25, 25, 25

# Pinto el fondo con el color elegido (bg)
screen.fill(bg)

# Cantidad de celdas en cada eje
nxC, nyC = 50, 50

# Ancho y alto de cada celda
dimCW = width / nxC
dimCH = height / nyC

# Estructura de datos que contiene todos los estados de las diferentes celdas
# Estados de las celdas: Vivas = 1 - Muertas = 0
# Inicializo matriz con ceros
gameState = np.zeros((nxC, nyC))

# Se añaden los estados en los que se desea que inicie el autómata

# Autómata 1:
# 0 1 0
# 0 1 0
# 0 1 0
gameState[5, 3] = 1
gameState[5, 4] = 1
gameState[5, 5] = 1

# Control de la ejecución - En True se inicia pausado (Para poder ver la forma inicial de los aútomatas):
pauseExec = True

# Controla la finalización del juego:
endGame = False

# Acumulador de cantidad de iteraciones:
iteration = 0

# Bucle de ejecución principal (Main Loop):
#while true :
while not endGame:
    #Se crea una copia para que en cada iteración no tenga en cuenta la anterior sino quee sean considerados todos los estados al tiempo
    newGameState = np.copy(gameState)

    # Vuelvo a colorear la pantalla con el color de fondo
    screen.fill(bg)

    # Agrego pequeña pausa para que el cpu no trabaje al 100% y se muestre un poco más claro para el usuario.
    time.sleep(0.2)

    # Registro de eventos de teclado y mouse
    ev = pygame.event.get()

    # Contador de población:
    population = 0

    for event in ev:

        # Si cierran la ventana finalizo el juego
        if event.type == pygame.QUIT:
            endGame = True
            break

        if event.type == pygame.KEYDOWN:

            # Si tocan escape finalizo el juego
            if event.key == pygame.K_ESCAPE:
                endGame = True
                break

            # Si se presiona la tecla r, se limpia la cuadrícula, se resetea la población e iteración y se pone en pausa
            if event.key == pygame.K_r:
                iteration = 0
                gameState = np.zeros((nxC, nyC))
                newGameState = np.zeros((nxC, nyC))
                pauseExec = True
            else:
                # Si tocan cualquier tecla no contemplada, se pausa o reanuda el juego
                pauseExec = not pauseExec

        # Detección de click del mouse:
        mouseClick = pygame.mouse.get_pressed()

        # Obtención de posición del cursor en la pantalla:
        # Si se hace click con cualquier botón del mouse, se obtiene un valor en mouseClick mayor a cero
        if sum(mouseClick) > 0:

            # Click del medio pausa / reanuda el juego
            if mouseClick[1]:

                pauseExec = not pauseExec

            else:

                # Obtengo las coordenadas del cursor del mouse en pixeles
                posX, posY, = pygame.mouse.get_pos()

                # Convierto de coordenadas en pixeles a celda clickeada en la cuadrícula; np.floor elimina y/o aproxima los decimales
                celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))

                # Click izquierdo y derecho permiten cambiar entre vida y muerte
                newGameState[celX, celY] = not gameState[celX, celY]

    if not pauseExec:
        # Incremento el contador de generaciones
        iteration += 1

    # Recorro cada una de las celdas generadas
    for y in range(0, nxC):
        for x in range(0, nyC):

            if not pauseExec:

                # Cálculo del número de vecinos cercanos con módulo, causando así el efecto toroide
                n_neigh = (
                    gameState[(x - 1) % nxC, (y - 1) % nyC]
                    + gameState[x % nxC, (y - 1) % nyC]
                    + gameState[(x + 1) % nxC, (y - 1) % nyC]
                    + gameState[(x - 1) % nxC, y % nyC]
                    + gameState[(x + 1) % nxC, y % nyC]
                    + gameState[(x - 1) % nxC, (y + 1) % nyC]
                    + gameState[x % nxC, (y + 1) % nyC]
                    + gameState[(x + 1) % nxC, (y + 1) % nyC]
                )

                # Regla 1: Una célula muerta con exactamente 3 células vecinas vivas "nace", es decir, al próximo turno estará viva.
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1

                # Regla 2: Una célula viva con 2 o 3 células vecinas vivas sigue viva, en otro caso muere (por "soledad" o "superpoblación").
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0

            # Incremento el contador de población:
            if gameState[x, y] == 1:
                population += 1

            # Creación del polígono de cada celda a dibujar
            poly = [
                (int(x * dimCW), int(y * dimCH)),
                (int((x + 1) * dimCW), int(y * dimCH)),
                (int((x + 1) * dimCW), int((y + 1) * dimCH)),
                (int(x * dimCW), int((y + 1) * dimCH)),
            ]

            if newGameState[x, y] == 0:
                # Dibujado de la celda para cada par de x e y:
                # screen          -> Pantalla donde dibujar
                # (128, 128, 128) -> Color a utilizar para dibujar, en este caso un gris
                # poly            -> Puntos que definan al poligono que se está dibujando
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                if pauseExec:
                    # Con el juego pausado pinto de gris las celdas
                    pygame.draw.polygon(screen, (128, 128, 128), poly, 0)
                else:
                    # Con el juego ejecutándose pinto de blanco las celdas
                    pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    # Actualizo el título de la ventana
    title = f"Juego de la vida - Brayan Alfonso - Población: {population} - Generación: {iteration}"
    if pauseExec:
        title += " - [PAUSADO]"
    pygame.display.set_caption(title)
    print(title)
    
    # Actualizo gameState
    gameState = np.copy(newGameState)

    # Muestro y actualizo los fotogramas en cada iteración del bucle principal
    pygame.display.flip()

print("Final - Brayan Alfonso", 'Referencia: https://www.youtube.com/watch?v=qPtKv9fSHZY')