import pygame
from recursos.colores import COLORES


class TrasteGuitarra:
    def __init__(self, ancho, alto, columnas):
        self.ancho_total = ancho
        self.alto = alto
        self.columnas = columnas
        self.ancho_traste = int(ancho * 0.6)  # Achicar traste al 60% del ancho de pantalla
        self.offset_x = (ancho - self.ancho_traste) // 2  # Centrado horizontal
        self.y_zona = alto - 80
        self.altura_zona = 50

    def dibujar(self, pantalla, presionadas):
        col_width = self.ancho_traste // self.columnas

        for i in range(self.columnas):
            x = self.offset_x + i * col_width + col_width // 2
            color = COLORES[i]

            # Línea vertical de columna
            pygame.draw.line(pantalla, (80, 80, 80), (x, 0), (x, self.alto), 3)

            # Botón de impacto
            pygame.draw.circle(pantalla, color, (x, self.y_zona), 20)
            if presionadas[i]:
                pygame.draw.circle(pantalla, (255, 255, 255), (x, self.y_zona), 26, 2)

        # Zona de impacto
        pygame.draw.rect(pantalla, (60, 60, 60),
                         (self.offset_x, self.y_zona - self.altura_zona // 2,
                          self.ancho_traste, self.altura_zona), 2)