---
name: review-change
description: Evidence-based review of the current diff, a branch, or a specific revision, with no edits. Use when the user asks to review changes, a PR, or a branch before merging.
argument-hint: "[base..target, branch, or blank for working tree]"
---

Review: $ARGUMENTS (blank means the current working tree vs. HEAD, including relevant untracked files)

1. **Pin the scope.** Resolve the exact base and target revisions and list the files in scope. State them in the report so the verdict is tied to a specific snapshot.
2. **Classify risk** with `docs/ai/ROUTING.md` from what the diff actually touches.
3. **Delegate** to `code-reviewer` with the scope. If escalation triggers apply, also delegate to `security-engineer`. Run them in parallel when both apply.
4. **Make no edits** during review. That includes "quick fixes."
5. **Consolidate.** Deduplicate findings, sort by severity per `docs/ai/REVIEW_PROTOCOL.md`, and drop anything you can't support with evidence.
6. **Independent review.** For Tier 3, prepare the prompt from `docs/ai/CODEX_HANDOFF.md` with the real revisions filled in, and mark the independent gate **pending**.
7. **Report:** scope, findings, checks run and not run, verdict, and gate status.
