# Independent review handoff (Codex or another tool)

**Optional; recommended for Tier 3.** A review from a *different* model or tool catches blind spots that Claude reviewing Claude's own work won't. Codex is the default suggestion because it reads the same `AGENTS.md`. Any other capable reviewer, or a human, works too.

How to run it:
- Open the reviewer in a **separate session** against the same repo, a pinned branch, or a worktree.
- Use read-only mode. If tests need to write files, use a separate disposable checkout.
- Give it the task facts and revisions, not Claude's summary of why the change is good.
- Replace every `[bracketed]` value before pasting.

## Before implementation: design review
> Review the proposed design independently. Do not edit files and do not implement the plan. Read `AGENTS.md`, `docs/ai/REVIEW_PROTOCOL.md`, `[task record or design doc path]`, and the relevant existing code and project docs. Base revision: `[commit]`. Check the proposal against the actual architecture, scope, contracts, failure modes, security, and testability. Look for a simpler viable alternative. Report prioritized findings per the review protocol, what you could not check, and a verdict.

## After implementation: code review
> Review this implementation independently. Do not modify files. Read `AGENTS.md`, `docs/ai/REVIEW_PROTOCOL.md`, and `[task record]`, then inspect the diff between `[base commit]` and `[target commit, or working tree incl. untracked files]`. Check acceptance criteria against the actual code, test quality, edge cases, security, data integrity, and regressions. Report findings with `path:line` evidence, impact, suggested verification, and a verdict. State exactly what you ran and didn't run. Do not assume the implementer's reported test results are true.

## Bringing findings back to Claude
Paste the raw findings and the reviewed revision into Claude. Ask Claude to:
1. Validate each finding against the code and record accept, reject, or defer, with evidence, in the task record.
2. Fix accepted blockers, add regression tests, and report the new revision.
3. Send the changed diff back for re-review if the fixes were non-trivial.

**Stop rule:** after two fix-and-review cycles with an unresolved high-severity disagreement, escalate to the human instead of looping.
