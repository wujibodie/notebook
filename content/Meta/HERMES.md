# HERMES.md — Dissertation Research Wiki Schema

**Version:** 0.1 (initial draft, expected to iterate over weeks)
**Domain:** Late Ming Minnan, fiscal/military/commercial history c. 1522–1620, with secondary tracks for the Wang Daokun constellation, Taiwan/camphor/sovereignty material, and the deferred opium-governance project.
**Harness:** Hermes Agent (Nous Research)
**Primary models:** DeepSeek V4-Pro (ingest, classical Chinese reading), DeepSeek V4-Flash (lint, indexing, plumbing), Kimi K2.6 (cross-check audits), Claude (English prose for synthesis pages only)
**Scope of agent authority:** read-only over `raw/` and `Drafts/`; read–write over `wiki/` and `meta/`; write-only-with-supersede over `wiki/atoms/`.

This document is the binding configuration for the agent. Anything not specified here is not authorized. When the schema and a user instruction conflict, the agent must surface the conflict before acting.

---

## 0. Pre-Migration State (as of 2026-04-26)

This section documents the vault as it exists before Phase 0 migration. The target topology is in §3. Read this before acting on any migration step.

### Current folder structure

**Read-only for the agent (existing research notes; agent reads, never writes):**

```
Bin Wong Qual Articles/   qualifying exam materials — Qing fiscal, commercial, and administrative history (~11 files)
Camphor/                  19th-century Taiwan camphor project — Hamburg firms, consular records, Qing documents (~20 files)
Dissertation/             secondary scholarship notes across all dissertation themes (60+ files)
Evernote/                 miscellaneous imports
Junping Junyao/           equalization (均平) research — Ming Shilu passages (83 occurrences), philosophical genealogy
Local Gazetteers/         primary source notes on 12 gazetteers (Quanzhou, Zhangzhou, county-level)
Primary Sources/          full OCR extracts of scanned primary sources — collected works, memorials, gazetteers
                          (20+ files); this is the main target for atom extraction
Sanjay Qual/              qualifying exam materials — Iberian and Dutch maritime history (14 files)
```

Loose `.md` files at the vault root (individual article notes, miscellany) are also read-only.

**Hard firewall — agent must never create, modify, rename, or delete anything here:**

```
Drafts/
  Minnan in the Early Ming/        foundational chapter — geographic and economic context
  Currents of Reform/              empire-wide fiscal reform context
  The Coast - Liu Yaohui/          most developed chapter (~170 lines of prose in Diagnosing the Crisis.md)
  Shuangyu to Nan'ao/              early chapter (Chapter Three.md)
  Whipping the Waves/              chapter in progress (Pang Shangpeng and the Single Whip.md)
  Bibliography/
  Core Arguments (Intro? Conclusion?).md
```

**Proto-wiki layers (overwritable by agent; to be remapped or replaced during migration):**

```
Summaries/    72 LLM-generated per-source summary pages; one file per source; maps to wiki/sources/ in the
              target architecture; no atom structure; provenance is vault-file level only, no edition/juan/folio

Officials/    52 structured entity .md files with YAML frontmatter (name_cn, name_en, zi, hao, native_place,
              jinshi_year, posts, mention_count, relationship_count, Summaries/ source links, network
              connections with weights); maps to wiki/entities/ in target architecture; lacks atom citations,
              dual dates, full alias tables, and verified biographical claims
```

**Newly created wiki infrastructure (2026-04-26):**

```
Meta/         operational files: index.md (catalog of Summaries/ pages), log.md (operation log),
              schema.md (conventions reference), plus glossary.md, open-questions.md, decisions.md
              to be created in Phase 0

Wiki/         content wiki: atoms/, sources/, entities/, concepts/, threads/ subdirectories created
              but empty; this is the target location for all agent-generated knowledge content
```

**Schema documents:**

```
CLAUDE.md     descriptive vault guide — informative for the agent, not binding
HERMES.md     this document — to be moved to Meta/ in Phase 0
```

