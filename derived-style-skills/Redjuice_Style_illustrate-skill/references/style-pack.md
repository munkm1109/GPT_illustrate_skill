# Style Pack

## Identity

- style label: Reference-Redjuice-derived editorial cyber-gothic wrapper
- dominant feeling: 아름다움과 위협이 동시에 멈춰 서 있는 정적의 압력
- viewer effect:
  1. 먼저 눈 / 얼굴에 붙는다
  2. 다음으로 의상, 파편, 건축, 식물, 유리, 간판 같은 구조 장치를 읽는다
  3. 마지막에 장면의 숨겨진 상황을 추측하게 만든다
- learning basis: `Reference-Redjuice` 폴더 29 JPG, reviewed 2026-04-24
- operational goal: local reference set의 반복 특징을 stage bias로 압축하고, 일반적 모델 디폴트 미감을 억제한다

## High-confidence style spine

- delicate face + harsh frame contrast
- face-first focal hierarchy
- engineered or ceremonial environment pressure
- narrow palette with surgically placed accent planes
- large dark masses broken by shards, ribbons, petals, glass, rails, signage, or floral structures
- restrained facial acting amplified by value, framing, and material contrast

## Priority lock

- The reference-derived wrapper must remain the **primary style identity** of the image.
- Other requested treatments are subordinate unless the user explicitly says to replace the wrapper.
- Do not let a secondary style request turn the whole piece into:
  - pure ink painting
  - generic historical illustration
  - soft fantasy postcard art
  - default polished anime poster
- If a mixed-style request appears, apply this rule:
  - character, mount, costume, and focal rendering stay reference-derived
  - the secondary treatment is limited to the specific area the user named
  - the final image should still be recognized as this wrapper first

## Step Bias

### Step 1 — Intent

- Emphasize:
  - sealed emotion
  - elegant danger
  - ritual authority
  - synthetic nature
  - theatrical stillness
  - engineered beauty under stress
- Reduce or avoid:
  - casual slice-of-life comfort
  - plain “pretty character” framing with no narrative pressure
  - cheerful energy as the default read
- Recurring scene archetypes:
  - enthroned authority under eclipse / halo pressure
  - fractured crystal / shard chamber
  - greenhouse or aquarium-like artificial Eden
  - gothic interior memory stage
  - clean design-sheet variant that still keeps precise focal and costume logic
- Intent sentence bias:
  - subject + controlled action or stillness + charged frame + 1-2 cold / restrained emotions + explicit viewer fascination or unease

### Step 2 — Composition

- Emphasize:
  - big readable silhouette first
  - secondary framing through arches, panes, crystals, bars, greenhouse ribs, cables, thorns, wings, parasols, signage, floral hangings, or architectural slabs
  - clear first-read region around face and upper torso
  - designed symmetry or controlled diagonal pressure
  - environment information that behaves like emotional machinery, not wallpaper
  - explicit decision about what the background is doing for the figure
- Reduce or avoid:
  - flat center crop with no counterforce
  - empty background solved only by blur
  - decorative clutter that dissolves silhouette clarity
- Recurring preference:
  - monarch / saint / sealed-icon staging
  - figures nested inside clear geometric or environmental cages
  - wide scenes with many support objects but one luminous face anchor

### Step 3 — Value

- Emphasize:
  - 3-5 major value groups
  - bright face / eye control against darker costume or environment
  - large black or deep cool masses around the focal zone
  - selective overexposed white, glass glare, or neon frame planes
- Reduce or avoid:
  - equalized midtone painting
  - bright-everywhere polish
  - every surface receiving the same polished finish
  - detail-driven contrast that steals from the face
- Recurring preference:
  - eclipse discs, luminous windows, LED frames, aquarium glass, crystal wedges, rim-lit hair, stage-like dark surround

### Step 4 — Face

