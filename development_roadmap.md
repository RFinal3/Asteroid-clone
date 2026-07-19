# Development Roadmap

## v1.0 — Classic Asteroids

### Core

- [x] Add a scoring system
- [x] Implement multiple lives and respawning
- [x] Display lives and score in the HUD

### Game Feel

- [x] Add asteroid explosion effects
- [x] Add momentum-based player movement
- [x] Add screen wrapping
- [x] Add a maximum player speed
- [x] Add momentum bleed-off
- [x] Render asteroids as irregular polygons
- [x] Give the ship a triangular hitbox
- [x] Make asteroid hitboxes match their visible shapes
- [ ] Make the ship break apart on collision with asteroid or UFO bullet

### Background System

- [x] Add a static starfield
- [x] Add star twinkling

### Architecture

- [x] Separate starfield ownership from gameplay sprites
- [x] Formalize rendering layers
- [x] Centralize player damage handling
- [x] Add reusable pickup handling

### Classic Features

- [x] Add a shield power-up
- [ ] Add a speed power-up
- [ ] Add bombs
- [ ] Add UFOs
- [ ] Add scaling difficulty
- [ ] Add high-score tracking
- [ ] Add a pause menu
- [ ] Add resume, restart, high-scores, and quit options


## v2.0 — Expanded Asteroids

Ideas under consideration:

- [ ] Add multiple levels
- [ ] Add level-specific background artwork
- [ ] Give levels different backgrounds
- [ ] Increase difficulty across levels
- [ ] Add a story or campaign
- [ ] Increase alien activity at higher levels
- [ ] Add bosses, such as an alien mothership


## v3.0 — Asteroids Roguelike

Ideas under consideration:

- [ ] Add upgrade choices between levels
- [ ] Offer three randomly selected upgrades after each level
- [ ] Add weapon upgrades, such as:
  - Double, triple, or quadruple shot
  - Piercing rounds
  - Increased damage
  - Increased fire rate
  - Attack drones
- [ ] Add meta-progression upgrades, such as:
  - Faster base fire rate
  - Stronger shields and hull
  - Faster acceleration
  - Larger bombs
  - Stronger pickups
- [ ] Add a limited number of meta-upgrade build slots
- [ ] Add periodic endless high-score rounds for comparing builds
- [ ] Display the top ten scores for each high-score round