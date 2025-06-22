import pygame
import math
from .proyectil import Proyectil

class Nave:
    def __init__(self):
        self.original_image = pygame.image.load("img/nave.png").convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(800 // 2, 600 // 2))
        self.angle = 0
        self.velocidad = 0
        self.max_velocidad = 3.5
        self.aceleracion = 0.1
        self.frenado = 0.1
        self.vidas = 3
        self.vx = 0
        self.vy = 0

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.angle -= 5  
        if keys[pygame.K_RIGHT]:
            self.angle += 5
        if keys[pygame.K_UP]:
            rad = math.radians(self.angle)
            self.vx += self.aceleracion * math.sin(rad)
            self.vy -= self.aceleracion * math.cos(rad)


        if keys[pygame.K_DOWN]:
            self.vx *= (1 - self.frenado)
            self.vy *= (1 - self.frenado)

        velocidad_total = math.hypot(self.vx, self.vy)
        if velocidad_total > self.max_velocidad:
            escala = self.max_velocidad / velocidad_total
            self.vx *= escala
            self.vy *= escala

        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 600:
            self.rect.bottom = 600

        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def disparar(self):
        angle_rad = math.radians(self.angle)
        dx = math.sin(angle_rad)
        dy = -math.cos(angle_rad)
        offset = 40
        front_x = self.rect.centerx + dx * offset
        front_y = self.rect.centery + dy * offset
        return Proyectil(front_x, front_y, dx * 10, dy * 10)

    def draw(self, win):
        win.blit(self.image, self.rect)

    def reiniciar_posicion(self):
        self.rect.center = (800 // 2, 600 // 2)
        self.vx = self.vy = 0
        self.angle = 0