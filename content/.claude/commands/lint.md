# Lint Operation — Wiki Health Check

You are running a periodic health check on the research wiki. No arguments needed.

Read `Meta/schema.md` for the full lint rules before proceeding.

## Procedure

1. **Read `Meta/index.md`** to get a complete picture of all pages.
2. **Read `Meta/log.md`** to see recent operations and active areas.
3. **Run the checks below**, organized by severity.
4. **Report findings** as three separate lists (FAIL, WARN, INFO) with proposed fixes.
5. **Append new gaps to `Meta/open-questions.md`** — don't just report them in chat.
6. **Append to `Meta/log.md`**:
   ```
   ## [YYYY-MM-DD HH:MM] LINT | FAIL: N, WARN: N, INFO: N — <summary of most significant issues>
   ```

---

## LINT_FAIL — Must fix before further ingest in the affected area

These are blockers. Report each with a specific fix.

- **Atom missing required citation fields** (`source`, `juan`, `page`) for `atom_type: primary` or `secondary`
- **Synthesis paragraph without atom citation** — any paragraph on a `Wiki/sources/`, `Wiki/entities/`, or `Wiki/concepts/` page that ends without citing an atom ID
- **Atom with edited `## Original`** — if git is initialized: detect via `git diff` against the atom's creation commit; if not: flag this check as unenforced and remind user git is not yet initialized
- **File created outside schema-allowed paths** — any agent-created file not in `Wiki/`, `Meta/`, or `Summaries/`
- **Any modification to `Drafts/`** — if git is initialized: detect via git author in Drafts/ history; if not: flag as unenforced

---

## LINT_WARN — Suggest fix; user resolves

Report each with a specific proposed action.

- **Entity page with no atoms** — entity stubs in `Wiki/entities/` or `Officials/` with biographical claims but no atom citations
- **Concept page with no atoms** — concept pages making definitional claims without atom grounding
- **Orphan atom** — atom with no entity or concept linkage (not cited by any synthesis page)
- **Stale synthesis page** — a `Wiki/sources/`, `Wiki/entities/`, or `Wiki/concepts/` page whose `atoms_used:` frontmatter lists atoms with IDs more recent than the page's `last_updated:` date
- **Conflicting atoms** — two atoms making incompatible factual claims about the same person, date, or event (e.g., Liu Yaohui assigned to two different posts in the same month)
- **Modern social-science vocabulary in atom paraphrase** — flag terms: capitalism, nationalism, modernization, public sphere, ethnic group, class struggle. Permitted in concept pages only in sections marked as user-overlay.
- **Pinyin-only or Wade-Giles-only mention** — in a synthesis page, a Chinese person or place cited without characters
- **Lunar date without Gregorian (or vice versa)** — unless `date_approx: true` is set
- **Summaries/ page without a corresponding `Wiki/sources/` entry** — after migration begins, flag Summaries/ pages that haven't been promoted
- **Web-clip older than 90 days untouched** — if any web clips exist in the vault

---

## LINT_INFO — Visibility only; no action required

Report as a summary block, not individual items.

- **Wiki-wide counts** — atom count, entity count, concept count, thread count, source page count
- **Most-cited atoms** — top 5–10 atoms by citation count (signal of load-bearing claims worth verifying)
- **Most-orphaned concept pages** — concepts with no atom citations (gaps in the wiki)
- **Summaries/ migration progress** — N of 72 promoted to `Wiki/sources/`; N of 52 Officials/ promoted to `Wiki/entities/`
- **Open-questions count** — number of unresolved entries in `Meta/open-questions.md`
- **Unenforced checks** — list any LINT_FAIL checks that cannot be run because git is not initialized
