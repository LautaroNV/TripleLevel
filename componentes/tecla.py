import pygame

class Tecla:
    def __init__(self, letra, x, y):
        self.letra = letra.upper()
        self.x = x
        self.y = y
        self.imagen_normal = None
        self.imagen_presionada = None
        self.presionada = False

    def cargar_imagenes(self):
        self.imagen_normal = pygame.image.load(f"imgs/{self.letra}.png")
        self.imagen_presionada = pygame.image.load(f"imgs/{self.letra}2.png")

    def actualizar(self, presionada):
        self.presionada = presionada

    def dibujar(self, pantalla):
        imagen = self.imagen_presionada if self.presionada else self.imagen_normal
        pantalla.blit(imagen, (self.x, self.y))
