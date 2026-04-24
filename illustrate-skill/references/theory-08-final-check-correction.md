# THEORY_08_FINAL_CHECK_CORRECTION

Summary: This theory provides the final quality gate before a piece is considered done. It checks whether intent, focus, value, color, face, texture, and output-readiness all point in the same direction.

Summary: Step 8 must verify the image in normal view, reduced-size view, and grayscale view, then apply final corrections instead of treating completion as a vague feeling.

## Purpose

1-7단계의 결과를 한 번에 재검토하고, 출력/공유 직전 퀄리티를 끌어올리는 마지막 게이트를 제공한다.
"끝낸 느낌"이 아니라, 의도·구도·값·색·질감이 모두 같은 방향을 보고 있는지 점검하는 것이 목표다.

이 단계에서 먼저 확인해야 하는 것:

- 이 그림이 지금 무엇을 보여주려 하는지
- 눈이 먼저 가는 곳이 맞는지
- 흑백 / 축소 / 색보정 관점에서 문제 없는지

## Global review principles

### Intent match

1단계의 장면 의도 문장을 다시 읽고 현재 그림과 비교한다.

질문:

- 이 그림만 봐도 그 감정과 상황이 드러나는가
- 단순히 예쁜 그림이 아니라, 그 순간의 한 컷처럼 느껴지는가

규칙:

- 애매하면 초점, 표정, 색, 구도 중 최소 하나를 수정해야 한다

### Focus and gaze flow

축소뷰와 흑백뷰에서 다시 본다.

질문:

- 눈이 가장 먼저 얼굴/눈으로 가는가
- 시선이 얼굴 -> 손/소품 -> 배경 순으로 자연스럽게 흐르는가
- 불필요한 디테일이나 색이 초점과 경쟁하고 있지 않은가

## Value check

흑백 모드에서 다시 본다.

점검:

- 얼굴/눈 주변이 가장 큰 명암 대비를 가진다
- 전체가 회색죽처럼 뭉개지지 않는다
- 덜 중요한 배경 요소는 값 대비가 더 낮다

수정 방향:

- curve / levels / local dodge-burn style correction
- focal contrast redistribution

## Color and tone correction

색 완성 후에도 마지막 톤 조정은 유효하다.

점검:

- 특정 색조로 과도하게 치우치지 않았는가
- 피부색이 베이스 톤과 충분히 분리되는가
- 포인트 컬러가 1-2개만 강하게 유지되는가

가능한 보정:

- color balance
- tone curve
- gradient map style global unification
- subtle highlight/shadow hue shift

## Face and eye final pass

얼굴은 마지막에 다시 봐야 하는 정답지다.

점검:

- Step 4 / 4A의 감정 패턴과 현재 얼굴이 일치하는가
- 눈의 디테일/대비가 다른 얼굴 부위보다 강한가
- 입과 눈썹은 여전히 절제되어 있는가

수정 방향:

- eye contrast increase
- iris highlight cleanup
- brow or mouth micro-angle adjustment

## Texture and density final pass

7단계가 과하거나 부족하지 않은지 판단한다.

점검:

- 피부/얼굴은 부드럽고 옷/배경은 상대적으로 거친가
- 그레인이 그림을 살리고 정보를 덮지 않는가
- 고밀도/저밀도 구역이 분명한가

수정 방향:

- texture opacity reduction
- mask cleanup near face
- density redistribution

## Output and medium check

필요할 때만 수행하지만, 명확한 출력 목적이 있으면 점검한다.

예:

- web resolution adequacy
- print resolution adequacy
- print color mode concerns
- tiny details disappearing at final size

## Self-feedback and archiving

완료 후 짧게 기록한다:

- 3 things that worked
- 3 things that should improve

정리:

- keep layered master
- keep export-ready output
- preserve references if they matter to future iteration

## Step 8 execution summary

1. Re-read the Step 1 intent sentence.
2. Compare the image against the intended story and mood.
3. Check reduced-size and grayscale views for focus and value stability.
4. Check color balance and accent control.
5. Recheck face, eyes, and emotional consistency.
6. Recheck texture, grain, and density zoning.
7. If relevant, verify output medium constraints.
8. Record brief self-feedback and archive-ready notes.

## Gate

The image is only complete if all are true:

- the intended feeling can be explained in one sentence from the image alone
- focus and mood survive reduced-size and grayscale checks
- value, color, and texture all support the face and eyes
- no competing color/detail/text steals focus from the face
- output settings are appropriate for the intended sharing medium

If any item fails, the image is not done.
