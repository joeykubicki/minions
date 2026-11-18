#!/usr/bin/env python3
"""Claude Code token usage for this project: a local ledger and a committed summary.

Part of the minions kit's usage-tracking add-on. Python 3.8+, standard library only.

    python3 .claude/usage/usage.py sync     copy new usage from Claude Code transcripts into the ledger
    python3 .claude/usage/usage.py report   sync, then write docs/ai/USAGE.md and print the headline

Claude Code saves transcripts in ~/.claude/projects/<encoded project path>/ and deletes them
after `cleanupPeriodDays` (default 30). The ledger (.claude/usage/ledger.jsonl, gitignored)
keeps the usage numbers so reports can cover the whole project. The transcript format is not
a documented API, so parsing is defensive: records that don't look as expected are skipped.
"""
import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

LEDGER_VERSION = 1
IDLE_GAP_SECONDS = 15 * 60  # longer gaps with Claude not working count as idle time
MAX_REQUEST_SECONDS = 30 * 60  # longer "requests" are treated as bad data, not work

# Anthropic API list prices in USD per million tokens:
# (input, output, 5-minute cache write, 1-hour cache write, cache read).
# Update when prices change; models missing here are reported as "no price".
PRICES_AS_OF = "2026-11"
PRICES = {
    "claude-fable-5-2": (8.00, 40.00, 10.00, 16.00, 0.20),
    "claude-fable-5-1": (10.00, 50.00, 12.50, 20.00, 0.25),
    "claude-fable-5": (10.00, 50.00, 12.50, 20.00, 1.00),
    "claude-opus-5-5": (4.00, 20.00, 5.00, 8.00, 0.20),
    "claude-opus-5": (5.00, 25.00, 6.25, 10.00, 0.50),
    "claude-opus-4-8": (5.00, 25.00, 6.25, 10.00, 0.50),
    "claude-opus-4-7": (5.00, 25.00, 6.25, 10.00, 0.50),
    "claude-opus-4-6": (5.00, 25.00, 6.25, 10.00, 0.50),
    "claude-sonnet-5-5": (2.00, 10.00, 2.50, 4.00, 0.10),
    "claude-sonnet-5": (2.00, 10.00, 2.50, 4.00, 0.20),
    "claude-sonnet-4-6": (3.00, 15.00, 3.75, 6.00, 0.30),
    "claude-haiku-5-5": (0.10, 0.50, 0.125, 0.20, 0.01),
    "claude-haiku-4-5": (1.00, 5.00, 1.25, 2.00, 0.10),
}
FAST_MODE_MULTIPLIER = 2.0  # fast mode bills at 2x standard rates


# --- reading transcripts ------------------------------------------------------

def transcript_dirs(root):
    """Claude Code transcript folders for this project, including subfolders and worktrees."""
    base = Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude") / "projects"
    encoded = re.sub(r"[^A-Za-z0-9]", "-", str(root))
    if not base.is_dir():
        return []
    return sorted(d for d in base.iterdir()
                  if d.is_dir() and (d.name == encoded or d.name.startswith(encoded + "-")))


def inside(cwd, root):
    return cwd == str(root) or cwd.startswith(str(root) + os.sep)


def agent_name(path):
    """'main' for the lead session, else the subagent type from its .meta.json."""
    if path.parent.name != "subagents":
        return "main"
    try:
        meta = json.loads(path.with_suffix(".meta.json").read_text())
        return meta.get("agentType") or "subagent"
    except (OSError, ValueError):
        return "subagent"


