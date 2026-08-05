# Beta Test Notes

## Internal Alpha Feedback

The internal alpha was tested by three family members.

General feedback:

- The game is fun and has a distinct arcade feel.
- The sound effects work well and contribute strongly to the experience.
- Gameplay systems worked as intended during the test.
- One tester repeatedly wanted to try again.
- Keyboard movement was initially difficult for less experienced players.
- Players tended to tap thrust rather than hold it.
- Pickups encouraged movement, although learning ship control took priority.

## Resolved During Beta

- [x] Add standardized controller support
- [x] Ignore unsupported joystick devices such as the connected HOTAS
- [x] Add analog ship movement
- [x] Add controller shooting, bombs, and pause controls
- [x] Add D-pad and analog-stick menu navigation
- [x] Add controller support across all menus
- [x] Add controller-friendly arcade high-score name entry
- [x] Prevent menu buttons from firing shots when gameplay resumes
- [x] Add missing title Options menu sounds
- [x] Increase player deceleration for more precise control
- [x] Scale deceleration with speed boosts
- [x] Spawn player shots from the ship muzzle
- [x] Add Ruff formatting and linting
- [x] Restore the game-over Top-10 result message

## Current Tuning

- [ ] Continue evaluating player deceleration; current value is `120`
- [ ] Gather more feedback on keyboard and controller movement
- [ ] Confirm speed boosts feel helpful rather than difficult to control
- [ ] Continue checking shot audio/visual synchronization

## Audio and Visual Polish

- [ ] Balance overall sound-effect levels
- [ ] Add master-volume control
- [ ] Clean up the speed-pickup sound tail
- [ ] Tune bomb-flash duration against the bomb sound
- [ ] Add a positive Top-10 result cue
- [ ] Consider separate idle and moving engine loops in a future version

## Release Testing

- [ ] Run additional friends-and-family testing
- [ ] Resolve significant Classic mode feedback
- [ ] Record issues or ideas that should carry into the Unity version