import pygame
import sys

pygame.init()

ANCHO = 900
ALTO = 900
NEGRO = (0, 0, 0)

fondo = pygame.image.load("imgs/background.png")

# Cargar fuente Hyperwave-One.ttf 
fuente = pygame.font.Font("recursos/fuentes/Hyperwave-One.ttf", 70)

opciones = ["ELEGIR NIVEL", "INSTRUCCIONES", "SALIR"]
opciones_rects = []

espaciado = 60
inicio_y = 360

def menu_principal(pantalla):
    seleccion = -1
    ejecutando = True

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(opciones_rects):
                    if rect.collidepoint(evento.pos):
                        seleccion = i
                        ejecutando = False

        pantalla.blit(pygame.transform.scale(fondo, (ANCHO, ALTO)), (0, 0))

        opciones_rects.clear()
        for i, texto in enumerate(opciones):
            render = fuente.render(texto, True, NEGRO)
            rect = render.get_rect(center=(ANCHO // 2, inicio_y + i * espaciado))
            pantalla.blit(render, rect)
            opciones_rects.append(rect)

        pygame.display.flip()

    if seleccion == 0:
        return "jugar"
    elif seleccion == 1:
        return "instrucciones"
    else:
        pygame.quit()
        sys.exit()

def mostrar_instrucciones(pantalla):
    ejecutando = True
    fuente_inst = pygame.font.Font("recursos/fuentes/Hyperwave-One.ttf", 40)
    instrucciones = [
        "Instrucciones del juego:",
        "- Presiona las teclas A, S, D, F, G para tocar las notas.",
        "- Mantén las notas largas pulsadas.",
        "- No falles demasiadas notas o perderás.",
        "Haz clic para volver al menú."
    ]

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                ejecutando = False

        pantalla.blit(pygame.transform.scale(fondo, (ANCHO, ALTO)), (0, 0))
        
        for i, linea in enumerate(instrucciones):
            texto_render = fuente_inst.render(linea, True, NEGRO)
            rect = texto_render.get_rect(center=(ANCHO // 2, 200 + i * 40))
            pantalla.blit(texto_render, rect)

        pygame.display.flip()

    return "menu"

if __name__ == "__main__":
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    seleccion = menu_principal(pantalla)
    print(f"Opción seleccionada: {seleccion}")
