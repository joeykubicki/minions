---
name: feature-delivery
description: Plan and implement a substantial feature or cross-module change with appropriate specialist reviews and verification.
---

Read AGENTS.md and docs/ai/ROUTING.md. Classify scope and risk. For routine changes use the lighter path.
1. Create a task record from docs/templates/TASK.md for substantial work. Clarify acceptance criteria with product-manager when needed.
2. Invoke product-designer for meaningful UI; system-architect for cross-module architecture; risk-specific roles as needed. Reconcile incompatible assumptions. Record plan and decisions.
3. For Tier 3 and other broad/high-risk designs, prepare docs/ai/CODEX_HANDOFF.md before implementation and request independent review. Stop at required approval gates until actual feedback arrives.
4. Implement in the main session or delegate disjoint work. Keep changes scoped and preserve existing changes. Integrate before verification.
5. Invoke QA and code-reviewer for substantial implemented changes. Run actual project checks. Save exact test evidence and review input revision.
6. Request independent Codex code review for high-risk/broad changes; reconcile findings, fix, re-test and re-review changed revisions. Do not mark missing gates passed.
7. Update durable project docs/ADRs if facts or decisions changed. Summarize acceptance criteria, evidence, risks and gate status. Do not merge/deploy without approval.
