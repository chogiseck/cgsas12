# NotebookLM MCP Server

Google NotebookLM Enterprise API와 연동하는 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) 서버입니다.

AI 어시스턴트(Claude, Cursor 등)에서 NotebookLM 노트북을 생성, 조회, 공유하고 데이터 소스를 관리할 수 있습니다.

## 사전 요구사항

- Node.js 18+
- Google Cloud 프로젝트 (NotebookLM Enterprise 활성화)
- Discovery Engine API 활성화
- Google Cloud 인증 설정 (`gcloud auth application-default login` 또는 서비스 계정 키)

## 설치

```bash
npm install
npm run build
```

## 환경 변수 설정

`.env.example`을 참고하여 `.env` 파일을 생성하세요:

```bash
# 필수: Google Cloud 프로젝트 번호
export GOOGLE_CLOUD_PROJECT_NUMBER=123456789

# 선택: 데이터 위치 (기본값: global)
export NOTEBOOKLM_LOCATION=global

# 선택: 서비스 계정 키 파일 경로
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
```

## MCP 클라이언트 설정

### Claude Desktop / Claude Code

`claude_desktop_config.json`에 추가:

```json
{
  "mcpServers": {
    "notebooklm": {
      "command": "node",
      "args": ["dist/index.js"],
      "env": {
        "GOOGLE_CLOUD_PROJECT_NUMBER": "your-project-number"
      }
    }
  }
}
```

### Cursor / VS Code

MCP 설정에 추가:

```json
{
  "mcpServers": {
    "notebooklm": {
      "command": "node",
      "args": ["/absolute/path/to/dist/index.js"],
      "env": {
        "GOOGLE_CLOUD_PROJECT_NUMBER": "your-project-number"
      }
    }
  }
}
```

## 제공 도구 (MCP Tools)

| 도구 | 설명 |
|------|------|
| `create_notebook` | 새 노트북 생성 |
| `get_notebook` | 노트북 상세 정보 조회 |
| `list_notebooks` | 최근 조회 노트북 목록 |
| `delete_notebooks` | 노트북 삭제 |
| `share_notebook` | 노트북 공유 (Owner/Writer/Reader) |
| `add_drive_sources` | Google Drive 문서를 소스로 추가 |
| `upload_file_source` | 로컬 파일을 소스로 업로드 |
| `delete_sources` | 노트북에서 소스 삭제 |

## 사용 예시

AI 어시스턴트에서 자연어로 사용할 수 있습니다:

- "새 노트북을 'AI 연구 정리'라는 이름으로 만들어줘"
- "최근 노트북 목록을 보여줘"
- "이 노트북에 Google Drive 문서를 소스로 추가해줘"
- "노트북을 team@example.com과 공유해줘"

## 라이선스

MIT
