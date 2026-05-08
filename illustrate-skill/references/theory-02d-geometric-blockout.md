# Theory 02D — Geometric Blockout Lock

## Core idea

Geometric blockout is the practice of reducing a complex subject into simple
3D primitives before adding anatomy, costume, lighting, texture, or decorative
detail. It is a structure-proof tool, not a requirement that the final image
look like a rigid 3D render.

Use this theory when a scene depends on believable body scale, perspective,
architecture, vehicles, props, weapons, crowds, or any environment where a
figure can accidentally read as giant, floating, or pasted onto the background.

## Primitive vocabulary

- `sphere` / `box`: head, skull mass, simple joint masses
- `ribcage box` / `ribcage barrel`: upper torso volume
- `pelvis box`: hip mass and leg attachment base
- `cylinder`: neck, upper arms, forearms, thighs, shins, fingers, pipes
- `sphere joint`: shoulder, elbow, wrist, hip, knee, ankle pivot
- `wedge`: feet, snout, hands in perspective, directional prop tips
- `slab`: rooftop, street, floor, wall, bridge deck
- `plane`: billboard, glass panel, sign face, facade face
- `grid module`: windows, tiles, panels, repeated architectural units

## Required construction order

1. Lock the perspective rig: camera height, horizon, vanishing points, support
   planes, contact planes, and scale anchors.
2. Block the environment as primitive forms: slabs, boxes, planes, grids,
   rails, mounted rectangles, and depth layers.
3. Block the anatomy as primitive forms: head sphere/box, ribcage box, pelvis
   box, cylindrical limbs, sphere joints, hand blocks, individual finger
   cylinders, and foot wedges.
4. Bind anatomy primitives and environment primitives to the same perspective
   grid and scale system.
5. Check contact, support, footprint size, object-object scale, and occlusion.
6. For scale-critical human-enterable scenes, add a temporary adult
   scale-proxy dummy/mannequin beside a door/window/occupant landmark on the
   same perspective grid. Use it to project adult height to the protagonist
   footpoint and record the numeric ratio before any style work.
7. Hide/delete the temporary dummy before user-facing composite/final art, but
   retain its measurement trace: height line, footpoint, projected baseline,
   and door/passenger/protagonist ratio markers.
8. Split the blockout into:
   - structural invariants to preserve
   - painterly freedoms allowed
9. For render-bound work, convert the blockout into a user-reviewable visual
   guide composite before style or final prompt work:
   - clay/solid pass as the base
   - lineart/wire/mask pass for object boundaries
   - depth/normal/mask inset when available
   - perspective / vanishing lines
   - protagonist footpoint and support plane
   - projected baseline and scale witness markers
   - retained scale-proxy dummy measurement trace, not the visible dummy body
   - door/passenger/protagonist height markers when scale-critical
   - contact/cut/grip markers when action depends on them
10. Stop at the visual-guide checkpoint. Collect user feedback on the composite,
   revise the blockout/composite if needed, and do not unlock pre-image handoff
   until the final feedback is applied and the composite is approved.
11. Only after the approved visual guide composite reads correctly, add anatomy refinement, clothing,
   face, hair, lighting, line, color, texture, and style density.

## Blender guide strength

When a real Blender pass is used, choose how strongly it should constrain the
final image:

- `loose guide`: preserve camera, support, contact, scale anchors, and major
  silhouettes; allow painterly compression, dark massing, partial occlusion,
  value/detail emphasis, and softened blockout edges without changing body
  scale to symbolize power.
- `medium guide`: preserve most blockout proportions and placements while
  allowing controlled stylization and edge integration.
- `strict guide`: preserve geometry closely for technical, product,
  mechanical, orthographic, or user-requested exactness.

For painterly, editorial, anime, symbolic, or mood-first image generation,
default to `loose guide` unless the user explicitly asks for strict geometric
precision.

## No hieratic scale by default

Do not express power by making a ruler physically larger than perspective,
anatomy, age, or sex/size logic supports. In commercial illustration, authority
should usually be shown through:

- throne or platform elevation
- camera height and framing
- value grouping and contrast control
- eye line, gesture, and pose
- costume silhouette and detail priority
- subordinate figures being lower-detail, darker, cropped, or bowed

Foreground adult men may appear larger in screen space than a farther seated
woman when perspective requires it. They can still remain compositionally
subordinate through darkness, cropping, lower detail, and bowed posture.
Use mythic/hieratic scale only when the user explicitly requests symbolic scale.

## Anatomy blockout rule

Human or humanoid figures must be understood as a primitive object stack before
they become a rendered character:

- head: sphere or simple box
- neck: short cylinder
- ribcage: tilted box or barrel
- pelvis: tilted box
- shoulders / hips: pivot line between box masses
- limbs: cylinder chains with sphere joints
- hands: palm block, thumb wedge, and individual thumb / index / middle / ring / little finger cylinders
- feet: wedge blocks aligned to the support plane

The anatomy blockout is not complete until it explains support, balance,
gesture, and prop contact.

## Environment blockout rule

Architecture and hard-surface backgrounds must also be simplified before
detail:

