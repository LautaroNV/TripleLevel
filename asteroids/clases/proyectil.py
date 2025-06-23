import pygame

class Proyectil:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.timer = 60

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.timer -= 1

    def draw(self, win):
        pygame.draw.circle(win, (255, 255, 255), (int(self.x), int(self.y)), 3)

    def is_alive(self):
        return (0 <= self.x <= 800 and 0 <= self.y <= 600) and self.timer > 0

    def get_rect(self):
        return pygame.Rect(self.x - 2, self.y - 2, 4, 4)