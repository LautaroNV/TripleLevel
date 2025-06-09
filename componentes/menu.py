import pygame
import sys
from recursos.colores import *

def mostrar_menu(pantalla):
    opciones = ["Elegir Nivel", "Instrucciones", "Salir"]
    seleccion = 0
    fuente = pygame.font.SysFont("Arial", 40)

    while True:
        pantalla.fill(NEGRO)
        titulo = fuente.render("Note Rush - Menú", True, VERDE)
        pantalla.blit(titulo, (250, 100))

        for i, texto in enumerate(opciones):
            color = BLANCO if i == seleccion else GRIS
            render = fuente.render(texto, True, color)
            pantalla.blit(render, (260, 250 + i * 60))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif e.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif e.key == pygame.K_RETURN:
                    if seleccion == 0:
                        return "jugar"
                    elif seleccion == 1:
                        return "instrucciones"
                    elif seleccion == 2:
                        pygame.quit()
                        sys.exit()

def mostrar_instrucciones(pantalla):
    fuente = pygame.font.SysFont("Arial", 30)
    instrucciones = [
        "Presiona A, S, D, F, G cuando la nota llegue al traste.",
        "Cada color representa una tecla distinta.",
        "¡Mantén el ritmo para obtener combos y puntaje!",
        "Presiona ESC para volver al menú."
    ]
    esperando = True
    while esperando:
        pantalla.fill(NEGRO)
        for i, linea in enumerate(instrucciones):
            render = fuente.render(linea, True, BLANCO)
            pantalla.blit(render, (80, 150 + i * 50))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return "menu"
