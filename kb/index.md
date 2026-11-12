# Jyotish Knowledge Base — Master Index

Tradition: Parashari (BPHS) as the base. Where Jaimini, KP, or regional (Tamil / Bengali / Kerala) practice differs, it is flagged inline. Ayanamsa: Lahiri. Houses: whole sign.

## Reading protocol (how the agent must read any chart)
1. **Lagna** — sign, degree, lord placement/dignity, planets in 1st, aspects on 1st. This is the body, the self, the overall strength.
2. **Moon** — sign, nakshatra, waxing/waning, dignity, planets with/aspecting. Mind, mother, public life. All *gochar* (transit) and dasha timing is Moon-referenced.
3. **Sun** — dignity, house. Soul, father, authority.
4. **Bhava by bhava** — for each house: (a) sign, (b) lord's placement + dignity + house it sits in, (c) occupants, (d) aspects, (e) karaka's condition. Never judge a house from one factor.
5. **Yogas** — scan for Raja, Dhana, Pancha Mahapurusha, Gaja Kesari, Neecha Bhanga, Viparita Raja, Kemadruma, Kaal Sarp, etc. Note *strength* (Shadbala / dignity) — a yoga formed by weak planets gives little.
6. **Doshas** — Mangal, Kaal Sarp, Pitru, Shani-related, Grahan.
7. **Vargas** — confirm D1 findings in D9 (marriage, inner strength; vargottama), D10 (career), D7 (children), D2 (wealth), D12 (parents), D60 (past karma, used only if birth time is precise to the minute).
8. **Dasha** — Vimshottari maha/antar/pratyantar. Judge dasha lord by: house it owns, house it sits in, dignity, yogas it participates in, its relation to lagna lord. Ashtottari / Yogini as cross-check where tradition demands.
9. **Gochar** — current Saturn (Sade Sati / Dhaiya), Jupiter, Rahu-Ketu from Moon and Lagna. Ashtakavarga bindus for the transiting sign.
10. **Synthesis** — repeated signals win. One indication = possibility; three = probability. Say what is *strong*, what is *weak*, what is *uncertain because the birth time is uncertain*.

## Working order for any chart (v2, 11 Nov 2026)
1. `readings/kundli-intake.md` — run the worksheet, cross-check, read time sensitivity, verify.
2. `dashas/antar-event-rules.md` — the in-house calibration rules (Rules 1–10). They outrank any single classical rule.
3. The life-area rule file for the question asked, checked line by line against the worksheet.
4. `readings/full-reading-protocol.md` — the form of the written reading.

## Files
| File | Contents |
|---|---|
| `readings/kundli-intake.md` | Document and birth-data processing, step by step |
| `readings/full-reading-protocol.md` | 13-part reading form |
| `dashas/antar-event-rules.md` | Project calibration rules from verified charts |
| `dashas/dasha-systems.md` | Vimshottari judging rules, Yogini, Ashtottari, Chara dasha (K.N. Rao method), conditional dashas |
| `life-areas/marriage-spouse.md` | Promise, delay, spouse description, plurality, timing, Mangal dosha with sourced cancellations and base rates |
| `life-areas/children.md` | Promise, delay, timing, Beeja/Kshetra sphuta, Santana tithi, curses and remedies |
| `life-areas/career-business.md` | 10th house, Karmajiva, D10, Amatyakaraka, A10, service vs business, foreign, timing |
| `life-areas/wealth.md` | Dhana and daridra yogas, Arudha Lagna, Indu Lagna, Hora, SAV rules |
| `life-areas/health-longevity.md` | Disease by planet and house, D30, balarishta, marakas, longevity methods; no diagnosis, no death prediction |
| `life-areas/family-members.md` | Derived houses for every relative, siblings, parents, D3/D12 |
| `foundations/strength-systems.md` | Shadbala, Bhava bala, Vimshopaka, avasthas, combustion, war, gandanta, pushkara, mrityu bhaga |
| `foundations/ashtakavarga.md` | Tables (Parashara and Varahamihira variants), reductions, Shodhya pinda, kakshya, transit use |
| `foundations/rectification-and-panchanga.md` | Which rectification methods discriminate and which only look precise; panchanga formulas |
| `kp/kp-system.md` | KP ayanamsa, cusps, sub-lords, significators, cuspal rules. Engine computes sub-lords for planets and the four angles only; intermediate Placidus cusps are not computed yet |
| `yogas/yogas-catalogue.md`, `yogas/yogas.json` | 160 yogas: condition, strength, cancellation, result, source |
| `transits/transits.md` | Sade Sati by phase, Saturn and Jupiter from Moon, vedha, double transit, Rahu-Ketu, Ashtakavarga scoring |
| `nakshatras/nakshatras-27.md` | The 27 nakshatras with padas |
| `planets/planets-in-houses.md` | Each planet in each house, lordship notes |
| `sources/bphs-verse-readings.md` | Parashara read in the Sanskrit: verse-by-verse readings and the rule corrections they caused |
| `remedies/remedies.md` | Remedies by planet with cautions |
| `rashis/functional-nature.md`, `bhavas/lord-placements.md`, `matching/match-protocol.md` | Earlier files, still current |

## Sources
Only free, openly readable material is used; see `SOURCES.md` for the policy and the audit of every source cited.

## How to read the rule files
- Each rule has an ID, a checkable condition, a result and the source that was actually opened in November 2026.
- `[UNSOURCED]` or "unsourced – common practice" means widely taught but not traced to a text. `[MEMORY]` or `[MEM-…]` means attributed to a book that could not be opened online (B.V. Raman, K.N. Rao, the KP Readers, K.S. Charak, Uttara Kalamrita). Treat both as lower confidence.
- No controlled study supporting any of these rules was found. Narlikar et al. (2009): 27 astrologers averaged 17.25 correct of 40 against 20 expected by chance. The project's own record is in `readings/kundli-intake.md`.
- Classical outcome wording ("wife dies", "childless") is read as trouble in that area, never stated literally.

## Sources the KB is built from
Brihat Parashara Hora Shastra (BPHS), Phaladeepika, Saravali, Jataka Parijata, Brihat Jataka, Uttara Kalamrita, Hora Ratna, Jaimini Sutras; B.V. Raman (300 Combinations, How to Judge a Horoscope), K.N. Rao (Predicting through Jaimini, Sade Sati), Sanjay Rath, KP Reader series (Krishnamurti). Muhurta: Muhurta Chintamani. Matching: standard North Indian Ashtakoota tables and South Indian Dashakoota.


## Source texts read in the Sanskrit (12 Nov 2026)
| File | What it holds |
|---|---|
| `sources/ANALYSIS.md` | **Read first.** The two texts taken as a whole: the shared method, where they differ, popular rules that are not in them, what was corrected, what our own cases can and cannot show |
| `sources/bphs/` | Brihat Parashara Hora Shastra, all 97 chapters, verse by verse, with engine checks |
| `sources/phaladeepika/` | Phaladeepika, 20 of 28 chapters in full, with the citation check |
| `SOURCES.md` | Source policy and audit: free and public-domain material only |
