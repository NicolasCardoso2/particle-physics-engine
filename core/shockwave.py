"""
Shockwave — anel expansivo gerado no impacto do projetil.

Fisica:
    - Raio cresce a cada frame com desaceleracao exponencial (speed *= 0.93)
    - Opacidade segue fade cubico: life = 255 * (1 - progress)^1.5
      (decai devagar no inicio, acelera no fim)
    - Espessura do anel diminui proporcionalmente ao progresso
"""

import pygame


class Shockwave:
    """
    Parametros:
        x, y       : ponto de origem
        color      : RGB base do anel
        max_radius : raio maximo antes de ser descartado
    """

    def __init__(
        self,
        x: float,
        y: float,
        color: tuple[int, int, int],
        max_radius: int = 110,
    ) -> None:
        self.x: float = x
        self.y: float = y
        self.color: tuple[int, int, int] = color
        self.radius: float = 6.0
        self.max_radius: float = float(max_radius)
        self.speed: float = 6.0
        self.life: int = 255

    # --- logica ----------------------------------------------------------

    def update(self) -> None:
        self.radius += self.speed
        self.speed = max(0.5, self.speed * 0.93)
        progress = self.radius / self.max_radius
        self.life = int(255 * max(0.0, 1.0 - progress) ** 1.5)

    @property
    def is_alive(self) -> bool:
        return self.radius < self.max_radius

    # --- renderizacao ----------------------------------------------------

    def draw(self, surface: pygame.Surface) -> None:
        if not self.is_alive or self.life <= 0:
            return
        r = int(self.radius)
        progress = self.radius / self.max_radius
        thickness = max(1, int(5 * (1.0 - progress)) + 1)
        diameter = r * 2 + 10
        surf = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        cx = diameter // 2
        pygame.draw.circle(surf, (*self.color, self.life), (cx, cx), r, thickness)
        surface.blit(surf, (int(self.x) - cx, int(self.y) - cx))
