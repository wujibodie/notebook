# Skill: extract-atoms-from-juan

**Version:** 0.4
**Models:** V4-Pro (extraction), V4-Flash (lint, citation audit), Kimi K2.6 (verification)
**Inputs:** `raw/primary/<source-slug>/<file>.md`
**Outputs:** atoms in `wiki/atoms/`, updated entity/concept/source pages, log entry

---

## 1. Input format (Zhiliu output)

YAML keys present: `source`, `total-pages`, `flagged-pages`, `status`, `ocr-engine`, `tags`. Body is continuous text under `## 全文整理`. May contain `## 研究笔记` (user notes) and `## 处理历史`.

NOT present: folio markers, page boundaries, per-section confidence, image cross-references, juan boundaries.

Structural signals in body:
- Repeated source-name lines + short title (juan markers, e.g. `止止堂集 / 横槊稿上`)
- Standalone short lines preceded/followed by blank lines (piece titles)
- Embedded reign-period dates (`嘉靖丁巳`, `萬曆丙戌春二月`)
- Genre-formulaic openings (`具官某告于`, `謹奏`, `銘曰`)

---

## 2. Atom unit: one text = one atom

**Binding rule. One text in the source = one atom. No atom contains two texts. No text spans two atoms. Length is irrelevant.**

| Genre | "One text" = |
|---|---|
| 文集 | one 序; one 詩 (with prose preface if present); one 詞/賦; one 祭文/告; one 墓誌銘 (with closing 銘); one 奏疏; one 書; one 記/碑/銘 |
| 方志 | one 子目 section (戶口, 田賦, 學校, 兵防, 災祥, 風俗, 物產) — one atom even when integrating centuries of data; one biography in 人物志; one piece in 藝文志 (文集 rules apply) |
| 奏議 | one memorial; 旨/批答 = separate atoms via `responds_to:` |
| 實錄 | one 條 |

Edge cases:
- **Sequenced poems** (病中偶成三首, 鐃歌十曲): N atoms; shared `piece_title`; `piece_subtitle: 其一/其二/...`; cross-link via `sibling_atoms:`.
- **Lists in 災祥**: integrating compiler voice → 1 atom; independent entries → N atoms.
- **Stitching artifacts**: do NOT atomize. Log to `meta/open-questions.md`. User repairs.

Sub-atoms via `parent_atom:` are user-discretionary. Agent never produces sub-atoms automatically.

---

## 3. Workflow

### Phase A — Structural reconnaissance (V4-Pro non-thinking)

Read `## 全文整理`. Produce structural map with: genre identification (`collected_works` / `gazetteer` / `memorial_collection` / `shilu` / `private_history` / `epigraphy` / `unknown`); juan-break candidates with confidence; logical units (`line_range`, `title|null`, `type_inferred`, `author_inferred|null`, `date_inferred|null`, `confidence`); unparseable regions.

Update `wiki/sources/s-<slug>.md`, mark `structural_map_status: provisional`. Report to user. **Stop and wait.**

### Phase B — Atom extraction (V4-Pro thinking)

Per logical unit:
1. Extract verbatim from line range. Preserve original punctuation, 異體字, `〇/口/□`, embedded brackets `〔〕` `（？）`.
2. Compute citation per §5.
3. Resolve entities to canonical slugs via `meta/glossary.md`. Ambiguous → `open-questions.md`, never into atom.
4. Identify concepts.
5. Extract dates: `date_lunar` from explicit text; `date_gregorian` only if unambiguous; else `date_approx: true`.
6. Write `## Paraphrase`. Write `## Note` only for genuine interpretive ambiguity.
7. Save as `wiki/atoms/A-YYYYMMDD-HHMM-<slug>.md`.
8. Pause every 15 atoms (5 in calibration mode). Present batch. **Stop.**

### Phase C — Cross-page propagation (V4-Pro non-thinking)

Update entity pages, concept pages, source page. Append to `meta/log.md`.

### Phase D — Lint (V4-Flash)

Run `lint-wiki` on affected pages. Surface LINT_FAIL in chat.

### Phase E — Citation precision audit (V4-Flash)

Set `citation_precision`:
- `high` — juan + title + line range + corroborating signal (date / author / cross-ref)
- `medium` — title + inferred juan, OR juan + uncertain title
- `low` — line range only
- `pending_scan` — would be medium/low but marked for image refinement

### Phase F — Verification sample (Kimi K2.6, async, stratified)

| Bucket | `char_count` | Sampling | Audit mode |
|---|---|---|---|
| Small | <500 | 15% | Whole atom |
| Medium | 500–5,000 | 10% | Whole atom |
| Large | 5,000–15,000 | 25% | One anchor section per cycle |
| Extreme | >15,000 | 100% over 12 mo | One anchor section per cycle |

