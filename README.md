# minions

A living kit of Claude Code **agents, skills, and working agreements** that you drop into a new project, so every project starts with the same AI engineering team and process. Each project you use it on should make the kit a little better.

- **Lead:** Claude Code in your main session plans, implements, and integrates.
- **Specialists:** a small set of subagents for the jobs where a separate context window actually helps: review, testing, debugging, research, architecture, and security.
- **Optional second opinion:** Codex (or any other tool or human) as an independent reviewer for high-risk changes.
- **You:** own scope, tradeoffs, and anything irreversible.

> Status: **v0.2, pre-proof-of-concept.** See [ROADMAP.md](ROADMAP.md) for what "v1" means.

## Quick start

```bash
# 1. Install the core kit into a project. It never overwrites existing files.
./install.sh ~/code/my-project

# 2. Optionally, add specialists the project needs.
./install.sh --list
./install.sh ~/code/my-project --add database-engineer product-designer

# 3. Open the project in Claude Code and run setup.
cd ~/code/my-project && claude
> /project-setup
```

`/project-setup` fills in `AGENTS.md` and `docs/project/*`. For an existing codebase it reads the code; for a brand-new project it interviews you. It then recommends which library agents to add.

Check that it worked: `/agents` should list the core agents, and typing `/` should show the skills.

## What gets installed

```
your-project/
├── AGENTS.md                 # shared rules + project commands (Claude and Codex both read this)
├── CLAUDE.md                 # imports AGENTS.md, plus lead-engineer behavior for Claude
├── .claude/
│   ├── settings.json         # blocks reading .env files, asks before git push
│   ├── agents/               # 6 core subagents
│   │   ├── code-reviewer.md      fresh-context review after changes
│   │   ├── qa-engineer.md        independent tests (edits test files only)
│   │   ├── debugger.md           root-cause investigation (no edits)
│   │   ├── research-engineer.md  docs/web research (no edits)
│   │   ├── system-architect.md   design before cross-module work (no edits)
│   │   └── security-engineer.md  security review for risky changes (no edits)
│   └── skills/
│       ├── project-setup/    /project-setup     first-time setup
│       ├── feature-delivery/ /feature-delivery  plan → build → verify → review
│       ├── bug-fix/          /bug-fix           reproduce → test → fix → verify
│       └── review-change/    /review-change     review a diff or branch
└── docs/
    ├── ai/                   # how the AI team works (routing tiers, review protocol, Codex handoff)
    │   └── MINIONS.md        # installed kit version, plus feedback to bring back to the kit
    ├── project/              # facts about THIS project (product, engineering, architecture, design)
    ├── decisions/            # ADRs
    ├── templates/            # TASK.md, ADR.md
    └── work/                 # task records for in-flight Tier 2+ work
```

## How the process scales

Work is sorted into tiers by **consequence**, not size (`docs/ai/ROUTING.md`):

| Tier | Example | What happens |
| --- | --- | --- |
| 0 | typo, config tweak | Claude just does it |
| 1 | small bug, small component | implement → test → `code-reviewer` |
| 2 | new feature or flow | `/feature-delivery`: task record, design pass, QA + review |
| 3 | auth, payments, data migrations | Tier 2 + your plan approval, security review, independent review |

Most day-to-day work should be Tier 0–1. The heavier process exists for when a mistake would be expensive.

## This repo

| Path | What it is |
| --- | --- |
| `template/` | Exactly what `install.sh` copies into a project |
| `library/agents/` | Optional specialists, added per project with `--add` ([index](library/README.md)) |
| `install.sh` | No-overwrite installer |
| [DESIGN.md](DESIGN.md) | Why it's built this way, how Claude Code loads these files, and a style guide for writing agents and skills |
| [ROADMAP.md](ROADMAP.md) | v1 criteria and the improvement backlog |
| [CHANGELOG.md](CHANGELOG.md) | What changed in each version |

## Making it better over time

1. While working in a project, when an agent or skill gets something wrong or misses something, Claude (or you) adds a line to that project's `docs/ai/MINIONS.md` under **Feedback for the kit**.
2. Every so often, collect those notes and apply the good ones here. Opening Claude Code in this repo works well for that.
3. Bump `VERSION` and add a `CHANGELOG.md` entry.
4. Upgrading an existing project is manual for now: `diff -ru template/ ~/code/my-project/`, then copy over what you want. An `--upgrade` mode is on the roadmap.

## Requirements
- [Claude Code](https://code.claude.com/docs). Agents and skills use its native `.claude/agents` and `.claude/skills` formats.
- Optional: [Codex](https://learn.chatgpt.com/docs/agent-configuration/agents-md) for independent review. It reads `AGENTS.md` natively.
- macOS or Linux shell for `install.sh`.

## License
[MIT](LICENSE). Use it, fork it, adapt it.
