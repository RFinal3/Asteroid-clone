# Modernstroids! *(Working Title)*

Modernstroids! is a fast-paced Pygame arcade shooter that began as the Boot.dev Asteroids project and has grown into my first larger game-development project.

The current goal is to complete and polish Classic mode in Pygame. Future development is expected to transition to Unity for expanded levels, story content, bosses, and roguelike progression.

## Current Status

Classic mode has completed its internal Windows alpha and is currently in beta development on the `beta/v1.0` branch.

The current build has been tested as a Windows PyInstaller one-folder package. Testing is presently limited to friends and family while gameplay, presentation, architecture, and balance are refined.

## Features

- Momentum-based ship movement and screen wrapping
- Keyboard, mouse, and standardized controller support
- Player lives, respawning, and temporary invulnerability
- Shields, speed boosts, and collectible bombs
- Irregular asteroids with matching polygonal collision
- UFO enemies and UFO projectiles
- Scaling asteroid and UFO difficulty
- Explosion particles and ship-destruction effects
- Bomb screen flash and temporary spawn pause
- Layered, twinkling starfield
- Persistent Top-10 high scores
- Keyboard and controller high-score name entry
- Title, pause, options, high-score, and game-over screens
- Persistent player rotation-speed setting
- Original gameplay and menu sound effects
- Debug overlay and gated developer controls
- Windows PyInstaller packaging

## Keyboard Controls

| Input | Action |
|---|---|
| `W` | Thrust forward |
| `S` | Thrust backward |
| `A` | Rotate left |
| `D` | Rotate right |
| `Space` | Fire |
| `B` | Use bomb |
| `Escape` | Pause, resume, or go back |
| Arrow keys | Navigate menus |
| `Enter` | Select menu option |
| Mouse | Navigate and select menu options |
| `F3` | Toggle debug overlay |

## Controller Controls

The game uses SDL’s standardized controller support. Compatible Xbox, PlayStation, Switch, and similar controllers should use the same logical mappings when recognized by SDL.

| Input | Gameplay |
|---|---|
| Left stick | Turn and thrust |
| `A` / South face button | Fire |
| `B` / East face button | Use bomb |
| Start | Pause or resume |

### Controller Menu Controls

| Input | Menu action |
|---|---|
| Left stick or D-pad | Navigate |
| `A` / South face button | Select |
| `B` / East face button | Go back |
| Start | Pause or resume gameplay |

### Controller High-Score Entry

| Input | Action |
|---|---|
| Up/Down | Cycle through characters |
| `A` / South face button | Add selected character |
| `B` / East face button | Delete previous character |
| Start | Submit name |

## Running from Source

Modernstroids! currently requires Python 3.13 or later.

The project uses `uv` for dependency management:

```bash
uv sync
uv run python main.py
```

## Development Checks

Ruff is used for formatting and linting:

```bash
uv run ruff format .
uv run ruff check .
```

## Development Roadmap

See [development_roadmap.md](development_roadmap.md) for completed milestones, current beta work, and future plans.

Testing observations and active polish notes are tracked in [betanotes.md](betanotes.md).

## Future Direction

After Classic mode is complete, planned milestones include:

- Expanded levels and backgrounds
- Story or campaign progression
- Increased alien activity
- Boss encounters
- Upgrade choices and character builds
- Meta-progression
- Endless and special high-score modes
- Player profiles and progression saves

The expanded and roguelike versions are expected to be developed in Unity. Broader public testing will likely begin once the roguelike version has a compelling repeatable gameplay loop.

## Project Origins

This project began with the Boot.dev Asteroids guided project.

The original tutorial established the basic Pygame loop, player, asteroids, shooting, and collision foundations. The project has since been expanded with original gameplay systems, menus, persistence, audio, controller support, effects, debugging tools, packaging, and a long-term design roadmap.

## Built With

- Python
- Pygame
- uv
- Ruff
- PyInstaller