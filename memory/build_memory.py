#!/usr/bin/env python3
"""
Memory Builder for Claude Code Conversations
Reads all session JSONL files and generates organized markdown memory files.
Run this script to refresh the memory folder.
"""

import json
import os
import sys
from datetime import datetime, timezone
from collections import defaultdict

# Paths - adjust BASE_DIR to match your Claude data folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECTS_DIR = os.path.join(BASE_DIR, "projects")
HISTORY_FILE = os.path.join(BASE_DIR, "history.jsonl")
MEMORY_DIR = os.path.join(BASE_DIR, "memory")
CONVERSATIONS_DIR = os.path.join(MEMORY_DIR, "conversations")

REPO_NAME_MAP = {
    "C--Users-97252-Downloads": "Downloads (vaad-app local)",
    "C--WINDOWS-system32": "System32 / Vaad-app dev",
}


def friendly_project_name(raw_name):
    return REPO_NAME_MAP.get(raw_name, raw_name.replace("C--", "").replace("-", "/"))


def parse_timestamp(ts_str):
    if not ts_str:
        return None
    try:
        ts_str = ts_str.replace("Z", "+00:00")
        return datetime.fromisoformat(ts_str)
    except Exception:
        return None


def extract_user_messages(jsonl_path):
    """Extract all user messages from a session JSONL file."""
    messages = []
    try:
        with open(jsonl_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue

                if entry.get("type") != "user":
                    continue

                msg = entry.get("message", {})
                content = msg.get("content", "")
                text = ""

                if isinstance(content, str):
                    text = content
                elif isinstance(content, list):
                    parts = []
                    for c in content:
                        if isinstance(c, dict) and c.get("type") == "text":
                            parts.append(c["text"])
                    text = "\n".join(parts)

                text = text.strip()
                if not text or text in ("resume", "Tool loaded."):
                    continue

                ts = parse_timestamp(entry.get("timestamp", ""))
                messages.append(
                    {
                        "timestamp": ts,
                        "text": text,
                        "session_id": entry.get("sessionId", ""),
                        "git_branch": entry.get("gitBranch", ""),
                    }
                )
    except Exception as e:
        print(f"  Warning: could not parse {jsonl_path}: {e}", file=sys.stderr)
    return messages


def load_all_sessions():
    """Load all sessions grouped by project."""
    project_sessions = defaultdict(list)  # project_name -> list of session dicts

    if not os.path.isdir(PROJECTS_DIR):
        print(f"Projects dir not found: {PROJECTS_DIR}", file=sys.stderr)
        return project_sessions

    for project_name in sorted(os.listdir(PROJECTS_DIR)):
        project_path = os.path.join(PROJECTS_DIR, project_name)
        if not os.path.isdir(project_path):
            continue

        # Find all jsonl files directly in project folder (skip subagents)
        for fname in sorted(os.listdir(project_path)):
            if not fname.endswith(".jsonl"):
                continue
            jsonl_path = os.path.join(project_path, fname)
            session_id = fname.replace(".jsonl", "")
            messages = extract_user_messages(jsonl_path)
            if not messages:
                continue

            first_ts = messages[0]["timestamp"]
            last_ts = messages[-1]["timestamp"]

            project_sessions[project_name].append(
                {
                    "session_id": session_id,
                    "first_ts": first_ts,
                    "last_ts": last_ts,
                    "messages": messages,
                    "git_branch": messages[0].get("git_branch", ""),
                }
            )

    return project_sessions


def build_project_page(project_name, sessions, output_dir):
    """Generate a markdown page for all sessions in a project."""
    os.makedirs(output_dir, exist_ok=True)

    friendly = friendly_project_name(project_name)

    # Group sessions by date
    by_date = defaultdict(list)
    for s in sessions:
        ts = s["first_ts"]
        date_key = ts.strftime("%Y-%m-%d") if ts else "unknown-date"
        by_date[date_key].append(s)

    for date_key, date_sessions in sorted(by_date.items(), reverse=True):
        out_path = os.path.join(output_dir, f"{date_key}.md")
        lines = []
        lines.append(f"# {friendly} — {date_key}\n")
        lines.append(f"**Repository:** `{project_name}`  ")
        lines.append(f"**Date:** {date_key}  ")
        lines.append(f"**Sessions:** {len(date_sessions)}\n")
        lines.append("---\n")

        for session in sorted(date_sessions, key=lambda s: s["first_ts"] or datetime.min):
            ts_label = session["first_ts"].strftime("%H:%M") if session["first_ts"] else "?"
            last_label = session["last_ts"].strftime("%H:%M") if session["last_ts"] else "?"
            branch = session.get("git_branch") or "—"
            lines.append(f"## Session `{session['session_id'][:8]}...`")
            lines.append(f"**Time:** {ts_label} → {last_label}  ")
            lines.append(f"**Branch:** `{branch}`  ")
            lines.append(f"**Prompts:** {len(session['messages'])}\n")

            for i, msg in enumerate(session["messages"], 1):
                msg_ts = msg["timestamp"].strftime("%H:%M:%S") if msg["timestamp"] else "?"
                # Indent multi-line messages
                text_lines = msg["text"].split("\n")
                first_line = text_lines[0][:200]
                rest = text_lines[1:] if len(text_lines) > 1 else []
                lines.append(f"### Prompt {i} — `{msg_ts}`")
                lines.append(f"> {first_line}")
                for extra in rest[:3]:
                    if extra.strip():
                        lines.append(f"> {extra[:200]}")
                lines.append("")

            lines.append("---\n")

        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"  Written: {out_path}")