- Emphasize:
  - restrained expression
  - long upper lash logic
  - crystalline iris construction
  - tiny mouth accents
  - gaze that feels knowing, distant, seductive, melancholy, or detached
- Reduce or avoid:
  - comical exaggeration
  - large mouth acting
  - generic moe simplification with weak eye structure
- Recurring preference:
  - half-smiles
  - near-neutral calm
  - low-temperature challenge
  - melancholy nobility

### Step 5 — Line & Shape

- Emphasize:
  - thin sensitive line for face, fingers, eyelids, hair tips
  - thicker or darker broken edge logic for costume seams, hard-surface borders, frame edges, thorns, shard clusters, and black shadow accents
  - large planes subdivided into triangles, petals, ribbons, facets, tapering wedges, and layered trims
- Reduce or avoid:
  - uniform outline width
  - blob-like cloth masses
  - soft undifferentiated background masses
  - edge treatment that ignores material differences
- Recurring preference:
  - hair as tapering blade-ribbons
  - costume as layered pointed petals, glass facets, ribbon knots, lace wedges, straps, and ceremonial trims

### Step 6 — Color & Accent

- Emphasize:
  - one dominant family plus one decisive accent family
  - dark or cool body palette with concentrated red / cyan / purple / white-light accents
  - accent concentration around eyes, jewelry, crystals, trims, flowers, interface lights, or ritual markers
- Reduce or avoid:
  - rainbow spread
  - accent colors sprinkled evenly across the canvas
  - happy pastel wash as the default finish
- Recurring preference:
  - black + crimson
  - black + violet
  - cyan / teal greenhouse glow
  - white flare against cool-violet shadow
  - selective green or blue atmospheric systems when the environment carries the story

### Step 7 — Texture

- Emphasize:
  - smooth skin
  - rough costume/background
  - grain, reflective haze, bloom, scratches, label fragments, floral clutter, environmental particulate
  - glass, water, neon, metal, lace, and hard-edged decorative materials as contrast tools
- Reduce or avoid:
  - equally smooth rendering everywhere
  - dirty texture directly over the face unless it is a controlled light effect
  - empty polished zones with no material signal
- Recurring preference:
  - glossy hard surfaces against matte fabric
  - signage and labels in support zones
  - reflected water, fog, greenhouse moisture, stained glass, marble, concrete, and crystalline scatter

### Step 8 — Final Check

- Emphasize:
  - eyes first
  - face second
  - then costume motif or environment structure
  - a reduced-size read that still implies story
  - anti-generic pressure: the image should feel designed, not default-smoothed
- Reject if:
  - background feels generic or empty
  - palette is too friendly, too pastel, or too evenly saturated
  - silhouette is weak
  - face is overacting
  - accents have scattered away from focal logic
  - environment density exists but does not support the figure
  - another style family has become the dominant read before the reference-derived wrapper

## Anti-GPT drift rules

### Never rely on these shortcuts

- vague glowing fog as a substitute for designed background
- single-character poster read with no secondary framing system
- indiscriminate bloom on every highlight
- face, costume, and background all polished to the same surface feel
- costume rendered as generic smooth fashion instead of segmented directional planes
- “pretty anime girl” default face with no psychological temperature
- random particles everywhere with no compositional job
- whole-image takeover by a secondary style request that should have remained local

### Force these checks before completion

- Is there a clear pressure frame around the subject?
- Is the environment helping the narrative rather than filling space?
- Are accents clustered at actual focal triggers?
- Do line weight and material handling differ by part?
- Does the face still win when the scene is visually dense?
- Does the image still read as this wrapper first, before any secondary treatment?

## Line Unit Grammar

### 1. Face line unit

- brow: light, narrow, directional
- upper lid: most decisive facial line
- lower lid: partial or shadow-assisted, rarely equal in weight to upper lid
- nose: hinted with 1-3 selective turns, not fully contoured
- mouth: small and understated unless deliberate intensity is needed

### 2. Hair line unit

