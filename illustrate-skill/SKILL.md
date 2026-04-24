---
name: illustrate-skill
description: Plan, specify, critique, and extend illustration work with a theory-first SOP: intent, composition, value, face, line, color, texture, and final check. Use this skill whenever the user asks to design an illustration, break a scene into staged art decisions, apply drawing theory before execution, refine an illustration workflow, or add new illustration theory blocks. Trigger phrases include "일러스트 그려줘", "그림 구도 잡아줘", "이론 기반으로 일러스트 설계해줘", "장면 의도부터 정리해줘", "이 그림 프로세스로 분석해줘", "구도랑 명암 구조 짜줘", "illustration workflow", "gothic portrait composition". Also trigger when the user provides mood/scene keywords, theory blocks, or reference-driven art direction and wants a staged illustration spec without explicitly naming the skill. Prefer this skill over imagegen when the user needs theory-driven planning, critique, workflow design, or stage-by-stage reasoning before any final image generation. Prefer this skill over object-research-skill when the user wants full-scene planning rather than isolated object lookup or object-library work.
---

# Illustrate Skill

Use this skill as a theory-first SOP folder for illustration planning and critique.
Keep procedure in this file. Load domain knowledge from `references/` only when needed.

## Default load order

1. Read `references/domain_context.md`.
2. Read `references/main-process.md`.
3. Read only the theory files needed for the active step.
4. Read `references/style-guide.md` when the task needs the workspace reference style.
5. If background, prop, age-band anatomy, sex-classification anatomy, or visible hand/finger knowledge is insufficient after Step 2 / Step 2.3 blocking, load `object-research-skill` and follow its SOP before resuming this workflow.

## Modes

Pick one mode explicitly.

- `SPEC`: turn user intent or keywords into a staged illustration spec
- `CRITIQUE`: review an existing illustration, prompt, or plan against the staged process
- `EXTEND`: add or rewrite theory blocks and update the process mapping

If the user mixes modes, do the blocking mode first:

- missing scene definition -> `SPEC`
- existing image or plan review -> `CRITIQUE`
- skill structure or theory library changes -> `EXTEND`

If the user's real task is **creating a new style-specific wrapper skill from reference images/folders**, do not continue as normal `SPEC`.
Hand off to `reference-copy-skill` first.

## SPEC mode

1. Capture the user's scene, mood, constraints, and deliverable.
2. For any SPEC run that is intended to reach final rendering or image generation, start from `templates/illustrate-spec-template.md` and write into a working spec artifact before Step 1. Use a path such as `.omx/runs/<timestamp>-<slug>-spec.md` or another user-requested location.
3. Create a theory-read proof artifact from `templates/theory-read-proof-template.md`, record its path in `THEORY_READ_PROOF_PATH`, and keep it updated during the run.
4. Read the relevant step theory before each step and record the read in the proof artifact, preferably via `python scripts/record_theory_read.py <proof-path> <step> <file> ...`.
5. Run the structural preflight before any value, face, line, color, texture, or image-generation work:
   - Step 2: composition and object-role summary
   - Step 2.1: perspective rig / horizon / vanishing points / support planes / scale anchors
   - Step 2.2: perspective-plane object inventory
   - Step 2.3: anatomy as object inventory plus anatomy structure gate
   - Step 2.4: object-knowledge query plan by lane
   - Step 2.5: object-research handoff when needed
   - Step 2.6: object relationship check
   - Step 2.7: anatomy-on-object relationship check
   - Step 2.8: 3D blockout / modeling contract, including geometric blockout lock
   - Step 2.9: image translation lock, including detail-after-blockout priority
6. If the task is an upgrade or repaint of a user-provided source image, identify the concrete objects already present in the source image before finalizing Step 2.2. Separate them into:
   - primary retained objects
   - structurally clear objects
   - structurally uncertain objects
7. List background objects by perspective plane, not as generic atmosphere:
   - support / ground / track plane
   - left vertical plane
   - right vertical plane
   - overhead plane
   - foreground frame
   - background depth
   - effects
   - text / glyph objects
8. Treat the human figure as an object stack in Step 2.3:
   - primary anatomy object
   - anatomy sub-objects
   - anatomy contact objects
   - anatomy scale relationships to supports, props, and vehicles
