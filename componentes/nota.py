import pygame
from recursos.colores import RUTAS_IMAGENES

ANCHO_NOTA = 80
ALTO_NOTA = 40
VELOCIDAD = 2.8

class Nota:
    def __init__(self, tiempo, columna, tipo='tap', duracion=0):
        self.tiempo = tiempo
        self.columna = columna
        self.tipo = tipo
        self.duracion = duracion
        self.y = -ALTO_NOTA
        self.imagen = pygame.image.load(RUTAS_IMAGENES[columna]).convert_alpha()
        self.imagen = pygame.transform.scale(self.imagen, (ANCHO_NOTA, ALTO_NOTA))

    def actualizar(self):
        self.y += VELOCIDAD

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.columna * 100 + 60, self.y))
        if self.tipo == 'hold':
            pygame.draw.rect(
                pantalla,
                (255, 255, 255),
                (self.columna * 100 + 90, self.y + ALTO_NOTA, 10, self.duracion * VELOCIDAD),
                border_radius=3
            )