def parse_transcript(path, root, exact_dir):
    """Yield ('req', row) and ('title', session, title) items from one transcript file.

    A request's "start" is the timestamp of the prompt or tool result before it, and its
    "ts" is the last line written for it, so start..ts is the time Claude spent working.
    """
    agent = agent_name(path)
    rows, last_user_ts = {}, ""
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if '"usage"' not in line and '"ai-title"' not in line and '"user"' not in line:
                continue
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            if not isinstance(rec, dict):
                continue
            cwd = rec.get("cwd")
            if cwd and not inside(cwd, root):
                continue
            if not cwd and not exact_dir:
                continue
            if rec.get("type") == "ai-title" and rec.get("aiTitle") and rec.get("sessionId"):
                yield ("title", rec["sessionId"], str(rec["aiTitle"])[:120])
                continue
            if rec.get("type") == "user":
                last_user_ts = rec.get("timestamp") or last_user_ts
                continue
            if rec.get("type") != "assistant":
                continue
            msg = rec.get("message") or {}
            usage = msg.get("usage")
            model = msg.get("model") or ""
            rid = rec.get("requestId") or msg.get("id")
            if not isinstance(usage, dict) or not rid or not model or model.startswith("<"):
                continue
            if rid in rows:  # same request, later content block
                rows[rid]["ts"] = max(rows[rid]["ts"], rec.get("timestamp") or "")
                continue
            cache_write = int(usage.get("cache_creation_input_tokens") or 0)
            split = usage.get("cache_creation") or {}
            cw1 = int(split.get("ephemeral_1h_input_tokens") or 0)
            rows[rid] = {
                "kind": "req", "v": LEDGER_VERSION, "id": rid,
                "start": last_user_ts,
                "ts": rec.get("timestamp") or "",
                "session": rec.get("sessionId") or "",
                "agent": "subagent" if agent == "main" and rec.get("isSidechain") else agent,
                "model": model,
                "branch": rec.get("gitBranch") or "",
                "in": int(usage.get("input_tokens") or 0),
                "out": int(usage.get("output_tokens") or 0),
                "cw5": max(cache_write - cw1, 0),
                "cw1": cw1,
                "cr": int(usage.get("cache_read_input_tokens") or 0),
                "fast": usage.get("speed") == "fast",
            }
    for row in rows.values():
        yield ("req", row)


# --- ledger -------------------------------------------------------------------

def load_ledger(ledger):
    reqs, titles = {}, {}
    if ledger.exists():
        with open(ledger, encoding="utf-8") as fh:
            for line in fh:
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                if row.get("kind") == "req" and row.get("id"):
                    reqs[row["id"]] = row
                elif row.get("kind") == "title" and row.get("session"):
                    titles[row["session"]] = row.get("title", "")
    return reqs, titles


def sync(root, ledger):
    """Append usage not yet in the ledger. Returns the number of new requests."""
    state_path = ledger.with_name("state.json")
    reqs, titles = load_ledger(ledger)
    state = {}
    if ledger.exists() and state_path.exists():
        try:
            state = json.loads(state_path.read_text())
        except ValueError:
            state = {}

    encoded = re.sub(r"[^A-Za-z0-9]", "-", str(root))
    new_rows, new_state = [], {}
    for d in transcript_dirs(root):
        for path in sorted(d.rglob("*.jsonl")):
            try:
                st = path.stat()
            except OSError:
                continue
            sig = [st.st_size, int(st.st_mtime)]
            new_state[str(path)] = sig
            if state.get(str(path)) == sig:
                continue
            for item in parse_transcript(path, root, d.name == encoded):
                if item[0] == "req":
                    row = item[1]
                    if row["id"] not in reqs:
                        reqs[row["id"]] = row
                        new_rows.append(row)
                else:
                    _, session, title = item
                    if titles.get(session) != title:
                        titles[session] = title
                        new_rows.append({"kind": "title", "session": session, "title": title})

    ledger.parent.mkdir(parents=True, exist_ok=True)
    if new_rows:
        with open(ledger, "a", encoding="utf-8") as fh:
            for row in new_rows:
                fh.write(json.dumps(row, separators=(",", ":")) + "\n")
    # Keep signatures of transcripts that have since been deleted, harmlessly.
    merged = {**state, **new_state}
    tmp = state_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(merged))
    tmp.replace(state_path)
    return sum(1 for r in new_rows if r["kind"] == "req")


# --- numbers ------------------------------------------------------------------

def price_for(model):
    return PRICES.get(model) or PRICES.get(re.sub(r"-\d{8}$", "", model))


def cost(row):
    p = price_for(row["model"])
    if p is None:
        return None
    usd = (row["in"] * p[0] + row["out"] * p[1] + row["cw5"] * p[2]
           + row["cw1"] * p[3] + row["cr"] * p[4]) / 1e6
    return usd * FAST_MODE_MULTIPLIER if row.get("fast") else usd


def parse_time(value):
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone()
    except (ValueError, AttributeError):
        return None


def when(row):
    return parse_time(row.get("ts"))


def working_interval(row):
    """(start, end) of the time Claude spent on one request."""
    end = when(row)
    start = parse_time(row.get("start")) or end
    if end and start and not 0 <= (end - start).total_seconds() <= MAX_REQUEST_SECONDS:
        start = end
    return start, end


def active_seconds(intervals):
    """Time covered by Claude working, plus gaps between work of up to IDLE_GAP_SECONDS."""
    total, cur_start, cur_end = 0.0, None, None
    for start, end in sorted(i for i in intervals if i[1]):
        if cur_end is not None and (start - cur_end).total_seconds() <= IDLE_GAP_SECONDS:
            cur_end = max(cur_end, end)
            continue
        if cur_end is not None:
            total += (cur_end - cur_start).total_seconds()
        cur_start, cur_end = start, end
    if cur_end is not None:
        total += (cur_end - cur_start).total_seconds()
    return total


