import pygame
from recursos.colores import COLORES

RADIO = 25
ANCHO_LINEA = 12
COLOR_GRIS = (150, 150, 150)

class HoldNote:
    def __init__(self, inicio, column, duracion, ancho_total=800, columnas=5):
        self.inicio = inicio
        self.column = column
        self.duracion = duracion
        self.tocada = False
        self.en_hold = False
        self.soltada = False
        self.completada = False

        self.ancho_total = ancho_total
        self.columnas = columnas
        self.ancho_traste = self.ancho_total * 0.6
        self.offset_x = (self.ancho_total - self.ancho_traste) // 2
        self.col_width = self.ancho_traste // self.columnas

        self.x = int(self.offset_x + self.col_width * column + self.col_width // 2)
        self.y = -RADIO
        self.y_fijada = None

        self.color = COLORES[self.column]

    def actualizar(self, velocidad, tiempo_actual):
        if self.completada:
            return

        if not self.y_fijada:
            self.y += velocidad

        tiempo_final = self.inicio + self.duracion
        if self.en_hold and tiempo_actual >= tiempo_final:
            self.completada = True

    def dibujar(self, pantalla):
        if self.completada:
            return

        self.dibujar_hold_linea(pantalla)
        self.dibujar_cabeza(pantalla)

    def dibujar_hold_linea(self, pantalla):
        alto_hold = self.duracion * 0.01
        y_base = self.y_fijada if self.y_fijada is not None else self.y
        y_final = int(y_base - alto_hold)

        color_dibujo = COLOR_GRIS if self.soltada else (self.color if not self.en_hold else self.brillo(self.color))

        pygame.draw.line(pantalla, color_dibujo, (self.x, int(y_base)), (self.x, y_final), ANCHO_LINEA)
        pygame.draw.line(pantalla, (255, 255, 255), (self.x, int(y_base)), (self.x, y_final), 2)

        pygame.draw.circle(pantalla, color_dibujo, (self.x, y_final), RADIO // 2)
        pygame.draw.circle(pantalla, (255, 255, 255), (self.x, y_final), RADIO // 4)

    def dibujar_cabeza(self, pantalla):
        y_draw = self.y_fijada if self.y_fijada is not None else self.y
        color_dibujo = COLOR_GRIS if self.soltada else self.color

        pygame.draw.circle(pantalla, color_dibujo, (self.x, int(y_draw)), RADIO)
        pygame.draw.circle(pantalla, (255, 255, 255), (self.x, int(y_draw)), RADIO // 2)

    def en_zona(self, y_zona, altura_zona):
        margen = 35
        return y_zona - altura_zona // 2 - margen <= self.y <= y_zona + altura_zona // 2 + margen

    def tocar(self, y_zona):
        self.tocada = True
        self.en_hold = True
        self.y_fijada = y_zona

    def soltar(self, tiempo_actual):
        self.en_hold = False
        self.soltada = True

    def fuera_de_pantalla(self, alto):
        y_base = self.y_fijada if self.y_fijada is not None else self.y
        final_y = y_base - self.duracion * 0.01
        return final_y > alto

    def brillo(self, color):
        return (
            min(color[0] + 60, 255),
            min(color[1] + 60, 255),
            min(color[2] + 60, 255)
        )
