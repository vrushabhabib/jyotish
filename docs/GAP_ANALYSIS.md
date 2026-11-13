# Where the present setup is lacking, and how to improve it (13 Nov 2026)

Written after reading Laghu Parashari, Laghu Jataka, Chamatkara Chintamani, Bhrigu Sutram and Shatpanchashika in full and taking stock of the day's tests. Figures are from `data/control_tests.json` (5 charts, 37 dated events, 10 exact dates).

## What works
- Calculation: positions, dashas, Ashtakavarga match AstroSage and JPL; 61 tests on two ephemeris engines.
- Faithfulness: Parashara, Brihat Jataka, Laghu Parashari, Laghu Jataka read in full from the Sanskrit; rules carry verse numbers.
- Honesty machinery: control-chart test, blind checks with sealed windows, forward ledger, fix-first rule.

## What the tests say
| Claim | Result |
|---|---|
| What a sub-period is about (link test) | 26 of 37 against 20.4 for wrong charts - a faint edge (7%) resting mostly on two people |
| What a main period is about | worse than wrong charts (88%) |
| Good or bad, four dasha-based methods (house from dasha lord + caution column; Parashara's template; ishta/kashta; Laghu Parashari) | all at chance |
| Good or bad, three transit methods (Jupiter and Saturn from the Moon; their own Ashtakavarga points; combined points) | all at chance (88%, 95%, 34%) |
| Blind checks on one chart | 0 of 2 |
| Forward statements | none matured |

## Where we are lacking
1. **Evidence of prediction.** Seven ways of judging good and bad have been tested; none beats wrong charts. This is the central gap and reading has not closed it.
2. **Data.** Five people, 37 events, 10 exact dates. Too little to confirm the faint edge or to find a small real effect; twelve rules have now been tried on the same events, so one looking good by luck is expected. There is no held-out set.
3. **A whole dasha doctrine is missing from the engine.** Varahamihira (Brihat Jataka 8, Laghu Jataka 10) and the Yavana text time life by the life-span dasha with sub-periods given only to planets joined to, in trine to, opposite or square the dasha lord. The engine has Vimshottari, Yogini, Chara and Ashtottari only. Untested because not built.
4. **A whole branch is missing: question charts.** Two classical texts on file. No module, no test.
5. **Unread timing chapters.** Vriddha Yavana Jataka ch. 6-8 (dasha, sub-period, Ashtakavarga results); Jataka Parijata ch. 9-10, 17, 18 v.77-172; Daivajna Vallabha ch. 2-15.
6. **Timing finer than a sub-period is untested** (sub-sub-periods; the eight-part division of a sign in Ashtakavarga transit).
7. **Divisional charts play no part in any tested rule.**
8. **Event coding is mine.** Which life area an event belongs to, and whether it is good or bad, is my judgement (salary counted as money or career changed one result). No second coder.
9. **Translations are unreviewed.** The e-texts are volunteer-typed, with typing errors and gaps; my readings have not been checked by a Sanskrit scholar or a practising astrologer.
10. **No Jaimini sutras or Saravali** - no clean free Sanskrit text found on either site searched.

## How to improve, in order of expected value
A. **Data drive.** A simple intake sheet (birth time and its source, 10-15 dated events from documents) for 50 people; split into a set for looking and a set kept unseen for confirming.
B. **Question-chart module with a fast forward test.** Code the rules of Shatpanchashika and Daivajna Vallabha; every question he asks gets a logged answer with a due date; results come in weeks, not years. This is the only route to quick, honest forward evidence.
C. **Build the life-span dasha** (after reading Yavana ch. 6-7 and re-reading Brihat Jataka 8) and put it through the control test beside Vimshottari.
D. **Finish the unread timing chapters** (item 5) before any more descriptive ones.
E. **Finer timing and divisional-chart rules**, each written down before its test.
F. **Outside review**: a Sanskrit reader for the translations; a second person to code events blind to the chart.
G. **Discipline already in place and kept**: rules stated before results, counts only in the repository, misses kept visible.

## What cannot be promised
That any of this produces accurate prediction. Each step either finds a signal or shows there is none; both outcomes are reported.

## Update, same evening
- Vriddha Yavana Jataka ch. 6-7 and Jataka Parijata ch. 18 (rest) read in full. They add no new timing method: both give fixed results for each pair of dasha lord and sub-lord by the planets' natures.
- That pattern, tested as a rule (natural benefic sub-lord = good), is the first direction rule to beat wrong charts: 17 of 25 against 11.4 (1.3%). One chart carries it (8 of 8); the other four are at chance. Frozen and pre-registered for confirmation on new people (antar-event-rules.md, Rule 18). Not used in readings.
- New item for the build list: the navamsa reversal (exalted sign with debilitated navamsa gives bad, and the reverse) - stated five times in Jataka Parijata 18, used by no rule.
- Still unread: Daivajna Vallabha ch. 2-15; Vriddha Yavana Jataka ch. 8-39; Jataka Parijata ch. 6, 8-12, 17 and the rest of 7.

## Update, reading batch 3 (13 Nov 2026)
- Read in full: Jataka Parijata ch. 10 (Ashtakavarga) and ch. 17 (Kalachakra dasha); Vriddha Yavana Jataka ch. 8 (Ashtakavarga).
- Tested (pre-stated): sub-lord's own Ashtakavarga points in its birth sign. 12 of 19 against 8.2 from wrong charts (10%). Not significant. Ninth direction rule tried.
- **New gap 11: no Kalachakra dasha in the engine.** A second clock, by signs, never built or tested (Parashara keeps Vimshottari as chief, BPHS 46.3). Sequences are already decoded from BPHS in kb/sources/bphs/ch46-50.md; the Jataka Parijata e-text is damaged at the sequence tables. Sensitive to birth time (Moon's star-quarter).
- **New gap 12: Ashtakavarga is used only for transits.** Both long texts also use it to judge the quality of a planet's own period (JP 10.10-11 by sign points; VYJ ch. 8 by the eighth-part). The second form is untested and its owner order is unsourced.
- Honest count of direction rules so far: nine tested on the same 25 events; one at 1.3% (carried by one chart), one at 10%, seven at chance. With nine tries, one result near 1% is weak evidence. Only new people can settle it.
- Still unread: Daivajna Vallabha ch. 2-15; Vriddha Yavana Jataka ch. 9-39; Jataka Parijata ch. 6, 8, 9, 11, 12 and the rest of 7.

## Update, reading batch 4 (13 Nov 2026)
- Read in full: Daivajna Vallabha (all 15 chapters, question charts) and Jataka Parijata ch. 6 (what breaks a chart).
- Daivajna Vallabha confirms Shatpanchashika's core test and adds counting devices for days and months. It strengthens the case that a question-chart module is the fastest honest test we can run.
- The copy of Daivajna Vallabha online is marked "personal reading only, not for commercial use". Fine for private study; if the project becomes a paid service, the text must be re-read from a scanned print edition.
- Jataka Parijata ch. 6 gives measurable "promise breakers" (8th lord stronger than 9th lord, 12th lord stronger than lagna lord, 11th lord combust, navamsa reversal v.36). No timing rule.
- **Correction to my earlier unread lists:** Jataka Parijata ch. 5 (length of life, 18 KB) and ch. 4 after v.80 were never read and I had left them off the list. Ch. 5 matters for the life-span dasha gap; it is read for method only, never to state a length of life.
- Still unread: Jataka Parijata ch. 4 (after v.80), 5, rest of 7, 8, 9, 11, 12 (about 125 KB); Vriddha Yavana Jataka ch. 9-39 (about 250 KB).
