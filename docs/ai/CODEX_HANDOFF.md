# Codex handoff

Open Codex in a separate session against the same repository or a pinned branch/worktree. Configure read-only sandboxing for review; if testing needs writes, use a separate authorized disposable workspace. Replace bracketed values. Codex does not need Claude's private conversation; provide task facts and revision rather than persuasive summaries.

## Before implementation — paste into Codex
Review the proposed design independently, without editing files. Read AGENTS.md, docs/ai/REVIEW_PROTOCOL.md, [task record or design path], and relevant existing code and project docs. The base revision is [commit]. Verify the proposal against actual architecture, scope, contracts, failure modes, security and testability. Look for simpler viable alternatives. Report prioritized findings using the review protocol, coverage limitations and a verdict. Do not implement the plan.

## After implementation — paste into Codex
Review the implementation independently and do not modify files. Read AGENTS.md, docs/ai/REVIEW_PROTOCOL.md, [task record], and inspect the diff between [base commit] and [target commit, or exact working-tree snapshot including relevant untracked files]. Check acceptance criteria against the actual code, test quality, edge cases, security, data integrity and regressions. Report findings with file/line evidence, impact, suggested verification and verdict. State precisely what you did and did not run. Do not assume Claude's reported tests passed.

## Return findings to Claude
Provide the raw review findings and reviewed revision. Ask Claude to validate each independently, record accept/reject/defer with evidence, fix confirmed blockers, add regression checks, and report the new revision. Send the changed diff back to Codex when appropriate. Never loop indefinitely: after two fix/review cycles with unresolved high-risk disagreement, escalate to the human.
