#!/usr/bin/env python3
"""
Claude Code Hook: Auto-save every prompt to memory log.
Configure in .claude/settings.json as a PostToolUse or Notification hook.

Usage (called by Claude Code hook):
  python3 /path/to/save_prompt.py --session SESSION_ID --project PROJECT --prompt "PROMPT_TEXT"

Or pipe JSON from Claude Code hook stdin:
  echo '{"session_id":"...","prompt":"..."}' | python3 save_prompt.py
"""

import json
import os
import sys
from datetime import datetime

MEMORY_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(MEMORY_DIR, "prompt_log.jsonl")


def save_prompt(session_id: str, project: str, prompt: str, branch: str = ""):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "session_id": session_id,
        "project": project,
        "branch": branch,
        "prompt": prompt[:2000],  # cap at 2000 chars
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main():
    # Try reading from stdin (Claude Code hook passes data via stdin)
    if not sys.stdin.isatty():
        try:
            data = json.loads(sys.stdin.read())
            save_prompt(
                session_id=data.get("session_id", ""),
                project=data.get("cwd", data.get("project", "")),
                prompt=data.get("prompt", data.get("display", "")),
                branch=data.get("git_branch", ""),
            )
        except Exception as e:
            print(f"save_prompt error: {e}", file=sys.stderr)
        return

    # CLI argument fallback
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--session", default="")
    parser.add_argument("--project", default="")
    parser.add_argument("--prompt", default="")
    parser.add_argument("--branch", default="")
    args = parser.parse_args()
    save_prompt(args.session, args.project, args.prompt, args.branch)


if __name__ == "__main__":
    main()