### What is not yet in place

- **Git not initialized.** The atom immutability contract (§2) relies on `git diff` to detect post-creation edits to atoms. Until git is initialized, immutability is a convention without enforcement. Do not begin large-scale atom extraction (§9 skills) until git is in place.
- **`raw/` folder does not exist.** Sources are in the existing folders listed above. The §6 ingest workflows that reference `raw/primary/` and `raw/secondary/` describe the target state. For now, treat `Primary Sources/` as the functional equivalent of `raw/primary/` — it contains full OCR extracts ready for atom extraction. `Dissertation/`, `Local Gazetteers/`, `Camphor/`, and `Junping Junyao/` are the equivalents of `raw/secondary/` and `raw/archives/`.
- **`Meta/glossary.md`, `Meta/open-questions.md`, `Meta/decisions.md`** need to be initialized in Phase 0.
- **`Summaries/` and `Officials/`** are interim structures with useful material but no atom-level provenance. Migration approach: use as starting material for `wiki/sources/` and `wiki/entities/` pages during Phases 1–2, backfilling atom citations as primary sources are processed.

---

## 1. Purpose of the Wiki

The wiki exists to make a growing body of late-Ming primary and secondary sources navigable, cross-referenced, and queryable without the user (Patrick) having to do the bookkeeping. It is **not** a writing surface for the dissertation, conference papers, Motes essays, or job-market materials. It is a curated, audit-able knowledge base feeding into those, the way a research notebook feeds into a chapter draft.

The wiki has two failure modes that must be designed against:

1. **Document corruption.** LLM-paraphrased claims on synthesis pages drift from what the underlying sources actually say, then become load-bearing for further synthesis. This compounds silently.
2. **Provenance loss.** A claim survives in the wiki without a traceable path back to a specific 卷, 葉, or page in a specific edition. This makes the wiki unusable for actual scholarship.

Every rule below exists to prevent one or both of these.

---

## 2. The Core Architectural Rule: Two-Tier Hybrid

The wiki has two tiers, and the difference between them is **not stylistic**. It is an enforced contract.

### Tier 1: Atoms (immutable)

An atom is a single source-anchored extract or claim with an identifier, a citation, and (where the source is textual) a verbatim original passage. Atoms are written once and **never edited**. If an atom is wrong or superseded, the response is to write a new atom that names the old one in `supersedes:` frontmatter. The old atom remains on disk with `superseded_by:` added.

The reason for immutability: atoms are the only layer that can be audited against the original sources. If they are revised, the audit trail dissolves.

### Tier 2: Synthesis (mutable, derived)

Entity pages, concept pages, thread pages, and source-overview pages are synthesis. They are mutable and the agent regenerates or revises them on every relevant ingest. **Every paragraph in a synthesis page must end with citations to the atoms it draws from.** A synthesis paragraph without an atom citation is a lint failure, full stop.

Synthesis pages carry a `regenerated:` timestamp in frontmatter and an `atoms_used:` manifest. If atoms in the manifest have been updated since `regenerated:`, the page is marked stale.

### The contract

- **Atoms cite sources. Synthesis cites atoms. Nothing on synthesis pages cites raw sources directly.**
- The agent never paraphrases a primary source onto a synthesis page without the paraphrase first existing on an atom.
- When in doubt, write an atom; never write into synthesis what isn't yet atom-grounded.

This contract is what protects against document corruption: every claim has a chain `synthesis → atom → source` that can be walked in five minutes.

---

## 3. Vault Topology

The vault expands the existing structure rather than replacing it. Existing folders keep their contents. New folders take agent-generated material.

