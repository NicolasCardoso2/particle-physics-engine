"""
FireProjectile — Disparo de Fogo
=================================
Comportamento:
    - Rastro denso (SPAWN_RATE = 6)
    - Drag reduzido: projetil mantem velocidade por mais tempo
    - Impacto: explosao dupla (camada laranja externa + faiscas amarelas internas)
    - Shockwave laranja de grande alcance (max_radius = 160)

Cor principal: (255, 100, 10) — laranja fogo
"""

from core.explosion import Explosion
from core.shockwave import Shockwave

from .base import Projectile


class FireProjectile(Projectile):
    """Projetil incendiario com explosao dupla em camadas."""

    SPAWN_RATE: int = 6
    DRAG: float = 0.995

    COLOR = (255, 100, 10)

    def __init__(self, x: float, y: float, vx: float, vy: float) -> None:
        super().__init__(x, y, vx, vy, color=self.COLOR)
        self.radius = 6

    def _on_impact(self) -> None:
        ix, iy = self.pos.x, self.pos.y

        # camada externa: bola de fogo laranja
        self.explosions.append(
            Explosion(ix, iy, (255, 80, 0), count=120, speed_range=(3, 12))
        )
        # camada interna: faiscas amarelas
        self.explosions.append(
            Explosion(ix, iy, (255, 220, 50), count=60, speed_range=(1, 6))
        )
        # onda de choque laranja
        self.shockwaves.append(
            Shockwave(ix, iy, (255, 140, 30), max_radius=160)
        )
        self.alive = False
