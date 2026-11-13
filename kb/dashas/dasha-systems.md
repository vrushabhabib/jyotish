# Dasha systems: Vimshottari judgement, Yogini, Ashtottari, Chara (K.N. Rao), Narayana, conditional dashas

Sources read in this session:
- **[PVR]** P.V.R. Narasimha Rao, *Vedic Astrology: An Integrated Approach*, ch. 16–18: https://www.vedicastrologer.org/articles/vedic_astro_textbook.pdf
- **[PVR-CD]** PVR, "Parasara's Chara dasa" paper: https://www.vedicastrologer.org/articles/pp_chara_dasa.pdf
- **[PVR-COND]** PVR, conditional dasas paper: https://www.vedicastrologer.org/articles/pp_cond_dasas.pdf
- **[JB]** PVR list post on Sc/Aq lords and K.N. Rao's practice: https://jyotish-blog.blogspot.com/2005/02/chara-dasa-lords-of-aq-and-sc-re.html
- **[SAT]** https://satyori.com/jyotish/dasha/chara/ and https://satyori.com/jyotish/dasha/ashtottari/
- **[TEM]** https://www.tempora.ltd/findings/chara-dasha-calculator-table
- **[ABX]** https://astrobix.com/learn/141-calculation-of-char-dasha.html
- **[MEM-KNR]** K.N. Rao, *Predicting through Jaimini's Chara Dasha* — from recall; the book itself was not readable online. Items so marked must be checked against the book.
- **[MEM]** standard teaching, from recall. (Laghu Parashari itself was read from the Sanskrit on 13 Nov 2026 - see `kb/sources/laghu-parashari/README.md`; lines below that still carry [MEM] and cite it are superseded by that file where they differ.)

---

## 1. Vimshottari — rules for judging (calculation assumed already implemented)

Order and years: Ketu 7, Venus 20, Sun 6, Moon 10, Mars 7, Rahu 18, Jupiter 16, Saturn 19, Mercury 17 = 120. Sub-period length = MD years × AD years / 120, starting from the MD lord.

### 1.1 What a dasha lord delivers (apply in this order) [MEM]
1. **Houses owned** (functional nature for the lagna): trikona lords (1, 5, 9) benefic; kendra lords neutralised; 3, 6, 11 lords malefic; 8 and 12 lords take the colour of association; 2 and 7 lords are marakas. (Laghu Parashari.)
2. **House occupied** and the sign dignity there.
3. **Planets conjunct / aspecting** the lord — it delivers their results too; Rahu/Ketu deliver the results of their dispositor and of planets conjunct them.
4. **Nakshatra lord of the dasha lord** — the dasha lord gives the results of the houses owned/occupied by its star lord (strong in KP and in most South Indian practice; a secondary factor in strict Parashari).
5. **Natural significations** (karakatva).
6. **Strength**: Shadbala ratio, Vimshopaka, avastha, combustion, retrogression, Ishta/Kashta — decides how much and how smoothly.
7. **Yogas** the lord takes part in fructify in its MD/AD.
8. **Repeat from Moon and from the relevant divisional chart** (D9 for marriage, D10 career, D7 children). A result promised by lagna, Moon and varga together is firm.

### 1.2 MD lord versus AD lord [MEM]
- Count the AD lord's sign from the MD lord's sign.
  - AD lord in the 6th, 8th or 12th from the MD lord: obstructs - loss of place, quarrels, expense, the AD breaks from the MD's direction. [BPHS ch. 52-60, stated pair by pair; read from the Sanskrit 12 Nov 2026]
  - AD lord in a kendra, a trine, the 3rd or the 11th from the MD lord: supports. The **2nd** from the MD lord is listed with the supportive places in most pairs - the earlier note here that 2/12 is adverse on both sides was wrong for the 2nd. [same source]
  - Exceptions the text states outright (bad first, good only when specially strong): Ketu's AD in the Sun's, Rahu's and Saturn's MDs; Rahu's AD in Saturn's MD; Saturn's AD in Ketu's MD; the Sun's AD in Venus's MD. See `kb/sources/bphs/ch51-60.md`.