```
vault/
  raw/                              # NEW. Immutable. Agent reads, never writes.
    primary/                        # gazetteers, collected works, memorials, archive scans
    secondary/                      # PDFs of monographs and articles
    archives/                       # Milisch correspondence, Sōtokufu material, etc.
    web-clips/                      # Obsidian Web Clipper output
    assets/                         # downloaded images, maps, charts (set in Obsidian: raw/assets/)
  wiki/                             # NEW. Agent-owned. The two-tier hybrid lives here.
    atoms/                          # immutable atomic notes
    sources/                        # one synthesis page per source in raw/
    entities/                       # 人物、地名、官職、書名、機構
    concepts/                       # 一條鞭法、海禁、均平、衛所、etc.
    threads/                        # research threads / arguments-in-progress
  meta/                             # NEW. Agent and user co-edit.
    HERMES.md                       # this document
    index.md                        # category-organized catalog (agent-maintained)
    log.md                          # append-only chronological log
    glossary.md                     # term normalization, alias tables
    open-questions.md               # generated by lint; reviewed by user
    decisions.md                    # schema decisions and their rationales
  Dissertation/                     # EXISTING. Agent reads, never writes.
  Drafts/                           # EXISTING. Agent reads, NEVER writes. Hard firewall.
  Junping Junyao/                   # EXISTING. Migrate gradually (see §11).
  Local Gazetteers/                 # EXISTING. Agent reads. Treat as raw/primary/ for now.
```

### The Drafts/ firewall

`Drafts/` contains your in-progress chapter prose: the Liu Yaohui chapter, the Currents of Reform pieces, the Minnan in the Early Ming foundational chapter. The agent **must never** create, modify, rename, or delete files anywhere under `Drafts/`. The agent may read these files for context only when the user explicitly asks ("look at how I framed Liu's mandate in `Diagnosing the Crisis.md`"). The agent must not propose edits to `Drafts/` files even when asked an open question like "is this argument complete?" — it should answer in chat, not by writing into `Drafts/`.

The same firewall applies, by extension, to any file the user later marks `agent_writable: false` in frontmatter.

### Existing files that bridge the architecture

The current vault already contains material that maps onto the two-tier model, just not cleanly separated:

- **`Dissertation/Onomastic Index.md`** is a flat entity database. It bootstraps `wiki/entities/`. The agent should not modify the existing file. Instead, on first run, it generates one `wiki/entities/<slug>.md` page per person, importing the biographical detail and adding a backlink to the source row in `Onomastic Index.md`. The original file remains as a reference, but new entity work happens in the per-person pages.
- **`Junping Junyao/Ming Shilu.md`** is a proto-atom collection: 83 passages of 均平 with citations. Each row should become one atom (`A-…`) in `wiki/atoms/` with the original verbatim, citation to 卷/條, and `concept: [[junping]]` linkage. The original file stays as a navigable index of those atoms.
- **`Junping Junyao/Random Quotes.md`** is mixed: some entries are atoms (specific passages), some are synthesis. The agent should propose a row-by-row classification before doing anything.
- **`Local Gazetteers/`** files are research notes ON gazetteers. Treat the gazetteers themselves as primary sources in `raw/primary/`; the existing notes become `wiki/sources/` synthesis pages, and specific extractable claims become atoms.
- **`Dissertation/`** secondary-scholarship notes (K.L. So, Fu Yiling, Rawski, etc.) become `wiki/sources/` pages of the secondary type, with atoms tagged `atom_type: secondary` to distinguish from primary extractions.

Migration is gradual and user-supervised. See §11.

---

## 4. Page Typologies and Templates

### 4.1 Atom

Filename: `A-YYYYMMDD-HHMM-<short-slug>.md`. Example: `A-20260425-1530-liu-yaohui-on-weisuo-decay.md`.

