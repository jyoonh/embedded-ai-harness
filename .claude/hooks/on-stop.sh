#!/bin/bash
# 트리거: Stop — Claude 응답 완료 시
# 메모리 갱신이 필요한 상황인지 체크하여 안내한다

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
MEMORY="$ROOT/.claude/memory/MEMORY.md"
ERRORS="$ROOT/.claude/memory/ERRORS.md"

# 오늘 날짜가 MEMORY.md에 없으면 갱신 리마인더 출력
TODAY=$(date +%Y-%m-%d)
if ! grep -q "$TODAY" "$MEMORY" 2>/dev/null; then
  echo "[memory] 오늘($TODAY) 갱신 기록 없음 — 중요한 결정이나 오류가 있었다면 memory를 갱신하세요"
fi
