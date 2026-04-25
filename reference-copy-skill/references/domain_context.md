# Domain Context

Summary: This skill exists so the user can keep `illustrate-skill` as the stable original method while generating new reference-derived wrapper skills from local reference sets.

Summary: The generated wrapper should not replace the base skill. It should load the base process and specialize it with a local style pack derived from the provided references.

## Rules

- Base skill to preserve: `illustrate-skill`
- Output location for derivatives: `derived-style-skills/`
- The derivative skill should remain compatible with the base process structure
- Style-specific knowledge should live in the derivative skill's `references/`, not be merged into the base skill

## User goal

The user wants to:

- interpret and analyze a local reference set
- extract a coherent style system from that set
- turn that extracted style into a reusable new skill
- keep the original illustration process unchanged

## Design stance

The derivative skill should act as:

- base process loader
- style pack applicator
- optional style-specific reference interpreter

It should not become a monolithic fork unless the user explicitly prefers a full replacement.
