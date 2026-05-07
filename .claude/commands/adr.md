Architecture Decision Record를 생성한다.

$ARGUMENTS 는 ADR 제목이다. 없으면 제목을 물어본다.

순서:
1. 오늘 날짜를 YYYY-MM-DD 형식으로 확인한다.
2. `.claude/docs/architecture/TEMPLATE.md`를 읽는다.
3. `.claude/docs/architecture/decisions/YYYY-MM-DD-<제목 소문자-하이픈>.md` 파일을 TEMPLATE.md 내용으로 생성한다.
   - 제목과 날짜를 채운다. 나머지 섹션은 빈 채로 둔다.
4. `.claude/docs/architecture/README.md`의 인덱스 테이블에 한 줄 추가한다.
   - 형식: `| [제목](decisions/파일명) | 검토 중 | YYYY-MM-DD |`

완료 후 생성된 파일 경로를 알린다.
