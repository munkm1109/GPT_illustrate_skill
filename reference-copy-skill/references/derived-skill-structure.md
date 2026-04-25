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
  3. execute the base steps through the lens of the local style pack
- explicitly say the base process is preserved

## style-pack.md responsibilities

Store style-specific rules aligned to the base process:

- step 1 intent mood bias
- step 2 composition bias
- step 3 lighting/value bias
- step 4 face/emotion bias
- step 5 line/shape bias
- step 6 color/accent bias
- step 7 texture/density bias
- step 8 final-check differences
- motifs
- do-not patterns
- anti-generic drift constraints

## reference-index.md responsibilities

Store:

- what references were analyzed
- what each reference contributed
- confidence notes
- evidence vs inference boundaries

## Why this structure

- base skill remains untouched
- derivative skill stays light
- style knowledge stays local to the derivative
- the user can generate many wrappers without corrupting the core process
