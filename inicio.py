# inicio.py
import pygame
import sys
import os
import subprocess

pygame.init()

ANCHO, ALTO = 800, 600
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("TRIPLELEVEL - Menú Principal")

FUENTE = pygame.font.SysFont("arial", 40)
BLANCO = (255, 255, 255)
GRIS = (180, 180, 180)
FONDO = (20, 20, 20)
AZUL = (50, 150, 255)

opciones = ["Rock Rush", "Asteroid", "Bird Hunt", "Salir"]
rutas = [
    os.path.join("rockrush", "juego.py"),
    os.path.join("asteroid", "main.py"),
    os.path.join("birdhunt", "main.py"),
    None
]
seleccion = 0

def dibujar_menu():
    PANTALLA.fill(FONDO)
    titulo = FUENTE.render("TRIPLELEVEL", True, AZUL)
    PANTALLA.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 80))
    for i, texto in enumerate(opciones):
        color = BLANCO if i == seleccion else GRIS
        render = FUENTE.render(texto, True, color)
        PANTALLA.blit(render, (ANCHO // 2 - render.get_width() // 2, 200 + i * 60))
    pygame.display.flip()

def ejecutar_juego(ruta):
    if ruta:
        pygame.quit()  # Cierra Pygame antes de lanzar el juego
        subprocess.run([sys.executable, ruta])
        
        # Al volver, reiniciar todo lo necesario
        pygame.init()
        global PANTALLA, FUENTE
        PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("TRIPLELEVEL - Menú Principal")
        FUENTE = pygame.font.SysFont("arial", 40)
        return True
    return False


reloj = pygame.time.Clock()
ejecutando = True

while ejecutando:
    dibujar_menu()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                seleccion = (seleccion - 1) % len(opciones)
            elif evento.key == pygame.K_DOWN:
                seleccion = (seleccion + 1) % len(opciones)
            elif evento.key == pygame.K_RETURN:
                if rutas[seleccion] is None:
                    ejecutando = False
                else:
                    volver = ejecutar_juego(rutas[seleccion])
                    if volver:
                        seleccion = 0
    reloj.tick(60)

pygame.quit()
