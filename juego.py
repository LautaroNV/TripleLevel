import pygame
import sys
from componentes.nota import Note
from componentes.hold import HoldNote
from componentes.traste import TrasteGuitarra
from componentes.menu import menu_principal as mostrar_menu, mostrar_instrucciones
from canciones.cancion1 import notas
from recursos.colores import *

pygame.init()
ANCHO, ALTO = 800, 900
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Rock Rush")
FPS = 60
RELOJ = pygame.time.Clock()

ESTADO = "menu"
COLUMNA_TECLAS = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_g]
CANT_COLUMNAS = 5
TIEMPO_TOTAL = 78_000
VELOCIDAD = 4.5

def juego():
    global ESTADO
    tiempo_inicio = pygame.time.get_ticks()
    traste = TrasteGuitarra(ANCHO, ALTO, CANT_COLUMNAS)

    # Cargar notas mixtas (tap y hold)
    notas_activas = []
    for n in notas:
        if len(n) == 3:
            notas_activas.append(HoldNote(*n, ancho_total=ANCHO))
        else:
            notas_activas.append(Note(*n, ancho_total=ANCHO))

    nota_idx = 0
    activas = []

    presionadas = [False] * CANT_COLUMNAS
    combo = 0
    puntuacion = 0
    vidas = 5  # máximo

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
                    acierto = False
                    for nota in activas:
                        if nota.column == col and nota.en_zona(traste.y_zona, traste.altura_zona) and not nota.tocada:
                            nota.tocar()
                            puntuacion += 100
                            combo += 1
                            acierto = True
                            break
                    if not acierto:
                        combo = 0
                        vidas -= 1
            if evento.type == pygame.KEYUP:
                if evento.key in COLUMNA_TECLAS:
                    col = COLUMNA_TECLAS.index(evento.key)
                    presionadas[col] = False
                    for nota in activas:
                        if hasattr(nota, 'en_hold') and nota.column == col and nota.en_hold:
                            nota.soltar()
                            combo = 0
                            vidas -= 1
                            break

        # Activar nuevas notas
        while nota_idx < len(notas_activas) and notas_activas[nota_idx].inicio <= tiempo_rel:
            activas.append(notas_activas[nota_idx])
            nota_idx += 1

        # Actualizar y eliminar notas fuera de pantalla
        for nota in activas:
            nota.actualizar(VELOCIDAD)

        nuevas_activas = []
        for nota in activas:
            if nota.fuera_de_pantalla(ALTO):
                if not nota.tocada:
                    vidas -= 1
                    combo = 0
            else:
                nuevas_activas.append(nota)
        activas = nuevas_activas

        # Dibujar
        PANTALLA.fill(NEGRO)
        traste.dibujar(PANTALLA, presionadas)

        for nota in activas:
            nota.dibujar(PANTALLA)

        # UI: Puntuación, combo, vidas
        fuente = pygame.font.SysFont("Arial", 28)
        puntos_txt = fuente.render(f"Puntos: {puntuacion}", True, BLANCO)
        combo_txt = fuente.render(f"Combo: {combo}", True, AZUL)
        PANTALLA.blit(puntos_txt, (20, 20))
        PANTALLA.blit(combo_txt, (20, 60))

        # Barra de vida visual
        pygame.draw.rect(PANTALLA, ROJO, (20, 100, 200, 25))
        pygame.draw.rect(PANTALLA, VERDE, (20, 100, max(0, int(200 * (vidas / 5))), 25))
        vida_txt = fuente.render(f"Vida", True, BLANCO)
        PANTALLA.blit(vida_txt, (230, 98))

        pygame.display.flip()

        if tiempo_rel >= TIEMPO_TOTAL or vidas <= 0:
            ESTADO = "menu"
            ejecutando = False

# Bucle principal
while True:
    if ESTADO == "menu":
        ESTADO = mostrar_menu(PANTALLA)
    elif ESTADO == "instrucciones":
        ESTADO = mostrar_instrucciones(PANTALLA)
    elif ESTADO == "jugar":
        juego()