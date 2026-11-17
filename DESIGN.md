# Design notes

Why the kit is shaped the way it is. Read this before adding or changing agents and skills, so the kit stays small and coherent as it grows.

## Principles
1. **The human owns decisions; the lead owns execution.** The main Claude session is the only agent that talks to you, so it owns scope clarification, integration, and the final report.
2. **Process scales with consequence.** Tier 0 has no ceremony. Tier 3 gets plan approval and independent review. Most work should feel lightweight.
3. **Evidence over claims.** Every agent separates verified facts from assumptions and never reports an unrun check as passing.
4. **Small core, opt-in library.** Every installed agent and skill description costs context on every turn, and gives the lead one more thing it might delegate to unnecessarily. Only things that earn their keep in most projects go in the core.
5. **Markdown is guidance, not enforcement.** Real guardrails are tool allowlists, `settings.json` permissions, sandboxing, branch protection, and CI. The prose tells agents what to do; those settings stop them when they don't.
6. **Grow by evidence.** Change the kit when a real project shows a gap (see the feedback loop in the README), not because a role sounds nice to have.

## When a subagent is worth it
A subagent is a fresh Claude instance with its own context window, its own system prompt (the agent file body), and a restricted toolset. That's useful for exactly three things:

| Benefit | Example |
| --- | --- |
| **Fresh eyes** | `code-reviewer` hasn't seen the reasoning that led to the code, so it's less likely to share the implementer's blind spots. |
| **Context isolation** | `debugger` and `research-engineer` churn through logs and web pages, and return only the conclusion. The main session stays clean. |
| **Parallelism** | QA and review running at the same time on the same snapshot, or two implementers on disjoint files. |

It is **not** worth it for "role-playing" a job the lead could do inline. Delegating has real costs: the subagent re-reads the code from scratch, can't see the conversation, can't ask you questions, and its output must be integrated. That's why the original framework's 15 agents became 6 core + 9 library:
- **Moved to the library:** `frontend-engineer` and `backend-engineer`. The lead implements by default, so these only help for parallel work. `product-manager` was moved because scoping is mostly a conversation with you, which a subagent can't have. Domain specialists (database, devops, performance, AI, design, docs) only matter for projects that have that domain.

## How Claude Code loads these files
Verified against the Claude Code docs (Nov 2026). Re-check when something seems off: <https://code.claude.com/docs/en/sub-agents>, <https://code.claude.com/docs/en/skills>.

- **`CLAUDE.md`** loads into every session. `@AGENTS.md` on its first line imports the shared file, so Claude and Codex read the same rules.
- **Subagents also load `CLAUDE.md`**, and therefore `AGENTS.md`. Two consequences:
  - Agent files don't need to say "read AGENTS.md". They already have it.
  - Lead-only instructions in `CLAUDE.md` are read by subagents too, which is why that section starts with "If you are a subagent, skip this section."
- **Subagents don't get** the main conversation, auto-memory, or the ability to ask you anything. Anything they need must be in the delegation prompt.
- **Agent `description`** is always in the lead's context and is how it decides when to delegate. Write it as *what + when* ("Use after…", "Use when…"). Keep it short; put instructions in the body, which only loads when the agent runs.
- **Agent `tools`** is an allowlist. Leaving out `Agent` means the subagent can't spawn more subagents. Note that `Bash` can write files, so "read-only + Bash" is a promise kept by the prompt, not by the tool list.
- **Skill `description`** is always in context. The `SKILL.md` body loads only when the skill is invoked (by `/name` or by Claude deciding it fits). `$ARGUMENTS` is replaced with whatever follows `/name`.
- **`disable-model-invocation: true`** hides a skill from Claude entirely, so only `/name` can run it. Use it for skills with real side effects (deploy, publish). It's not used here, because hidden skills confuse the lead when `CLAUDE.md` mentions them.
- **YAML gotcha:** a `: ` inside an unquoted `description` breaks the frontmatter and the file silently fails to load. Use parentheses or quote the value.
- **Settings:** `.claude/settings.json` is committed and shared. `.claude/settings.local.json` is personal and gitignored. `deny` rules apply immediately; `allow` rules wait for the folder to be trusted.

## Why Codex (or anything else) as the independent reviewer
Claude reviewing Claude's work catches a lot, but it's the same model with correlated blind spots. A different model, or a human, is a genuinely independent check. It's reserved for Tier 3 because it costs a manual round-trip. The handoff is copy-paste on purpose for now: it's simple, auditable, and works without wiring two tools together. Automating it is on the roadmap.

## Why copy-into-project (for now) instead of a plugin
Claude Code plugins can package agents and skills, install them from a GitHub repo, and update centrally. That's the natural long-term home for the generic agents and skills. For v1, plain copying wins because:
- Each project can tweak its agents without forking anything.
- Project docs (`docs/project/*`, `AGENTS.md`) must be per-project files anyway.
- There's nothing to learn or debug beyond "files in `.claude/`."

Per-project tweaks are expected, not a failure. The project's `CLAUDE.md` lets Claude propose changes to its agents and skills when something about the project calls for it, with a reason and your approval. Each change is logged under "Local customizations" in `docs/ai/MINIONS.md`, and lessons that apply to any project go under "Feedback for the kit." Any future plugin version has to keep this ability, e.g. a plugin provides the defaults and the project's `.claude/agents/` overrides them, since project agents take precedence over plugin agents.

The cost is drift: projects don't get kit improvements automatically. `docs/ai/MINIONS.md` records the installed version to make manual upgrades easier. Revisit once the agents stabilize (see ROADMAP).

## Style guide for agents and skills
Agent files (`template/.claude/agents/`, `library/agents/`):
```markdown
---
name: kebab-case-name
description: <What it does>. Use when <trigger>. <Read-only | May edit X only>.
tools: <minimal allowlist>
model: inherit
color: <optional: red|blue|green|yellow|purple|orange|pink|cyan>
---
# Title
One line: who you are and what you hand back.
## Contract   – scope, what you may/may not change, how to label evidence
## Method     – numbered steps; concrete, not aspirational
## Output     – the exact sections the lead should get back
```
- Give the narrowest toolset that works. Advisory roles get `Read, Grep, Glob`.
- Make method steps concrete enough that a different model would do the same thing.
- Every agent should have a clear "done" condition and an explicit way to say "I found nothing" or "I'm blocked."

Skills (`template/.claude/skills/<name>/SKILL.md`):
- Keep the frontmatter `description` to *what + when*. Keep the body to numbered steps, under ~60 lines; move long reference material into a sibling file the skill links to.
- Reference docs by path rather than copying them in, so there's one source of truth.
