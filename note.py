# note.py
import pygame

NOTE_RADIUS = 20
COLUMN_WIDTH = 600 // 4 
HIT_ZONE_Y = 700
HIT_ZONE_HEIGHT = 60
HIT_ZONE_WIDTH = COLUMN_WIDTH

class Note:
    def __init__(self, column, time_ms, hold=False, hold_length=0):
        self.column = column
        self.time_ms = time_ms
        self.hold = hold
        self.hold_length = hold_length
        self.hit = False
        self.holding = False
        self.remove = False
        self.missed = False
        self.missed_time = 0
        self.x = column * COLUMN_WIDTH + COLUMN_WIDTH // 2
        self.y = -NOTE_RADIUS

    def move(self, speed):
        self.y += speed

    def draw(self, screen, color):
        if not self.remove:
            pygame.draw.circle(screen, color, (self.x, int(self.y)), NOTE_RADIUS)
            if self.hold:
                top = self.y - self.hold_length
                left = self.x - 5
                width = 10
                height = self.hold_length
                pygame.draw.rect(screen, color, (left, top, width, height))

    def is_in_hit_zone(self):
        rect_left = self.column * COLUMN_WIDTH
        rect_top = HIT_ZONE_Y - HIT_ZONE_HEIGHT // 2
        rect = pygame.Rect(rect_left, rect_top, HIT_ZONE_WIDTH, HIT_ZONE_HEIGHT)
        note_rect = pygame.Rect(self.x - NOTE_RADIUS, self.y - NOTE_RADIUS, NOTE_RADIUS * 2, NOTE_RADIUS * 2)
        return rect.colliderect(note_rect)

    def is_below_hit_zone(self):
        return self.y > HIT_ZONE_Y + HIT_ZONE_HEIGHT // 2 + self.hold_length

    def start_miss(self, current_time):
        self.missed = True
        self.missed_time = current_time