- start from large lock masses
- split into long tapering ribbons or blade-like strands
- keep tips needle-thin, sometimes abruptly broken
- allow a few crossing stray strands near the face to add tension and framing

### 3. Hand line unit

- thin and nervous near fingertips
- knuckle turns lightly indicated
- silhouette of fingers must remain elegant even in dramatic poses

### 4. Costume line unit

- straps, seams, lace, trim, zipper, and layered panel edges get darker / harder treatment
- black design shapes often substitute for fully drawn internal line
- cloth folds are not round bundles; they are wedge folds, petal splits, directional breaks, or segmented planes

### 5. Structure / background line unit

- arches, frames, weapons, greenhouse ribs, thorns, bars, parasol spokes, signage edges, aquarium frames
- can be rougher, heavier, or more mechanical than facial line
- background scratches and wire-like marks add threat, ceremony, or pressure

## Plane Unit Grammar

### 1. Skin plane

- broad and quiet
- soft warm or rosy halftone inside a cooler system
- limited segmentation
- speculars are small and controlled

### 2. Hair plane

- large ribbon planes first
- secondary glossy bands next
- terminal shards / taper planes last

### 3. Costume plane

- layered wedge planes
- petal-like flares
- black mass interruptions
- trim and lace create micro-plane rhythm at edges

### 4. Hard-surface plane

- weapon / crystal / signage / glass surfaces use sharp facet turns
- bright white or cyan edge planes can cut through darker surroundings

### 5. Background plane

- often begins as a dominant dark mass or luminous architectural slab
- then breaks with subordinate leaves, shards, labels, roses, rails, reflections, tanks, or interior framing

### 6. Accent plane

- tiny but decisive: iris glint, flower red, neon line, crystal face, rose petal, earring flare, warning label
- these small planes steer attention more than their area suggests

## Intent Inference Heuristics

- If the scene uses throne + eclipse + frontal symmetry:
  - inferred intent = enthroned danger, ritual authority, forbidden divinity
- If it uses greenhouse / aquarium / neon glass + plants:
  - inferred intent = synthetic nature, artificial Eden, beauty trapped in designed ecology
- If it uses cathedral window / arch / marble / roses:
  - inferred intent = sacred theatricality, preserved memory, melancholic grandeur
- If it uses shards / weapons / black mass + white flare:
  - inferred intent = impact, fracture, emotional danger, technological violence
- If it uses sketch-only graphite:
  - inferred intent = line must still carry elegance, aloofness, tension, and material separation before color

## Motifs

- crystals and glass facets
- horns, wings, thorn silhouettes
- ribbons, ties, tassels, lace, straps
- roses, lilies, hanging blossoms, greenhouse leaves
- crowns, thrones, parasols, cathedral or palace windows
- warning labels, interface text, signage, industrial frames
- eclipse discs, star fields, halo-like rings
- aquarium tanks, reflective water, luminous panes

## Do Not

- do not use flat cute expressions as the primary mood
- do not fill the scene with unrelated props
- do not smooth every edge into soft airbrush rendering
- do not use equal line weight everywhere
- do not let accent colors roam without focal discipline
- do not leave large background areas as generic blur if the scene claims this atmosphere
- do not sacrifice silhouette readability for decorative noise

## Evidence Notes

### Observed

- The set repeatedly combines delicate faces with harsher structural framing.
- Many pieces reserve bright accents for the eyes, crystals, flowers, or luminous architecture.
- Sketch references show that the line logic already carries elegance and tension even without color.
- Environmental pieces repeatedly merge gothic framing with cyber, industrial, or greenhouse systems.
- The strongest wide scenes remain readable because the face is still value-anchored inside dense environments.

### Inferred

- The preferred emotional target is fascination mixed with danger.
- The environment is treated as emotional machinery, not mere setting.
- Small accent planes act as narrative triggers.
- Compositional pressure and material contrast amplify restrained facial acting.