```yaml
---
id: A-20260425-1530
atom_type: primary           # primary | secondary | archival | observation
created: 2026-04-25
created_by: deepseek-v4-pro  # which model wrote it; "human" if hand-written
verified: false              # true once user has checked against original
source: "[[s-liu-yaohui-memorials]]"   # link to source page
edition: "光緒重刻本"           # edition matters; record it
juan: 4
page: "12a-13b"              # 葉/folio for traditional pagination
date_lunar: "萬曆元年九月"
date_gregorian: "1573-10"    # approximate is fine; mark as approx if so
date_approx: false
location: "[[fuzhou-prefecture]]"
entities: ["[[liu-yaohui]]", "[[zhang-juzheng]]"]
concepts: ["[[weisuo-system]]", "[[fiscal-military-deadlock]]"]
tags: [memorial, military, fiscal]
supersedes: []
superseded_by: []
---

## Original

> [verbatim 文言, faithful to the edition cited above; no normalization
>  of variant characters, no silent emendation, no modernization]

## Paraphrase

[modern paraphrase — Chinese or English, agent's choice based on
 the entity/concept the atom is feeding into. Marked clearly as paraphrase.
 Never replaces the original, always sits below it.]

## Note

[optional: user's marginal observation, or agent's flag of an interpretive
 ambiguity. Kept brief. If it grows past a paragraph, promote to a thread.]
```

**Hard rules for atoms:**

- The `## Original` block is verbatim. The agent does not normalize 異體字, expand abbreviations, or correct what looks like scribal error. If the edition has 「衞」, the atom has 「衞」.
- If the source is non-textual (an image, a map, a coin, a stele rubbing), the atom contains a description in `## Original` and must include a path to the asset under `raw/assets/`.
- If the atom is from a secondary source (`atom_type: secondary`), `## Original` may be a quoted paraphrase of the secondary author's claim, but must still include the page citation. `verified: true` here means "I have checked the secondary author cites their primary source correctly."
- Atoms about the user's own observations (`atom_type: observation`) require no source citation but must be flagged so they are never confused with source-anchored claims.

### 4.2 Source page

Filename: `s-<slug>.md`. Example: `s-wanli-quanzhou-fuzhi.md`.

Frontmatter: title (Chinese + English), compiler, edition(s) consulted, date of compilation, location of physical/digital copy, total juan, current ingest progress.

Body: a structural enumeration (juan-by-juan, fascicle-by-fascicle), an inline list of atoms extracted from each section, gaps marked clearly. The source page is the navigation hub for one source.

### 4.3 Entity page

Filename: `<slug>.md` under `wiki/entities/`. Sections, in order: names and aliases (with characters, pinyin, Wade-Giles, hao, zi, posthumous title); life dates; one-paragraph brief; positions held with dates (lunar + Gregorian); networks (linked entities); concepts associated; atoms citing this entity (auto-generated list via Dataview-compatible query block); open questions about this entity.

Hard rule: every claim in the brief and the positions-held section ends with atom citation. If you can't cite an atom, the claim doesn't go on the entity page yet — it goes in `open-questions.md`.

### 4.4 Concept page

Filename: `<slug>.md` under `wiki/concepts/`. Sections: term and translations; period-specific definition (with atom citations); how the concept evolves across the period; modern scholarly framings (treated as analysis, marked as user-overlay, may contain modern social-science vocabulary); related concepts; atoms; open questions.

### 4.5 Thread page

A thread is a research argument-in-progress. Filename: `t-<slug>.md`. Threads are where exploration happens — comparison, hypothesis, "what if" reasoning. They cite atoms heavily and may cite other threads. They are explicitly **not** dissertation prose; if a thread matures into chapter-worthy material, the user copies it into `Drafts/` by hand, where the agent will not touch it.

### 4.6 Index, log, glossary, open-questions, decisions

- `index.md`: agent-maintained catalog organized by category. Updated on every ingest.
- `log.md`: append-only. Every entry begins `## [YYYY-MM-DD HH:MM] <op> | <subject>` for grep-ability.
- `glossary.md`: alias tables for names (人名), places (地名), titles (官名), texts (書名), and reign-period/Gregorian conversions. The single most leverage-y plumbing file.
- `open-questions.md`: generated by lint and by the user. The agent appends; the user prunes.
- `decisions.md`: when a schema rule changes, the rationale lands here so future-you understands why.

---

## 5. Citation, Naming, Language, Date Conventions

### 5.1 Source citation

