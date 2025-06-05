import pygame
import sys
from canciones import cancion1
from componentes.nota import Nota
from componentes.traste import dibujar_traste
from componentes.menu import mostrar_menu, mostrar_instrucciones

ANCHO, ALTO = 640, 480
FPS = 60

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Rock Rush")
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("arial", 30)

    estado = "menu"
    tiempo_inicio = 0
    notas = []
    indice = 0

    while True:
        pantalla.fill((0, 0, 0))
        tiempo_actual = pygame.time.get_ticks() - tiempo_inicio

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if estado == "menu":
                    if evento.key == pygame.K_1:
                        estado = "juego"
                        tiempo_inicio = pygame.time.get_ticks()
                        notas = []
                        indice = 0
                    elif evento.key == pygame.K_2:
                        estado = "instrucciones"
                    elif evento.key == pygame.K_3:
                        pygame.quit()
                        sys.exit()
                elif estado == "instrucciones" and evento.key == pygame.K_ESCAPE:
                    estado = "menu"
                elif estado == "juego" and evento.key == pygame.K_ESCAPE:
                    estado = "menu"

        if estado == "menu":
            mostrar_menu(pantalla, fuente)

        elif estado == "instrucciones":
            mostrar_instrucciones(pantalla, fuente)

        elif estado == "juego":
            while indice < len(cancion1.notas) and tiempo_actual >= cancion1.notas[indice]["tiempo"]:
                nota_info = cancion1.notas[indice]
                notas.append(Nota(**nota_info))
                indice += 1

            for nota in notas:
                nota.actualizar()
                nota.dibujar(pantalla)

            dibujar_traste(pantalla, ALTO)

        pygame.display.flip()
        reloj.tick(FPS)

if __name__ == "__main__":
    main()
