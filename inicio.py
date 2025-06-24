import pygame
import sys
import subprocess
import os
import math

pygame.init()
pygame.mixer.init()

ANCHO, ALTO = 900, 600
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("TRIPLELEVEL - Menú Principal")

FUENTE = pygame.font.SysFont("arial", 40, bold=True)
BLANCO = (255, 255, 255)
ROJO = (147, 17, 17)
NEGRO = (0, 0, 0)
AZUL = (50, 150, 255)
DORADO = (218, 165, 32)

# Música de fondo del menú
pygame.mixer.music.load("imgs_menu/menu_inicio.wav")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

# Cargar imágenes
logo = pygame.image.load("imgs_menu/logo_triplelevel.png").convert_alpha()
logo = pygame.transform.scale(logo, (320, 160))

logo_bird = pygame.image.load("imgs_menu/bird_hunter.png").convert_alpha()
logo_bird = pygame.transform.smoothscale(logo_bird, (320, 160))  # Más grande

img_rock_rush = pygame.image.load("imgs_menu/rock_rush.png").convert_alpha()
img_rock_rush = pygame.transform.smoothscale(img_rock_rush, (250, 80))

img_asteroid = pygame.image.load("imgs_menu/asteroids.png").convert_alpha()
img_asteroid = pygame.transform.smoothscale(img_asteroid, (250, 80))

opciones = ["Rock Rush", "Asteroids", "Bird Hunt", "Salir"]
rect_opciones = []

def ejecutar_juego(ruta):
    if ruta:
        pygame.mixer.music.stop()  # Detener música del menú
        pygame.quit()
        carpeta_juego = os.path.dirname(ruta)
        script_juego = os.path.basename(ruta)
        subprocess.run([sys.executable, script_juego], cwd=carpeta_juego)
        pygame.init()
        pygame.mixer.init()
        global PANTALLA, FUENTE, logo, img_rock_rush, img_asteroid, logo_bird
        PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("TRIPLELEVEL - Menú Principal")
        FUENTE = pygame.font.SysFont("arial", 40, bold=True)
        logo = pygame.image.load("imgs_menu/logo_triplelevel.png").convert_alpha()
        logo = pygame.transform.scale(logo, (320, 160))
        logo_bird = pygame.image.load("imgs_menu/bird_hunter.png").convert_alpha()
        logo_bird = pygame.transform.smoothscale(logo_bird, (320, 160))
        img_rock_rush = pygame.image.load("imgs_menu/rock_rush.png").convert_alpha()
        img_rock_rush = pygame.transform.smoothscale(img_rock_rush, (250, 80))
        img_asteroid = pygame.image.load("imgs_menu/asteroids.png").convert_alpha()
        img_asteroid = pygame.transform.smoothscale(img_asteroid, (250, 80))
        # Volver a poner la música del menú al regresar
        pygame.mixer.music.load("imgs_menu/menu_inicio.wav")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
        return True
    return False

def animar_fondo(t):
    # Degradado animado entre ROJO y NEGRO
    for y in range(0, ALTO, 2):
        factor = (math.sin(t + y / 60) + 1) / 2
        color = (
            int(ROJO[0] * factor + NEGRO[0] * (1 - factor)),
            int(ROJO[1] * factor + NEGRO[1] * (1 - factor)),
            int(ROJO[2] * factor + NEGRO[2] * (1 - factor)),
        )
        pygame.draw.rect(PANTALLA, color, (0, y, ANCHO, 2))

def dibujar_menu(pos_mouse, t):
    animar_fondo(t)
    PANTALLA.blit(logo, (ANCHO // 2 - logo.get_width() // 2, 30))
    rect_opciones.clear()

    # Opciones de juegos (sin "Salir")
    juegos = ["Rock Rush", "Asteroids", "Bird Hunt"]
    total_juegos = len(juegos)
    margen = 180  # Ajusta este valor para más/menos separación lateral
    espacio = (ANCHO - 2 * margen) // (total_juegos - 1)
    y = 300  # Altura para las opciones de juegos

    for i, opcion in enumerate(juegos):
        x = margen + i * espacio
        resaltado = False

        if opcion == "Rock Rush":
            rect = img_rock_rush.get_rect(center=(x, y))
            if rect.collidepoint(pos_mouse):
                resaltado = True
                escala = 1.12 + 0.03 * math.sin(t * 2)
                img = pygame.transform.smoothscale(img_rock_rush, (int(250 * escala), int(80 * escala)))
                rect = img.get_rect(center=(x, y))
                PANTALLA.blit(img, rect.topleft)
            else:
                PANTALLA.blit(img_rock_rush, rect.topleft)

        elif opcion == "Asteroids":
            rect = img_asteroid.get_rect(center=(x, y))
            if rect.collidepoint(pos_mouse):
                resaltado = True
                escala = 1.12 + 0.03 * math.sin(t * 2)
                img = pygame.transform.smoothscale(img_asteroid, (int(250 * escala), int(80 * escala)))
                rect = img.get_rect(center=(x, y))
                PANTALLA.blit(img, rect.topleft)
            else:
                PANTALLA.blit(img_asteroid, rect.topleft)

        elif opcion == "Bird Hunt":
            rect = logo_bird.get_rect(center=(x, y))
            if rect.collidepoint(pos_mouse):
                resaltado = True
                escala = 1.13 + 0.03 * math.sin(t * 2)
                img = pygame.transform.smoothscale(logo_bird, (int(320 * escala), int(160 * escala)))
                rect = img.get_rect(center=(x, y))
                PANTALLA.blit(img, rect.topleft)
            else:
                PANTALLA.blit(logo_bird, rect.topleft)

        rect_opciones.append((rect, opcion))

    # Opción "Salir" debajo, centrada
    salir_y = y + 140
    x = ANCHO // 2
    color = DORADO if pygame.Rect(x - 100, salir_y - 25, 200, 50).collidepoint(pos_mouse) else BLANCO
    escala = 1.10 if color == DORADO else 1.0
    texto = FUENTE.render("Salir", True, color)
    rect = texto.get_rect(center=(x, salir_y))
    if escala > 1.0:
        texto = pygame.transform.smoothscale(texto, (int(rect.width * escala), int(rect.height * escala)))
        rect = texto.get_rect(center=(x, salir_y))
    PANTALLA.blit(texto, rect.topleft)
    rect_opciones.append((rect, "Salir"))

    pygame.display.flip()

# Bucle principal
clock = pygame.time.Clock()
t = 0
while True:
    t += clock.get_time() / 1000
    pos_mouse = pygame.mouse.get_pos()
    dibujar_menu(pos_mouse, t)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
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
                        pygame.mixer.music.stop()
                        pygame.quit()
                        sys.exit()
    clock.tick(60)
