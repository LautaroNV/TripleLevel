import pygame
import sys
from configuracion import blanco

def mostrar_arma(pantalla, estado, arma_esperando, arma_disparo, arma_retroceso, ancho, largo):
    if estado == "esperando":
        arma = arma_esperando
        offset_y = 0
    elif estado == "disparo":
        arma = arma_disparo
        offset_y = -20
    elif estado == "retroceso":
        arma = arma_retroceso
        offset_y = 10
    else:
        return

    arma_ancho = arma.get_width()
    arma_alto = arma.get_height()
    x = (ancho - arma_ancho) // 2
    y = largo - arma_alto - 10 + offset_y
    pantalla.blit(arma, (x, y))

def procesar_eventos(platos, sonido_disparo, balas_restantes, platos_destruidos, puntacion):
    arma_estado = "esperando"

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.MOUSEBUTTONDOWN and balas_restantes > 0:
            sonido_disparo.play()
            balas_restantes -= 1
            arma_estado = "disparo"
            mx, my = pygame.mouse.get_pos()
            for plato in platos:
                if plato.colision(mx, my):
                    platos_destruidos += 1
                    puntacion += 100
<<<<<<< HEAD
                    plato.reset()

    return arma_estado, balas_restantes, platos_destruidos, puntacion


def actualizar_pantalla(pantalla, platos, fuente, platos_destruidos, balas_restantes, arma_estado, arma_esperando, arma_disparo, arma_retroceso, ancho, largo, puntacion):
=======

    return arma_estado, balas_restantes, platos_destruidos, puntacion

def actualizar_pantalla(pantalla, platos, fuente, platos_destruidos, balas_restantes,
                         arma_estado, arma_esperando, arma_disparo, arma_retroceso,
                         ancho, largo, puntacion):
>>>>>>> main
    for plato in platos:
        plato.mover()
        plato.actualizar_estado()
        plato.dibujar(pantalla)

<<<<<<< HEAD
    texto = fuente.render(f"Platos destruidos: {platos_destruidos}", True, blanco)
    pantalla.blit(texto, (20, 20))
    texto2 = fuente.render(f"Balas restantes: {balas_restantes}", True, blanco)
    pantalla.blit(texto2, (20, 50))
    texto3 = fuente.render(f"Puntuación: {puntacion}", True, blanco)
    pantalla.blit(texto3, (20, 80))
    mostrar_arma(pantalla, arma_estado, arma_esperando, arma_disparo, arma_retroceso, ancho, largo)


