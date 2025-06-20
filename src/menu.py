import pygame
import sys
from configuracion import ancho, largo

def mostrar_menu():
    pygame.init()
    pantalla = pygame.display.set_mode((ancho, largo))
    pygame.display.set_caption("Deadshoot - Menú")

    fondo_menu = pygame.image.load("imgs/logo.png").convert()
    fondo_menu = pygame.transform.scale(fondo_menu, (ancho, largo))

    fondo_instrucciones = pygame.image.load("imgs/logo4.png").convert()
    fondo_instrucciones = pygame.transform.scale(fondo_instrucciones, (ancho, largo))

    fondo_nombre = pygame.image.load("imgs/logo5.png").convert()
    fondo_nombre = pygame.transform.scale(fondo_nombre, (ancho, largo))

    reloj = pygame.time.Clock()

    zonas_boton = {
        "JUGAR": pygame.Rect(500, 350, 300, 50),
        "INSTRUCCIONES": pygame.Rect(460, 420, 400, 50),
        "SALIR": pygame.Rect(540, 490, 200, 50)
    }

    fuente_boton = pygame.font.SysFont(None, 36)

    def pedir_nombre():
        nombre = ""
        fuente_nombre = pygame.font.SysFont(None, 40)
        input_active = True
        input_rect = pygame.Rect(400, 300, 400, 50)
        color_input_box = pygame.Color('red')
        color_input_text = pygame.Color('white')

        while input_active:
            pantalla.blit(fondo_nombre, (0, 0))

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN and nombre != "":
                        input_active = False
                    elif evento.key == pygame.K_BACKSPACE:
                        nombre = nombre[:-1]
                    else:
                        nombre += evento.unicode

            texto_nombre = fuente_nombre.render(f"Ingresá tu nombre: {nombre}", True, color_input_text)
            pantalla.blit(texto_nombre, (input_rect.x + 10, input_rect.y + 10))
            pygame.draw.rect(pantalla, color_input_box, input_rect, 2)

            pygame.display.update()
            reloj.tick(60)

        return nombre

    def mostrar_instrucciones():
        pantalla.blit(fondo_instrucciones, (0, 0))
        instrucciones_texto = (
            "El juego consiste en derribar los platos que van pasando.\n"
            "Derriba 5 platos para pasar al siguiente nivel.\n"
            "Cada nivel aumenta la velocidad, sé rápido.\n"
            "Solo tienes 10 balas, ¡afina tu puntería!\n"
            "Buena suerte.\n"
            "Pulsa ENTER para volver al menú."
        )

        fuente_instrucciones = pygame.font.SysFont(None, 30)
        lineas = instrucciones_texto.splitlines()

        y_offset = 100
        for linea in lineas:
            texto_render = fuente_instrucciones.render(linea, True, (255, 255, 255))
            pantalla.blit(texto_render, (50, y_offset))
            y_offset += 40

        pygame.display.update()

        esperando = True
        while esperando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                    esperando = False

    while True:
        pantalla.blit(fondo_menu, (0, 0))

        for nombre_boton, rect in zonas_boton.items():
            pygame.draw.rect(pantalla, (0, 0, 0), rect, 0)
            texto = fuente_boton.render(nombre_boton, True, (255, 0, 0))
            texto_rect = texto.get_rect(center=rect.center)
            pantalla.blit(texto, texto_rect)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos = pygame.mouse.get_pos()

                if zonas_boton["JUGAR"].collidepoint(pos):
                    nombre_jugador = pedir_nombre()
                    print(f"Jugador: {nombre_jugador}")
                    return nombre_jugador

                elif zonas_boton["INSTRUCCIONES"].collidepoint(pos):
                    mostrar_instrucciones()

                elif zonas_boton["SALIR"].collidepoint(pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        reloj.tick(60)
