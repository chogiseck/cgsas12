#!/bin/bash
# Claude Code 세션 시작 훅 — AI 뉴스 상태 확인
# 클라우드(웹) 환경에서만 실행

set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

DATE=$(date +%Y-%m-%d)
NEWS_FILE="${CLAUDE_PROJECT_DIR}/AI뉴스/${DATE}.md"

echo "📰 AI 뉴스 훅 확인 중..."

if [ -f "$NEWS_FILE" ]; then
  echo "✅ 오늘(${DATE}) AI 뉴스가 이미 저장되어 있습니다: AI뉴스/${DATE}.md"
else
  echo "⏳ 오늘(${DATE}) AI 뉴스가 아직 없습니다."
  echo "   → GitHub Actions가 매일 08:00(KST)에 자동 수집합니다."
  echo "   → 지금 바로 보고 싶다면 Claude에게 'AI 뉴스 저장해줘' 라고 말하세요."
fi