class Totals:
    def __init__(self):
        self.requests = 0
        self.new_input = 0
        self.output = 0
        self.cache_read = 0
        self.cost = 0.0
        self.unpriced = 0
        self.times = []
        self.intervals = []

    def add(self, row):
        self.requests += 1
        self.new_input += row["in"] + row["cw5"] + row["cw1"]
        self.output += row["out"]
        self.cache_read += row["cr"]
        c = cost(row)
        if c is None:
            self.unpriced += 1
        else:
            self.cost += c
        t = when(row)
        if t:
            self.times.append(t)
            self.intervals.append(working_interval(row))

    @property
    def tokens(self):
        return self.new_input + self.output

    @property
    def active(self):
        return active_seconds(self.intervals)


def fmt_tokens(n):
    for size, suffix in ((1e9, "B"), (1e6, "M"), (1e3, "K")):
        if n >= size:
            value = n / size
            return f"{value:.1f}{suffix}" if value < 100 else f"{value:.0f}{suffix}"
    return str(n)


def fmt_time(seconds):
    minutes = int(round(seconds / 60))
    return f"{minutes // 60}h {minutes % 60:02d}m" if minutes >= 60 else f"{minutes}m"


def fmt_cost(t):
    return f"${t.cost:,.2f}" + ("*" if t.unpriced else "")


def cell(text):
    return str(text).replace("|", "\\|").replace("\n", " ")


# --- report -------------------------------------------------------------------

