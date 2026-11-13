# Antardasha event rules — what a sub-period can and cannot deliver

Added 4 Oct 2026 after a 20-line verified timeline (Hoang Anh, b. 1993) scored 14 hits / 6 misses.
Every miss broke one of the rules below. Every hit obeyed them. These rules are mandatory before any
dated prediction is written.

## Rule 1 — Sambandha test (connection test)
An antar (sub-period) lord delivers an event in a life area ONLY if it has sambandha with that area's
house, house lord or karaka. Sambandha = any of:
- occupies the house
- owns the house
- conjoins the house lord or karaka
- aspects the house, its lord or its karaka (full aspect; Mars 4/7/8, Jupiter 5/7/9, Saturn 3/7/10, others 7th only)
- disposes the house lord or karaka (they sit in its sign)
- is the nakshatra lord of the house lord / karaka (KP-style, secondary)

No sambandha → that antar gives results of the lord's OWN houses and placement, nothing else.
Never borrow an event from the neighbouring antar. A relationship in antar N does not imply one in antar N+1.

Verified on the test chart (Aries lagna, Venus 12th = 7L, Jupiter husband karaka in 6th):
| Antar | Link to Venus / 7th / Jupiter | Predicted | Actual |
|---|---|---|---|
| Rahu–Venus | Venus itself | relationship | yes |
| Rahu–Sun | none (Sun 10th, aspects 4th) | relationship | NO — study/career only |
| Rahu–Moon | Moon 6th aspects 12th (Venus) — weak | heartbreak | partial — friendship quarrel only |
| Rahu–Mars | none (Mars 3rd aspects 6/9/10) | someone returns | NO — independence, effort |
| Jup–Jup | Jupiter = husband karaka, aspects Venus | sincere relationship | yes |
| Jup–Sat | Saturn aspects 7th AND Venus | marriage talk | yes |
| Jup–Mer | none (Mercury 11th aspects 5th) | online relationship | NO — job move to global agency (11th) |
| Jup–Ketu | Ketu in Venus's sign (disposed by 7L) | ending | yes |
| Jup–Venus | Venus itself | foreign partner | yes |

Weight of link: occupancy/ownership/conjunction = strong; aspect from a strong planet = strong; aspect
from the chart's weakest planet (Shadbala rank last) = weak, needs a second link or a transit trigger.

## Rule 2 — Karakas by gender
- Woman's chart: husband karaka = JUPITER. Venus = her own desire/attractiveness, still 7L if it owns the 7th.
- Man's chart: wife karaka = VENUS.
- Mercury is NEVER a spouse karaka. (Error made once; do not repeat.)
- Father = Sun (and 9th), mother = Moon (and 4th), siblings = Mars (and 3rd), children = Jupiter (and 5th).

## Rule 3 — Read the 6th house as contest first
The 6th is illness, debt, enemies — AND competition, service, exams, scholarships, employment, winning
against rivals. A benefic (Jupiter) or a vargottama planet in the 6th tilts it to "defeats enemies" (Viparita
flavour). Health lines held on the test chart; "setback / dropout / obstacle" lines failed while the native
was winning scholarships and topping her class.

## Rule 4 — No invented specifics
Write the house meaning and stop. 12th = foreign/travel/private; do not add "alone". 11th = network/
gains; do not add "visa". 7th by Saturn = older/serious partner; do not add a profession. Specifics the
chart cannot carry are the first things a sceptical native will mark false.

## Rule 5 — Internal consistency
Before sending a timeline, reread it top to bottom. "First employment" cannot appear in two periods.
A pattern stated at the end ("five or six relationships") must equal the count in the lines above.

