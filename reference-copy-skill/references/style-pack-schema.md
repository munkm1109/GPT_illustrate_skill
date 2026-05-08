# Style Pack Schema

Summary: A style pack is the local style brain for a derivative illustration wrapper. It should describe how the reference set bends or sharpens each base step without replacing the base process itself.

## Suggested structure

```text
# Style Pack

## Identity
- style label
- dominant feeling
- viewer effect

## AI Reference Provenance Note
- assumed source type
- confidence
- handling note

## Evidence Basis
- pixel-plane Markdown report
- pixel-plane JSON report
- visual-grammar synthesis
- reference count and batching note

## Diagnostic Pixel Bands
- value / bloom / dark-anchor behavior
- palette pools
- edge density / edge luma
- 3x3 composition pressure

## Reference Style Observation Matrix
| ref | observed trait | base step | evidence strength | production meaning |

## Style Grammar Extraction
- composition grammar
- value/light grammar
- face/eye grammar
- line/shape grammar
- color/accent grammar
- texture/density grammar

## Step Bias
### Step 1
### Step 2
### Step 3
### Step 4
### Step 5
### Step 6
### Step 7
### Step 8

## Aesthetic Render Brief
- compact production-facing style language

## Style Application Boundary
- style may affect
- style must not override

## Motifs

## Do Not

## Anti-generic and Anti-overfit Rules

## Evidence Notes
```

## Guidance

### Identity

Define:

- what this wrapper feels like
- what it emphasizes
- what it suppresses

### AI Reference Provenance Note

For this project, default to `user-provided AI style-study outputs` unless the user says otherwise. This lowers concern about direct source-image imitation, but does not remove the need to prevent overfitting to one reference or copying accidental artifacts.

### Reference Style Observation Matrix

Record observations as evidence rows. Each row should map the observation to a base illustration step and state whether it is weak, medium, or strong evidence. Use the pixel-plane report as the measured evidence floor, then add manual visual inspection.

### Evidence Basis and Diagnostic Pixel Bands

Every new/refined style pack should cite the pixel-plane report paths or explicitly state why measurement was not possible. Pixel-plane reports should be measured at source resolution unless the user explicitly asks for a fast approximation. Keep diagnostic bands concise. They are drift-check evidence for the wrapper, not image-prompt wording.

Use these sections for:

- measured value / bloom / dark-anchor ranges
- recurring palette pools and accent behavior
- measured edge density and edge hardness
- 3x3 composition pressure
- batch/merge notes for large folders

Do not convert raw pixel percentages into universal hard locks unless a separate segmentation or manual vision pass supports that rule.

### Style Grammar Extraction

Turn repeated observations into reusable production rules. Write grammar, not captions:

- how focal hierarchy is created
- how dark/light masses are arranged
- how line weight and edge hardness behave
- how accent color is rationed
- where texture density gathers or drops out

### Step Bias

For each base step, state:

- what to emphasize relative to the base skill
- what to reduce or avoid
- what recurring visual preference appears in the references

### Aesthetic Render Brief

Write compact natural image-generation language. Do not leak schema names, validator text, or research commentary into final prompt wording.

### Style Application Boundary

Make the boundary explicit: style can control rendering and mood, but cannot override scene requirements, source identity, object research, perspective math, camera class, scale hard locks, approved visual guide composite markers, or conditioning/handoff constraints.

### Motifs

Common repeating objects, framing devices, material tendencies, or symbolic patterns.

### Do Not

Patterns that would break the style, even if technically acceptable under the base process.

### Anti-generic and Anti-overfit Rules

List:

- default model drifts to resist
- signs that the wrapper has been overridden by another style family
- single-reference details that must not become hard rules
- AI artifacts that should be suppressed rather than learned

### Evidence Notes

State what came from pixel-plane measurement, what came from direct visual observation, what was inferred from repeated patterns, and what became a production rule.
