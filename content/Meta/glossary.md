# Glossary — Name and Term Normalization

Alias tables for names, places, offices, texts, and dates. The single most leveraged plumbing file for the wiki. The agent consults this on every INGEST to resolve encountered forms to canonical slugs. Ambiguous cases not resolvable from this file go to `Meta/open-questions.md`.

---

## People (人名)

Format: `canonical-slug | 字 | 號 | 籍貫 | dates | alias forms`

| Canonical slug | Characters | Pinyin | 字/號 | 籍貫 | Dates (Gregorian approx.) | Known aliases |
|---------------|-----------|--------|------|------|--------------------------|---------------|
| liu-yaohui | 劉堯誨 | Liú Yáohuì | 字藎卿 | 廣西桂林 | 1522–1585 | Liu Yao-hui |
| zhang-juzheng | 張居正 | Zhāng Jūzhèng | 字叔大，號太岳 | 湖廣江陵 | 1525–1582 | Zhang Chu-cheng |
| pang-shangpeng | 龐尚鵬 | Páng Shàngpéng | 字少南，號惺庵 | 廣東南海 | 1524–1581 | Pang Shang-p'eng |
| yu-dayou | 俞大猷 | Yú Dàyóu | 字志輔，號虛江 | 福建泉州晉江 | 1503–1579 | Yu Ta-yu |
| tan-lun | 譚綸 | Tán Lún | 字子理，號二華 | 江西宜黃 | 1520–1577 | Tan Lun |
| lin-feng | 林鳳 | Lín Fèng | — | 廣東潮州 | fl. 1560s–1580s | Limahong (Span.) |
| lin-xiyuan | 林希元 | Lín Xīyuán | 字茂貞，號次崖 | 福建泉州同安 | 1480–1560 | Lin Hsi-yüan |
| qi-jiguang | 戚繼光 | Qī Jìguāng | 字元敬，號南塘 | 山東蓬萊 | 1528–1588 | Ch'i Chi-kuang |
| wang-daokun | 汪道昆 | Wāng Dàokūn | 字伯玉，號南溟 | 徽州歙縣 | 1525–1593 | Wang Tao-k'un |

*Add new entries as entities are created. If two people share a name, append `-(date)` to disambiguate: `lin-feng-pirate` vs `lin-feng-historian`.*

---

## Places (地名)

| Historical name (canonical) | Characters | Modern equivalent (search aid only) |
|----------------------------|-----------|--------------------------------------|
| quanzhou-fu | 泉州府 | Quanzhou, Fujian |
| zhangzhou-fu | 漳州府 | Zhangzhou, Fujian |
| fujian-bu | 福建布政使司 | Fujian Province |
| tongan-xian | 同安縣 | Tong'an, now part of Xiamen |
| jinjiang-xian | 晉江縣 | Jinjiang, Fujian |
| nan-an-xian | 南安縣 | Nan'an, Fujian |
| yuegang | 月港 | Haicheng, Zhangzhou (pirate/trade port) |
| luzon | 呂宋 | Luzon / Manila |

---

## Offices and Titles (官名)

| Term | Characters | Translation | Period |
|------|-----------|-------------|--------|
| xunfu | 巡撫 | Governor; Regional Surveillance Commissioner | Ming |
| zongdu | 總督 | Governor-General | Ming |
| bingbei dao | 兵備道 | Defense Circuit Intendant | Ming |
| zongbing | 總兵 | Regional Military Commissioner | Ming |
| shoufu | 首輔 | Senior Grand Secretary | Ming |
| weisuo | 衛所 | Guard-Station system | Ming |
| lijia | 里甲 | Community-tithing registration system | Ming |
| junyao | 均徭 | Equalized corvée | Ming |

---

## Key Texts (書名)

| Canonical slug | Full title (characters) | Author | Date | Notes |
|---------------|------------------------|--------|------|-------|
| wanli-quanzhou-fuzhi | 萬曆泉州府志 | 陽思謙 修 | 1612 | ⭐⭐ Richest gazetteer; also 乾隆重刻本 |
| zhengde-zhangzhou-fuzhi | 正德漳州府志 | — | 1521 | Yuegang port data |
| xulai-ji | 虛籟集 | 劉堯誨 | fl. 1572–76 | Liu Yaohui's memorials |
| zhengqi-tang-quanji | 正氣堂全集 | 俞大猷 | — | Yu Dayou's collected works |
| ming-shilu | 明實錄 | — | compiled Xuande–Tianqi | Cite: reign + year + month + fascicle |
| da-ming-huidian | 大明會典 | — | 1587 (Wanli ed.) | Institutional reference |

---

## Reign Periods (年號) — Gregorian Conversion

| Reign title | Characters | Emperor | Gregorian |
|-------------|-----------|---------|-----------|
| Jiajing | 嘉靖 | Shizong | 1522–1566 |
| Longqing | 隆慶 | Muzong | 1567–1572 |
| Wanli | 萬曆 | Shenzong | 1573–1620 |
| Tianqi | 天啟 | Xizong | 1621–1627 |
| Chongzhen | 崇禎 | Sizong | 1628–1644 |

*For lunar-to-Gregorian conversion of specific dates, use Zhongyang Yanjiuyuan's online conversion tool and record the result in the atom's `date_gregorian` field.*
