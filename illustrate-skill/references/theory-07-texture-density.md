# THEORY_07_TEXTURE_DENSITY

Summary: This theory controls texture and information density in the final stage so the image feels finished rather than flat or randomly noisy. It decides where the image should stay smooth, where it should become rough, and how density supports focus.

Summary: Step 7 must define texture behavior for skin, clothing, background, and fragments, divide the image into density zones, control global/local grain, and place labels or symbols without competing with the face.

## Purpose

그림의 마지막 단계에서 재질감, 노이즈, 파편, 라벨/기호를 이용해 화면 밀도를 조절하고 완성도를 높인다.
질감을 무작정 얹지 않고, 어디를 매끈하게 두고 어디를 거칠게 만들지 의도적으로 결정하는 것이 목표다.

이 단계에서 먼저 결정해야 하는 것:

- 피부 / 의상 / 배경 / 파편 각각에 어떤 질감을 줄지
- 어디를 고밀도 / 중밀도 / 저밀도로 둘지
- 그레인 / 노이즈를 어느 강도로, 어느 범위에 적용할지

## Basic concepts

### Texture

질감은 브러시 스트로크, 노이즈, 패턴, 표면 거칠기/매끈함으로 느껴지는 시각적 표면 특성이다.

- soft texture -> skin, haze, soft light
- rough texture -> concrete, stone, scratched metal, dust
- patterned texture -> cloth weave, tile, wall pattern

### Image density

화면 밀도는 단위 면적당 정보량이다.

- high density -> more detail, texture, labels, fragments
- low density -> simpler shapes and rest space

기본 규칙:

- focal area -> high density
- near-support areas -> medium density
- outer frame / unimportant areas -> low density

## Part-based texture strategy

### Skin

목표:

- soft, clean, alive
- not plastic-smooth
- integrated into the scene light and shadow

규칙:

- only very light noise or color variation
- slight texture can live around nose, cheek, forehead transitions
- avoid strong grain, scratch, or rough brush damage on skin
- avoid AI-like glass, porcelain, wax, airbrushed doll, or plastic beauty rendering
- preserve small natural value shifts from hair shadow, eyelids, nose plane, mouth tension, pipe/prop shadow, and surrounding dark background
- the face may be cleaner than clothing/background, but it must not look separately retouched or pasted on top

### Clothing and accessories

목표:

- separate material types
- carry story and worldbuilding

규칙:

- cloth -> directional brush texture and fold emphasis
- metal -> hard highlights, scratches, reflected light
- decoration -> increase density, but do not exceed the face

### Background / fragments / environment

목표:

- support the figure
- control the scene's overall density

규칙:

- near background can hold medium texture
- far background should simplify in value and texture
- fragments, ribbons, dust, and noise are useful carriers but must remain organized

## Grain and noise theory

### Global grain

약한 전체 그레인은 디지털 밋밋함을 줄이고 필름 같은 통일감을 준다.

규칙:

- keep opacity low
- if grain reads before the image content, it is too strong
- dark regions are especially sensitive to dirty-looking overgrain

### Local grain / texture

부분적인 강한 노이즈는 구조와 재질을 강화할 수 있다.

규칙:

- stronger grain belongs more to clothing, background, and shadow zones
- face and skin should be masked away from heavy grain
- if grain implies light scatter, align it with the light direction and color

## Labels, symbols, and text fragments

작은 텍스트, 숫자, 경고 코드, 심벌은 세계관 정보와 화면 밀도를 동시에 높인다.

규칙:

- place them on edges, empty areas, object surfaces, or secondary support zones
- keep them small and fragmentary
- do not place readable text in a way that competes with the face

## Density zoning

### High / medium / low density regions

Step 7 should divide the image into:

- high density
- medium density
- low density

기본 규칙:

- no more than 1-2 high-density zones in a single image
- low-density zones are necessary so the image can breathe

### Detail projection

디테일은 보통 얼굴에서 시작해 손, 목, 소품 쪽으로 점차 약해진다.

규칙:

- allow the face and immediate support objects to carry the most information
- keep most of the distant background simplified

## Brush and layer guidance

도구적 기준:

- texture brushes -> clothing, background, fragment zones
- soft brushes -> skin, glow, atmospheric blend
- overlay / soft light -> texture fused with color
- multiply / screen -> texture pushed into shadow or light behavior

규칙:

- prefer a few controlled texture layers over many stacked noisy layers
- use masking to protect face and skin from over-texturing

## Step 7 execution summary

1. Divide the image into high / medium / low density zones.
2. Define texture strategy by part:
   - skin
   - clothing / accessories
   - background / fragments
3. Add a low-intensity global grain if it improves cohesion.
4. Add stronger local texture only where needed:
   - clothing
   - background
   - fragments
5. Place a limited number of labels, symbols, or text fragments.
6. Mask or reduce texture around the face and eye zone.
7. Check that skin remains soft but alive: not noisy, not waxy, not porcelain, not plastic, and still affected by the scene's shadows.
8. Check the image at reduced size and confirm that density is organized, not chaotic.

## Gate

Do not continue to Step 8 unless all are true:

- skin remains softer than clothing and background
- skin has subtle living variation and belongs to the same light environment as hair, props, and background
- skin does not read as AI plastic, glass, porcelain, wax, or over-airbrushed doll surface
- global grain supports the image without obscuring information
- high / medium / low density zones are clearly differentiated
- labels and symbols support worldbuilding without stealing focus
- when reduced in size, the texture reads as organized noise rather than clutter

If any item fails, revise texture strength, placement, or density distribution first.