K2.6 reads OCR file (NOT scan), verifies `## Original` matches OCR ll. L1–L2 character-for-character and paraphrase faithfully renders it. Catches extraction errors, not OCR errors. Log: `meta/audit-coverage.md`.

---

## 4. User-chunking mode

When auto-detection unreliable or user specifies, atomize within explicit chunks:

```yaml
chunks:
  - line_range: [33, 40]
    unit_type: preface
    title: "止止堂集序"
    juan: null
    author: "王世貞"
    date_lunar: "萬曆十四年二月既望"
    date_gregorian: "1586-03-26"
  - line_range: [42, 800]
    unit_type: container
    juan: "横槊稿上"
    extract_units: auto
```

Skips Phase A. Required when Phase A juan-confidence < 0.85.

Inline-chat paste: user pastes text + states title/genre/juan. Atom gets `from_chat_paste: true`, `citation_precision: medium`, no line range.

---

## 5. Citation

### 5.1 YAML fields

```yaml
source: "[[s-<slug>]]"
juan: <string|null>
juan_inferred: <string|null>
piece_title: <string|null>
piece_subtitle: <string|null>     # 其一/其二 for sequences
piece_ordinal: <int>
sibling_atoms: []
ocr_file: <path>
ocr_line_range: [<int>, <int>]
edition: <string|null>
edition_year_gregorian: <int|null>
holder: <string|null>
scan_image: <path|null>
citation_precision: high|medium|low|pending_scan
char_count: <int>                 # length of ## Original; drives Phase F
has_internal_anchors: <bool>
```

`char_count` updated only on supersede, not on metadata edits.

### 5.2 Citation strings (in `## Original` block)

```
High:        《止止堂集·横槊稿上·元宵王萬戶席上》（OCR ll. 51–52）。
Med (juan):  《止止堂集·〔横槊稿上〕·元宵王萬戶席上》（OCR ll. 51–52；juan待覆核）。
Med (title): 《止止堂集·横槊稿上·〔第五首〕》（OCR ll. 88；篇題待補）。
Low:         《止止堂集》（OCR ll. 259–263；juan、篇題俱待覆核）。
Pending:     《止止堂集·横槊稿上·讀史》（OCR ll. 46；待原書頁影核）。
With anchor: 《萬曆泉州府志·卷八·戶口》（OCR ll. 1432–1891；本atom含内部錨點）。
```

### 5.3 Edition backfill

When edition supplied later: backfill `edition`, `edition_year_gregorian`, `holder` to atoms in source. Requires user authorization. Log original frontmatter snapshot to `meta/log.md`.

### 5.4 Scan-image refinement

Scan supplied → update `scan_image:` and `citation_precision`. If scan reveals OCR error, create new atom with `supersedes:`. Never re-extract verbatim from scan into existing atom.

### 5.5 Within-atom citation (synthesis side)

Atoms with `has_internal_anchors: true` cited as `[[A-...#anchor-name]]`. Rules:
- Synthesis MUST use anchor form when atom has anchors and claim is localized → citing whole atom = LINT_WARN.
- Anchor names match headers verbatim (异体字, traditional/simplified preserved).
- Multi-section claims cite each anchor separately.
- Agent NEVER modifies atom anchors for citation convenience.

---

## 6. Atomization heuristics

### 6.1 Genre rules (one text = one atom, regardless of length)

文集: poem = 1; prose piece (序/記/銘/祭文/書/碑/疏/議) = 1; poem + prose preface = 1; 墓誌銘 + 銘曰 = 1; N首 = N atoms with `sibling_atoms:`.

方志: 子目 section = 1 (even at 30,000+ chars); biography in 人物志 = 1; 藝文志 piece = 1 (文集 rules).

奏議: memorial = 1; 旨/批答 = separate atoms with `responds_to:`.

實錄: 條 = 1.

### 6.2 Stitching-artifact detection

Signals: poem with non-uniform line lengths; prose → untitled partial poem → prose; mid-sentence logical breaks. Action: do NOT atomize. Log to `meta/open-questions.md`.

### 6.3 Date extraction

Recognize: reign + year (`嘉靖丁巳`); cyclical-only (requires juan-context disambiguation, flag if ambiguous); relative (`前年`, `去歲`, `客秋` — record relative, no Gregorian); time-relational (`未幾`, `頃之` — no date).

Never invent specificity. `去年` → record as `去年`, leave Gregorian empty, `date_approx: true`.

### 6.4 Entity extraction

Resolve all encountered names to canonical slugs via `meta/glossary.md`. Strip honorifics (`君`, `公`) for slug; preserve in `## Original`. Long entity lists in titles are normal (止止堂集 line 245 has 13+ officials in one poem title).

### 6.5 Untitled pieces

`piece_title: null`, `piece_ordinal: N`. Slug from first 10 chars. Note: "untitled in OCR; first line: 「...」".

