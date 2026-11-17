# Task routing

Choose by consequence, not line count. Use the fewest roles that materially reduce risk.

| Tier | Examples | Process |
| --- | --- | --- |
| 0 — trivial | Typo, label, small isolated styling token | Lead implements and verifies locally. No specialist or task record required. |
| 1 — routine | Local bug, small component or internal behavior | Lead + relevant specialist if needed; targeted regression checks. |
| 2 — feature | New flow, screen, integration, cross-module change | Product manager if scope unclear, designer for UI, architect for cross-module contracts, QA and reviewer. Track a task record and acceptance criteria. |
| 3 — high-risk | Auth, payment, privacy, destructive data migration, public API compatibility, major architectural change | Explicit approval of plan, relevant specialists, independent design and code review, migration/rollback strategy and release approval. |

Escalation triggers (even for small diffs): authorization, secrets, data exposure, production state, irreversible operations, money, or breaking public interfaces. Never downgrade a task to avoid review.

## Role triggers
- `product-manager`: unclear scope, competing priorities, acceptance criteria, multi-step delivery.
- `product-designer`: new or meaningfully changed UI/UX, navigation or interactions.
- `system-architect`: cross-module boundaries, new services, integrations, architectural tradeoffs.
- `frontend-engineer`: complex client-side or native UI implementation; use only if delegated.
- `backend-engineer`: API, service, job or business-logic implementation; use only if delegated.
- `database-engineer`: schema, queries, migrations, constraints, data integrity.
- `qa-engineer`: test planning, independent regression coverage, verification.
- `code-reviewer`: implementation review for correctness and maintainability.
- `security-engineer`: auth, permissions, secrets, privacy, third-party inputs.
- `performance-engineer`: suspected or measured latency, load, cost, memory or rendering issues.
- `devops-engineer`: CI, deployment, environments, release and rollback planning.
- `debugger`: failures with unclear root cause, hard-to-reproduce regressions.
- `documentation-engineer`: API documentation, onboarding, architecture docs, releases.
- `research-engineer`: uncertain library/API behavior, technical spikes, feasibility.
- `ai-engineer`: LLM prompts, retrieval, evaluations, agent systems, AI costs and failure modes.

Designer and architect can work in parallel if independent; reconcile assumptions before implementation. QA and code review can work in parallel against the same integrated snapshot. Avoid overlapping writes; never have the same agent approve its own work as an independent review.
