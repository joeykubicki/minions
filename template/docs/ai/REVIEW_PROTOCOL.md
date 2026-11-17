# Review protocol

Shared by `code-reviewer`, `security-engineer`, `/review-change`, and any external reviewer.

## Ground rules
- Review an **exact** scope: base and target revision, or a specified diff. A verdict applies only to that snapshot. Later changes need re-review.
- Review independently. Don't accept the implementer's conclusions or reported test results without checking.
- Read-only. If a check needs to write files, run it in an isolated checkout or report it as not run. Never touch production.
- Don't invent findings. A clean review that says "nothing found" is a valid result.

## Design review: look for
Missing states and edge cases, unclear contracts, security and data-lifecycle gaps, compatibility breaks, operational cost, failure and recovery, testability, and a **simpler alternative** that would do the job.

## Code review: look for
Defects **introduced or exposed** by this change. Trace execution paths, compare against acceptance criteria, check error paths, and check whether tests would actually fail if the change were wrong. List pre-existing issues and optional improvements separately, briefly.

## Finding format
```
[ID] P1 — Short title
Location: path/to/file.ts:42
Evidence / failure scenario: what input or state leads to what wrong outcome
Impact: who or what is affected
Fix: specific remediation
Verify: how to confirm the fix
Confidence: high | medium | low
```

## Severity
- **P0:** security compromise, severe data loss, or outage. Blocks release.
- **P1:** substantial correctness, reliability, security, or compatibility defect. Blocks release.
- **P2:** bounded defect or important gap. Needs an explicit decision (fix now, defer with a ticket, or accept) before merge.
- **P3:** minor issue or optional refinement. Label optional items as optional.

## Verdict
**PASS** / **PASS WITH FOLLOW-UPS** / **CHANGES REQUIRED** / **INCOMPLETE** (couldn't finish, so the gate isn't met).
A missing reviewer is never a pass. The human resolves disagreements about scope or risk.

Record in the task record: reviewer (and model or tool), revisions reviewed, checks run, findings, and how each was resolved.
