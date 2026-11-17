# Task routing

Choose process by **consequence, not line count**. Use the fewest roles that actually reduce risk. Most work should be Tier 0–1.

| Tier | Examples | Process |
| --- | --- | --- |
| 0 — trivial | Typo, copy change, config value, isolated style tweak | Lead implements and verifies. No subagents, no task record. |
| 1 — routine | Local bug, small component, internal behavior change | Lead implements → targeted tests → `code-reviewer`. |
| 2 — feature | New flow, screen, integration, cross-module change | `/feature-delivery`: task record + acceptance criteria, `system-architect` if crossing modules, `qa-engineer` + `code-reviewer`. |
| 3 — high-risk | Auth, payments, privacy/PII, destructive migration, public API change, major architecture change | Tier 2, plus: human approves the plan before coding, `security-engineer`, migration and rollback plan, **independent** review (Codex or human), and human release approval. |

**Escalation triggers.** These bump a change to Tier 3 regardless of size: authorization, secrets, user data exposure, production state, irreversible operations, money, or breaking a public interface. Never downgrade a task to avoid review.

## Core agents (installed by default)
| Agent | Use when | Why it's a subagent |
| --- | --- | --- |
| `code-reviewer` | Any Tier 1+ change is done | Fresh context; not anchored to the implementation |
| `qa-engineer` | Tier 2+, or a bug fix needs a regression test | Tests written by someone other than the implementer |
| `debugger` | Root cause isn't obvious after a quick look | Keeps noisy logs and dead ends out of the main context |
| `research-engineer` | Library/API behavior, version questions, choosing a library | Keeps web research out of the main context |
| `system-architect` | Change crosses module boundaries or alters data model | Focused design pass before code |
| `security-engineer` | Any escalation trigger above | Adversarial read-only pass |

## Library agents (add per project)
Optional agents live in the kit's `library/agents/`. `docs/ai/MINIONS.md` lists which ones this project has added. If an agent isn't in `.claude/agents/`, don't try to call it. Do the work inline, or suggest adding it.

## Coordination rules
- Designer and architect can run in parallel; reconcile their assumptions before implementation.
- QA and code review can run in parallel against the same integrated snapshot.
- Never run parallel writers on overlapping files.
- No agent approves its own work as an "independent" review.
