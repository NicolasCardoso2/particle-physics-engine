"""
Explosion — burst radial de particulas gerado no impacto do projetil.

Fisica:
    - N particulas distribuidas em angulos uniformes (vetores polares)
    - Angulos com ruido aleatorio para aparencia organica
    - Impulso vertical negativo (vy - random) = particulas sobem
    - Micro-gravidade por frame durante o update
"""

import math
import random

import pygame

from .particle import Particle


class Explosion:
    """
    Parametros:
        x, y        : ponto de origem
        color       : RGB das particulas
        count       : numero de particulas geradas
        speed_range : intervalo (min, max) da velocidade inicial
    """

    def __init__(
        self,
        x: float,
        y: float,
        color: tuple[int, int, int],
        count: int = 80,
        speed_range: tuple[float, float] = (2.0, 9.0),
    ) -> None:
        self.particles: list[Particle] = []

        for i in range(count):
            # distribui angulos uniformemente com ruido
            angle = math.radians((360 / count) * i + random.uniform(-5, 5))
            speed = random.uniform(*speed_range)
            p = Particle.create(
                x, y, color,
                vx=math.cos(angle) * speed,
                vy=math.sin(angle) * speed - random.uniform(0, 4),
                decay=random.randint(3, 9),
                size=random.randint(2, 6),
            )
            self.particles.append(p)

    # --- logica ----------------------------------------------------------

    def update(self) -> None:
        for p in self.particles:
            p.vy += 0.15   # micro-gravidade
            p.update()

        alive: list[Particle] = []
        for p in self.particles:
            if p.is_alive:
                alive.append(p)
            elif Particle._pool is not None:
                Particle._pool.release(p)   # recicla no pool
        self.particles = alive

    @property
    def is_alive(self) -> bool:
        return bool(self.particles)

    # --- renderizacao ----------------------------------------------------

    def draw(self, surface: pygame.Surface) -> None:
        for p in self.particles:
            p.draw(surface)
