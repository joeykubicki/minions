# Changelog

## 0.3.0 — 2026-11-18
**Added**
- **`usage-tracking` add-on** (`./install.sh <project> --add usage-tracking`). It measures the Claude Code work that went into a project: tokens first, then active time and an API-equivalent cost estimate.
  - `.claude/usage/usage.py` (Python 3, standard library only) reads the project's local transcripts, subagents included. It counts each API request once and appends the usage to a gitignored ledger, so numbers survive Claude Code's 30-day transcript cleanup.
  - A `SessionEnd` hook keeps the ledger current.
  - `/usage-report` writes a committed `docs/ai/USAGE.md` with totals and breakdowns by model, agent, day, and session.
  - Tested against real project histories: the cost estimate came within 0.3% of Claude Code's own per-session cost records.
- **Add-ons in the library** (`library/addons/<name>/`): a `files/` tree plus an optional `settings.json` hooks fragment. `install.sh --add` and `--list` handle add-ons as well as agents, and merge an add-on's hooks into the project's `.claude/settings.json` without duplicating them on a re-run.

**Changed**
- `docs/ai/MINIONS.md`: "Library agents added" is now "Library additions", covering both agents and add-ons. `/project-setup` mentions add-ons when it recommends library agents.

## 0.2.0 — 2026-11-17
First structured revision of the initial framework.

**Fixed**
- Agents and skills now install to `.claude/` (the extracted copy had `claude/` with no dot, so Claude Code found none of them).
- Subagents load `CLAUDE.md`, so they were reading the "you are the lead" instructions. That section now tells subagents to skip it.
- Removed the "Read AGENTS.md" boilerplate from every agent, since subagents already load it.

**Changed**
- Split the 15 agents into 6 **core** (installed by default: code-reviewer, qa-engineer, debugger, research-engineer, system-architect, security-engineer) and 9 **library** agents (opt-in via `install.sh --add`).
- Rewrote agent descriptions as "what + when" triggers, and the bodies as Contract / Method / Output.
- Rewrote skills as numbered steps with `$ARGUMENTS` and argument hints.
- `AGENTS.md` now has a "Project at a glance" block for commands, the most-used facts in any session.
- The Codex handoff is explicitly optional and tool-agnostic. The review protocol has a concrete finding template.

**Added**
- `/project-setup` skill: fills project docs from code (existing repo) or an interview (greenfield), and recommends library agents.
- `install.sh`: a no-overwrite installer that records the kit version.
- `.claude/settings.json`: deny reading `.env` files, ask before `git push`.
- `docs/ai/MINIONS.md` per project: kit version, added agents, local customizations, and a feedback log.
- Per-project tailoring rule in `CLAUDE.md`: Claude may propose project-specific changes to kit agents and skills, with a stated reason and your approval, and logs them in `MINIONS.md`.
- MIT `LICENSE`.
- Repo docs: README, DESIGN (rationale, loading behavior, style guide), ROADMAP (v1 criteria), this changelog.

## 0.1.0 — 2026-11-17
Initial framework generated with ChatGPT (`ai-coding-team-starter.zip`): 15 agents, 3 skills, routing tiers, review protocol, Codex handoff, project doc templates.
