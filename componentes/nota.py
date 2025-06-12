import pygame
from recursos.colores import COLORES

RADIO = 25

class Note:
    def __init__(self, tiempo_inicio, columna, duracion=0, ancho_total=800, columnas=5):
        self.inicio = tiempo_inicio  # en ms
        self.duracion = duracion  # en ms (solo >0 si es HOLD)
        self.column = columna
        self.ancho_total = ancho_total
        self.columnas = columnas

        col_width = self.ancho_total * 0.6 // self.columnas
        self.offset_x = (self.ancho_total - self.ancho_total * 0.6) // 2
        self.x = int(self.offset_x + col_width * columna + col_width // 2)

        self.y = -RADIO
        self.tocada = False
        self.en_hold = False
        self.finalizada = False

    def actualizar(self, velocidad):
        self.y += velocidad

    def en_zona(self, y_zona, altura_zona):
        margen = 25  # margen para que sea más fácil tocar
        return y_zona - altura_zona // 2 - margen <= self.y <= y_zona + altura_zona // 2 + margen

    def tocar(self):
        self.tocada = True
        if self.duracion > 0:
            self.en_hold = True

    def soltar(self):
        if self.en_hold:
            self.en_hold = False
            self.finalizada = True

    def fuera_de_pantalla(self, alto):
        if self.finalizada or (self.duracion == 0 and self.tocada):
            return True
        final_y = self.y + self.duracion * 0.01
        return final_y > alto

    def dibujar(self, pantalla):
        if self.finalizada:
            return

        color = COLORES[self.column]

        # HOLD (línea delgada + línea central blanca para estilo GH)
        if self.duracion > 0:
            alto_hold = self.duracion * 0.01
            y_final = int(self.y + alto_hold)

            # Línea gruesa de color de la nota
            pygame.draw.line(pantalla, color, (self.x, int(self.y)), (self.x, y_final), 10)

            # Línea blanca central para efecto visual (opcional)
            pygame.draw.line(pantalla, (255, 255, 255), (self.x, int(self.y)), (self.x, y_final), 2)

        # Cabeza de la nota
        if not self.tocada or self.duracion == 0:
            pygame.draw.circle(pantalla, color, (self.x, int(self.y)), RADIO)
            pygame.draw.circle(pantalla, (255, 255, 255), (self.x, int(self.y)), RADIO // 2, 2)