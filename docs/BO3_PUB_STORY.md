# Pub story — Chicken Jalfrezi run

Sam's opening hook: the bartender tells the survivors, "You need to get down
to Taraj for a Chicken Jalfrezi."

## Implemented opening

The first-round preparation callback lasts 60 seconds, Sam's latest selection.
Four seconds into preparation it displays the bartender's Jalfrezi line. Seven
seconds later he adds: "First, keep this pub standing. We will sort the road out
after." The remaining 49 seconds complete the preparation period. Later rounds
retain a two-second prestart callback. Stock round spawning remains in control.

These are on-screen subtitles, without recorded speech or a speaking character
animation. The generator owns the script so regeneration preserves the opening.
`CORE65_STORY_INTRO taraj_jalfrezi` identifies the line in developer logs.

## Agreed next mechanics — not implemented by these subtitles

- A bartender behind the bar can be attacked and killed by zombies.
- Keeping him alive preserves the bar ammo/discount service. His death removes
  that service; ordinary rounds and the game continue.
- Players can buy a defensive turret on the bar. Its cost and service prices
  remain tuning decisions; no prices have been promised to Sam.
- Zombies spawn outside and enter through climbable window barricades, rather
  than rising out of the pub floor. The current stock riser setup still needs
  replacement and actual AI traversal testing.
- Taraj becomes a later story destination. It is excluded from core65's current
  playable geometry, so no active objective tells players to reach it yet.

Suggested arc for review: defend the pub, establish a safe route, reach Taraj,
then bring the Jalfrezi back. Only the opening dialogue is currently authored;
collection, return, rewards and any ending remain future work.

Keep this distinction in playtest notes: a compiled subtitle is not a working
escort/defence objective, a turret, or an implemented Taraj mission.