- Natural and temporary friendship between the two lords: friends cooperate, enemies obstruct.
- Laghu Parashari rules, **now read from the Sanskrit (13 Nov 2026, `kb/sources/laghu-parashari/README.md`) - these replace the recalled version:** (a) no planet gives its own nature's result in its own sub-period of its own dasha; it gives it in the sub-periods of planets related to it or of the same nature (v.29-30); (b) **in a malefic's dasha the sub-period of an unrelated benefic gives bad results, of a related benefic mixed results, and of an unrelated yoga-maker very bad results (v.37-38)** - the earlier recalled line "a yogakaraka's AD inside a malefic's MD still gives good results if the two are related" overstated it: the text says mixed; (c) Saturn and Venus give each other's results in each other's periods (v.40); (d) the 2nd and 12th lords go by association and by their other house (v.8); the 8th lord is not good unless he is also the lagna lord, and the Sun and Moon carry no 8th-lord blemish (v.9, 11); the maraka verses are not used. Tested as a direction rule on 13 Nov 2026: 7 right of 15 calls, wrong charts average 8.1 - at chance (antar-event-rules.md, Rule 17).
- The AD lord is judged for houses counted from the MD lord's sign as a temporary lagna (e.g. AD lord in the 10th from the MD lord → work prominence).
- Pratyantar (PD) lords are read the same way relative to the AD lord; use PD only to narrow timing once MD and AD both agree.

### 1.3 Dasha sandhi and Dasha chhidra [MEM]
- **Dasha sandhi**: the junction between two mahadashas. Common working window: the last and first portions of the adjoining MDs (many use about 6 months either side, or the last AD of the ending MD plus the first AD of the new MD). Transitional, unstable; riskier when the two MD lords are mutual enemies or 6/8 from each other (e.g. Rahu→Jupiter, Venus→Sun, Mars→Rahu). In matching, overlapping sandhis of the couple within a short time are considered unfavourable.
- **Dasha chhidra**: the last antardasha of a mahadasha (e.g. Venus MD – Ketu AD; Saturn MD – Jupiter AD). Regarded as the "gap" of the dasha: endings, loss of what the MD built, health dips, especially for the old or when the AD lord is a maraka or ill-placed.
- Nakshatra-edge note: when the Moon is within a few arc-minutes of a nakshatra boundary, the whole Vimshottari sequence is uncertain; flag it.

### 1.4 Honesty rule for the engine
Dasha dates are astronomically reliable; the mapping from lords to events is not unique. Every planet rules/occupies/aspects enough houses that some rationale can be found for almost any event (the project's own test: 248 candidate charts scored within half a point). Therefore: state predictions as themes with the specific chain of reasons (lordship → placement → star lord → strength), demand agreement of MD + AD + transit (Jupiter/Saturn "double transit") + a second dasha system before calling a period significant, and never use post-hoc PD/sookshma fits as evidence.

---

## 2. Yogini dasha (36-year cycle) [MEM — standard and uniform across sources; not re-read this session]

| # | Yogini | Lord | Years |
|---|---|---|---|
| 1 | Mangala | Moon | 1 |
| 2 | Pingala | Sun | 2 |
| 3 | Dhanya | Jupiter | 3 |
| 4 | Bhramari | Mars | 4 |
| 5 | Bhadrika | Mercury | 5 |
| 6 | Ulka | Saturn | 6 |
| 7 | Siddha | Venus | 7 |
| 8 | Sankata | Rahu | 8 |

**Starting yogini**: `r = (N + 3) mod 8`, N = Moon's nakshatra number (Ashwini = 1 … Revati = 27); r = 0 → Sankata (8), otherwise yogini number r.
Check values: Ashwini → 4 Bhramari; Bharani → 5 Bhadrika; Krittika → 6 Ulka; Rohini → 7 Siddha; Mrigashira → 8 Sankata; Ardra → 1 Mangala; Punarvasu → 2 Pingala; Pushya → 3 Dhanya.

**Balance at birth**: `balance = years(start) × (1 − fraction_of_nakshatra_traversed_by_Moon)`. Then proceed in order 1→8 cyclically; the 36-year cycle repeats (3 cycles = 108 years).

**Antardasha**: within MD of M years, the AD of a yogini with A years lasts `M × A / 36` years; sequence starts from the MD yogini itself and continues in order.

**Reading**: Mangala, Dhanya, Bhadrika, Siddha are favourable; Pingala, Bhramari, Ulka, Sankata give strain (travel, upheaval, loss, crisis). Judge the lord planet exactly as a Vimshottari lord. Yogini is the conventional cross-check for Vimshottari in North India: an event window is trusted when both agree.

---

## 3. Ashtottari dasha (108 years) [PVR ch. 17; SAT]

**Applicability** — three positions in the literature [PVR]:
1. applies to all charts;
2. when Rahu, not in the lagna, is in a kendra or trikona from the lagna lord (BPHS condition, also in [PVR-COND]);
3. day birth in Krishna paksha or night birth in Shukla paksha.
Recommended: compute it always, flag which of (2) and (3) hold, and use it as a secondary system only when at least one holds.

**Order, years and nakshatra arcs** [PVR table; Abhijit not used]:

| Lord | Years | Nakshatras | Sidereal arc |
|---|---|---|---|
| Sun | 6 | Ardra, Punarvasu, Pushya, Ashlesha | 66°40'–120°00' |
| Moon | 15 | Magha, P.Phalguni, U.Phalguni | 120°00'–160°00' |
| Mars | 8 | Hasta, Chitra, Swati, Vishakha | 160°00'–213°20' |
| Mercury | 17 | Anuradha, Jyeshtha, Mula | 213°20'–253°20' |
| Saturn | 10 | P.Ashadha, U.Ashadha, Shravana | 253°20'–293°20' |
| Jupiter | 19 | Dhanishta, Shatabhisha, P.Bhadrapada | 293°20'–333°20' |
| Rahu | 12 | U.Bhadrapada, Revati, Ashwini, Bharani | 333°20'–26°40' |
| Venus | 21 | Krittika, Rohini, Mrigashira | 26°40'–66°40' |

Ketu has no dasha. Order of dashas: Sun → Moon → Mars → Mercury → Saturn → Jupiter → Rahu → Venus.

**Balance** [PVR]: find the arc containing the Moon; `balance = years × (arc_end − Moon) / arc_length`. Arc lengths are 53°20' (4 stars) or 40° (3 stars). PVR's example: Moon at 144° in Moon's arc, 16° of 40° left → 0.4 × 15 = 6 years.

Variant [MEM]: the classical version includes Abhijit in Saturn's group (U.Ashadha, Abhijit, Shravana — hence "4 stars") and apportions years per nakshatra (each star of a 4-star group gets 1/4 of the lord's years, each of a 3-star group 1/3). PVR's continuous-arc method and the per-star method give different balances for Saturn's group. Label the method.

