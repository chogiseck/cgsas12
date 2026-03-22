#!/bin/bash
# morning.sh — 매일 아침 실행

# 데일리 노트 열기
obsidian daily

# 어제 미완료 할 일 확인
echo ""
echo "📋 미완료 할 일:"
obsidian tasks all todo
