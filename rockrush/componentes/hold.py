import pygame
from recursos.colores import COLORES

RADIO = 25
ANCHO_LINEA = 12
COLOR_GRIS = (150, 150, 150)

class HoldNote:
    def __init__(self, inicio, column, duracion, ancho_total=800, columnas=5):
        # Tiempo de inicio de la nota, columna, duración (en ms)
        self.inicio = inicio
        self.column = column
        self.duracion = duracion
        self.tocada = False      # Si la nota fue tocada
        self.en_hold = False     # Si se está manteniendo presionada
        self.soltada = False     # Si se soltó antes de tiempo
        self.completada = False  # Si se completó correctamente

        # Cálculo de posición horizontal según columna y ancho de trastes
        self.ancho_total = ancho_total
        self.columnas = columnas
        self.ancho_traste = self.ancho_total * 0.6
        self.offset_x = (self.ancho_total - self.ancho_traste) // 2
        self.col_width = self.ancho_traste // self.columnas

        self.x = int(self.offset_x + self.col_width * column + self.col_width // 2)
        self.y = -RADIO  # Empieza fuera de pantalla arriba
        self.y_fijada = None     # Y donde se tocó la nota

        self.color = COLORES[self.column % len(COLORES)]
        self.tiempo_tocado = None
        self.tiempo_actual = 0

        self.factor_pixeles = 1  # Escala para la longitud visual de la nota

    def actualizar(self, velocidad, tiempo_actual):
        """Actualiza la posición y estado de la nota."""
        self.tiempo_actual = tiempo_actual

        if self.completada:
            return

        # Si no fue tocada, sigue bajando
        if not self.y_fijada:
            self.y += velocidad

        # Si está siendo mantenida, verifica si se completó el hold
        if self.en_hold:
            tiempo_pasado = tiempo_actual - self.tiempo_tocado
            if tiempo_pasado >= self.duracion:
                self.completada = True

    def dibujar(self, pantalla):
        """Dibuja la nota hold en pantalla."""
        if self.completada:
            return

        if self.tocada:
            self.dibujar_hold_linea(pantalla)
        else:
            self.dibujar_hold_linea(pantalla)
            self.dibujar_cabeza(pantalla)

    def dibujar_hold_linea(self, pantalla):
        """Dibuja la línea vertical de la nota hold."""
        if self.soltada:
            return

        # Si está siendo tocada, la línea se va acortando según el tiempo restante
        if self.tocada:
            tiempo_pasado = self.tiempo_actual - self.tiempo_tocado
            porcentaje = max(0, 1 - tiempo_pasado / self.duracion)
            alto_hold = max(5, self.duracion * self.factor_pixeles * porcentaje)
        else:
            alto_hold = self.duracion * self.factor_pixeles

        y_base = self.y_fijada if self.y_fijada is not None else self.y
        y_final = int(y_base - alto_hold)

        # Si está en hold, la línea brilla más
        if self.en_hold:
            color_dibujo = self.brillo(self.color)
        else:
            color_dibujo = self.color

        # Línea principal
        pygame.draw.line(pantalla, color_dibujo, (self.x, int(y_base)), (self.x, y_final), ANCHO_LINEA)
        # Línea blanca central
        pygame.draw.line(pantalla, (255, 255, 255), (self.x, int(y_base)), (self.x, y_final), 2)

        # Si no fue tocada, dibuja la "cabeza" de la nota al final de la línea
        if not self.tocada:
            pygame.draw.circle(pantalla, (0, 0, 0), (self.x, y_final), RADIO // 2 + 2)
            pygame.draw.circle(pantalla, color_dibujo, (self.x, y_final), RADIO // 2)
            pygame.draw.circle(pantalla, (0, 0, 0), (self.x, y_final), RADIO // 4 + 2)
            pygame.draw.circle(pantalla, (255, 255, 255), (self.x, y_final), RADIO // 4)

    def dibujar_cabeza(self, pantalla):
        """Dibuja la cabeza de la nota (círculo grande)."""
        if self.tocada:
            return

        y_draw = self.y_fijada if self.y_fijada is not None else self.y
        color_dibujo = COLOR_GRIS if self.soltada else self.color

        pygame.draw.circle(pantalla, (0, 0, 0), (self.x, int(y_draw)), RADIO + 2)
        pygame.draw.circle(pantalla, color_dibujo, (self.x, int(y_draw)), RADIO)
        pygame.draw.circle(pantalla, (0, 0, 0), (self.x, int(y_draw)), RADIO // 2 + 2)
        pygame.draw.circle(pantalla, (255, 255, 255), (self.x, int(y_draw)), RADIO // 2)

    def en_zona(self, y_zona, altura_zona):
        """Devuelve True si la cabeza de la nota está en la zona de activación."""
        margen = 35
        return y_zona - altura_zona // 2 - margen <= self.y <= y_zona + altura_zona // 2 + margen

    def tocar(self, y_zona):
        """Marca la nota como tocada y comienza el hold."""
        self.tocada = True
        self.en_hold = True
        self.y_fijada = y_zona
        self.tiempo_tocado = pygame.time.get_ticks()

    def soltar(self, tiempo_actual):
        """Llama cuando el jugador suelta la tecla. Marca como completada si corresponde."""
        if self.tocada:
            tiempo_pasado = tiempo_actual - self.tiempo_tocado
            if tiempo_pasado >= self.duracion:
                self.completada = True
            else:
                self.en_hold = False
                self.soltada = True

    def fuera_de_pantalla(self, alto):
        """Devuelve True si la nota ya salió de la pantalla por abajo."""
        y_base = self.y_fijada if self.y_fijada is not None else self.y
        final_y = y_base - self.duracion * self.factor_pixeles
        return final_y > alto

    def brillo(self, color):
        """Devuelve una versión más brillante del color dado."""
        return (
            min(color[0] + 60, 255),
            min(color[1] + 60, 255),
            min(color[2] + 60, 255)
        )
