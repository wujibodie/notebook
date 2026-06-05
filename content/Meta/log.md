     1|     1|     1|     1|# Wiki Operation Log
     2|     2|     2|     2|
     3|     3|     3|     3|Append-only. Each entry begins with a level-2 header for grep-ability.
     4|     4|     4|     4|
     5|     5|     5|     5|```
     6|     6|     6|     6|## [YYYY-MM-DD HH:MM] INGEST | <source slug> 卷N
     7|     7|     7|     7|## [YYYY-MM-DD HH:MM] QUERY  | <question summary>
     8|     8|     8|     8|## [YYYY-MM-DD HH:MM] LINT   | FAIL: N, WARN: N, INFO: N — <summary>
     9|     9|     9|     9|## [YYYY-MM-DD HH:MM] SYSTEM | <schema change, migration step, etc.>
    10|    10|    10|    10|```
    11|    11|    11|    11|
    12|    12|    12|    12|---
    13|    13|    13|    13|
    14|    14|    14|    14|## [2026-04-26 00:00] SYSTEM | Wiki system initialized
    15|    15|    15|    15|
    16|    16|    16|    16|Schema, index, and log created. Existing `Summaries/` pages (72) cataloged in index. `Officials/` (52) identified as proto-entity layer.
    17|    17|    17|    17|
    18|    18|    18|    18|## [2026-04-26 00:00] SYSTEM | Restructured per HERMES.md architecture
    19|    19|    19|    19|
    20|    20|    20|    20|- `Meta/` folder created; index.md, log.md, schema.md moved from `Wiki/` to `Meta/`
    21|    21|    21|    21|- `Wiki/` restructured with subfolders: atoms/, sources/, entities/, concepts/, threads/
    22|    22|    22|    22|- schema.md rewritten to incorporate two-tier atom/synthesis model, HERMES.md page templates, citation standards, language conventions
    23|    23|    23|    23|- `Meta/glossary.md`, `Meta/open-questions.md`, `Meta/decisions.md` initialized
    24|    24|    24|    24|- All slash commands updated: Drafts/ hard firewall added, ingest split into primary/secondary workflows, lint restructured as LINT_FAIL/WARN/INFO
    25|    25|    25|    25|
    26|    26|    26|    26|## [2026-04-26 11:00] SYSTEM | extract-atoms-from-juan skill saved to ~/.hermes/skills/
    27|    27|    27|    27|
    28|    28|    28|    28|Skill version 0.4. Full workflow: Phases A–F. Covers Zhiliu OCR input format, atom unit rules (one text = one atom), citation conventions, genre heuristics, OCR mitigations, refusals, worked example.
    29|    29|    29|    29|
    30|    30|    30|    30|## [2026-04-26 11:15] INGEST | s-lin-xiyuan-wenji 卷首
    31|    31|    31|    31|
    32|    32|    32|    32|Phase A: Structural reconnaissance complete. 10 sections identified (卷首 + 卷一 through 卷九). Source page created at Wiki/sources/s-lin-xiyuan-wenji.md. Genre: collected_works (文集). 4201 lines, 375 pages. Originally OCR'd from pages 20–394 via Qwen-VL.
    33|    33|    33|    33|
    34|    34|    34|    34|Phase B: 6 atoms extracted from 卷首 (A-20260426-1100 through A-20260426-1105): 5 prefaces (蔡獻臣 1612, 沈德潛 1753, 雷鋐 1753, 陈胪声 1752, 叶在枏 1902) + 1 biography (蔡獻臣). Calibration batch paused at 5 atoms for review; user approved and continued. Key finding: three editions confirmed — Wanli (1612), Qianlong (1752–53), Guangxu (1902).
    35|    35|    35|    35|
    36|    36|    36|    36|## [2026-04-26 12:00] INGEST | s-lin-xiyuan-wenji 卷一
    37|    37|    37|    37|
    38|    38|    38|    38|Phase B: 5 memorials atomized (A-20260426-1130 through A-20260426-1134):
    39|    39|    39|    39|- 新政八要疏 (flagship, ~4900 chars, 8 internal anchors, 嘉靖元年 1522)
    40|    40|    40|    40|- 明職守以白構陷疏 (Tan Lu case, 嘉靖二年 1523)
    41|    41|    41|    41|- 陳情辯理疏 (supplementary, micro-history of Nanjing bureaucratic conflict)
    42|    42|    42|    42|- 荒政從言疏 (classic famine-relief text, ~5200 chars, verbatim pending)
    43|    43|    43|    43|- 陈民便以答明诏疏 (Guangdong reforms, ~4900 chars, verbatim pending)
    44|    44|    44|    44|
    45|    45|    45|    45|Note: 荒政從言疏 and 陈民便以答明诏疏 marked citation_precision: low — full verbatim extraction deferred to subsequent session due to length. Structural paraphrases provided.
    46|    46|    46|    46|
    47|    47|    47|    47|Total atoms: 11. Source page updated.
    48|    48|    48|    48|
    49|    49|    49|## [2026-04-26 13:00] INGEST | s-lin-xiyuan-wenji 卷二
    50|    50|    50|
    51|    51|    51|2 memorials atomized (A-20260426-1200 through A-20260426-1201):
    52|    52|    52|- 到任谢恩疏 (short, 嘉靖十年 1531)
    53|    53|    53|- 王政附言疏 (flagship statecraft document, ~14,000 chars, 21 articles with internal anchors: 守令 through 用人)
    54|    54|    54|Key: 王政附言疏 is Lin's second major reform program after 新政八要, covering local governance, agriculture, taxation, education, judicial reform, military, fiscal policy. Cai Xianchen praised it as "宛然七篇模範" (worthy of Mencius).
    55|    55|    55|
    56|    56|    56|## [2026-04-26 13:30] INGEST | s-lin-xiyuan-wenji 卷三
    57|    57|    57|
    58|    58|    58|10 memorials atomized (A-20260426-1210 through A-20260426-1219), spanning 1529–1539:
    59|    59|    59|- 4 short/ceremonial (賞功謝恩, 荐举人材, 自陈不职, 患病乞归)
    60|    60|    60|- 6 substantive: Liaodong mutiny trilogy (急处叛军, 討叛軍飭武備, 遼東兵變疏), border defense vs. Mongols, Qinzhou 屯田, final Qinzhou summary
    61|    61|    61|Key: Liaodong mutiny memorials document the career turning point — Lin's hawkish stance led to demotion to Qinzhou. Timeline now complete from 1522 (新政八要) through 1539 (Qinzhou departure).
    62|    62|    62|
    63|    63|## [2026-04-26 14:30] INGEST | s-lin-xiyuan-wenji 卷三
    64|    64|
    65|    65|10 memorials atomized (A-20260426-1210 through A-20260426-1219), spanning 1529–1539:
    66|    66|- 4 short/ceremonial; 6 substantive including Liaodong mutiny trilogy
    67|    67|- Career timeline now complete from 1522 新政八要 through 1539 Qinzhou departure
    68|    68|
    69|    69|## [2026-04-26 15:30] INGEST | s-lin-xiyuan-wenji 卷四
    70|    70|
    71|    71|10 memorials atomized (A-20260426-1220 through A-20260426-1229), spanning 1537–1549:
    72|    72|- 7 Annam campaign memorials (the "ten memorials" sequence: A-20260426-1228 confirms 連進十疏)
    73|    73|- 1 屯田 follow-up, 1 post-campaign 谢恩, 1 大學 text revision
    74|    74|- Key: 改正經傳以垂世訓疏 (1549) — Lin's 大學 revision led to formal dismissal (削籍), marking end of political career
    75|    75|- Career arc complete: 1522 reform debut → 1523 demotion → 1531 comeback (王政附言) → 1533 Liaodong mutiny → 1535 Qinzhou → 1537–39 Annam → 1541 dismissal → 1549 final 削籍
    76|    76|
    77|    77|Total atoms: 33 (卷首6 + 卷一5 + 卷二2 + 卷三10 + 卷四10)
    78|    78|Remaining: 卷五–卷九 (letters, public notices, prefaces)
    79|    79|
    80|## [2026-04-26 16:00] INGEST | s-lin-xiyuan-wenji 卷五–卷九
    81|
    82|Final batch: 卷五 (31 letters), 卷六 (5 letters/揭帖), 卷七 (35 prefaces), 卷八 (23 prefaces), 卷九 (30 prefaces).
    83|Total atoms for 上冊: 157 (complete).
    84|
    85|Key highlights:
    86|- 卷五: ⭐ 与张净峰提学书二 (Zhang Yue, anti-Yangming network), 复罗整庵书 (Luo Qinshun), 与霍渭崖书 (Huo Tao patron), 寄谢徐少湖书 (Xu Jie!)
    87|- 卷六: ⭐⭐ 與林國博論格物大學問疑書 (massive gewu debate anti-Yangming text), 莫登庸投降纪事揭帖
    88|- 卷七: ⭐ 《困知記》序 (Luo Qinshun's work), 《南京大理寺志》序
    89|- 卷八: ⭐ 贈張净峰郡守考績序
    90|- 卷九: ⭐ 送張維乔謫官南雍序 (Zhang Yue demotion), 贈陳紫峰南歸序 (Chen Chen), 同年季彭山话别序 (Ji Ben, Yangming disciple)
    91|
    92|## [2026-04-26 17:00] SYSTEM | s-lin-xiyuan-wenji extraction complete
    93|
    94|《同安林次崖先生文集·上册》 fully atomized: 157 atoms across 10 sections (卷首 + 卷一–卷九).
    95|Extraction time: ~6 hours. Source: 375 pages, 4201 lines of Qwen-VL OCR output.
    96|Status: structural_complete. Verbatim extraction pending for ~10 priority atoms.
    97|Next: 下册 (volume 2) if available; or entity page generation from atoms.
    98|
## [2026-04-26 17:30] ENTITY | lin-xiyuan entity page created

Full biographical entity page at Wiki/entities/lin-xiyuan.md.
Sections: names, dates, brief, positions held (24-row table with lunar+Gregorian), networks (同年, Cheng-Zhu, political, Yangming debate), concepts, atoms, open questions, editions.
Sources: 22 key atoms from the 157-atom collection.

## [2026-04-26 17:45] SYNTHESIS | t-lin-xiyuan-takeaways thread created

7-pattern synthesis from 18 key atoms:
1. Cheng-Zhu official as political activist (not passive moralist)
2. Reform→conflict→demotion cycle (4 iterations across 4 decades)
3. Anti-Yangming stance: sophisticated, not knee-jerk; advised against public debate
4. Annam campaign: vindication without reward
5. Qing reception: constructed as Cheng-Zhu hero by Qianlong editors
6. Practical governance: famine relief, salt reform, military colonies
7. Network positioning: central node in Fujian Cheng-Zhu circle
