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
        self.altura_zona = 80

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
            y = self.y_zona
            color = COLORES[i]
            presionada = presionadas[i]

            # Tamaño dinámico según si está presionado
            radio_base = 28
            incremento = 4 if presionada else 0
            radio_exterior = radio_base + incremento
            radio_medio = radio_base - 4 + incremento
            radio_interior = radio_base - 8 + incremento

            # Capa exterior negra (contorno fuerte)
            pygame.draw.circle(pantalla, (0, 0, 0), (x, y), radio_exterior)

            # Capa intermedia del color de la nota (borde brillante)
            color_borde = tuple(min(255, c + 80) if presionada else c for c in color)
            pygame.draw.circle(pantalla, color_borde, (x, y), radio_medio)

            # Centro del botón con el color original
            pygame.draw.circle(pantalla, color, (x, y), radio_interior)

            # Detalle blanco chico
            pygame.draw.circle(pantalla, (230, 230, 230), (x, y), 6)

        # Zona rectangular general
        pygame.draw.rect(pantalla, (60, 60, 60),
                         (self.offset_x, self.y_zona - self.altura_zona // 2,
                          self.ancho_traste, self.altura_zona), 2)
