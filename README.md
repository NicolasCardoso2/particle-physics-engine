<div align="center">

# Particle Physics Engine

**Simulação de física de partículas com projéteis, rastros dinâmicos, explosões radiais e ondas de choque.**

[![Python](https://img.shields.io/badge/Python_3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame_2.x-008000?style=flat-square&logo=python&logoColor=white)](https://www.pygame.org/)

> Motor de simulação 2D desenvolvido com Python + Pygame e arquitetura orientada a objetos. Implementa herança, polimorfismo, Object Pool, Template Method, composição recursiva e física parabolica com drag por frame.

</div>

---

## Índice

- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Como Rodar](#como-rodar)
- [Controles](#controles)
- [Tipos de Projétil](#tipos-de-projétil)
- [Conceitos Técnicos](#conceitos-técnicos)
- [Estrutura do Projeto](#estrutura-do-projeto)

---

## Funcionalidades

- 3 tipos de projéteis com física e visual distintos (Fogo, Plasma, Gravidade)
- Rastros dinâmicos por partícula com decaimento e fade cúbico
- Explosões radiais com shockwave expansivo
- Object Pool de partículas — reutiliza instâncias para performance
- HUD com métricas em tempo real
- Extensível: adicionar novos projéteis exige apenas uma nova subclasse

---

## Tecnologias

| Tecnologia | Versão | Uso |
|---|---|---|
| Python | 3.10+ | Linguagem principal |
| Pygame | 2.x | Renderização e loop de jogo |

---

## Como Rodar

```bash
# Instalar dependência
pip install pygame

# Executar
python main.py
```

---

## Controles

| Entrada | Ação |
|---|---|
| Clique esquerdo | Disparar projétil na direção do cursor |
| `1` | Selecionar Fogo |
| `2` | Selecionar Plasma |
| `3` | Selecionar Gravidade |
| `SPACE` | Limpar todos os projéteis da tela |
| `ESC` | Sair |

---

## Tipos de Projétil

### Fogo

| Propriedade | Valor |
|---|---|
| Cor | Laranja `(255, 100, 10)` |
| Rastro | Denso — 6 partículas/frame |
| Drag | 0.995 (baixo, mantém velocidade) |
| Impacto | Explosão dupla: bola de fogo laranja + faíscas amarelas |
| Shockwave | Laranja, raio máximo 160px |

### Plasma

| Propriedade | Valor |
|---|---|
| Cor | Azul elétrico `(80, 200, 255)` |
| Velocidade | +40% em relação ao padrão |
| Rastro | Fino — 2 partículas/frame, decaimento lento |
| Drag | 0.999 (quasi-zero, trajetória quase linear) |
| Impacto | Flash elétrico azul claro |
| Shockwave | Ciano, raio máximo 130px |

### Gravidade

| Propriedade | Valor |
|---|---|
| Cor | Violeta `(180, 60, 220)` |
| Rastro | Médio — 4 partículas/frame |
| Drag | 0.990 (alto, cai mais rápido) |
| Impacto primário | Fragmenta em **3 mini-projéteis** (-40, 0, +40 graus) |
| Impacto secundário | Cada fragmento explode com shockwave próprio |
| Shockwave primário | Violeta, raio máximo 90px |
| Shockwave dos fragmentos | Roxo claro, raio máximo 50px |

---

## Conceitos Técnicos

| Conceito | Onde |
|---|---|
| **Herança** | `FireProjectile`, `PlasmaProjectile`, `GravityProjectile` herdam de `Projectile` |
| **Polimorfismo** | `_on_impact()` e `_spawn_particles()` sobrescritos em cada subclasse |
| **Encapsulamento** | Cada classe com responsabilidade única e interface mínima |
| **Object Pool** | `ParticlePool` em `core/pool.py` — reutiliza objetos mortos em O(1) |
| **Template Method** | `Projectile.update()` chama `_on_impact()` definido na subclasse |
| **Factory Method** | `Particle.create()` delega ao pool quando disponível |
| **Composição recursiva** | `GravityProjectile` cria instâncias filhas de si mesmo |
| **Vetores polares** | `Explosion` converte `(r, theta)` em `(vx, vy)` via `cos/sin` |
| **Surface Cache** | `_get_cached_surf()` em `core/particle.py` — evita alocação por frame |
| **Física parabolica** | Gravidade + drag aplicados por frame em `Projectile.update()` |
| **Fade cúbico** | `Shockwave.life = 255 * (1 - progress)^1.5` |
| **Motion blur** | Overlay semi-transparente aplicado sobre o frame anterior |

---

## Estrutura do Projeto

```
particle-physics-engine/
├── main.py                    # ponto de entrada
├── core/                      # motor da simulação
│   ├── constants.py           # constantes globais (tela, fps, física)
│   ├── particle.py            # classe Particle + Surface Cache
│   ├── pool.py                # ParticlePool (Object Pool Pattern)
│   ├── shockwave.py           # Shockwave (anel expansivo)
│   └── explosion.py          # Explosion (burst radial)
├── projectiles/               # um arquivo por tipo de projétil
│   ├── base.py                # Projectile (classe base)
│   ├── fire.py                # FireProjectile
│   ├── plasma.py              # PlasmaProjectile
│   └── gravity.py             # GravityProjectile
└── ui/                        # interface e loop de jogo
    ├── hud.py                 # HUD (métricas em tempo real)
    ├── launcher.py            # Launcher (calcula direção e instancia projétil)
    └── game.py                # Game (loop principal)
```

---

<div align="center">

Feito por [Nicolas Cardoso](https://github.com/NicolasCardoso2) · [LinkedIn](https://www.linkedin.com/in/nicolas-cardoso-vilha-do-lago-2483b1322/)

</div>