Primary textual sources cite **edition + 卷 + 葉 (folio side a/b) + line if needed**. Modern reprints cite the modern edition's page in addition, never instead. For shilu and other multi-section sources, also cite reign + year + month + the fascicle's editorial number.

Example acceptable citation: `《萬曆泉州府志》卷四，葉十二a，乾隆四十六年重刻本，廈門大學圖書館藏；中華書局影印本第87頁。`

### 5.2 Name normalization

Every named individual has one **canonical entity slug**. Choose simplified-pinyin form for filenames (`liu-yaohui`), but the entity page itself lists all aliases: 劉堯誨 / 劉堯誨 (traditional same here) / 劉藎卿 / 字藎卿 / Liu Yaohui / Liu Yao-hui.

The agent must resolve all encountered forms to the canonical slug on ingest. Ambiguous resolutions go to `open-questions.md`. Two distinct people with the same name get distinct slugs (`liu-yaohui-1522` vs `liu-yaohui-jurchen`) and a disambiguation note.

Place names: canonical form is **historical name in characters** (`福州府`, `泉州府`), with modern administrative equivalent listed in the entity page but never used as the canonical form. Modern names are search aids only.

### 5.3 Language

**Classical Chinese is preserved verbatim.** Atoms quoting 文言 keep the original; paraphrase sits beneath it, never above, never instead. The agent never silently renders 文言 into modern Chinese on a synthesis page; if a synthesis page needs to quote, it pulls the verbatim original from the underlying atom and quotes it as a quote.

Chinese characters in synthesis pages: traditional by default (matches your sources). Simplified is used only when discussing modern PRC scholarship that uses simplified.

English in synthesis pages: clean academic register. The agent does not coin neologisms. Period-specific terms (weisuo, lijia, junyao, wokou) are kept untranslated and italicized on first use, with a brief gloss linked to the concept page.

Japanese scholarship references: name in 漢字 with reading in furigana on first mention, then 漢字 only.

### 5.4 Dates

Every dated atom carries both lunar and Gregorian. Reign year is in `date_lunar:` (e.g., `"萬曆元年九月十五日"`); ISO Gregorian goes in `date_gregorian:` (`"1573-10-30"`). When the lunar date is approximate (only month known, only year known), use `date_approx: true` and the closest defensible Gregorian range.

The agent does **not** infer dates. If a source says only "去年", the atom records "去年" with a lunar context note, and the Gregorian field is left empty with `date_approx: true`.

### 5.5 Bilingual considerations for the job market

Where wiki content might later inform Chinese-language job-market materials (Hong Kong, mainland 世界史/海洋史 positions), atoms should preferentially carry Chinese paraphrases alongside English. This is a soft rule for now; revisit when the application timeline is closer.

---

## 6. Ingest Workflows

### 6.1 Primary textual source (e.g. a new juan of 太函集 or a gazetteer chapter)

