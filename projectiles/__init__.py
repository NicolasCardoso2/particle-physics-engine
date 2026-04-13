"""API publica do pacote projectiles."""

from .base import Projectile
from .fire import FireProjectile
from .gravity import GravityProjectile
from .plasma import PlasmaProjectile

__all__ = [
    "Projectile",
    "FireProjectile",
    "PlasmaProjectile",
    "GravityProjectile",
]