**Antardasha**: `MD × AD / 108`, in the same order starting from the MD lord [SAT]. (Some texts start from the lord after the MD lord — verify if sub-periods are published.)

---

## 4. Jaimini Chara dasha — K.N. Rao's method

Status: steps 4.1–4.3 below are corroborated by pages read online ([ABX], [SAT], [TEM], [JB]); the Scorpio/Aquarius tie-break order (4.4) and antardasha direction (4.5) are from recall of Rao's book and need checking against it.

### 4.1 Mahadasha sequence
The first MD is the lagna sign. All 12 signs follow consecutively.
- **Direct (zodiacal) sequence** if the lagna is Aries, Leo, Virgo, Libra, Aquarius or Pisces.
- **Reverse (anti-zodiacal) sequence** if the lagna is Taurus, Gemini, Cancer, Scorpio, Sagittarius or Capricorn.

This is the same thing as the padakrama rule "look at the 9th sign from lagna: if it is odd-footed (Aries, Taurus, Gemini, Libra, Scorpio, Sagittarius) go forward, if even-footed (Cancer, Leo, Virgo, Capricorn, Aquarius, Pisces) go backward" [PVR-CD; SAT attributes the 9th-from-lagna key to Rao].

### 4.2 Dasha years of each sign
- Signs counted **forward** to their lord: Aries, Taurus, Gemini, Libra, Scorpio, Sagittarius.
- Signs counted **backward** to their lord: Cancer, Leo, Virgo, Capricorn, Aquarius, Pisces.
- Count inclusively from the dasha sign to the sign holding its lord, then **subtract 1** → years [PVR-CD; ABX; TEM].
- Lord in its own dasha sign → **12 years** (not 0).
- Result range 1–12.

Examples: Taurus with Venus in Scorpio → forward, Taurus(1)…Scorpio(7) = 7, minus 1 = **6 years**. ([ABX] prints "8 → 7" for this case, which looks like a counting slip on that page; Taurus to Scorpio is 7 signs inclusive.) Virgo with Mercury in Capricorn → backward: Virgo(1), Leo, Cancer, Gemini, Taurus, Aries, Pisces, Aquarius, Capricorn(9) → 9 − 1 = **8 years** (matches [ABX]).

