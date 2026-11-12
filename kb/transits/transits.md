# Transits (Gochara) — rules for the engine

Tradition: Parashari, Lahiri, whole-sign. All "house from Moon" counts are whole signs counted inclusively from the natal Moon sign (Janma rashi). Read every transit under three locks: (1) natal promise, (2) running dasha, (3) transit. A transit cannot deliver what the chart and dasha do not promise.

Source tags used below:
- **[PD26]** Phaladeepika ch. 26, verses 26-30 read at https://www.siva.sh/phaladeepika/26/26-30
- **[Sastri]** Dr. P.S. Sastri, "Transit Influences", Astrological Magazine Dec 1977, read at https://saptarishisastrology.com/?p=1170
- **[JSD44]** "Gochara Phala Adhyaya" summary read at https://theeyeofvedas.blogspot.com/2025/11/chapter-44-gochara-phala-adhyaya.html (secondary)
- **[OJ102]** https://www.onlinejyotish.com/free-astrology/astrology-lessons/lesson_102.php (secondary)
- **[JH-G]** https://jagannathhora.com/gochara/ ; **[JH-SS]** https://jagannathhora.com/sade-sati-effects-all-moon-signs/ (secondary, modern)
- **[DP]** https://dekhopanchang.com/en/learn/gochar (secondary, modern)
- **[BPHS]** English e-text at https://sanskritdocuments.org/brihatparashara (Sanskrit root text; English reading not yet re-verified) (ch. 66-72 Ashtakavarga)
- **[PVR]** P.V.R. Narasimha Rao, "Two transit principles" https://www.vedicastrologer.org/articles/pp_transits.pdf
- **[WK]** written from working knowledge of the named text; not re-read this session

---

## 1. Favourable houses from the natal Moon (base table)

| Planet | Good houses from Moon | Time per sign (approx.) | Source |
|---|---|---|---|
| Sun | 3, 6, 10, 11 | 1 month | [OJ102], [Sastri] |
| Moon | 1, 3, 6, 7, 10, 11 | 2.25 days | [OJ102], [Sastri] |
| Mars | 3, 6, 11 | ~45 days (longer when retrograde) | [OJ102], [Sastri] |
| Mercury | 2, 4, 6, 8, 10, 11 | ~1 month | [JSD44]; [Sastri] prints 2, 4, 6, 7, 10, 11 (variant/garbled) |
| Jupiter | 2, 5, 7, 9, 11 | ~1 year | [OJ102], [JH-G] |
| Venus | 1, 2, 3, 4, 5, 8, 9, 11, 12 (bad in 6, 7, 10) | ~1 month | [JSD44], [Sastri] |
| Saturn | 3, 6, 11 | ~2.5 years | [OJ102], [JH-G] |
| Rahu | 3, 6, 11 (some add 10) | ~18 months, always retrograde in mean motion | [OJ102]; [Sastri] gives 3, 6, 10, 11 |
| Ketu | 3, 6, 11 (some add 10) | ~18 months | same |

Rule: `good = house_from_moon(transit_planet) in table[planet]`; all planets are good in the 11th. Nodes are not in the classical gochara verses; "like Mars/Saturn" is convention.

## 2. Vedha (obstruction) tables

**Rule.** A planet in a favourable house F gives its good result only if no other planet is at the same time in the paired vedha house V (both counted from natal Moon). The reverse (*vipareeta vedha*) is also taught: a planet in a bad house V has its bad result blocked when another planet occupies the paired good house F. [WK for the reverse form; the forward form per Sastri]

| Planet | Favourable → Vedha house |
|---|---|
| Sun | 3→9, 6→12, 10→4, 11→5 |
| Moon | 1→5, 3→9, 6→12, 7→2, 10→4, 11→8 |
| Mars | 3→12, 6→9, 11→5 |
| Mercury | 2→5, 4→3, 6→9, 8→1, 10→8, 11→12 |
| Jupiter | 2→12, 5→4, 7→3, 9→10, 11→8 |
| Venus | 1→8, 2→7, 3→1, 4→10, 5→9, 8→5, 9→11, 11→3, 12→6 |
| Saturn | 3→12, 6→9, 11→5 |
| Rahu/Ketu | usually left outside the scheme; if used, as Saturn |

