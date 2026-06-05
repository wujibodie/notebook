# Ingest Operation

You are ingesting a source into the research wiki. The source file path is: $ARGUMENTS

Read `Meta/schema.md` for the full page templates and citation standards before proceeding. The workflow differs by source type.

**Note on source types:** Files in `Primary Sources/` are full OCR extracts of scanned primary texts — they contain actual 文言 suitable for verbatim atoms. This folder is the main target for atom extraction. Files in `Dissertation/`, `Local Gazetteers/`, and `Camphor/` are typically research notes or secondary-level material and use Workflow B unless the file is clearly an OCR extract.

---

## Step 0: Identify and locate

Read the file at the path given. If the path doesn't exist, report and stop. Identify: Is this a primary source (classical Chinese text, archival document) or secondary source (monograph, article, dissertation)? Note the language.

Consult `Meta/glossary.md` to resolve any personal names, place names, and office titles to their canonical slugs. Flag ambiguous resolutions in `Meta/open-questions.md` rather than guessing.

---

## Workflow A: Primary textual source

*Use for: gazetteers, collected works, memorials, archival documents*

1. **Discuss key findings** — 3–5 sentences on what this source contributes. Flag anything surprising, contradictory, or load-bearing for the dissertation's core argument.

2. **Write or update the source page** at `Wiki/sources/s-<slug>.md` (see template in `Meta/schema.md`). Include structural enumeration (juan-by-juan or section-by-section) and mark which sections have been read.

3. **Extract atoms** for each passage worth tracking — verbatim `## Original` in 文言, `## Paraphrase` below it, and full frontmatter (edition, juan, page/folio, date_lunar, date_gregorian). **Hard rules:**
   - Verbatim `## Original` — no normalization of 異體字, no silent emendation
   - **Never infer dates.** If a source says only "去年" or "月", record that and leave `date_gregorian` blank with `date_approx: true`
   - If only year is known, use the first day of that year as `date_gregorian` with `date_approx: true`
   - Atom filenames: `Wiki/atoms/A-YYYYMMDD-HHMM-<slug>.md`

4. **Update entity and concept pages** — for each atom, add its ID to the `atoms_used:` frontmatter of the relevant `Wiki/entities/` and `Wiki/concepts/` pages. Create pages if they don't yet exist.

5. **Update `Meta/index.md`** — add or update the entry for the source page.

6. **Append to `Meta/log.md`**:
   ```
   ## [YYYY-MM-DD HH:MM] INGEST | <source slug> 卷N — <one-line summary>
   ```

7. **Stop and wait** — after each batch of 10–20 atoms, pause for user review before continuing to the next section.

---

## Workflow B: Secondary scholarship

*Use for: monographs, journal articles, dissertations in any language*

1. **Discuss key findings** — what argument does this source make, and how does it bear on the dissertation?

2. **Write or update the source page** at `Wiki/sources/s-<slug>.md`. Include: argument summary, methodological notes, primary sources the author uses, specific claims or data relevant to the dissertation, disagreements with other secondary literature (flag these in `Meta/open-questions.md`).

3. **Extract atoms only for specific cited claims** the user wants to track — not every assertion in the source. The user specifies which claims to atomize; everything else lives at source-page granularity. Use `atom_type: secondary`; `## Original` is a verbatim quote of the secondary author's claim with page citation.

4. **Update entity/concept pages**, `Meta/index.md`, and `Meta/log.md` as in Workflow A.

---

## Workflow C: Archival document

*Use for: Hamburg State Archives material, Milisch correspondence, Sōtokufu reports, etc.*

Same as Workflow A, but: replace juan/folio with archival reference (collection + box/folder + item number). Add `confidential: true` to atom frontmatter for unpublished archival transcriptions. Do not include confidential atoms in any output destined outside the vault.

---

## Language notes

- Chinese: translate key terms and passages into the paraphrase; leave `## Original` in characters
- Japanese: romanize names on first mention with 漢字; paraphrase in English
- German: paraphrase in English; quote key German phrases in `## Original` where they are technically precise
