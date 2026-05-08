# Theory 02J — Camera Class and Scale-Critical Shot Gate

## Purpose

Camera class is a structural input, not a decorative prompt adjective. When a
scene depends on a human being correctly sized against a tram, train, building,
room, bus, or other human-enterable object, the chosen shot class determines
whether the scale proof can survive image generation.

## Camera class presets

Use a first-class camera preset before final composition:

- `extreme_wide_scale_shot`
- `wide_establishing_shot`
- `wide_action_shot`
- `full_body_action_shot`
- `medium_action_shot`
- `close_portrait_shot`
- `low_angle_hero_shot`
- `top_down_diagrammatic_shot`
- `telephoto_compressed_city_shot`
- `dutch_angle_dynamic_shot`
- `custom_user_camera_class`

The user may set the preset directly. Record the lock level:

- `soft` — the skill may adjust the camera when structure requires it.
- `hard` — preserve the user camera class; if it conflicts with scale, block
  image handoff and report the conflict.
- `adaptive` — preserve the user intent initially, but allow post-image repair
  to escalate the camera class if the verdict fails.

## Scale-critical rule

If `SCALE_CRITICAL_MODE: yes`, close, medium, portrait, and face-first hero
camera classes are unsafe until scale passes. The scale proof must move into a
wide/long shot class:

- The vehicle/container/building must dominate the frame.
- The protagonist must read as a small figure, not a heroic close-up.
- Doors, windows, seats, aisle, passengers/occupants, roof rails, and repeated
  modules must be visible enough to compare human size.
- Face and eyes can remain focal, but only as small bright accents, not as a
  portrait crop.

For long vehicles such as trams/trains, a typical repair target is:

- extreme wide / wide scale shot
- full multi-car or long passenger cabin visibility
- 12+ window/door/module witnesses when feasible
- protagonist roughly one adult door/window/passenger height
- protagonist under 5% of visible vehicle length when the full vehicle length is
  the main scale witness

## Perspective calculation chain

Camera cuts and scale adjustments must always move through this chain:

```text
perspective calculation
  -> temporary adult scale-proxy dummy placement
  -> dummy-to-hero projection
  -> blockout / guide
  -> hide/delete dummy, retain measurement trace
  -> visual guide composite
  -> user feedback / approval
  -> final prompt
```

Do not solve a camera or scale problem by placing a door next to the protagonist
by default. A nearby door is only one possible witness. The required invariant is
that a reliable baseline is projected to the protagonist's foot/support plane:

1. Declare `HERO_FOOTPOINT_PLANE` (for example, `tram_roof_plane`).
2. Declare `BASELINE_OBJECT` (for example, a 1.95m tram door, 1.65m passenger,
   roof width, seat/aisle module, or another measured object).
3. Project that baseline through the shared horizon / vanishing points /
   perspective grid to the protagonist position.
4. Record `PROJECTED_BASELINE_TO_HERO_POSITION` with numbers, e.g. heroine
   1.58m is 0.81 of a projected 1.95m door at her footpoint.
5. For scale-critical human-enterable objects, add a temporary adult
   scale-proxy dummy/mannequin beside the door/window/occupant baseline and
   record `SCALE_PROXY_DUMMY_REQUIRED`, `SCALE_PROXY_DUMMY_HEIGHT`,
   `SCALE_PROXY_DUMMY_BASELINE_OBJECT`, `SCALE_PROXY_DUMMY_PLACEMENT_PLAN`, and
   `SCALE_PROXY_DUMMY_TO_HERO_PROJECTION`.
6. Mark `SCREEN_OCCUPANCY_IS_DERIVED: yes` and
   `SCREEN_OCCUPANCY_MUST_NOT_OVERRIDE_WORLD_SCALE: yes`.

This separates two ideas that image models often confuse:

- screen occupancy / crop prominence
- physical world scale

A full-body or knee-shot protagonist may occupy more screen space because the
camera is close, but that screen share must be derived from the camera and must
not resize the character against projected doors, passengers, roof modules, or
other world-scale anchors.

Step 2.8 must transfer the calculation into blockout/guide evidence:

- `PERSPECTIVE_CALCULATION_BLOCKOUT_TRANSFER`
- `PROJECTED_BASELINE_BLOCKOUT_CHECK`
- `SCREEN_OCCUPANCY_BLOCKOUT_RECONCILIATION`
- `SCALE_PROXY_DUMMY_BLOCKOUT_PLACEMENT`
- `SCALE_PROXY_DUMMY_BLOCKOUT_CHECK`
- `SCALE_PROXY_DUMMY_REMOVAL_POLICY`
- `SCALE_PROXY_TRACE_OVERLAY`
- `SCALE_PROXY_TO_HERO_BLOCKOUT_VERDICT`
- `VISUAL_GUIDE_COMPOSITE_PATH`
- `VISUAL_GUIDE_COMPOSITE_OVERLAYS`
- `USER_VISUAL_GUIDE_APPROVAL_STATUS`

The visual guide composite must be an actual image reference, not a prose
description. It should show the same projected baseline, support plane,
protagonist footpoint, door/passenger/protagonist scale markers, and relevant
contact/cut/grip markers that the final image must obey. Image handoff remains
blocked until the user has reviewed the composite and the final feedback has
been applied.

For scale-critical scenes, set `SCALE_COMPOSITE_HARD_LOCK: yes`. The composite
is not the sole authority for the entire image, but it **is** the binding visual
authority for scale. Protagonist/object size, footpoints, door/passenger/container
ratios, projected baselines, dummy-derived traces, and screen occupancy must
follow the approved composite. If style, action drama, beauty framing, or prompt
wording conflicts with the composite scale, the composite scale wins.

The temporary dummy is a measuring instrument, not a final character. It may be
visible in blockout/clay review while scale is being solved. Before the
user-facing visual guide composite and before final art handoff, hide/delete the
dummy mesh/body but keep its measurement trace: height line, footpoint, projected
baseline, and ratio labels/markers. If the dummy remains visible as a person in
the final image, the scale-proxy process failed.

After approval, do not let image generation use only the composite. Step 2.9
must record that the composite is one strong reference in the full stack:
source image, user commands, object research, Step 2.1 perspective math,
scale-proxy projection, Blender passes, visibility report, approved composite,
and compiled final prompt. A composite-only or text-only handoff is not the same
as the approved process.

Step 2.9 must also include `SCALE_MUST_FOLLOW_COMPOSITE_PROMPT_LOCK`: the final
image prompt/handoff has to say in natural language that scale follows the
approved composite markers and fails if it drifts. Step 8 must include
`SCALE_COMPOSITE_HARD_LOCK_VERDICT_CHECK`.

Step 2.9 must compile the same calculation into natural image language, not raw
field names. Example:

```text
Her full body fills the frame because the camera is close on the tram roof, but
her world scale follows the projected tram-door height at her foot position; she
is smaller than the projected adult door height, not enlarged by the crop.
```

Step 8 must verdict both the projection and the screen/world-scale separation.
It must also audit that the final image generation used the approved visual
guide composite as a structure reference and did not proceed while approval was
pending. In scale-critical scenes it must also audit `SCALE_PROXY_TRACE_VERDICT_CHECK`:
the hidden dummy's retained measurement trace controlled protagonist size, while
the dummy itself did not appear in the final illustration.

## Conflict handling

When user camera class and scale proof conflict:

1. Record `CAMERA_CLASS_CONFLICT_STATUS: conflict`.
2. State the reason, e.g. close portrait cannot prove tram/person scale.
3. If lock is `soft` or `adaptive`, resolve by widening to a scale-proving shot.
4. If lock is `hard`, do not silently override; block image handoff or ask the
   user to choose between the hard camera lock and scale correctness.

## Prompt compiler rule

For scale-critical handoff, the compiled prompt must begin with the visual shot
class, not with validator fields or character beauty:

```text
Extreme wide scale shot, no close-up heroine. A long multi-car passenger tram
dominates the frame...
```

Then state the scale witnesses:

- repeated doors/windows/modules
- visible passenger/occupant silhouettes
- protagonist as a small roof/support-plane figure
- face/eyes as small accents

Do not pass raw field names such as `CAMERA_CLASS_PROMPT_OPENING`,
`SCALE_CRITICAL_SHOT_CLASS`, `Tier 0`, or verdict keys to image generation.

## Post-image repair rule

If any scale-related verdict fails (`container_scale_pass`,
`hero_fits_inside_object`, `occupant_anchor_valid`,
`protagonist_to_occupant_ratio_pass`, or `scale_visual_guide_pass`), repair the
camera/framing first:

- escalate to extreme wide / wide scale shot
- reduce protagonist screen share
- show full container/vehicle visibility
- increase door/window/passenger/module witnesses
- demote face/eyes to small bright accents
- simplify dragon, cloak, blood, signs, or texture if they hide scale witnesses

Adding more ratio prose without changing shot class is not a valid repair.