def build_index(project_sessions):
    """Generate the master index markdown file."""
    lines = []
    lines.append("# Claude Code Memory — Conversation Index\n")
    lines.append(f"_Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n")
    lines.append("---\n")

    total_sessions = sum(len(v) for v in project_sessions.values())
    total_prompts = sum(
        len(s["messages"]) for sessions in project_sessions.values() for s in sessions
    )
    lines.append(f"**Total repositories:** {len(project_sessions)}  ")
    lines.append(f"**Total sessions:** {total_sessions}  ")
    lines.append(f"**Total prompts:** {total_prompts}\n")
    lines.append("---\n")

    for project_name, sessions in sorted(project_sessions.items()):
        friendly = friendly_project_name(project_name)
        all_ts = [s["first_ts"] for s in sessions if s["first_ts"]]
        if all_ts:
            first_date = min(all_ts).strftime("%Y-%m-%d")
            last_date = max(all_ts).strftime("%Y-%m-%d")
            date_range = f"{first_date} → {last_date}"
        else:
            date_range = "unknown"

        all_prompts = sum(len(s["messages"]) for s in sessions)

        lines.append(f"## {friendly}")
        lines.append(f"**Path:** `{project_name}`  ")
        lines.append(f"**Date range:** {date_range}  ")
        lines.append(f"**Sessions:** {len(sessions)} | **Prompts:** {all_prompts}\n")

        # List most recent sessions
        recent = sorted(sessions, key=lambda s: s["first_ts"] or datetime.min, reverse=True)[:5]
        lines.append("**Recent sessions:**\n")
        for s in recent:
            ts = s["first_ts"].strftime("%Y-%m-%d %H:%M") if s["first_ts"] else "?"
            first_prompt = s["messages"][0]["text"][:80].replace("\n", " ") if s["messages"] else ""
            date_key = s["first_ts"].strftime("%Y-%m-%d") if s["first_ts"] else "unknown-date"
            rel_path = f"conversations/{project_name}/{date_key}.md"
            lines.append(f"- `{ts}` — [{first_prompt}...]({rel_path})")

        lines.append("\n---\n")

    index_path = os.path.join(MEMORY_DIR, "index.md")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Index written: {index_path}")


def build_latest_md(project_sessions):
    """Generate a LATEST.md for quick resume — shows last session per project."""
    lines = []
    lines.append("# Quick Resume — Latest Conversations\n")
    lines.append(f"_Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n")
    lines.append("---\n")
    lines.append("Use this file to quickly resume your last conversation in each repository.\n")

    for project_name, sessions in sorted(project_sessions.items()):
        friendly = friendly_project_name(project_name)
        latest = max(sessions, key=lambda s: s["last_ts"] or datetime.min)

        ts = latest["last_ts"].strftime("%Y-%m-%d %H:%M") if latest["last_ts"] else "?"
        date_key = latest["first_ts"].strftime("%Y-%m-%d") if latest["first_ts"] else "unknown-date"
        branch = latest.get("git_branch") or "—"

        lines.append(f"## {friendly}")
        lines.append(f"**Last active:** {ts}  ")
        lines.append(f"**Session ID:** `{latest['session_id']}`  ")
        lines.append(f"**Branch:** `{branch}`  ")
        lines.append(f"**Detail file:** [conversations/{project_name}/{date_key}.md](conversations/{project_name}/{date_key}.md)\n")

        lines.append("**Last prompts:**\n")
        for msg in latest["messages"][-3:]:
            msg_ts = msg["timestamp"].strftime("%H:%M") if msg["timestamp"] else "?"
            text = msg["text"][:150].replace("\n", " ")
            lines.append(f"- `{msg_ts}` {text}")
        lines.append("\n**To resume:** Run `claude --resume {}`\n".format(latest["session_id"]))
        lines.append("---\n")

    latest_path = os.path.join(MEMORY_DIR, "LATEST.md")
    with open(latest_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Latest written: {latest_path}")


def main():
    print("Building Claude Code memory...")
    print(f"  Projects dir: {PROJECTS_DIR}")
    print(f"  Memory dir: {MEMORY_DIR}\n")

    os.makedirs(CONVERSATIONS_DIR, exist_ok=True)

    project_sessions = load_all_sessions()

    if not project_sessions:
        print("No sessions found. Check that PROJECTS_DIR is correct.")
        return

    for project_name, sessions in project_sessions.items():
        print(f"Processing project: {project_name} ({len(sessions)} sessions)")
        project_out_dir = os.path.join(CONVERSATIONS_DIR, project_name)
        build_project_page(project_name, sessions, project_out_dir)

    build_index(project_sessions)
    build_latest_md(project_sessions)

    print(f"\nDone! Open memory/index.md or memory/LATEST.md to browse.")


if __name__ == "__main__":
    main()
