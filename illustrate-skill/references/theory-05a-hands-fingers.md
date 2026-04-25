# THEORY_05A_HANDS_FINGERS

Summary: This auxiliary Step 5 theory prevents hands from collapsing into mitten shapes or noodle fingers. It treats the hand as a small structural object with a palm block, thumb wedge, five individually modeled finger chains, and contact logic.

Summary: Use this theory whenever hands are visible, expressive, close to camera, holding props, or otherwise important enough that finger separation and grip logic must stay readable.

## Purpose

손과 손가락을 얼굴 다음으로 민감한 읽기 포인트로 다룬다.
특히 클로즈업 손, 소품을 쥔 손, 검/총/담배/파이프를 잡은 손, 화면 실루엣을 만드는 손은 `손목/손바닥 덩어리 -> 엄지 쐐기 -> 검지/중지/약지/새끼 각각의 독립 관절 체인` 순서로 구조를 잠가야 한다.

이 단계에서 먼저 결정해야 하는 것:

- 손이 화면에서 어떤 역할을 하는가
- 손바닥 덩어리와 엄지 방향이 어떻게 읽히는가
- 각 손가락이 손바닥 어느 지점에서 시작하고, 어떤 관절 체인과 접촉/겹침을 갖는가
- 접촉/압박이 있는지, 있다면 어디가 눌리는가

## Core principles

### Palm block first

손은 먼저 작은 얼굴처럼 디테일을 붙이는 것이 아니라, 손바닥 박스/쐐기 덩어리로 본다.

기본 규칙:

- 손바닥 덩어리 없이 손가락만 그리면 즉시 뭉개진다
- 손목 -> 손바닥 -> 엄지 기저부 -> 검지/중지/약지/새끼의 독립 체인 순서로 읽혀야 한다

### Thumb wedge is structural

엄지는 장식이 아니라 손의 방향을 결정하는 보강축이다.

규칙:

- 엄지의 시작점은 손바닥 옆면/앞면의 분명한 쐐기처럼 읽혀야 한다
- 엄지가 빠지면 손은 평평한 장갑처럼 보인다

### No finger grouping: individual finger-chain modeling

손가락은 절대 하나의 뭉친 그룹으로 대체하지 않는다.
오브젝트가 많거나 손이 작아도 손가락은 항상 인체 구조 우선으로 모델링한다.

기본 독립 체인:

- 엄지: 손바닥 옆면에서 시작하는 반대압 쐐기와 2-3 관절 방향
- 검지: 손잡이/제스처 방향을 읽히게 하는 독립 주도 체인
- 중지: 가장 긴 독립 체인, 힘을 가장 많이 받는 경우가 많음
- 약지: 중지와 비슷한 방향을 따라가더라도 실루엣과 관절은 분리
- 새끼: 가장 짧은 독립 체인, 작아도 손바닥 기저부와 끝점이 분리되어야 함

규칙:

- 축소뷰에서도 먼저 확인할 것은 “손가락이 뭉개지지 않고 각각 어디서 시작해 어디로 가는가”이다
- 모든 손가락 간격을 균일하게 벌리면 마네킹 손처럼 보이지만, 그렇다고 중지/약지/새끼를 한 덩어리로 합치면 안 된다
- 겹침과 가림은 허용하지만, 가려진 손가락도 시작점 / 압박 방향 / 끝점 중 최소 하나로 독립성이 암시되어야 한다
- 장갑, 혈흔, 소매, 검 손잡이, 장식선은 손가락 분리 구조를 덮는 핑계가 될 수 없다

## Proportion and rhythm

### Finger length flow

대체로:

- 중지가 가장 길다
- 검지와 약지는 그보다 약간 짧다
- 새끼는 확실히 짧다

규칙:

- 손가락 끝 높이가 계단형 리듬을 가져야 한다
- 네 손가락 끝이 한 줄에 서면 부자연스럽다

### Thickness taper

규칙:

- 손가락은 기저부가 더 두껍고 끝으로 갈수록 가늘어진다
- 마디마다 약간의 두께 변화가 있어야 한다
- 손끝을 끝까지 같은 굵기로 밀면 고무튜브처럼 보인다

### Knuckle cadence

규칙:

- 손등이 보이는 손에서는 손마디 높낮이가 한 줄 직선이 아니라 완만한 리듬으로 보여야 한다
- 손바닥 쪽은 접히는 주름과 압박으로 리듬이 달라진다

## Pose and contact logic

### Relaxed open hand

- 손가락은 완전 직선보다 약한 곡선이 기본
- 검지/중지가 주도 방향을 만든다
- 약지/새끼는 조금 더 따라온다

### Holding a prop

규칙:

- 파지 물체가 손가락을 밀어내며 각도와 간격을 바꾼다
- 닿는 손가락은 압박, 겹침, 일부 가림이 생겨야 한다
- 손가락이 물체 표면을 따라 감기는 방향이 보여야 한다

파지 체크:

- 어떤 손가락이 주로 누르는가
- 엄지가 반대 압력을 주는가
- 손목이 물체 축과 어떤 관계를 갖는가

### Foreshortened hand

규칙:

- 손가락 길이를 억지로 다 보이게 펴지 않는다
- 겹침, 앞뒤 층, 큰 끝/작은 기저부 비율로 공간감을 만든다
- 카메라에 가까운 손가락 하나가 주도권을 가져도 괜찮다

## Rendering priority

인체는 오브젝트 수나 배경 밀도와 상관없이 항상 최우선 모델링 대상이다.
손은 얼굴 다음 우선순위로 본다 when:

- 얼굴 가까이에 있음
- 무기/담배/파이프/장신구를 쥠
- 감정 제스처를 담당함
- 전경에 크게 보임

그 외에는:

- 개별 손가락의 시작점 / 방향 / 끝점은 유지하고, 마디 주름·손톱·작은 선 디테일만 줄인다
- 손이 작아도 손가락을 하나의 검은 덩어리, 장갑 덩어리, 장식선, 혈흔, 또는 소매 그림자로 대체하지 않는다

## Step 5 execution summary

1. Decide whether the hand is focal, support, or background.
2. Block the palm mass and thumb wedge first.
3. Model thumb, index, middle, ring, and little finger as separate chains before rendering costume, props, blood, or background detail.
4. Check finger length rhythm and taper.
5. If holding a prop, show contact pressure and overlap.
6. If foreshortened, prioritize depth overlap over full finger visibility.
7. At reduced size, confirm the hand still reads as five structurally separate fingers attached to one palm, not a mitten, claw accident, or fused glove.

## Gate

Do not pass Step 5 when visible hands matter unless all are true:

- palm block and thumb direction are readable
- thumb, index, middle, ring, and little finger each have a distinct start/direction/end or visible overlap/contact cue
- finger lengths and tapers are not uniform
- prop contact or gesture logic is believable
- the hand supports the focal flow instead of collapsing into noise

If any item fails, revise individual finger-chain modeling and contact logic before color/texturing.
