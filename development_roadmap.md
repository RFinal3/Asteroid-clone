# Development Roadmap

## v1.0 — Asteroids

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
- [x] Make the ship break apart when the player loses a life

### Background System

- [x] Add a static starfield
- [x] Add star twinkling

### Architecture

- [x] Separate starfield ownership from gameplay sprites
- [x] Formalize rendering layers
- [x] Centralize player damage handling
- [x] Add reusable pickup handling
- [x] Add bounded shot and pickup lifetimes
- [x] Add an asteroid population cap
- [x] Cache rendered star glyph surfaces

### Arcade Features

- [x] Add a shield power-up
- [x] Add a speed power-up
- [x] Add bomb pickups, inventory, and basic activation
- [x] Add pickup spawning
- [x] Add UFOs
- [ ] Add scaling difficulty
- [ ] Add high-score tracking
- [ ] Add pause-menu and game-over options
- [ ] Add audio

## Remaining Work for v1.0

### 1. UFOs

- [x] Add UFO sprite and movement
- [x] Add UFO spawning
- [x] Add UFO shooting
- [x] Add UFO bullets
- [x] Add UFO collision, destruction, and scoring
- [x] Make bombs destroy UFOs

### 2. Destruction Effects

- [x] Make the player ship break apart when the player loses a life
- [x] Trigger destruction from asteroids and UFO bullets

### 3. Bomb Polish

- [x] Add explosion particles to bomb targets
- [x] Add a screen flash and fade
- [x] Briefly pause asteroid spawning after detonation

### 4. Scaling Difficulty

- [x] Scale asteroid spawn rate
- [x] Scale asteroid population cap
- [x] Scale UFO frequency and behavior
- [x] Consider asteroid speed scaling

### 5. Game States and Menus

- [x] Add debug mode and diagnostic overlay
- [x] Add pause and resume
- [x] Add restart and quit
- [x] Add a game-over screen
- [x] Replace immediate `sys.exit()` on game over

### 6. High Scores

- [x] Save and load high scores
- [x] Display the high-score table
- [x] Add completed runs to the table

### 7. Audio

- [ ] Add shooting, thrust, explosion, pickup, shield, bomb, and UFO sounds
- [ ] Create original sounds or use appropriately licensed assets

### 8. Beta and v1.0 Release

- [ ] Run family high-score playtest
- [ ] Gather balance and usability feedback
- [ ] Fix beta bugs
- [ ] Remove or toggle development diagnostics
- [ ] Release v1.0


## v2.0 — Expanded Asteroids

Ideas under consideration:

- [ ] Add multiple levels
- [ ] Add level-specific backgrounds and artwork
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