## Rule 6 — Timing is Moon-based; do not shift birth time to fix interpretation
Dasha boundaries and transits over the Moon do not move with ±10 min of birth time. If dates land and
meanings miss, the fault is interpretation (Rules 1–5), never the clock. Shift the lagna only when
lagna-dependent facts (health from 6th, mother from 4L, secret vs open love from Venus's house) fail.

## Rule 7 — Verification protocol (what worked)
1. Cast both candidate lagnas when birth time is within 15 min of a sign boundary.
2. Ask 3–4 questions where the two lagnas give OPPOSITE answers (never Moon-based facts, which hold in both).
3. Then send dated periods, ages first, and let the native answer cold.
4. Keep misses visible in the native's copy ("chart said / you said"). Honesty is what buys trust for the future sections.
5. Score: ≥70% hits with zero timing misses = chart confirmed; proceed to future. Record misses here.

## Rule 8 — Sambandha cannot rectify a birth DATE (tested 20 Oct 2026)
Test: one native, home birth, no record. 11 dated life events + 4 transit checks + 6 static facts scored with one fixed
rubric on 248 candidate charts (every day ±30 days, four times in the 9–10am window). Median 13.5/18, recorded date 15/18
(top ~7%), best 15.5/18 — half a point, i.e. noise. Almost any date "links" its sub-period lords to the event's house,
because each planet owns/occupies/aspects/disposes several houses. Consequences:
- Do NOT say "the timing works" because the events fell in linked sub-periods after the fact. That passes for most dates.
- The real accuracy measure is forward predictions answered cold (here 5/14 = 36%).
- To rectify a date, use facts that change sharply with the Moon: festival/tithi memory (e.g. "day after Ram Navami"),
  Sade Sati/Ashtama Shani onset months, nakshatra-based dasha START months matched to a sharp life change.

## Rule 9 — Lessons from the same case (misses turned into rules, single case: treat as provisional)
- Ketu in the 3rd + Saturn and Mars aspecting the 3rd = no younger siblings (native was youngest of four), even with an
  own-sign Moon in the 3rd. Do not let one dignified occupant outvote three malefic influences.
- Injury location: read the HOUSE that Mars and Saturn both afflict (3rd = arms/shoulders), not the sign Mars sits in.
- A Ketu mahadasha that follows a loss reads as quiet and withdrawn (living with family, no new relationship). Do not
  assign events to Ketu antardashas from transits alone — two forecast events in that period both failed.
- A sub-lord conjunct the 7th lord can deliver marriage even when it is also the career lord (9L+10L Saturn conjunct
  7L Mars gave marriage, not a first job). List every area the sub-lord links to before choosing one.
- Spouse's age: Saturn with the 7th lord predicted an older husband; the second husband was 4 years younger.
  Second marriage may need the 2nd house (8th from 7th) as well as the 7th. Unresolved.

## Rule 10 — The calculator is checked before the chart is (added 11 Nov 2026)
A reading is only as good as its positions. On 20 Oct 2026 a fallback calculator written in the chat read planets in the wrong reference frame. Every planet was 8 arc-minutes off for a 1990 birth, and every dasha date about two months early. The check made at the time ("within 3 arc-minutes of AstroSage", "ingress dates match") was too loose to catch it.
- Run `python3 -m pytest -q tests` at the start of every session. The tests compare the engine with JPL Horizons and a printed AstroSage chart.
- A cross-check passes at 1 arc-minute for planets, not 3. Above that, find the reason.
- Eight arc-minutes of Moon equals two months of Vimshottari. Any statement dated to the month depends on the Moon to the minute of arc and on the birth time to about four minutes of clock time. Say so.

## Rule 11 — A timing method is trusted only after a back-test (added 12 Nov 2026)
The five-system convergence vote (Vimshottari main and sub lord, Yogini, Chara, Jupiter-Saturn double transit) looked rigorous. Tested on the eight dated past events on file, a 4-of-5 month caught 2 and missed 6 (career 2 of 3, marriage 0 of 3, home/property 0 of 2). One of the two charts is unconfirmed and eight events prove little either way, but the method has NOT earned the right to veto or to date anything alone.
- Every new timing method gets `engine.convergence.backtest` on known events before it is used in a reading; counts are stored in `data/`.
- Agreement between systems that share inputs (Vimshottari and Yogini both start from the Moon's nakshatra) is not independent confirmation.
- Shadbala (12 Nov): settled against two references. Mercury's Saptavargaja, the Hora lord and the dwadasamsa boundaries follow Raman's worked example exactly; AstroSage deviates on all three. The Moon's paksha bala is doubled (Raman, BPHS).


## Rule 12 — A sub-lord joined to Rahu is not read on its strength alone (added 13 Nov 2026, one case: provisional)
First miss of the rebuilt system. A sub-period of the 4th and 11th lord, second in Shadbala, in a friend's sign and well placed from the dasha lord, was read as "earnings improve and the home base changes". The person reported the opposite for earnings; the move came a year later.
What was skipped: the sub-lord sat within about 3 degrees of Rahu, and the texts say a planet joined to Rahu does not give good in its period (Jataka Parijata 18.28 - rule 13 in `dasha-systems.md`); Saturn was also in the 8th from the Moon for most of the period.
- Before reading the good side of a sub-lord's houses, check rule 13 of `dasha-systems.md` (debilitated, joined to a debilitated planet, joined to Rahu). If it applies, state the houses as the subject and do not promise the gain.
- Strength (Shadbala rank) decides how much a planet can do, not whether a planet tied to Rahu does it cleanly.
- One case only. Counts for and against go in the ledger; drop this rule if later cases contradict it.

## Rule 13 — Movable significators are shown in the link test, not yet counted (added 13 Nov 2026, under test)
The link test counts houses, their lords and the fixed significators. A sibling's birth fell in the sub-period of a planet with no such link to the 3rd or 11th; that planet was the native's movable significator of siblings by Parashara's own list (BPHS 32.13-16).
- The worksheet now marks the movable significator of each area with 'm' in the link-test table. It is displayed only.
- Evidence so far, sibling births on file (3 births, 2 charts): the house-and-fixed-significator test covered 2 of 3; the third is the case above. In one of those charts five of nine planets are strongly linked to siblings, so the test barely discriminates for this area anyway.
- Do not state an event on an 'm' alone. Promote it to a counted link only if forward-logged cases support it; drop the mark if they do not. Keep the count here.

## Rule 14 — Fix first (standing instruction of the owner, 13 Nov 2026)
Whenever a mistake, a gap, a limitation that can be reduced or an improvement to the process is found - during verification, a reading or any other work - it is fixed before the next question is asked or the next statement is made: the rule is written here, the check is coded into the engine where it can be coded, a test is added, the worksheet is rebuilt, and the change is pushed. Only then does the work continue. What cannot be fixed is stated plainly as a limit instead.

## Rule 15 — Dates are collected before the chart is shown; every verified chart gets a control-chart test (added 13 Nov 2026)
`python3 -m engine.control EVENTS.json --n 1000 --save` scores each rule on the real chart and on 1,000 charts with a wrong birth moment (events file kept outside the repository; only counts are saved in `data/control_tests.json`).
First run, one chart: with all 11 dated events from the verification answers the sub-period link rule scored 9 of 11 against a control average of 6.2 (11% of wrong charts did as well; link-or-movable 4%; link-and-polarity 7%). But four of those dates had been given in reply to questions that named the chart's own period. On the 7 independently dated events the edge disappears (31%, 16%, 22%). The main-period lord's link did worse than the controls in both runs (80% and 93%).
- A "yes" to "did X happen in period P?" yields a date anchored to the chart. Such dates may be scored as checks but must NOT be used as evidence that the timing works.
- Therefore: at intake, BEFORE any chart statement is shown, ask the person for 10-15 dated events of their life from their own memory or documents (month and year where possible; births, moves, jobs started and lost, marriage, losses, court matters). Store them outside the repository and run the control test on them.
- Report the control-test table in Part 1 of the reading beside the verification score. Near 50% = the rule says nothing about this person.
- No rule is called supported on one chart. Pool the counts across charts in `data/control_tests.json`; a rule that stays near or above 50% across several charts is demoted (the main-period link is the first candidate).

## Rule 16 — Blind checks: seal the windows, then ask for the date (added 13 Nov 2026)
Asking "did X happen in period P?" anchors the answer (Rule 15). The blind form removes that:
1. Choose an event type whose date is not yet known. `engine.control.indicated(birth, sex, area, polarity, start, end)` lists the sub-periods the rules point to and the share of the span they cover - the chance of a hit by luck. Prefer types where the share is under about a third; above half the check cannot discriminate and is not asked.
2. Log the windows in the ledger with `--kind blind` and push BEFORE asking. The commit time is the seal. Do not show the windows.
3. Ask only for the date ("which month and year did ... happen?"), one question at a time.
4. Reveal the sealed windows, score hit or miss (no "partly" for a single dated event; an event with several dates is scored date by date), and compare the hit rate with the average sealed share.
5. The dated answers go into the person's private events file for the control-chart test.
- **Choice form (added the same day, first chart).** Most people do not carry dates in their heads: three open "when did it happen?" questions in a row could not be answered. Offer instead three or four periods that together cover the plausible span, cut at the chart's own sub-period boundaries, WITHOUT saying which the chart points to; the person picks one (or names the month). Recognition is easier than recall and the answer is still blind. Chance of a hit by luck = the share of the offered span inside the sealed windows. Never fall back to "the chart says X - right or wrong?" (Rule 15).
- First blind result: one scorable answer out of four questions, a miss (sealed share 25%).
- Second blind result (same chart): best period for income fell in salaried years, outside the sealed "money, good" windows (share 31%) - a miss. Observation to test on other charts, NOT acted on from one case: the "money" row uses the 2nd and 11th houses and Jupiter only, so pay from employment (a 10th-house matter) is invisible to it; the same years were inside the "career, good" windows. If employed people's best-income years keep falling in career windows, the money row for an employee should read 2nd, 10th and 11th together.
- Running blind tally, first chart: 5 asked, 2 scorable, 0 hits (about 0.6 expected by luck).

## Rule 17 — What the pooled control test says so far (13 Nov 2026; 5 charts, 37 dated events, 10 exact dates)
`engine.control.pool` on every dated event in the stored answers (counts in `data/control_tests.json`):
| Rule | Real charts | Wrong charts (average) | Wrong charts as good | Same on the 28 cleanly dated events |
|---|---|---|---|---|
| Sub-period lord strongly linked to the event's area | 26 of 37 | 20.3 | 7% | 21 of 28, 5% |
| Main-period lord linked to the area | 16 of 37 | 20.4 | 89% | 10 of 28, 94% |
| Good/bad by house from the dasha lord + caution column | 13 of 27 | 13.9 | 74% | 11 of 21, 63% |
| Good/bad by Parashara's full template (house from lagna, dignity, house from dasha lord) | 13 of 24 | 12.5 | 51% | 13 of 19, 18% |
Working conclusions until more data arrives (each to be re-run whenever a chart is added):
1. **What a sub-period is about** (the link test) is the only rule with any edge - a hint, not a finding (7%, and one of the five charts scored far below its controls).
2. **The main-period lord's link carries no information** here and is not used as evidence for an area; it stays only as the frame the sub-periods sit in. The convergence table's main-period vote is to be read with that in mind.
3. **Whether a period goes well or badly is at chance** by both methods. Until that changes, a reading states the SUBJECT of a period and marks any good/bad direction as unsupported by the project's own data. The caution column of Rule 12 stays as a brake on promising gains; it is not evidence that a period will go badly.
4. The gap is therefore specific: judging direction, and timing finer than a sub-period. More people with independently dated events is the only way to close it; more reading of the texts helps only if it yields a different, testable way of judging direction.
- **Added the same day - Parashara's own good/bad measure (ch. 28, ishta and kashta), now coded (`engine.control.ishta_kashta`, worksheet section 9).** Pre-stated rule: a sub-period is good when its lord's ishta exceeds its kashta. Pooled result: 11 of 25, wrong charts average 11.0 (57% as good) - at chance. Three independent ways of judging direction have now been tested and all three sit at chance.
- **Laghu Parashari (all 42 verses, Sanskrit Wikisource) read the same day** and its direction doctrine coded as `polarity_lp` - the rule table was committed (c3a92e2) before the test was run. Pooled result: 7 right of 15 calls, wrong charts average 8.1 (75% as good) - at chance. **Four independent ways of judging good/bad have now been tested - house from the dasha lord with the caution column, Parashara's sub-period template, Parashara's ishta/kashta, and Laghu Parashari's functional natures - and all four sit at chance on 37 events.** The study gap named on the roadmap is closed; the result did not change. What remains is data (more people, exact dates) and the forward ledger.
- Free Sanskrit natal texts found on sanskritdocuments.org and not yet read: Bhrigu Sutram, Chamatkara Chintamani, Laghu Jataka (Varahamihira), Vriddha Yavana Jataka part 1; prashna texts Daivajna Vallabha and Shatpanchashika; plus the unread chapters of Jataka Parijata. They describe planets in houses and signs; none is known to hold a different method for direction or timing, so they are lower priority than data.
- **Three transit rules for good/bad tested the same day** (pre-stated, commit 47e66b4; Parashara 72.30-31 and Laghu Jataka 11.15 put direction in transit through Ashtakavarga): Jupiter and Saturn by house from the Moon 5 of 12 (wrong charts 6.7); by their own Ashtakavarga points 7 of 22 (10.8); by combined points 14 of 25 (12.5). All at chance. Seven direction rules tested in all. Texts read in full the same day: Laghu Jataka, Chamatkara Chintamani, Bhrigu Sutram, Shatpanchashika (`kb/sources/other-texts/README.md`). Gap analysis: `docs/GAP_ANALYSIS.md`.
