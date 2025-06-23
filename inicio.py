import pygame
import sys
import subprocess
import os

pygame.init()

ANCHO, ALTO = 800, 600
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("TRIPLELEVEL - Menú Principal")

FUENTE = pygame.font.SysFont("arial", 48)
BLANCO = (255, 255, 255)
AZUL = (50, 150, 255)
NEGRO = (0, 0, 0)

opciones = ["Rock Rush"]
rect_opciones = []

def ejecutar_juego(ruta):
    if ruta:
        pygame.quit()
        carpeta_juego = os.path.dirname(ruta)
        script_juego = os.path.basename(ruta)
        subprocess.run([sys.executable, script_juego], cwd=carpeta_juego)
        pygame.init()
        global PANTALLA, FUENTE
        PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("TRIPLELEVEL - Menú Principal")
        FUENTE = pygame.font.SysFont("arial", 48)
        return True
    return False

def dibujar_menu(pos_mouse):
    PANTALLA.fill(NEGRO)
    rect_opciones.clear()

    for i, opcion in enumerate(opciones):
        x = ANCHO // 2
        y = 250 + i * 100
        color = AZUL if pygame.Rect(x - 150, y - 30, 300, 60).collidepoint(pos_mouse) else BLANCO
        texto = FUENTE.render(opcion, True, color)
        rect = texto.get_rect(center=(x, y))
        PANTALLA.blit(texto, rect.topleft)
        rect_opciones.append((rect, opcion))

    pygame.display.flip()

# Bucle principal
while True:
    pos_mouse = pygame.mouse.get_pos()
    dibujar_menu(pos_mouse)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for rect, opcion in rect_opciones:
                if rect.collidepoint(event.pos):
                    if opcion == "Rock Rush":
                        ejecutar_juego(os.path.join("rockrush", "juego.py"))
