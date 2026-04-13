"""
GravityProjectile — Disparo de Gravidade
==========================================
Comportamento:
    - Alto drag: cai mais rapido que os demais
    - Impacto primario: fragmenta em 3 mini-projeteis em angulos divergentes
      (-40 deg, 0 deg, +40 deg relativo ao vetor de impacto)
    - Cada fragmento explode individualmente com shockwave proprio
    - Demonstra composicao recursiva de objetos (fragmentos sao instancias
      de GravityProjectile com o flag _is_fragment=True)

Cor principal: (180, 60, 220) — violeta
"""

import math

from core.explosion import Explosion
from core.shockwave import Shockwave

from .base import Projectile


class GravityProjectile(Projectile):
    """Projetil que fragmenta em 3 mini-projeteis ao impactar."""

    SPAWN_RATE: int = 4
    DRAG: float = 0.990

    COLOR = (180, 60, 220)

    def __init__(
        self,
        x: float,
        y: float,
        vx: float,
        vy: float,
        _is_fragment: bool = False,
    ) -> None:
        super().__init__(x, y, vx, vy, color=self.COLOR)
        self._is_fragment: bool = _is_fragment
        self._fragments: list[GravityProjectile] = []
        self.radius = 3 if _is_fragment else 6

    # --- impacto ---------------------------------------------------------

    def _on_impact(self) -> None:
        ix, iy = self.pos.x, self.pos.y

        if not self._is_fragment:
            # projetil principal: gera 3 fragmentos
            speed = max(self.vel.length() * 0.6, 5.0)
            for angle_deg in (-40, 0, 40):
                angle = math.radians(angle_deg - 90)   # -90 aponta para cima
                frag = GravityProjectile(
                    ix, iy,
                    math.cos(angle) * speed,
                    math.sin(angle) * speed,
                    _is_fragment=True,
                )
                self._fragments.append(frag)

            self.shockwaves.append(
                Shockwave(ix, iy, (200, 80, 255), max_radius=90)
            )
        else:
            # fragmento: explode individualmente
            self.explosions.append(
                Explosion(ix, iy, (220, 120, 255), count=35, speed_range=(1, 5))
            )
            self.shockwaves.append(
                Shockwave(ix, iy, (220, 120, 255), max_radius=50)
            )

        self.alive = False

    # --- ciclo de vida dos fragmentos ------------------------------------

    def update(self) -> None:
        super().update()
        for f in self._fragments:
            f.update()
        self._fragments = [f for f in self._fragments if f.is_alive]

    @property
    def is_alive(self) -> bool:
        return super().is_alive or bool(self._fragments)

    def draw(self, screen) -> None:
        super().draw(screen)
        for f in self._fragments:
            f.draw(screen)
