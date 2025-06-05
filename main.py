
import pygame
pygame.init()
import sys
from game import game_loop



WIDTH, HEIGHT = 600, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Note Rush")
FONT = pygame.font.SysFont("Arial", 30)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)

def draw_text(text, size, color, x, y, center=True):
    font = pygame.font.SysFont("Arial", size)
    rendered = font.render(text, True, color)
    rect = rendered.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    SCREEN.blit(rendered, rect)

def main_menu():
    selected = 0
    options = ["Mississippi Queen - Mountain - Fácil", "Salir"]
    running = True

    while running:
        SCREEN.fill(BLACK)
        draw_text("Rock Rush", 48, GREEN, WIDTH // 2, 100)

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
                        game_loop()
                    elif selected == 1:
                        pygame.quit()
                        sys.exit()

if __name__ == "__main__":
    main_menu()
