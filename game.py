import pygame
import random
import math
import os
from clases.nave import Nave
from clases.proyectil import Proyectil
from clases.asteroide import Asteroide
from database import guardar_puntuacion, obtener_top5

pygame.init()
FONT_TITULO_CHICO = pygame.font.Font("fuentes/Silkscreen-Regular.ttf", 28)
FONT = pygame.font.Font("fuentes/Silkscreen-Regular.ttf", 24)  
FONT_GRANDE = pygame.font.Font("fuentes/Silkscreen-Regular.ttf", 32)
FONT_TITULO = pygame.font.Font("fuentes/Silkscreen-Regular.ttf", 48)
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids Clone")

fondo_frames = []
fondo_frame_index = 0
fondo_animacion_velocidad = 5  
frame_contador = 0

sonido_game_over = pygame.mixer.Sound('sonidos/gamestart-272829.mp3')
sonido_explosion = pygame.mixer.Sound('sonidos/game-over-arcade-6435.mp3')
sonido_disparo = pygame.mixer.Sound('sonidos/arcade-fx-288597.mp3')

btn_jugar_img = pygame.image.load("img/jugar_de_nuevo.png").convert_alpha()
btn_menu_img = pygame.image.load("img/menu_principal.png").convert_alpha()

game_over_img = pygame.image.load("img/game_over.png").convert_alpha()
fondo_path = "img/fondo_juego"
for nombre_archivo in sorted(os.listdir(fondo_path)):
    if nombre_archivo.endswith(".png"):
        img = pygame.image.load(os.path.join(fondo_path, nombre_archivo)).convert()
        img = pygame.transform.scale(img, (WIDTH, HEIGHT))
        fondo_frames.append(img)

ASTEROID_FRAMES = []
frame_folder = os.path.join(os.path.dirname(__file__), 'img/asteroid_frames')
for i in range(5):
    frame_path = os.path.join(frame_folder, f'frame_{i}.png')
    image = pygame.image.load(frame_path).convert_alpha()
    ASTEROID_FRAMES.append(image)

EXPLOSION_FRAMES = []
explosion_folder = os.path.join("img", "explosion")
for i in range(6):
    frame = pygame.image.load(os.path.join(explosion_folder, f"explosion_{i}.png")).convert_alpha()
    EXPLOSION_FRAMES.append(pygame.transform.scale(frame, (100, 100)))  

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60

