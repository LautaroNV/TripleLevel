import pygame
from recursos.colores import COLORES

def dibujar_traste(pantalla, alto_pantalla):
    for i, color in enumerate(COLORES):
        x = i * 100 + 60
        pygame.draw.rect(pantalla, color, (x, alto_pantalla - 40, 80, 20))
