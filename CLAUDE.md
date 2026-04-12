# Vaad-App — Claude Code Project Context

## MANDATORY: Git & Deployment Workflow

**Every code change request MUST follow this workflow automatically — no exceptions, no need to ask.**

### Step-by-step (follow every time)

1. **Make the code changes** as requested
2. **Stage and commit** with a clear `feat:` / `fix:` message
3. **Push immediately** to the current session branch:
   ```bash
   git push -u origin <current-session-branch>
   ```
4. **Done** — the platform auto-creates a PR and auto-merges to `main`, which triggers GitHub Pages deployment

### Rules
- **NEVER push without explicit user approval.** After committing, always stop and ask the user to test the change locally first. Only push after the user explicitly says to (e.g. "push", "looks good", "go ahead").
- Never leave committed changes un-pushed **once the user has approved**
- Branch naming: `claude/<description>-<SESSION_ID>` (provided by the system per session)
- Never push directly to `main` (blocked by the proxy)
- The platform handles PR creation + merge to main automatically on each push

### What happens automatically
```
You push to claude/branch  →  Platform opens PR  →  Platform merges to main  →  GitHub Pages redeploys
```

### Deployment URL
https://rottembz-prog.github.io/Vaad-app/

---

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

---

## Project

Vaad-App (ועד בית) — Building management expense tracker.
- **Tech:** Vanilla JS + Firebase (Firestore + Auth)
- **Hosting:** GitHub Pages
- **Repo:** https://github.com/rottembz-prog/Vaad-app
