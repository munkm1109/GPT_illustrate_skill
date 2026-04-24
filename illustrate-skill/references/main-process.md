# Illustration Main Process

## Purpose

This document defines the main illustration workflow for this workspace.
The workflow is theory-first:

`load stage theories -> derive decision rules -> execute step -> produce output -> run gate check`

Do not execute a step blindly. Before each step, review the theory blocks mapped to that step and extract concrete decision rules.

## Current Theory Storage Model

- Primary unit: individual theory blocks
- Secondary mapping: process-step linkage

Current mapped theory:

- `references/theory-01-intent.md` -> `STEP 1: INTENT`
- `references/theory-02-composition-silhouette.md` -> `STEP 2: SILHOUETTE & COMPOSITION`
- `references/theory-02b-balance-cog.md` -> `STEP 2: SILHOUETTE & COMPOSITION`
- `references/theory-02c-anatomy-structure-gate.md` -> `STEP 2.3: ANATOMY STRUCTURE GATE`
- `references/theory-02d-geometric-blockout.md` -> `STEP 2.3: ANATOMY STRUCTURE GATE`, `STEP 2.8: 3D BLOCKOUT / MODELING CONTRACT`, `STEP 2.9: IMAGE TRANSLATION LOCK`
- `references/theory-03-lighting-value.md` -> `STEP 3: VALUE DESIGN`
- `references/theory-04-face-eyes.md` -> `STEP 4: FACE`
- `references/theory-04a-face-emotion-patterns.md` -> `STEP 4: FACE`
- `references/theory-05-line-shape.md` -> `STEP 5: LINE & SHAPE`
- `references/theory-05a-hands-fingers.md` -> `STEP 5: LINE & SHAPE`
- `references/theory-06-color-palette-point.md` -> `STEP 6: COLOR & ACCENT`
- `references/theory-07-texture-density.md` -> `STEP 7: TEXTURE`
- `references/theory-08-final-check-correction.md` -> `STEP 8: FINAL CHECK`

This means theories are not stored only as step summaries. They are kept as distinct theory units and then attached to one or more process steps.

## Global knowledge

Read these references when needed:

- `references/domain_context.md` for user-specific workflow expectations
- `references/style-guide.md` for the workspace art direction

## Review responsibility overlay

- In `SPEC`, the system must produce a complete staged plan with explicit reasoning hooks, then let validation / pipeline checks judge structure and completeness.
- In `CRITIQUE`, the user's success/failure judgment is primary whenever it is provided.
- The system's role in `CRITIQUE` is diagnostic:
  - explain what supports the user's read
  - explain what conflicts with the user's read
  - suggest the smallest useful next change
- The system may disagree, but it must label that disagreement as analysis, not as an override of the user's verdict.

## Process Overview

1. `STEP 1: INTENT`
2. `STEP 2: SILHOUETTE & COMPOSITION`
2.1 `STEP 2.1: PERSPECTIVE RIG`
2.2 `STEP 2.2: OBJECT INVENTORY FROM PERSPECTIVE`
2.3 `STEP 2.3: ANATOMY STRUCTURE GATE`
2.4 `STEP 2.4: OBJECT KNOWLEDGE QUERY PLAN`
2.5 `STEP 2.5: OBJECT RESEARCH HANDOFF`
2.6 `STEP 2.6: OBJECT RELATIONSHIP CHECK`
2.7 `STEP 2.7: ANATOMY-ON-OBJECT RELATIONSHIP CHECK`
2.8 `STEP 2.8: 3D BLOCKOUT / MODELING CONTRACT`
2.9 `STEP 2.9: IMAGE TRANSLATION LOCK`
3. `STEP 3: VALUE DESIGN`
4. `STEP 4: FACE`
5. `STEP 5: LINE & SHAPE`
6. `STEP 6: COLOR & ACCENT`
7. `STEP 7: TEXTURE`
8. `STEP 8: FINAL CHECK`

## Standard Step Format

Each step should be executed in the following order:

1. `THEORY`
2. `DECISION RULE`
3. `EXECUTION`
4. `OUTPUT`
5. `CHECK / GATE`

If the gate fails, revise the same step before moving forward.

## STEP 1: INTENT

### Theory

- `references/theory-01-intent.md`

### Decision Rule

Before execution, define:

- time or lighting
- environment
- subject role
- current action
- primary emotion axis (1-2 emotions)
- audience feeling

The intent sentence must be concrete and imageable.
Reject vague wording such as "pretty", "cool", or "nice" if it does not describe scene meaning.

### Execution

Input example:

