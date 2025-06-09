import pygame
import sys
from componentes.nota import Note
from componentes.traste import TrasteGuitarra
from componentes.menu import mostrar_menu, mostrar_instrucciones
from canciones.cancion1 import notas
from recursos.colores import *

pygame.init()
ANCHO, ALTO = 800, 900
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Note Rush")
FPS = 60
RELOJ = pygame.time.Clock()

ESTADO = "menu"
COLUMNA_TECLAS = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_g]
CANT_COLUMNAS = 5
TIEMPO_TOTAL = 78_000  # duración exacta Mississippi Queen en GH3 medio
VELOCIDAD = 4.5

def juego():
    global ESTADO
    tiempo_inicio = pygame.time.get_ticks()
    traste = TrasteGuitarra(ANCHO, ALTO, CANT_COLUMNAS)

    # 👇 Esta línea permite cargar notas con duraciones (para holds)
    notas_activas = [Note(*n, ancho_total=ANCHO) for n in notas]

    nota_idx = 0
    activas = []

    presionadas = [False] * CANT_COLUMNAS
    combo = 0
    puntuacion = 0

    ejecutando = True
    while ejecutando:
        RELOJ.tick(FPS)
        ahora = pygame.time.get_ticks()
        tiempo_rel = ahora - tiempo_inicio

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key in COLUMNA_TECLAS:
                    col = COLUMNA_TECLAS.index(evento.key)
                    presionadas[col] = True
                    for nota in activas:
                        if nota.column == col and nota.en_zona(traste.y_zona, traste.altura_zona) and not nota.tocada:
                            nota.tocar()
                            puntuacion += 100
                            combo += 1
                            break
                    else:
                        combo = 0
            if evento.type == pygame.KEYUP:
                if evento.key in COLUMNA_TECLAS:
                    col = COLUMNA_TECLAS.index(evento.key)
                    presionadas[col] = False
                    for nota in activas:
                        if nota.column == col and nota.en_hold:
                            nota.soltar()


        # Activar nuevas notas según tiempo
        while nota_idx < len(notas_activas) and notas_activas[nota_idx].inicio <= tiempo_rel:
            activas.append(notas_activas[nota_idx])
            nota_idx += 1

        # Actualizar notas
        for nota in activas:
            nota.actualizar(VELOCIDAD)

        activas = [n for n in activas if not n.fuera_de_pantalla(ALTO)]

        # Dibujar
        PANTALLA.fill(NEGRO)
        traste.dibujar(PANTALLA, presionadas)

        for nota in activas:
            nota.dibujar(PANTALLA)

        # Puntuación
        fuente = pygame.font.SysFont("Arial", 28)
        puntos_txt = fuente.render(f"Puntos: {puntuacion}", True, BLANCO)
        combo_txt = fuente.render(f"Combo: {combo}", True, AZUL)
        PANTALLA.blit(puntos_txt, (20, 20))
        PANTALLA.blit(combo_txt, (20, 60))

        pygame.display.flip()

        if tiempo_rel >= TIEMPO_TOTAL:
            ESTADO = "menu"
            ejecutando = False


while True:
    if ESTADO == "menu":
        ESTADO = mostrar_menu(PANTALLA)
    elif ESTADO == "instrucciones":
        ESTADO = mostrar_instrucciones(PANTALLA)
    elif ESTADO == "jugar":
        juego()