Source: [Sastri] for all rows (his Saturn row is misprinted on the page as "9→9"; 6→9 is the standard value and matches [JH-G]). Jupiter and Saturn rows independently confirmed by [JH-G].

**Disagreement to flag:** for Venus many circulated tables give 11→6 and 12→3; Sastri (pair list and his sign grid agree with each other) gives 11→3 and 12→6. Engine: use Sastri's, expose a switch.

**Exceptions (no mutual vedha):** Sun and Saturn do not obstruct each other; Moon and Mercury do not obstruct each other (father-son pairs). [Sastri], [JSD44], [JH-G]. Sastri words it one-directionally and adds Sun does not obstruct Mars; the two-pair rule is the common form.

**Other vedha notes**
- The obstruction holds only while the obstructing planet is actually in the vedha house. [JH-G]
- A planet giving good results but aspected by a malefic, or a planet giving bad results but aspected by a benefic, becomes ineffective; both lose effect when aspected by their enemies. [PD26 v.30]
- Use vedha as a refinement, not a primary verdict. [JH-G]

## 3. Saturn: Sade Sati, Ashtama, Ardhashtama, Kantaka

| Name | Condition | Classical/usual result | Source |
|---|---|---|---|
| Sade Sati phase 1 (rising) | Saturn in house 12 from Moon | expenses, poor sleep, displacement, eyes/feet, pressure through distant matters | [DP], [JH-SS] |
| Sade Sati phase 2 (peak) | Saturn in house 1 from Moon (Janma Shani) | mind and body under load, identity/career restructure; sharpest within ±3°20' of natal Moon and while in the Moon's own nakshatra | [DP], [JH-SS] |
| Sade Sati phase 3 (setting) | Saturn in house 2 from Moon | family and money restructured, speech, food; easing | [DP], [JH-SS] |
| Ardhashtama / Dhaiya (4th) | Saturn in house 4 from Moon | loss of ease at home, mother, property, relocation | [JH-G], [JSD44] |
| Ashtama Shani / Dhaiya (8th) | Saturn in house 8 from Moon | fear, illness, obstruction, humiliation; often judged harder than Sade Sati for health | [JH-G], [JSD44] |
| Kantaka Shani ("thorn") | Saturn in house 4, 7 or 10 from Moon (some lists: 1, 4, 7, 10; some also count from Lagna) | hindrance in work, spouse/partnership strain, travel, fatigue | [WK] — term is from South Indian practice; not in the pages read |
| Good Saturn | Saturn in 3, 6, 11 from Moon | courage, victory over opponents, gains | §1 |

Arithmetic: `sade_sati = house_from_moon(Saturn) in {12,1,2}`; each sign ≈ 2.5 years, whole period ≈ 7.5 years, repeating every ≈ 29.5 years (typically 2-3 times in a life). Retrograde re-entries split phases; compute by actual ingress dates.

