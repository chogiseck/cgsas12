# NotebookLM + Obsidian 영상 자료 노트북

> 생성일: 2026-02-10
> 목적: NotebookLM과 Obsidian 연동 관련 영상 자료를 모아 학습용 노트북 구성

---

## 소스로 추가할 영상/자료 URL 목록

### 영상 자료

1. **WanderLoots - "How I Use NotebookLM With Obsidian"**
   - https://wanderloots.xyz/digital-garden/tutorials/how-i-use-notebook-lm-with-obsidian-practical-note-taking-ai/
   - 내용: NotebookLM + Obsidian 실전 노트 테이킹 + AI 활용법

2. **Android Police - "NotebookLM + YouTube로 더 빠르게 학습하기"**
   - https://www.androidpolice.com/paired-notebooklm-with-youtube-learned-faster/
   - 내용: YouTube to NotebookLM Chrome 확장 활용, 영상 기반 학습 워크플로우

3. **HoverNotes - "아무 영상이나 NotebookLM에 추가하기"**
   - https://hovernotes.io/en/blog/add-any-video-to-notebooklm-with-hovernotes
   - 내용: HoverNotes로 YouTube 영상 노트를 Markdown으로 저장 → NotebookLM 연동

### 가이드/문서 자료

4. **Storylane - "NotebookLM + Obsidian 연동 1분 가이드"**
   - https://www.storylane.io/tutorials/how-to-integrate-notebooklm-with-obsidian
   - 내용: Obsidian 노트를 PDF로 내보내 NotebookLM에 업로드하는 방법

5. **XDA Developers - "NotebookLM + Obsidian은 게임 체인저"**
   - https://www.xda-developers.com/using-notebooklm-with-obsidian/
   - 내용: Markdown 직접 업로드, 웹링크/PDF/YouTube 트랜스크립션 활용

6. **Mark Grabe - "Obsidian 폴더를 NotebookLM에 업로드하기"**
   - https://medium.com/@markgrabe/upload-obsidian-folders-to-notebooklm-bd9aa0bc8ea7
   - 내용: Better Export PDF 플러그인으로 여러 노트를 하나의 PDF로 합쳐 업로드

7. **캐럿 블로그 - "NotebookLM 사용법 완벽 가이드 (2026)"**
   - https://carat.im/blog/notebooklm-guide
   - 내용: 논문 요약부터 비주얼 콘텐츠 제작까지, 멀티모달 분석 포함

8. **피카부랩스 - "NotebookLM AI 비서 완벽 가이드 (2025)"**
   - https://peekaboolabs.ai/blog/notebooklm-ai-assistant-guide
   - 내용: 자료 조사 시간 90% 절약, Deep Search 활용법

---

## NotebookLM 노트북 생성 가이드

위 URL들을 NotebookLM 노트북에 소스로 추가하려면:

1. [NotebookLM](https://notebooklm.google.com) 접속
2. "+ 새 노트북" 클릭
3. 노트북 이름: **"Obsidian + NotebookLM 연동 학습"**
4. 소스 추가 → "웹사이트" 선택 → 위 URL을 하나씩 붙여넣기
5. 모든 소스 추가 후 AI에게 질문:
   - "이 자료들을 종합해서 Obsidian과 NotebookLM을 연동하는 최적의 워크플로우를 정리해줘"
   - "YouTube 영상을 NotebookLM에 추가하는 방법들을 비교해줘"
   - "초보자가 시작하기 가장 좋은 연동 방법은?"

---

## MCP 서버를 통한 자동 생성 (API)

환경 변수가 설정되어 있다면 MCP 서버의 `create_notebook` 도구로 자동 생성 가능:

```json
{
  "tool": "create_notebook",
  "arguments": {
    "title": "Obsidian + NotebookLM 연동 학습"
  }
}
```

소스 추가 (Google Drive에 업로드된 경우):
```json
{
  "tool": "add_drive_sources",
  "arguments": {
    "notebookId": "<생성된-노트북-ID>",
    "driveResourceIds": ["<drive-file-id-1>", "<drive-file-id-2>"]
  }
}
```
