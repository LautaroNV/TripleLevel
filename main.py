import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

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
HIT_ZONE_HEIGHT = 60  # Zona de impacto más alta
HIT_ZONE_WIDTH = COLUMN_WIDTH  # Zona de impacto igual al ancho de columna
NOTE_RADIUS = 20
LEVEL_DURATION = 30_000  # milisegundos (30 segundos)
MISS_SHOW_TIME = 600  # ms para mostrar rojo cuando se falla el hold

# Estados del juego
MENU, GAME, INSTRUCTIONS = "menu", "game", "instructions"
game_state = MENU

clock = pygame.time.Clock()


class Note:
    def __init__(self, column, hold=False):
        self.column = column
        self.x = column * COLUMN_WIDTH + COLUMN_WIDTH // 2
        self.y = -NOTE_RADIUS
        self.hold = hold
        self.hold_length = 100 if hold else 0
        self.hit = False
        self.holding = False
        self.remove = False
        self.missed = False  # Para mostrar rojo en fallo hold
        self.missed_time = 0

    def move(self):
        self.y += NOTE_SPEED

    def draw(self):
        # Color base
        color = BLUE if self.hold else WHITE

        # Cambia color si hold activo (verde) o fallido (rojo)
        if self.hold:
            if self.holding and not self.missed:
                color = GREEN
            elif self.missed:
                color = RED

        # Dibujo del círculo (nota)
        if not self.remove:
            pygame.draw.circle(SCREEN, color, (self.x, int(self.y)), NOTE_RADIUS)

        # Dibujo de la barra hold encima del círculo (desde círculo hacia arriba)
        if self.hold:
            top = self.y - self.hold_length
            left = self.x - 5
            width = 10
            height = self.hold_length
            pygame.draw.rect(SCREEN, color, (left, top, width, height))

    def is_in_hit_zone(self):
        rect_left = self.column * COLUMN_WIDTH
        rect_top = HIT_ZONE_Y - HIT_ZONE_HEIGHT // 2
        rect = pygame.Rect(rect_left, rect_top, HIT_ZONE_WIDTH, HIT_ZONE_HEIGHT)
        note_rect = pygame.Rect(self.x - NOTE_RADIUS, self.y - NOTE_RADIUS, NOTE_RADIUS * 2, NOTE_RADIUS * 2)
        return rect.colliderect(note_rect)

    def is_below_hit_zone(self):
        return self.y > HIT_ZONE_Y + HIT_ZONE_HEIGHT // 2 + self.hold_length

    def start_miss(self):
        self.missed = True
        self.missed_time = pygame.time.get_ticks()


def draw_hit_zones(held_keys):
    for i in range(COLUMNS):
        rect = pygame.Rect(i * COLUMN_WIDTH, HIT_ZONE_Y - HIT_ZONE_HEIGHT // 2, HIT_ZONE_WIDTH, HIT_ZONE_HEIGHT)
        pygame.draw.rect(SCREEN, GRAY, rect, 3)
        # Dibujo círculo referencia dentro del área para tocar
        x = i * COLUMN_WIDTH + COLUMN_WIDTH // 2
        y = HIT_ZONE_Y
        # Cambia color si tecla está presionada
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
    global game_state

    notes = []
    score = 0
    combo = 0
    max_combo = 0
    held_keys = {key: False for key in COLUMN_KEYS}

    start_time = pygame.time.get_ticks()
    last_spawn = 0
    spawn_interval = 800  # ms

    running = True
    while running:
        clock.tick(FPS)
        SCREEN.fill(BLACK)
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time

        if elapsed_time >= LEVEL_DURATION:
            game_state = MENU
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
                            score += 10 + combo * 2
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
                            # Si soltó antes de tiempo, falla hold
                            note.holding = False
                            if note.y < HIT_ZONE_Y:  # No llegó al final aún
                                note.start_miss()
                            else:
                                # Si llegó al final, es correcto
                                note.remove = True
                                notes.remove(note)
                            break

        # Spawn de notas
        if current_time - last_spawn > spawn_interval:
            column = random.randint(0, COLUMNS - 1)
            hold = random.random() < 0.3
            notes.append(Note(column, hold))
            last_spawn = current_time

        # Mover y dibujar notas
        for note in notes[:]:
            note.move()
            note.draw()

            if note.hold:
                if note.holding and not note.missed:
                    score += 1  # puntos por hold activo
                    combo += 0.01
                if note.missed:
                    # Mostrar rojo unos milisegundos antes de eliminar
                    if current_time - note.missed_time > MISS_SHOW_TIME:
                        note.remove = True
                        notes.remove(note)

            if note.is_below_hit_zone():
                if not note.hit:
                    combo = 0
                # Si es hold y está siendo sostenido pero ya pasó la zona, marcar como final correcto
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


def show_instructions():
    global game_state
    waiting = True
    while waiting:
        SCREEN.fill(BLACK)
        draw_text("Instrucciones", 50, WHITE, WIDTH // 2, 100)
        draw_text("Presiona A, S, D, F cuando las notas lleguen a la zona", 26, WHITE, WIDTH // 2, 200)
        draw_text("Las notas largas (azules) requieren mantener la tecla", 26, WHITE, WIDTH // 2, 240)
        draw_text("Si soltás antes, la nota se pondrá roja y desaparecerá", 26, RED, WIDTH // 2, 280)
        draw_text("Cuanto más combo tengas, ¡más puntos haces!", 26, GREEN, WIDTH // 2, 320)
        draw_text("Presiona ESC para volver al menú", 26, GRAY, WIDTH // 2, 360)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_state = MENU
                waiting = False


def main_menu():
    global game_state
    selected = 0
    options = ["Jugar Nivel", "Instrucciones", "Salir"]

    while game_state == MENU:
        SCREEN.fill(BLACK)
        draw_text("Triple Level - Note Rush", 48, GREEN, WIDTH // 2, 100)

        for i, option in enumerate(options):
            color = WHITE if i == selected else GRAY
            draw_text(option, 36, color, WIDTH // 2, 250 + i * 60)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        game_state = GAME
                        return
                    elif selected == 1:
                        game_state = INSTRUCTIONS
                        return
                    elif selected == 2:
                        pygame.quit()
                        sys.exit()


# --- Loop principal ---
while True:
    if game_state == MENU:
        main_menu()
    elif game_state == GAME:
        game_loop()
    elif game_state == INSTRUCTIONS:
        show_instructions()
