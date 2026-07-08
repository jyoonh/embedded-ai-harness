Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.
Tradeoff: These guidelines bias toward caution over speed. For trivial tasks, use judgment.

1. Think Before Coding
Don't assume. Don't hide confusion. Surface tradeoffs.

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

2. Simplicity First
Minimum code that solves the problem. Nothing speculative.
- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

3. Surgical Changes
Touch only what you must. Clean up only your own mess.

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

4. Goal-Driven Execution
Define success criteria. Loop until verified.

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

These guidelines are working if: fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

---

## 세션 시작 시 (Session Init)

세션을 열거나 초기화할 때 반드시 아래 순서로 실행한다:

1. `.claude/memory/MEMORY.md`를 읽어 인덱스를 확인한다
2. 인덱스에 등록된 모든 memory 파일을 읽는다
3. `.claude/memory/ERRORS.md`를 읽어 반복하지 말아야 할 오류를 파악한다

## 메모리 갱신 트리거 (Memory Update)

다음 상황에서 관련 `.claude/memory/` 파일을 갱신한다:

- 새로운 원칙이나 규칙이 결정됐을 때
- 오류가 발생하고 원인이 파악됐을 때 → `ERRORS.md`
- 의사결정이 내려졌을 때 → `docs/architecture/decisions/`
- 작업 세션이 마무리될 때 → `MEMORY.md` Current Status 업데이트

## 에이전트 라우팅 (Agent Routing)

요청 내용에 따라 아래 에이전트를 호출한다. 에이전트 정의는 `.claude/agents/`에 있다.

| 요청 패턴 | 에이전트 | 파일 |
|-----------|---------|------|
| 구현, 코드 작성, 추가, 수정 | implementer | `.claude/agents/implementer.md` |
| 테스트, 실행, 결과 검증, 성능 측정 | evaluator | `.claude/agents/evaluator.md` |
| 설계, 방안 제시, 분석, 조사 | algorithm-developer | `.claude/agents/algorithm-developer.md` |
| 리뷰, 검토, 점검 | code-reviewer | `.claude/agents/code-reviewer.md` |

에이전트를 호출할 때는 해당 에이전트 파일의 규칙과 보고 양식을 따른다.
