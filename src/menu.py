import pygame
import sys
from configuracion import ancho, largo

def mostrar_menu():
    pygame.init()
    pantalla = pygame.display.set_mode((ancho, largo))
    pygame.display.set_caption("Deadshoot - Menú")

    fondo = pygame.image.load("imgs/fondo.png").convert()
    fondo = pygame.transform.scale(fondo, (ancho, largo))

    color_normal = (180, 180, 180)
    color_hover = (255, 255, 0)
    color_borde = (0, 0, 0)
    fuente = pygame.font.SysFont(None, 50)
    fuente_titulo = pygame.font.SysFont(None, 60)
    reloj = pygame.time.Clock()

    def boton(pantalla, texto, x, y, ancho, alto):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + ancho and y < mouse[1] < y + alto:
            pygame.draw.rect(pantalla, color_hover, (x, y, ancho, alto))
            if click[0] == 1:
                return True
        else:
            pygame.draw.rect(pantalla, color_normal, (x, y, ancho, alto))

        pygame.draw.rect(pantalla, color_borde, (x, y, ancho, alto), 5)

        texto_render = fuente.render(texto, True, (0, 0, 0))
        texto_rect = texto_render.get_rect(center=(x + ancho // 2, y + alto // 2))
        pantalla.blit(texto_render, texto_rect)

        return False

    
    def pedir_nombre():
        nombre = ""
        fuente_nombre = pygame.font.SysFont(None, 40)
        input_active = True
        input_rect = pygame.Rect(250, 300, 300, 50)
        color_input_box = pygame.Color('lightskyblue3')
        color_input_text = pygame.Color('black')

        while input_active:
            pantalla.fill((255, 255, 255))

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

            texto_nombre = fuente_nombre.render(f"Introduce tu nombre: {nombre}", True, color_input_text)
            pantalla.blit(texto_nombre, (input_rect.x + 10, input_rect.y + 10))
            pygame.draw.rect(pantalla, color_input_box, input_rect, 2)

            pygame.display.update()
            reloj.tick(60)

        return nombre

    def mostrar_instrucciones():
        fondo_instr = pygame.image.load("imgs/img9.jpg").convert()
        fondo_instr = pygame.transform.scale(fondo_instr, (ancho, largo))
        pantalla.blit(fondo_instr, (0, 0))

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
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        esperando = False

    while True:
        pantalla.blit(fondo, (0, 0))

        if boton(pantalla, "Jugar", 300, 250, 200, 60):
            nombre_jugador = pedir_nombre()
            print(f"Jugador: {nombre_jugador}")
            return nombre_jugador

        if boton(pantalla, "Instrucciones", 300, 340, 200, 60):
            mostrar_instrucciones()

        if boton(pantalla, "Salir", 300, 430, 200, 60):
            pygame.quit()
            sys.exit()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        reloj.tick(60)
