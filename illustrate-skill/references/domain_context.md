# Domain Context

Summary: This skill is being built for a Korean-speaking user who wants a reusable illustration SOP skill. The process skeleton and the theory library must stay separate. Theories are stored as individual files and mapped to steps, not flattened into one generic note.

Summary: The skill should support theory-first planning, critique, and skill extension. It should be able to consume user-authored theory blocks, clean hyperlink residue, preserve intent, and apply the theory before each stage executes.

## User context

- User language in conversation: Korean
- Skill body preference: English procedure, Korean trigger coverage
- Primary goal: make a Claude-style skill for illustration workflow design and staged art reasoning
- Secondary goal: keep the skill expandable as more theories are added

## Workflow expectations

- Process is the main execution skeleton.
- Theories are separate modules attached to process steps.
- Before a step runs, the relevant theory must be read and turned into decision rules.
- If a theory gate fails, the process must stop and revise that step instead of pushing forward.
- If object knowledge is insufficient for background props, structures, or machinery, hand off to `object-research-skill` after Step 2 blocking and resume with object-informed revision before Step 3.

## Workspace style context

When the user asks for the workspace reference style, read `style-guide.md`.

Current style signals:

- sharp variable line weight
- dark, textured backgrounds
- high contrast around eyes and face
- restrained expressions
- crystalline eye highlights
- rough black accents in clothing and background
- accent colors concentrated in red, teal, purple, or white light

## Related skill boundary

- `illustrate-skill`: full-scene illustration planning and critique
- `object-research-skill`: object lookup, object research, object-card updates, and scene-recipe building

## Extension rules

- Each new theory becomes its own file in `references/`.
- The process file should point to the theory file by name.
- Do not collapse theory files into one monolithic reference.
- Ignore broken hyperlink residue unless it changes meaning.
