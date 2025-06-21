# birdhunt/main.py
import pygame
import sys

def menu_birdhunt():
    pygame.init()
    ANCHO, ALTO = 800, 600
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Bird Hunt")
    fuente = pygame.font.SysFont("arial", 36)
    reloj = pygame.time.Clock()
    opciones = ["Iniciar juego (demo)", "Volver"]
    seleccion = 0
    ejecutando = True

    while ejecutando:
        pantalla.fill((30, 15, 0))
        titulo = fuente.render("BIRD HUNT", True, (255, 200, 100))
        pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 80))

        for i, texto in enumerate(opciones):
            color = (255, 255, 255) if i == seleccion else (150, 150, 150)
            render = fuente.render(texto, True, color)
            pantalla.blit(render, (ANCHO // 2 - render.get_width() // 2, 200 + i * 60))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif evento.key == pygame.K_RETURN:
                    if seleccion == 0:
                        print("Aquí arrancaría el juego de Bird Hunt 🦆")
                    elif seleccion == 1:
                        ejecutando = False

        reloj.tick(60)

    pygame.quit()

if __name__ == "__main__":
    menu_birdhunt()
