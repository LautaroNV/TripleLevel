import pygame
from recursos.colores import COLORES

RADIO = 25
ANCHO_LINEA = 40  # igual al ancho visual de la nota

class HoldNote:
    def __init__(self, inicio, column, duracion, ancho_total=800, columnas=5):
        self.inicio = inicio
        self.column = column
        self.duracion = duracion  # en ms
        self.tocada = False
        self.en_hold = False
        self.finalizada = False

        # Posicionamiento igual que la clase Note
        self.ancho_total = ancho_total
        self.columnas = columnas
        self.ancho_traste = self.ancho_total * 0.6
        self.offset_x = (self.ancho_total - self.ancho_traste) // 2
        self.col_width = self.ancho_traste // self.columnas

        self.x = int(self.offset_x + self.col_width * column + self.col_width // 2)
        self.y = -RADIO

        self.color = COLORES[self.column]

    def actualizar(self, velocidad):
        self.y += velocidad

    def dibujar(self, pantalla):
        if self.finalizada:
            return

        alto_hold = self.duracion * 0.01
        y_final = int(self.y + alto_hold)

        # Dibujar la línea del hold (color sólido)
        pygame.draw.line(pantalla, self.color, (self.x, int(self.y)), (self.x, y_final), ANCHO_LINEA)

        # Cabeza de la nota (como una nota normal + círculo blanco completo)
        pygame.draw.circle(pantalla, self.color, (self.x, int(self.y)), RADIO)
        pygame.draw.circle(pantalla, (255, 255, 255), (self.x, int(self.y)), RADIO // 2)  # relleno blanco total

    def en_zona(self, y_zona, altura_zona):
        margen = 25
        return y_zona - altura_zona // 2 - margen <= self.y <= y_zona + altura_zona // 2 + margen

    def tocar(self):
        self.tocada = True
        self.en_hold = True

    def soltar(self):
        if self.en_hold:
            self.en_hold = False
            self.finalizada = True

    def fuera_de_pantalla(self, alto):
        final_y = self.y + self.duracion * 0.01
        return final_y > alto
