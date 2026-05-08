# Derived Skill Structure

Summary: A derivative style skill should be a thin wrapper around the base illustration process, not a destructive fork. This preserves the original skill and keeps future maintenance manageable.

## Recommended structure

```text
derived-style-skills/
  <slug>/
    SKILL.md
    references/
      domain_context.md
      style-pack.md
      reference-index.md
      optional deep-analysis.md
```

## Derivative SKILL.md responsibilities

- define trigger phrases for the specific reference-derived wrapper
- tell the agent to:
  1. read the base process from `illustrate-skill/references/main-process.md`
  2. read the local style pack
  3. apply the wrapper's `AESTHETIC_RENDER_BRIEF` only after the base scene structure is locked
  4. execute the base steps through the lens of the local style pack
- explicitly say the base process is preserved
- explicitly say style never overrides camera, perspective, object research, source-image, scale, visual-guide-composite, or handoff locks

## style-pack.md responsibilities

Store style-specific rules aligned to the base process:

- AI reference provenance note
- reference style observation matrix
- style grammar extraction
- step 1 intent mood bias
- step 2 composition bias
- step 3 lighting/value bias
- step 4 face/emotion bias
- step 5 line/shape bias
- step 6 color/accent bias
- step 7 texture/density bias
- step 8 final-check differences
- aesthetic render brief
- style application boundary
- motifs
- do-not patterns
- anti-generic and anti-overfit drift constraints

## reference-index.md responsibilities

Store:

- what references were analyzed
- provenance note when known
- what each reference contributed
- confidence notes
- evidence vs inference vs production rule boundaries
- one-off details that should not become hard rules

## Why this structure

- base skill remains untouched
- derivative skill stays light
- style knowledge stays local to the derivative
- final prompts stay production-usable instead of analysis-heavy
- scale/perspective/composite locks remain compatible with any style wrapper
- the user can generate many wrappers without corrupting the core process