9. For source-image upgrade runs, also identify any visible hands, gripping poses, finger silhouettes, or hand-held props that are important to the scene read.
10. For source-image upgrade runs, prefer Step 2.5 object research on the recognized source-image objects whenever their structure, material, scale, perspective role, or style-critical construction would benefit from confirmation, even if the objects are already visible in the source image.
11. If the scene shows a meaningful amount of human figure information beyond a close face crop, run the Step 2.3 anatomy structure gate before Step 2.5. Lock age band, sex classification, proportion logic, and limb-chain logic before treating hands as a local problem.
12. If hands or fingers are visible and they are focal, close to camera, expressive, foreshortened, or holding a prop/weapon, treat them as an anatomy submodule under the Step 2.3 body decision, not as a free-floating object guess.
13. For anatomy-gated scenes, default toward Step 2.5 lookup / research of:
   - one age-band body base card
   - one sex-classification overlay card
   - the hand anatomy submodule
   before trusting raw model intuition.
14. For structurally important scenes, Step 2.4 must plan object research in separate lanes:
   - anatomy
   - core scale anchors
   - hard-surface background / architecture
   - weapon / prop
   - effects / text
15. Unknown object policy:
   - If an object cannot be named, functionally defined, placed on a plane, or assigned a relationship, do not convert it into random texture, fake signage, fake machinery, or unidentified pattern.
   - Resolve it by asking the user, researching it, removing it, replacing it with a known object, intentionally abstracting it with a declared function, or stopping the render-bound flow.
16. Blender / ControlNet hard-route policy:
   - Use Blender for every render-bound SPEC run. Do not treat Blender as conditional for final illustration or image-generation handoffs.
   - Set `BLENDER_BLOCKOUT_REQUIRED: yes` for all render-bound SPEC artifacts, including simple portraits; lower-complexity scenes may use a minimal camera/plane/mannequin blockout, but they still need Blender evidence.
   - When `BLENDER_BLOCKOUT_REQUIRED: yes`, create or reference a `.blend` file and a Blender Python render script before Step 3.
   - Render at least a clay/solid pass and one structure pass usable for conditioning or review: lineart/wire, depth, normal, or mask.
   - Record the `.blend`, render script, pass outputs, visual review, and downstream ControlNet/img2img plan in Step 2.8.
   - Treat Blender as structural evidence, not as the final aesthetic authority. The default handoff is a **loose guide**: preserve camera, support/contact, scale anchors, perspective size relationships, adult/sex/age scale logic, and major silhouettes, but allow painterly compression, partial occlusion, and dark massing when those improve the illustration.
   - Do not let later style, value, line, color, or texture stages override the approved Blender camera, contact points, support planes, scale anchors, or named non-negotiable object relationships.
   - Do not let Blender harden the final image into a CAD-like, plastic, over-explained, or mannequin-like composition when the user’s target is painterly, editorial, anime, symbolic, or mood-first.
   - Do not express power hierarchy by making the ruler physically larger than perspective, anatomy, or adult male/female scale logic allows. For commercial illustration, show authority through staging, framing, value, gesture, costume, eye line, camera height, and detail priority rather than hieratic body-size distortion unless the user explicitly asks for symbolic scale.
   - If Blender is installed locally, prefer background rendering through the discovered `blender.exe` path; if unavailable, ask for/export viewport renders rather than pretending the `.blend` was reviewed.
17. User checkpoints:
   - Checkpoint A after perspective rig / composition direction when the view can branch.
   - Checkpoint B after unknown-object triage or object query when naming / replacement decisions are needed.
   - Checkpoint C after 3D blockout when scale, contact, or support logic can branch.
   - Checkpoint D before image generation when structure is locked and later corrections would be expensive.
   - If the choice is obvious and non-branching, record the assumed direction in the checkpoint field; if it is materially branching, ask the user before continuing.
18. Execute the stages in `references/main-process.md` in order unless the user explicitly scopes the task to a subset of stages.
19. Fill the stage results under clear headings and template fields, not just summary prose:
   - intent
   - silhouette/composition
   - perspective rig
   - object inventory from perspective
   - anatomy structure gate
   - anatomy primitive blockout
   - object knowledge query plan
   - object research handoff, if needed
   - object relationship check
   - anatomy-on-object relationship check
   - 3D blockout / modeling contract
   - Blender blockout artifacts and pass outputs when required
   - shared perspective / scale lock
   - detail-after-blockout lock
   - image translation lock
   - value
   - face
   - line/shape
   - color/accent
   - texture
   - final check
