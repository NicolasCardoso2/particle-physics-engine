# Particle Simulation — OOP & Physics Engine

Simulacao de fisica de particulas com sistema de projeteis, rastros dinamicos, explosoes radiais e ondas de choque (shockwave). Desenvolvido em Python + Pygame com arquitetura orientada a objetos.

---

## Requisitos

| Dependencia | Versao minima |
|---|---|
| Python | 3.10+ |
| pygame | 2.x |

```bash
pip install pygame
```

---

## Como Executar

```bash
python main.py
```

---

## Controles

| Entrada | Acao |
|---|---|
| Clique esquerdo | Disparar projetil na direcao do cursor |
| `1` | Selecionar Fogo |
| `2` | Selecionar Plasma |
| `3` | Selecionar Gravidade |
| `SPACE` | Limpar todos os projeteis da tela |
| `ESC` | Sair |

---

## Tipos de Disparo

### 1. Fogo
**Arquivo:** `projectiles/fire.py`

| Propriedade | Valor |
|---|---|
| Cor | Laranja `(255, 100, 10)` |
| Rastro | Denso — 6 particulas/frame |
| Drag | 0.995 (baixo, mantem velocidade) |
| Impacto | Explosao dupla: bola de fogo laranja + faiscas amarelas |
| Shockwave | Laranja, raio maximo 160px |

Indicado para demonstrar **explosoes em camadas** e **efeito de area grande**.

---

### 2. Plasma
**Arquivo:** `projectiles/plasma.py`

| Propriedade | Valor |
|---|---|
| Cor | Azul eletrico `(80, 200, 255)` |
| Velocidade | +40% em relacao ao padrao |
| Rastro | Fino — 2 particulas/frame, decaimento lento |
| Drag | 0.999 (quasi-zero, trajetoria quase linear) |
| Impacto | Flash eletrico azul claro |
| Shockwave | Ciano, raio maximo 130px |

Indicado para demonstrar **alta velocidade**, **rastro sutil** e **fisica de baixo drag**.

---

### 3. Gravidade
**Arquivo:** `projectiles/gravity.py`

| Propriedade | Valor |
|---|---|
| Cor | Violeta `(180, 60, 220)` |
| Rastro | Medio — 4 particulas/frame |
| Drag | 0.990 (alto, cai mais rapido) |
| Impacto primario | Fragmenta em **3 mini-projeteis** (-40, 0, +40 graus) |
| Impacto secundario | Cada fragmento explode com shockwave proprio |
| Shockwave primario | Violeta, raio maximo 90px |
| Shockwave dos fragmentos | Roxo claro, raio maximo 50px |

Indicado para demonstrar **composicao recursiva de objetos** e **reacao em cadeia**.

---

## Estrutura do Projeto

```
particle-simulation/
│
├── main.py                    # ponto de entrada
│
├── core/                      # motor da simulacao
│   ├── __init__.py
│   ├── constants.py           # constantes globais (tela, fps, fisica)
│   ├── particle.py            # classe Particle + Surface Cache
│   ├── pool.py                # ParticlePool (Object Pool Pattern)
│   ├── shockwave.py           # Shockwave (anel expansivo)
│   └── explosion.py          # Explosion (burst radial)
│
├── projectiles/               # um arquivo por tipo de disparo
│   ├── __init__.py
│   ├── base.py                # Projectile (classe base)
│   ├── fire.py                # FireProjectile
│   ├── plasma.py              # PlasmaProjectile
│   └── gravity.py             # GravityProjectile
│
└── ui/                        # interface e loop de jogo
    ├── __init__.py
    ├── hud.py                 # HUD (metricas em tempo real)
    ├── launcher.py            # Launcher (calcula direcao e instancia projetil)
    └── game.py                # Game (loop principal)
```

---

## Conceitos Tecnicos Demonstrados

| Conceito | Onde |
|---|---|
| **Heranca** | `FireProjectile`, `PlasmaProjectile`, `GravityProjectile` herdam de `Projectile` |
| **Polimorfismo** | `_on_impact()` e `_spawn_particles()` sobrescritos em cada subclasse |
| **Encapsulamento** | Cada classe com responsabilidade unica e interface minima |
| **Object Pool** | `ParticlePool` em `core/pool.py` — reutiliza objetos mortos em O(1) |
| **Template Method** | `Projectile.update()` chama `_on_impact()` definido na subclasse |
| **Factory Method** | `Particle.create()` delega ao pool quando disponivel |
| **Composicao recursiva** | `GravityProjectile` cria instancias filhas de si mesmo |
| **Vetores polares** | `Explosion` converte `(r, theta)` em `(vx, vy)` via `cos/sin` |
| **Surface Cache** | `_get_cached_surf()` em `core/particle.py` — evita alocacao por frame |
| **Fisica parabolica** | Gravidade + drag aplicados por frame em `Projectile.update()` |
| **Fade cubico** | `Shockwave.life = 255 * (1 - progress)^1.5` |
| **Motion blur** | Overlay semi-transparente aplicado sobre o frame anterior |

---

## Adicionando um Novo Tipo de Disparo

1. Crie `projectiles/<nome>.py` herdando de `Projectile`
2. Sobrescreva `_on_impact()` e/ou `_spawn_particles()`
3. Adicione uma entrada em `Launcher.TYPES` em `ui/launcher.py`

```python
# Exemplo: projectiles/ice.py
from core.explosion import Explosion
from core.shockwave import Shockwave
from .base import Projectile

class IceProjectile(Projectile):
    SPAWN_RATE = 3
    DRAG = 0.993
    COLOR = (150, 230, 255)

    def __init__(self, x, y, vx, vy):
        super().__init__(x, y, vx, vy, color=self.COLOR)

    def _on_impact(self):
        self.explosions.append(Explosion(self.pos.x, self.pos.y, self.COLOR, count=60))
        self.shockwaves.append(Shockwave(self.pos.x, self.pos.y, self.COLOR, max_radius=100))
        self.alive = False
```

```python
# ui/launcher.py — adicionar na entrada TYPES:
4: ("Gelo      [4]", IceProjectile, (150, 230, 255)),
```
