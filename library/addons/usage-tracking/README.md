# usage-tracking

Measures how much Claude Code work went into a project, so you can show how efficiently it was built: tokens first, then active time and an estimated API-equivalent cost. Everything runs locally from Claude Code's own transcripts. No account access or telemetry setup is needed.

```bash
./install.sh ~/code/my-project --add usage-tracking
```

| Installed file | What it does |
| --- | --- |
| `.claude/usage/usage.py` | Reads this project's transcripts in `~/.claude/projects/` (subagents included) and appends new requests to a local ledger. `report` also writes `docs/ai/USAGE.md`. Python 3.8+, standard library only. |
| `.claude/usage/.gitignore` | Keeps the ledger local, so only the summary gets committed. |
| `.claude/skills/usage-report/SKILL.md` | `/usage-report` updates the summary and tells you the headline. |
| `SessionEnd` hook in `.claude/settings.json` | Syncs the ledger at the end of every session. It never blocks or fails a session. |

The installer merges the hook into your existing `.claude/settings.json` and leaves everything else in that file alone.

## Why a ledger
By default, Claude Code deletes transcripts after 30 days (the `cleanupPeriodDays` setting). The ledger keeps the numbers, about 250 bytes per request, so a report can cover a project's whole history. On install, run `/usage-report` once to backfill whatever transcripts are still on disk. Consider raising `cleanupPeriodDays` in `~/.claude/settings.json` too.

## What the report shows
- **Tokens:** new input (uncached input plus cache writes) and output, with cache reads shown separately. Cache reads are often more than 95% of raw input, so adding them to the total would overstate the work. Each API request is counted once, even though transcripts repeat it across several lines.
- **Active time:** time Claude spent working on requests, plus gaps of up to 15 minutes between them (reading output, reviewing, writing the next prompt). Change `IDLE_GAP_SECONDS` in `usage.py` to adjust.
- **Estimated cost:** API list prices from the `PRICES` table in `usage.py`. Update the table when prices change. Models missing from it are flagged rather than guessed.
- **Breakdowns:** by model, by agent (lead or subagent type), by day, and by session (Claude Code's auto-generated title, start time, branch).

## Limits
- The transcript format isn't a documented API. The script skips anything it doesn't recognize, so a format change shows up as missing numbers, not a crash. Re-check after major Claude Code updates.
- Small background requests that Claude Code doesn't save to transcripts aren't counted. Compared against Claude Code's own per-session cost records, the estimate came within 0.3%.
- Sessions in a git worktree outside the project folder aren't found.
- Plan usage limits (the 5-hour and weekly windows) aren't covered here. A status line for those is on the roadmap.

For daily or 5-hour-block views across all projects, the open-source [`ccusage`](https://github.com/ryoppippi/ccusage) is a good complement. This add-on is different in two ways: it keeps the history inside each project, and it writes a summary meant to be committed.
