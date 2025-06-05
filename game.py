
import pygame
import sys
from note import Note
from songs import cancion1

# Configuración de pantalla
WIDTH, HEIGHT = 600, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Note Rush")
FONT = pygame.font.SysFont("Arial", 30)

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 150, 255)
YELLOW = (255, 255, 0)

# Configuración de juego
FPS = 60
NOTE_SPEED = 5
COLUMN_KEYS = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f]
COLUMNS = 4
COLUMN_WIDTH = WIDTH // COLUMNS
HIT_ZONE_Y = HEIGHT - 100
HIT_ZONE_HEIGHT = 60
HIT_ZONE_WIDTH = COLUMN_WIDTH
NOTE_RADIUS = 20
LEVEL_DURATION = 30000  #(30 segundos)
MISS_SHOW_TIME = 600  # ms para mostrar rojo cuando se falla el hold

clock = pygame.time.Clock()

def draw_hit_zones(held_keys):
    for i in range(COLUMNS):
        rect = pygame.Rect(i * COLUMN_WIDTH, HIT_ZONE_Y - HIT_ZONE_HEIGHT // 2, HIT_ZONE_WIDTH, HIT_ZONE_HEIGHT)
        pygame.draw.rect(SCREEN, GRAY, rect, 3)
        x = i * COLUMN_WIDTH + COLUMN_WIDTH // 2
        y = HIT_ZONE_Y
        key = COLUMN_KEYS[i]
        color = YELLOW if held_keys[key] else WHITE
        pygame.draw.circle(SCREEN, color, (x, y), NOTE_RADIUS // 2, 3)

def draw_text(text, size, color, x, y, center=True):
    font = pygame.font.SysFont("Arial", size)
    rendered = font.render(text, True, color)
    rect = rendered.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    SCREEN.blit(rendered, rect)

def game_loop():
    notes = cancion1.notes.copy()
    score = 0
    combo = 0
    max_combo = 0
    held_keys = {key: False for key in COLUMN_KEYS}

    start_time = pygame.time.get_ticks()
    running = True
    while running:
        clock.tick(FPS)
        SCREEN.fill(BLACK)
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time

        if elapsed_time >= LEVEL_DURATION:
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in COLUMN_KEYS:
                    col = COLUMN_KEYS.index(event.key)
                    held_keys[event.key] = True
                    for note in notes:
                        if note.column == col and note.is_in_hit_zone() and not note.hit:
                            score += 10 + int(combo) * 2
                            combo += 1
                            note.hit = True
                            if note.hold:
                                note.holding = True
                            else:
                                note.remove = True
                                notes.remove(note)
                            break
                    else:
                        combo = 0

            if event.type == pygame.KEYUP:
                if event.key in COLUMN_KEYS:
                    col = COLUMN_KEYS.index(event.key)
                    held_keys[event.key] = False
                    for note in notes[:]:
                        if note.column == col and note.hold and note.holding:
                            note.holding = False
                            if note.y < HIT_ZONE_Y:
                                note.start_miss(current_time)
                            else:
                                note.remove = True
                                notes.remove(note)
                            break

        for note in notes[:]:
            note.move(NOTE_SPEED)
            color = BLUE if note.hold else WHITE
            if note.hold:
                if note.holding and not note.missed:
                    color = GREEN
                    score += 1
                    combo += 0.01
                elif note.missed:
                    color = RED
                    if current_time - note.missed_time > MISS_SHOW_TIME:
                        note.remove = True
                        notes.remove(note)
            note.draw(SCREEN, color)

            if note.is_below_hit_zone():
                if not note.hit:
                    combo = 0
                if note.hold and note.holding:
                    note.holding = False
                    note.remove = True
                    notes.remove(note)
                elif not note.remove:
                    notes.remove(note)

        max_combo = max(max_combo, int(combo))

        draw_hit_zones(held_keys)
        draw_text(f"Puntaje: {int(score)}", 28, GREEN, 20, 20, center=False)
        draw_text(f"Combo: {int(combo)}", 28, BLUE, 20, 60, center=False)
        draw_text(f"Tiempo: {max(0, (LEVEL_DURATION - elapsed_time) // 1000)}s", 28, RED, WIDTH - 160, 20, center=False)

        pygame.display.flip()
