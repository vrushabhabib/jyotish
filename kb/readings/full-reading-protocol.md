# Full Reading Protocol — the default for every chart

Status: DEFAULT. Built 4 Oct 2026 from the Hoang Anh reading (13 parts, verified against her life, errors audited). When Vrushab shares a horoscope, a PDF, or a date/time/place, produce the reading in THIS form unless he asks for something shorter. Read `kb/dashas/antar-event-rules.md` with this file.

## 0. Intake and verification (before any interpretation)
1. Extract name, sex, date, time (24h), place, lat/lon, tz, time confidence (record / memory / estimate).
2. Build the chart with the engine; cross-check lagna degree, Moon nakshatra-pada, dasha balance against any source document. >1° mismatch → stop and resolve. Take Shadbala, SAV/BAV, Bhava Bala, D7/D9/D10, Jaimini karakas, KP sub-lords from the source PDF if present. Save `data/charts/<name>_<date>.json`.
3. Compute and record: lagna distance to sign boundary (minutes of time it represents); D2 (hora) per planet from degrees; D30 (trimsamsa) per planet; waning/waxing and tithi from Sun–Moon distance; Arudha Lagna, Darapada (A7), Upapada (UL) with the 1st/7th exceptions; 2nd and 8th from UL; 7th from Moon and from Venus; 5th from Moon and from Jupiter; 10th from Venus and from Jupiter; the derived parent houses (father's wealth = 10th, mother's wealth = 5th, maternal relatives = 6th, paternal siblings = 11th).
4. Compute transits for the next 25 years (Jupiter, Saturn, Rahu/Ketu ingress dates). pyswisseph is often unavailable: use the Keplerian-elements script (±2 weeks) and SAY the tolerance. Derive Sade Sati from Saturn's ingress into 12th/1st/2nd from Moon, never from memory.
5. Verify ALL antardasha dates by arithmetic (MD years × AD lord years / 120) before quoting any. Keep one dated table and quote only from it.
6. BIRTH-TIME TEST when the lagna is near a boundary: send 4 questions where Lagna-A and Lagna-B give opposite answers (health in youth, mother, secret vs open love, contest/scholarship), plus 4 dated life periods. Let the person answer cold. Record hits and misses visibly ("chart said / you said"). Only then write the future.

## 1. Delivery form
- 13 parts, sent one at a time, each self-contained, in the person's languages (English first, then full translation; Vietnamese for Hoang Anh). Each part has three blocks: **The astrology** (every factor, named and placed) → **In plain words** (laymen, no jargon left unexplained) → **The years** (period by period, with dates) → a closing **rules for you** paragraph → "Next part: …".
- Headings are PART n. TITLE. No sub-lettering (no 10A/10B); an add-on is "PART n, ADDITION. TITLE".
- Parts: 1 How this was made and checked (verification table) · 2 Chart at a glance · 3 Nature (lagna, Moon, Sun) · 4 Past timeline (dasha-dated, for verification) · 5 Now (current MD/AD/PD + live transits) · 6 Career · 7 Money & property · 8 Health · 9 Family · 10 Marriage & love (+ addition: where the differences will be, and what holds) · 11 Children & parenthood · 12 Long view to end of next MD · 13 Uncertainties, spiritual note, remedies.
- After approval: fill the person's Claude Doc section by section, add the translation tab, export PDF. Corrections found later are sent as short standalone correction messages AND applied to the doc.

## 2. Completeness procedure (per part)
List and tick before writing: occupants of the house; lord's placement, dignity, retrogression, combustion; EVERY aspect on the house and on the lord (check Mars 4/7/8, Jupiter 5/7/9, Saturn 3/7/10, Rahu/Ketu 5/7/9 explicitly); natural karaka and its condition; Jaimini chara karaka; the same house from Moon and from Sun (and from Venus for marriage, from Jupiter for children/husband); relevant varga (D9 marriage, D10 career, D7 children, D2 wealth, D30 health); KP sub-lord; SAV/BAV bindus; cross-house links already found in earlier parts; what the master doc / people file already says. **A feature omitted is the same class of error as a feature invented.** Never tilt toward anyone; completeness, never bias.