- mood: `cold, dangerous smile`
- scene: `gothic portrait, neon laboratory background`

Procedure:

1. Answer the 5 intent questions internally:
   - when is this scene
   - where is this scene
   - what is the character doing
   - what 1-2 emotions dominate
   - what should the viewer feel first
2. Generate one intent line using a stable sentence pattern.
3. Tag the sentence into:
   - `environment`
   - `time_or_lighting`
   - `role`
   - `action`
   - `emotion_axis`
   - `audience_feeling`
4. Store these tags for Steps 2, 3, and 4.

### Output

- `scene_intent_sentence`
- `environment`
- `time_or_lighting`
- `role`
- `action`
- `emotion_axis`
- `audience_feeling`

### Check / Gate

All conditions must pass:

- the subject is identifiable
- where / when / what is visible in the sentence
- the emotion axis is narrowed to 1-2 emotions
- the audience feeling is explicit
- the sentence contains concrete nouns or verbs

If any condition fails, rewrite Step 1 before continuing.

## STEP 2: SILHOUETTE & COMPOSITION

### Theory

- `references/theory-02-composition-silhouette.md`
- `references/theory-02b-balance-cog.md` for grounded standing / leaning balance checks

### Decision Rule

- determine first read / focal placement
- determine composition type from intent:
  - rule of thirds
  - center / symmetry
  - asymmetry / diagonal tilt
- determine dominant black-mass placement
- determine negative-space ratio
- determine gaze-flow direction and return path
- determine whether visible hands are focal, support, or safely abstract
- determine whether finger grouping / prop grip logic needs explicit research
- when the pose is grounded, determine:
  - support leg
  - balance line
  - body-mass fall over the foot base
  - counter-balance between shoulders and pelvis
- when the scene is full-body, standing, braced, leaning, or uses stylized/exaggerated proportions:
  - make the support logic explicit in the written output
  - do not leave balance as an unstated intuition

### Execution

1. Read the Step 1 intent output.
2. Decide the focal point.
3. Classify the emotion as stable vs tense.
4. Generate `3-5` small grayscale thumbnails.
5. In each thumbnail, block only:
   - character position
   - large black mass
   - major leading lines
6. Choose the thumbnail that best matches the scene intent.
7. Build the silhouette blocking from that choice.
8. If the pose is standing, braced, or leaning:
   - mark head, torso, pelvis, and foot anchors
   - estimate the body-mass center
   - drop a balance line toward the support foot or foot base
   - adjust feet, torso tilt, or pelvis tilt until the pose reads as physically supportable
9. List visible hands and classify them as:
   - not visible
   - visible but safely simplified
   - visible and research-critical
10. If hands are visible, write:
   - palm / silhouette read
   - finger grouping read
11. If the scene contains structurally uncertain props, signage, vehicles, machinery, architecture, source-image objects, or visible hands/fingers that are focal / expressive / foreshortened / gripping:
   - list them explicitly before Step 2.5
   - do not continue to Step 3 on guesswork alone
12. If the scene shows a meaningful amount of human figure information beyond a close face crop, route the pose through Step 2.3 before Step 2.5 so age band, sex classification, limb-chain logic, and hand-submodule logic are locked.
13. Add shard, ribbon, or hair flow only after the large masses, hand read, and pose balance read clearly.

Example directional setup when the intent calls for pressure and danger:

- place character at `center-right`
- place a large black mass behind head and shoulders
- flow hair and ribbons in an `S-curve` toward `bottom-left`
- add sharp triangular shards around the character

### Output

- thumbnail set
- chosen composition type
- character position
- camera angle
- visible hands and poses
- black-mass map
- negative-space balance
- flow-direction map
- hand silhouette note
- finger grouping note
- supporting-leg note
- balance-line note
- shoulder/pelvis tilt note

### Check / Gate

- silhouette readable at thumbnail size
- focal area is not swallowed by background
- head / body / arm / prop shapes remain separable
- if hands are visible, the hand silhouette and finger grouping are readable enough that they do not collapse into mitten shapes
- shard flow supports the face instead of competing with it
- gaze stays inside the frame instead of escaping outward
- for grounded poses, the mass reads as supported by the chosen foot or base
- for grounded poses, instability reads intentional rather than anatomically broken
- for full-body or exaggerated grounded poses, the written support notes explain the pose well enough that another artist could reconstruct the balancing logic

## STEP 2.1: PERSPECTIVE RIG

### Decision Rule

Before listing dense background objects, lock the camera and perspective system:

- camera position and view height
- horizon line
- vanishing point count / placement
- primary depth axis
- support planes and contact planes
- vertical plane locks
- scale anchor objects
- perspective fail conditions

### Output

- `camera_position`
- `horizon_line`
- `vanishing_points`
- `primary_depth_axis`
- `support_planes`
- `vertical_plane_locks`
- `scale_anchor_objects`
- `contact_planes`
- `perspective_fail_conditions`

### Check / Gate

- the main support plane is named
- the primary depth axis is explicit
- objects that must share perspective are named together
- scale anchors are visible or intentionally implied
- later detail cannot contradict the rig

## STEP 2.2: OBJECT INVENTORY FROM PERSPECTIVE

### Decision Rule

List objects by perspective plane and role instead of collapsing them into generic texture or atmosphere.

Required categories:

- source-image objects when present
- primary retained objects
- structurally clear objects
- structurally uncertain objects
- foreground frame objects
- support-plane objects
- left / right vertical-plane objects
- overhead-plane objects
- background-depth objects
- effect objects
- text / glyph objects
- unknown-object triage

Unknown objects must be resolved by asking, researching, removing, replacing with a known object, intentionally abstracting with a declared function, or stopping the render-bound flow. Do not fake them as random pattern/noise.

### Check / Gate

- every structurally important object has a plane or role
- unknown objects have an action, not a decorative excuse
- text / signage is either researchable or intentionally abstracted as glyph blocks
- source-image upgrades list original-image objects before object research

## STEP 2.3: ANATOMY STRUCTURE GATE

### Theory

- `references/theory-02c-anatomy-structure-gate.md`
- `references/theory-02d-geometric-blockout.md` for primitive anatomy construction

### Decision Rule

- decide whether anatomy gating is required before Step 2.5
- default to anatomy gating when any of the following are true:
  - the scene is full-body, half-body, thigh-up, seated, leaning, jumping, lunging, or twisting
  - arms, shoulders, ribcage, pelvis, legs, or hands materially affect the read
  - the scene uses visible hands that are focal, expressive, foreshortened, or gripping
  - the request implies age-coded or sex-coded body language
- lock:
  - one age-band body base
  - one sex-classification overlay
  - one current default body-type baseline
  - one hand anatomy submodule relationship
- keep hands subordinate to the body decision:
  - hand size must agree with the chosen age band
  - wrist / elbow / shoulder logic must agree with the chosen body structure
  - prop grips must agree with both the hand module and the arm chain
- construct the body as primitive volumes before trusting detail:
  - head sphere / box
  - ribcage box or barrel
  - pelvis box
  - limb cylinder chains
  - sphere joints
  - palm blocks, thumb wedges, grouped finger cylinders
  - foot wedges aligned to the support plane

### Execution

1. Read the Step 1 intent and Step 2 composition outputs.
2. Decide whether anatomy gating is required for this scene.
3. If anatomy gating is required, choose:
   - `age_band`
   - `sex_classification`
   - `body_type_baseline`
   - `body_anatomy_base_card`
   - `sex_overlay_card`
   - `hand_anatomy_submodule_card`
4. Write the stylization level explicitly:
   - realistic leaning
   - anime simplified
   - stylized elegant
   - or another concrete mode
5. Lock the body with notes for:
   - head-to-body ratio
   - ribcage to pelvis relation
   - shoulder width
   - hip width
   - arm-chain logic
   - leg-chain logic
   - hand-size relation
   - foot-size relation
6. Reduce the body to a primitive blockout:
   - state the head primitive
   - state the ribcage primitive
   - state the pelvis primitive
   - state the limb cylinder chain
   - state the joint sphere map
   - state hand / foot primitives
   - state primitive anatomy fail conditions
7. If the user request implies a “beautiful / handsome / pretty” default body but no detailed body-type taxonomy, keep the baseline broad and note that the current system uses a beautified default rather than a fine-grained subtype.
8. If anatomy gating is not required, explicitly note why the scene is safe to keep outside the full anatomy stack.

### Output

- anatomy gate required
- age band
- sex classification
- body-type baseline
- body anatomy base card
- sex overlay card
- hand anatomy submodule card
- stylization level
- head-to-body ratio
- ribcage-pelvis relation
- shoulder width note
- hip width note
- limb proportion note
- elbow-wrist chain note
- hip-knee-ankle chain note
- hand size relative note
- foot size relative note
- anatomy primitive blockout
- head primitive
- ribcage primitive
- pelvis primitive
- limb cylinder chain
- joint sphere map
- hand / foot primitives
- anatomy primitive fail conditions
- anatomy research decision note

### Check / Gate

