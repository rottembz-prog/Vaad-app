# Memory — Downloads workspace

## vaad-horim-app (ועד הורים)
- **Location:** `~/Downloads/vaad-app/`
- **Type:** Hebrew RTL React app — school parent committee budget manager
- **Stack:** React 18 + Vite (no TypeScript in use, JSX only)
- **Status:** Fully scaffolded and ready to run

### Key files
- `standalone.html` — works NOW without Node.js (CDN React + Babel)
- `index.html` + `vite.config.js` + `src/main.jsx` — Vite project
- `src/App.demo.jsx` — complete single-file app (all 5 tabs)
- `src/types/index.ts` — TypeScript interfaces
- `src/hooks/useSheets.ts` — Google Sheets sync hook
- `gas/Code.gs` — Google Apps Script backend
- `.env.example` — VITE_GAS_URL, VITE_SPREADSHEET_ID

### Design rules (from CLAUDE.md)
- Always RTL (`direction: rtl`), Hebrew Heebo font
- No localStorage — in-memory React state
- Mobile-first (375px)
- Colors: primary #7c3aed, accent #db2777, success #059669

### Data
- 27 students, ₪500/student, class ו׳ תשפ״ד–תשפ״ה
- 15 budget events totaling ₪5,455
- Budget structure in `תקציב_ועד_ו_3.xlsx`

### Node.js
- Node.js NOT installed on this machine
- Use `standalone.html` for immediate use (open in browser)
- Install Node.js from nodejs.org then run: `npm install && npm run dev`

## Environment
- Windows 11, WSL bash shell
- No Node.js installed (as of 2026-03-02)