### 6.6 Within-atom anchors

**Mandatory when ANY:**
1. `## Original` > 3,000 chars AND ≥3 distinct date markers
2. Structured numerical compilation organized by period/jurisdiction in source
3. Gazetteer 子目 section (any in §6.1)

When mandatory: set `has_internal_anchors: true`. Lint verifies headers exist.

Optional otherwise. 5,000-char coherent memorial without internal date-organized structure: no anchors.

**Anchors mirror source landmarks ONLY:**
- Year markers in original text (洪武二十四年, 嘉靖三十七年)
- 子目 names from gazetteer's organization
- Numbered subsections (其一, 其二; 一曰, 二曰)
- Source-indicated breaks (blank line, indentation, 子目 header)

**Forbidden:** anchors fabricated for tidiness ("early Ming", "mid Ming"). Atom mirrors source, not regularized version.

**Format:** H3 (`### `) inside `## Original`, separated from source text by blank lines. Compiler's intro/outro stay outside any anchor.

```markdown
## Original

> [compiler's intro prose]

### 洪武二十四年戶口

> 本府戶X，口Y。
> 晉江縣 戶X 口Y
> [...]

### 嘉靖三十七年戶口

> [census text]
> 本府戶X，口Y。較永樂時減六七。

> [compiler's closing commentary]

《萬曆泉州府志·卷八·戶口》（OCR ll. 1432–1891；本atom含内部錨點）。
```

Anchors are addressing scaffolding, not sub-atoms. Atom remains one file, one ID. Lint distinguishes: anchor = `[[A-...#name]]`; sub-atom = separate atom with `parent_atom:`.

---

## 7. OCR-error mitigations

V4 + K2.6 catch extraction errors, not OCR errors. Partial mitigations:
- **Genre-signal flagging.** Grammatically broken text, wrong-reign 避諱, regulated-verse violations (七律 with 8-char line) → set `ocr_uncertain: true`.
- **Cross-source corroboration.** Same `piece_title` in different sources → auto-compare; discrepancies → `open-questions.md`.

Periodic random scan-back audit (5 `citation_precision: high` atoms/quarter) is human work, not agent.

---

## 8. Refusals

Agent refuses to:
- Atomize stitching-artifact regions
- Atomize unclear regions without `ocr_uncertain: true`
- Invent dates not stated in source
- Invent entities not present in passage
- Apply anachronistic concepts to atom frontmatter without flagging
- Place paraphrase content in `## Original` block
- Modify atom content after creation (errors → new atom with `supersedes:`)
- Fabricate within-atom anchors not present in source structure
- Resolve ambiguous names without flagging to `open-questions.md`
- Silently normalize 異體字 / 通假字 / damaged characters (`〇`, `□`)

---

## 9. Worked example (schema reference)

Input: `raw/primary/zhi-zhi-tang-ji/zhi-zhi-tang-ji.md` lines 33–40, Wang Shizhen 序.

```yaml
---
id: A-20260425-1430
atom_type: primary
source: "[[s-zhi-zhi-tang-ji]]"
juan: null
juan_inferred: null
piece_title: "止止堂集序"
piece_subtitle: null
piece_ordinal: 1
sibling_atoms: []
unit_type: preface
ocr_file: "raw/primary/zhi-zhi-tang-ji/zhi-zhi-tang-ji.md"
ocr_line_range: [33, 40]
edition: null
edition_year_gregorian: null
holder: null
scan_image: null
citation_precision: medium
char_count: 612
has_internal_anchors: false
ocr_uncertain: false
date_lunar: "萬曆十四年二月十六日"
date_gregorian: "1586-03-26"
date_approx: false
location: null
entities:
  - "[[wang-shizhen]]"
  - "[[qi-jiguang]]"
related_entities:
  - "[[yi-yin]]"
  - "[[zhou-gong]]"
  - "[[lü-shang]]"
  - "[[zhongshan-fu]]"
  - "[[yin-jifu]]"
concepts:
  - "[[wen-wu-zhi-dao]]"
  - "[[xing-ming]]"
  - "[[bing-fa]]"
tags: [preface, literary-criticism, military-literature]
supersedes: []
superseded_by: []
---

## Original

> 吾今而後乃知文武之道也。當三代盛時...
> [verbatim, full text with original punctuation and 【？】 markers preserved]
> ...萬曆丙戌春二月既望，吳郡王世貞撰。

《止止堂集·〔序〕·止止堂集序》（OCR ll. 33–40；版本待補）。

## Paraphrase (Chinese)

[modern Chinese rendering]

## Note

OCR markers `【？】` at "立數剔朣" and "二幾" preserved. Latter likely OCR error of 「二紀」 (≈ 20 years). Needs scan verification.
```

---

*End.*