- age band is explicit when anatomy gating is required
- sex classification is explicit when anatomy gating is required
- body-type baseline is explicit even if the system is still using one broad beautified default
- ribcage, pelvis, and limb-chain logic are concrete enough that another artist could rebuild the pose skeleton
- anatomy primitives are named before clothing, face, hair, fur, effects, or line detail are trusted
- the primitive stack explains the torso / pelvis / limb connection before silhouette styling is allowed
- if hands are visible, the hand module is clearly subordinate to the chosen body structure rather than guessed independently
- if anatomy gating is skipped, the written note explains why the scene can safely avoid a full body-structure pass

## STEP 2.4: OBJECT KNOWLEDGE QUERY PLAN

### Theory

- external skill planning surface: `object-research-skill`

### Decision Rule

Before handoff, convert the object inventory into research lanes. Do not let anatomy, vehicles, hard-surface background, weapons, effects, and text compete in one flat list.

Use lanes such as:

- anatomy
- core scale anchors
- hard-surface background / architecture
- weapon / prop
- effects / text

### Output

- research lanes
- local card lookup plan
- existing matched cards
- missing or weak cards
- research-required objects
- query terms
- confidence by object
- draw-ready locks needed
- user checkpoint B object direction

### Check / Gate

- weak cards are named instead of marked “none” by default
- every critical object has a lane
- query terms are specific enough to retrieve or build cards
- the user is asked when an unknown object requires a material branch, naming decision, or removal / replacement decision

## STEP 2.5: OBJECT RESEARCH HANDOFF

### Theory

- external skill handoff: `object-research-skill`

### Decision Rule

Hand off when the scene needs specific background objects, props, machinery, furniture, architectural structures, scale anchors, vehicles, weapons, signage/text policy, age-band anatomy cards, sex overlays, or visible hand/finger structures whose believable form is not already clear.

Default to handoff when any of the following are true:

- the scene includes signage, vehicles, weapons, machinery, or architecture that must read believably
- the source image already contains objects whose structure or material needs confirmation
- Step 2.3 anatomy gating is required for the human figure
- the scene includes visible hands or fingers that are focal, close-up, expressive, foreshortened, or gripping a prop / weapon / cigarette / pipe / accessory
- the Step 2.2 notes include structurally uncertain objects
- the spec depends on environment storytelling that would become vague without concrete object form

Before handoff, define:

- scene intent
- scene type
- required objects
- research lanes used
- style mode
- priority
- unknown-object resolution policy

### Execution

1. Use Step 2.4 lanes as the handoff packet.
2. Query the local object library first.
3. Return matched cards by lane.
4. Research or create missing/weak cards when structure matters.
5. Return per-object draw locks, scale/perspective locks, relationship notes, and generation prompt locks.
6. If unknown objects remain, ask / research / remove / replace / intentionally abstract with declared function / stop. Do not fake them as random detail.

### Output

- object research request packet
- returned object cards by lane
- missing or weak cards by lane
- unknown-object resolution
- draw-ready locks
- generation prompt locks

### Check / Gate

- every structurally important object is either already understood or backed by a card / declared abstraction
- every anatomy-gated human figure has a body base + sex overlay, and a hand submodule when hands matter
- every visible focal hand is either already understood or backed by a reusable hand/finger card
- unresolved object ambiguity does not remain in critical background or prop forms
- object research returns locks that can be checked in Steps 2.6-2.9

## STEP 2.6: OBJECT RELATIONSHIP CHECK

### Theory

- external skill output from `object-research-skill`

### Decision Rule

Check how objects interact before styling them. Correct-looking isolated objects can still fail if scale, occlusion, contact, collision, or material/light relationships contradict each other.

### Output

- scale relation table
- occlusion order
- contact and support
- collision check
- material / light interaction
- rigid object geometry locks
- text rendering policy

### Check / Gate

- human / vehicle / creature / architecture scales are mutually believable
- occlusion order is explicit enough for image generation
- supports attach to supports: feet to planes, trams to rails, signs to walls, cables to anchors
- swords, rails, windows, signage panels, and vehicles do not melt into effects or texture
- text/signage policy prevents fake typography when exact text cannot be guaranteed

## STEP 2.7: ANATOMY-ON-OBJECT RELATIONSHIP CHECK

### Theory

- `references/theory-02c-anatomy-structure-gate.md`
- external object-research output

### Decision Rule

Place anatomy on top of the object relationship map. The body is not solved until it contacts, grips, balances on, or avoids the surrounding objects believably.

### Output

