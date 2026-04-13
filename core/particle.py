"""
Modulo de particulas.

Contem:
  - _get_cached_surf : cache de Surface por (size, color) — evita alocacao por frame
  - Particle         : unidade minima do sistema de particulas
"""

import random

import pygame

# ---------------------------------------------------------------------------
# Surface Cache
# Chave: (size, color) | Max ~42 entradas (7 tamanhos x 6 cores)
# Usa colorkey + set_alpha() em vez de SRCALPHA: compativel com pool de blit.
# ---------------------------------------------------------------------------
_SURF_CACHE: dict = {}


def _get_cached_surf(size: int, color: tuple) -> pygame.Surface:
    """Retorna Surface pre-renderizada para (size, color)."""
    key = (size, color)
    if key not in _SURF_CACHE:
        s = pygame.Surface((size * 2, size * 2))
        s.fill((1, 1, 1))
        pygame.draw.circle(s, color, (size, size), size)
        s.set_colorkey((1, 1, 1))
        _SURF_CACHE[key] = s
    return _SURF_CACHE[key]


# ---------------------------------------------------------------------------
# Particle
# ---------------------------------------------------------------------------
class Particle:
    """
    Unidade minima do sistema.

    Atributos principais:
        x, y    : posicao atual
        vx, vy  : velocidade
        life    : opacidade atual (255 -> 0); controla visibilidade e tamanho
        decay   : quantidade subtraida de life por frame
        size    : raio maximo em pixels
        color   : RGB
    """

    # Referencia ao ParticlePool global; definida em Game.__init__
    _pool: "ParticlePool | None" = None  # type: ignore[name-defined]

    def __init__(
        self,
        x: float,
        y: float,
        color: tuple[int, int, int],
        vx: float | None = None,
        vy: float | None = None,
        decay: int | None = None,
        size: int | None = None,
    ) -> None:
        self.x: float = x + random.uniform(-2, 2)
        self.y: float = y + random.uniform(-2, 2)
        self.vx: float = vx if vx is not None else random.uniform(-0.8, 0.8)
        self.vy: float = vy if vy is not None else random.uniform(-0.5, 0.5)
        self.life: int = 255
        self.decay: int = decay if decay is not None else random.randint(8, 18)
        self.size: int = size if size is not None else random.randint(3, 7)
        self.color: tuple[int, int, int] = color

    @classmethod
    def create(cls, x: float, y: float, color: tuple, **kwargs) -> "Particle":
        """
        Factory method: usa o ParticlePool global quando disponivel,
        evitando alocacoes desnecessarias.
        """
        if cls._pool is not None:
            return cls._pool.acquire(x, y, color, **kwargs)
        return cls(x, y, color, **kwargs)

    # --- logica ----------------------------------------------------------

    def update(self) -> None:
        self.life -= self.decay
        self.x += self.vx
        self.y += self.vy + 0.2   # micro-gravidade propria

    @property
    def is_alive(self) -> bool:
        return self.life > 0

    # --- renderizacao ----------------------------------------------------

    def draw(self, surface: pygame.Surface) -> None:
        if not self.is_alive:
            return
        size = max(1, int(self.size * (self.life / 255)))
        alpha = max(0, min(255, self.life))
        surf = _get_cached_surf(size, self.color)
        surf.set_alpha(alpha)
        surface.blit(surf, (int(self.x) - size, int(self.y) - size))
