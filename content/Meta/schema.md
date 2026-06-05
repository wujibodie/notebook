# Wiki Schema — Research Vault Knowledge Base

Full conventions for operating, maintaining, and growing the wiki. Read at session start or before a lint pass. The binding document is `HERMES.md`; this is the operational reference.

---

## Two-Tier Architecture

The wiki has two tiers. The difference is **not stylistic** — it is an enforced provenance contract.

**Tier 1 — Atoms** (`Wiki/atoms/`): Immutable. Each atom is a single source-anchored extract with a verbatim original, a citation to edition + 卷 + 葉, and a paraphrase. Atoms are written once and never edited. Errors are corrected by superseding: write a new atom naming the old one in `supersedes:` frontmatter, and add `superseded_by:` to the old atom. The old atom remains on disk.

**Tier 2 — Synthesis** (`Wiki/sources/`, `Wiki/entities/`, `Wiki/concepts/`, `Wiki/threads/`): Mutable. Every claim on a synthesis page must end with a citation to the atom(s) it draws from. A synthesis paragraph without an atom citation is a LINT_FAIL.

**The chain:** synthesis → atom → source. Every claim can be walked back to a specific folio in a specific edition in five minutes.

---

## Folder Map

```
Meta/                    operational files (agent + user co-edit)
  schema.md              this file
  index.md               category-organized catalog (agent-maintained)
  log.md                 append-only operation log
  glossary.md            name/place/title/text normalization; alias tables; date conversions
  open-questions.md      research gaps; appended by lint and agent; pruned by user
  decisions.md           schema changes and their rationales

Wiki/                    agent-owned knowledge content
  atoms/                 immutable atomic notes
  sources/               one synthesis page per source
  entities/              people, places, offices, institutions, texts
  concepts/              terms, institutions, processes
  threads/               research arguments in progress

Proto-wiki (overwritable; being migrated into the above):
  Summaries/             72 per-source summaries → target: wiki/sources/
  Officials/             52 entity stubs → target: wiki/entities/

Source material (agent reads, never writes):
  Primary Sources/          ← MAIN INGEST TARGET: full OCR extracts of scanned primary texts
  Local Gazetteers/         primary source notes on gazetteers (some may also be OCR extracts)
  Dissertation/             secondary scholarship notes
  Junping Junyao/           equalization research; Ming Shilu passages ready for atom conversion
  Camphor/                  camphor project research notes
  Bin Wong Qual Articles/   qualifying exam materials
  Sanjay Qual/              qualifying exam materials
  Evernote/                 miscellaneous imports
  [loose root files]

Hard firewall (agent must never write here under any circumstances):
  Drafts/
```

---

## Page Templates

### Atom (`Wiki/atoms/A-YYYYMMDD-HHMM-<slug>.md`)

```yaml
---
id: A-YYYYMMDD-HHMM
atom_type: primary        # primary | secondary | archival | observation
created: YYYY-MM-DD
verified: false           # true once user has checked against original
source: "[[Wiki/sources/s-<slug>]]"
edition: ""               # e.g. 光緒重刻本; 中華書局影印本
juan: ~
page: ""                  # 葉 and side (e.g. 12a–13b); page number for modern editions
date_lunar: ""            # e.g. 萬曆元年九月十五日
date_gregorian: ""        # ISO, e.g. 1573-10-30; leave blank if unknown
date_approx: false        # true if only year or month known — never infer
location: "[[Wiki/entities/]]"
entities: []
concepts: []
tags: []
supersedes: []
superseded_by: []
---

## Original

> [Verbatim 文言 or quoted text, faithful to the edition cited above.
>  No normalization of 異體字, no silent emendation, no modernization.]

## Paraphrase

[Modern Chinese or English paraphrase. Clearly marked as paraphrase.
 Sits below the original, never replaces it.]

## Note

[Optional: interpretive flag, ambiguity, or user observation.
 If it grows past a paragraph, promote to a thread page.]
```

**Hard rules:**
- `## Original` is verbatim. Do not normalize 異體字, expand abbreviations, or correct scribal error.
- For non-textual sources (maps, images, rubbings): `## Original` contains a description and a path to the asset.
- For secondary sources (`atom_type: secondary`): `## Original` is a verbatim quote of the secondary author's claim with page citation.
- For the user's own analytical observations (`atom_type: observation`): no source citation; the type flag prevents confusion with source-grounded claims.
- **Never infer dates.** If a source says only "去年", record "去年" in `date_lunar` and leave `date_gregorian` blank with `date_approx: true`.

---

### Source page (`Wiki/sources/s-<slug>.md`)

```yaml
---
type: source
title_cn: ""
title_en: ""
author: ""
compiler: ""
edition: ""               # edition(s) consulted
date_composed: ""
juan_total: ~
location: ""              # physical/digital copy location
project: ""               # Dissertation | Camphor | Both
ingested: YYYY-MM-DD
ingest_progress: ""       # e.g. "卷1–4 complete; 卷5 pending"
---
```