def reproducir_explosion(win, x, y, frames):
    sonido_explosion.play()
    for frame in frames:
        win.blit(fondo_frames[fondo_frame_index], (0, 0))  
        win.blit(frame, (x - frame.get_width() // 2, y - frame.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(70)

def pantalla_game_over(puntos, nombre):
    sonido_game_over.play()
    fondo_frame_index = 0
    frame_contador = 0
    fondo_animacion_velocidad = 5

    guardar_puntuacion(nombre, puntos)
    top5 = obtener_top5()

    btn_jugar_rect = btn_jugar_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 130))
    btn_menu_rect = btn_menu_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 180))

    while True:
        frame_contador += 1
        if frame_contador >= fondo_animacion_velocidad:
            fondo_frame_index = (fondo_frame_index + 1) % len(fondo_frames)
            frame_contador = 0

        WIN.blit(fondo_frames[fondo_frame_index], (0, 0))

        WIN.blit(game_over_img, (WIDTH // 2 - game_over_img.get_width() // 2, 40))

        puntos_texto = FONT.render(f"Puntos: {puntos}", True, WHITE)
        WIN.blit(puntos_texto, (WIDTH // 2 - puntos_texto.get_width() // 2, 160))

        y_base = 200
        espaciado_extra = 20  

        titulo = FONT_TITULO_CHICO.render("TOP 5 PUNTUACIONES", True, WHITE)
        WIN.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, y_base))

        for i, (jugador, score) in enumerate(top5):
            texto = FONT.render(f"{i+1}. {jugador}: {score}", True, WHITE)
            WIN.blit(texto, (WIDTH // 2 - texto.get_width() // 2, y_base + 30 + espaciado_extra + i * 25))


        WIN.blit(btn_jugar_img, btn_jugar_rect.topleft)
        WIN.blit(btn_menu_img, btn_menu_rect.topleft)

        pygame.display.update()
        pygame.time.delay(33)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    iniciar_juego(nombre)
                    return
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn_jugar_rect.collidepoint(event.pos):
                    iniciar_juego(nombre)
                    return
                elif btn_menu_rect.collidepoint(event.pos):
                    pygame.mixer.music.load('sonidos/8-bit-heaven-26287.mp3')  
                    pygame.mixer.music.play(-1)  
                    return
                
def mostrar_puntuaciones():
    fondo_frames = []
    fondo_path = "img/fondo_menu"
    for nombre_archivo in sorted(os.listdir(fondo_path)):
        if nombre_archivo.endswith(".png"):
            img = pygame.image.load(os.path.join(fondo_path, nombre_archivo)).convert()
            img = pygame.transform.scale(img, (WIDTH, HEIGHT))
            fondo_frames.append(img)

    pygame.init()
    clock = pygame.time.Clock()
    WHITE = (255, 255, 255)
    FONT = pygame.font.Font("fuentes/Silkscreen-Regular.ttf", 24)  
    FONT_GRANDE = pygame.font.Font("fuentes/Silkscreen-Regular.ttf", 32)
    FONT_TITULO = pygame.font.Font("fuentes/Silkscreen-Regular.ttf", 48)
    
    top5 = obtener_top5()
    mostrando = True
    fondo_index = 0
    fondo_contador = 0
    fondo_velocidad = 5

    while mostrando:
        fondo_contador += 1
        if fondo_contador >= fondo_velocidad:
            fondo_index = (fondo_index + 1) % len(fondo_frames)
            fondo_contador = 0

        WIN.blit(fondo_frames[fondo_index], (0, 0))

        titulo = FONT_TITULO.render("TOP 5 PUNTUACIONES", True, WHITE)
        WIN.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 50))

        for i, (nombre, puntos) in enumerate(top5):
            linea = FONT.render(f"{i+1}. {nombre}: {puntos}", True, WHITE)
            WIN.blit(linea, (WIDTH // 2 - linea.get_width() // 2, 120 + i * 40))

        salir = FONT.render("Presiona ESC para volver", True, (180, 180, 180))
        WIN.blit(salir, (WIDTH // 2 - salir.get_width() // 2, 500))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                mostrando = False

        clock.tick(60)
                    
def mostrar_menu_principal():
    seleccionando = True
    fondo_frame_index = 0
    frame_contador = 0
    fondo_animacion_velocidad = 5

    while seleccionando:
        frame_contador += 1
        if frame_contador >= fondo_animacion_velocidad:
            fondo_frame_index = (fondo_frame_index + 1) % len(fondo_frames)
            frame_contador = 0

        WIN.blit(fondo_frames[fondo_frame_index], (0, 0))

        titulo = FONT.render("ASTEROIDS CLONE", True, WHITE)
        iniciar = FONT.render("1 - Iniciar juego", True, WHITE)
        salir = FONT.render("ESC - Salir", True, WHITE)

        WIN.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, HEIGHT // 2 - 100))
        WIN.blit(iniciar, (WIDTH // 2 - iniciar.get_width() // 2, HEIGHT // 2))
        WIN.blit(salir, (WIDTH // 2 - salir.get_width() // 2, HEIGHT // 2 + 40))

        pygame.display.update()
        pygame.time.delay(33)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    nombre = pedir_nombre_jugador()
                    iniciar_juego(nombre)
                    return
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

def pedir_nombre_jugador():
    nombre = ""
    escribiendo = True

    while escribiendo:
        WIN.fill(BLACK)
        texto = FONT.render("Escribe tu nombre y presiona Enter:", True, WHITE)
        nombre_render = FONT.render(nombre, True, WHITE)
        WIN.blit(texto, (WIDTH // 2 - texto.get_width() // 2, HEIGHT // 2 - 50))
        WIN.blit(nombre_render, (WIDTH // 2 - nombre_render.get_width() // 2, HEIGHT // 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()  
                    return nombre if nombre.strip() != "" else "Jugador"
                elif event.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    if len(nombre) < 12:
                        nombre += event.unicode

def iniciar_juego(nombre):
    print(f"Nombre del jugador: {nombre}")
    clock = pygame.time.Clock()
    nave = Nave()
    asteroides = []
    spawn_timer = 0
    proyectiles = []
    score = 0
    run = True
    can_shoot = True

    max_asteroides = 3  
    frame_contador = 0
    fondo_frame_index = 0

    while run:
        clock.tick(FPS)
        spawn_timer += 1

        if score >= 6000:
            max_asteroides =10 
        elif score >= 3500:
            max_asteroides = 7
        elif score >= 200:
            max_asteroides = 4

        if spawn_timer > 60 and len(asteroides) < max_asteroides:
            asteroides.append(Asteroide(frames=ASTEROID_FRAMES))
            spawn_timer = 0

        WIN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                can_shoot = True

        keys = pygame.key.get_pressed()

        frame_contador += 1
        if frame_contador >= fondo_animacion_velocidad:
            fondo_frame_index = (fondo_frame_index + 1) % len(fondo_frames)
            frame_contador = 0

        WIN.blit(fondo_frames[fondo_frame_index], (0, 0))

        nave.update(keys)

        if keys[pygame.K_SPACE] and can_shoot:
            if len(proyectiles) < 10:
                proyectiles.append(nave.disparar())
                sonido_disparo.play()
                can_shoot = False

        for asteroide in asteroides[:]:
            if nave.rect.colliderect(asteroide.get_rect()):
                nave.vidas -= 1
                if nave.vidas <= 0:
                    reproducir_explosion(WIN, nave.rect.centerx, nave.rect.centery, EXPLOSION_FRAMES)
                    pygame.time.delay(500)
                    pantalla_game_over(score, nombre)
                    return
                else:
                    nave.reiniciar_posicion()
                    asteroides.remove(asteroide)
                    asteroides.extend(asteroide.dividir(ASTEROID_FRAMES))
                break

        for proyectil in proyectiles[:]:
            proyectil.update()
            if not proyectil.is_alive():
                proyectiles.remove(proyectil)

        for proyectil in proyectiles[:]:
            for asteroide in asteroides[:]:
                if proyectil.get_rect().colliderect(asteroide.get_rect()):
                    score += asteroide.get_puntos()
                    proyectiles.remove(proyectil)
                    asteroides.remove(asteroide)
                    asteroides.extend(asteroide.dividir())
                    break

        for asteroide in asteroides:
            asteroide.update()
            asteroide.draw(WIN)

        for proyectil in proyectiles:
            proyectil.draw(WIN)

        nave.draw(WIN)

        texto = FONT.render(f"Puntos: {score}", True, WHITE)
        vidas_texto = FONT.render(f"Vidas: {nave.vidas}", True, WHITE)
        texto_nombre = FONT.render(f"Jugador: {nombre}", True, WHITE)
        
        WIN.blit(texto, (10, 10))
        WIN.blit(vidas_texto, (10, 40))
        WIN.blit(texto_nombre, (10, 70))

        pygame.display.update()
