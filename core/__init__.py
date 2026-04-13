"""API publica do pacote core."""

from .constants import BG_COLOR, DRAG_DEFAULT, FPS, GRAVITY, GROUND_Y, SCREEN_H, SCREEN_W
from .explosion import Explosion
from .particle import Particle
from .pool import ParticlePool
from .shockwave import Shockwave

__all__ = [
    "SCREEN_W", "SCREEN_H", "FPS", "GRAVITY",
    "DRAG_DEFAULT", "GROUND_Y", "BG_COLOR",
    "Particle", "ParticlePool", "Shockwave", "Explosion",
]
