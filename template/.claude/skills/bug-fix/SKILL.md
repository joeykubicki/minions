---
name: bug-fix
description: Reproduce, root-cause, and fix a bug with a regression test and evidence. Use when the user reports a bug, error, failing test, or unexpected behavior and wants it fixed.
argument-hint: "[bug description or issue link]"
---

Fix this bug: $ARGUMENTS

1. **Pin down the bug.** Expected vs. actual behavior, how to trigger it, and the risk tier from `docs/ai/ROUTING.md`. If the report is too vague to reproduce, ask the human before guessing.
2. **Reproduce** with the smallest safe command and capture the real output. If the root cause isn't obvious after a quick look, delegate to the `debugger` subagent with the reproduction and relevant paths.
3. **Write a failing regression test** that captures the bug, when practical. Confirm it fails for the right reason.
4. **Implement the smallest fix** that addresses the root cause, not just the symptom. Don't refactor nearby code in the same change.
5. **Verify.** The regression test now passes, the original reproduction is resolved, and the relevant existing checks still pass.
6. **Review by tier.** Tier 1: delegate to `code-reviewer`. Tier 3, or any escalation trigger: also `security-engineer`, and mark an independent review pending (see `CLAUDE.md`).
7. **Report:** root cause, changed files, tests and checks run with results, anything unverified, review status. If you noticed unrelated failures, mention them. Don't hide them, and don't fix them in this change.
