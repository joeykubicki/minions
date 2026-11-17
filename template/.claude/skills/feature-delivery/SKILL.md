---
name: feature-delivery
description: Plan, implement, verify, and review a substantial feature or cross-module change (Tier 2+). Use when the user asks for a new feature, flow, screen, integration, or significant change that needs a plan before code.
argument-hint: "[feature description]"
---

Deliver this feature: $ARGUMENTS

Classify the risk tier with `docs/ai/ROUTING.md` first. If it's actually Tier 0–1, say so and just do it without this process.

## 1. Scope (with the human)
- Restate the goal, in-scope items, out-of-scope items, and **testable acceptance criteria**. Ask the human about anything ambiguous. This is the step where talking to the human matters most, and subagents can't do it.
- Create a task record in `docs/work/` from `docs/templates/TASK.md`.

## 2. Design
- Cross-module or data-model changes: delegate to `system-architect`.
- Auth, secrets, user data, payments, or other escalation triggers: also delegate to `security-engineer` for a design-level review.
- If the project has added library agents (see `docs/ai/MINIONS.md`), use them where relevant, e.g. `product-designer` for new UI or `database-engineer` for schema changes.
- Reconcile conflicting advice. Record the plan in the task record and draft an ADR for significant decisions.
- **Tier 3:** get the human's explicit approval of the plan before writing code. An independent design review (`docs/ai/CODEX_HANDOFF.md`) is recommended.

## 3. Implement
- Implement in the main session by default. Delegate only disjoint pieces, never overlapping files in parallel.
- Keep changes inside the agreed scope. If scope needs to grow, stop and ask.

## 4. Verify
- Run the project's real checks (see `AGENTS.md`). Delegate test-writing to `qa-engineer` for independent coverage of the acceptance criteria.
- Delegate to `code-reviewer`, plus `security-engineer` if triggers apply. QA and review can run in parallel against the same snapshot.
- Fix confirmed findings, re-run checks, and re-review the changed parts.

## 5. Close out
- **Tier 3:** request independent code review (`docs/ai/CODEX_HANDOFF.md`) and mark it pending until findings actually arrive.
- Update `docs/project/*` and ADRs if durable facts changed.
- Report: each acceptance criterion with evidence, checks run, review verdicts and dispositions, open risks, and decisions the human still needs to make.
- Don't merge or deploy without approval.
