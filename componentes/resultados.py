import pygame
import sqlite3
import datetime

def cargar_fuente(tamano):
    return pygame.font.Font("recursos/fuentes/Hyperwave-One.ttf", tamano)

def guardar_puntuacion(nombre, puntos, combo_max, aciertos, nivel):
    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    conn = sqlite3.connect("puntuaciones.db")
    cursor = conn.cursor()

    # Asegura que la tabla tenga todas las columnas necesarias
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS puntuaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            puntos INTEGER,
            combo_max INTEGER,
            aciertos INTEGER,
            nivel TEXT,
            fecha TEXT
        )
    """)

    # Guarda los datos
    cursor.execute("""
        INSERT INTO puntuaciones (nombre, puntos, combo_max, aciertos, nivel, fecha)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nombre, puntos, combo_max, aciertos, nivel, fecha_actual))

    conn.commit()
    conn.close()

def pantalla_resultado(pantalla, puntos, combo_max, aciertos, nivel):
    fuente_titulo = cargar_fuente(60)
    fuente_texto = cargar_fuente(32)
    fuente_input = cargar_fuente(40)

    titulo = fuente_titulo.render("RESULTADO FINAL", True, (255, 255, 0))
    puntos_txt = fuente_texto.render(f"Puntos: {puntos}", True, (255, 255, 255))
    combo_txt = fuente_texto.render(f"Combo Máximo: {combo_max}", True, (255, 255, 255))
    aciertos_txt = fuente_texto.render(f"Aciertos: {aciertos}", True, (255, 255, 255))

    ingreso = ""
    activo = True
    clock = pygame.time.Clock()

    while True:
        pantalla.fill((0, 0, 0))
        pantalla.blit(titulo, (pantalla.get_width() // 2 - titulo.get_width() // 2, 80))
        pantalla.blit(puntos_txt, (100, 200))
        pantalla.blit(combo_txt, (100, 260))
        pantalla.blit(aciertos_txt, (100, 320))

        input_txt = fuente_texto.render("Ingresá tu nombre:", True, (255, 255, 255))
        pantalla.blit(input_txt, (100, 400))

        entrada_render = fuente_input.render(ingreso, True, (255, 255, 255))
        pygame.draw.rect(pantalla, (255, 255, 255), (100, 450, 600, 50), 2)
        pantalla.blit(entrada_render, (110, 455))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN and activo:
                if evento.key == pygame.K_RETURN:
                    if ingreso.strip() != "":
                        guardar_puntuacion(ingreso.strip(), puntos, combo_max, aciertos, nivel)
                        return
                elif evento.key == pygame.K_BACKSPACE:
                    ingreso = ingreso[:-1]
                elif len(ingreso) < 20 and evento.unicode.isprintable():
                    ingreso += evento.unicode

        pygame.display.flip()
        clock.tick(60)
