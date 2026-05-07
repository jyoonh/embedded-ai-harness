"""
동기화 갭 감지 도구.

코드 변화 후 실행하여 하네스 구성 요소 간 불일치를 탐지한다.

검사 항목:
  1. .claude/agents/   — 필수 섹션 누락, ERRORS.md 참조 누락
  2. .claude/memory/   — MEMORY.md 인덱스와 실제 파일 불일치
  3. .claude/skills/   — 파일 정의 여부
  4. .claude/docs/     — README.md 인덱스와 decisions/ 파일 불일치
  5. git               — 변경된 파일 기준 연관 파일 업데이트 여부

사용법:
  python .claude/scripts/validate.py [--git-diff]
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent  # .claude/scripts/ → .claude/ → repo root

AGENT_REQUIRED_SECTIONS = ["## 역할", "## 시작 전 필수", "## 보고 양식"]

ok_count = 0
fail_count = 0


def ok(msg: str) -> None:
    global ok_count
    print(f"  ✓ {msg}")
    ok_count += 1


def fail(msg: str) -> None:
    global fail_count
    print(f"  ✗ {msg}")
    fail_count += 1


# ── 1. agents/ 검사 ───────────────────────────────────────────────

def check_agents() -> None:
    print("\n[agents/]")
    agent_files = sorted((ROOT / ".claude" / "agents").glob("*.md"))
    if not agent_files:
        fail("agents/ 디렉토리가 비어 있음")
        return

    errors_path = ROOT / ".claude" / "memory" / "ERRORS.md"
    for f in agent_files:
        content = f.read_text()
        for section in AGENT_REQUIRED_SECTIONS:
            if section not in content:
                fail(f"{f.name}: '{section}' 섹션 누락")
            else:
                ok(f"{f.name}: '{section}' 존재")

        if "ERRORS.md" not in content:
            fail(f"{f.name}: memory/ERRORS.md 참조 누락")
        else:
            ok(f"{f.name}: ERRORS.md 참조 확인")

    if not errors_path.exists():
        fail("memory/ERRORS.md 파일 없음")
    else:
        ok("memory/ERRORS.md 존재")


# ── 2. memory/ 인덱스 검사 ────────────────────────────────────────

def check_memory() -> None:
    print("\n[memory/]")
    memory_dir = ROOT / ".claude" / "memory"
    index = memory_dir / "MEMORY.md"
    if not index.exists():
        fail("MEMORY.md 없음")
        return

    index_text = index.read_text()
    actual_files = {f.name for f in memory_dir.glob("*.md") if f.name != "MEMORY.md"}

    for fname in actual_files:
        if fname in index_text:
            ok(f"{fname}: 인덱스에 등록됨")
        else:
            fail(f"{fname}: MEMORY.md 인덱스에 미등록")

    linked = set(re.findall(r'\[.*?\]\((\S+?\.md)\)', index_text))
    for link in linked:
        target = memory_dir / link
        if not target.exists():
            fail(f"MEMORY.md 링크 대상 없음: {link}")
        else:
            ok(f"링크 대상 존재: {link}")


# ── 3. .claude/commands/ 검사 ────────────────────────────────────

def check_commands() -> None:
    print("\n[.claude/skills/]")
    commands_dir = ROOT / ".claude" / "skills"
    settings = ROOT / ".claude" / "settings.json"

    if not commands_dir.exists():
        fail(".claude/commands/ 디렉토리 없음")
        return

    cmd_files = sorted(commands_dir.glob("*.md"))
    if not cmd_files:
        fail(".claude/commands/ 비어 있음")
        return

    for f in cmd_files:
        content = f.read_text()
        if "$ARGUMENTS" not in content and len(content.strip()) < 20:
            fail(f"{f.name}: 내용이 너무 짧거나 비어 있음")
        else:
            ok(f"{f.name}: 정의됨")

    if not settings.exists():
        fail(".claude/settings.json 없음")
    else:
        ok("settings.json 존재")


# ── 4. docs/architecture/ 인덱스 검사 ────────────────────────────

def check_architecture() -> None:
    print("\n[docs/architecture/]")
    arch_dir = ROOT / ".claude" / "docs" / "architecture"
    readme = arch_dir / "README.md"
    decisions_dir = arch_dir / "decisions"

    if not readme.exists():
        fail("docs/architecture/README.md 없음")
        return

    readme_text = readme.read_text()
    decision_files = list(decisions_dir.glob("*.md")) if decisions_dir.exists() else []

    if not decision_files:
        ok("decisions/ 비어 있음 (기록 없음)")
        return

    for f in decision_files:
        if f.name in readme_text:
            ok(f"{f.name}: 인덱스에 등록됨")
        else:
            fail(f"{f.name}: README.md 인덱스에 미등록")


# ── 4. git 변경 파일 기반 연관 갭 탐지 ───────────────────────────

def check_git_diff() -> None:
    print("\n[git 변경 감지]")
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            capture_output=True, text=True, cwd=ROOT
        )
        changed = [Path(p) for p in result.stdout.strip().splitlines() if p]
    except Exception:
        fail("git 실행 실패")
        return

    if not changed:
        ok("변경된 파일 없음")
        return

    for f in changed:
        print(f"  → 변경됨: {f}")

    # .claude/agents/ 변경 → .claude/memory/MEMORY.md 업데이트 권고
    agent_changed = any(".claude/agents/" in str(f) for f in changed)
    memory_changed = any(".claude/memory/" in str(f) for f in changed)
    if agent_changed and not memory_changed:
        fail(".claude/agents/ 변경됨 — .claude/memory/MEMORY.md 업데이트 여부 확인")

    # docs/architecture/decisions/ 추가 → README 인덱스 미등록 탐지
    new_decisions = [f for f in changed if "decisions/" in str(f)]
    if new_decisions:
        readme = ROOT / ".claude" / "docs" / "architecture" / "README.md"
        if readme.exists():
            readme_text = readme.read_text()
            for d in new_decisions:
                if d.name not in readme_text:
                    fail(f"{d.name}: docs/architecture/README.md 인덱스에 미등록")
                else:
                    ok(f"{d.name}: 인덱스 등록 확인")


# ── main ─────────────────────────────────────────────────────────

def main() -> None:
    use_git = "--git-diff" in sys.argv

    print("=" * 50)
    print("embedded-ai-harness 동기화 갭 검사")
    print("=" * 50)

    check_agents()
    check_memory()
    check_commands()
    check_architecture()
    if use_git:
        check_git_diff()

    print(f"\n결과: 통과 {ok_count} / 실패 {fail_count}")
    if fail_count > 0:
        print("위 항목을 수정한 후 다시 실행하세요.")
        sys.exit(1)
    else:
        print("모든 검사 통과.")


if __name__ == "__main__":
    main()
