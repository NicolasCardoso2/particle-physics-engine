"""
Launcher — calcula velocidade inicial e instancia o tipo de projetil correto.

Responsabilidades:
    - Normalizar o vetor direcao (origem -> alvo)
    - Multiplicar pelo SPEED para obter a velocidade inicial
    - Instanciar a classe de projetil selecionada pelo usuario

Adicionar um novo tipo de disparo:
    1. Crie a classe em projectiles/<nome>.py herdando de Projectile
    2. Importe aqui
    3. Adicione uma entrada em TYPES com a tecla desejada
"""

import pygame

from projectiles import FireProjectile, GravityProjectile, PlasmaProjectile
from projectiles.base import Projectile


class Launcher:
    SPEED: float = 14.0

    # mapeamento: tecla numerica -> (rotulo exibido, classe, cor do HUD)
    TYPES: dict[int, tuple[str, type, tuple[int, int, int]]] = {
        1: ("Fogo      [1]", FireProjectile,    (255, 100, 10)),
        2: ("Plasma    [2]", PlasmaProjectile,  (80,  200, 255)),
        3: ("Gravidade [3]", GravityProjectile, (180,  60, 220)),
    }

    def __init__(self, x: float, y: float) -> None:
        self.origin = pygame.Vector2(x, y)
        self.selected: int = 1

    def fire(self, target_x: float, target_y: float) -> Projectile:
        direction = pygame.Vector2(
            target_x - self.origin.x,
            target_y - self.origin.y,
        )
        if direction.length() == 0:
            direction = pygame.Vector2(1, 0)
        else:
            direction = direction.normalize()

        vel = direction * self.SPEED
        cls = self.TYPES[self.selected][1]
        return cls(self.origin.x, self.origin.y, vel.x, vel.y)

    @property
    def type_label(self) -> str:
        return self.TYPES[self.selected][0]

    @property
    def type_color(self) -> tuple[int, int, int]:
        return self.TYPES[self.selected][2]
