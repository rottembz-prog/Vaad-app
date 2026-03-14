# Vaad-App — Claude Code Project Context

## Memory System

All conversations are automatically saved in the [`memory/`](./memory/) folder.

### Quick Resume
Open [`memory/LATEST.md`](./memory/LATEST.md) to see the last session per repository
and get the exact `claude --resume <session_id>` command to continue.

### Full History
Open [`memory/index.md`](./memory/index.md) for a complete index of all sessions
organized by repository and date.

### Rebuild Memory
```bash
python3 memory/build_memory.py
```

### Structure
```
memory/
  index.md                          # Master index of all conversations
  LATEST.md                         # Quick resume — last session per repo
  prompt_log.jsonl                  # Live log of every prompt (auto-appended)
  build_memory.py                   # Script to regenerate markdown files
  save_prompt.py                    # Hook script (auto-called per prompt)
  conversations/
    C--WINDOWS-system32/            # Per-project conversation logs
      2026-03-05.md
      2026-03-06.md
    C--Users-97252-Downloads/
      2026-03-02.md
```

## Project
Vaad-App (ועד בית) — Building management expense tracker.
- **Tech:** Vanilla JS + Firebase (Firestore + Auth)
- **Hosting:** GitHub Pages
- **Repo:** https://github.com/rottembz-prog/Vaad-app