### 3a. Which charts suffer less (modifiers)
| Modifier | Condition | Effect | Source |
|---|---|---|---|
| Saturn as yogakaraka | Lagna = Taurus or Libra | Sade Sati tends to restructure and elevate rather than break | [JH-SS] |
| Saturn as lagna lord | Lagna = Capricorn or Aquarius | Saturn protects the body/self; pressure is workload | [WK] standard functional-nature rule |
| Saturn functional malefic | Lagna = Cancer or Leo (7th/8th and 6th/7th lord) | harsher on marriage, health, opponents | [JH-SS] |
| Moon sign friendly to Saturn | Moon in Taurus, Libra, Capricorn, Aquarius (also Gemini, Virgo) | milder: Saturn is in own/exalted/friendly sign during the peak or neighbouring phase | [JH-SS] |
| Moon weak | Moon in Scorpio (debilitated), or with Rahu/Ketu, or dark Moon | harsher | [JH-SS] |
| Moon in fire/enemy signs | Aries (Saturn debilitated at peak), Cancer, Leo | harsher peak | [JH-SS] |
| Natal Saturn strong | natal Saturn own/exalted, or well placed from Lagna | milder | [JH-SS] |
| Ashtakavarga | Saturn's own bindus in the transited sign ≥ 4 and SAV ≥ 28 | that 2.5-year phase is workable; ≤ 2 bindus = heavy | [JH-G], [DP], [BPHS ch. 72] |
| Dasha | running dasha lord a functional benefic and unconnected to Saturn/8th/12th | transit stays in the background | [JH-SS]; K.N. Rao's well-known position that Sade Sati must be read through dasha and ashtakavarga [WK] |
| Moorti | Saturn's ingress moorti is gold/silver (see §7) | that sign's transit turns favourable | [JSD44] |

Per-Moon-sign severity as printed by [JH-SS] (modern opinion, not classical): very high Scorpio; high Leo, Sagittarius; moderate-high Aries, Cancer, Pisces; moderate Taurus, Gemini, Virgo, Capricorn, Aquarius; low-moderate Libra.

Per-Moon-sign phase table (computable): for Moon sign M, phase 1 = Saturn in M-1, phase 2 = Saturn in M, phase 3 = Saturn in M+1. Saturn's dignity in each of those signs (own: Capricorn, Aquarius; exalted: Libra; debilitated: Aries; friendly: Taurus, Gemini, Virgo; inimical: Cancer, Leo, Scorpio; neutral: Sagittarius, Pisces) grades each phase.

## 4. Jupiter transit by house from Moon

| House from Moon | Result (paraphrase of the standard gochara verses) | Good? |
|---|---|---|
| 1 | change of place, expenses, loss of standing, mental strain | no |
| 2 | wealth, family happiness, effective speech | yes |
| 3 | obstacles, loss of position, friction with associates | no |
| 4 | trouble through relatives, no peace at home | no |
| 5 | children, intelligence, good counsel, gains | yes |
| 6 | worry from opponents/illness despite effort | no |
| 7 | marriage, partnership, pleasant travel, comforts | yes |
| 8 | fatigue, illness, sorrow, wearisome journeys | no |
| 9 | fortune, success, guidance, dharma | yes |
| 10 | pressure on position, heavy work, risk to status | no |
| 11 | gains, recovery of position, honours | yes |
| 12 | expenses (often on good causes), distance, grief | no |

Source: good/bad pattern [OJ102], [JH-G]; per-house phrases [JSD44], [DP] plus [WK] of Phaladeepika ch. 26 / Brihat Samhita ch. 104 for houses those pages leave blank (1, 6). Vedha: §2.

## 5. Saturn transit by house from Moon
1 illness, grief (Janma Shani) · 2 loss of money and family ease · 3 gains, position, courage · 4 loss of comfort, relatives, home · 5 worry over children, clouded judgment · 6 victory over enemies and disease · 7 travel, spouse strain, wandering · 8 suffering, fear, ill-health (Ashtama) · 9 obstruction to fortune, father, dharma · 10 new/heavy work, risk to standing · 11 gains of all kinds · 12 expenses, fatigue (start of Sade Sati). Sources: [JSD44] for 1-4, 6, 8, 11, 12; others [WK].

## 6. Rahu / Ketu transit
| Rule | Condition | Result | Source |
|---|---|---|---|
| Good houses | node in 3, 6, 11 (some: 10) from Moon | courage, win over opponents, gains | §1 |
| Bad houses | Rahu or Ketu in 1, 5, 7, 8, 9, 12 from Moon | confusion, fear, scandal (7), accident risk (8, 12) | [JSD44] |
| Axis on 1/7 | Rahu-Ketu on Moon/Lagna and 7th | identity and relationship reshaped for ~18 months | [DP] |
| Over natal planets | node within ~5° of a natal planet | amplifies (Rahu) or strips/detaches (Ketu) that planet's matters; eclipse-like if on Sun/Moon | [WK] |
| Ashtakavarga | nodes have no own ashtakavarga | read via SAV of the sign occupied | [JH-G] |
| Nodal return | Rahu returns to natal sign every ~18.6 years; reversal (Rahu on natal Ketu) at ~9.3, 27.9, 46.5 | turning points in direction/ambition | arithmetic; interpretation modern |

