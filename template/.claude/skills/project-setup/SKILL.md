---
name: project-setup
description: First-time setup after installing the minions kit. Fills AGENTS.md and docs/project/* from the repo (existing code) or from a short interview (new project), and recommends optional library agents. Run once per project, or again after a major change in stack.
---

Set up this project's AI-team docs. Work in this order and keep the human in the loop.

## 1. Detect the situation
- **Existing codebase:** there is real application code. Derive facts from evidence: manifests, lockfiles, CI config, READMEs, scripts, directory layout.
- **New / greenfield:** little or no code yet. You can't infer facts, so **interview the human**. Ask a few short questions at a time: what it is and who it's for, the core use cases, explicit non-goals, the intended stack and platform, constraints (budget, deadline, hosting), and what "v1 done" looks like.
- Mixed: infer what you can, then ask about the rest.

## 2. Fill the docs
Fill each in place. Keep the existing headings. Replace `TBD` only with facts you verified or the human told you. Leave real unknowns as `TBD`.
- `AGENTS.md` → "Project at a glance": one-line purpose, stack, and the **exact** install, run, test, and lint commands. For an existing codebase, run each command once to confirm it works, and note any that fail rather than recording them as working.
- `docs/project/PRODUCT.md`: purpose, users, use cases, scope and non-goals, success criteria.
- `docs/project/ENGINEERING.md`: stack and versions, setup, env var **names** (never values), conventions, test approach, CI.
- `docs/project/ARCHITECTURE.md`: existing codebase only. Describe the current state; don't describe a design you'd like. For greenfield, leave it TBD until there's code.
- `docs/project/DESIGN_SYSTEM.md`: only if the project has a UI. Otherwise set its status line to "Not applicable (no UI)".

Keep each doc short. These are reference pages, not essays.

## 3. Recommend library agents
Read `docs/ai/MINIONS.md` to find the kit's source path. Its `library/README.md` lists optional agents and when each is worth adding. Recommend only the ones this project clearly needs, with one sentence each on why. **Ask before copying any.** Then copy the approved ones from `<source>/library/agents/` into `.claude/agents/` and list them under "Library additions" in `docs/ai/MINIONS.md`. The same README lists add-ons (e.g. `usage-tracking`). Those include hooks, so install them with `<source>/install.sh <project-dir> --add <name>` rather than copying files.

## 4. Optional safety settings
Suggest permission rules for `.claude/settings.json` that fit this stack. For example, add the project's test and lint commands to `permissions.allow` so they don't prompt every time. Show the change and ask before writing it.

## 5. Report
Summarize: what you filled in and from what evidence, what's still TBD, any commands that didn't work, and suggested first tasks. Remind the human to review the docs, since the next sessions will trust them.
