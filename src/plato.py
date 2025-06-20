import pygame

<<<<<<< HEAD
class Plato:
    def __init__(self, x, y, ancho, largo):
=======
class Plato(pygame.sprite.Sprite):
    def __init__(self, x, y, ancho, largo):
        super().__init__()
>>>>>>> main
        self.x = x
        self.y = y
        self.ancho = ancho
        self.largo = largo
<<<<<<< HEAD
        self.imagen_normal = pygame.image.load("imgs/img4.png").convert_alpha()
        self.imagen_rota = pygame.image.load("imgs/img4(roto).png").convert_alpha()
=======

        self.imagen_normal = pygame.image.load("imgs/plato1.png").convert_alpha()
        self.imagen_rota = pygame.image.load("imgs/plato2.png").convert_alpha()
>>>>>>> main

        self.imagen_normal = pygame.transform.scale(self.imagen_normal, (60, 60))
        self.imagen_rota = pygame.transform.scale(self.imagen_rota, (60, 60))

<<<<<<< HEAD
        self.rect = self.imagen_normal.get_rect()
=======
        self.image = self.imagen_normal
        self.rect = self.image.get_rect()
>>>>>>> main
        self.rect.topleft = (self.x, self.y)

        self.destruido = False
        self.tiempo_destruido = 0
        self.tiempo_mostrar_roto = 300 

    def mover(self):
        if not self.destruido:
            self.y -= 3
            if self.y < 0:
                self.y = self.largo
            self.rect.topleft = (self.x, self.y)

    def dibujar(self, pantalla):
<<<<<<< HEAD
        if self.destruido:
            pantalla.blit(self.imagen_rota, self.rect)
        else:
            pantalla.blit(self.imagen_normal, self.rect)
=======
        pantalla.blit(self.image, self.rect)
>>>>>>> main

    def colision(self, mx, my):
        if self.rect.collidepoint(mx, my) and not self.destruido:
            self.destruido = True
            self.tiempo_destruido = pygame.time.get_ticks()
<<<<<<< HEAD
            return True
        return False

    def reset(self):
        self.y = self.largo
        self.rect.topleft = (self.x, self.y)
        self.destruido = False
        self.tiempo_destruido = 0

=======
            self.image = self.imagen_rota
            return True
        return False

>>>>>>> main
    def actualizar_estado(self):
        if self.destruido:
            ahora = pygame.time.get_ticks()
            if ahora - self.tiempo_destruido > self.tiempo_mostrar_roto:
                self.reset()
<<<<<<< HEAD
    
=======

    def reset(self):
        self.y = self.largo
        self.rect.topleft = (self.x, self.y)
        self.image = self.imagen_normal
        self.destruido = False
        self.tiempo_destruido = 0
>>>>>>> main
