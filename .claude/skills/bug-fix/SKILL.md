---
name: bug-fix
description: Reproduce and fix a bug with evidence and targeted regression verification.
---
Read AGENTS.md and docs/ai/ROUTING.md. Establish expected versus actual behavior and risk tier. Use debugger if root cause is unclear. Reproduce safely; preserve logs and avoid secrets. Add a failing regression test when practical, implement the smallest fix, run relevant checks, and confirm the original failure is resolved. Consult security or architecture specialists if risk warrants. Request review according to tier. Report root cause, changed files, tests, unverified items and gate status. Do not hide unrelated failures.
