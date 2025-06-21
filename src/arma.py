import pygame

class Arma(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        escala = 0.3  # Ajustá según el tamaño deseado

        # Cargar y escalar los frames
        self.frames = []
        for i in range(5):
            img = pygame.image.load(f"Imgs/arma{i}.png").convert_alpha()
            ancho = int(img.get_width() * escala)
            alto = int(img.get_height() * escala)
            img = pygame.transform.scale(img, (ancho, alto))
            self.frames.append(img)

        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(midbottom=pos)

        self.animando = False
        self.tiempo_animacion = 50  # ms entre frames
        self.ultimo_update = pygame.time.get_ticks()

    def disparar(self):
        self.animando = True
        self.index = 0
        self.ultimo_update = pygame.time.get_ticks()

    def update(self):
        if self.animando:
            ahora = pygame.time.get_ticks()
            if ahora - self.ultimo_update > self.tiempo_animacion:
                self.index += 1
                if self.index >= len(self.frames):
                    self.index = 0
                    self.animando = False
                self.image = self.frames[self.index]
                self.rect = self.image.get_rect(midbottom=self.rect.midbottom)  # mantener posición
                self.ultimo_update = ahora