- body support logic
- anatomy structure apply note
- hand / prop relation
- hand structure apply note
- foot / object relation
- torso action relation
- anatomy-object fail conditions

### Check / Gate

- body mass follows a support or airborne arc
- hands originate from arm chains and grip props with thumb opposition / pressure logic
- feet match support surface scale and perspective
- ribcage, pelvis, and shoulders remain connected under action and clothing
- fail conditions are explicit enough to reject bad generations

## STEP 2.8: 3D BLOCKOUT / MODELING CONTRACT

### Theory

- `references/theory-02d-geometric-blockout.md`

### Decision Rule

Before image translation, express the scene as simple 3D primitives. Real 3D software is optional for spec-only work, but Blender evidence is mandatory for render-bound runs under the project hard-route. The blockout proves camera, support, contact, scale, and major silhouette; it does not automatically become the final aesthetic authority.

For full-body, humanoid, creature, architecture, rooftop, street, vehicle, weapon, or large perspective scenes, Step 2.8 must bind the environment blockout and anatomy blockout into one perspective and scale system before any detail stage may proceed.

For painterly, editorial, anime, symbolic, or mood-first outputs, use Blender as a loose structural guide by default: preserve solved camera/support/contact/scale relationships, perspective size relationships, and anatomy scale logic, but allow painterly compression, dark massing, partial occlusion, and softened rigid edges when they improve the image read. Use a stricter guide only when the user needs technical/mechanical/product/orthographic precision.

Do not use hieratic or symbolic body-size distortion to show power in ordinary commercial illustration. Authority should come from staging, camera placement, throne elevation, value grouping, costume, gaze, gesture, and detail hierarchy, while adult body scale and perspective remain believable unless the user explicitly requests mythic/symbolic scale.

The construction order is:

1. perspective rig
2. environment primitive blockout
3. anatomy primitive blockout
4. shared perspective grid
5. meter / human-scale lock
6. support, contact, footprint, and module-size checks
7. structural invariant vs painterly freedom split
8. detail-after-blockout lock

### Output

- primitive blocks
- environment primitive blockout
- shared perspective grid
- meter scale lock
- anatomy to architecture scale check
- window to head size check
- parapet to body height check
- footprint on support plane check
- detail after blockout lock
- camera blockout
- depth layer order
- contact points
- scale check
- perspective check
- optional 3D reference plan
- structural invariants to preserve
- painterly freedoms allowed
- Blender guide strength
- user checkpoint C blockout direction

### Check / Gate

- major objects can be rebuilt from boxes, cylinders, wedges, slabs, tubes, and planes
- contact points and depth layers are explicit
- scale and perspective are checked before rendering language is added
- anatomy and environment primitives share one perspective grid
- architectural modules, parapets, railings, vehicles, or fixtures keep human scale when figures are present
- detail is explicitly blocked from overriding support/contact/scale and named non-negotiable relationships
- painterly compression is explicitly allowed or disallowed rather than left implicit
- user direction is requested when blockout choices materially branch

## STEP 2.9: IMAGE TRANSLATION LOCK

### Theory

- `references/theory-08-final-check-correction.md`
- `references/theory-02d-geometric-blockout.md` for detail-after-blockout priority

### Decision Rule

Translate the structural plan into image-generation constraints. Style may enrich the locked structure but cannot replace the named support/contact/scale relationships.

When the scene has anatomy plus architecture, vehicles, props, or strong perspective, prompt priority must say that primitive blockout, perspective, contact, and scale are solved before face, costume, hair, fur, effects, lighting, color, texture, or decorative detail.

The image handoff must state the Blender guide strength:

- `loose guide`: preserve camera, contact, support, scale anchors, perspective size relationships, anatomy scale logic, and major silhouettes; allow painterly compression, partial occlusion, mood-first grouping, and value/detail emphasis without changing body scale to symbolize power.
- `medium guide`: preserve most blockout proportions and placements while allowing limited edge softening and detail integration.
- `strict guide`: preserve blockout geometry closely for product, mechanical, orthographic, or highly technical accuracy.

Default to `loose guide` for painterly/editorial/anime final images unless the user explicitly prioritizes geometric precision over beauty and mood.

### Output

- generation priority order
- non-negotiable locks
- style allowed after structure
- Blender guide strength
- painterly compression allowance
- no hieratic scale distortion lock
- prompt compression rule
- unknown object policy lock
- user checkpoint D pre-render direction

### Check / Gate

