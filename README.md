# embedded-ai-harness

Claude Code용 **자기점검형(self-checking) 에이전트 하네스**. 두 가지 원칙(최소주의·SSOT)을 규칙으로 못박고, 훅과 검증 스크립트로 그 규칙이 깨지지 않는지 자동 감시한다.

프로젝트에 종속되지 않은 범용 템플릿이다. 아무 프로젝트에나 `.claude/`와 `CLAUDE.md`를 복사해 사용한다.

## 사용법

```bash
# 대상 프로젝트 루트에서
cp -r /path/to/embedded-ai-harness/.claude   ./.claude
cp    /path/to/embedded-ai-harness/CLAUDE.md ./CLAUDE.md
```

이후 Claude Code가 세션 시작 시 `CLAUDE.md`의 Session Init 절차에 따라 메모리를 읽고, 요청 유형에 맞는 서브 에이전트로 라우팅한다.

## 구성

```
.claude/
├── agents/        4개 전문 서브 에이전트 (역할 분리)
│   ├── implementer.md          구현 (코드 작성·수정·버그픽스)
│   ├── evaluator.md            검증 (테스트·벤치마크 실행·비교)
│   ├── algorithm-developer.md  설계 (방안 설계·조사, 구현은 안 함)
│   └── code-reviewer.md        리뷰 (정확성·스타일·제약 검토, 수정 안 함)
├── commands/      슬래시 커맨드
│   ├── adr.md         /adr        — 아키텍처 결정 기록 생성
│   ├── log-error.md   /log-error  — 오류를 ERRORS.md에 기록
│   └── validate.md    /validate   — 동기화 갭 검사 실행
├── hooks/         자동 훅 (settings.json에 연결)
│   ├── post-edit.sh       파일 수정 후 validate.py 자동 실행
│   ├── post-bash-fail.sh  Bash 실패 시 /log-error 안내
│   └── on-stop.sh         응답 종료 시 메모리 갱신 리마인더
├── memory/        세션 간 지속 메모리
│   ├── MEMORY.md      인덱스 (세션 시작 시 필독)
│   ├── ERRORS.md      반복 오류 로그
│   ├── minimalism.md  최소주의 원칙
│   └── ssot.md        SSOT 원칙
├── docs/architecture/  ADR (아키텍처 결정 기록) + 템플릿
├── scripts/validate.py 하네스 구성요소 간 정합성 검사기
└── settings.json       훅 등록
```

## 핵심 원칙

- **최소주의** — 요청된 것만, 인접 코드 손대지 않기, 확인 없이 완료 선언 금지
- **SSOT** — 하나의 사실은 한 곳에서만 정의하고 나머지는 참조

## 동기화 갭 검사

파일을 수정하면 `post-edit` 훅이 `validate.py`를 자동 실행해 다음을 검사한다:

- 에이전트에 필수 섹션(`## 역할`·`## 시작 전 필수`·`## 보고 양식`)과 `ERRORS.md` 참조가 있는가
- `MEMORY.md` 인덱스 ↔ 실제 memory 파일 일치, 죽은 링크 여부
- 커맨드 정의 여부
- ADR 인덱스 정합성
- (`--git-diff`) 에이전트 변경 시 메모리 미갱신, 신규 ADR 미등록

수동 실행:

```bash
python .claude/scripts/validate.py --git-diff
```

## 프로젝트 종속 항목

`settings.local.json`(프로젝트별 권한)은 `.gitignore`로 제외한다. 각 프로젝트에서 개별 관리한다.
