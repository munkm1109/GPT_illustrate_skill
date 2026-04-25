# Theory 02E — Object Density / Human Priority Edge Case

## Purpose

Use this theory when a scene contains many objects, effects, creatures,
vehicles, architectural structures, particles, signage, or dense background
systems **and** a human figure still matters to the read.

The rule is simple:

> Dense object design is allowed only after human anatomy, contact, scale, and
> perspective have been solved.

This does not weaken the existing perspective / geometric blockout process. It
adds a priority rule inside that process: when density competes with anatomy,
reduce non-human density first.

## Trigger conditions

Treat the scene as an object-density edge case when any two or more are present:

- vehicles, rails, machinery, weapons, furniture, signs, architecture
- creatures, mounts, crowds, soldiers, background figures
- blood, smoke, fire, water, petals, shards, particles, motion streaks
- dense city / palace / lab / battlefield / transit / market backgrounds
- source-image upgrades where the original already contains many objects
- full-body / half-body human figures in perspective-heavy environments
- visible hands, fingers, feet, grip, gesture, or prop contact

## Priority order

Resolve in this order:

1. Perspective rig, support planes, scale anchors, and camera
2. Whole-body proportion and balance
3. Ribcage / pelvis / limb chains
4. Hands, individual fingers, feet, grip, and contact anatomy
5. Body-touching props and supports
6. Primary creature / vehicle / architecture relationships
7. Background density, particles, blood, signage, texture, and decoration

If the scene becomes too dense, reduce items from the bottom of the list before
changing items near the top.

## Non-negotiables

- Do not hide broken anatomy with costume, hair, blood, smoke, glow, or shadow.
- Do not fuse fingers because the hand is small or the scene is busy.
- Do not replace contact anatomy with decorative line noise.
- Do not let style density resize the figure, break limb chains, float feet, or
  disconnect hands from props.
- Do not solve dense scenes by pushing hands unnaturally forward unless the
  composition explicitly calls for foreshortening.

## Allowed reductions

When anatomy competes with density, reduce:

- background window count
- signage legibility
- particle count
- blood/smoke overlap
- costume micro-trim
- creature scale texture
- secondary prop detail
- local contrast around the hand/feet/body contact

## Required spec language

For triggered scenes, the spec must state:

- density edge case is active
- human anatomy is prioritized over object density
- what non-human details may be reduced
- what human structures are non-negotiable
- how perspective / scale / blockout remain preserved
- how image-generation prompt priority prevents style or density from hiding anatomy

## Gate

Do not pass the image-translation lock when:

- non-human effects cover unresolved hands, feet, limbs, or contact points
- the generation priority order does not place anatomy before style density
- final prompt does not explicitly say to reduce clutter before breaking anatomy
- hand/finger instructions rely on grouping or fusion instead of separate chains