- structure priority is above style density
- the prompt explicitly says detail follows the locked support/contact/scale relationships rather than replacing them
- the prompt explicitly says whether Blender is a loose, medium, or strict guide
- painterly compression cannot break named non-negotiables such as grip, support, scale, or required object identity
- human figure scale follows perspective and anatomy; power hierarchy is not expressed by making the ruler physically oversized unless the user explicitly requests symbolic scale
- unknown objects cannot become random pattern/noise
- non-negotiable locks are short enough to survive prompt compression
- image generation is blocked when user direction is needed for an unresolved object or structural branch

## STEP 3: VALUE DESIGN

### Theory

- `references/theory-03-lighting-value.md`

### Decision Rule

- define the key light:
  - direction
  - intensity / hardness
  - temperature / color character
- limit value groups to `3-5`
- lock the largest contrast around face and eyes
- separate skin values and edges from clothes/background values and edges
- compress outer-frame values so the focal area wins in grayscale

### Execution

1. Read the Step 1 intent and Step 2 composition output.
2. Define the key light.
3. If needed, define fill light and rim light.
4. Choose a value count within `3-5`.
5. Reserve the strongest contrast for face and eyes.
6. Group the background and corners into quieter, lower-priority values.
7. Paint values in grayscale order:
   - large masses
   - middle transitions
   - focal accents
8. Separate materials by value behavior:
   - skin: soft warm-leaning midtone, soft shadow, softer edges
   - clothes/background: cooler rough dark tones, stronger cast shadows, sharper edges
9. Run a grayscale reduction test before moving on.

Example default when the scene calls for high tension:

- use `4` value levels
- skin: soft warm midtone, soft shadow
- clothes/background: cool rough dark tones
- strongest contrast around eyes and face
- darken corners and outer areas

### Output

- lighting plan
- value-count decision
- grayscale value map
- focal contrast zone
- corner / outer-area suppression plan
- material edge plan

### Check / Gate

- light direction and strength are readable
- grayscale focal point holds
- value groups remain controlled instead of muddy
- skin reads separately from costume/background
- outer frame supports center focus
- face / eye region holds the strongest contrast

## STEP 4: FACE

### Theory

- `references/theory-04-face-eyes.md`
- `references/theory-04a-face-emotion-patterns.md`

### Decision Rule

- re-read Step 1 intent and Step 3 lighting before making facial decisions
- separate:
  - surface emotion
  - inner emotion
- extract:
  - main emotion
  - support emotion
- decide emotion intensity:
  - low
  - medium
  - high
- convert emotion into a brow / eyelid / pupil / highlight / mouth pattern set
- use `main 70% + support 30%` blending when the expression is mixed
- eyes are the first-render priority
- expression must stay restrained
- expression must feel lived-in: the face should belong to the situation rather than directly describing a role label
- avoid cliché direct acting by default: no villain grin, no wide-eyed power stare, no exaggerated seduction mouth, no obvious authority scowl
- nose and mouth remain understated
- iris, pupil, and highlight design must reinforce focal clarity and agree with the scene light
- controlled asymmetry should be attempted when action, strong emotion, or situational realism would otherwise look too perfect or AI-like

### Execution

1. Re-read Step 1 intent output.
2. Re-read the Step 3 lighting plan.
3. Decide:
   - surface emotion
   - inner emotion
   - main emotion
   - support emotion
   - intensity
4. Select the facial pattern set:
   - eye openness
   - brow angle
   - gaze direction
   - pupil size
   - highlight amount
   - mouth shape and size
5. If mixed emotion is needed, blend the pattern as `main 70% + support 30%`.
6. Add only tiny controlled asymmetry when expression, action, or realism benefits:
   - one brow slightly higher
   - one lid slightly tighter
   - one mouth corner slightly shifted
   - head angle, hair shadow, pipe, hand, or prop interrupts perfect front-facing symmetry
7. Fully render eyes first in this order:
   - iris base
   - 2-3 value steps for depth
   - pupil placement
   - 1-2 main highlights
8. Use crystal-like highlight shapes in the iris.
9. Layer transparent-looking color over the iris structure.
10. Keep brows and mouth controlled rather than exaggerated.
11. Keep the nose small and understated.
12. Check the face at reduced size and make sure the eye area still wins.

### Output

- eye render plan
- surface / inner emotion note
- main / support emotion note
- expression note
- face focal map
- eye-light consistency note
- asymmetry note, if used
- natural acting / anti-direct-expression lock

### Check / Gate