### 4.3 Exaltation / debilitation adjustment
BPHS/Jaimini commentaries add 1 year if the lord is exalted and subtract 1 if debilitated. **K.N. Rao does not apply this** ([JB]: "Sri KN Rao ignores this exception"; his example gives Scorpio 7 years with a debilitated Ketu where the Parashara variant gives 6). PVR also recommends dropping it [PVR-CD]. Implement as an option, default off for the Rao variant.

### 4.4 Scorpio and Aquarius (two lords)
Scorpio: Mars and Ketu. Aquarius: Saturn and Rahu. Decide which lord to count to [MEM-KNR for the order; individual tests corroborated by PVR-CD/SAT/TEM]:
1. Both lords in the sign itself → 12 years.
2. One lord in the sign, the other elsewhere → count to the one placed elsewhere.
3. Both elsewhere, in different signs → the stronger one:
   a. the one conjoined with more planets;
   b. if equal, the one in exaltation (dignity) [TEM also lists "an exalted occupant settles it"];
   c. if still equal, sign-quality test — sources disagree on direction: [PVR-CD] movable > fixed > dual; Rath-school texts dual > fixed > movable. Rao's book position not verified;
   d. if still equal, the one that yields the larger number of years ([PVR-CD] rule 6); [SAT] instead mentions "higher degree decides".
4. Both lords together in some other sign → no choice needed; count to that sign.

Implement 1, 2, 3a, 4 as certain; make 3b–3d a configurable ordered list and log which test decided.

### 4.5 Antardashas
- 12 antardashas, each = MD/12 (so an MD of n years has ADs of n months each) [ABX; SAT; TEM].
- The MD sign's own antardasha comes **last**; the sequence starts from the next sign in the direction of travel [SAT].
- Direction: [ABX], [SAT], [TEM] say "same direction as the mahadasha sequence". From recall of Rao's book the direction of sub-periods is fixed by the MD sign's own group (4.1 list applied to the MD sign), which gives a different order whenever the MD sign's group differs from the lagna's. RESOLVED for this project (12 Nov 2026): the AstroSage printout for a Capricorn lagna shows Libra, Virgo and Leo mahadashas running their sub-periods forward and Cancer, Gemini and Taurus backward, i.e. direction by the MD sign's own group. `engine/dashas_extra.py` follows that and reproduces all twelve AstroSage mahadasha lengths (AstroSage itself prints Aquarius as "-1 Year", a wrap-around bug; the rule gives 11). Rao's book is still unread.

