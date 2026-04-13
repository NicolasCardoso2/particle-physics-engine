"""
ParticlePool — padrao Object Pool aplicado a particulas.

Problema resolvido:
    Criar e destruir centenas de objetos Particle por segundo gera pressao
    no garbage collector e fragmenta a memoria. O pool pre-aloca um conjunto
    de shells e os reutiliza via free-list (deque), garantindo O(1) nas duas
    operacoes criticas.

Complexidade:
    acquire()  -> O(1)  (pop de deque)
    release()  -> O(1)  (append de deque)
"""

from collections import deque

from .particle import Particle


class ParticlePool:
    """
    Gerencia um conjunto fixo de objetos Particle reciclados.

    Uso:
        pool = ParticlePool(capacity=1500)
        Particle._pool = pool          # registra globalmente

        p = pool.acquire(x, y, color)  # pega do pool ou cria novo
        pool.release(p)                # devolve ao pool quando morto
    """

    def __init__(self, capacity: int = 1500) -> None:
        self._free: deque[Particle] = deque()
        self.total_created: int = 0
        self.reuses: int = 0

        # Pre-aloca shells: apenas 'life' precisa estar definido
        for _ in range(capacity):
            p = Particle.__new__(Particle)
            p.life = 0
            self._free.append(p)
            self.total_created += 1

    # --- interface publica -----------------------------------------------

    def acquire(self, x: float, y: float, color: tuple, **kwargs) -> Particle:
        """Retorna particula reciclada (O(1)) ou cria nova se pool vazio."""
        if self._free:
            p = self._free.pop()
            p.__init__(x, y, color, **kwargs)
            self.reuses += 1
        else:
            p = Particle(x, y, color, **kwargs)
            self.total_created += 1
        return p

    def release(self, p: Particle) -> None:
        """Devolve particula morta ao pool (O(1))."""
        self._free.append(p)

    @property
    def free_count(self) -> int:
        """Numero de slots disponiveis no momento."""
        return len(self._free)