20. If background objects, props, furniture, machinery, weapons, signage, vehicles, architectural structures, source-image upgrade objects, visible hands/fingers, or anatomy-gated human figure structures need believable form, hand off to `object-research-skill` after Step 2.4 and before Step 2.6.
21. When Step 2.5 is required for a render-bound scene, create an object-research artifact from `templates/object-research-artifact-template.md` and record its path in the spec field `OBJECT_RESEARCH_ARTIFACT_PATH`.
22. After the object-research handoff, revise object scale, perspective locks, inter-object contact, body structure, limb-chain logic, hand/finger grouping, and material planning before continuing to value design.
23. If the user requests the workspace reference look, read `references/style-guide.md`, record that read in the proof artifact, and fold its rules into the stage decisions only after structure locks remain readable.
24. Before treating the spec as complete, run `python scripts/validate_illustrate_spec.py <spec-path> --strict-object-research`.
25. If the validator fails, revise the failed sections instead of skipping forward.
26. Before any final render handoff, run `python scripts/run_illustrate_pipeline.py <spec-path> --strict-object-research`.
27. If the user ultimately wants an image render, finish the theory-driven spec first, pass validation and the pipeline runner, then hand off to image generation.

## CRITIQUE mode

1. Identify what artifact is being reviewed: illustration, prompt, process document, or stage output.
2. Read `references/main-process.md`.
3. Evaluate the artifact stage by stage against the process.
4. If a step has a mapped theory file, read it before judging that step.
5. Treat the user's verdict as the primary success/failure label whenever the user provides one.
6. Report findings in process order. Be explicit about what is missing, weak, or contradictory.
7. Structure the output as:
   - `User Verdict`
   - `System Read`
     - `intent`
     - `process`
     - `readability`
     - `delivery`
   - `Agreement / Tension`
   - `Next Move`
8. Recommend corrections as concrete edits, not vague advice.

## EXTEND mode

1. Treat each user-provided theory as an individual unit, not as a paragraph to merge into a generic step summary.
2. Clean formatting noise such as broken hyperlink residue, but do not discard semantic content.
3. Save each theory as its own file in `references/` using a stable name such as `theory-01-intent.md`.
4. Update `references/main-process.md` so the affected step points to the new theory file.
5. If the new theory changes how the skill should activate or route, update this `SKILL.md`.
6. Preserve the rule that process is the skeleton and theories are attached modules.

## Working rules

