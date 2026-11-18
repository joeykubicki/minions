# Roadmap

## v1.0 proof of concept: definition of done
The kit is "v1" when it's been used for real, not just written. Check these off:

- [ ] Installed into one **greenfield** project, and `/project-setup` produced usable `PRODUCT.md` / `ENGINEERING.md` from the interview.
- [ ] Installed into one **existing** codebase, and `/project-setup` filled in correct, working commands in `AGENTS.md`.
- [ ] Each core agent used at least once on real work, with output that was actually useful. Note duds in `MINIONS.md` feedback.
- [ ] `/feature-delivery` run end to end on one Tier 2 feature.
- [ ] `/bug-fix` run on at least one real bug.
- [ ] Feedback from those projects collected and applied here.
- [x] License chosen (MIT).
- [x] Repo public on GitHub (https://github.com/joeykubicki/minions).

## Next up (small, high value)
- **`--upgrade` mode for `install.sh`:** show diffs for kit-owned files (`.claude/agents`, `.claude/skills`, `docs/ai/*`) and update them, never touching `docs/project/*` or `AGENTS.md`.
- **Validation script / CI:** parse every agent and skill frontmatter (catches the silent `: ` YAML failure), check required fields, and check that `install.sh` runs cleanly into a temp dir. Run as a GitHub Action.
- **Usage tracking (`usage-tracking` add-on).** Goal: show how efficiently a project was built with AI, e.g. "built in X tokens over Y active hours", without having to check claude.ai.
  - ~~**v0.3.0: ledger + report.**~~ Shipped as the `usage-tracking` add-on ([README](library/addons/usage-tracking/README.md)). Not yet included: lines of code changed, and sessions in worktrees outside the project folder.
  - **v0.3.1: per-task attribution.** Each request is attributed in this order: (1) the task tag active at its timestamp, set and cleared automatically by `/feature-delivery` and `/bug-fix`, or manually for ad-hoc work; (2) the git branch, unless it's `main`, `master` or `HEAD`; (3) otherwise "untagged", listed by session title. The report shows the share of tokens attributed to a task, so gaps stay visible. Branch-only attribution was ruled out: about 86% of real requests across past projects ran on `main` or `HEAD`.
  - **Later: status line.** A `statusline` add-on showing 5-hour and 7-day limit usage with reset times, read from the status line's `rate_limits` input, plus context % and session cost. It's a user-level setting, so it ships with setup steps rather than through `install.sh`. A history dashboard can come later if there's a real need.
- **Hooks:** a `PostToolUse` hook that runs the project's formatter or linter after edits. Per-stack, so it probably belongs in `/project-setup` as a suggestion.

## Later (once there's evidence it's needed)
- **Plugin packaging:** ship the generic agents and skills as a Claude Code plugin + marketplace from this GitHub repo, so improvements reach every project via `/plugin update`. The project-docs scaffold stays a copy-in template. See DESIGN.md for the tradeoff.
- **Automated Codex review:** have the lead invoke Codex non-interactively for Tier 3 reviews instead of copy-paste.
- **Model tiering:** try cheaper models (`model: sonnet` / `haiku`) for research and exploration agents, and keep the strongest for review and architecture. Measure before committing.
- **Agent memory:** the subagent `memory: project` field, so e.g. `code-reviewer` remembers recurring issues in a codebase.
- **Stack packs:** `library/stacks/<stack>/` with stack-specific settings, hooks, and conventions (e.g. Next.js, Python/FastAPI, iOS).
- **More skills, if real usage asks for them:** `/spike` (time-boxed research → recommendation), `/release-check` (pre-release checklist), `/pr-description`, `/retro` (end of task: what should the kit learn?).
- **Evals:** a few fixed scenarios (planted bug, insecure endpoint) to check that agents still catch what they should after edits to their prompts.

## Ideas parked on purpose
- A full PM/designer/eng "org chart" running autonomously. The lead + specialists model is easier to steer and debug; revisit only if a real project hits its limits.
