# THEORY_03_LIGHTING_VALUE

Summary: This theory defines lighting direction and value structure before color is introduced. The goal is to make form, focus, and atmosphere readable in grayscale alone.

Summary: Step 3 must decide where the key light comes from, how many value groups are allowed, how contrast concentrates around the face and eyes, and how skin/material edges separate by value behavior.

## Purpose

2단계에서 만든 구도와 실루엣 위에 빛의 방향과 값 구조를 설계해 장면의 분위기와 초점을 확정한다.
색을 넣기 전에, 흑백만으로도 입체감, 감정, 초점이 성립하는 상태를 만드는 것이 목표다.

이 단계에서 먼저 결정해야 하는 것:

- 광원은 어디에서 얼마나 강하게 오는가
- 얼굴/눈을 가장 밝게 하고 주변을 얼마나 어둡게 누를 것인가
- 값 단계를 몇 단계로 제한할 것인가

## Basic concepts

### Value and light/shadow

- value: 색을 제외한 밝기/어두움의 정도
- 명암: 빛이 닿는 부분, 닿지 않는 부분, 그리고 그 사이의 단계들

값 구조가 강해야:

- 색이 없어도 형태가 읽힌다
- 초점이 유지된다
- 분위기가 선명하게 느껴진다

### Light/shadow components

- highlight: 가장 밝은 부분
- light: 빛을 받는 큰 밝은 면
- midtone: 빛과 그림자 사이의 중간 영역
- form shadow / core shadow: 형태 자체에서 생기는 진한 그림자
- cast shadow: 다른 물체에 떨어지는 그림자
- reflected light: 주변에서 튕겨오는 약한 빛

## Lighting setup theory

### Minimum light definition

Step 3 must define at least:

- direction
- intensity / softness
- temperature or color character

최소 1개의 `key light`는 반드시 정한다.
필요하면 `fill light`와 `rim light`를 추가할 수 있다.

### Common lighting types

- front / 45-degree side light: 기본적인 입체감
- back light / rim light: 실루엣과 분위기 강조
- hard light: 강한 대비, 날카로운 그림자
- soft light: 부드러운 그라데이션, 차분한 분위기

## Value-step design

### Value count

값 단계는 기본적으로 `3-5`단계 안에 제한한다.

예:

- 3 values: bright / middle / dark
- 4 values: bright / light / middle / dark
- 5 values: highlight / light / middle / shadow / deep shadow

규칙:

- 값 단계가 많아질수록 제어가 어려워진다
- 기본값은 3-5단계의 통제된 구조다

### Focal contrast distribution

가장 큰 대비는 초점 부위, 보통 얼굴과 눈 주변에 둔다.

규칙:

- 얼굴/눈 주변은 값의 양 극단을 모두 사용해 대비를 만든다
- 배경과 가장자리는 중간값 위주로 모아 초점 경쟁을 줄인다

## Material and edge separation

### Skin vs clothing / background

피부:

- 부드러운 그라데이션
- 좁은 값 변화

옷/배경:

- 더 넓은 값 차이
- 더 강한 구조적 그림자

규칙:

- 같은 값 단계 수 안에서도 피부는 완만하게
- 옷/배경은 더 크게 끊어 재질을 분리한다

### Hard edge vs soft edge

Hard edge:

- 개체 경계
- 강한 그림자 경계
- 초점 부위
- 금속/유리/날카로운 재질

Soft edge:

- 피부
- 덜 중요한 영역
- 둥근 형태 변화

규칙:

- 초점 부위는 하드 엣지 비율을 높인다
- 덜 중요한 영역은 소프트 엣지로 흐리게 둔다

## Intent-to-light link

1단계 의도와 연결해 광원과 대비를 정한다.

예:

- 긴장 / 스릴 / 위험 -> 강한 대비, 하드 라이트, 측광/역광
- 고요 / 안정 / 따뜻함 -> 낮은 대비, 소프트 라이트, 넓은 라이트 영역
- 미스터리 / 고딕 / 공포 -> 큰 어둠 + 작은 밝음, 화면 대부분 암부

## Digital grayscale workflow

실무 규칙:

- 먼저 그레이스케일로 값 구조를 완성한다
- 큰 덩어리부터 나누고, 중간 단계, 마지막으로 디테일 순서로 간다
- 큰 값 분할은 큰 브러시와 높은 불투명도
- 그라데이션은 부드러운 브러시와 낮은 불투명도
- 얼굴, 피부, 손 같은 중요한 부위를 먼저 확정한다

## Step 3 execution summary

1. Define the key light:
   - direction
   - intensity / hard vs soft
   - cool / warm / colored character
2. Decide the value count within `3-5`.
3. Decide where the strongest contrast will live:
   - usually eyes / face
4. Group the outer frame and background into quieter values.
5. Assign value behavior by material:
   - skin = softer, narrower shifts
   - clothing/background = stronger breaks and cast shadows
6. Paint grayscale values over the silhouette:
   - big masses
   - middle structure
   - focal accents
7. Run a grayscale thumbnail test.

## Gate

Do not continue to Step 4 unless all are true:

- light direction and intensity are readable from the image
- value groups stay controlled within 3-5 levels
- the largest contrast sits around face and eyes
- skin, clothing, and background separate by value and edge behavior
- the focal point and atmosphere still hold in grayscale at reduced size

If any item fails, revise the value structure first.
