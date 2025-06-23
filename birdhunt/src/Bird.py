import pygame
import random
import os

class Bird:
    def __init__(self):
        self.frames = []
        self.cargar_animacion()
        self.frame_actual = 0
        self.contador_animacion = 0
        self.velocidad = random.randint(2, 5)
        self.rect = self.frames[0].get_rect()
        self.reset_pos()

    def cargar_animacion(self):
        for i in range(7):
            ruta = os.path.join("birdhunt", "Imgs", f"pajaro{i}.png")
            imagen = pygame.image.load(ruta).convert_alpha()
            imagen = pygame.transform.scale(imagen, (45, 45))
            self.frames.append(imagen)

    def reset_pos(self):
        self.rect.x = -random.randint(60, 300)
        self.rect.y = random.randint(50, 400)

    def mover(self):
        self.rect.x += self.velocidad
        if self.rect.x > 800:
            self.reset_pos()

        self.contador_animacion += 1
        if self.contador_animacion >= 5:
            self.frame_actual = (self.frame_actual + 1) % len(self.frames)
            self.contador_animacion = 0

    def dibujar(self, pantalla):
        pantalla.blit(self.frames[self.frame_actual], self.rect)
