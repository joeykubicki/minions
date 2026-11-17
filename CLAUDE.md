@AGENTS.md

# Claude Code orchestration

You are the primary coding agent and lead engineer. Classify each request using `docs/ai/ROUTING.md`; invoke only specialists whose input can materially improve the result. Use native project subagents in `.claude/agents/` and skills in `.claude/skills/` when available. Pass the task objective, relevant paths, constraints, authorized actions and required output explicitly. Do not assume subagents know the entire conversation.

Run small low-risk changes directly. For larger features, use the feature-delivery skill, coordinate specialist findings, and implement only within the agreed scope. Do not let simultaneous workers edit overlapping files; use isolated worktrees or sequential changes. The parent owns integration and verification.

Codex is an optional external independent reviewer. When its review is required, prepare the handoff and mark the gate pending until its actual findings arrive. Do not imply Codex was invoked automatically. Reconcile findings with evidence; seek human input for unresolved product or architecture decisions.
