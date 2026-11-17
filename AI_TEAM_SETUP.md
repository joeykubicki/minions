# AI coding team starter kit

This scaffold targets Claude Code as lead and Codex as optional independent reviewer. It is framework-neutral and contains no runnable application code or automatic cross-provider orchestration.

## Install
1. Inspect the files and merge them into the repository root. Do not overwrite existing AGENTS.md, CLAUDE.md, docs or agent definitions blindly. Include hidden `.claude/` directories.
2. Ask Claude to inspect the repository and populate docs/project/ from evidence; review and correct the result. Leave unknowns marked TBD.
3. Start a fresh Claude Code session, check `/agents` and `/memory` or `/context all`, and verify project instructions and profiles are visible. Start Codex separately and confirm it loads AGENTS.md. Native subagent availability and permissions depend on version and configuration.
4. Test on a small non-production change, then try a feature. Use `/feature-delivery`, `/bug-fix`, or `/review-change` in Claude Code when available, or ask for the workflow in natural language.
5. For Codex audits, use docs/ai/CODEX_HANDOFF.md with the actual revision and task record. It deliberately uses a manually launched independent session rather than an automatic bridge. If Codex is unavailable, record required review as pending.

## Design choices
- Shared AGENTS.md is canonical; CLAUDE.md imports it and provides lead-agent behavior.
- Role definitions are native Claude Markdown profiles with explicit triggers and tool lists. Codex can read any role file as a reference, but does not automatically register Claude's subagents. No duplicate Codex role registry is needed for the independent session.
- Most specialist profiles are advisory; frontend/backend, scoped QA and documentation roles may edit assigned files. Bash can also write, so tool lists and Markdown descriptions are not a sandbox. Configure actual permissions, worktrees and CI separately.
- Project information, procedures and task records are separate. Avoid copying all docs into startup context.
- No pinned models, framework assumptions, deployment hooks, CI pipelines, or external tools are configured. Choose real tests and enforcement per repo. No automatic Codex invocation is included.

## References
- Claude Code custom subagents: https://code.claude.com/docs/en/sub-agents
- Claude Code project instructions and AGENTS.md import: https://code.claude.com/docs/en/memory
- Codex project instructions: https://learn.chatgpt.com/docs/agent-configuration/agents-md
- Codex subagents: https://learn.chatgpt.com/docs/agent-configuration/subagents
