import pygame
import random

class Asteroide:
    def __init__(self, x=None, y=None, size=None, frames=None):
        self.size = size or random.choice([50, 70, 90])
        self.x = x or random.randint(0, 800)
        self.y = y or random.randint(0, 600)
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.frames = frames or []
        self.current_frame = 0
        self.frame_delay = 5
        self.frame_counter = 0
        self.scaled_frames = [pygame.transform.scale(f, (self.size, self.size)) for f in self.frames] if self.frames else []

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.x %= 800
        self.y %= 600
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.scaled_frames)

    def draw(self, win):
        if self.scaled_frames:
            frame = self.scaled_frames[self.current_frame]
            win.blit(frame, (int(self.x - self.size // 2), int(self.y - self.size // 2)))

    def get_rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)

    def get_puntos(self):
        if self.size >= 60:
            return 20
        elif self.size >= 40:
            return 50
        else:
            return 100

    def dividir(self, frames=None):
        if self.size > 20:
            new_size = self.size // 2
            return [
                Asteroide(self.x, self.y, new_size, frames or self.frames),
                Asteroide(self.x, self.y, new_size, frames or self.frames)                
                ]
        else:
            return []