- emotion reads through the eye / brow / mouth combination
- eyes read first at first glance
- the eye region has the highest local detail and strongest focal contrast
- iris / pupil / highlight design matches the scene light
- expression matches the intent sentence without overstatement
- expression reads as a person inhabiting the situation, not a direct symbol for villainy, power, seduction, anger, or authority
- pupil size and highlight amount support the intended emotional intensity
- asymmetry, if present, reads as controlled design rather than a mistake
- small asymmetry has been considered when the face risks looking too perfectly centered, polished, or AI-like
- lower face does not overpower the eyes

## STEP 5: LINE & SHAPE

### Theory

- `references/theory-05-line-shape.md`
- `references/theory-05a-hands-fingers.md` when hands are visible

### Decision Rule

- re-read Step 2 silhouette and Step 3 value structure
- if hands are visible, treat them as an anatomy submodule problem under the chosen body structure, not as decorative line noise
- split the image into line groups:
  - thin sensitive group
  - thick broken group
- keep line-weight stages within `2-3`
- decide which large planes will be decomposed into:
  - triangles
  - shards
  - ribbons
  - pointed petal forms
- decide where shape alone is enough and where line must reinforce the read
- use shape direction to guide the eye from eyes -> face -> support object
- for visible hands, decide:
  - palm block direction
  - thumb wedge read
  - finger grouping
  - where individual finger separation matters vs where grouping is enough

### Execution

1. Re-read the Step 2 silhouette and Step 3 value plan.
2. Assign the thin sensitive line group to:
   - hair
   - hands
   - jawline
   - nose indication
   - eye area
3. Assign the thick broken line group to:
   - clothing folds
   - accessories
   - background structures
   - architecture
   - shard and ribbon outer edges
4. Lock line weights to `2` levels by default, with an optional third accent level only if needed.
5. Decompose large clothing, background, and light planes into:
   - triangles
   - glass-like shard polygons
   - ribbons
   - pointed petal forms
6. Align those forms to the gaze path so the eye moves from the face toward the next supporting element without leaving the frame.
7. If hands are visible:
   - block palm first
   - place thumb second
   - separate fingers as grouped rhythms before splitting into individuals
   - keep finger thickness taper and knuckle cadence readable
   - show pressure / overlap when a prop is being held
8. Decide where broad shapes carry the read without line, especially in larger shadow and light masses.
9. Check the whole image at reduced size and confirm the style reads through line, shape, and hand readability alone.

### Output

- line hierarchy
- line-weight map
- shape-decomposition plan
- gaze-guidance motif map
- hand line priority note
- line-vs-shape role note

### Check / Gate

- sensitive parts use thin line logic while clothing/background use thicker broken logic
- if hands are visible, palm / thumb / finger grouping reads before tiny wrinkle detail
- if hands are visible, finger lengths and tapers are not uniform
- line weight is not uniform and remains controlled within 2-3 stages
- shape rhythm supports focal flow
- large planes are broken into a coherent shard / ribbon / petal language
- line and shape already communicate the intended style before color
- background roughness does not erase the silhouette

## STEP 6: COLOR & ACCENT

### Theory

- `references/theory-06-color-palette-point.md`

### Decision Rule

- re-read Step 1 intent and Step 3 value structure
- choose:
  - 2-3 base colors
  - 1-2 support colors if needed
  - 1-2 accent colors
- keep overall palette narrow and dark
- limit hue-family spread to about `3-4` regions or fewer
- preserve the value hierarchy while recoloring
- assign accent priority:
  - eyes / face first
  - selected hair / accessories second
  - small background lights or signs third
- keep strong accent area roughly under `10-20%` of the canvas
- skin color must avoid glass, porcelain, wax, plastic, or isolated beauty-retouch tones
- skin must receive the scene's shadows and bounce light so the face belongs to the same environment as hair, props, and background

### Execution

1. Re-read Step 1 intent and Step 3 value map.
2. Choose `2-3` dark low-saturation base colors.
3. Choose `1-2` accents from:
   - red
   - teal
   - purple
   - white light
4. Assign color roles:
   - main
   - support
   - accent
5. Recolor the image while preserving the existing value structure.
6. Distribute colors by part:
   - skin stays muted warm gray-beige / warm low-saturation, softer than the environment but still affected by hair shadow, prop shadow, and cool/warm bounce light
   - hair stays near the base palette with selective accent support
   - clothing uses base variations more than accent
   - background stays mostly in base tones
7. Place accent mainly in:
   - eyes / iris / highlights
   - some hair strands, ribbons, or key accessories
   - a few shards or controlled background object lights
8. Reduce or remove accents if the background begins to compete with the face.
9. Check the image at reduced size and confirm color alone still supports focus and mood.

### Output

- palette selection
- accent placement map
- base / support / accent role note
- per-part color distribution note
- non-plastic skin tone lock
- value-preservation note

