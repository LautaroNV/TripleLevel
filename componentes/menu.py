import pygame
import sys

pygame.init()

ANCHO = 900
ALTO = 900
NEGRO = (0, 0, 0)

# Fondos
fondo = pygame.image.load("imgs/background.png")
fondo_instrucciones = pygame.image.load("imgs/background2.png")
fondo_instrucciones = pygame.transform.scale(fondo_instrucciones, (ANCHO, ALTO))

# Fuentes
fuente = pygame.font.Font("recursos/fuentes/Hyperwave-One.ttf", 70)
fuente_inst = pygame.font.Font("recursos/fuentes/Hyperwave-One.ttf", 36)

# Opciones del menú
opciones = ["ELEGIR NIVEL", "INSTRUCCIONES", "SALIR"]
opciones_rects = []

espaciado = 120
inicio_y = 360

# Teclas animadas (A1.png/A2.png, etc.)
teclas = {
    "A": [pygame.image.load("imgs/A1.png"), pygame.image.load("imgs/A2.png")],
    "S": [pygame.image.load("imgs/S1.png"), pygame.image.load("imgs/S2.png")],
    "J": [pygame.image.load("imgs/J1.png"), pygame.image.load("imgs/J2.png")],
    "K": [pygame.image.load("imgs/K1.png"), pygame.image.load("imgs/K2.png")],
    "L": [pygame.image.load("imgs/L1.png"), pygame.image.load("imgs/L2.png")]
}

# Escalar teclas
for k in teclas:
    teclas[k][0] = pygame.transform.scale(teclas[k][0], (64, 64))
    teclas[k][1] = pygame.transform.scale(teclas[k][1], (64, 64))

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
    reloj = pygame.time.Clock()
    ejecutando = True

    instrucciones = [
        "Presiona las teclas para tocar las notas.",
        "Mantén las notas largas pulsadas.",
        "No falles demasiadas notas o perderás."
    ]

    # Animación de teclas
    frame_actual = 0
    frame_rate = 20
    teclas_orden = ["A", "S", "J", "K", "L"]
    x_base = ANCHO // 2 - (5 * 64 + 4 * 10) // 2
    y_teclas = 450  # MÁS ARRIBA: DENTRO del papel blanco

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                ejecutando = False

        pantalla.blit(fondo_instrucciones, (0, 0))

        # Dibujar instrucciones DENTRO del papel blanco
        y_inicio = 280
        for i, linea in enumerate(instrucciones):
            render = fuente_inst.render(linea, True, NEGRO)
            rect = render.get_rect(center=(ANCHO // 2, y_inicio + i * 40))
            pantalla.blit(render, rect)

        # Animación teclas (bucle)
        frame_actual = (frame_actual + 1) % (frame_rate * 2)
        imagen_index = 0 if frame_actual < frame_rate else 1

        for i, tecla in enumerate(teclas_orden):
            imagen = teclas[tecla][imagen_index]
            pantalla.blit(imagen, (x_base + i * (64 + 10), y_teclas))

        pygame.display.flip()
        reloj.tick(60)

    return "menu"

if __name__ == "__main__":
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    seleccion = menu_principal(pantalla)
    print(f"Opción seleccionada: {seleccion}")