- Run the process as `theory -> decision rule -> execution -> output -> gate`.
- If the user asks to derive or generate a **new illustration style skill** from references, stop treating the task as scene planning and route to `reference-copy-skill`.
- Do not skip a gate just because the likely answer feels obvious.
- Do not claim that SPEC mode was completed correctly if the required stage fields are missing from the working artifact.
- For render-bound SPEC runs, do not jump directly from the raw user prompt to image generation.
- For source-image upgrade runs, inspect and list the objects already present in the original image before deciding whether Step 2.5 is needed.
- For source-image upgrade runs, default toward researching the recognized original-image objects when that improves structural clarity, material believability, or style-faithful reinterpretation.
- Perspective comes before background detail: establish horizon, vanishing points, support planes, contact planes, and scale anchors before listing dense city / rail / architecture detail.
- Background object lists must be plane-aware. Do not write only “city detail” or “pressure frame” when the scene depends on buildings, rail structures, signage, glass, cables, vehicles, or architecture.
- Human anatomy is also an object stack. List the body, hands, feet, contact points, and prop relations as anatomy objects before value or style work.
- Unknown or weakly named objects must go through triage: ask, research, remove, replace with a known object, intentionally abstract with declared function, or stop. Never fake them as random pattern/noise.
- Object research must return draw-ready locks by lane: matched cards, missing/weak cards, scale/perspective locks, relationship notes, and generation prompt locks.
- Step 2.6 must check object-object scale, occlusion, contact/support, collision, material/light interaction, rigid geometry, and text/glyph policy.
- Step 2.7 must check anatomy on top of objects: support, hand-prop relation, foot-surface relation, torso action relation, and fail conditions.
- Step 2.8 must express the scene as primitive 3D/blockout forms before image translation. For render-bound SPEC runs, real Blender output is mandatory, not optional.
- Blender hard-route is mandatory for every render-bound SPEC: the spec must include `BLENDER_BLOCKOUT_REQUIRED: yes`, a `.blend` path, render script path, pass output paths, visual review result, and ControlNet/img2img conditioning plan before Step 3.
- Blender hard-route does not replace Step 2.1-2.7; it consumes their perspective, object, anatomy, and relationship locks and turns them into a reviewable/conditionable blockout.
- Blender hard-route is an evidence route, not a rigidity route: Step 2.8 must explicitly separate `STRUCTURAL_INVARIANTS_TO_PRESERVE` from `PAINTERLY_FREEDOMS_ALLOWED`, so the final handoff can use Blender as a loose guide when appropriate.
- For scenes with full-body, humanoid, creature, architecture, vehicles, rooftops, streets, props, weapons, or strong perspective, Step 2.8 must use constructive geometric blockout: environment primitives and anatomy primitives must share one perspective grid and one scale system before detail is allowed.
- Human anatomy must be blockout-first when the body read matters: head sphere / box, ribcage box or barrel, pelvis box, limb cylinder chains, sphere joints, hand blocks / thumb wedges / grouped finger cylinders, and foot wedges on the support plane.
- Environment structure must also be blockout-first: slabs, boxes, planes, grids, mounted rectangles, support surfaces, facade modules, and scale anchors must be named before dense city, texture, signage, glow, or atmospheric detail.
- Detail must follow the locked blockout where the blockout solves contact, support, scale, and named object relationships. Face, costume, hair, fur, smoke, glow, motion effects, line style, color accents, and texture are not allowed to resize the figure, hide broken limb chains, shrink architectural modules, or replace rigid object geometry.
- Painterly compression is allowed after structure when it does not break support/contact/scale: crowds may merge into readable dark masses, stairs may compress for drama, background forms may subordinate to mood, and ornate detail may soften rigid block edges.
- Painterly compression must not shrink foreground adults into decorative markers, override real perspective size, or use hieratic/symbolic body-size exaggeration to show authority unless explicitly requested.
- For architecture-scale scenes with figures, Step 2.8 must explicitly check body-to-architecture scale: window-to-head size, parapet/railing-to-body height, footprint on the support plane, and whether foreground enlargement is matched by nearby foreground anchors.
- Step 2.9 must lock image-generation priority order and non-negotiable structure before style density is allowed.
- Step 2.9 must state that primitive blockout, perspective, contact, and scale are solved before face, costume, lighting, color, texture, or decorative detail.
- Step 2.9 must state the Blender conditioning strength: `loose guide`, `medium guide`, or `strict guide`. Default to `loose guide` for painterly/editorial/anime/image-generation handoffs unless the user asks for technical precision, product accuracy, orthographic consistency, or a mechanically exact scene.
- Step 2.9 must explicitly lock `NO_HIERATIC_SCALE_DISTORTION` for commercial illustration scenes with human figures: foreground adult men may appear larger in screen space than a farther seated woman when perspective requires it, while still remaining lower-detail and subordinate by value/composition.
- For human figure scenes that show more than a close face crop, run Step 2.3 anatomy structure gating before Step 3.
- Step 2.3 must lock an age-band body base, a sex-classification read, a temporary default body-type baseline, and the hand submodule relationship before hand rendering decisions are trusted.
- For visible hands and fingers, especially focal hands, expressive gestures, foreshortened poses, or prop-holding grips, default toward Step 2.5 as an anatomy submodule lookup instead of guessing.
- For structurally uncertain background objects, complex props, machinery, signage, vehicles, or architecture, default toward Step 2.5 instead of guessing.
- For grounded full-body or standing poses, Step 2.3 must include support-leg, balance-line, and shoulder/pelvis logic that explains why the pose is physically supportable.
- For anatomy-gated scenes, Step 2.5 should return the anatomy references that Step 2.7 will apply: age-band body base, sex overlay, and hand submodule when hands matter.
- For visible hands that materially affect silhouette or storytelling, Step 2.3 must include a hand silhouette read and a finger-grouping note before Step 3.
- When Step 2.5 is needed, Step 2.6 and Step 2.7 are mandatory before Step 3.
- When Step 2.5 is needed for a render-bound scene, the object-research artifact path must exist before final completion.
- The theory-read proof must exist and cover every required step theory before final completion.
- In CRITIQUE mode, the user owns the primary verdict and the system adds a diagnostic layer rather than overruling it.
- Keep style knowledge out of this file; point to `references/style-guide.md`.
- Keep user-specific context out of this file; point to `references/domain_context.md`.
- If the user gives a new theory in Korean, it is acceptable for the reference file to stay close to the user's original meaning while the process file remains English.
- If the user asks only for one stage, still state what upstream assumptions you inherited.

## Required SPEC artifact

For full-scene SPEC runs that are meant to drive rendering:

1. Create or update a spec file from `templates/illustrate-spec-template.md`.
2. Create or update a proof file from `templates/theory-read-proof-template.md` and record its path in the spec.
3. Fill all global fields plus every required step field.
4. If Step 2.5 is required, create an object-research artifact from `templates/object-research-artifact-template.md` and record its path in the spec.
5. Mark gate status explicitly per step.
6. Run `scripts/validate_illustrate_spec.py` before claiming completion.
7. Run `scripts/run_illustrate_pipeline.py` before any image-generation handoff.
8. Keep validator / pipeline output as part of the verification trail.

## Outputs

Prefer concise, production-usable outputs:

- one-line scene intent
- composition map
- value plan
- facial focal rules
- line and shape hierarchy
- palette and accent plan
- texture density plan
- final gate verdict

When extending the skill, list changed files and the new theory-to-step mapping.
