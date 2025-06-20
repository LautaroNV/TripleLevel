import pygame
import sys
import sqlite3
from componentes.nota import Note
from componentes.hold import HoldNote
from componentes.traste import TrasteGuitarra
from componentes.resultados import pantalla_resultado
from componentes.menu import menu_principal as mostrar_menu, mostrar_instrucciones, mostrar_seleccion_nivel
from componentes.menu import mostrar_puntuaciones
from canciones.cancion1 import notas as cancion1
from canciones.cancion2 import notas as cancion2
from canciones.cancion3 import notas as cancion3
from recursos.colores import *

pygame.init()
ANCHO, ALTO = 800, 900
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Rock Rush")
FPS = 60
RELOJ = pygame.time.Clock()

ESTADO = "menu"
COLUMNA_TECLAS = [pygame.K_a, pygame.K_s, pygame.K_j, pygame.K_k, pygame.K_l]
CANT_COLUMNAS = 5
VELOCIDAD = 15

fondo = pygame.image.load("imgs/background3.png").convert()
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

archivos_canciones = {
    "jugar_1": "canciones/cancion1.wav",
    "jugar_2": "canciones/cancion2.wav",
    "jugar_3": "canciones/cancion3.wav",
}

tiempos_canciones = {
    "jugar_1": 150000,
    "jugar_2": 190000,
    "jugar_3": 170000,
}

def juego(notas, estado_actual):
    global ESTADO
    tiempo_inicio = pygame.time.get_ticks()
    traste = TrasteGuitarra(ANCHO, ALTO, CANT_COLUMNAS)
    tiempo_total = tiempos_canciones.get(estado_actual, 90000)
    archivo_musica = archivos_canciones.get(estado_actual)
    if archivo_musica:
        pygame.mixer.music.load(archivo_musica)
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play()

    notas_activas = [HoldNote(*n, ancho_total=ANCHO) if len(n) == 3 else Note(*n, ancho_total=ANCHO) for n in notas]
    nota_idx = 0
    activas = []
    presionadas = [False] * CANT_COLUMNAS
    combo = 0
    combo_max = 0
    puntuacion = 0
    vidas = 50
    aciertos = 0

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
                            if isinstance(nota, HoldNote):
                                nota.tocar(traste.y_zona)
                            else:
                                nota.tocar()
                            puntuacion += 100
                            combo += 1
                            combo_max = max(combo_max, combo)
                            aciertos += 1
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
                        if isinstance(nota, HoldNote) and nota.column == col and nota.en_hold:
                            nota.soltar(ahora)
                            if not nota.completada:
                                combo = 0
                                vidas -= 1
                            break

        while nota_idx < len(notas_activas) and notas_activas[nota_idx].inicio <= tiempo_rel:
            activas.append(notas_activas[nota_idx])
            nota_idx += 1

        nuevas_activas = []
        for nota in activas:
            if isinstance(nota, HoldNote):
                nota.actualizar(VELOCIDAD, ahora)
            else:
                nota.actualizar(VELOCIDAD)

            # Si ya salió de la pantalla y no fue tocada, penaliza
            if nota.fuera_de_pantalla(ALTO):
                if not nota.tocada:
                    combo = 0
                    vidas -= 1
                continue  # no se agrega a nuevas_activas
            nuevas_activas.append(nota)
        activas = nuevas_activas

        PANTALLA.blit(fondo, (0, 0))
        traste.dibujar(PANTALLA, presionadas)
        for nota in activas:
            nota.dibujar(PANTALLA)

        fuente = pygame.font.Font("recursos/fuentes/Hyperwave-One.ttf", 28)
        PANTALLA.blit(fuente.render(f"Puntos: {puntuacion}", True, BLANCO), (20, 20))
        PANTALLA.blit(fuente.render(f"Combo: {combo}", True, AZUL), (20, 60))
        pygame.draw.rect(PANTALLA, ROJO, (20, 100, 200, 20))
        pygame.draw.rect(PANTALLA, VERDE, (20, 100, max(0, int(200 * (vidas / 50))), 20))
        PANTALLA.blit(fuente.render("Vida", True, BLANCO), (230, 98))

        pygame.display.flip()

        if tiempo_rel >= tiempo_total or vidas <= 0:
            pygame.mixer.music.stop()
            pantalla_resultado(PANTALLA, puntuacion, combo_max, aciertos, estado_actual)
            ESTADO = "menu"
            ejecutando = False

# Bucle principal
while True:
    if ESTADO == "menu":
        ESTADO = mostrar_menu(PANTALLA)
    elif ESTADO == "instrucciones":
        ESTADO = mostrar_instrucciones(PANTALLA)
    elif ESTADO == "elegir_nivel":
        ESTADO = mostrar_seleccion_nivel(PANTALLA)
    elif ESTADO == "puntuaciones":
        ESTADO = mostrar_puntuaciones(PANTALLA)
    elif ESTADO == "jugar_1":
        juego(cancion1, "jugar_1")
    elif ESTADO == "jugar_2":
        juego(cancion2, "jugar_2")
    elif ESTADO == "jugar_3":
        juego(cancion3, "jugar_3")
