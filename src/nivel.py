import pygame
import sys
import time
from configuracion import Configuracion

class Nivel:
    def __init__(self, pantalla, fuente, reloj, config):
        self.pantalla = pantalla
        self.fuente = fuente
        self.reloj = reloj
        self.config = config

    def mostrar_arma(self, estado, arma_esperando, arma_disparo, arma_retroceso):
        ancho, largo = self.config.ancho, self.config.largo
        if estado == "esperando":
            arma = arma_esperando
            offset_y = 0
        elif estado == "disparo":
            arma = arma_disparo 
            offset_y = -20
        elif estado == "retroceso":
            arma = arma_retroceso
            offset_y = 10
        elif estado == "recargando":
            arma = arma_esperando
            offset_y = 0
        else:
            return

        arma_ancho = arma.get_width()
        arma_alto = arma.get_height()
        x = (ancho - arma_ancho) // 2
        y = largo - arma_alto - 10 + offset_y
        self.pantalla.blit(arma, (x, y))

    def procesar_eventos(self, pajaros, sonido_disparo, balas_restantes, pajaros_destruidos, puntuacion, tiempo_recarga):
        arma_estado = "esperando"
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN and balas_restantes > 0 and tiempo_recarga <= 0:
                if sonido_disparo:
                    sonido_disparo.play()
                balas_restantes -= 1
                arma_estado = "disparo"
                mx, my = pygame.mouse.get_pos()
                for pajaro in pajaros:
                    if pajaro.rect.collidepoint(mx, my):
                        pajaros_destruidos += 1
                        puntuacion += 100
                        pajaro.reset_pos()

            if evento.type == pygame.MOUSEBUTTONUP:
                arma_estado = "esperando"

            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_e and balas_restantes < 5 and tiempo_recarga <= 0:
                print("Recargando...")
                tiempo_recarga = pygame.time.get_ticks()
                arma_estado = "recargando"

        return arma_estado, balas_restantes, pajaros_destruidos, puntuacion, tiempo_recarga

    def actualizar_pantalla(self, pajaros, pajaros_destruidos, balas_restantes, arma_estado,
                            arma_esperando, arma_disparo, arma_retroceso, puntuacion, tiempo_restante):
        for pajaro in pajaros:
            pajaro.mover()
            pajaro.dibujar(self.pantalla)

        blanco = Configuracion.blanco
        self.pantalla.blit(self.fuente.render(f"Pájaros derribados: {pajaros_destruidos}", True, blanco), (20, 20))
        self.pantalla.blit(self.fuente.render(f"Puntuación: {puntuacion}", True, blanco), (20, 50))
        self.pantalla.blit(self.fuente.render(f"Balas restantes: {balas_restantes}", True, blanco), (20, 80))
        self.pantalla.blit(self.fuente.render(f"Tiempo restante: {int(tiempo_restante)}s", True, blanco), (20, 110))
        self.mostrar_arma(arma_estado, arma_esperando, arma_disparo, arma_retroceso)

    def ejecutar_modo_tiempo(self, pajaros, sonido_disparo, imagen_fondo,
                             arma_esperando, arma_disparo, arma_retroceso, puntuacion_inicial):
        arma_esperando = pygame.transform.smoothscale(arma_esperando, (100, 100))
        arma_disparo = pygame.transform.smoothscale(arma_disparo, (100, 100))
        arma_retroceso = pygame.transform.smoothscale(arma_retroceso, (100, 100))
        imagen_fondo = pygame.transform.scale(imagen_fondo, (self.config.ancho, self.config.largo))

        pajaros_destruidos = 0
        balas_restantes = 5
        arma_estado = "esperando"
        puntuacion = puntuacion_inicial
        tiempo_limite = 60
        tiempo_inicio = pygame.time.get_ticks()

        tiempo_recarga = 0
        velocidad_pajaros = 3

        while True:
            tiempo_actual = pygame.time.get_ticks()
            segundos_transcurridos = (tiempo_actual - tiempo_inicio) / 1000
            tiempo_restante = max(0, tiempo_limite - segundos_transcurridos)

            if tiempo_restante <= 0:
                return puntuacion

            if tiempo_restante > 45:
                velocidad_pajaros = 3
            elif tiempo_restante > 30:
                velocidad_pajaros = 4
            elif tiempo_restante > 25:
                velocidad_pajaros = 5
            elif tiempo_restante > 10:
                velocidad_pajaros = 6
            else:
                velocidad_pajaros = 7

            for pajaro in pajaros:
                pajaro.velocidad = velocidad_pajaros

            self.pantalla.blit(imagen_fondo, (0, 0))

            arma_estado, balas_restantes, pajaros_destruidos, puntuacion, tiempo_recarga = self.procesar_eventos(
                pajaros, sonido_disparo, balas_restantes, pajaros_destruidos, puntuacion, tiempo_recarga
            )

            if arma_estado == "disparo":
                self.mostrar_arma(arma_estado, arma_esperando, arma_disparo, arma_retroceso)
                pygame.display.flip()
                pygame.time.delay(80)
                self.mostrar_arma("retroceso", arma_esperando, arma_disparo, arma_retroceso)
                pygame.display.flip()
                pygame.time.delay(80)
                arma_estado = "esperando"

            self.actualizar_pantalla(
                pajaros, pajaros_destruidos, balas_restantes, arma_estado,
                arma_esperando, arma_disparo, arma_retroceso, puntuacion, tiempo_restante
            )

            if tiempo_recarga > 0 and (pygame.time.get_ticks() - tiempo_recarga) / 1000 >= 3:
                balas_restantes = 5
                tiempo_recarga = 0

            pygame.display.update()
            self.reloj.tick(self.config.fps)
