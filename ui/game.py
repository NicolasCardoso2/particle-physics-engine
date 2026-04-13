"""
Game — loop principal da simulacao.

Responsabilidades:
    - Inicializar pygame e criar a janela
    - Instanciar e registrar o ParticlePool global
    - Processar eventos (mouse, teclado)
    - Orquestrar update e draw de todos os projeteis
    - Renderizar HUD, fundo com motion blur e indicadores visuais
"""

import pygame

from core.constants import BG_COLOR, FPS, GROUND_Y, SCREEN_H, SCREEN_W
from core.particle import Particle
from core.pool import ParticlePool
from projectiles.base import Projectile
from ui.hud import HUD
from ui.launcher import Launcher


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Particle Simulation — OOP & Physics")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 16)

        # --- Object Pool -------------------------------------------------
        self.pool = ParticlePool(capacity=1500)
        Particle._pool = self.pool   # registra globalmente na classe

        # --- componentes -------------------------------------------------
        self.launcher = Launcher(SCREEN_W // 2, SCREEN_H - 40)
        self.projectiles: list[Projectile] = []
        self.hud = HUD(self.font)

    # --- loop ------------------------------------------------------------

    def run(self) -> None:
        running = True
        while running:
            self.clock.tick(FPS)
            running = self._handle_events()
            self._update()
            self._draw()
        pygame.quit()

    # --- eventos ---------------------------------------------------------

    def _handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_SPACE:
                    self.projectiles.clear()
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    self.launcher.selected = event.key - pygame.K_0

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                self.projectiles.append(self.launcher.fire(mx, my))

        return True

    # --- atualizacao -----------------------------------------------------

    def _update(self) -> None:
        for proj in self.projectiles:
            proj.update()
        self.projectiles = [p for p in self.projectiles if p.is_alive]

    # --- renderizacao ----------------------------------------------------

    def _draw(self) -> None:
        # motion blur: fade semi-transparente sobre o frame anterior
        fade = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        fade.fill((*BG_COLOR, 45))
        self.screen.blit(fade, (0, 0))

        for proj in self.projectiles:
            proj.draw(self.screen)

        # linha de chao
        pygame.draw.line(
            self.screen, (40, 40, 60),
            (0, GROUND_Y), (SCREEN_W, GROUND_Y), 1,
        )

        # base do lancador
        ox = int(self.launcher.origin.x)
        oy = int(self.launcher.origin.y)
        pygame.draw.circle(self.screen, (100, 100, 140), (ox, oy), 8)
        pygame.draw.circle(self.screen, (200, 200, 255), (ox, oy), 4)

        # linha de mira ate o cursor
        mx, my = pygame.mouse.get_pos()
        pygame.draw.line(self.screen, (50, 50, 70), (ox, oy), (mx, my), 1)

        # contagem total de particulas vivas
        total_particles = sum(
            len(p.trail) + sum(len(e.particles) for e in p.explosions)
            for p in self.projectiles
        )
        self.hud.draw(
            self.screen,
            len(self.projectiles),
            total_particles,
            self.launcher,
            self.pool,
        )
        pygame.display.flip()
