# Independent review protocol

Review the explicit task scope and exact base/target revision or supplied diff. Review independently rather than accepting the implementer's conclusion. In read-only mode do not modify files; if tests are necessary and write generated outputs, use an authorized isolated workspace or report that they were not run. Never deploy or access production.

## Design review
Read acceptance criteria, proposed design, actual repository boundaries, relevant ADRs and constraints. Challenge assumptions, missing states, contracts, security, data lifecycle, compatibility, operational cost, failure modes, testability and alternatives as relevant. Prefer simpler solutions when justified by evidence.

## Code review
Inspect actual changes and surrounding code, trace execution paths, compare to acceptance criteria, validate error paths and regressions, and inspect tests for behavioral coverage. Identify concrete defects introduced or exposed by the change; separate pre-existing issues and optional improvements.

## Finding format
- Stable ID, severity (P0 critical, P1 high, P2 medium, P3 low), title.
- Location (path:line or section), evidence and failure scenario, impact.
- Specific remediation or alternative, suggested verification, confidence (high/medium/low).
- State assumptions and coverage limits. Do not invent findings. Distinguish confirmed defects from hypotheses.

P0: security compromise, severe data loss, or catastrophic failure. P1: substantial correctness, reliability, security or compatibility defect. P2: bounded defect or important gap. P3: minor concrete defect or optional refinement (label optional items explicitly).

Verdict: PASS / PASS WITH FOLLOW-UPS / CHANGES REQUIRED / INCOMPLETE. Unresolved P0/P1 block release; an incomplete mandatory review blocks the gate. P2 items require explicit disposition before merge. The human resolves disagreements involving scope/risk. Do not call a missing reviewer a pass.

Record reviewer, model/tool when known, base/target revision (and diff identity if dirty), files/checks reviewed, findings, disposition, and whether changes need re-review. After fixes, review the new revision; a prior verdict is not approval of subsequent changes.