### 4.6 Algorithm
```
signs 0..11 (Aries=0)
SEQ_DIRECT   = {0,4,5,6,10,11}          # lagna groups for MD order
COUNT_FWD    = {0,1,2,6,7,8}            # signs counted forward to lord
lord = {0:Mars,1:Venus,2:Mercury,3:Moon,4:Sun,5:Mercury,6:Venus,7:[Mars,Ketu],8:Jupiter,9:Saturn,10:[Saturn,Rahu],11:Jupiter}

years(s):
    L = sign of chosen lord (apply 4.4 for s in {7,10})
    if L == s: return 12
    n = (L - s) % 12 if s in COUNT_FWD else (s - L) % 12     # n = inclusive count - 1
    return n                                                   # 1..11

order = [(lagna + k) % 12 for k in 0..11] if lagna in SEQ_DIRECT else [(lagna - k) % 12 for k in 0..11]
```
Total of the 12 dashas varies by chart (it is not a fixed cycle). After the 12th dasha a second cycle starts; a common rule for the second cycle is `12 − first-cycle years` [PVR gives this for Narayana dasha; Rao rarely needs it]. Dasha starts at birth with the full lagna-sign dasha (no balance calculation in Rao's method).

### 4.7 Reading Chara dasha (Rao's approach, brief) [MEM-KNR]
Chara karakas (7-karaka scheme in Rao: AK, AmK, BK, MK, PK, GK, DK by descending degrees, Rahu excluded), Jaimini rasi aspects (movable signs aspect fixed signs except the adjacent one; fixed aspect movable except adjacent; dual aspect dual), karakamsa, pada lagna (arudha) and upapada. An MD/AD sign delivers the karakas placed in or aspecting it: e.g. marriage when the dasha sign contains or aspects DK, or is the 7th/DK-navamsa sign; career rise with AmK and the 10th from the dasha sign.

---

## 5. Narayana dasha (mention) [PVR ch. 18]
- Seed: the stronger of lagna and the 7th house.
- Progression: movable seed → consecutive signs; fixed seed → every 6th sign; dual seed → trinal order (1st, 5th, 9th then next kendra group).
- Direction: by the 9th sign from the seed — odd-footed forward, even-footed backward. Saturn in the seed forces regular zodiacal progression; Ketu in the seed reverses the direction.
- Years: count from the dasha sign to its lord, minus 1; lord in the sign → 12; **+1 if lord exalted, −1 if debilitated** (kept in Narayana dasha). Scorpio/Aquarius use the stronger co-lord.
- Second cycle: 12 − first-cycle years.
- Use: a general-purpose rasi dasha showing environment and direction of effort; needs divisional-chart versions for specific areas. Not for the first engine version, but the years routine is shared with Chara dasha.

## 6. Conditional (nakshatra) dashas of BPHS [PVR-COND]

| Dasha | Years | Condition | Seed nakshatra |
|---|---|---|---|
| Ashtottari | 108 | Rahu in kendra/trikona from lagna lord, not in lagna | Ardra |
| Shodashottari | 116 | Lagna in Sun's hora in Shukla paksha, or Moon's hora in Krishna paksha | Pushya |
| Dwadashottari | 112 | Lagna in Taurus or Libra navamsa | Revati (counted backward) |
| Panchottari | 105 | Lagna in Cancer dwadasamsa | Anuradha |
| Shatabdika | 100 | Lagna vargottama (same sign in D1 and D9) | Revati (counted forward) |
| Chaturashiti-sama | 84 | 10th lord in the 10th | Swati |
| Dwisaptati-sama | 72 | Lagna lord in 7th, or 7th lord in lagna | Mula |
| Shashtihayani (Shashti-sama) | 60 | Sun in lagna | Ashwini |
| Shat-trimsa-sama | 36 | Day birth with lagna in Sun's hora, or night birth with lagna in Moon's hora | Shravana |

Planet orders and per-planet years for these were not in the page read; take them from BPHS ch. 46 (Santhanam) before implementing. Other systems to know by name: Kalachakra (navamsa-pada based, BPHS), Sthira, Shoola/Niryana Shoola (longevity), Drig, Sudasa (wealth), Mandooka, Moola dasha.

---

## Implementation notes

- Yogini: nakshatra number from the Moon's Lahiri longitude: `N = floor(moon / 13.3333) + 1`; traversed fraction = `(moon mod 13.3333) / 13.3333`. Year length: use the same convention as the Vimshottari implementation (365.25 days vs sidereal/tropical year vs 360-day) so cross-checks line up.
- Ashtottari: Rahu's arc wraps 360°; add 360 to the Moon when it is below 26°40'. Applicability test (2) needs kendra/trikona counted by sign from the lagna lord's sign.
- Chara: use rasi positions only; Rahu and Ketu use true or mean node — sign changes are possible near boundaries, log it. Lagna within ~1° of a sign boundary changes the entire sequence; flag as unstable.
- Chara: when a single lord (Mars/Saturn) and its co-lord (Ketu/Rahu) are in the same non-home sign, count to that sign.
- Keep `years(sign, variant)` as one function with switches: `minus_one` (always true here), `exalt_debil_adjust` (false for Rao, true for Parashara/Narayana), `dual_lord_rules` (ordered list).
- Antardasha direction switch: `by_md_sequence | by_md_sign_group` until verified.
- Dasha sandhi/chhidra: emit as flags on the period table (last AD of each MD = chhidra; ±6 months around MD change = sandhi, window configurable).
- MD/AD relationship: precompute sign distance (1–12) between lords and classify {1/1, 2/12, 3/11, 4/10, 5/9, 6/8, 7/7}.

## Reliability notes

- Yogini table and formula: uniform across every source known; safe to code. Spot checks above are self-consistent with the standard nakshatra lists (Mangala = Ardra, Chitra, Shravana).
- Ashtottari table and balance: read from [PVR]; the Abhijit/per-star variant is real and changes results in Saturn's group.
- Chara dasha: the two sign groups, minus-one rule, 12-year rule and Rao's rejection of the exaltation adjustment are corroborated online. NOT verified against Rao's own text: the tie-break order for Sc/Aq lords beyond "more conjunct planets", and antardasha direction. Software packages differ on exactly these points.
- Many websites state "odd signs forward, even signs backward" for Chara dasha — that is a different (wrong for Rao) rule; do not use it.
- Vimshottari judgement rules are textbook Laghu Parashari practice from recall; chapter/verse numbers were not looked up.
- Interpretation is the weak link in every dasha system; treat single-system, single-level matches as non-evidence.


## Rules for judging a dasha and sub-period, read in the Sanskrit (Phaladeepika 20.22-63 and BPHS 47-60; 12 Nov 2026)
Source notes: `kb/sources/phaladeepika/ch20-28.md`, `kb/sources/bphs/ch46-50.md`, `ch51-60.md`. These replace the "from memory" tags on the Laghu-Parashari lines above.
1. **Subject and outcome.** The lord's houses say what the period is about (BPHS 48.2-7); its strength and placement say how it goes (PD 20.2-20). A lord of the 6th, 8th, 11th or 12th that is strong and well placed gives the good side of its house (PD 20.7, 9, 12, 13).
2. **Scale.** Good results: full in exaltation, three quarters in moolatrikona, half in own sign, a quarter in a friend's, little in an enemy's, none in debilitation or combustion; bad results the other way (PD 20.30; BPHS 3.59-60). The twenty-point strength grades it (BPHS 7.26-27).
3. **Sub-lord from dasha lord.** The sub-lord gives the results of the house it occupies counted from the dasha lord; the 6th, 8th and 12th from it are hard, the rest comfortable (PD 20.29; BPHS ch. 52-60).
4. **Own sub-period.** A planet does not give its own results in its own sub-period; they come in the sub-periods of planets connected with it or of like nature (PD 20.43-44).
5. **Kendra and trine lords.** Trine lords always good; a benefic owning a kendra is blemished (Jupiter and Venus most, then Mercury, then the Moon), a malefic owning one improves; lords of the 3rd, 6th and 11th give trouble; the 8th lord too unless it is also lagna lord or is the Sun or Moon (PD 20.41, 50-51; BPHS ch. 34). Kendra and trine lords connected give yoga and help in each other's sub-periods (PD 20.42, 45-49).
6. **When in the period.** By the third of the sign (BPHS 47.3-4) and by the rising-type of the sign (BPHS 50.88-89; PD 20.33); stated only when the two agree.
7. **Transit of the dasha lord itself.** The house it is passing through prospers while it is in its own, exaltation or a friend's sign (if strong at birth), and suffers while it is debilitated, combust or in an enemy's sign (PD 20.34-35, 37).
8. **Month trigger.** The good of a favourable dasha lord arrives when the Sun (or Jupiter) is in that lord's own or exaltation sign; the hardship of an unfavourable one when the Sun is in its debilitation or an enemy's sign (PD 20.38).
9. **Day-level tone.** The Moon in the dasha lord's exaltation or friendly sign, or in the 3rd, 6th, 7th, 10th, 11th or a trine from it: favourable days (PD 20.36, 60-62).
10. **Fixed grids are tie-breakers only.** Mantreshvara's 81 unconditional sub-period verses (PD ch. 21) and Parashara's finer-level grids (BPHS ch. 61-63) ignore placement; rules 1-3 override them.

## Further verified dasha rules (Jataka Parijata ch. 18 and Brihat Jataka ch. 8, read in the Sanskrit 12 Nov 2026)
These agree with the ten rules above and add four things.
11. **The moment a period begins matters** (Brihat Jataka 8.10; Jataka Parijata 18.6-9, 14): good when the dasha lord is then in the lagna or the 3rd, 6th, 10th or 11th; and when the Moon is then in the lord's friend's or exaltation sign, or in the 7th, a trine or an upachaya house from it. Deliberately not computed: it needs the start of the period to the hour, and a quarter-hour of doubt in the birth time already moves every start by about ten weeks (see the 'How firm the dates are' table in the worksheet).
12. **Dasha lord and sub-lord: mutual friends and strong - good; mutual enemies and weak - harm; in the 6th and 8th from each other - fear, loss of position, leaving one's place** (Jataka Parijata 18.16, 18.30, 18.53). With rule 4 above (sub-lord's house from the dasha lord) this is now stated by three texts.
13. **A debilitated planet, a planet joined to it, a planet joined to Rahu, and the lord of a debilitated planet's sign do not give good in their periods** (18.28). A planet at a sign junction gives strain in its period (18.27).
14. **Which third of a period gives what** (18.57-58): a benefic gives the matters of its house first, of its sign in the middle, of the aspects on it last; a malefic gives the result of its dignity first, of its house in the middle, of the aspects last. Together with the head-rising / back-rising rule (four texts) this is the texts' whole method for timing inside a period.
15. Sub-periods of the lords of the 2nd, 4th, 6th, 8th and 9th stars from the birth star are helped (18.25) - a small additional vote, untested here.
All five are the texts' statements, not findings of this project; none has a hit rate in the ledger yet.