def mostrar_game_over(pantalla, fuente, ancho, largo):
    texto_game_over = fuente.render("¡Game Over!", True, blanco)
    pantalla.blit(texto_game_over, (ancho // 2 - 100, largo // 2))
    texto_restart = fuente.render("Presioná R para reiniciar", True, blanco)
    pantalla.blit(texto_restart, (ancho // 2 - 150, largo // 2 + 50))
    pygame.display.update()
    pygame.time.delay(2000)

def seleccionar_nivel(pantalla, ancho, fuente, largo):
    seleccionado = True
    nivel = 1

    while seleccionado:
        pantalla.fill((0, 0, 0)) 
        texto_titulo = fuente.render("Selecciona un Nivel", True, blanco)
        pantalla.blit(texto_titulo, (ancho // 2 - 150, 100))

        texto_nivel1 = fuente.render("Presiona 1 para Nivel 1", True, blanco)
        pantalla.blit(texto_nivel1, (ancho // 2 - 150, 200))

        texto_nivel2 = fuente.render("Presiona 2 para Nivel 2", True, blanco)
        pantalla.blit(texto_nivel2, (ancho // 2 - 150, 250))

        texto_nivel3 = fuente.render("Presiona 3 para Nivel 3", True, blanco)
        pantalla.blit(texto_nivel3, (ancho // 2 - 150, 300))

        texto_salir = fuente.render("Presiona ESC para salir", True, blanco)
        pantalla.blit(texto_salir, (ancho // 2 - 150, 350))
=======
    pantalla.blit(fuente.render(f"Platos destruidos: {platos_destruidos}", True, blanco), (20, 20))
    pantalla.blit(fuente.render(f"Balas restantes: {balas_restantes}", True, blanco), (20, 50))
    pantalla.blit(fuente.render(f"Puntuación: {puntacion}", True, blanco), (20, 80))

    mostrar_arma(pantalla, arma_estado, arma_esperando, arma_disparo, arma_retroceso, ancho, largo)

def mostrar_game_over(pantalla, fuente, ancho, largo):
    pantalla.blit(fuente.render("¡Game Over!", True, blanco), (ancho // 2 - 100, largo // 2))
    pantalla.blit(fuente.render("Presioná R para reiniciar", True, blanco), (ancho // 2 - 150, largo // 2 + 50))
    pygame.display.update()
    pygame.time.delay(2000)

def seleccionar_nivel(pantalla, ancho, fuente, largo, logo):
    seleccionado = True
    nivel = 1
    logo_escalado = pygame.transform.scale(logo, (180, 230))

    while seleccionado:
        pantalla.fill((0, 0, 0))
        pantalla.blit(fuente.render("Selecciona un Nivel", True, blanco), (ancho // 2 - 150, 100))
        pantalla.blit(fuente.render("Presiona 1 para Nivel 1", True, blanco), (ancho // 2 - 150, 200))
        pantalla.blit(fuente.render("Presiona 2 para Nivel 2", True, blanco), (ancho // 2 - 150, 250))
        pantalla.blit(fuente.render("Presiona 3 para Nivel 3", True, blanco), (ancho // 2 - 150, 300))
        pantalla.blit(fuente.render("Presiona ESC para salir", True, blanco), (ancho // 2 - 150, 350))
        pantalla.blit(logo_escalado, (ancho - 220, 100))
>>>>>>> main

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
<<<<<<< HEAD

=======
>>>>>>> main
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    nivel = 1
                    seleccionado = False
                elif evento.key == pygame.K_2:
                    nivel = 2
                    seleccionado = False
                elif evento.key == pygame.K_3:
                    nivel = 3
                    seleccionado = False
<<<<<<< HEAD
                elif evento.key == pygame.K_ESCAPE:  
=======
                elif evento.key == pygame.K_ESCAPE:
>>>>>>> main
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

    return nivel

def mostrar_opciones_post_victoria(pantalla, fuente, ancho, largo):
<<<<<<< HEAD
    texto_opciones = fuente.render("¡Ganaste! Selecciona una opción:", True, blanco)
    pantalla.blit(texto_opciones, (ancho // 2 - 150, largo // 2 - 50))

    texto_volver = fuente.render("Presiona M para Volver al Menú", True, blanco)
    pantalla.blit(texto_volver, (ancho // 2 - 150, largo // 2))

    texto_reiniciar = fuente.render("Presiona R para Reiniciar el Nivel", True, blanco)
    pantalla.blit(texto_reiniciar, (ancho // 2 - 150, largo // 2 + 50))

    pygame.display.update()


def volver_al_menu(pantalla, fuente, ancho, largo):
    texto_volver = fuente.render("Presiona M para Volver al Menú", True, blanco)
    pantalla.blit(texto_volver, (ancho // 2 - 150, largo // 2))
=======
    pantalla.blit(fuente.render("¡Ganaste! Selecciona una opción:", True, blanco), (ancho // 2 - 150, largo // 2 - 50))
    pantalla.blit(fuente.render("Presiona M para Volver al Menú", True, blanco), (ancho // 2 - 150, largo // 2))
    pantalla.blit(fuente.render("Presiona R para Reiniciar el Nivel", True, blanco), (ancho // 2 - 150, largo // 2 + 50))
    pygame.display.update()

def volver_al_menu(pantalla, fuente, ancho, largo):
    pantalla.blit(fuente.render("Presiona M para Volver al Menú", True, blanco), (ancho // 2 - 150, largo // 2))
>>>>>>> main
    pygame.display.update()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_m:
            return True

    return False

<<<<<<< HEAD
    


def ejecutar_nivel(pantalla, reloj, fuente, platos, platos_para_pasar, sonido_disparo, ancho, imagen_fondo, mensaje, arma_esperando, arma_disparo, arma_retroceso, puntacion):
    largo = pantalla.get_height()
    nuevo_ancho = 100
    nuevo_alto = 100

    arma_esperando = pygame.transform.smoothscale(arma_esperando, (nuevo_ancho, nuevo_alto))
    arma_disparo = pygame.transform.smoothscale(arma_disparo, (nuevo_ancho, nuevo_alto))
    arma_retroceso = pygame.transform.smoothscale(arma_retroceso, (nuevo_ancho, nuevo_alto))
=======
def ejecutar_nivel(pantalla, reloj, fuente, platos, platos_para_pasar,
                   sonido_disparo, ancho, imagen_fondo, mensaje,
                   arma_esperando, arma_disparo, arma_retroceso, puntacion):

    largo = pantalla.get_height()
    arma_esperando = pygame.transform.smoothscale(arma_esperando, (100, 100))
    arma_disparo = pygame.transform.smoothscale(arma_disparo, (100, 100))
    arma_retroceso = pygame.transform.smoothscale(arma_retroceso, (100, 100))
>>>>>>> main
    imagen_fondo = pygame.transform.scale(imagen_fondo, (ancho, largo))

    platos_destruidos = 0
    balas_restantes = 10
    arma_estado = "esperando"
    game_over = False
    nivel_completado = False

    while True:
        pantalla.blit(imagen_fondo, (0, 0))

        if not game_over and not nivel_completado:
            arma_estado, balas_restantes, platos_destruidos, puntacion = procesar_eventos(
                platos, sonido_disparo, balas_restantes, platos_destruidos, puntacion
            )

            if arma_estado == "disparo":
                mostrar_arma(pantalla, arma_estado, arma_esperando, arma_disparo, arma_retroceso, ancho, largo)
                pygame.display.flip()
                pygame.time.delay(80)
                arma_estado = "retroceso"
                mostrar_arma(pantalla, arma_estado, arma_esperando, arma_disparo, arma_retroceso, ancho, largo)
                pygame.display.flip()
                pygame.time.delay(80)
                arma_estado = "esperando"

            actualizar_pantalla(
                pantalla, platos, fuente, platos_destruidos, balas_restantes,
                arma_estado, arma_esperando, arma_disparo, arma_retroceso, ancho, largo, puntacion
            )

            if platos_destruidos >= platos_para_pasar:
                nivel_completado = True

        elif nivel_completado:
            mostrar_opciones_post_victoria(pantalla, fuente, ancho, largo)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_m:
                        return puntacion
                    elif evento.key == pygame.K_r:
<<<<<<< HEAD
                        return ejecutar_nivel(pantalla, reloj, fuente, platos, platos_para_pasar,
                                              sonido_disparo, ancho, imagen_fondo, mensaje,
                                              arma_esperando, arma_disparo, arma_retroceso, puntacion)
=======
                        return ejecutar_nivel(
                            pantalla, reloj, fuente, platos, platos_para_pasar,
                            sonido_disparo, ancho, imagen_fondo, mensaje,
                            arma_esperando, arma_disparo, arma_retroceso, puntacion
                        )
>>>>>>> main

        if balas_restantes == 0 and platos_destruidos < platos_para_pasar:
            game_over = True
            mostrar_game_over(pantalla, fuente, ancho, largo)

        pygame.display.update()
        reloj.tick(60)
