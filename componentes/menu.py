import pygame

def mostrar_menu(pantalla, fuente):
    opciones = ["Elegir Nivel", "Instrucciones", "Salir"]
    pantalla.fill((0, 0, 0))
    for i, texto in enumerate(opciones):
        render = fuente.render(texto, True, (255, 255, 255))
        pantalla.blit(render, (100, 100 + i * 60))
    pygame.display.flip()

def mostrar_instrucciones(pantalla, fuente):
    pantalla.fill((0, 0, 0))
    instrucciones = [
        "Presiona las teclas correctas cuando las notas lleguen al traste.",
        "Notas HOLD requieren mantener la tecla presionada.",
        "Presiona ESC para volver al menú."
    ]
    for i, texto in enumerate(instrucciones):
        render = fuente.render(texto, True, (255, 255, 255))
        pantalla.blit(render, (50, 100 + i * 40))
    pygame.display.flip()
