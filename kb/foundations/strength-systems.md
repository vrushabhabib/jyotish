# Strength systems (Parashari): Shadbala, Bhava bala, Vimshopaka, Avasthas, special degrees

Conventions: sidereal longitudes (Lahiri), whole-sign houses. 60 virupas (shashtiamsas) = 1 rupa.
Source tags used below:

- **[SAR]** Saravali-site bala pages, read online: https://saravali.github.io/astrology/bala_summary.html , https://saravali.github.io/astrology/bala_sthana.html , https://saravali.github.io/astrology/bala_kala.html
- **[PVR]** P.V.R. Narasimha Rao, *Vedic Astrology: An Integrated Approach*, read online (parts): https://www.vedicastrologer.org/articles/vedic_astro_textbook.pdf
- **[BPHS45]** BPHS ch. 45 (Avasthas), Santhanam numbering, read via https://www.barbarapijan.com/bpa/Amsha/avasta_BPHS_ch45_Avasta.htm
- **[MEM-Raman]** B.V. Raman, *Graha and Bhava Balas* — stated from recall, NOT re-read online in this session. Verify before relying on the exact number.
- **[MEM-BPHS]** BPHS (Santhanam) ch. 26 (drishti), ch. 27 (Shadbala), ch. 16 (Vimshopaka) — from recall, not re-read.

---

## A. Shadbala (BPHS ch. 27; Raman, *Graha and Bhava Balas*)

Total Shadbala = Sthana + Dig + Kala + Cheshta + Naisargika + Drik (virupas). Divide by 60 for rupas.
Only the seven planets Sun..Saturn get Shadbala (no Rahu/Ketu).

### A1. Sthana bala (positional) = Uchcha + Saptavargaja + Ojayugma + Kendradi + Drekkana

**1. Uchcha bala** [SAR; MEM-Raman]
`uchcha = arc(planet, debilitation_point) / 3`, where arc is the shorter angular distance (0–180). Max 60 at exact exaltation, 0 at exact debilitation.

| Planet | Exaltation point | Debilitation point (abs. longitude) |
|---|---|---|
| Sun | 10° Aries | 10° Libra (190°) |
| Moon | 3° Taurus | 3° Scorpio (213°) |
| Mars | 28° Capricorn | 28° Cancer (118°) |
| Mercury | 15° Virgo | 15° Pisces (345°) |
| Jupiter | 5° Cancer | 5° Capricorn (275°) |
| Venus | 27° Pisces | 27° Virgo (177°) |
| Saturn | 20° Libra | 20° Aries (20°) |

**2. Saptavargaja bala** — dignity of the planet in 7 vargas: D1, D2, D3, D7, D9, D12, D30. Sum the 7 scores.

| Dignity | Raman [MEM-Raman] | BPHS/Santhanam as shown on [SAR] |
|---|---|---|
| Moolatrikona (Raman: counted in D1 only) | 45 | 45 |
| Own sign (swakshetra) | 30 | 30 |
| Great friend (adhimitra) | 22.5 | 20 |
| Friend (mitra) | 15 | 15 |
| Neutral (sama) | 7.5 | 10 |
| Enemy (shatru) | 3.75 | 4 |
| Great enemy (adhishatru) | 1.875 | 2 |

Two published scales exist. Raman's halving series (45, 30, 22.5, 15, 7.5, 3.75, 1.875) is what most software (incl. Jagannatha Hora) uses; the rounded BPHS reading (45, 30, 20, 15, 10, 4, 2) is what [SAR] shows. Pick one and label it. Exaltation/debilitation are NOT scored here (already in Uchcha bala). Dignity uses the compound (panchadha) relationship = natural + temporal friendship, temporal computed from the rasi chart positions.

**3. Ojayugma bala** [SAR] — Moon and Venus: 15 if in an even sign in D1, plus 15 if in an even sign in D9. Sun, Mars, Jupiter, Mercury, Saturn: 15 for odd sign in D1, plus 15 for odd sign in D9. Max 30.

**4. Kendradi bala** [SAR] — kendra (1,4,7,10) 60; panaphara (2,5,8,11) 30; apoklima (3,6,9,12) 15.

