#!/bin/bash
# 트리거: PostToolUse — Write | Edit | MultiEdit
# 파일 수정 후 동기화 갭을 즉시 감지한다

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
python "$ROOT/.claude/scripts/validate.py" 2>&1 | tail -6
