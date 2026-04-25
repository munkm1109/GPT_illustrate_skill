# Test Cases

## Should trigger

1. `이 레퍼런스 폴더 분석해서 새로운 그림체 스킬 만들어줘. 원본 illustrate-skill은 유지해.`
   - Expected mode: `ANALYZE -> GENERATE`

2. `reference set으로 파생 스타일 스킬 만들고 싶어. base process는 건들지 마.`
   - Expected mode: `ANALYZE -> GENERATE`

3. `이 새 레퍼런스 몇 장 추가해서 기존 파생 스타일 스킬 보강해줘.`
   - Expected mode: `ANALYZE -> REFINE`

4. `illustrate-skill에서 쓸 새 reference-derived wrapper 만들어줘.`
   - Expected mode: `ANALYZE -> GENERATE`

## Should not trigger

1. `이 한 장면 구도만 잡아줘.`
   - Better fit: `illustrate-skill`

2. `배경 오브젝트 구조 조사해줘.`
   - Better fit: `object-research-skill`

3. `이 결과가 망했는지 critique만 해줘.`
   - Better fit: `illustrate-skill` or the existing derived wrapper in `CRITIQUE`
