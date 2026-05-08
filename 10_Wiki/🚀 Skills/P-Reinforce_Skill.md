---
id: "skill-001-p-reinforce-20260508"
category: "[[10_Wiki/🚀 Skills]]"
confidence_score: 0.97
tags: [autonomous-agent, knowledge-management, reinforcement-learning, wiki-architecture, karpathy]
last_reinforced: 2026-05-08
github_commit: "c332b3c"
---

# [[P-Reinforce_Skill]]

## 📌 한 줄 통찰 (The Karpathy Summary)
> 파편화된 정보를 던지면, RL 보상 함수가 그것을 영속적 지식 그래프로 자동 변환하는 자율 정원사 엔진.

## 📖 구조화된 지식 (Synthesized Content)

### 핵심 아키텍처
- **기반 이론:** Andrej Karpathy의 LLM-Wiki + 강화학습(RL) 정책 결합
- **목표:** 인간 개입 없이 (1) 분류 → (2) 폴더링 → (3) 링크 → (4) Git 버전관리를 자동화
- **보상 함수:**
  ```
  R = w₁(Categorization Accuracy) + w₂(Graph Connectivity) + w₃(User Satisfaction)
  ```

### RL 상태-행동-보상 사이클

| 단계 | 설명 |
|------|------|
| **State** | `10_Wiki/` 폴더 트리 + `20_Meta/Graph.json` 읽기 → 지식 지형도 파악 |
| **Action: 분류** | 유사도 ≥ 85% → 기존 폴더 / < 85% → 새 폴더 생성 |
| **Action: 재구조화** | 폴더 내 파일 > 12개 → 하위 카테고리 세분화(Refactoring) 제안 |
| **Action: 합성** | Wiki 템플릿 정제 + 최소 2개 관련 지식 링크 |
| **Reward** | 사용자 피드백(칭찬/수정/방치) → `20_Meta/Policy.md` 가중치 갱신 |

### 추출된 패턴
- **칭찬** → 해당 주제 유사도 가중치 `w₁` 상향
- **수정("코딩 → 비즈니스로 이동")** → 두 카테고리 간 경계선 재설정 (Boundary Shift)
- **방치(무수정 사용)** → 암묵적 보상으로 정책 고착화

### Git 동기화 프로토콜
```bash
git add .
git commit -m "[P-Reinforce] {{Action_Summary}}"
git push origin main
# 성공 → confidence_score 보너스 / 실패 → 로그 기록 후 재시도
```

### 폴더 구조 설계 원칙
```
root/
├── 00_Raw/YYYY-MM-DD/   # 불변 원본 (Source of Truth)
├── 10_Wiki/             # RL 정책에 따라 자동 구조화
│   ├── 🛠️ Projects/    # 목표 중심
│   ├── 💡 Topics/      # 개념 중심
│   ├── ⚖️ Decisions/   # 의사결정 중심
│   └── 🚀 Skills/      # 실행 워크플로우 중심
├── 20_Meta/             # 엔진 두뇌 데이터
└── .github/             # 자동화 워크플로우
```

## ⚠️ 모순 및 업데이트 (Contradictions & RL Update)
- **과거 데이터와의 충돌:** 초기 버전은 수동 폴더 구조를 강제했으나, 현 설계는 폴더 트리를 고정하지 않고 지식 맥락에 따라 동적으로 확장한다.
- **정책 변화:** 최초 `confidence_score` 기준값 0.85 → 실제 운용 시 카테고리별 임계값 차등화 필요 (기술 지식 0.90 / 감성·창작 지식 0.80).

## 🔗 지식 연결 (Graph)
- **Parent:** [[10_Wiki/🚀 Skills]]
- **Related:** [[AI-Image-Prompt-Engineering]], [[Surreal-Athlete-Sand-Cheetah]], [[Knowledge-Graph-Design]]
- **Raw Source:** [[00_Raw/2026-05-08/Surreal-Athlete-Sand-Cheetah_raw.md]]
