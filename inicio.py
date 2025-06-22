import pygame
import sys
import subprocess
import os

pygame.init()

ANCHO, ALTO = 800, 600
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("TRIPLELEVEL - Menú Principal")

FUENTE = pygame.font.SysFont("arial", 40)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (50, 150, 255)

opciones = ["Rock Rush", "Asteroid", "Bird Hunt", "Salir"]
opcion_seleccionada = 0

def ejecutar_juego(ruta):
    if ruta:
        pygame.quit()
        subprocess.run([sys.executable, ruta])

        pygame.init()
        global PANTALLA, FUENTE
        PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("TRIPLELEVEL - Menú Principal")
        FUENTE = pygame.font.SysFont("arial", 40)
        return True
    return False

def dibujar_menu():
    PANTALLA.fill(NEGRO)
    titulo = FUENTE.render("Elige un juego", True, BLANCO)
    PANTALLA.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 100))

    for i, opcion in enumerate(opciones):
        color = AZUL if i == opcion_seleccionada else BLANCO
        texto = FUENTE.render(opcion, True, color)
        PANTALLA.blit(texto, (ANCHO // 2 - texto.get_width() // 2, 200 + i * 60))

    pygame.display.flip()

while True:
    dibujar_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                opcion_seleccionada = (opcion_seleccionada - 1) % len(opciones)
            elif event.key == pygame.K_DOWN:
                opcion_seleccionada = (opcion_seleccionada + 1) % len(opciones)
            elif event.key == pygame.K_RETURN:
                if opciones[opcion_seleccionada] == "Rock Rush":
                    ejecutar_juego(os.path.join("rockrush", "juego.py"))
                elif opciones[opcion_seleccionada] == "Asteroid":
                    ejecutar_juego(os.path.join("asteroid", "main.py"))
                elif opciones[opcion_seleccionada] == "Bird Hunt":
                    ejecutar_juego(os.path.join("birdhunt", "src", "main.py"))
                elif opciones[opcion_seleccionada] == "Salir":
                    pygame.quit()
                    sys.exit()