# Test Cases

Use these prompts to verify trigger coverage, validator behavior, and critique shape after each structural change.

For outcome reviews, record both:

- `User Verdict`
- `System Diagnostic`

The user verdict is primary.
The system diagnostic is a supporting read across intent / process / readability / delivery.

## SPEC trigger coverage

1. `차갑고 위험한 미소의 소녀를 네온 실험실 배경으로 설계해줘. 의도부터 구도, 명암, 얼굴까지 단계별로.`
   - Expected mode: `SPEC`
   - Expected refs: `domain_context.md`, `main-process.md`, `theory-01-intent.md`, `style-guide.md`
   - Validator focus: full staged output + workspace style proof

2. `매우 마른 전신 모델인데 과장된 상체 비율이 있는 패션 광고 장면을 스펙으로 짜줘.`
   - Expected mode: `SPEC`
   - Expected refs: Step 2 balance theories + style guide
   - Validator focus: support leg / balance line / shoulder-pelvis logic must be meaningful

3. `홍콩 골목, 네온 간판, 오토바이, 배수관, 젖은 바닥이 있는 장면을 렌더용 스펙으로 만들어줘.`
   - Expected mode: `SPEC`
   - Expected refs: Step 2 + Step 2.5 / 2.6
   - Validator focus: object-research should be required

4. `이 원본 이미지를 더 고급스럽게 다시 그릴 스펙을 짜줘. 원본의 간판, 유리창, 코트를 유지해야 해.`
   - Expected mode: `SPEC`
   - Expected refs: source-image object identification + Step 2.5 / 2.6
   - Validator focus: source-image objects must be listed before handoff choice

## CRITIQUE coverage

1. `이 그림 프로세스로 분석해줘. 지금 장면은 고딕 인물상인데 eyes first가 잘 안 살아.`
   - Expected mode: `CRITIQUE`
   - Expected refs: `domain_context.md`, `main-process.md`, `style-guide.md`
   - Output shape:
     - `User Verdict`
     - `System Read`
     - `Agreement / Tension`
     - `Next Move`

2. `나는 이 결과를 성공이라고 보는데, 너는 어디가 불안한지 process 기준으로만 말해줘.`
   - Expected mode: `CRITIQUE`
   - Expected behavior: user verdict stays primary; system may disagree only as diagnostic commentary

## Validator pass cases

1. Premium fashion ad spec with full-body standing pose
   - Should pass when:
     - Step 2 explicitly explains support logic
     - Step 3 names key light direction and 3-5 value grouping
     - Step 4 and Step 6 keep face/eyes first in the written logic

2. Complex environment spec with object-research artifact
   - Should pass when:
     - Step 2.5 artifact path exists
     - invocation log exists
     - Step 2.6 is `applied`

## Validator fail / warn cases

1. Full-body standing spec with empty or vague balance notes
   - Expected: fail

2. Step 3 without readable light direction or missing value count
   - Expected: fail

3. Step 6 accent map that never mentions face / eyes
   - Expected: fail

4. Step 8 correction list that contains only praise and no actionable edits
   - Expected: fail

5. Complex background keywords present but Step 2.5 says `HANDOFF_REQUIRED: no`
   - Expected: warn or fail depending on strict object-research mode

6. Source-image upgrade spec that does not list original-image objects
   - Expected: fail

## Style drift checks

1. Result gets too pastel or evenly clean
   - User Verdict: optional
   - System Diagnostic: should flag style drift against dark palette / variable ink / rough black accents

2. Background and character share the same texture density
   - User Verdict: optional
   - System Diagnostic: should flag texture separation failure

## Should not trigger

1. `이 사진 배경 지워줘.`
   - Better fit: image editing / image generation flow

2. `파이썬 타입 에러 고쳐줘.`
   - Better fit: coding or build-fix skills
