# Vaad-App Project Memory

## File Location
`C:/Users/97252/Downloads/vaad-app/standalone.html`
Opened via: `file:///C:/Users/97252/Downloads/vaad-app/standalone.html`

## Tech Stack
Single-file React app (Babel standalone, React 18 UMD, no build step).
Hebrew RTL UI. Data persisted in localStorage (`vaad_budgets`, `vaad_gifts`).

## App Structure
- **HomeScreen** — lists budgets, add/edit/delete budgets
- **BudgetScreen** — 4-tab layout for a single budget:
  - `BudgetTab` (תקציב) — budget events (income/expense), sorted by date
  - `CollectTab` (גבייה) — student payment tracking
  - `GiftsTab` (רעיונות) — gift/idea directory (shared across budgets)
  - `CashTab` (מזומן) — cash log + auto-derived budget expenses

## Key Data Shapes
```js
// Budget event
{ id, name, date, budget, spent, category, notes, paidBy, done, type: "expense"|"income" }

// Student
{ id, name, paid, amount, note, paidBy }

// Cash log entry (manual)
{ id, date, desc, amount, type, paidBy }

// Gift/idea
{ id, icon, name, forWhom, priceRange, tag, notes, vendorName, vendorPhone, vendorLink, photo }
```

## Fixes Applied This Session

### Bug Fix: Nested components causing autoFocus loop
- `EventForm`, `GiftForm`, `CashForm` were defined INSIDE their parent components
- React re-mounted them on every keystroke → autoFocus on first field every time
- Fix: moved all three to top-level function declarations outside parent components
- `handlePhotoUpload` also moved to top-level (used by GiftForm)

### Feature: Budget expenses auto-appear in מזומן (read-only)
- `CashTab` receives `events` prop
- Derives `budgetExpenses` from events where `type==="expense" && spent > 0`
- These appear as read-only entries (purple border, "📊 תקציב" badge, no edit/delete)
- Labeled section: "📊 הוצאות מתקציב — עריכה רק מלשונית תקציב"
- Manual entries labeled: "📝 תנועות ידניות"
- `totalInKupa` in BudgetScreen header accounts for budget expenses

### Feature: Sort תקציב events by date
- `parseSortDate` parses `DD.MM.YY` / `DD.MM.YYYY` → timestamp
- Free-text dates (Hebrew, etc.) → `Infinity` (sorted to end)
- `sorted = [...filtered].sort(...)` used for render

### Feature: לפי קופה (replaced לפי נציג in מזומן)
- Shows all amounts (positive AND negative) from גבייה + מזומן + budget expenses
- Named collectors (paidBy) → grouped per person with signed balance
- No paidBy → summed into "🏦 קופת איסוף" (reconciles with Paybox/Bit)
- Footer row shows סה"כ = totalInKupa (full reconciliation check)
- Card shown when any entry is non-zero

## Important Architecture Notes
- NEVER define React components inside other components (causes remount loop)
- Budget expenses in מזומן are DERIVED at render time, not stored in cashLog
- `totalInKupa = collectedFromStudents + cashBalance + budgetExpTotal`
- Sum of all קופות (named + קופת איסוף) == totalInKupa (reconciles exactly)
