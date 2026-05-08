---
id: "topic-001-ai-prompt-eng-20260508"
category: "[[10_Wiki/💡 Topics]]"
confidence_score: 0.91
tags: [ai-image, prompt-engineering, midjourney, stable-diffusion, dalle, generative-ai]
last_reinforced: 2026-05-08
github_commit: "c332b3c"
---

# [[AI-Image-Prompt-Engineering]]

## 📌 한 줄 통찰 (The Karpathy Summary)
> 좋은 AI 이미지 프롬프트는 카메라 감독, 조명 설계자, 색채 보정자의 언어를 한 줄에 압축한 기술 명세서다.

## 📖 구조화된 지식 (Synthesized Content)

### 추출된 패턴: 프롬프트 7계층 구조

| 계층 | 역할 | 예시 키워드 |
|------|------|------------|
| 1. 스타일/매체 | 장르와 품질 기준 설정 | `cinematic concept art`, `8K`, `VFX` |
| 2. 피사체 | 인물/사물의 구체적 묘사 | `lean muscular male athlete, late 20s` |
| 3. 액션 | 움직임과 역동성 | `mid-stride sprinting, left to right` |
| 4. 환경 | 배경, 공간, 날씨 | `vast Sahara desert dunes, partly cloudy` |
| 5. 카메라 | 렌즈, 앵글, 심도 | `24mm wide angle, low angle, f/8` |
| 6. 조명 | 광원 방향, 색온도, 그림자 | `harsh top-left sunlight, warm daylight` |
| 7. 색보정 | 색상 감정선 | `desaturated blues, earthy tans, high contrast` |

### 플랫폼별 프롬프트 전략

**Midjourney**
```
{positive_prompt} --ar 16:9 --v 6.1 --style raw --q 2
```
- `--style raw`: AI 과잉 미화 억제, 지시 충실도 우선
- `--q 2`: 최고 품질 (렌더링 시간 증가)

**Stable Diffusion / SDXL**
```
Positive: {positive_prompt}
Negative: {negative_prompt}
```
- 네거티브 프롬프트가 결과 품질을 결정하는 주 변수
- 핵심 패턴: 원치 않는 속성을 명시적으로 배제

**DALL-E 3**
```
Create a photorealistic digital concept art image. {prompt}
The style should look like a high-end sports brand campaign advertisement.
```
- 지시형 문장으로 시작 → 맥락 이해도 향상
- 스타일 레퍼런스를 문장 말미에 추가

### 네거티브 프롬프트 설계 원칙
1. **물리적 오류 방지:** `solid [creature]` → 볼류메트릭 효과 보호
2. **스케일 오류 방지:** `normal-sized [entity]` → 카이주 스케일 유지
3. **품질 저하 방지:** `low quality, blurry, deformed, ugly`
4. **컨텍스트 오염 방지:** `indoor, nighttime, urban, cartoon`

### 브랜드 프롬프트 커스터마이제이션 패턴
```python
# 공식: [색상] [브랜드명] [의류] with the [브랜드명] [로고형태] logo on the [위치]
"light grey Nike athletic t-shirt with the Nike swoosh logo on the chest"
```

## ⚠️ 모순 및 업데이트 (Contradictions & RL Update)
- **과거 데이터와의 충돌:** 초기 프롬프트 이론은 '길수록 좋다'는 경향이 있었으나, 실제 Midjourney v6에서는 핵심 개념 밀도가 분산되면 오히려 정확도 하락.
- **정책 변화:** 7계층 구조를 순서대로 배치하면 토큰 우선순위 면에서 '스타일/매체' → '피사체' 순으로 처리되므로 전체 이미지 방향성이 먼저 고정된다.

## 🔗 지식 연결 (Graph)
- **Parent:** [[10_Wiki/💡 Topics]]
- **Related:** [[Surreal-Athlete-Sand-Cheetah]], [[P-Reinforce_Skill]], [[Particle-Simulation-VFX]]
- **Raw Source:** [[00_Raw/2026-05-08/prompt_generator.py]]
