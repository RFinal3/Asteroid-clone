# Modernstroids! Development Roadmap

Modernstroids! began as the Boot.dev Asteroids project and is being developed into a larger original arcade game.

The current focus is completing and polishing Classic mode in Pygame. Future development is expected to transition to Unity after Classic mode is complete.

## Current Status

Development is currently on the `beta/v1.0` branch.

The internal Windows alpha was completed, packaged, tested, and tagged as `v1.0.0-alpha.1`.

## Classic Mode

### Completed Alpha Milestone

- [x] Complete arcade gameplay loop
- [x] Lives, respawning, shields, speed boosts, and bombs
- [x] Asteroids, UFOs, UFO bullets, and scaling difficulty
- [x] Explosion particles, ship destruction, bomb flash, and spawn pause
- [x] Persistent Top-10 high scores and keyboard name entry
- [x] Title, pause, options, high-score, and game-over screens
- [x] Persistent rotation-speed setting
- [x] Debug overlay and gated developer controls
- [x] Original gameplay and menu sound effects
- [x] Windows PyInstaller packaging
- [x] Internal family alpha playtest

### Completed Beta Work

- [x] Standardized controller detection and input handling
- [x] Controller movement, shooting, bombs, and pause support
- [x] Controller navigation across all menus
- [x] D-pad and analog-stick menu navigation
- [x] Ten-character controller high-score name entry
- [x] Prevention of menu-button input bleeding into gameplay
- [x] Improved title and in-game menu sounds
- [x] Ruff formatting and linting
- [x] Increased player deceleration for more precise control
- [x] Speed boosts now improve deceleration
- [x] Player shots now spawn from the ship muzzle

### Current Beta Work

- [ ] Continue tuning ship acceleration and deceleration
- [ ] Review architecture and remove unnecessary complexity
- [ ] Profile and optimize gameplay where useful
- [ ] Resolve additional playtest feedback
- [ ] Perform a final visual-polish pass

### Audio Polish

- [ ] Add master-volume control
- [ ] Mix and balance overall sound-effect levels
- [ ] Clean up the speed-pickup sound tail
- [ ] Tune bomb-flash timing against the bomb sound
- [ ] Add a positive Top-10 result cue

### Visual Identity and Art Polish

- [ ] Redesign the shield pickup with a blue shield icon and white outline
- [ ] Redesign the bomb pickup with a circular bomb body, fuse, and spark
- [ ] Redesign the speed pickup with grouped yellow speed arrows
- [ ] Establish consistent colors and outlines for gameplay icons
- [ ] Choose and package a distinctive game font
- [ ] Apply the font consistently across the HUD and menus
- [ ] Perform a final menu and interface layout pass
- [ ] Decide whether Modernstroids! remains the final name
- [ ] Establish basic title treatment and visual branding

### Classic Mode Completion

- [ ] Complete the remaining gameplay, audio, and visual polish
- [ ] Package a release-candidate Windows build
- [ ] Run additional friends-and-family testing
- [ ] Resolve significant feedback and bugs
- [ ] Package a stable Classic mode showcase build
- [ ] Document the completed Classic milestone

## Expanded Asteroids Milestone

Planned after Classic mode, likely following the transition to Unity.

- [ ] Multiple levels
- [ ] Level-specific backgrounds and artwork
- [ ] Story or campaign progression
- [ ] Increased alien activity
- [ ] Boss encounters
- [ ] Alien mothership encounter
- [ ] Broader visual and audio presentation

## Asteroids Roguelike Milestone

- [ ] Upgrade choices between levels
- [ ] Randomized upgrade selections
- [ ] Multiple weapons and firing patterns
- [ ] Drones and other support systems
- [ ] Build-focused gameplay
- [ ] Meta-progression
- [ ] Endless score rounds
- [ ] Separate high-score tables for special modes

### Public Testing and Release

- [ ] Build a compelling repeatable roguelike gameplay loop
- [ ] Prepare the first broadly playable public build
- [ ] Run public playtesting
- [ ] Gather balance, progression, and usability feedback
- [ ] Continue toward the complete public release

## Deferred Until Unity

- [ ] Player profiles
- [ ] Profile-based progression and unlocks
- [ ] Multiple progression save slots
- [ ] Profile-linked high scores
- [ ] Expanded accessibility and graphics settings
- [ ] More advanced input configuration