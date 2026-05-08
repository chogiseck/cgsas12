---
id: "proj-001-sand-cheetah-20260508"
category: "[[10_Wiki/🛠️ Projects]]"
confidence_score: 0.94
tags: [concept-art, vfx, sports-advertising, ai-image-generation, sand-cheetah, surrealism]
last_reinforced: 2026-05-08
github_commit: "c332b3c"
---

# [[Surreal-Athlete-Sand-Cheetah]]

## 📌 한 줄 통찰 (The Karpathy Summary)
> 인간의 질주와 모래 치타의 추격이 하나의 모래 흐름으로 연결될 때, 스포츠 광고는 신화가 된다.

## 📖 구조화된 지식 (Synthesized Content)

### 핵심 콘셉트
- **장르:** 초현실주의(Surrealism) × 스포츠 광고 × 서사 영화
- **핵심 장치:** 치타는 실체가 없다 — 수백만 모래 입자의 볼류메트릭 시뮬레이션
- **상징:** 선수가 차올리는 모래 먼지 = 치타를 구성하는 재료 → 인간이 속도를 소환한다

### 피사체 & 액션

| 요소 | 상세 |
|------|------|
| 피사체 | 20대 후반 남성, 린-머슬 러너 체형, 브론즈 피부 |
| 자세 | 왼→오른 방향 전력 질주, 앞으로 기울어진 미드스트라이드 |
| 표정 | 강렬한 집중, 입 살짝 벌림 |
| 치타 | 카이주 스케일, 머리+앞발, 모래폭풍과 경계 없이 용해 |

### 카메라 & 조명 사양

```
렌즈:   24mm 와이드 시네마 프라임
조리개: f/8 (전경-중경 모두 선명)
앵글:   로우 앵글 트래킹 샷
조명:   좌상단 강한 태양광 (따뜻한 주광색)
색보정: 탈채도 블루 + 풍부한 베이지/탄 어스톤, 하이 콘트라스트
```

### 깊이 레이어링
```
[전경] 선수 + 비산 모래
  ↓
[중경] 모래 치타 엔티티
  ↓
[원경] 파란 하늘 + 큐뮬러스 구름
```

### 브랜드 커스터마이제이션 매트릭스

| 브랜드 | 의류 색상 | 신발 포인트 | 로고 위치 |
|--------|----------|-------------|---------|
| Nike | 라이트 그레이 | 볼트 그린 | 가슴 센터 |
| Adidas | 화이트 | 코랄 | 가슴 센터 |
| Puma | 블랙 | 네온 옐로 | 가슴 센터 |

### AI 이미지 생성 프롬프트 운용
- **파일:** `00_Raw/2026-05-08/prompt_generator.py`
- **지원 플랫폼:** Midjourney (`--ar 16:9 --v 6.1`), Stable Diffusion SDXL, DALL-E 3
- **핵심 네거티브 프롬프트:** `solid cheetah, realistic cheetah, normal-sized cheetah`

## ⚠️ 모순 및 업데이트 (Contradictions & RL Update)
- **과거 데이터와의 충돌:** 초안 `Surreal-Athlete-Sand-Cheetah.md`는 단순 서술형이었으나, P-Reinforce 템플릿으로 재구조화하면서 브랜드 매트릭스와 카메라 사양이 정량화되었다.
- **정책 변화:** 창작 프로젝트 문서에는 브랜드/기술 사양을 테이블로 정리하는 패턴이 효과적임을 확인 → `Policy.md` `creative_project` 카테고리에 반영.

## 🔗 지식 연결 (Graph)
- **Parent:** [[10_Wiki/🛠️ Projects]]
- **Related:** [[AI-Image-Prompt-Engineering]], [[P-Reinforce_Skill]], [[Particle-Simulation-VFX]]
- **Raw Source:** [[00_Raw/2026-05-08/scene.json]], [[00_Raw/2026-05-08/prompt_generator.py]]
