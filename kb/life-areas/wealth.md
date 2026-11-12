# Wealth, Gains, Debt and Property — KB rules

Tradition: Parashari base (BPHS), Lahiri ayanamsa, whole-sign houses. Houses counted from Lagna unless stated.

## 0. Verified rules - these win over anything below that differs
*(Moved to the top on 12 Nov 2026. Each rule below was read in the Sanskrit. Where an older numbered rule further down says something different, the older rule is the one in doubt.)*

### Rules confirmed in the Sanskrit (read 12 Nov 2026; `kb/sources/bphs/ch41-45.md`, `ch71-80.md`, `kb/sources/phaladeepika/`)
- **SRC-W1** The lords of the 9th and 5th give wealth, and so do the planets joined with them, in their own periods (BPHS 41.16). The two tables of BPHS 41.2-15 (5th house with the 11th; lagna in a planet's own sign) are in the engine as `dhana_5_11` and `dhana_lagna_own`.
- **SRC-W2** 2nd lord in a chief house with benefics in the 2nd: family wealth and foresight (PD 16.5). A strong 2nd lord's period: family established, money by speech and livelihood; a weak one's: spending, unsettled family (PD 20.3, 20.15).
- **SRC-W3** Poverty combinations are narrow and always involve the lagna lord in the 6th, 8th or 12th with a maraka's aspect, or the lords of the 5th and 9th in the 6th and 12th (BPHS 42.2-7). "Dhana yoga present" fires in most charts and is never offered as a distinction; a poverty combination is stated only as "care with money", with its verse.
- **SRC-W4** Harsha, Sarala, Vimala - the lords of the 6th, 8th and 12th in the 6th, 8th or 12th - give comfort, firmness and saving (PD 6.63, 65, 69). Vimala in particular: "spends little, saves much".
- **SRC-W5** Rays (BPHS 73): a scale of means "according to the family's standing"; remarked on only above 30 or below 12.
- **SRC-W6** Ashtakavarga house comparisons as in career rule SRC-C8; the three-part table for which third of life carries the most (BPHS 72.9-10).
- **SRC-W7** Gain and loss by house through the 11th and 12th lords (PD 16.29-30).

- **SRC-W8** All benefics in upachaya houses (3, 6, 10, 11) from the lagna - very wealthy; from the Moon - wealthy; two of them - middling (Brihat Jataka 13.9; BPHS 37.6). About 8% of charts.
- **SRC-W9** Parashara's remaining poverty combinations (42.8-11, 13-15) are now tested by the engine and printed in worksheet section 8b with how common each is. Two of them are so common they say nothing alone: 'joined with a 6th, 8th or 12th lord and unaspected by a trine lord' (68% of charts - a note for that planet's own period only) and 'lord of the Moon's navamsa with a maraka' (32%).
- **SRC-W10** Rays (BPHS 73), the twenty-point strength of the 2nd and 11th lords (BPHS 7.17-27) and argala on the 2nd and 11th houses (BPHS 31.13-16: 'argala on the 2nd - wealth and grain; on the 11th - gains') are the three strength lines to read for means; each only at its extremes.

## Source keys (URL actually read)

