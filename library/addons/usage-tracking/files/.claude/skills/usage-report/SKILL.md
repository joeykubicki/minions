---
name: usage-report
description: Update docs/ai/USAGE.md, the committed summary of Claude Code tokens, active time, and estimated cost spent on this project. Use when the user asks how many tokens, how much time, or how much AI usage the project or a session took.
---

1. Run `python3 .claude/usage/usage.py report`. It copies new usage from Claude Code's transcripts into the local ledger (`.claude/usage/ledger.jsonl`, gitignored), then rewrites `docs/ai/USAGE.md`.
2. If it fails, show the error. Don't edit the ledger or the report by hand.
3. Reply with the headline line it printed, plus anything notable in the report: the largest sessions, the subagent share, or models with no price (marked `*`).
4. Session titles in the report are auto-generated from your prompts. Remind the user to skim them before committing, since the report is meant to be committed. Don't commit unless asked.

Tokens are the main measure. Cost is an API-equivalent estimate, not what a subscription bills. How each number is calculated is explained at the end of `docs/ai/USAGE.md`.
