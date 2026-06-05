# Query Operation

You are running a structured research query against the wiki. The question is: $ARGUMENTS

## Procedure

1. **Identify candidate pages** — read `Meta/index.md` to find which `Wiki/sources/`, `Wiki/entities/`, `Wiki/concepts/`, and `Wiki/threads/` pages are most likely to contain relevant evidence. Also check `Summaries/` pages where atoms don't yet exist.

2. **Read the candidate pages** — do not answer from training-data knowledge; read the actual vault files. Where atoms exist, read the atoms cited from those pages.

3. **Synthesize a cited answer:**
   - If atoms exist: cite atom IDs — `[[Wiki/atoms/A-YYYYMMDD-HHMM-slug.md]]` — as the primary citation unit
   - If only Summaries/ pages exist: cite as `(Summaries/filename.md — specific claim)` and note that the citation is vault-file-level, not atom-level
   - Where evidence is strong, say so. Where it is inferential, say so. Where it is from training knowledge, flag it explicitly as non-vault.

4. **If the question is not answerable from existing wiki content:** say so explicitly — "no atoms or source pages in the wiki support a direct answer." Do not synthesize from training knowledge and present it as wiki-grounded. Identify the closest available evidence and what would need to be ingested to answer properly.

5. **Flag gaps** — if the query reveals a genuine research gap (missing evidence, not just unread sources), append it to `Meta/open-questions.md`.

6. **Offer to file the answer** — if the synthesized answer is substantial and reusable (a nuanced argument, a compiled table, a biographical synthesis), ask whether to save it as a new `Wiki/threads/` or `Wiki/entities/` page.

7. **Append to `Meta/log.md`**:
   ```
   ## [YYYY-MM-DD HH:MM] QUERY | <question summary> — <answer summary, 1–2 sentences>
   ```

## Citation Standard

In synthesis pages produced by this operation:
- Atom IDs are the preferred citation unit: `[[Wiki/atoms/A-YYYYMMDD-HHMM-slug.md]]`
- Summaries/ pages as fallback: `(Summaries/Author-Title.md)`
- Primary source notes: `(Primary Sources/Title.md, juan X)` — and note this is not yet atom-grounded
- Never cite the original publication directly — cite the vault's representation of it