**5. Drekkana bala** — 15 virupas if:
- male planets (Sun, Mars, Jupiter) in 1st decanate (0–10°);
- neuter planets (Mercury, Saturn) in 2nd decanate (10–20°);
- female planets (Moon, Venus) in 3rd decanate (20–30°). [MEM-BPHS, MEM-Raman]

DISCREPANCY: the [SAR] page gives Moon/Venus the middle decanate and Mercury/Saturn the last. BPHS 27 order is "male, neuter, female → first, middle, last". Use the BPHS order above; verify once against Santhanam ch. 27.

### A2. Dig bala (directional) [MEM-Raman; principle confirmed on SAR summary]

`dig = arc(planet, powerless_point) / 3` (arc 0–180 → 0–60).

| Planets | Full strength at | Powerless point |
|---|---|---|
| Jupiter, Mercury | Lagna (east) | Descendant (Asc + 180°) |
| Sun, Mars | 10th (south) | IC (MC + 180°) |
| Saturn | 7th (west) | Ascendant |
| Moon, Venus | 4th (north) | MC |

### A3. Kala bala (temporal) = Nathonnata + Paksha + Tribhaga + Abda + Masa + Vara + Hora + Ayana (+/− Yuddha)

**1. Nathonnata (diva-ratri) bala** [SAR qualitative; formula MEM-Raman]
Let `u` = time distance of birth from local apparent midnight, as a fraction of half a day (0 at midnight, 1 at local apparent noon).
- Sun, Jupiter, Venus (day-strong): `60 × u`
- Moon, Mars, Saturn (night-strong): `60 × (1 − u)`
- Mercury: 60 always.
(Raman: unnata = 30 ghatis − nata, where nata = ghatis from midday; bala = 2 × unnata for the day group.)

**2. Paksha bala** [SAR]
`p = ((Moon − Sun) mod 360) / 3`; if `p > 60` then `p = 120 − p`.
- Benefics (Jupiter, Venus, and Mercury if not with a malefic; Moon — see note): `p`
- Malefics (Sun, Mars, Saturn; Mercury if conjunct a malefic): `60 − p`
- The Moon's paksha bala is doubled [MEM-BPHS/Raman].
Note on Moon: [SAR] treats the Moon as benefic in the bright half and malefic in the dark half; Raman simply gives the Moon the benefic value `p` and doubles it. Results differ only for the waning Moon. Make it a config switch; default to Raman.

**3. Tribhaga bala** [SAR] — split day (sunrise→sunset) into 3 equal parts: lords Mercury, Sun, Saturn. Split night (sunset→next sunrise) into 3: Moon, Venus, Mars. The lord of the part containing birth gets 60. Jupiter always gets 60.

**4. Abda (year lord) 15, Masa (month lord) 30, Vara (weekday lord) 45, Hora (hour lord) 60** [SAR for the values]
- Vara lord: weekday reckoned sunrise to sunrise.
- Hora lord: 24 horas from sunrise; first hora = weekday lord; each next = next in the order Sun → Venus → Mercury → Moon → Saturn → Jupiter → Mars (repeat).
- Abda and Masa lords [MEM-BPHS/Raman, verify]: with ahargana A (days elapsed from the Surya-siddhantic creation epoch, as tabulated by Raman): year lord = weekday number `((floor(A/360) × 3) + 1) mod 7`, month lord = `((floor(A/30) × 2) + 1) mod 7`, counted from Sunday = 1 (0 → Saturday). I.e. the lords of the weekday on which the running 360-day "year" and 30-day "month" began. Some software instead uses the weekday lord of the solar year start (Mesha sankranti) and of the solar month start (latest sankranti) or lunar month start. These give different lords; label which is used.

