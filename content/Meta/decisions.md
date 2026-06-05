# Schema Decisions

When a schema rule changes, the rationale lands here so future sessions understand why. Ordered chronologically; newest last.

---

## 2026-04-26 — Initial architecture adopted from HERMES.md v0.1

**Decision:** Adopt HERMES.md's two-tier atom/synthesis model as the core architectural principle.

**Rationale:** The original wiki setup (flat Summaries/ pages) had no protection against document corruption: LLM-paraphrased claims could be re-read and re-paraphrased, compounding silently, with no traceable path back to a specific edition, juan, or folio. The atom layer solves this by enforcing immutability and verbatim preservation of original sources.

---

## 2026-04-26 — Meta/ folder separation adopted

**Decision:** Separate operational files (index, log, schema, glossary, open-questions, decisions) into `Meta/` rather than placing them in `Wiki/`.

**Rationale:** Wiki/ should contain only knowledge content (atoms, sources, entities, concepts, threads). Mixing operational scaffolding with content pages complicates navigation and makes it harder to reason about what the agent owns.

---

## 2026-04-26 — Officials/ and Summaries/ designated as proto-wiki layers

**Decision:** Both `Officials/` (52 entity stubs) and `Summaries/` (72 source summaries) are agent-overwritable interim structures, not raw sources. They will be migrated to `Wiki/entities/` and `Wiki/sources/` respectively as atom backfilling proceeds.

**Rationale:** These were generated before the two-tier model was in place. They contain useful material but lack atom-level provenance. Treating them as read-only would prevent the migration needed to achieve the full provenance contract.

---

## 2026-04-26 — Drafts/ firewall made explicit as hard prohibition

**Decision:** Added to all command files: the agent must never create, modify, rename, or delete any file under `Drafts/`. This applies even when the user asks open questions like "is this argument complete?" — the agent answers in chat, not by writing into `Drafts/`. The agent may read `Drafts/` files only when the user explicitly requests it.

**Rationale:** Drafts/ contains in-progress chapter prose. Inadvertent agent modifications would be very hard to detect and could corrupt the work.

---

## 2026-04-26 — Lint restructured as LINT_FAIL / LINT_WARN / LINT_INFO

**Decision:** Replaced the original P1/P2/P3 priority scheme with HERMES.md's three-level lint taxonomy.

**Rationale:** LINT_FAIL (blocker) / LINT_WARN (suggest) / LINT_INFO (visibility) more precisely captures which issues prevent further work vs. which are quality improvements. In particular, LINT_FAIL blocks further ingest in the affected area rather than just requesting user attention.

---

## 2026-04-26 — Git not yet initialized; atom immutability is convention only

**Decision:** Atom immutability will not be mechanically enforced until git is initialized in the vault root.

**Rationale:** Git diff is the cleanest mechanism for detecting post-creation atom edits. Until it is in place, immutability relies on the agent following the rule. Large-scale atom extraction should wait for git initialization.

---

## 2026-04-26 — extract-atoms-from-juan skill patched: annotated editions + long-text fallback

**Decision:** Added two new sections to the `extract-atoms-from-juan` skill based on findings from the first real atom extraction session (Lin Xiyuan Wenji, 卷首 + 卷一):

1. **§1.1 Modern annotated editions** — Rules for handling modern collated editions with inline numbered annotations ([1], 〔¹〕, etc.): strip all modern annotations from verbatim, preserve OCR uncertainty markers, record the editor in edition metadata.

2. **§3.1 Long-text fallback** — When a unit exceeds ~3,000 chars and full verbatim extraction would be unreliable in one pass, use structural paraphrase + `citation_precision: low` as an intermediate state, with the expectation of later supersede with full verbatim.

**Rationale:** The vault contains many modern collated editions (何丙仲校注, 曾祥波点校, etc.) with heavily annotated texts. Blindly copying inline annotations into verbatim would corrupt the `## Original` block. Additionally, some memorials are 5,000+ characters — transcribing them character-for-character in a single LLM turn risks omissions and errors. The fallback strategy provides a documented intermediate state that lint can track and the user can prioritize for later verification.