Note: use one convention (mean or true node) consistently; ingress dates differ by weeks.

## 7. Moorti Nirnaya (gold / silver / copper / iron)

**Condition.** At the exact moment a planet enters a new sign, find the transit Moon's sign and count it from the native's natal Moon sign.

| Moon at ingress, counted from natal Moon | Moorti | Result |
|---|---|---|
| 1, 6, 11 | Swarna (gold) | excellent; even an otherwise bad transit turns good |
| 2, 5, 9 | Rajata (silver) | very good; honour |
| 3, 7, 10 | Tamra (copper) | middling, mixed |
| 4, 8, 12 | Loha (iron) | poor; setbacks even from a "good" house |

Source: mapping from [JSD44]; the four categories also in [OJ102] (which does not give the mapping). Used mainly for Saturn, Jupiter and the nodes. Disagreement: this is a muhurta/panchanga-practice device (not in BPHS); the page claims it can override the house-from-Moon verdict — treat as a modifier of ±1 grade, not an override.

## 8. Double transit (K.N. Rao)

**Rule as used in practice.** For an event of house H to happen:
1. Transit Jupiter AND transit Saturn must both influence house H **and/or the lord of H**, where influence = occupying that sign or aspecting it (Jupiter: 5th, 7th, 9th; Saturn: 3rd, 7th, 10th);
2. counted from Lagna, and confirmed from the Moon;
3. within a dasha/antardasha that promises the same event;
4. a retrograde planet is treated as also influencing from the previous sign;
5. the faster triggers (Mars, Sun, Moon) then fix month and day.

Typical uses: marriage → 7th house/7th lord (also Lagna/Lagna lord, 2nd, 11th); childbirth → 5th and 9th houses/lords; career rise → 10th house/lord.

Source: the one-sentence form ("both Jupiter and Saturn must simultaneously aspect the relevant house" plus dasha support) is on [DP], unattributed. Points 2, 4, 5 and the attribution to K.N. Rao are [WK]; Rao's own text could not be opened this session (the Scribd copy returned no body text). Treat the retrograde clause as unverified.

**Complementary precision method [PVR]:** events cluster within about two months of (a) Jupiter or Saturn turning stationary within 3° of a sensitive natal point (by conjunction or aspect, in the relevant divisional chart), or (b) two transit planets forming an exact 0°/120°/180°/240° while the slower one touches a key natal point.

## 9. Transit over natal planets and houses
| Rule | Condition | Result | Source |
|---|---|---|---|
| Benefic over natal point | Jupiter conjunct or aspecting a natal planet/house lord | that planet's promise is switched on | [WK] |
| Malefic over natal point | Saturn/Mars/Rahu/Ketu conjunct or aspecting a natal planet | pressure, delay or separation in that planet's matters; constructive if the natal planet is strong | [WK] |
| From Lagna as well | repeat house counts from Lagna | events of the world show from Lagna; state of mind from Moon | [WK]; K.N. Rao school uses both |
| Dasha lord's transit | the running dasha/antardasha lord transiting a kendra/trikona from its natal place or from Lagna, in good dignity | period improves; in 6/8/12 or debilitated: dip | [WK] |
| Dasha + transit both bad | unfavourable dasha and unfavourable gochara together | the hardest stretch | https://blog.indianastrologysoftware.com/?p=210 |
| Orb | sign-level by classical rule; tighter (±3°) for timing | | [PVR] |

## 10. Nakshatra-based transit: Tara bala (Navatara)

`tara = ((N_transit − N_birth) mod 9) + 1`, with stars numbered 1-27.

