# Test Cases

Use these prompts to verify trigger coverage and workflow behavior.

## Should trigger

1. `네온 실험실 배경에 들어갈 specimen tank랑 cable bundle 구조 조사해줘. 나중에도 재사용할 수 있게 카드로 저장해.`
   - Expected mode: `LOOKUP -> RESEARCH`

2. `고딕 홀 배경에서 자주 쓰는 chandelier, altar, stained glass 조합을 scene recipe로 정리해줘.`
   - Expected mode: `LOOKUP -> RECIPE`

3. `warning panel 오브젝트 카드가 이미 있으면 불러오고, 부족하면 업데이트해줘.`
   - Expected mode: `LOOKUP` with optional `RESEARCH`

## Should not trigger

1. `차갑고 위험한 미소의 소녀 구도 잡아줘.`
   - Better fit: `illustrate-skill`

2. `이 캐릭터 눈을 더 반짝이게 만드는 방법 알려줘.`
   - Better fit: `illustrate-skill`