### Check / Gate

- hue-family count stays controlled
- accent color count stays controlled
- the base tone remains dark and coherent
- value structure remains intact after color
- color emphasis reinforces the focal point
- skin reads alive and scene-integrated rather than porcelain, glass, wax, plastic, or separately retouched
- non-accent areas remain quiet enough
- face / eyes remain the strongest color focus

## STEP 7: TEXTURE

### Theory

- `references/theory-07-texture-density.md`

### Decision Rule

- divide the image into:
  - high density
  - medium density
  - low density
- separate smooth skin from rough costume/background
- skin must be soft but alive, with subtle local value/color variation rather than AI plastic smoothness
- define texture strategy by part:
  - skin
  - clothing / accessories
  - background / fragments
- decide whether a low global grain layer is useful
- decide where local stronger grain or texture is allowed
- decide where labels / symbols / text fragments can appear without competing with the face

### Execution

1. Divide the image into high / medium / low density zones.
2. Keep the face and immediate focal support area as the primary high-density zone.
3. Keep skin relatively smooth with light micro-variation from nose/cheek/forehead planes, eyelid shadow, hair shadow, pipe/prop shadow, and neighboring dark background.
4. Emphasize rougher texture on clothing, accessories, background structures, and fragments.
5. Add a low-intensity global grain layer only if it improves cohesion.
6. Add stronger local texture or noise selectively to:
   - clothing
   - background
   - dark secondary zones
   - fragments / ribbons / debris
7. Mask or reduce heavy texture around the face and eye region, but do not erase all skin variation into a wax/porcelain surface.
8. Add a limited number of labels, symbols, or small text fragments in secondary support zones or edges.
9. Check the image at reduced size and confirm the texture reads as organized density rather than dirt.

### Output

- texture-density map
- rough/smooth separation plan
- secondary symbol placement
- global grain note
- local texture emphasis note
- non-plastic skin surface note

### Check / Gate

- skin remains cleaner than the environment
- skin remains soft but alive, not glassy, porcelain, waxy, airbrushed-doll, or AI-plastic
- face belongs to the same light/shadow environment as hair, pipe/props, clothing, and background
- global grain supports rather than obscures the image
- texture adds atmosphere without masking the face
- density zoning is readable and the focal area stays primary
- labels / symbols support worldbuilding without stealing focus
- corners and outer regions do not become messy noise fields

## STEP 8: FINAL CHECK

### Theory

- `references/theory-08-final-check-correction.md`

### Decision Rule

- re-read Step 1 intent and compare it against the current image
- verify focus in:
  - normal view
  - reduced-size view
  - grayscale view
- verify value structure, color balance, face consistency, and texture density as one aligned system
- identify any element that competes with the face
- if output medium matters, verify resolution and color-mode suitability

### Execution

1. Re-read the Step 1 intent sentence.
2. Ask whether the image still communicates that story and feeling.
3. Check the image at reduced size.
4. Check the image in grayscale.
5. Verify:
   - eyes / face still read first
   - visible hands still read as believable hands, not fused mittens or broken claws
   - value structure still supports focus
   - color balance is controlled
   - accent colors do not spread too far
   - face and eye expression still match Step 4 / 4A
   - texture and density still support the focal area
6. If needed, make final corrections to:
   - contrast
   - tone balance
   - accent placement
   - face micro-expression
   - texture opacity / masking
7. If the piece has a known delivery medium, check output size / resolution / color suitability.
8. Record brief self-feedback and archiving notes.

### Output

- pass/fail review notes
- final correction list
- output-medium note, if relevant
- self-feedback note
- archive note

## CRITIQUE output contract

When using this process in `CRITIQUE` mode, report in this order:

1. `User Verdict`
2. `System Read`
   - `intent`
   - `process`
   - `readability`
   - `delivery`
3. `Agreement / Tension`
4. `Next Move`

The user's verdict sets the primary label.
The system diagnostic explains why the result works, fails, or remains unstable across the process steps.

### Check / Gate

All must pass before completion:

- the intended feeling can be explained in one sentence from the image
- eyes are first read
- silhouette has line and edge rhythm
- skin/background separation is clear
- grayscale focal hierarchy remains intact
- value, color, and texture all support the face
- no competing color/detail/text steals focus from the face
- output settings are appropriate for the sharing medium, if specified

## Expansion Rule

When a new theory is provided:

1. keep it as an individual theory unit
2. map it to one or more steps
3. extract decision rules from theory before execution
4. only compress into step summaries after the theory block is preserved
