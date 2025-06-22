import pygame
import sys
from game import iniciar_juego, mostrar_puntuaciones
import os

pygame.init()


FONT = pygame.font.Font("fuentes/Silkscreen-Regular.ttf", 24) 
FONT_GRANDE = pygame.font.Font("fuentes/Silkscreen-Regular.ttf", 32)
FONT_TITULO = pygame.font.Font("fuentes/Silkscreen-Regular.ttf", 48)
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids - Menú Principal")

FONT = pygame.font.Font("fuentes/Silkscreen-Regular.ttf", 24) 
FONT_GRANDE = pygame.font.Font("fuentes/Silkscreen-Regular.ttf", 32)
FONT_TITULO = pygame.font.Font("fuentes/Silkscreen-Regular.ttf", 48)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BLUE = (0, 120, 255)

menu_fondo_frames = []
menu_fondo_path = "img/fondo_menu"
for nombre_archivo in sorted(os.listdir(menu_fondo_path)):
    if nombre_archivo.endswith(".png"):
        img = pygame.image.load(os.path.join(menu_fondo_path, nombre_archivo)).convert()
        img = pygame.transform.scale(img, (WIDTH, HEIGHT))
        menu_fondo_frames.append(img)

menu_fondo_index = 0
menu_fondo_velocidad = 5
menu_fondo_contador = 0

def dibujar_texto(texto, y):
    render = FONT.render(texto, True, WHITE)
    rect = render.get_rect(center=(WIDTH // 2, y))
    WIN.blit(render, rect)
    return rect

def pedir_nombre():
    global menu_fondo_index, menu_fondo_contador
    nombre = ""
    escribiendo = True
    clock = pygame.time.Clock()

    titulo_nombre_img = pygame.image.load("img/titulo_nombre.png").convert_alpha()

    while escribiendo:
        menu_fondo_contador += 1
        if menu_fondo_contador >= menu_fondo_velocidad:
            menu_fondo_index = (menu_fondo_index + 1) % len(menu_fondo_frames)
            menu_fondo_contador = 0

        WIN.blit(menu_fondo_frames[menu_fondo_index], (0, 0))

        titulo_nombre_rect = titulo_nombre_img.get_rect(center=(WIDTH // 2, 200))
        WIN.blit(titulo_nombre_img, titulo_nombre_rect)

        input_render = FONT.render(nombre, True, WHITE)
        input_rect = input_render.get_rect(center=(WIDTH // 2, 300))
        WIN.blit(input_render, input_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and nombre:
                    pygame.mixer.music.stop()  
                    escribiendo = False

                elif event.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    if len(nombre) < 12:
                        nombre += event.unicode

        clock.tick(60)
    return nombre

def menu_principal():
    global menu_fondo_index, menu_fondo_contador
    clock = pygame.time.Clock()

    pygame.mixer.music.load("sonidos/8-bit-heaven-26287.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    volumen_on_img = pygame.image.load("img/volumen/volumen.png").convert_alpha()
    volumen_off_img = pygame.image.load("img/volumen/volumen2.png").convert_alpha()
    volumen_on_img = pygame.transform.scale(volumen_on_img, (48, 48))  
    volumen_rect = volumen_on_img.get_rect(topleft=(10, 10)) 

    musica_activa = True

    start_img = pygame.image.load("img/start.png").convert_alpha()
    start_img = pygame.transform.scale(start_img, (150, 70))

    salir_img = pygame.image.load("img/salir.png").convert_alpha()
    salir_img = pygame.transform.scale(salir_img, (140, 60))

    puntuaciones_img = pygame.image.load("img/puntuaciones.png").convert_alpha()
    puntuaciones_img = pygame.transform.scale(puntuaciones_img, (200, 73))

    while True:
        menu_fondo_contador += 1
        if menu_fondo_contador >= menu_fondo_velocidad:
            menu_fondo_index = (menu_fondo_index + 1) % len(menu_fondo_frames)
            menu_fondo_contador = 0

        WIN.blit(menu_fondo_frames[menu_fondo_index], (0, 0))

        titulo_img = pygame.image.load("img/logo_menu.png").convert_alpha()
        titulo_img = pygame.transform.scale(titulo_img, (550, 190))
        WIN.blit(titulo_img, (WIDTH // 2 - titulo_img.get_width() // 2, 2))

        start_btn_rect = start_img.get_rect(center=(WIDTH // 2, 250))
        puntuaciones_btn_rect = puntuaciones_img.get_rect(center=(WIDTH // 2, 340))
        salir_btn_rect = salir_img.get_rect(center=(WIDTH // 2, 430))

        WIN.blit(start_img, start_btn_rect)
        WIN.blit(puntuaciones_img, puntuaciones_btn_rect)
        WIN.blit(salir_img, salir_btn_rect)

        
        if musica_activa:
            WIN.blit(volumen_on_img, volumen_rect)
        else:
            WIN.blit(volumen_off_img, volumen_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn_rect.collidepoint(event.pos):
                    nombre = pedir_nombre()
                    iniciar_juego(nombre)
                elif puntuaciones_btn_rect.collidepoint(event.pos):
                    mostrar_puntuaciones()
                elif salir_btn_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                elif volumen_rect.collidepoint(event.pos):
                
                    if musica_activa:
                        pygame.mixer.music.pause()
                        musica_activa = False
                    else:
                        pygame.mixer.music.unpause()
                        musica_activa = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_3:
                    pygame.quit()
                    sys.exit()

        clock.tick(60)

if __name__ == "__main__":
    menu_principal()
