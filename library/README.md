# Library

## Agents

Optional specialists. Add only the ones a project actually needs:

```bash
./install.sh <project-dir> --add <name> [<name>...]
```

`/project-setup` will recommend some based on the project. Once added, list them in the project's `docs/ai/MINIONS.md`.

| Agent | Add when the project… | Mode |
| --- | --- | --- |
| `database-engineer` | has a relational DB with migrations, or data integrity matters | read-only |
| `product-designer` | has a meaningful UI and no designer | read-only, returns a spec |
| `ai-engineer` | calls LLMs (prompts, RAG, agents, evals) | read-only |
| `devops-engineer` | has CI/CD, infrastructure config, or real deployments | read-only, never deploys |
| `performance-engineer` | has latency, cost, or scale concerns you can measure | measures, no edits |
| `documentation-engineer` | has external users of its API or docs | edits docs only |
| `product-manager` | is large or ambiguous enough to need written scope and milestones | read-only (lead relays questions to you) |
| `frontend-engineer` | needs parallel UI implementation on disjoint files | edits assigned paths |
| `backend-engineer` | needs parallel backend implementation on disjoint files | edits assigned paths |

These follow the older, more compact body format from v0.1 (Responsibilities / Output). When one gets real use and feedback, rewrite it in the core agents' Contract / Method / Output format (see DESIGN.md's style guide). If a library agent turns out to be useful in most projects, promote it to `template/.claude/agents/`.

## Add-ons
Add-ons are more than one file: scripts, skills, and hooks. `install.sh --add <name>` copies `library/addons/<name>/files/` into the project without overwriting anything, then merges the add-on's hooks into `.claude/settings.json`. List them under "Library additions" in the project's `docs/ai/MINIONS.md` as well.

| Add-on | Add when you want… | Adds |
| --- | --- | --- |
| [`usage-tracking`](addons/usage-tracking/README.md) | to show how many tokens and how much active time a project took to build | `/usage-report`, a local usage ledger, a `SessionEnd` hook, and a committed `docs/ai/USAGE.md` |

Add-ons need whatever their README says (`usage-tracking` needs `python3`). Like everything in `template/`, they must stay project-agnostic.
