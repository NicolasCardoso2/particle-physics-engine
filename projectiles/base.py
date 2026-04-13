"""
Projectile — classe base para todos os tipos de disparo.

Responsabilidades:
    - Fisica parabolica (gravidade + resistencia do ar por frame)
    - Gerenciamento do rastro de particulas (spawn + recicla no pool)
    - Deteccao de colisao com o chao -> dispara _on_impact()
    - Renderizacao: rastro, explosoes, shockwaves e nucleo

Subclasses devem sobrescrever:
    _on_impact()       : comportamento ao tocar o chao
    _spawn_particles() : personalizar o rastro (opcional)

Constantes de classe (override nas subclasses):
    SPAWN_RATE : particulas geradas por frame no rastro
    DRAG       : coeficiente de resistencia do ar (0 < DRAG <= 1)
"""

import pygame

from core.constants import DRAG_DEFAULT, GRAVITY, GROUND_Y, SCREEN_W
from core.explosion import Explosion
from core.particle import Particle
from core.shockwave import Shockwave


class Projectile:
    SPAWN_RATE: int = 3
    DRAG: float = DRAG_DEFAULT

    def __init__(
        self,
        x: float,
        y: float,
        vx: float,
        vy: float,
        color: tuple[int, int, int] | None = None,
    ) -> None:
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(vx, vy)
        self.trail: list[Particle] = []
        self.explosions: list[Explosion] = []
        self.shockwaves: list[Shockwave] = []
        self.alive: bool = True
        self.color: tuple[int, int, int] = color or (255, 255, 255)
        self.radius: int = 5

    # --- metodos de template (override nas subclasses) -------------------

    def _spawn_particles(self) -> None:
        for _ in range(self.SPAWN_RATE):
            self.trail.append(Particle.create(self.pos.x, self.pos.y, self.color))

    def _on_impact(self) -> None:
        self.explosions.append(Explosion(self.pos.x, self.pos.y, self.color))
        self.shockwaves.append(Shockwave(self.pos.x, self.pos.y, self.color))
        self.alive = False

    # --- logica ----------------------------------------------------------

    def update(self) -> None:
        if self.alive:
            self.vel.y += GRAVITY
            self.vel *= self.DRAG
            self.pos += self.vel
            self._spawn_particles()

            if self.pos.y >= GROUND_Y:
                self.pos.y = GROUND_Y
                self._on_impact()

            if self.pos.x < -50 or self.pos.x > SCREEN_W + 50:
                self.alive = False

        # rastro: atualiza e recicla mortos
        for p in self.trail:
            p.update()
        alive_trail: list[Particle] = []
        for p in self.trail:
            if p.is_alive:
                alive_trail.append(p)
            elif Particle._pool is not None:
                Particle._pool.release(p)
        self.trail = alive_trail

        for e in self.explosions:
            e.update()
        self.explosions = [e for e in self.explosions if e.is_alive]

        for sw in self.shockwaves:
            sw.update()
        self.shockwaves = [sw for sw in self.shockwaves if sw.is_alive]

    @property
    def is_alive(self) -> bool:
        return self.alive or bool(self.trail) or bool(self.explosions) or bool(self.shockwaves)

    # --- renderizacao ----------------------------------------------------

    def draw(self, screen: pygame.Surface) -> None:
        for p in self.trail:
            p.draw(screen)
        for e in self.explosions:
            e.draw(screen)
        for sw in self.shockwaves:
            sw.draw(screen)

        if self.alive:
            r = self.radius
            glow = pygame.Surface((r * 6, r * 6), pygame.SRCALPHA)
            pygame.draw.circle(glow, (*self.color, 60), (r * 3, r * 3), r * 3)
            screen.blit(glow, (int(self.pos.x) - r * 3, int(self.pos.y) - r * 3))
            pygame.draw.circle(
                screen, (255, 255, 255),
                (int(self.pos.x), int(self.pos.y)), r,
            )
