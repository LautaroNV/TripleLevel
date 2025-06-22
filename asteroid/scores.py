import pygame
import os
from database import obtener_top5

pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids - Top 5")

FONT = pygame.font.SysFont("arial", 28)
WHITE = (255, 255, 255)


fondo_frames = []
fondo_path = "img/fondo_menu"  

for nombre_archivo in sorted(os.listdir(fondo_path)):
    if nombre_archivo.endswith(".png"):
        ruta = os.path.join(fondo_path, nombre_archivo)
        img = pygame.image.load(ruta).convert()
        img = pygame.transform.scale(img, (WIDTH, HEIGHT))
        fondo_frames.append(img)

print("Frames cargados:", len(fondo_frames)) 

def mostrar_puntuaciones():
    top5 = obtener_top5()
    clock = pygame.time.Clock()
    fondo_index = 0
    fondo_contador = 0
    fondo_velocidad = 5
    corriendo = True

    while corriendo:
        fondo_contador += 1
        if fondo_contador >= fondo_velocidad:
            fondo_index = (fondo_index + 1) % len(fondo_frames)
            fondo_contador = 0
    
        WIN.blit(fondo_frames[fondo_index], (0, 0))

    
        titulo = FONT.render("Top 5 Puntuaciones", True, WHITE)
        WIN.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 50))

        for i, (nombre, puntuacion) in enumerate(top5):
            texto = FONT.render(f"{i+1}. {nombre}: {puntuacion}", True, WHITE)
            WIN.blit(texto, (WIDTH // 2 - texto.get_width() // 2, 120 + i * 40))

        volver = FONT.render("Presiona ESC para volver", True, (200, 200, 200))
        WIN.blit(volver, (WIDTH // 2 - volver.get_width() // 2, HEIGHT - 60))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                corriendo = False

        clock.tick(60)