Body: structural enumeration (juan-by-juan or chapter-by-chapter), inline list of atoms from each section, gaps marked clearly. The source page is the navigation hub for one source.

---

### Entity page (`Wiki/entities/<slug>.md`)

```yaml
---
type: entity
entity_type: person       # person | place | office | institution | text
slug: ""
last_updated: YYYY-MM-DD
atoms_used: []
---
```

Sections in order: (1) names and aliases — characters (traditional), pinyin, Wade-Giles, 字, 號, posthumous title, other attested forms; (2) life dates — lunar + Gregorian, `date_approx: true` where uncertain; (3) one-paragraph brief — every claim ends with atom citation; uncited claims go to `Meta/open-questions.md` instead; (4) positions held — table: post | dates (lunar + Gregorian) | atom citation; (5) networks — linked entity slugs with relationship type; (6) associated concepts; (7) atoms citing this entity; (8) open questions.

---

### Concept page (`Wiki/concepts/<slug>.md`)

```yaml
---
type: concept
slug: ""
term_cn: ""
term_en: ""               # established translation, or blank if untranslatable
last_updated: YYYY-MM-DD
atoms_used: []
---
```

Sections: term and translations; period-specific definition (cited to atoms); how the concept evolves across the period; modern scholarly framings (marked explicitly as user-overlay; modern social-science vocabulary permitted only here); related concepts; atoms; open questions.

---

### Thread page (`Wiki/threads/t-<slug>.md`)

```yaml
---
type: thread
slug: ""
last_updated: YYYY-MM-DD
atoms_used: []
status: active            # active | dormant | promoted
---
```

A thread is a research argument in progress — explicitly not dissertation prose. If a thread matures into chapter-worthy material, the user copies it into `Drafts/` by hand. The agent never writes to `Drafts/`. Threads cite atoms heavily and may cite other threads.

---

## Citation Standards

**Primary sources:** edition + 卷 + 葉/folio + line if needed; modern reprint page in addition, never instead.

Example: `《萬曆泉州府志》卷四，葉十二a，乾隆四十六年重刻本；中華書局影印本第87頁。`

**Shilu and dated records:** additionally cite reign + year + month + fascicle number.

**Secondary sources:** author, title, year, page. Verbatim quotes in `## Original` of the atom.

**In synthesis pages:** cite atom IDs (`[[Wiki/atoms/A-20260426-1200-liu-yaohui-weisuo.md]]`). Synthesis pages never cite raw sources directly — the atom is the citation unit.

---

## Naming Conventions

| Page type | Location | Pattern |
|-----------|----------|---------|
| Atom | `Wiki/atoms/` | `A-YYYYMMDD-HHMM-<slug>.md` |
| Source | `Wiki/sources/` | `s-<slug>.md` |
| Entity | `Wiki/entities/` | `<slug>.md` (kebab-case pinyin) |
| Concept | `Wiki/concepts/` | `<slug>.md` (romanized term) |
| Thread | `Wiki/threads/` | `t-<slug>.md` |

No spaces in filenames.

---

## Name and Place Normalization

Every named individual has one canonical entity slug (simplified pinyin: `liu-yaohui`). The entity page lists all aliases. Ambiguous resolutions go to `Meta/open-questions.md`. Two distinct people with the same name get distinct slugs with a disambiguation note.

**Place names:** canonical form is the historical name in characters (福州府, 泉州府). Modern administrative equivalents are search aids only — never canonical.

Alias tables and reign-period/Gregorian conversions live in `Meta/glossary.md`.

---

## Language Conventions

- Classical Chinese is preserved verbatim in atoms. Paraphrase sits below, never above, never instead.
- Synthesis pages quote classical Chinese by pulling verbatim from the underlying atom — they do not re-paraphrase.
- Characters in synthesis: traditional by default (matches the sources). Simplified only for PRC scholarship that uses simplified.
- English register: clean academic. No coined neologisms. Period-specific terms (weisuo, lijia, junyao, wokou, haijin) untranslated, italicized on first use, linked to concept page.
- Japanese scholarship: name in 漢字 with reading on first mention.
- Modern social-science vocabulary (capitalism, nationalism, modernization, public sphere, ethnic group) is a LINT_WARN in atom paraphrases; permitted in concept pages only in sections marked as user-overlay.

---

## Log Format (`Meta/log.md`)

Append-only. Each entry begins with a level-2 header for grep-ability:
```
## [YYYY-MM-DD HH:MM] INGEST | <source slug> 卷N
## [YYYY-MM-DD HH:MM] QUERY  | <question summary>
## [YYYY-MM-DD HH:MM] LINT   | FAIL: N, WARN: N, INFO: N — <summary>
## [YYYY-MM-DD HH:MM] SYSTEM | <schema change, migration step, etc.>
```

---

## Index Format (`Meta/index.md`)

Category-organized. Each entry: `- [[path/to/file.md]] — one-line description`. Updated on every INGEST. Covers all pages in `Wiki/` plus key pages in `Meta/`.