def build_report(rows, titles):
    rows = sorted(rows, key=lambda r: r.get("ts", ""))
    total, by_model, by_agent = Totals(), defaultdict(Totals), defaultdict(Totals)
    by_day, by_session = defaultdict(Totals), defaultdict(Totals)
    day_sessions, session_branches = defaultdict(set), defaultdict(Counter)
    for r in rows:
        total.add(r)
        by_model[r["model"]].add(r)
        by_agent[r["agent"]].add(r)
        by_session[r["session"]].add(r)
        session_branches[r["session"]][r["branch"]] += 1
        t = when(r)
        if t:
            day = t.date().isoformat()
            by_day[day].add(r)
            day_sessions[day].add(r["session"])

    first, last = (total.times[0].date(), total.times[-1].date()) if total.times else (None, None)
    today = datetime.now().date().isoformat()
    out = [
        "# AI usage",
        "",
        f"Claude Code usage for this project, generated by `/usage-report` on {today}. "
        "Tokens are the main measure; cost is an API-equivalent estimate. See "
        "[how these numbers are measured](#how-these-numbers-are-measured).",
        "",
    ]
    if not rows:
        out += ["No usage recorded yet.", ""]
        return "\n".join(out)

    share = total.cache_read / (total.cache_read + total.new_input) if total.cache_read else 0
    out += [
        f"**{fmt_tokens(total.tokens)} tokens** (new input + output), plus "
        f"{fmt_tokens(total.cache_read)} tokens re-read from cache, over "
        f"**{fmt_time(total.active)}** of active time in {len(by_session)} sessions "
        f"({first} to {last}). Estimated API-equivalent cost: {fmt_cost(total)}.",
        "",
        "## Totals",
        "",
        "| Measure | Value |",
        "| --- | ---: |",
        f"| New input tokens (uncached input + cache writes) | {total.new_input:,} |",
        f"| Output tokens (including thinking) | {total.output:,} |",
        f"| **Total tokens (new input + output)** | **{total.tokens:,}** |",
        f"| Cache reads | {total.cache_read:,} |",
        f"| Share of input served from cache | {share:.1%} |",
        f"| Requests | {total.requests:,} |",
        f"| Sessions | {len(by_session)} |",
        f"| Days with activity | {len(by_day)} |",
        f"| Active time | {fmt_time(total.active)} |",
        f"| Estimated API-equivalent cost | {fmt_cost(total)} |",
        "",
    ]

    def table(title, labels, groups, right_aligned=()):
        """groups: (leading cells, Totals). Leading columns are labels; numbers follow."""
        numbers = ["Requests", "Tokens", "Output", "Cache reads", "Est. cost"]
        align = ["---:" if h in right_aligned else "---" for h in labels] + ["---:"] * len(numbers)
        lines = ["## " + title, "", "| " + " | ".join(labels + numbers) + " |",
                 "| " + " | ".join(align) + " |"]
        for lead, t in groups:
            vals = [cell(v) for v in lead] + [f"{t.requests:,}", fmt_tokens(t.tokens),
                                              fmt_tokens(t.output), fmt_tokens(t.cache_read), fmt_cost(t)]
            lines.append("| " + " | ".join(vals) + " |")
        return lines + [""]

    def by_tokens(groups):
        return sorted(groups.items(), key=lambda kv: -kv[1].tokens)

    def started(t):
        return t.times[0] if t.times else datetime.max.replace(tzinfo=timezone.utc)

    def session_branch(s):
        branch = session_branches[s].most_common(1)[0][0]
        return f"`{branch}`" if branch else "-"

    out += table("By model", ["Model"], [([m], t) for m, t in by_tokens(by_model)])
    out += table("By agent", ["Agent", "Share of tokens"],
                 [([a, f"{t.tokens / total.tokens:.1%}" if total.tokens else "-"], t)
                  for a, t in by_tokens(by_agent)], right_aligned=["Share of tokens"])
    out += table("By day", ["Date", "Sessions", "Active time"],
                 [([d, len(day_sessions[d]), fmt_time(t.active)], t) for d, t in sorted(by_day.items())],
                 right_aligned=["Sessions", "Active time"])
    out += table("By session", ["Started", "Session", "Branch", "Active time"],
                 [([started(t).strftime("%Y-%m-%d %H:%M") if t.times else "-",
                    titles.get(s) or (s[:8] if s else "unknown"), session_branch(s), fmt_time(t.active)], t)
                  for s, t in sorted(by_session.items(), key=lambda kv: started(kv[1]))],
                 right_aligned=["Active time"])

    unpriced = sorted({r["model"] for r in rows if price_for(r["model"]) is None})
    out += [
        "## How these numbers are measured",
        "",
        "- **Source:** Claude Code's local transcripts for this project, including subagents, "
        "copied into a local ledger (`.claude/usage/ledger.jsonl`, not committed) so that numbers survive "
        "Claude Code's transcript cleanup. Work from before the ledger existed is included only if its "
        f"transcripts were still on disk. Earliest recorded activity: {first}.",
        "- **Tokens:** each API request is counted once. *New input* is uncached input plus cache writes, "
        "meaning context sent to the model for the first time. *Output* includes thinking. "
        "*Cache reads* are context re-read from the prompt cache on later requests. They're billed at a "
        "small fraction of the input price, so they're shown separately rather than added to the total.",
        "- **Active time:** time Claude spent working on requests, plus gaps of up to "
        f"{IDLE_GAP_SECONDS // 60} minutes between them (reading, reviewing, typing the next prompt). "
        "Longer gaps count as idle. It's an approximation of hands-on time.",
        f"- **Estimated cost:** Anthropic API list prices as of {PRICES_AS_OF}, at standard or fast-mode "
        "rates. A Claude subscription doesn't bill per token, so treat this as what the same work would "
        "cost on the API.",
    ]
    if unpriced:
        out.append(f"- \\* Costs exclude requests on models with no price in `usage.py`: "
                   f"{', '.join(unpriced)}.")
    out += [
        "- **Not counted:** small background requests Claude Code doesn't save to transcripts "
        "(for example, generating session titles), and work done outside Claude Code.",
        "",
    ]
    return "\n".join(out)


def main():
    here = Path(__file__).resolve()
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("command", choices=["sync", "report"])
    parser.add_argument("--project", type=Path, default=here.parents[2],
                        help="project root (default: the project this script is installed in)")
    parser.add_argument("--ledger", type=Path, help="ledger path (default: .claude/usage/ledger.jsonl)")
    parser.add_argument("--out", type=Path, help="report path (default: docs/ai/USAGE.md)")
    parser.add_argument("--quiet", action="store_true",
                        help="never fail or print; for the SessionEnd hook")
    args = parser.parse_args()

    root = args.project.expanduser().resolve()
    ledger = (args.ledger or root / ".claude" / "usage" / "ledger.jsonl").expanduser()
    try:
        added = sync(root, ledger)
        if args.command == "sync":
            if not args.quiet:
                print(f"Added {added} requests to {ledger}")
            return 0
        reqs, titles = load_ledger(ledger)
        report = build_report(reqs.values(), titles)
        out = (args.out or root / "docs" / "ai" / "USAGE.md").expanduser()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report, encoding="utf-8")
        headline = next((l for l in report.splitlines() if l.startswith("**")), "No usage recorded yet.")
        print(f"Wrote {out} ({added} new requests synced)\n\n{headline}")
        return 0
    except Exception as exc:  # the hook must never break a session
        if args.quiet:
            return 0
        print(f"usage.py: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