| Tara | Name | Stars from birth star | Result |
|---|---|---|---|
| 1 | Janma | 1, 10, 19 | mixed; body/mind sensitive, avoid risky starts |
| 2 | Sampat | 2, 11, 20 | wealth, good |
| 3 | Vipat | 3, 12, 21 | danger, loss — avoid |
| 4 | Kshema | 4, 13, 22 | well-being, good |
| 5 | Pratyari | 5, 14, 23 | obstacles, opponents — avoid |
| 6 | Sadhaka | 6, 15, 24 | accomplishment, good |
| 7 | Naidhana (Vadha) | 7, 16, 25 | severe; avoid |
| 8 | Mitra | 8, 17, 26 | friendly, good |
| 9 | Parama Mitra | 9, 18, 27 | very friendly, good |

Use: daily Moon for muhurta; slow planets' star position for period quality; dasha lord's tara from the birth star as a quick benefic/malefic test. Source: muhurta tradition [WK]. Supporting classical verse: malefic transit on the 1st, 3rd, 5th, 7th, 10th, 19th, 23rd stars from the birth star endangers; benefic there only fails ventures [PD26 v.28]; the Sun or a malefic on the birth star (janma), 10th (karma) and 19th (adhana) is singled out [PD26 v.26-27]; these become critical on sankranti, eclipse or planetary-war days [PD26 v.29].

**Latta (kick) [Sastri citing PD 26.42-47]:** forward: 12th star from the Sun, 3rd from Mars, 6th from Jupiter, 8th from Saturn; backward: 5th from Venus, 7th from Mercury, 9th from Rahu, 22nd from the Moon. If the birth star is the latta star of a transiting planet → ill-health/sorrow for that time.

