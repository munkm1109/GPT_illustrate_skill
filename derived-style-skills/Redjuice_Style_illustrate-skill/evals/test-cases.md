# Test Cases

Use these cases to verify the reference-derived wrapper after any change to:

- `SKILL.md`
- `references/style-pack.md`
- `references/reference-index.md`
- `references/line-plane-intent-analysis.md`

For critique-oriented checks, always record both:

- `User Verdict`
- `System Diagnostic`

The user verdict is primary.
The system diagnostic explains agreement, tension, and next move.

## Trigger / routing coverage

1. `고딕 사이버 분위기의 인물 일러스트를 설계해줘. 얼굴은 절제되고, 배경은 유리창과 결정, 붉은 악센트가 있는 의식 공간이면 좋겠어.`
   - Expected skill: `Redjuice_Style_illustrate-skill`
   - Expected mode: `SPEC`
   - Expected refs:
     - base `illustrate-skill` process
     - derived `style-pack.md`
     - derived `domain_context.md`

2. `차갑고 정적인 표정, 얼굴 초점, 온실+수조+네온 간판이 함께 있는 wide scene으로 잡아줘.`
   - Expected skill: `Redjuice_Style_illustrate-skill`
   - Expected mode: `SPEC`
   - Expected behavior:
     - environment density should be treated as mandatory, not optional decoration
     - Step 2.5 object research likely required

3. `이 결과가 너무 GPT풍이야. 이 레퍼런스 기반 스타일 래퍼 기준으로 어디서 generic해졌는지 봐줘.`
   - Expected skill: `Redjuice_Style_illustrate-skill`
   - Expected mode: `CRITIQUE`
   - Expected behavior:
     - anti-generic drift diagnosis should be front-loaded

## SPEC pass-shape cases

### Case A — ritual symmetry

Prompt:
`월식 같은 원형 광원과 왕좌, 검은 드레스, 붉은 포인트가 있는 정면 대칭 인물 장면을 설계해줘.`

Expected:
- Step 1 intent includes sealed emotion or ritual authority
- Step 2 uses symmetry or controlled ceremonial pressure
- Step 3 uses dark surround + bright focal face logic
- Step 6 keeps palette narrow, not rainbow
- Step 8 rejects generic empty background solutions

### Case B — synthetic greenhouse

Prompt:
`온실과 수조, 경고 라벨, 형광 프레임 조명, 식물과 유리 반사가 많은 장면으로 설계해줘.`

Expected:
- environment treated as emotional machinery
- Step 2.5 object research likely required
- Step 7 texture separates skin from glass / plant / signage density
- reduced-size read still holds on the face

### Case C — line-first monochrome portrait

Prompt:
`흑백 스케치 기반으로도 긴장감이 살아 있는 초상을 설계해줘. 색보다 선과 면 분해가 핵심이야.`

Expected:
- line-plane-intent-analysis is relevant
- Step 5 line hierarchy carries the style before color
- Step 6 does not invent unnecessary rainbow accent logic

## CRITIQUE coverage

### Case D — user says success, system adds tension

Prompt:
`나는 이 결과를 성공이라고 보는데, 네가 보기엔 어디가 generic한지 이 파생 스킬 기준으로만 말해줘.`

Expected output shape:
- `User Verdict: success`
- `System Diagnostic`
  - intent
  - process
  - readability
  - delivery
- `Agreement / Tension`
- `Next Move`

Expected diagnostic focus:
- background pressure system
- face anchor strength
- accent clustering
- line-weight separation

### Case E — user says failure because it looks too normal

Prompt:
`이건 예쁘긴 한데 너무 평범해. 왜 이 reference-derived wrapper 기준에서 실패인지 말해줘.`

Expected:
- system should avoid vague “more details needed”
- should name specific failure classes such as:
  - empty background
  - under-framed silhouette
  - uniform polish
  - weak accent discipline

## Anti-generic drift checks

### Case F — blur-background drift

Failure shape:
- single character
- soft bloom
- vague background blur
- no meaningful architecture / shards / signage / frame

Expected diagnostic:
- background pressure absent
- default poster crop
- environment not functioning as narrative machinery

### Case G — uniform-surface drift

Failure shape:
- skin, clothing, and background all rendered with the same soft finish

Expected diagnostic:
- material separation failure
- texture-density hierarchy collapse

### Case H — accent spread drift

Failure shape:
- red, cyan, purple, and white glows scattered evenly across the whole image

Expected diagnostic:
- accent clustering failure
- face no longer wins the color hierarchy

### Case I — cute-face drift

Failure shape:
- overly cute, generic anime face
- large mouth acting
- weak iris structure

Expected diagnostic:
- restrained facial psychology lost
- face temperature no longer matches the reference pack

## Object-research dependent cases

### Case J — aquarium / greenhouse interior

Prompt:
`온실 수조, 유리 프레임, 식물, 경고 라벨, 천장 구조물이 모두 보이는 wide shot을 스펙으로 짜줘.`

Expected:
- Step 2.5 object research strongly recommended or required
- validator should warn/fail if handoff is skipped without justification

### Case K — throne / parasol / palace-window scene

Prompt:
`왕좌, 파라솔, 창문 구조, 꽃 장식이 모두 있는 정적인 인물 장면을 설계해줘.`

Expected:
- object research may be required if the structures are treated concretely
- composition should not collapse into simple center portrait with symbolic words only

## Source-image upgrade cases

### Case L — preserve original object identity

Prompt:
`원본 이미지의 온실 프레임, 간판, 유리 수조를 유지하면서 이 reference-derived wrapper 방향으로 업그레이드해줘.`

Expected:
- original objects listed before Step 2.5 decision
- object research starts from recognized source objects
- output preserves object identity while upgrading line / plane / pressure

### Case M — fail if style hides bad structure

Failure shape:
- source image contains complex signage / glass / props
- spec tries to hide uncertainty with glow, particles, or blur

Expected diagnostic:
- weak object understanding cannot be masked by atmosphere

## Reference-pack fidelity checks

### Case N — ritual authority lane

Target traits:
- eclipse / halo pressure
- throne / wing / ceremony framing
- stillness as force

Expected:
- scene reads as controlled authority, not casual fantasy glamour

### Case O — cyber-organic lane

Target traits:
- greenhouse / aquarium / signage / industrial frame
- life + machine collision

Expected:
- environment should feel designed and story-bearing, not wallpaper

### Case P — fracture lane

Target traits:
- shards
- black mass
- white cutting planes
- restrained face inside violent structure

Expected:
- scene keeps face-first hierarchy despite aggressive planes

## Regression checks

1. The wrapper must still preserve the base `illustrate-skill` staged workflow.
2. The wrapper must not instruct direct living-artist imitation.
3. The wrapper must remain usable as a reference-derived style pack, not just a folder of aesthetic adjectives.
