# Krishnamurti Paddhati (KP)

KP is a separate system from Parashari: it uses its own ayanamsa, Placidus cusps and nakshatra sub-lords. Keep its outputs in a separate module and never mix KP cusps with whole-sign house judgements.

Sources read in this session:
- **[ROXY-KP]** https://roxyapi.com/blogs/kp-astrology-krishnamurti-paddhati-sub-lord-horary-guide
- **[DKP]** https://dekhopanchang.com/en/learn/kp-system
- **[AS-BTR]** AstroSage KP tutorial, birth time rectification: https://sites.google.com/a/astrosage.com/kpastrology/kp-learning-home/tutorial/birth-time-rectification
- **[ROXY-AY]** https://roxyapi.com/blogs/ayanamsa-lahiri-raman-kp-developers ; **[JH-AY]** https://jagannathhora.com/kp-new-ayanamsha-explained/
- **[MEM-KP]** K.S. Krishnamurti, *KP Readers* I–VI — from recall, not re-read.

---

## 1. Ayanamsa
- KP uses the **Krishnamurti ayanamsa**, based on Newcomb's precession. It is smaller than Lahiri (Chitrapaksha) by roughly **6 arc-minutes** ([DKP]; [ROXY-AY] gives a constant gap of 0.097° ≈ 5.8'; [JH-AY] "can approach 6 arc-minutes").
- Approximate values [ROXY-AY]: KP 23.76° at 2000 vs Lahiri 23.85°; KP ≈ 24.13° in 2026.
- "KP old" = values tabulated by Krishnamurti in the Readers; "KP new (KPNA)" = later recomputation with a refined precession model; "KP straight-line" = linear-rate variant. They differ by arc-seconds, which can still move a cusp across a sub boundary.
- [MEM-KP, verify]: Krishnamurti's definition takes the zero-ayanamsa year as 291 CE with Newcomb's rate (≈50.2388" per year, slowly increasing). Swiss Ephemeris offers `SE_SIDM_KRISHNAMURTI` and, in newer versions, a `KRISHNAMURTI_VP291` mode — check the constant names in the installed version.
- Effect: 6' ≈ 24 seconds of time on the ascendant; planets shift 6' too, which changes sub-lords near boundaries (smallest sub = 40'). A KP reading done with Lahiri positions is not a KP reading.

## 2. Houses
- **Placidus** cusps; the cusp is the *beginning* of the house (not the middle as in Sripati) [DKP; MEM-KP]. A planet belongs to the house whose cusp it has passed.
- Houses are unequal (roughly 25°–35° at Indian latitudes; far more at high latitudes; Placidus fails beyond the polar circles).

## 3. Sign lord, star lord, sub lord, sub-sub lord

Every longitude has four rulers:
1. **Sign lord**.
2. **Star lord** — Vimshottari lord of the nakshatra (13°20' = 800').
3. **Sub lord** — the nakshatra is cut into 9 unequal parts in Vimshottari proportion, starting with the star lord and following Vimshottari order (Ketu, Venus, Sun, Moon, Mars, Rahu, Jupiter, Saturn, Mercury, cyclic).
4. **Sub-sub lord** — each sub is cut the same way again, starting with the sub lord.

`sub length = 800' × years / 120` [ROXY-KP; arithmetic]:

| Lord | Years | Sub arc |
|---|---|---|
| Ketu | 7 | 0°46'40" |
| Venus | 20 | 2°13'20" |
| Sun | 6 | 0°40'00" |
| Moon | 10 | 1°06'40" |
| Mars | 7 | 0°46'40" |
| Rahu | 18 | 2°00'00" |
| Jupiter | 16 | 1°46'40" |
| Saturn | 19 | 2°06'40" |
| Mercury | 17 | 1°53'20" |
| Total | 120 | 13°20'00" |

Sub-sub length = `sub length × years / 120`.

**249 numbers**: 27 × 9 = 243 subs; six subs straddle a sign boundary and are counted twice, giving 249 [ROXY-KP for the 243 + 6 statement]. Worked out arithmetically here: in the three Sun-ruled stars (Krittika, U.Phalguni, U.Ashadha) the sign boundary falls 200' into the star, inside the Rahu sub; in the three Jupiter-ruled stars (Punarvasu, Vishakha, P.Bhadrapada) it falls 600' in, inside the Moon sub. In the Mars-ruled stars the boundary (400') coincides exactly with the end of the Saturn sub, so nothing is split there. Horary: the querent's number 1–249 fixes the ascendant at the start of that sub.

### Worked example
Point at **15°00' Taurus** (absolute 45°00').
- Nakshatra: index = floor(45 / 13°20') = 3 → 4th star, Rohini (40°00'–53°20'), star lord **Moon**. Sign lord Venus.
- Offset inside the star = 5°00' = 300'.
- Subs start from Moon: Moon 0'–66'40"; Mars 66'40"–113'20"; Rahu 113'20"–233'20"; Jupiter 233'20"–340'00". 300' falls in the **Jupiter** sub.
- Offset inside that sub = 300' − 233'20" = 66'40". Jupiter sub length 106'40". Sub-subs start from Jupiter: Jupiter 14'13" (0–14'13"); Saturn 16'53" (to 31'07"); Mercury 15'07" (to 46'13"); Ketu 6'13" (to 52'27"); Venus 17'47" (to 70'13"). 66'40" falls in the **Venus** sub-sub.
- Result: sign lord Venus / star lord Moon / sub lord Jupiter / sub-sub lord Venus.

```python
ORDER = ["Ketu","Venus","Sun","Moon","Mars","Rahu","Jupiter","Saturn","Mercury"]
YEARS = {"Ketu":7,"Venus":20,"Sun":6,"Moon":10,"Mars":7,"Rahu":18,"Jupiter":16,"Saturn":19,"Mercury":17}
def lords(lon, depth=3):                 # lon in degrees, KP ayanamsa applied
    span = 360/27; idx = int(lon // span); off = lon - idx*span
    out = [ORDER[idx % 9]]
    for _ in range(depth-1):
        i = ORDER.index(out[-1]); acc = 0.0
        for k in range(9):
            p = ORDER[(i+k) % 9]; seg = span * YEARS[p] / 120
            if off < acc + seg or k == 8:
                out.append(p); off -= acc; span = seg; break
            acc += seg
    return out                            # [star, sub, sub-sub]
```

## 4. Significators (four-fold hierarchy) [ROXY-KP; DKP]

For a house H, strongest to weakest:
- **A** planets in the star of an occupant of H;
- **B** occupants of H;
- **C** planets in the star of the lord of H (lord of the sign on the cusp);
- **D** the lord of H.
- (E, weaker still, [MEM-KP]: planets conjoined with or aspected by the above.)

Planet-wise reading (the direction used in practice): a planet signifies, in order, (1) houses occupied by its star lord, (2) the house it occupies, (3) houses owned by its star lord, (4) houses it owns. A planet with no planet in its stars is a strong significator of its own occupied/owned houses. Rahu and Ketu act as agents: they give the results of planets conjunct them, aspecting them, their sign lord and star lord, in preference to those planets themselves.

Core dictum [MEM-KP]: the planet is the source, the star lord shows the nature of the result (which houses), the sub lord decides whether that result is favourable or denied.

## 5. Cuspal sub lord rules

Method: take the sub lord of the principal cusp. List the houses that sub lord signifies (section 4, planet-wise). If it signifies the promise group, the event is promised; if it signifies the denial group (generally the 12th from each promise house), it is denied or spoiled. The event then occurs in the joint period (dasha–bhukti–antara) of significators of the promise houses, with transit agreement.

| Matter | Principal cusp | Promise houses | Denial / adverse houses | Source |
|---|---|---|---|---|
| Marriage | 7th | 2, 7, 11 | 1, 6, 10 (also 12) | ROXY-KP, DKP |
| Second marriage / separation | 7th (2nd for remarriage) | — | 1, 6, 10 with 12 for separation; 2 with 7, 11 again for remarriage | MEM-KP |
| Job / service | 6th and 10th | 2, 6, 10, 11 | 1, 5, 9 (12 for loss of job) | ROXY-KP |
| Career success | 10th | 2, 6, 10, 11 | 5, 8, 12 | ROXY-KP / MEM-KP |
| Business | 7th and 10th | 2, 7, 10, 11 | 5, 8, 12 | MEM-KP |
| Child birth | 5th | 2, 5, 11 | 1, 4, 10 | ROXY-KP (promise); MEM-KP (denial) |
| Foreign travel / settlement | 12th (and 9th) | 3, 9, 12 | 2, 4, 11 (return / stay home) | ROXY-KP (promise); MEM-KP |
| Property, house, vehicle | 4th | 4, 11, 12 (12 = outlay) | 3, 5, 10 | MEM-KP |
| Education | 4th (9th higher, 11th completion) | 4, 9, 11 | 3, 5, 8 | MEM-KP |
| Illness | 6th | 6, 8, 12 | — | MEM-KP |
| Cure / recovery | 6th | 1, 5, 11 | 6, 8, 12 | MEM-KP |
| Longevity | 1st | 1, 5, 9, 10, 11 | badhaka and maraka houses, 6, 8, 12 | MEM-KP |
| Money gain | 2nd and 11th | 2, 6, 11 | 5, 8, 12 | ROXY-KP |
| Borrowing a loan | 6th | 2, 6, 11 | 5, 8, 12 (repayment) | MEM-KP |
| Litigation success | 6th | 1, 6, 11 | 5, 7, 12 | MEM-KP |

Only the rows tagged ROXY-KP/DKP were confirmed on a page in this session; the rest are the standard Reader groups from recall and must be checked against KP Reader IV/VI before being quoted as authoritative.

Additional KP rules [MEM-KP]: badhaka house = 11th for movable lagnas, 9th for fixed, 7th for dual; marakas = 2nd and 7th. A sub lord that is retrograde does not deny but delays (the classic position: the cuspal sub lord should not be in the star of a retrograde planet for the promise to hold).

## 6. Ruling planets (RP) [AS-BTR; ROXY-KP]

Computed for the **moment and place of judgement** (not birth):
1. Day lord (weekday from sunrise to sunrise);
2. Moon sign lord;
3. Moon star lord;
4. Ascendant sign lord;
5. Ascendant star lord;
(+ Moon sub lord and Ascendant sub lord in later practice [ROXY-KP].)

Strength order, strongest first [AS-BTR]: Ascendant star lord > Ascendant sign lord > Moon star lord > Moon sign lord > Day lord.
Rahu/Ketu enter the list when conjunct or aspected by an RP or sitting in an RP's sign, and then take precedence over that planet. Planets in the star or sub of a retrograde planet are dropped when the list must be shortened [AS-BTR].

Use: common planets between the event's significators and the RPs are the "fruitful" significators; the event is timed to their dasha/bhukti/antara and to transits of Sun/Moon/Jupiter over the sign–star–sub positions ruled by them.

## 7. KP birth time rectification

1. **RP method** [AS-BTR]: note the RPs when the astrologer starts the rectification. The natal ascendant's sign lord, star lord and sub lord should be drawn from the RPs. Within the stated time window, choose the ascendant degree whose sign/star/sub (and sub-sub) lords are RPs, taking the strongest RPs for the higher levels.
2. **Moon–Lagna link** [MEM-KP, widely taught]: the natal ascendant's sub lord (or sub-sub lord) should be connected with the natal Moon's star lord or sign lord (same planet, or in its star, or conjunct/aspecting).
3. **Gender check** [MEM-KP]: ascendant sub-sub lord in a male sign/star for a male birth, female for a female birth (weak rule).
4. **Event check**: cusp sub lords must agree with known facts (married or not: 7th CSL; children: 5th CSL; profession: 10th CSL). A candidate time whose 7th cusp sub lord denies marriage for a married native is rejected.

What it can and cannot resolve: an ascendant sub lasts 40'–2°13' of arc, i.e. about 2.5–9 minutes of time, and a sub-sub well under a minute, so KP can *output* a time to the minute. But the RP method anchors on the moment the astrologer happens to look at the chart; it has no independent validation, and with 5–7 ruling planets out of 9 a large share of all sub positions qualify. Treat an RP-rectified time as a convention-consistent choice, not a measurement. The event check (step 4) is the only part that uses information about the native, and it discriminates only between sub lords that give different yes/no answers on known facts.

---

## Implementation notes

- Compute KP positions with the KP ayanamsa end to end (planets and cusps); do not convert Lahiri outputs by a fixed 6'.
- Placidus cusps from Swiss Ephemeris house system 'P' on the tropical ascendant/MC, then subtract the ayanamsa. Guard for latitudes above ~66°.
- Sub-lord lookup: use exact rational arithmetic or integer arc-seconds (sub lengths are whole arc-seconds: Ketu 2800", Venus 8000", Sun 2400", Moon 4000", Mars 2800", Rahu 7200", Jupiter 6400", Saturn 7600", Mercury 6800"; total 48000"). Sub-sub lengths are not whole arc-seconds; use fractions.
- Boundary sensitivity: report the distance of each cusp and planet to the nearest sub boundary, in arc-minutes and, for cusps, in seconds of clock time.
- Significator tables: build both house→planets (A–D) and planet→houses (4 levels). Occupancy uses Placidus cusps; ownership uses the sign on the cusp.
- Aspects in KP: Parashari full aspects by degree-independent sign count are used by most KP software; Krishnamurti also used Western aspects in places. Label the choice.
- Ruling planets need the place and time of the query, the local sunrise for the day lord, and the KP ayanamsa.
- The 249 table: generate programmatically by walking the zodiac sub by sub and splitting a sub at every sign boundary; assert the count is 249.

## Reliability notes

- Confirmed on pages read: Placidus use, ~6' ayanamsa gap, sub-lord proportional division, 243 + 6 = 249, four-level significators and their order, marriage/job/children/foreign/money cusp groups, the five ruling planets, their strength order and the retrograde-star pruning rule.
- From recall only: exact ayanamsa definition (291 CE, Newcomb rate), Swiss Ephemeris constant names, the E-level significator, the remaining cusp groups (property, education, illness, longevity, litigation, loans, business), badhaka rule, Moon–Lagna rectification link, gender rule.
- KP sources online are mostly secondary blogs; the KP Readers themselves were not accessible. Before publishing the cusp-rule table, check it against KP Reader VI (*Horary Astrology*) or Reader IV (*Marriage, Married Life and Children*).
- KP gives crisp yes/no outputs, which makes it testable — and also makes it sensitive to birth-time error of a few minutes. Do not present KP cuspal results for a chart whose time is uncertain by more than about 2–4 minutes without saying so.