**5. Ayana bala** [MEM-Raman]
`ayana = (23°27' ± δ) / (46°54') × 60`, δ = planet's declination (kranti).
- Sun, Mars, Jupiter, Venus: use +δ for north declination, −δ for south.
- Moon, Saturn: opposite (south declination adds).
- Mercury: always add |δ|.
- Sun's ayana bala is doubled.
(Older texts use 24° instead of 23°27'.)

**6. Yuddha bala** (planetary war) [SAR; MEM-Raman]
Only among Mars, Mercury, Jupiter, Venus, Saturn, when two are within 1° of longitude. Take the difference between the two planets' strength accumulated so far (Sthana + Dig + Kala through Hora bala); divide by the difference of their apparent disc diameters (Raman's bimba values: Mars 9.4", Mercury 6.6", Jupiter 190.4", Venus 16.6", Saturn 158.0"); add the result to the victor's Kala bala and subtract it from the loser's. [SAR] simplifies to "transfer the difference". Victor: see section E2.

### A4. Cheshta bala (motional) [MEM-Raman]

- Sun: cheshta = its Ayana bala. Moon: cheshta = its Paksha bala (undoubled values in Raman).
- Mars..Saturn: `cheshta_kendra = sighrocha − (mean_longitude + true_longitude)/2`; reduce to 0–180 (if >180, subtract from 360); `cheshta = cheshta_kendra / 3`.
  - Sighrocha of Mars, Jupiter, Saturn = mean Sun.
  - For Mercury and Venus: mean_longitude = mean Sun, sighrocha = the planet's own heliocentric mean longitude.
- Effect: maximal (≈60) at the middle of retrogression (opposition / inferior conjunction), minimal near superior conjunction (combust, fast direct).
- BPHS 27 alternative by eight motion types [MEM-BPHS, verify]: vakra (retrograde) 60, anuvakra 30, vikala (stationary) 15, manda 30, mandatara 15, sama 7.5, chara 45, atichara 30.

### A5. Naisargika bala (natural, fixed) [MEM-BPHS]

Sun 60.00, Moon 51.43, Venus 42.86, Jupiter 34.29, Mercury 25.71, Mars 17.14, Saturn 8.57 (= 60 × k/7).

### A6. Drik bala (aspectual) [MEM-BPHS ch. 26 + Raman; verify the special-aspect handling]

Aspect value (drishti, 0–60 virupas) of aspecting planet P on aspected point Q, with `d = (Q − P) mod 360`:

| d (degrees) | value |
|---|---|
| 0–30 | 0 |
| 30–60 | (d − 30) / 2 |
| 60–90 | (d − 60) + 15 |
| 90–120 | (120 − d) / 2 + 30 |
| 120–150 | 150 − d |
| 150–180 | (d − 150) × 2 |
| 180–300 | (300 − d) / 2 |
| 300–360 | 0 |

Special aspects (Raman's additive form): Mars +15 when d is in 90–120 or 210–240; Jupiter +30 when d is in 120–150 or 240–270; Saturn +45 when d is in 60–90 or 270–300. (BPHS ch. 26 gives separate piecewise formulas for these three; outputs differ slightly at range edges.)

`Drik bala of Q = ( Σ aspects from benefics − Σ aspects from malefics ) / 4`; Raman adds the aspects of Mercury and Jupiter in full (not quartered). Can be negative.

### A7. Required minimum strength [SAR, confirmed]

| Planet | Rupas | Virupas |
|---|---|---|
| Sun | 6.5 | 390 |
| Moon | 6.0 | 360 |
| Mars | 5.0 | 300 |
| Mercury | 7.0 | 420 |
| Jupiter | 6.5 | 390 |
| Venus | 5.5 | 330 |
| Saturn | 5.0 | 300 |

These are the BPHS ch. 27 figures; Raman uses the same. Component minima (BPHS, [SAR]):

| Group | Sthana | Dig | Kala | Cheshta | Ayana |
|---|---|---|---|---|---|
| Sun, Jupiter, Mercury | 165 | 35 | 50 | 112 | 30 |
| Moon, Venus | 133 | 50 | 30 | 100 | 40 |
| Mars, Saturn | 96 | 30 | 40 | 67 | 20 |

Report "Shadbala ratio" = total / required. >1 strong, <1 weak. Rank the seven planets by ratio, not by raw total (the minima differ).

### A8. Ishta and Kashta phala [MEM-BPHS/Raman]

`Ishta = sqrt(Uchcha bala × Cheshta bala)`; `Kashta = sqrt((60 − Uchcha) × (60 − Cheshta))`. Both 0–60. Ishta > Kashta: the planet's dasha tends to give its good results more easily; Kashta > Ishta: results come with strain.

### A9. How to interpret Shadbala

- Shadbala measures **capacity to act**, not whether the action is benign. A strong functional malefic harms forcefully; a strong benefic delivers. Decide good/bad from lordship, placement and yogas first; use Shadbala for "how much / how reliably".
- Low ratio (<1): the planet's significations and the houses it owns under-deliver, need outside support, and its dasha is hesitant or dependent on the dispositor and aspecting planets.
- High ratio (>1.2 or so): the planet dominates its dasha; its natural significations are prominent in the life.
- Read components separately: high Sthana = secure status/resources; high Dig = right direction/placement in life; high Kala = good timing/luck; high Cheshta = drive and effort (retrogrades score high); high Drik = supported by others, negative Drik = opposed.
- Strongest planet overall often describes the dominant temperament; compare with lagna lord strength.
- Ishta/Kashta refine dasha quality as in A8.

---

## B. Bhava bala [MEM-Raman, *Graha and Bhava Balas*; verify]

`Bhava bala = Bhavadhipati bala + Bhava Dig bala + Bhava Drishti bala` (+ Raman's occupancy and day/night adjustments).

1. **Bhavadhipati bala** = total Shadbala of the house lord.
2. **Bhava Dig bala** — depends on the class of the sign on the house, 60 at the strongest house, falling 10 per house away to 0 at the opposite house: `60 − 10 × circular_distance(house, strongest_house)` with distance 0..6.
   - Nara (human) signs — Gemini, Virgo, Libra, Aquarius, first half of Sagittarius: strongest as 1st house.
   - Chatushpada (quadruped) — Aries, Taurus, Leo, first half of Capricorn, second half of Sagittarius: strongest as 10th.
   - Jalachara (watery) — Cancer, Pisces, second half of Capricorn: strongest as 4th.
   - Keeta — Scorpio: strongest as 7th.
3. **Bhava Drishti bala** — aspect values (table A6) of each planet on the house midpoint; benefic aspects positive, malefic negative; total divided by 4, with Mercury's and Jupiter's taken in full.
4. Raman's extras: a bhava occupied by Jupiter or Mercury +60; occupied by Saturn, Mars or Sun −60; sirshodaya signs (Gemini, Leo, Virgo, Libra, Scorpio, Aquarius) +15 for day birth; prishtodaya signs (Aries, Taurus, Cancer, Sagittarius, Capricorn) +15 for night birth; Pisces (ubhayodaya) +15 at twilight.

Interpretation: rank the 12 houses; the strongest houses are the life areas that work with least effort, the weakest need the most. No fixed classical minimum; Raman treats roughly 7–8 rupas as average.

---

## C. Vimshopaka bala (BPHS ch. 16, "20-point strength") [MEM-BPHS; weights re-derived to sum to 20]

`Vimshopaka = Σ_vargas weight × (dignity_points / 20)`; result 0–20.

| Varga | Shadvarga (6) | Saptavarga (7) | Dashavarga (10) | Shodashavarga (16) |
|---|---|---|---|---|
| D1 Rasi | 6 | 5 | 3 | 3.5 |
| D2 Hora | 2 | 2 | 1.5 | 1 |
| D3 Drekkana | 4 | 3 | 1.5 | 1 |
| D4 Chaturthamsa | – | – | – | 0.5 |
| D7 Saptamsa | – | 2.5 | 1.5 | 0.5 |
| D9 Navamsa | 5 | 4.5 | 1.5 | 3 |
| D10 Dasamsa | – | – | 1.5 | 0.5 |
| D12 Dwadasamsa | 2 | 2 | 1.5 | 0.5 |
| D16 Shodasamsa | – | – | 1.5 | 2 |
| D20 Vimsamsa | – | – | – | 0.5 |
| D24 Chaturvimsamsa | – | – | – | 0.5 |
| D27 Bhamsa | – | – | – | 0.5 |
| D30 Trimsamsa | 1 | 1 | 1.5 | 1 |
| D40 Khavedamsa | – | – | – | 0.5 |
| D45 Akshavedamsa | – | – | – | 0.5 |
| D60 Shashtiamsa | – | – | 5 | 4 |
| **Total** | 20 | 20 | 20 | 20 |

Dignity points (out of 20): own sign (and moolatrikona/exaltation in most software) 20; great friend 18; friend 15; neutral 10; enemy 7; great enemy 5.
BPHS reading of the total: 0–5 no good result, 5–10 little, 10–15 medium, 15–20 full. BPHS also says a planet below 5 cannot give its dasha results well. Vimshopaka is the best single number for "is this planet comfortable across the divisional charts"; use it beside Shadbala (which is mostly D1/astronomical).

---

## D. Avasthas (BPHS ch. 45) [BPHS45, PVR — both read online and they agree]

### D1. Baladi (age) avasthas — v. 3–4

| Odd sign | Even sign | State | Result fraction |
|---|---|---|---|
| 0–6° | 24–30° | Bala (infant) | 1/4 |
| 6–12° | 18–24° | Kumara (youth) | 1/2 |
| 12–18° | 12–18° | Yuva (adult) | full |
| 18–24° | 6–12° | Vriddha (old) | negligible |
| 24–30° | 0–6° | Mrita (dead) | nil |

### D2. Jagradadi (alertness) — v. 5–6
- Jagrat (awake): own or exaltation sign → full results.
- Swapna (dreaming): friend's or neutral's sign → medium.
- Sushupti (asleep): enemy's or debilitation sign → nil/negligible.

### D3. Deeptadi (mood), 9 states — v. 7–10
Deepta: exalted. Swastha: own sign. Mudita/Pramudita: great friend's sign. Shanta: friend's sign. Deena: neutral's sign. Duhkhita: enemy's sign. Vikala: conjunct a malefic. Khala: great enemy's sign per the BPHS reading ([PVR] words it "a malefic's sign"). Kopa/Kopita: combust.
(The online ch. 45 text names only eight; [PVR] lists all nine as above.) Results follow the name: deepta = fame and success, swastha = comfort, mudita = happiness, shanta = calm/steady gains, deena = dejection, duhkhita = sorrow, vikala = disability/disturbance, khala = quarrel and loss, kopa = anger, loss through authority.

### D4. Lajjitadi, 6 states — v. 11–18, results v. 19–29
- **Lajjita** (ashamed): in the 5th house AND conjunct Rahu, Ketu, Sun, Saturn or Mars.
- **Garvita** (proud): in exaltation or moolatrikona.
- **Kshudhita** (hungry): in an enemy's sign, OR conjunct/aspected by an enemy, OR conjunct Saturn.
- **Trishita** (thirsty): in a watery sign, aspected by an enemy/malefic, with no benefic aspect.
- **Mudita** (delighted): in a friend's sign, OR conjunct/aspected by a friend/benefic, OR conjunct Jupiter. ([PVR] words the last clause as "and"; BPHS45 reads "or".)
- **Kshobhita** (agitated): conjunct the Sun AND aspected/conjoined by a malefic or aspected by an enemy.

Results: Garvita and Mudita planets strengthen their house (property, status, gains, happiness). The house holding a Kshudhita or Kshobhita planet is damaged. Lajjita, Kshudhita or Kshobhita in the 10th: persistent career difficulty. Lajjita in the 5th: trouble regarding children. Kshobhita or Trishita in the 7th: harm to spouse/marriage. Trishita: loss through one's own people, illness through bad associations.

### D5. Shayanadi (12 activity states) — v. 30–39
`index = ((C × P × A) + M + G + L) mod 12` (0 → 12), where C = planet's nakshatra number (Ashwini 1), P = planet number (Sun 1, Moon 2, Mars 3, Mercury 4, Jupiter 5, Venus 6, Saturn 7, Rahu 8, Ketu 9), A = navamsa number within the sign (1–9), M = Moon's nakshatra number, G = ghati of birth running from sunrise (1–60), L = lagna sign number (Aries 1).
States: 1 Shayana, 2 Upavesana, 3 Netrapani, 4 Prakashana, 5 Gamana, 6 Agamana, 7 Sabha, 8 Agama, 9 Bhojana, 10 Nrityalipsa, 11 Kautuka, 12 Nidra.
Sub-state: `((index² + name_syllable_number) mod 12 + planet_add) mod 3`; planet_add: Sun 5, Moon 2, Mars 2, Mercury 3, Jupiter 5, Venus 3, Saturn 3, Rahu 4, Ketu 4; remainder 1 = Drishti (medium), 2 = Cheshta (full), 0 = Vicheshta (little). Needs the first syllable of the name (table in [PVR] Table 37) — low priority to implement.

---

## E. Special conditions

### E1. Combustion (astangata)
Orbs = angular distance from the Sun, traditional figures from **Surya Siddhanta** (repeated by most authors; BPHS itself names the condition but gives no degree table). Read at https://www.onlinejyotish.com/free-astrology/astrology-lessons/lesson_148.php

| Planet | Direct | Retrograde |
|---|---|---|
| Moon | 12° | – |
| Mars | 17° | 17° |
| Mercury | 14° | 12° |
| Jupiter | 11° | 11° |
| Venus | 10° | 8° |
| Saturn | 15° | 15° |

Variants in circulation: Mercury 13°, Venus 9° (some modern lists); some authors treat only within ~3–5° as "deep" combustion and the outer band as mild. Rahu/Ketu are never combust. Interpretation: the planet's own significations and its karaka matters are obscured or dependent on the Sun's agenda; house lordship results still occur but with less visible credit. Mercury is so often combust that most authors discount it. Deep combustion plus weak dignity is the real problem case.

### E2. Planetary war (graha yuddha)
Condition: two of Mars, Mercury, Jupiter, Venus, Saturn within 1° of longitude [SAR]. Sun and Moon (and nodes) never take part.
Victor — sources disagree:
- Surya Siddhanta tradition: the planet with greater northern latitude / the brighter and larger disc wins; Venus is generally victor.
- [SAR]: the planet with the higher longitude wins.
- Some software (Jagannatha Hora option): lower longitude wins.
Default suggestion: north latitude rule, expose as config, report both planets' latitudes. The loser's significations and houses suffer in its dasha; the victor absorbs the strength (Yuddha bala, A3.6).

### E3. Retrograde (vakri) interpretation
- Shadbala: retrogression raises Cheshta bala (A4) — the planet is close to Earth and bright.
- Saravali and Phaladeepika tradition: a retrograde planet is strong like an exalted one even in a poor sign; retrograde benefics give strong good results, retrograde malefics strong trouble.
- Uttara Kalamrita tradition: a retrograde planet in exaltation behaves as if debilitated and a retrograde debilitated planet as if exalted.
- Working rule for the engine: treat retrograde as "strength up, behaviour unconventional/delayed/returning"; do NOT flip dignity automatically; state the Uttara Kalamrita reversal only as an alternative reading. Chapter references for these three texts were not re-read here.

### E4. Gandanta
Junction of water and fire signs, which is also a nakshatra junction: Pisces/Aries (Revati/Ashwini), Cancer/Leo (Ashlesha/Magha), Scorpio/Sagittarius (Jyeshtha/Mula).
- Wide definition: last 3°20' of the water sign and first 3°20' of the fire sign (one pada each side).
- Narrow definitions used in practice: within 1° either side, or 0°48' (2 ghatis of the nakshatra) each side.
Applies to Moon (nakshatra gandanta), lagna (lagna gandanta), and by extension planets. BPHS treats gandanta birth among the inauspicious births needing shanti (see rectification-and-panchanga.md). Flag severity by band: within 1° = strong, 1°–3°20' = mild.

### E5. Pushkara navamsa and Pushkara bhaga
Read at https://gkayapilla.blogspot.com/2020/08/pushkara-namamsha-and-bhaga.html (cites Jataka Parijata 1.58 and C.S. Patel, *Navamsa and Nadi Astrology*). **Jataka Parijata 1.58 was then read in the Sanskrit (12 Nov 2026) and its letter-number code decoded: the twelve degrees in the first column below are confirmed exactly** (`kb/sources/jataka-parijata/`).

Pushkara navamsa (two per sign, by element):

| Signs | Degree ranges | Navamsa signs |
|---|---|---|
| Fire: Aries, Leo, Sagittarius | 20°00'–23°20' and 26°40'–30°00' | Libra, Sagittarius |
| Earth: Taurus, Virgo, Capricorn | 6°40'–10°00' and 13°20'–16°40' | Pisces, Taurus |
| Air: Gemini, Libra, Aquarius | 16°40'–20°00' and 23°20'–26°40' | Pisces, Taurus |
| Water: Cancer, Scorpio, Pisces | 0°00'–3°20' and 6°40'–10°00' | Cancer, Virgo |

(The source prints the second fire range as "26 deg to 30"; the navamsa boundary is 26°40'.) Rule of thumb: the pushkara navamsas are the navamsas ruled by Venus, Jupiter (Pisces/Sagittarius), Moon and Mercury (Virgo) as listed — 24 in all.

Pushkara bhaga (single degree per sign):

| Sign | Jataka Parijata 1.58 (confirmed from the Sanskrit) | C.S. Patel set |
|---|---|---|
| Aries | 21 | 21 |
| Taurus | 14 | 14 |
| Gemini | 18 | 24 |
| Cancer | 8 | 7 |
| Leo | 19 | 21 |
| Virgo | 9 | 14 |
| Libra | 24 | 24 |
| Scorpio | 11 | 7 |
| Sagittarius | 23 | 21 |
| Capricorn | 14 | 14 |
| Aquarius | 19 | 24 |
| Pisces | 9 | 7 |

The element-based set (fire 21, earth 14, air 24, water 7) is the one most software uses. "Degree N" is usually read as the N-th degree, i.e. (N−1)°00' to N°00'; some read it as N°. Use a ±1° tolerance and report which set matched. A planet in pushkara navamsa/bhaga is nourished: it gives its good results more readily and softens affliction.

### E6. Mrityu bhaga (fatal degrees)
Table read at https://astrobix.com/learn/400-fatal-planetary-positions-in-vedic-astrology.html (the page does not name its text; the same table is normally attributed to Jataka Parijata / Sarvartha Chintamani). **Checked 12 Nov 2026: Jataka Parijata ch. 1 has one such list only (1.57), for the Moon alone - 8, 25, 22, 22, 21, 1, 4, 23, 18, 20, 20, 10 - and it is not the Moon column below. The attribution to that text is not supported; treat this whole table as source-unidentified and low confidence.** Degree within the sign:

| Sign | Lagna | Sun | Moon | Mars | Merc | Jup | Ven | Sat | Rahu | Ketu | Mandi |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Aries | 1 | 20 | 26 | 19 | 15 | 19 | 28 | 10 | 14 | 8 | 23 |
| Taurus | 9 | 9 | 12 | 28 | 14 | 29 | 15 | 4 | 13 | 18 | 24 |
| Gemini | 22 | 12 | 13 | 25 | 13 | 12 | 11 | 7 | 12 | 20 | 11 |
| Cancer | 22 | 6 | 25 | 23 | 12 | 27 | 17 | 9 | 11 | 10 | 12 |
| Leo | 25 | 8 | 24 | 28 | 9 | 6 | 10 | 12 | 24 | 21 | 13 |
| Virgo | 2 | 24 | 11 | 28 | 18 | 4 | 13 | 16 | 23 | 22 | 14 |
| Libra | 4 | 16 | 26 | 14 | 20 | 13 | 4 | 3 | 22 | 23 | 8 |
| Scorpio | 23 | 17 | 14 | 21 | 10 | 10 | 6 | 18 | 21 | 24 | 18 |
| Sagittarius | 18 | 22 | 13 | 2 | 21 | 17 | 27 | 28 | 10 | 11 | 20 |
| Capricorn | 20 | 2 | 25 | 15 | 22 | 11 | 12 | 14 | 20 | 12 | 10 |
| Aquarius | 10 | 3 | 5 | 11 | 7 | 15 | 29 | 13 | 18 | 13 | 21 |
| Pisces | 10 | 23 | 12 | 6 | 5 | 28 | 19 | 15 | 8 | 14 | 22 |

Known variant cells (other printed tables, from recall): Mars in Leo 29, Mercury in Leo 8, Lagna in Aquarius 24. Treat those three cells as uncertain. Use ±1° orb. Interpretation: a planet on its mrityu bhaga is fragile for health and for the houses it owns/occupies, mainly when also otherwise afflicted; it is a supporting factor, never a standalone death indication.

### E7. Vargottama
Planet (or lagna) in the same sign in D1 and D9. Occurs in the first navamsa of movable signs (0°–3°20'), the middle (5th) navamsa of fixed signs (13°20'–16°40'), the last navamsa of dual signs (26°40'–30°). Gives strength and consistency comparable to own-sign placement; a debilitated vargottama planet is consistently weak rather than rescued (authors differ — state both).

### E8. Sandhi
- Rasi sandhi: within about 1° of a sign boundary (first or last degree). Planet is unsettled; results weak, especially at 29°+ (also check Mrita avastha, gandanta).
- Bhava sandhi applies to unequal house systems (Sripati/KP); with whole-sign houses it coincides with rasi sandhi.
- Nakshatra sandhi / dasha sandhi: see dasha-systems.md.

---

## Implementation notes

- Keep every component in virupas as floats; convert to rupas only for display. Store component breakdown per planet.
- Arc helper: `arc(a,b) = min((a−b) mod 360, (b−a) mod 360)`.
- Dig bala needs true Asc and MC degrees even though houses are whole-sign. MC is not Asc+270 at most latitudes; compute it. At high latitudes be explicit.
- Kendradi bala with whole-sign houses uses sign distance from lagna sign. Raman used bhava-chalit (Sripati) houses; results differ when a planet is near a sign edge.
- Nathonnata/Tribhaga/Hora need true local sunrise, sunset, apparent noon (equation of time). Define sunrise convention once (upper limb with refraction vs centre of disc) and reuse it across panchanga, hora, tribhaga, Shayanadi ghati.
- Births before sunrise belong to the previous Vedic weekday for Vara and Hora lords.
- Paksha bala: Mercury's benefic/malefic status depends on conjunction (same sign) with a natural malefic; decide whether waning Moon counts as malefic for that test.
- Ayana bala needs declination (ecliptic latitude included). Cheshta bala needs mean longitudes and, for Mercury/Venus, heliocentric mean longitude; Swiss Ephemeris gives heliocentric true longitude, so mean elements must come from formulae. A common approximation is to scale by speed relative to mean speed; label it as approximate if used.
- Abda/Masa lords: the ahargana-epoch method and the sankranti method differ; expose a switch; unit-test against Raman's worked example and against Jagannatha Hora output.
- Saptavargaja: two scales; D30 has no Sun/Moon lordship (only five planets own trimsamsas); D2 hora only Sun/Moon — dignity there is by relationship to Sun or Moon.
- Drik bala can be negative; do not clamp.
- Yuddha: requires Kala bala partial totals; apply after computing both planets.
- Avasthas: baladi band edges (exactly 6°, 12°…) — use half-open intervals [lo, hi). Lajjitadi conditions overlap; a planet can hold several states; store all.
- Combustion: use geocentric longitude difference; check retrograde flag for Mercury and Venus orbs.
- Mrityu bhaga / pushkara bhaga: degree-number convention (N-th degree vs N°) is ambiguous; implement with tolerance and report the distance.

## Reliability notes

- Confirmed by a page read in this session: required Shadbala minima and component minima; Uchcha, Saptavargaja (BPHS scale), Ojayugma, Kendradi values; Paksha and Tribhaga rules; Abda/Masa/Vara/Hora values; Baladi, Jagradadi, Deeptadi, Lajjitadi, Shayanadi definitions; combustion orbs; pushkara tables; mrityu bhaga table.
- From recall, not re-read (verify against Raman's *Graha and Bhava Balas* or Santhanam's BPHS ch. 26–27): Raman's Saptavargaja scale, Drekkana bala gender order, Dig bala formula, Nathonnata formula, Ayana bala formula and planet grouping, Cheshta bala procedure, disc diameters for Yuddha bala, Drik bala piecewise table and special-aspect additions, Abda/Masa lord formulas, all of Bhava bala, Vimshopaka weights (they do sum to 20 in each scheme), Naisargika values, Ishta/Kashta formulas.
- Genuinely disputed in the tradition (not just unverified): Saptavargaja scale, Moon's handling in Paksha bala, year/month lord method, planetary-war victor rule, pushkara bhaga set, retrograde dignity reversal, vargottama of a debilitated planet.
- Shadbala is a deterministic computation, so two programs should match to the virupa once conventions are aligned; mismatches almost always come from the convention switches listed above.