## 3. Interpretation rules learned (all verified against life events)
- **Sambandha test for sub-periods**: a relationship is read in an AD/PD ONLY if the sub-lord occupies/owns/aspects/disposes Venus, the 7th or the 7th lord. Otherwise read that planet's own houses. No filler romance. Same logic for career (10th/10L/AmK), money (2/11), children (5/5L/Jupiter), property (4/4L).
- **Female chart husband karaka = Jupiter** (Parashari). Jaimini Darakaraka describes the spouse and times Chara dasha only; it does not trigger Vimshottari events. Jupiter retrograde as husband karaka = second-approach marriage / a man known before.
- **Sun in the 10th is the native's own authority first.** Attribute strength to the father only after checking 9L condition and whether Saturn/Sun are combust or weak. Saturn combust by the native's Sun + 9L weak = the native overtook a weaker father.
- **6th house = contest first, trouble second**: scholarships, competition, service excellence, immune response; also debt, illness, maternal relatives. Jupiter in 6th = defeats enemies; Moon in 6th = worry somatised into the gut.
- **12th house with exalted Venus** = foreign life + private/physical happiness + spending; not poverty. 7L in 12th in BOTH D1 and D9 = foreign spouse / residence abroad (probability, not possibility).
- **UL in 9th** = formal, sanctioned marriage; UL lord in 6th = contest/paperwork before marriage; 2nd from UL strong = marriage lasts; 8th from UL empty = no break. A7 on AL = partner and public image coincide.
- **Mangalya sthana (8th) for women** = marriage longevity; strong 8th with strong lord = enduring marriage, even with Rahu there.
- **Marriage timing** = double transit (Jupiter in/aspecting 7th + Saturn aspecting 7th) inside a sub-period with sambandha to Venus/7th/Jupiter. Engagement/commitment often one sub-period earlier when Jupiter aspects the UL or lagna.
- **Children timing** = double transit on the 5th inside the AD of the planet sitting in the 5th from Moon/Jupiter or ruling the 5th; Saturn with the 5L = late (35+); Rahu on D7 lagna/5th + Jupiter in 6th = medical route / foreign birth. Moon+Mars in D7 12th = supervise pregnancy, say so plainly without fear-mongering.
- **Health**: D30 portions (Mars = heat/surgery/inflammation; Venus = hormonal/reproductive; Jupiter = protective/liver; Saturn = chronic); weakest planet names the soft point; Sade Sati peak = the don't-push-through period. Give regime, not diagnosis.
- **Money**: D2 hora count (Sun = self-earned, Moon = received); 2L/11L link; 5th for speculation; 8th Rahu = in-laws/inheritance; 4th condition for property timing. Separate accounts if Ketu 2nd + Rahu 8th.
- **Family**: dasha change at a childhood age often matches a confirmed life event (e.g. fostered until the Mars→Rahu change at 4y10m). Check the childhood dasha boundaries against what the person reports.
- **Dates**: never shift birth time to rescue an interpretation. Keep internal consistency across parts (grep earlier parts before writing new ones). Quote Saturn/Jupiter/Rahu returns and nodal returns where they fall.

## 4. Honesty and purity rules
- State the error rate from the verification round and say it applies forward.
- Least reliable: sex of a child; another person's character read from this chart alone. Say so.
- **Purity**: a reading sent to a third person describes THEIR chart only — never Vrushab's situation, current events between them, or his hopes. No tilting. A caught tilt destroys trust.
- Health lines are tendencies for a doctor, remedies are tradition, nothing replaces medicine/law/conversation.
- Don't predict death; say longevity indicators are strong/weak and stop.
- Spiritual beliefs the person states (e.g. a patron deity, dream realms): map the placements that carry them (Ketu/Rahu axis, 12th, 8th, Moon+Jupiter, D9 Jupiter in 8th, Uttara Bhadrapada etc.) respectfully; the chart confirms the person built to hold the story, not the story.

## 5. Remedies by lagna (never by Moon sign)
- Strengthen the weakest functional-benefic planet first; recommend at most one stone; forbid stones for maraka lords and for combust Saturn; pacify Saturn by service; Rahu remedy = plainness (ask, don't investigate); Ketu in 2nd remedy = speak before writing; Jupiter = respect for a teacher/elder; weekday observances listed per planet. Repeat the practical rules from each part once in Part 13.

## 6. Audit log of mistakes made (so they are not repeated)
- Filler romance in unlinked sub-periods (6 misses). · 6th read only as illness. · "first job" after "first employment" (inconsistency). · Invented specifics ("trip alone", "visa"). · Jupiter transit sign wrong (Mithuna vs Karka) from memory. · Sade Sati dates from memory (2034–41) instead of computed (2036–43). · Saturn–Ketu AD dates misquoted. · "Father's standard" from Sun+Saturn in 10th (she overtook a weaker father). · "Venus exalted in D9" carried from a wrong summary (D9 Venus was Vrishchika 12th). · Referenced the client's current personal events in her reading (purity breach). · Sub-lettered parts (10B) confusing to the reader.
