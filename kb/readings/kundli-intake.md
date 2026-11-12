# Kundli intake and processing — v2 (11 Nov 2026)

How any birth data or kundli document is turned into a reading. Follow the steps in order. Nothing is computed by hand any more: every factor comes from the worksheet, so nothing is missed and nothing is invented.

## Step 0 — Start the engine

```bash
cd /home/claude && git clone https://github.com/vrushabhabib/jyotish.git && cd jyotish
pip install -q ephem pytest geonamescache --break-system-packages
bash tools/install_swisseph.sh                             # optional second engine; the two agree to about 1 arc-second
python3 -m pytest -q tests                                # must be all green before any chart is trusted
```

`engine/ephemeris.py` picks Swiss Ephemeris when installed and pyephem otherwise. Both are checked against JPL Horizons in the tests. Do not write one-off position code in a chat: a hand-rolled fallback on 20 Oct 2026 read planets in the J2000 frame and put every planet 8′ off for a 1990 birth (dasha dates two months early). The tests exist so that cannot recur.

## Step 1 — Get the birth data

| Source | What to do |
|---|---|
| AstroSage PDF | `python3 -m engine.report --pdf file.pdf --out /tmp/ws` — the parser (`engine/astrosage_pdf.py`) reads birth data, planets, 16 vargas, Shadbala, Bhava Bala, Ashtakavarga, KP cusps, Jaimini karakas, dashas, and cross-checks them against our own computation. |
| Other PDF / photo of a chart | Read the birth data by eye, run the worksheet from date/time/place, then compare lagna, Moon nakshatra-pada and every planet's house with the document. |
| Date, time, place only | `python3 -m engine.report DATE TIME "Place" --name N --sex F --out /tmp/ws` looks the town up offline (towns above 15,000 people; old names such as Hubli, Bangalore, Belgaum are understood). For a village give a plus code or coordinates, or the nearest town. With coordinates: `python3 -m engine.report DATE TIME LAT LON TZ --name N --sex F|M --out /tmp/ws`. |

Record at intake: where the **time** comes from (hospital record / family memory / estimate / window), where the **date** comes from, sex, and whether the person is employed, in business, or both.

## Step 2 — Cross-check (stop if it fails)

- Lagna and every planet within **5′** of the document; a difference over 1′ is noted. Known: AstroSage's own Sun runs about 0.5′ and its Jupiter about 3′ from JPL — those two residuals are AstroSage's, not ours.
- Moon nakshatra and pada identical. Vimshottari balance within about a week.
- Sarvashtakavarga identical sign by sign (ours reproduces AstroSage exactly).
- A mismatch above 1° means wrong date, time, time zone or place. Resolve it before reading anything.

## Step 3 — Read section 1 of the worksheet first: birth-time sensitivity

The table shows the minute at which the lagna, D9, D10, D7, D12 and D3 lagnas change. Compare with how sure the time is:

- time from a record → ±2 minutes; family memory → ±15; "morning" → the whole window.
- Any lagna that changes inside that margin makes its findings **uncertain** — mark them so (◇) and keep time-proof findings (Moon, planets' signs, karakas) separate (◆).
- If the D1 lagna itself changes inside the margin, run both charts and ask discriminating questions (Step 5) before writing.

## Step 4 — Use the worksheet, section by section

| Worksheet section | Feeds |
|---|---|
| 2 Planets (dignity, D9 dignity, avastha, combust/retro/vargottama/gandanta) | strength of every statement |
| 3 Rulerships and functional nature | written out before any interpretation (protocol rule) |
| 4–5 Houses from lagna and from Moon (occupants, aspects, lord, lord's company, SAV) | every life area; the completeness checklist |
| 6 Divisional charts | Uses as Parashara states them (BPHS 7.1-8): D2 wealth, D3 siblings, D4 fortune (property is the later reading), D7 children, D9 spouse, D10 "the great result" (career, standing), D12 parents, D16 comforts and vehicles, D20 worship, D24 learning, D27 strength and weakness, D30 misfortunes, D40 and D45 good and bad in general, D60 everything |
| 7 Jaimini (karakas, arudhas, UL and its 2nd/8th, karakamsa) | spouse, image, career |
| 8 Yogas, Manglik with cancellations, Kaal Sarp, Pitru | never state a yoga without its "weakened by" column |
| 9 Ashtakavarga, Shadbala, special points, KP lords | strength, fertility points, KP confirmation |
| 10 Link test | which sub-period lords can deliver which area — strong links only |
| 11 Vimshottari with area tags and pratyantars | every dated statement |
| 12–13 Saturn phases, transits with SAV/BAV, double transit, returns | timing windows |
| 13a KP cusps, sub-lords, significators; Bhava Chalit shifts | KP confirmation of promise; planets that sit on a house border |
| 13b Yogini and Chara dashas | second and third timing systems |
| 13c Convergence table and track record | experimental cross-check of timing. Back-test 12 Nov 2026: 2 of 8 known events fell in a 4-of-5 month (career 2 of 3, marriage 0 of 3, home/property 0 of 2). Not a filter: state such windows as tentative and log them |

Added 12 Nov 2026 from the Sanskrit reading (all in sections 9 and 11, each with its verse): twenty-point strength, rays, running Sudarshana year, livelihood pointer, special lagnas, three-part combined Ashtakavarga, months to prefer and avoid, direction of the spouse, birth-time conditions, conditional star dashas; in section 11 the sub-lord's house from the dasha lord, when in its period a planet delivers (stated only where two pointers agree), and the dasha lord's own transit with its month trigger (tentative). Read `kb/sources/ANALYSIS.md` first: it says which of these the texts treat as primary and what our own cases do and do not support.

Column "How common" in section 8: a yoga found in more than 40% of random charts (Dhana 88%, Raja kendra-trikona 80%, Pitru 61%, Budha-Aditya 51%) is not mentioned as a distinction. Lead with the uncommon ones.

Take Shadbala and Bhava Bala from the PDF when one is supplied; `engine/shadbala.py` is used otherwise, and its unverified components are listed in the worksheet.

## Step 5 — Verify before reading (unchanged principle, sharper method)

Parashara's own warrant for this step (BPHS 76.18, read in the Sanskrit): "for those whose birth is unknown, the running dasha is to be known from the results being experienced" - the chart is checked against the life, not the other way round.

1. Ask 8–14 questions, one at a time, answered cold. Score hits/partly/miss in the open.
2. **70 % or more → confirmed.** Below that, say so and limit the reading to timing of periods.
3. Choose questions that discriminate:
   - between two candidate lagnas: facts that flip (younger siblings, mother's centrality, career drive);
   - within a time window: the *month* a dasha begins, matched to a sharp life change;
   - for an unrecorded date: festival/tithi memory ("the day after Ram Navami"), Saturn-phase onset months.
4. Do **not** treat "past events fall in linked sub-periods" as proof. Tested on 248 candidate dates: nearly all pass (Rule 8). Only forward statements answered cold count.

### Uncertain time: let the engine pick the questions
`python3 -m engine.discriminate DATE T0 T1 LAT LON TZ` lists the minutes at which lagna, D9, D10, D7 and the Moon's pada change inside the window, how many months the dasha starts move, and which kind of question separates the segments. Ask only those.

### Log before you send
Every dated forward statement goes into the ledger first: `python3 -m engine.ledger add --chart NAME --category timing --kind forward --statement "..." --window YYYY-MM-DD:YYYY-MM-DD --basis "..." --confidence 0.x`. When the person reports back: `python3 -m engine.ledger score ID hit|partly|miss`. `python3 -m engine.ledger report` gives the running hit rate by category; the worksheet prints it.

## Step 6 — Write

Follow `kb/readings/full-reading-protocol.md` (13 parts; block form; plain words; years; rules). For each part, open the matching `kb/life-areas/*.md` rule file and go down its checklist against worksheet sections 4–8. State evidence counts (1 = possibility, 2 = likely, 3+ = probability) and the verification score in Part 1.

## Step 7 — File

- `data/charts/<name>_<date>.json`: birth data, time confidence, verification log (question, chart said, person said, score), readings delivered. No sensitive personal history beyond what the user approves.
- Memory `/people/<name>.md`: what the user stated.
- New lesson learned from a miss → `kb/dashas/antar-event-rules.md` as a numbered rule, marked provisional until seen twice.

## Accuracy record
Kept in `data/ledger.jsonl`; print it with `python3 -m engine.ledger report`. On 12 Nov 2026: 39 questions about the past, 62% fully right (65% counting partly-right as half) - Hoang Anh 14 of 20, Saira 5 of 14, Tanzil 5 of 5. All eight "event placed in a sub-period that had no link to the area" statements were wrong; dated period statements held far better. One forward prediction is open; none has matured.
