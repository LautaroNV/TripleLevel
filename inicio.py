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

# Cargar imágenes
logo = pygame.image.load("imgs_menu/logo_triplelevel.png").convert_alpha()
logo = pygame.transform.scale(logo, (300, 150))

img_rock_rush = pygame.image.load("imgs_menu/rock_rush.png").convert_alpha()
img_rock_rush = pygame.transform.scale(img_rock_rush, (250, 80))

img_asteroid = pygame.image.load("imgs_menu/asteroids.png").convert_alpha()
img_asteroid = pygame.transform.scale(img_asteroid, (250, 80))

opciones = ["Rock Rush", "Asteroids", "Bird Hunt", "Salir"]
rect_opciones = []

def ejecutar_juego(ruta):
    if ruta:
        pygame.quit()
        carpeta_juego = os.path.dirname(ruta)
        script_juego = os.path.basename(ruta)
        subprocess.run([sys.executable, script_juego], cwd=carpeta_juego)

        pygame.init()
        global PANTALLA, FUENTE, logo, img_rock_rush, img_asteroid
        PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("TRIPLELEVEL - Menú Principal")
        FUENTE = pygame.font.SysFont("arial", 40)

        logo = pygame.image.load("imgs_menu/logo_triplelevel.png").convert_alpha()
        logo = pygame.transform.scale(logo, (300, 150))

        img_rock_rush = pygame.image.load("imgs_menu/rock_rush.png").convert_alpha()
        img_rock_rush = pygame.transform.scale(img_rock_rush, (250, 80))

        img_asteroid = pygame.image.load("imgs_menu/asteroids.png").convert_alpha()
        img_asteroid = pygame.transform.scale(img_asteroid, (250, 80))

        return True
    return False

def dibujar_menu(pos_mouse):
    PANTALLA.fill(NEGRO)
    PANTALLA.blit(logo, (ANCHO // 2 - logo.get_width() // 2, 30))
    rect_opciones.clear()

    for i, opcion in enumerate(opciones):
        x = ANCHO // 2
        y = 220 + i * 80

        if opcion == "Rock Rush":
            rect = img_rock_rush.get_rect(center=(x, y))
            if rect.collidepoint(pos_mouse):
                resaltada = pygame.transform.scale(img_rock_rush, (270, 90))
                rect = resaltada.get_rect(center=(x, y))
                PANTALLA.blit(resaltada, rect.topleft)
            else:
                PANTALLA.blit(img_rock_rush, rect.topleft)

        elif opcion == "Asteroids":
            rect = img_asteroid.get_rect(center=(x, y))
            if rect.collidepoint(pos_mouse):
                resaltada = pygame.transform.scale(img_asteroid, (270, 90))
                rect = resaltada.get_rect(center=(x, y))
                PANTALLA.blit(resaltada, rect.topleft)
            else:
                PANTALLA.blit(img_asteroid, rect.topleft)

        else:
            color = AZUL if pygame.Rect(x - 100, y - 20, 200, 40).collidepoint(pos_mouse) else BLANCO
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
                    elif opcion == "Asteroids":
                        ejecutar_juego(os.path.join("asteroids", "main.py"))
                    elif opcion == "Bird Hunt":
                        ejecutar_juego(os.path.join("birdhunt", "src", "main.py"))
                    elif opcion == "Salir":
                        pygame.quit()
                        sys.exit()