1. User drops the source (PDF, OCR'd text from Zhiliu, or transcription) into `raw/primary/<source-slug>/`.
2. Agent (V4-Pro, non-thinking mode) reads the table of contents and writes/updates `wiki/sources/s-<slug>.md` with structural enumeration. No atoms yet.
3. User specifies which juan/section to ingest.
4. Agent (V4-Pro, thinking mode) extracts atoms one passage at a time. Each atom gets verbatim original + paraphrase + minimal note. The agent flags ambiguities rather than guessing.
5. After each batch (10–20 atoms), agent updates relevant entity and concept pages with new atom citations. Synthesis paragraphs are revised to reflect new evidence; conflicting atoms are flagged in `open-questions.md`.
6. Agent appends `## [date] ingest | <source> 卷N` to `log.md`.
7. **Stop.** Wait for user review before processing the next juan.

For a 200-page gazetteer, this means ingest happens over weeks, not in one session. That is correct.

### 6.2 Secondary scholarship (English/Japanese monograph or article)

1. Source goes in `raw/secondary/<author-year-slug>/`.
2. Agent (V4-Pro) reads and produces a `wiki/sources/s-<author-year>.md` page: argument summary, methodological notes, primary sources used, gaps relevant to the dissertation.
3. Atoms (`atom_type: secondary`) are extracted only for **specific cited claims** the user wants to track — not for every assertion in the book. The user picks which claims to atomize. Most secondary scholarship lives at source-page granularity.
4. Disagreements with other secondary scholarship surface in `open-questions.md` as a comparison item.

### 6.3 Web clip (Obsidian Web Clipper output)

1. Goes in `raw/web-clips/`. Title and source URL captured automatically.
2. Agent treats as ephemeral: produces a brief summary at most, no atoms unless the user upgrades it to a tracked source.
3. After 90 days, lint flags untouched web-clips for archival or deletion.

### 6.4 Archive material (Milisch correspondence, Sōtokufu reports)

1. Each document gets a source page even if very short — archives are typically letter-by-letter or report-by-report.
2. Atoms include archival reference (collection, box, folder, item) instead of juan/page.
3. Sensitive material (working drafts of unpublished archive transcriptions) carries `confidential: true` frontmatter; agent must not include such atoms in any output destined for outside the vault.

---

## 7. Query Workflow

When the user asks a substantive question:

1. Agent (V4-Flash) reads `meta/index.md` and identifies candidate pages.
2. Agent (V4-Pro) reads the candidate entity, concept, and thread pages, then the atoms cited from those pages.
3. Agent answers in chat with citations — atom IDs first, source citations via the atoms.
4. If the answer is non-trivial and likely to be useful again, agent offers to file it as a new thread page. User confirms. Filed answer is then itself a synthesis page subject to all synthesis rules.

When the user asks a question and the answer is not derivable from existing atoms, agent says so explicitly: "no atoms in the wiki support a direct answer; closest material is X; want me to flag this in `open-questions.md`?" The agent does **not** answer from model priors and present it as wiki-grounded.

---

## 8. Lint Workflows

Lint runs on demand and weekly via Hermes scheduled automation. V4-Flash is the lint model.

### 8.1 LINT_FAIL (must fix before further ingest in affected area)

- Atom missing `source`, `juan`, `page` (for primary/secondary types)
- Atom edited after creation (detected by git diff against last commit; should not happen if rules are followed)
- Synthesis paragraph without trailing atom citation
- Drafts/ folder modified by agent (this is a hard regression test — the agent's git author should never appear in `Drafts/` history)
- Atom with `## Original` block silently emended (detected by re-checking against `raw/`)
- File created outside the schema's allowed paths

### 8.2 LINT_WARN (suggest, user resolves)

- Entity page with no atoms
- Concept page with no atoms
- Atom orphan (no entity or concept linkage)
- Stale synthesis (atom in `atoms_used:` updated since `regenerated:`)
- Two atoms with conflicting factual claims (e.g., Liu Yaohui in two different posts in the same month)
- Modern social-science vocabulary in atom paraphrase (a soft heuristic list: capitalism, nationalism, class struggle, modernization, ethnic group, public sphere — flag, don't block)
- Pinyin-only or Wade-Giles-only mention without canonical character form
- Lunar date without Gregorian or vice versa (allowed only with `date_approx: true`)
- Web-clip older than 90 days untouched

### 8.3 LINT_INFO (visibility only)

- Wiki-wide atom count, entity count, concept count
- Most-cited atoms (signal of load-bearing claims worth verifying)
- Most-orphan concept pages (gaps in the wiki)
- Suggested new questions to investigate (Kimi K2.6 generates these monthly; user reviews)

---

## 9. Hermes Skills

Each skill is a narrow, parameterized procedure. Skills live in `~/.hermes/skills/<skill-name>/skill.md` per the Hermes/agentskills.io convention.

Initial skill set:

- **`extract-atoms-from-juan`** — input: source slug, juan number, page range. Output: N atom files. Model: V4-Pro thinking. Always asks for user confirmation between batches of 10.
- **`update-entity-on-new-atom`** — input: atom ID. Output: updated entity pages. Model: V4-Pro non-thinking.
- **`regenerate-synthesis-page`** — input: page path. Output: rewritten page citing atoms. Model: Claude (when target is `entities/`, `concepts/`) or V4-Pro (when target is `threads/` and reasoning matters more than prose). Adds `regenerated:` timestamp.
- **`lint-wiki`** — runs §8 checks. Model: V4-Flash. Outputs to `meta/lint-report.md`.
- **`audit-atom`** — input: atom ID. Cross-checks atom against source file in `raw/`. Model: Kimi K2.6 (independent reading). Used periodically on samples or on flagged atoms.
- **`resolve-name`** — input: a name as encountered in a source. Output: canonical slug or "ambiguous, see open-questions". Model: V4-Flash. Heavy use of `glossary.md`.
- **`migrate-onomastic-index`** — one-time skill to crawl `Dissertation/Onomastic Index.md` and propose entity-page splits. Output: a draft of `wiki/entities/` for user review.
- **`migrate-ming-shilu-passages`** — one-time skill to convert each row of `Junping Junyao/Ming Shilu.md` into an atom.
- **`generate-open-questions`** — input: scope (entity, concept, or wiki-wide). Output: appended entries in `meta/open-questions.md`. Model: Kimi K2.6.

Skills are versioned. When a skill is updated, the change goes in `meta/decisions.md` with rationale.

---

## 10. Model Routing

| Task | Model | Mode |
|---|---|---|
| Atom extraction from primary 文言 | DeepSeek V4-Pro | thinking |
| Source structural enumeration | DeepSeek V4-Pro | non-thinking |
| Entity / concept page regeneration | Claude (Opus 4.7) | — |
| Thread page drafting | DeepSeek V4-Pro | thinking |
| Lint, indexing, frontmatter validation | DeepSeek V4-Flash | non-thinking |
| Name resolution / glossary lookup | DeepSeek V4-Flash | non-thinking |
| Atom audit (verification against source) | Kimi K2.6 | — |
| Open-question generation | Kimi K2.6 | — |
| Secondary-source summary | Claude or V4-Pro | — |

Routing is hardcoded in skills, not chosen at query time. The cost/quality calculus is more stable than per-query routing logic and easier to audit.

---

## 11. Migration Plan from Existing Vault

This is staged. Do not attempt all at once.

### Phase 0 — Setup (week 1)

- Create `raw/`, `wiki/`, `meta/` directories.
- Place this `HERMES.md` in `meta/`.
- Initialize `index.md`, `log.md`, `glossary.md`, `open-questions.md`, `decisions.md` as empty files with skeletons.
- Configure Obsidian: attachment folder → `raw/assets/`; Web Clipper → `raw/web-clips/`.
- Initialize git in vault root if not already.
- Stand up Hermes Agent with the skill set in §9, hardcoded model routing per §10.

### Phase 1 — Bootstrap entities (week 1–2)

- Run `migrate-onomastic-index`. Review proposed entity pages. Approve a first batch of ~30 (Liu Yaohui, Zhang Juzheng, Pang Shangpeng, Yu Dayou, Tan Lun, Lin Feng, Lin Xiyuan, Qi Jiguang, plus the most-cited names from your dissertation drafts).
- Hand-edit any entity page where the agent's import is wrong. Hand-edits become reference for refining the migration skill.

### Phase 2 — Bootstrap atoms via Ming Shilu passage tracker (week 2–3)

- Run `migrate-ming-shilu-passages`. This produces ~83 atoms with `concept: [[junping]]`. The 均平 concept page becomes the first real test case for synthesis regeneration.
- Audit a 10% sample with Kimi K2.6 (`audit-atom`).

### Phase 3 — First primary-source ingest (week 3–4)

- Pick one juan of 萬曆泉州府志 with material relevant to the Liu Yaohui chapter. Run `extract-atoms-from-juan`.
- Verify every atom by hand. This is your calibration set.
- Regenerate the Liu Yaohui entity page and at least one concept page (e.g., 衛所制) from the new atoms.

### Phase 4 — Liu Yaohui chapter cross-reference (week 4–6)

- Read your `Drafts/The Coast - Liu Yaohui/Diagnosing the Crisis.md` against the now-existing entity and concept pages. The wiki should be able to support every footnote-worthy claim in the chapter via atom citations, or expose a gap worth investigating.
- Gaps go in `open-questions.md`. The chapter is **not** rewritten from the wiki.

### Phase 5 — Expand outward (ongoing)

- Pang Shangpeng Records, Zhang Letters, the Yu Dayou Quanji, Tan Lun's memorials. One source at a time.
- Local Gazetteers folder: ingest one gazetteer per month.
- Begin pulling in the Wang Daokun material (Taihan Ji) when the schema has stabilized — that constellation will stress-test the entity/network handling.

### Phase 6 — Guangzhou prep (Aug–Sep 2026)

- Before the residency: `lint-wiki`, prune orphans, regenerate stale synthesis. Export a snapshot.
- During the residency: archive findings come in fresh as atoms. The wiki is now a working research tool, not a migration project.

---

## 12. Hard Prohibitions

The agent must never:

1. Modify, create, or delete any file under `Drafts/`.
2. Edit an atom after creation. Errors are corrected via `supersedes:`.
3. Paraphrase 文言 onto a synthesis page without first creating an atom containing the verbatim original.
4. Infer dates not stated in the source.
5. Silently translate place names to modern administrative equivalents.
6. Coin English neologisms for late-Ming institutions (use the established term in italics + a glossary link, or leave it untranslated).
7. Assert a claim on any synthesis page without an atom citation.
8. Adapt analytical conclusions to user preferences as part of the Honcho user model. Stylistic preferences (traditional vs simplified, footnote format, English vs Chinese paraphrase) are fine to learn. Substantive interpretive positions ("Patrick thinks Jiao Hong was a Yangming sympathizer") must not be modeled, because the model will then begin confirming them on ingest.
9. Send any atom or synthesis page marked `confidential: true` to an external service that does not honor the project's data policy. (For DeepSeek V4 via the official API, this means treating archival transcriptions as non-confidential by default; route confidential material through a self-hosted V4-Flash deployment or skip agent processing entirely.)
10. Use a model not listed in §10 without an entry being added to `decisions.md` first.

---

## 13. Co-evolution Notes

This document is v0.1. Expect to revise weekly for the first month and monthly thereafter. Specific decisions deferred to later revisions:

- **Search.** At current scale (hundreds of pages projected), `index.md` plus Obsidian's built-in search should suffice. Reconsider if/when atom count exceeds ~2,000. `qmd` (Tobi's tool) is a candidate.
- **Confidentiality and archival material.** Concrete data-policy choices for archive transcriptions (Sōtokufu, Milisch correspondence) need a decision before Phase 5 expands into archives. Default until then: do not ingest archival material via the cloud API.
- **Bilingual atom defaults.** Whether atoms default to Chinese paraphrase, English paraphrase, or both. Currently agent's choice; revisit when first job applications go out.
- **Image and map handling.** Currently atoms can reference assets; richer image-aware ingest (e.g., reading a map of 衛所 distribution) deferred until the text pipeline is stable.
- **Integration with Zhiliu.** The OCR pipeline upstream of `raw/primary/` should produce text in a consistent format the agent can rely on. Define the contract in `decisions.md` once Zhiliu's classical-Chinese output schema is finalized.
- **Drafting back into Motes / Substack.** Currently out of scope. The wiki feeds; it does not draft public-facing prose. Reconsider only if a clear safe-mode emerges.

When this document is revised, the previous version is preserved via git, and the rationale for the change is recorded in `meta/decisions.md`. The agent reads `HERMES.md` at the start of every session and surfaces any rule it does not understand before acting.

---

*End of HERMES.md v0.1.*
