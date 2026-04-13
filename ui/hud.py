"""
HUD (Heads-Up Display) — painel de informacoes em tempo real.

Exibe:
    - Contagem de projeteis ativos
    - Contagem de particulas vivas
    - Estado do ParticlePool (slots livres e total de reuses)
    - Tipo de projetil selecionado
    - Controles do teclado/mouse
"""

import pygame


class HUD:
    def __init__(self, font: pygame.font.Font) -> None:
        self.font = font

    def draw(
        self,
        screen: pygame.Surface,
        projectile_count: int,
        particle_count: int,
        launcher,          # type: Launcher (evita import circular)
        pool,              # type: ParticlePool
    ) -> None:
        lines: list[tuple[str, tuple[int, int, int]]] = [
            # metricas de runtime
            (f"Projeteis : {projectile_count}",   (255, 220, 80)),
            (f"Particulas: {particle_count}",     (255, 220, 80)),
            (f"Pool livre: {pool.free_count}",    (100, 220, 160)),
            (f"Reuses   : {pool.reuses}",         (100, 220, 160)),
            ("",                                  (0, 0, 0)),
            # disparo selecionado
            (f"Tipo: {launcher.type_label}",      launcher.type_color),
            ("",                                  (0, 0, 0)),
            # controles
            ("Clique .... disparar",              (140, 140, 160)),
            ("1/2/3 ..... tipo",                  (140, 140, 160)),
            ("SPACE ..... limpar",                (140, 140, 160)),
            ("ESC ....... sair",                  (140, 140, 160)),
        ]
        for i, (text, color) in enumerate(lines):
            if text:
                surf = self.font.render(text, True, color)
                screen.blit(surf, (12, 12 + i * 22))