| Key | Source | URL |
|---|---|---|
| BPHS-n | Brihat Parashara Hora Shastra ch. n (chapter numbers match Santhanam; verse numbers are this site's) | https://enjoylearningsanskrit.com/scriptures/parashara/chapter-n (n = 7, 13, 15, 17, 20, 22, 24, 29, 39, 41, 42) |
| PD-6 | Phaladeepika ch. 6 (yogas), V. Subrahmanya Sastri ed. 1950 (OCR text) | https://www.wisdomlib.org/uploads/ocr/essays/phaladeepika/phaladeepika-2nd-ed-1950-by-v-subrahmanya-sastri-text.pdf |
| WP-Dhana | Wikipedia "Dhana yoga" (quotes BPHS, Mansagari, Bhrigu Samhita, Jataka Tattva, Raman) | https://en.wikipedia.org/wiki/Dhana_yoga |
| PVR | P.V.R. Narasimha Rao, *Vedic Astrology: An Integrated Approach* | https://www.vedicastrologer.org/articles/vedic_astro_textbook.pdf |
| INDU | Astrobix, "Analysis of Indu Lagna" | https://astrobix.com/learn/436-analysis-of-indu-lagna.html |
| D2-P | B. Pijan Lama, D-2 Hora page (quotes BPHS ch. 6 v.5–6) | https://barbarapijan.com/bpa/Varga/D2_Hora.htm |
| AV | Slideshare "Use of Ashtakavarga as a predictive technique" (cites BPHS ch. 66, 71, 72) | https://www.slideshare.net/slideshow/the-use-of-asthakavarga-as-a-predictive-technique/25369219 |
| DT-L | Light on Vedic Astrology, double transit | https://www.lightonvedicastrology.com/blog/the-double-transit-effect-of-jupiter-and-saturn |

---

## 1. Order of analysis (agent procedure)

1. 2nd and 11th houses and lords; links between lords of 1, 2, 5, 9, 11 — WLT-01..12.
2. Lagna-specific BPHS yogas — WLT-13..26.
3. Named yogas (Lakshmi etc.) and poverty yogas — WLT-27..47.
4. Arudha Lagna (11th/12th/2nd/7th from AL), Hora Lagna, Indu Lagna, D2 — WLT-48..62.
5. Ashtakavarga check — WLT-63..66.
6. Debt, loss, inheritance, property, vehicles, speculation — WLT-67..82.
7. Timing — WLT-83..88.

---

## 2. General rules: 2nd, 11th and the 1-2-5-9-11 links

| ID | Condition (checkable) | Result | Source | Notes |
|---|---|---|---|---|
| WLT-01 | 2nd lord in the 2nd, or in a kendra or trikona | Wealth | BPHS-13 v.1 | |
| WLT-02 | 2nd lord (or a wealth-giving planet) in 6th, 8th or 12th | Loss of wealth | BPHS-13 v.2 | |
| WLT-03 | Natural benefic in 2nd → gives wealth; natural malefic in 2nd → destroys it | | BPHS-13 v.2 | Exception: see WLT-46 (Mars + Saturn in 2nd aspected by Mercury) |
| WLT-04 | Jupiter is the 2nd lord and sits in the 2nd, or Jupiter in 2nd, or 2nd lord conjunct Mars | Wealthy | BPHS-13 v.3; WP-Dhana ("Jupiter with Mars in the 2nd gives much wealth") | |
| WLT-05 | 2nd lord in 11th, or 11th lord in 2nd, or both in kendra/trikona | Wealthy | BPHS-13 v.4 | Core rule |
| WLT-06 | 2nd lord in a kendra, 11th lord in a trikona, both joined/aspected by Jupiter and Venus | Financial gain | BPHS-13 v.5 | |
| WLT-07 | 2nd lord in own sign or exaltation | Helper of people, renowned | BPHS-13 v.10 | |
| WLT-08 | 11th lord in the 11th, in a kendra/trikona, or exalted | Large gains | BPHS-22 v.2 | |
| WLT-09 | 11th lord in 2nd AND 2nd lord in a kendra AND Jupiter linked to the 2nd | Major gain | BPHS-22 v.3 | |
| WLT-10 | 2nd lord in 11th AND 11th lord in 2nd (exchange) | Great fortune after marriage | BPHS-22 v.9 | |
| WLT-11 | Lagna lord and 2nd lord linked (conjunction, mutual aspect, exchange) with 5th, 9th or 11th lord; or 2nd lord with 5th/9th/11th lord; or 5th with 9th/11th; or 9th with 11th | Dhana yoga | WP-Dhana (general formation; no verse given); PVR §11.9 (5th and 9th lords and planets joining them give money in their dashas; 11th should be strong) | The standard "2-5-9-11" definition |
| WLT-12 | Moon, Mercury, Jupiter or Venus exalted in the 2nd house | Very rich | BPHS-39 v.18; PVR §11.9 | |

---

## 3. BPHS chapter 41 — the specific yogas

### 3a. By the 5th house (BPHS-41 v.2–8)

| ID | 5th house is a sign of… and that planet is in the 5th | AND in the 11th | Result |
|---|---|---|---|
| WLT-13 | Venus (Taurus/Libra) | Mars | Great wealth |
| WLT-14 | Mercury (Gemini/Virgo) | Moon, Mars and Jupiter | Great wealth |
| WLT-15 | Sun (Leo) | Saturn, Moon and Jupiter | Great wealth |
| WLT-16 | Saturn (Capricorn/Aquarius) | Sun and Moon conjunct | Great wealth |
| WLT-17 | Jupiter (Sagittarius/Pisces) | Mercury | Great wealth |
| WLT-18 | Mars (Aries/Scorpio) | Venus | Wealthy leader |
| WLT-19 | Moon (Cancer) | Saturn | Wealthy leader |

Text variant: WP-Dhana gives WLT-13 as "Venus in own sign in the 5th with Mars in the Lagna". Santhanam's reading is Mars in the 11th. Flag when a chart depends on it.

### 3b. By the Lagna (BPHS-41 v.9–15)

Lagna must be the planet's own sign AND that planet must be in the Lagna AND be conjoined or aspected by the listed planets.

| ID | Lagna (lord in Lagna) | Joined/aspected by | Result |
|---|---|---|---|
| WLT-20 | Leo, Sun in Lagna | Mars and Jupiter | Wealthy |
| WLT-21 | Cancer, Moon in Lagna | Mercury and Jupiter | Wealthy |
| WLT-22 | Aries/Scorpio, Mars in Lagna | Mercury, Venus and Saturn | Prosperous |
| WLT-23 | Gemini/Virgo, Mercury in Lagna | Saturn and Jupiter | Wealthy |
| WLT-24 | Sagittarius/Pisces, Jupiter in Lagna | Mercury and Mars | Wealthy |
| WLT-25 | Taurus/Libra, Venus in Lagna | Saturn and Mercury | Wealthy |
| WLT-26 | Capricorn/Aquarius, Saturn in Lagna | Mars and Jupiter | Wealthy |

PVR §11.9(1)–(12) grades these: lord in own Lagna with the listed aspects = "very rich"; a weaker form = "very affluent".

### 3c. Modifiers

| ID | Condition | Result | Source |
|---|---|---|---|
| WLT-26a | Kendras are Vishnu's houses, trikonas are Lakshmi's; a link between their lords | Raja yoga (which also brings wealth) | BPHS-41 v.28 |
| WLT-26b | Weigh benefic vs malefic participants and their strength before declaring any yoga | Result full, partial or cancelled | BPHS-41 v.17 |

---

## 4. Named wealth yogas

| ID | Yoga | Condition | Result | Source | Notes |
|---|---|---|---|---|---|
| WLT-27 | Lakshmi | 9th lord AND Venus each in own or exaltation sign, placed in a kendra or trikona | Wealthy, brilliant | PD-6 sl. 21, 24 | B.V. Raman (*300 Important Combinations*) is usually quoted with a different definition — Lagna lord powerful and 9th lord in own/exaltation sign in a kendra/trikona. I did not read Raman at a URL: unverified attribution. Use the PD form as primary and log which variant fired |
| WLT-28 | Vasumati | All natural benefics in upachaya houses (3, 6, 10, 11) from Lagna or from Moon | Commands plenty of money | PD-6 sl. 19–20 | |
| WLT-29 | Amala | Natural benefic in the 10th from Lagna or Moon | Wealth and lasting fame | PD-6 sl. 19–20 | |
| WLT-30 | Pushkala | Lord of Moon sign with Lagna lord in a kendra/strong place, and a benefic aspecting Lagna | Wealthy, honoured | PD-6 sl. 19–20 | OCR partly garbled; verify exact wording |
| WLT-31 | Durudhara | Planets (other than Sun) in both the 2nd and 12th from Moon | Abundant wealth and vehicles | PD-6 sl. 5, 7 | |
| WLT-32 | Shubha-kartari | Benefics in both the 2nd and 12th from Lagna | Long-lived, healthy, rich | PD-6 sl. 11 | Reverse (malefics both sides) = poor, unhappy |
| WLT-33 | Chandra–Mangala | Moon conjunct Mars | Steady wealth | Mansagari via WP-Dhana | Often said to give earnings by rough means; that qualifier unsourced |
| WLT-34 | Malavya | Venus in a kendra in Taurus, Libra or Pisces | Wealth, vehicles, comforts | PD-6 sl. 1–4 | |
| WLT-35 | Lagna lord in Lagna | | Steady wealth | Mansagari via WP-Dhana | |
| WLT-36 | Exalted planet in the 5th or 9th | | Fortunate and famous | Bhavartha Ratnakara via WP-Dhana | |
| WLT-37 | Lagna lord and 2nd lord exchange signs | | Desirable for wealth | Raman, *300 Important Combinations* yogas 118–143, as cited by WP-Dhana | |
| WLT-38 | Kubera / Kalanidhi / "Maha Lakshmi" etc. | Many definitions online (e.g. Jupiter in 2nd or 5th joined/aspected by Mercury and Venus = Kalanidhi) | Wealth | **Unsourced – common practice / internet lore.** No classical verse read | Do not use as primary evidence |

---

## 5. Daridra (poverty) yogas — BPHS chapter 42

"Maraka" below = lord of the 2nd or 7th.

| ID | Condition | Result | Source |
|---|---|---|---|
| WLT-39 | Lagna lord in 12th AND 12th lord in Lagna, either joined/aspected by a maraka lord | Poverty | BPHS-42 v.2 |
| WLT-40 | Lagna lord in 6th AND 6th lord in Lagna, joined/aspected by a maraka lord | Without wealth | BPHS-42 v.3 |
| WLT-41 | Lagna lord or Moon with Ketu, AND Lagna lord in 8th joined/aspected by maraka lord | Poverty | BPHS-42 v.4 |
| WLT-42 | Lagna lord in 6/8/12 with a malefic AND 2nd lord debilitated or in an enemy sign | Poverty even if born rich | BPHS-42 v.5 |
| WLT-43 | 5th lord in 6th AND 9th lord in 12th, aspected by maraka lord | Poverty | BPHS-42 v.7 |
| WLT-44 | Lord of the Moon's navamsa sign conjunct a maraka lord or in a maraka house | Poverty | BPHS-42 v.10 |
| WLT-45 | Lagna lord and lord of the Lagna's navamsa both in 6/8/12, joined/aspected by maraka lord | Poverty | BPHS-42 v.11 |
| WLT-45a | Natural malefics in good houses and benefics in bad houses | Poverty | BPHS-42 v.12 |
| WLT-45b | A planet joined with a 6/8/12 lord and not aspected by a trikona lord | Financial loss in that planet's dasha | BPHS-42 v.13 |
| WLT-46 | Mars AND Saturn in the 2nd | Wealth destroyed — unless Mercury aspects them, then great wealth | BPHS-42 v.16–17 |
| WLT-47 | Sun in the 2nd aspected by Saturn → constant poverty; Sun in 2nd not aspected by Saturn → wealth and fame; Saturn in 2nd aspected by Sun → wealth | | BPHS-42 v.17–18 (read as referring to the 2nd house, per Santhanam's arrangement; site gloss is terse) |
| WLT-47a | 2nd lord AND 11th lord both in 6th, or both afflicted by malefics | Poor | BPHS-13 v.6 |
| WLT-47b | 2nd and 11th lords debilitated or combust and with malefics | Poor from birth | BPHS-13 v.7 |
| WLT-47c | 11th lord debilitated, or in 6/8/12 with malefics | No gain despite effort | BPHS-22 v.11 (site gloss also names the 7th; likely a mis-gloss — verify) |
| WLT-47d | Kemadruma: no planet (other than Sun) in the 2nd or 12th from Moon, none with Moon | Penury, obscurity | PD-6 sl. 5, 7 | Cancelled, per "some authorities" in the same verse, if a kendra is occupied or the Moon is with a planet |
| WLT-47e | 11th lord in a 6/8/12 house; or 11th/12th lord in the 8th with no benefic influence | Bankruptcy | Bhrigu Samhita via WP-Dhana | |

Saving factor stated by PVR §11.10: conjunction or aspect of a trikona lord rescues a daridra yoga; a maraka's conjunction/aspect confirms it.

---

## 6. Arudha Lagna (AL)

Calculation: count from Lagna to Lagna lord's sign, then the same count from there. Exception (PVR §9.2): if the result is the Lagna or the 7th, take the 10th from the result. BPHS-29 v.4–5 words the exception slightly differently — log which is used.

| ID | Condition | Result | Source |
|---|---|---|---|
| WLT-48 | Planets occupy or aspect the 11th from AL | Wealth; by fair means if benefics, by unfair means if malefics | BPHS-29 v.8–9 |
| WLT-49 | 11th from AL is aspected/occupied but the 12th from AL is not | Gains without obstruction | BPHS-29 v.12 |
| WLT-50 | Many planets, or exalted/friendly-sign planets, aspect the 11th from AL | Gains multiply; if all planets aspect it, king-like | BPHS-29 v.10–11, 13–15 |
| WLT-51 | 12th from AL joined/aspected by benefics and malefics | Heavy expenses; benefics = on proper channels, malefics = improper | BPHS-29 v.16–17 |
| WLT-52 | In the 12th from AL: Sun, Venus or Rahu → expenses through government/authority; Mercury → on relatives or disputes; Jupiter aspect → taxes; Saturn + Mars → on siblings | Channel of expense. The same planets in the 11th from AL give gain through that channel | BPHS-29 v.18–22 |
| WLT-53 | Jupiter, Venus or Moon (any) in the 7th from AL; or any planet exalted in the 7th from AL | Wealthy, well-reputed | BPHS-29 v.25–26 |
| WLT-54 | Benefic in the 2nd from AL; exalted Mercury, Jupiter or Venus in the 2nd from AL | Prosperity; rules over many | BPHS-29 v.27–28, 30 |
| WLT-55 | Compare the 11th and 12th from AL: stronger 11th = income exceeds outgo | Net accumulation | PVR §9.3 (Parashara and Jaimini both teach 11th/12th from AL = gains/expenses) |

Jaimini aspects (rasi drishti) are usually applied to AL work; BPHS-29 does not say which aspect type. State the choice.

---

## 7. Hora Lagna, Indu Lagna, Hora chart (D2)

| ID | Condition | Result | Source | Notes |
|---|---|---|---|---|
| WLT-56 | Hora Lagna (HL): advances one sign per hour from the Sun's sunrise position | HL shows the self in terms of money | PVR §5.3, §5.6 | |
| WLT-57 | A planet that owns, occupies or aspects both Lagna and HL | "Yogada" for money — its dasha brings wealth | PVR §13.2 | |
| WLT-58 | **Indu Lagna calculation.** Kalas: Sun 30, Moon 16, Mars 6, Mercury 8, Jupiter 10, Venus 12, Saturn 1 (nodes excluded). Add the kalas of the 9th lord from Lagna and the 9th lord from Moon. Divide by 12; remainder r (use 12 if r = 0). Count r signs from the Moon's sign, Moon's sign = 1. That sign is Indu Lagna | | INDU | Worked example at INDU: Libra Lagna, Moon in Cancer → Mercury 8 + Jupiter 10 = 18 → r = 6 → Sagittarius. Origin: INDU credits BPHS ("Moon yoga"); the method is usually credited to Kalidasa's *Uttara Kalamrita* (ch. 4). I could not read the Uttara Kalamrita verse online — attribution unverified, and I did not find it in the BPHS chapters read |
| WLT-59 | Benefics (or an exalted planet) in Indu Lagna or in kendras from it; a lone unafflicted benefic there | Wealth in that planet's dasha; malefics there give less, or wealth with trouble | INDU (general statement only); details unsourced – common practice | Low–medium reliability; use as a secondary check |
| WLT-60 | **D2 (Parashara Hora).** Odd signs: 0–15° = Sun's hora, 15–30° = Moon's hora. Even signs: reversed | | PVR §6.2.2; D2-P (BPHS ch. 6 v.5–6) | BPHS-7 v.1: Hora judges wealth |
| WLT-61 | Sun, Mars, Jupiter in Sun's hora; Moon, Venus, Saturn in Moon's hora; Mercury either | Planets "in their right hora" help wealth. Sun's hora = money by own effort/creation; Moon's hora = by accumulation and care | D2-P | Only two positions exist, so the chart is coarse |
| WLT-62 | Count planets in each hora | Majority in Sun's hora = self-earned, harder; majority in Moon's hora = easier, inherited or accumulated | Unsourced – common practice | PVR §6.2.2 explicitly does not use the Parashara hora chart. Other hora schemes (Kashinatha, parivritti) give 12-sign D2 charts and different readings |

---

## 8. Ashtakavarga

| ID | Condition | Result | Source | Notes |
|---|---|---|---|---|
| WLT-63 | SAV(11th) > SAV(10th) AND SAV(12th) < SAV(11th) AND SAV(Lagna) > SAV(12th) | Wealthy and comfortable: income exceeds effort, expense below income | AV (attributed there to BPHS ch. 71–72) | AV words the last clause as "Lagna has the most"; the common form is Lagna > 12th. Popular rule; test it |
| WLT-64 | SAV of a sign ≥ 30 strong; 25–30 average; < 25 weak | Strength of that house's results | PVR §12.4; AV | |
| WLT-65 | For 6th, 8th, 12th: SAV < 25 is good, > 25 adverse | | AV | Not in PVR; treat as secondary |
| WLT-66 | Transit of Jupiter/Saturn/dasha lord through a sign where its own BAV ≥ 5 | Gains; ≤ 3 = strain | PVR §12.3; DT-L | |

---

## 9. The 11th lord in each house (BPHS-24 v.121–132)

| ID | 11th lord in | Stated result |
|---|---|---|
| WLT-G1 | 1st | Wealthy, happy, even-minded, eloquent; always gains |
| WLT-G2 | 2nd | Wealthy, accomplished, generous, happy |
| WLT-G3 | 3rd | Skilled, wealthy, has siblings; occasional colic-type pain |
| WLT-G4 | 4th | Gains via mother's family; happiness from home and land |
| WLT-G5 | 5th | Happy, learned children; devoted to dharma |
| WLT-G6 | 6th | Illness, harsh temper, much travel, trouble from enemies |
| WLT-G7 | 7th | Gains through spouse's family; generous; influenced by spouse |
| WLT-G8 | 8th | Setbacks in undertakings; long life; spouse dies first |
| WLT-G9 | 9th | Fortunate, honoured by rulers, wealthy |
| WLT-G10 | 10th | Honoured by rulers, intelligent, self-controlled |
| WLT-G11 | 11th | Gains in all efforts; happiness grows daily |
| WLT-G12 | 12th | Spends on good causes; many attachments; mixes with foreigners |

2nd lord by house (BPHS-24 v.13–24), short form: 1 = wealth but family friction; 2 = wealthy, proud; 3 = brave, greedy; 4 = prosperous (with exalted Jupiter, king-like); 5 = wealthy, children earn; 6 = gain or loss via enemies by benefic/malefic influence; 7 = gain through spouse/medicine, marital strain; 8 = land and wealth but little marital or elder-sibling happiness; 9 = wealthy, sickly early, better later; 10 = respected, learned, wealthy; 11 = gains of every kind, fame; 12 = lacks wealth, depends on others.

---

## 10. Debt (6th) and loss (12th)

| ID | Condition | Result | Source | Notes |
|---|---|---|---|---|
| WLT-67 | 11th lord in 6th AND 6th lord in 11th | Wealth lost through enemies (text: at age 31) | BPHS-17 v.26 | |
| WLT-68 | 2nd and 11th lords in 6/8/12, Mars in 11th, Rahu in 2nd | Loss through government penalty | BPHS-13 v.8 | |
| WLT-69 | 6th lord linked with 2nd lord/2nd house, with malefic influence and no benefic aspect; Daridra yoga of PD-6 sl. 66–69 | Debts | PD-6 (names the yoga and "debts" as result); specific 6th-lord wording unsourced – common practice | Mars as karaka of debt is common practice, unsourced |
| WLT-70 | 12th lord in 1 (extravagant), 4 (losses in land/vehicles), 7 (expenses via spouse), 10 (expenses via government), 11 (losses in gains), 12 (excess spending) | Channel of loss | BPHS-24 v.133–144 | 12th lord in 8th = steady gains (v.140) — a vipareeta-type exception |
| WLT-71 | Lord of a significator aspects its own 12th, and Lagna lord aspects the 12th from Lagna | Strong tendency to overspend | BPHS-42 v.15 | |
| WLT-72 | Jupiter in 11th, Venus in 2nd, 2nd and 12th lords with benefics | Spends on religious/good works | BPHS-13 v.9 | |
| WLT-73 | Expense channel by planets in 12th from AL | See WLT-52 | BPHS-29 v.18–21 | |

---

## 11. Inheritance (8th)

| ID | Condition | Result | Source | Notes |
|---|---|---|---|---|
| WLT-74 | 2nd lord in 8th | Abundant land and wealth, but little marital happiness | BPHS-24 v.20 | Read by many as inherited/unearned wealth |
| WLT-75 | 8th lord strong and linked with 2nd/11th lords or Lagna lord, benefic influence on the 8th | Legacy, insurance, partner's money | Unsourced – common practice | No classical verse read |
| WLT-76 | Nirbhagya yoga | Loss of paternal property | PD-6 sl. 66–69 | Exact formation not legible in the OCR; verify |
| WLT-76a | 9th lord in the 2nd from the 9th (i.e. the 10th), or 9th lord debilitated, or Mars linked with the 4th | Father poor (small patrimony) | BPHS-20 v.4 | |

---

## 12. Property, vehicles, speculation

| ID | Condition | Result | Source | Notes |
|---|---|---|---|---|
| WLT-77 | 4th lord in the 4th, or Lagna lord in the 4th, aspected by benefics | Full domestic happiness | BPHS-15 v.2 | |
| WLT-78 | 4th lord in own sign, own navamsa or exaltation | Land, houses, vehicles | BPHS-15 v.3 | |
| WLT-79 | 4th lord conjunct 10th lord in a kendra or trikona | Fine, large house | BPHS-15 v.4 | |
| WLT-80 | 10th lord in 4th | Vehicles, land, houses | BPHS-24 v.112 | |
| WLT-80a | 12th lord in 4th | Losses in land, vehicles, houses | BPHS-24 v.136 | |
| WLT-80b | D4 (Chaturthamsa): parts of 7°30′ mapping to the 1st, 4th, 7th, 10th from the sign; read 4th house/lord and Mars (land), Saturn (old/agricultural property) there | Property and fixed assets | Calculation PVR §6.2.4 (D4 = residence, houses, property). BPHS-7 v.2 says D4 = fortune (bhagya). Mars = land, Saturn = old property: unsourced – common practice | |
| WLT-81 | Vehicles: 4th lord in the 4th exalted; or 4th lord with 10th lord in an exalted navamsa; or 11th lord in 4th / 4th lord with 11th lord. Ages named: 12, 32, 42 | Acquires vehicles | BPHS-15 v.11–13 | Venus as vehicle karaka is in v.12; D16 for vehicles is standard (Santhanam) but the site gloss of BPHS-7 v.3 is garbled |
| WLT-82 | Speculation: 5th house/lord strong and linked to 2nd/11th, with Jupiter or a well-placed Rahu; 5th lord or 11th lord in 8th/12th or 6th–11th exchange = losses | Gain or loss by speculation | Unsourced – common practice (KP: 5th cusp sub-lord signifying 2, 6, 11 = gain; 8, 12 = loss — unverified) | BPHS-24 v.17: 2nd lord in 5th = wealthy, children earn |

---

## 13. Timing of gains

| ID | Condition | Result | Source |
|---|---|---|---|
| WLT-83 | Dasha/antardasha of the 2nd and 9th lords (text) / 5th and 9th lords (PVR) and of planets joined with them | Wealth comes then | BPHS-41 v.16; PVR §11.9 |
| WLT-84 | Dasha of a planet joined with a 6/8/12 lord and lacking trikona-lord aspect | Financial loss | BPHS-42 v.13 |
| WLT-85 | Fixed ages in the text: 11th lord in 3rd with benefics → gain at 36; 11th lord in kendra/trikona with benefics → at 40; 11th lord in Lagna and Lagna lord with 11th → at 33; 9th–2nd exchange → after 32 | Indicative ages | BPHS-22 v.4, 5, 8; BPHS-20 v.10 |
| WLT-86 | Dasha of a yogada (WLT-57) or of planets in the 11th/2nd from AL | Visible rise in means (PVR example: Jupiter in 2nd from AL) | PVR §13.2, Ex. 32 |
| WLT-87 | Jupiter and Saturn both transiting/aspecting the 2nd or 11th (or their lords) in a supporting dasha | Year of gain | DT-L (double transit; modern) |
| WLT-88 | Transit through high-SAV signs (≥ 30) by Jupiter/Saturn; through low-SAV signs (< 25) = lean period | | PVR §12.4; AV |

---

## Reliability notes

**Widely agreed classical rules:** WLT-01..12 (2nd/11th lord placement), the chapter 41 yogas WLT-13..26, chapter 42 poverty yogas WLT-39..47, AL 11th/12th rules WLT-48..55, lord-in-house tables. These are directly in BPHS and repeated by PVR and Raman.

**Classical but with text problems:** WLT-13 (Mars in 11th vs Lagna), WLT-47 (terse verse), WLT-47c (7th house gloss), WLT-30/76 (OCR). BPHS itself has variant recensions; chapters on yogas differ between editions.

**Modern or weakly sourced:** Indu Lagna reading rules (WLT-59), counting planets in D2 (WLT-62), the SAV comparison (WLT-63 — attributed to BPHS by the page read, but I did not see the verse), Kubera/Kalanidhi and similar named yogas (WLT-38), all speculation and inheritance rules except the lord-in-house lines, double transit for money (WLT-87).

**Practical cautions:**
- "Great wealth", "king", "beggar" are relative to family station (BPHS-39 v.44–45 says so for raja yogas).
- A dhana yoga without a supporting dasha in working life may never show. Always pair a natal yoga with WLT-83.
- Daridra yogas need the maraka-lord link AND no trikona-lord relief before being stated; never tell a client "poverty" from one factor.

**Empirical tests:** none found for any wealth rule. The one controlled Indian test read (Narlikar et al. 2009, *Current Science* 96(5); summary at https://thoughtnaction.antisuperstition.org/an-indian-test-of-indian-astrology/) found astrologers at chance on a different question. Score these rules against the project's own verified charts before trusting them.