- rooftop / street / floor: large slab
- parapet / railing / curb: long box with human-scale height
- building: vertical slab
- facade: plane with large window modules
- billboard / signage: mounted rectangle plane
- glass: flat reflective panel, not random texture
- crowd below: tiny depth clusters tied to the street plane

Dense detail is not allowed to replace readable planes and modules.

## Shared scale lock

The figure and environment must share a single scale logic. For high-rise,
street, vehicle, or architectural scenes, explicitly check:

- a figure's full body is adult-human scale unless the intent says otherwise
- boots or feet occupy small patches of the support plane, not the whole slab
- nearby parapets / railings / curbs have believable body-relative height
- windows are architectural modules, not tiny texture dots
- a single nearby window must not become tiny compared with the head
- if a figure is large because it is close to camera, nearby roof edges,
  parapet thickness, fixtures, doors, vents, rails, or foreground anchors must
  enlarge with matching foreshortening
- a figure silhouette must not span multiple building floors unless giant scale
  is intentional

## Detail-after-blockout rule

Detail may enrich the blockout, but it may not create a new structure where the
blockout solved support, contact, scale, or named object identity.

Do not let:

- face priority enlarge the head beyond the scale grid
- costume shape hide broken torso / pelvis connection
- cloak, hair, fur, smoke, glow, or motion effects replace limb geometry
- background window grids shrink into tiny texture that implies giant figures
- blade, weapon, railing, or signage melt into effects

If detail contradicts the primitive blockout, the detail loses.

## Visual guide composite approval gate

Render-bound specs must not rely on text-only projection math. The structure
must become an actual image reference that the user can inspect before the
final aesthetic stages continue.

The composite is not final art. It is a control/reference image for camera,
perspective, scale, support/contact, and object placement. The final image may
ignore clay material, labels, arrows, and guide text, but it must obey the
approved spatial relationships.

The composite is also not the only authority. It is one reference in the
handoff stack. The final generator must still receive or obey the source image
conditioning status, immutable user commands, object research, perspective math,
scale-proxy projection, Blender passes, visibility report, and compiled final
prompt. If a handoff uses only the composite and drops those earlier locks, it
has not followed the process.

Exception/clarification for scale-critical work: the composite is not the only
authority for the whole image, but it is the hard authority for scale. The
approved composite's scale markers, projected baselines, footpoints,
dummy-derived traces, door/passenger/container ratios, and screen occupancy
must be followed. If the final image has attractive style but scale drifts from
the composite, the image fails.

For scale-proxy dummy workflows, the dummy is a temporary measuring object. It
may appear in clay/blockout review, but it must be hidden/deleted before the
visual guide composite and final art unless the user explicitly wants a visible
extra person. Keep only the measurement trace/height line/baseline overlay.

For image generation, the composite must be supplied as an actual image input
or external ControlNet/depth/lineart control, not merely described in the text
prompt. If the runtime only accepts text, the run is a prompt-only fallback and
cannot claim strong structure conditioning.

Required checkpoint logic:

- `VISUAL_GUIDE_COMPOSITE_REQUIRED: yes`
- create `VISUAL_GUIDE_COMPOSITE_PATH`
- record source passes and overlays
- for scale-critical scenes, record the hidden scale-proxy trace overlay and
  its pass/fail projection verdict
- show or reference the composite for user review
- record `USER_VISUAL_GUIDE_FEEDBACK`
- apply the final feedback
- keep `PRE_IMAGE_HANDOFF_READY: no` until
  `USER_VISUAL_GUIDE_APPROVAL_STATUS: approved` and
  `USER_VISUAL_GUIDE_FEEDBACK_APPLIED: pass`
- carry `PRE_COMPOSITE_EVIDENCE_STACK_LOCK` and
  `COMPOSITE_IS_REFERENCE_NOT_SOLE_AUTHORITY` into Step 2.9 before generation
- carry `SCALE_MUST_FOLLOW_COMPOSITE_PROMPT_LOCK` and Step 8
  `SCALE_COMPOSITE_HARD_LOCK_VERDICT_CHECK` for scale-critical scenes

Painterly compression is different from contradiction. It is allowed when it
keeps the solved relationships readable:

- crowds may merge into dark masses if adult scale and bowing posture still read
- foreground adult figures may be cropped, dark, or low-detail, but not shrunk
  below plausible perspective/anatomy scale to flatter the ruler
- stair or architecture spacing may compress for drama if hierarchy and support
  remain clear
- background panels may become emotional texture if they remain attached to
  their surfaces
- ornate detail may soften rigid cube edges if object identity remains clear

## Fail conditions

Revise before rendering if any of these are true:

- the figure reads as a giant because windows, doors, or parapets are too small
- feet do not sit on a named support plane
- anatomy cylinders do not connect to ribcage / pelvis boxes
- hands grip a weapon without clear palm / thumb / individual finger-chain relations
- foreground scale is enlarged but nearby foreground architecture is not
- buildings are random patterns instead of slabs, planes, and modules
- style density appears before the viewer can read the blockout
- Blender conditioning makes the final image feel CAD-like, plastic, or
  over-explained when the intended output is painterly or mood-first
- painterly compression breaks a named invariant such as grip, foot support,
  scale hierarchy, or required object identity
- power hierarchy is represented by impossible body-size scaling instead of
  composition, value, camera, pose, or staging