## 11. Returns and typical ages
| Cycle | Period | Ages | Reading |
|---|---|---|---|
| Jupiter return | 11.86 y | ~12, 24, 36, 48, 60, 72 | renewal of the natal Jupiter's promise; judged by natal Jupiter's house/dignity |
| Jupiter opposite natal | | ~6, 18, 30, 42, 54 | aspecting natal Jupiter: expansion via others |
| Saturn return | 29.46 y | ~29-30, 58-59, 88 | maturity checkpoints; restructuring of the natal Saturn's house |
| Saturn opposite / square natal | | ~14-15, 44; ~7, 22, 37, 51 | pressure points (squares are a Western notion; Parashari uses Saturn's 3/7/10 aspect back to natal Saturn at ~7.4, 14.7, 22 y offsets) |
| Sade Sati | every ~29.5 y | depends on Moon | §3 |
| Rahu/Ketu return | 18.6 y | ~18-19, 37, 56, 74 | nodal themes restart |
| Nodal reversal | | ~9, 28, 46-47, 65 | Rahu over natal Ketu |
| Jupiter-Saturn both back | | ~59-60 | Shashtiabdapurti age; both return near natal places |

Arithmetic is exact; the readings are modern synthesis [WK]. Ages are approximate because of retrogression; compute actual dates.

## 12. Eclipses
| Rule | Condition | Result | Source |
|---|---|---|---|
| Eclipse on natal point | solar/lunar eclipse within ~5° (same nakshatra) of natal Sun, Moon, Lagna degree or dasha lord | health/mind/status sensitive for weeks to ~6 months; matters of that house stirred | [WK] Brihat Samhita tradition; modern orbs |
| Eclipse in birth star | eclipse falls in Janma nakshatra (or the 10th/19th) | advised: rest, no major starts, japa/daan | [PD26 v.29] names eclipse days falling on the janma-group stars as dangerous |
| House of eclipse | eclipse sign counted from Moon/Lagna | 3, 6, 10, 11 comparatively harmless; 1, 4, 7, 8, 12 sensitive | [WK] |
| Birth in eclipse | born during an eclipse | birth dosha with shanti | [BPHS ch. 91] |
| Muhurta | 3 days before / after an eclipse avoided for auspicious starts (practice varies: 1-7 days) | | [WK] |

## 13. Ashtakavarga-qualified transit
| Rule | Condition | Result | Source |
|---|---|---|---|
| Planet's own bindus (BAV) | bindus of the transiting planet in the sign it transits: 0-2 very weak, 3 below average, 4 average-good, 5-8 good-excellent | the transit result is scaled by this, even overriding the house-from-Moon verdict at the extremes | [DP]; [JH-G] (Saturn with 5-6 behaves decently in a hard house; with 1-2 underdelivers in a good one) |
| Sarvashtakavarga (SAV) | total bindus in the sign: > 30 favourable, 25-30 medium, < 25 adverse (popular single cut-off: 28 = 337/12) | quality of any transit through that sign | [BPHS ch. 72 vv.3-5]; 28 threshold [JH-G], [DP] |
| Kakshya (1/8-sign sub-division) | each sign = 8 kakshyas of 3°45' ruled in order by Saturn, Jupiter, Mars, Sun, Venus, Mercury, Moon, Lagna; good while the transiting planet is in a kakshya whose lord contributed a bindu in that sign | fine timing inside a sign | [WK] standard ashtakavarga practice |
| Saturn's danger star | (Saturn BAV bindus × shodhya pinda) ÷ 27 → remainder nakshatra; Saturn transiting it (or its trines) harms the house concerned | timing of grief | [BPHS ch. 70 vv.1-6] |
| Muhurta check | before any function check the sign's ashtakavarga; avoid Sun in a sign with few bindus | | [BPHS ch. 70 vv.19-20, ch. 72 vv.30-31] |
| Totals | each planet 0-8 per sign; grand total 337 | sanity check for code | [JH-G] |

Terminology trap: some editions call the benefic marks *rekha* and the malefic marks *bindu* (the BPHS e-text does this); modern usage is the opposite. In this KB "bindu" = benefic point.

## 14. Order of operations for the engine
1. Dasha/antardasha lords and what they promise.
2. Saturn, Jupiter, Rahu, Ketu: house from Moon and from Lagna → base verdict (§1, §3-6).
3. Vedha check (§2).
4. Ashtakavarga scaling (§13).
5. Moorti at ingress (§7) — ±1 grade.
6. Double transit for the event house (§8).
7. Conjunction/aspect to natal planets, with degrees (§9); tara of the transiting star (§10).
8. Eclipses near natal points (§12).
Output each step separately so a human can see why the verdict moved.

## Reliability notes
- **Classical consensus:** favourable houses from the Moon for the seven planets; the vedha principle and the two father-son exceptions; janma/karma/adhana star sensitivity (Phaladeepika 26.26-30, read); Ashtakavarga thresholds and Saturn's danger-star method (BPHS 70, 72, read); birth-in-eclipse dosha (BPHS 91, read); Latta (via Sastri citing Phaladeepika 26.42-47).
- **Classical, but table details differ between editions:** Venus's last two vedha pairs; Mercury's good houses as printed by Sastri; whether nodes have gochara/vedha rules at all.
- **Traditional practice outside the big Parashari texts:** Moorti Nirnaya, Tara bala as used for transits, Kantaka Shani, the words "Sade Sati" and "Dhaiya" themselves (the classical verses only give Saturn's results in the 12th, 1st, 2nd, 4th, 8th).
- **Modern method (20th century):** K.N. Rao's double transit; P.V.R. Narasimha Rao's stationary and mutual-trine transit principles (read); reading Sade Sati through lagna lordship and ashtakavarga.
- **Modern internet lore:** per-Moon-sign "severity rankings" of Sade Sati; fixed claims such as "Kaal Sarp ends at 47"; planetary "return" psychology borrowed from Western astrology.
- **Not sourced this session:** K.N. Rao's own statement of double transit (incl. the retrograde clause); a primary text for Moorti Nirnaya; a primary definition of Kantaka Shani; Phaladeepika 26 verses 1-25 (full per-house results for all planets) — the page available covered only vv. 26-30, so several per-house phrases for Jupiter/Saturn are from working knowledge and marked [WK].
