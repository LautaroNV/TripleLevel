import pygame
import sys
from configuracion import ancho, largo, fondo_color, platos_para_pasar
from plato import Plato
from nivel import ejecutar_nivel, seleccionar_nivel
from menu import mostrar_menu

pygame.init()
pygame.mixer.init()

pantalla = pygame.display.set_mode((ancho, largo))
pygame.display.set_caption("Deadshoot")
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont(None, 36)

sonido_disparo = pygame.mixer.Sound("Sonido/pistol-sound.mp3")
sonido_musica = pygame.mixer.Sound("Sonido/music.mp3")
pygame.mixer.Sound.play(sonido_musica, loops=-1)
arma_esperando = pygame.image.load("imgs/arma_apuntando.png").convert_alpha()
arma_disparo = pygame.image.load("imgs/arma_disparando.png").convert_alpha()
arma_retroceso = pygame.image.load("imgs/arma_esperando.png").convert_alpha()

imagen_fondo_nivel_1 = pygame.image.load("imgs/img6.png").convert()
imagen_fondo_nivel_2 = pygame.image.load("imgs/img6.png").convert()
imagen_fondo_nivel_3 = pygame.image.load("imgs/img6.png").convert()
logo = pygame.image.load("imgs/logo3.png").convert_alpha()

def volver_al_menu():
    mostrar_menu()
    nivel_elegido = seleccionar_nivel(pantalla, ancho, fuente, largo, logo)
    if nivel_elegido == 1:
        nivel = niveles[0]
    elif nivel_elegido == 2:
        nivel = niveles[1]
    else:
        nivel = niveles[2]
    pygame.display.set_caption(nivel["titulo"])
    return nivel

def crear_platos_separados(cantidad, y, ancho_total, largo_total):
    platos = []
    espacio = ancho_total // (cantidad + 1)
    for i in range(cantidad):
        x = espacio * (i + 1) - 30
        platos.append(Plato(x, y, ancho_total, largo_total))
    return platos

niveles = [
    {
        "titulo": "Deadshoot - Nivel 1",
        "platos": crear_platos_separados(2, largo - 100, ancho, largo),
        "fondo": imagen_fondo_nivel_1,
        "mensaje": "¡Nivel 1 superado!"
    },
    {
        "titulo": "Deadshoot - Nivel 2",
        "platos": crear_platos_separados(3, largo - 100, ancho, largo),
        "fondo": imagen_fondo_nivel_2,
        "mensaje": "¡Nivel 2 superado!"
    },
    {
        "titulo": "Deadshoot - Nivel 3",
        "platos": crear_platos_separados(4, largo - 100, ancho, largo),
        "fondo": imagen_fondo_nivel_3,
        "mensaje": "¡Nivel 3 superado! Fin del juego."
    }
]

puntacion = 0

def iniciar_juego():
    global puntacion
    nivel = volver_al_menu()
    while True:
        puntacion = ejecutar_nivel(
            pantalla, reloj, fuente, nivel["platos"], platos_para_pasar,
            sonido_disparo, ancho, nivel["fondo"], nivel["mensaje"],
            arma_esperando, arma_disparo, arma_retroceso, puntacion
        )
        if puntacion == -1:
            break
        nivel = volver_al_menu()

def controlar_eventos():
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                confirmar_salida()

def confirmar_salida():
    pantalla.fill((0, 0, 0))
    texto = fuente.render("¿Seguro que deseas salir? (S para salir / C para continuar)", True, (255, 255, 255))
    pantalla.blit(texto, (ancho // 2 - 250, largo // 2))
    pygame.display.update()
    salir = False
    while not salir:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_s:
                    pygame.quit()
                    sys.exit()
                elif evento.key == pygame.K_c:
                    salir = True
                    pygame.display.set_caption("Deadshoot")

iniciar_juego()
