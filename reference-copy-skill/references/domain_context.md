# Domain Context

Summary: This skill exists so the user can keep `illustrate-skill` as the stable original method while generating new reference-derived wrapper skills from local reference sets.

Summary: The generated wrapper should not replace the base skill. It should load the base process and specialize it with a local style pack derived from the provided references.

## Project reference assumption

Unless the user says otherwise, reference folders in this project should be treated as user-provided AI-generated style-study outputs rather than original artist source images. Do not stall the workflow on direct artist-source imitation concerns under this default. Still translate references into reusable visual grammar and suppress overfit, one-image copying, and accidental AI artifacts.

## Rules

- Base skill to preserve: `illustrate-skill`
- Output location for derivatives: `derived-style-skills/`
- The derivative skill should remain compatible with the base process structure
- Style-specific knowledge should live in the derivative skill's `references/`, not be merged into the base skill
- Style wrappers should feed the base final-prompt compiler with compact aesthetic render language, not raw analysis fields
- Style wrappers must not weaken camera, perspective, scale, object-research, source-image, composite, or image-generation handoff locks

## User goal

The user wants to:

- interpret and analyze a local reference set
- extract a coherent style system from that set
- turn that extracted style into a reusable new skill
- keep the original illustration process unchanged
- use style references as rendering grammar while preserving structure-critical scene controls

## Design stance

The derivative skill should act as:

- base process loader
- style pack applicator
- aesthetic render brief provider
- optional style-specific reference interpreter

It should not become a monolithic fork unless the user explicitly prefers a full replacement.
