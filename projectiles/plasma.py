"""
PlasmaProjectile — Disparo de Plasma
======================================
Comportamento:
    - Velocidade 40% maior que o padrao (vx * 1.4, vy * 1.4)
    - Rastro fino: particulas pequenas (size 2-4) com decaimento lento (20-40)
    - Praticamente sem drag: trajetoria quase linear
    - Impacto: flash eletrico azul claro
    - Shockwave ciano de alcance medio (max_radius = 130)

Cor principal: (80, 200, 255) — azul eletrico
"""

import random

from core.explosion import Explosion
from core.particle import Particle
from core.shockwave import Shockwave

from .base import Projectile


class PlasmaProjectile(Projectile):
    """Projetil de alta velocidade com rastro eletrico fino."""

    SPAWN_RATE: int = 2
    DRAG: float = 0.999

    COLOR = (80, 200, 255)

    def __init__(self, x: float, y: float, vx: float, vy: float) -> None:
        super().__init__(x, y, vx * 1.4, vy * 1.4, color=self.COLOR)
        self.radius = 4

    def _spawn_particles(self) -> None:
        """Rastro fino: dispersao minima, decaimento lento."""
        for _ in range(self.SPAWN_RATE):
            p = Particle.create(
                self.pos.x, self.pos.y, self.color,
                vx=random.uniform(-0.3, 0.3),
                vy=random.uniform(-0.3, 0.3),
                decay=random.randint(20, 40),
                size=random.randint(2, 4),
            )
            self.trail.append(p)

    def _on_impact(self) -> None:
        ix, iy = self.pos.x, self.pos.y

        # flash eletrico em azul claro
        self.explosions.append(
            Explosion(ix, iy, (180, 240, 255), count=50, speed_range=(4, 15))
        )
        # onda de choque ciano
        self.shockwaves.append(
            Shockwave(ix, iy, (140, 220, 255), max_radius=130)
        )
        self.alive = False
