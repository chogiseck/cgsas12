# NotebookLM + Obsidian 최신 자료 조사 노트

> 작성일: 2026-02-10
> 주제: NotebookLM과 Obsidian 연동 활용법 및 최신 동향

---

## 1. NotebookLM + Obsidian 연동 방식

### 방법 1: Markdown 파일 직접 업로드
- NotebookLM은 Markdown을 지원하므로 Obsidian 볼트의 `.md` 파일을 직접 업로드 가능
- 참고: [XDA Developers - NotebookLM with Obsidian](https://www.xda-developers.com/using-notebooklm-with-obsidian/)

### 방법 2: PDF로 내보내기 후 업로드
- Obsidian 플러그인 "Better Export PDF"를 사용하면 폴더 내 여러 노트를 하나의 PDF로 합쳐서 내보낼 수 있음
- NotebookLM의 소스 수 제한(무료 50개, Plus 300개)을 우회하는 효과적인 방법
- 참고: [Mark Grabe - Upload Obsidian Folders to NotebookLM](https://medium.com/@markgrabe/upload-obsidian-folders-to-notebooklm-bd9aa0bc8ea7)

### 방법 3: Obsidian Publish + 웹 URL
- Obsidian Publish로 공개한 노트의 URL을 NotebookLM 소스로 등록
- 노트 업데이트 시 자동 반영되는 장점

### 방법 4: HoverNotes 활용 (2026년 1월)
- YouTube 영상 노트를 Markdown으로 저장 → Google Drive 업로드 → NotebookLM 소스로 추가
- Obsidian 사용자에게 특히 적합한 워크플로우
- 참고: [HoverNotes - Add Any Video to NotebookLM](https://hovernotes.io/en/blog/add-any-video-to-notebooklm-with-hovernotes)

---

## 2. 추천 워크플로우: Obsidian + NotebookLM + YouTube

### YouTube → NotebookLM Chrome 확장 프로그램
- "YouTube to NotebookLM" Chrome 확장으로 YouTube 영상/플레이리스트를 한 클릭으로 NotebookLM에 추가
- URL 수동 복사 없이 바로 전송 가능
- 참고: [Android Police - NotebookLM with YouTube](https://www.androidpolice.com/paired-notebooklm-with-youtube-learned-faster/)

### 최적의 역할 분담
| 도구 | 역할 |
|------|------|
| **Obsidian** | 영구 지식 아카이브 (장기 지식 베이스) |
| **NotebookLM** | 프로젝트별 연구·분석 (AI 기반 소스 질의) |
| **YouTube** | 학습 소스 (NotebookLM으로 직접 추가 가능) |

---

## 3. NotebookLM 2025~2026 주요 업데이트

### Deep Search 기능 (2025년 11월)
- AI가 수백 개의 웹사이트를 자동 탐색하여 관련 자료 수집
- 기존 Fast Search(7개 소스) → Deep Search(33개+ 고품질 소스)

### 멀티모달 분석 (2026년)
- 텍스트뿐 아니라 이미지, 도표까지 분석
- 마인드맵, 인포그래픽, 슬라이드, 데이터 표 자동 생성

### 한국어 음성 기능
- 문서·YouTube 자료를 한국어 팟캐스트로 변환 가능
- 설정에서 출력 언어를 '한국어'로 변경

### 소스 지원 현황
- PDF, Google Docs, Word, 텍스트, 웹사이트 URL, YouTube 영상, Google Slides
- 무료: 노트북당 50개 소스 / Plus: 300개 소스

---

## 4. 비교: NotebookLM vs Obsidian (2026년 기준)

| 항목 | NotebookLM | Obsidian |
|------|-----------|----------|
| AI 질의 | 내장 (Gemini 기반) | 플러그인 필요 (Smart Composer 등) |
| 데이터 소유권 | Google 클라우드 | 로컬 파일 (완전 소유) |
| YouTube 연동 | URL 붙여넣기로 즉시 분석 | 수동 요약 필요 |
| 지식 그래프 | 노트북 간 격리됨 | 링크·태그로 자유 연결 |
| 가격 | 무료 (Plus 선택) | 무료 (Sync/Publish 유료) |

- 참고: [NotebookLM vs Obsidian vs Atlas (2026)](https://www.atlasworkspace.ai/blog/notebooklm-vs-obsidian-vs-atlas)
- 참고: [NotebookLM vs Obsidian - ClickUp](https://clickup.com/blog/notebook-lm-vs-obsidian/)

---

## 5. 오픈소스 대안

### Open Notebook (2026년)
- NotebookLM의 오픈소스 대안, 셀프호스팅 가능
- REST API로 n8n/Zapier를 통해 Obsidian, Notion 등과 연동
- 프라이버시 중시 사용자에게 적합
- 참고: [TechnomiPro - Open Notebook](https://www.technomipro.com/open-notebook-private-open-source-notebooklm-alternative/)

---

## 참고 자료 모음

- [NotebookLM 사용법 완벽 가이드 2026 - 캐럿](https://carat.im/blog/notebooklm-guide)
- [NotebookLM AI 비서 가이드 2025 - 피카부랩스](https://peekaboolabs.ai/blog/notebooklm-ai-assistant-guide)
- [Storylane - NotebookLM + Obsidian 연동 가이드](https://www.storylane.io/tutorials/how-to-integrate-notebooklm-with-obsidian)
- [WanderLoots - NotebookLM + Obsidian 실전 활용 영상](https://wanderloots.xyz/digital-garden/tutorials/how-i-use-notebook-lm-with-obsidian-practical-note-taking-ai/)
- [Pocket-lint - NotebookLM and Obsidian Dynamic Duo](https://www.pocket-lint.com/obsidian-notebooklm-collaboration/)
- [Obsidian Forum - NotebookLM 기능 논의](https://forum.obsidian.md/t/notebooklm-features/82253)
