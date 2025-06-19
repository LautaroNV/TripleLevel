import pygame
from recursos.colores import COLORES

class TrasteGuitarra:
    def __init__(self, ancho, alto, columnas):
        self.ancho_total = ancho
        self.alto = alto
        self.columnas = columnas
        self.ancho_traste = int(ancho * 0.6)
        self.offset_x = (ancho - self.ancho_traste) // 2
        self.y_zona = alto - 80

        # ⚠️ Zona de impacto más generosa
        self.altura_zona = 80  # Antes 50 → ahora más tolerante

        # Cargar y escalar imagen del traste
        imagen_original = pygame.image.load("imgs/traste.png").convert()
        self.imagen = pygame.transform.scale(imagen_original, (self.ancho_traste, imagen_original.get_height()))
        self.scroll_y = 0

    def dibujar(self, pantalla, presionadas):
        self.scroll_y += 8
        if self.scroll_y >= self.imagen.get_height():
            self.scroll_y = 0

        pantalla.blit(self.imagen, (self.offset_x, self.scroll_y - self.imagen.get_height()))
        pantalla.blit(self.imagen, (self.offset_x, self.scroll_y))

        pygame.draw.rect(pantalla, (60, 60, 60),
                         (self.offset_x, self.scroll_y - 2, self.ancho_traste, 4))

        col_width = self.ancho_traste // self.columnas
        for i in range(self.columnas):
            x = self.offset_x + i * col_width + col_width // 2
            color = COLORES[i]

            pygame.draw.line(pantalla, (80, 80, 80), (x, 0), (x, self.alto), 3)
            pygame.draw.circle(pantalla, color, (x, self.y_zona), 25)
            if presionadas[i]:
                pygame.draw.circle(pantalla, (255, 255, 255), (x, self.y_zona), 26, 2)

        pygame.draw.rect(pantalla, (60, 60, 60),
                         (self.offset_x, self.y_zona - self.altura_zona // 2,
                          self.ancho_traste, self.altura_zona), 2)
