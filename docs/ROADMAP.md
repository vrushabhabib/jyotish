# Roadmap - two tracks (owner's decision, 13 Nov 2026)

The owner's goal is a model that predicts accurately. The measured position on 13 Nov 2026 (`kb/dashas/antar-event-rules.md`, Rule 17): the sub-period link test has a faint edge over wrong charts; whether a period goes well or badly is at chance; no forward prediction has matured. He chose to run both tracks below, on the view that the domain has not yet been studied thoroughly and accurately enough.

## Track A - the working agent (faithful, exact, open about limits)
Computes charts exactly, reads them by the classical texts, states the subject of each period, marks direction as unsupported until the data says otherwise, logs every dated statement.

## Track B - research: find out whether a real signal exists, and grow it if it does
1. **Study, aimed at the measured gap (direction and finer timing), Sanskrit first, free sources only.**
   - DONE 13 Nov 2026 (at chance as a direction rule): Laghu Parashari / Jataka Chandrika (42 verses on judging dasha results - which sub-period gives a planet's results, functional benefics and malefics, yoga-givers, marakas). The KB's dasha-judgement rules from it are still tagged [MEM]: find a free Sanskrit text, read it, replace the [MEM] lines, code what can be coded.
   - DONE 13 Nov 2026 (at chance as a direction rule): Parashara's own measures of how good or bad a planet's period is: Ishta and Kashta phala (was not coded in the engine yet), with Shadbala and the twenty-point strength already coded. Read the chapter again, code it, test it as a direction rule.
   - The unread chapters of Jataka Parijata (6, 8-12, 17, rest of 7 and 18).
   - Finer timing inside a sub-period: sub-sub-periods and Ashtakavarga transit (kaksha) as Parashara states them.
   - Every rule that comes out of study enters the control test as a pre-stated rule BEFORE its result is looked at; rules are never tuned on the events they are scored on.
2. **Data.** The bottleneck. Target: at least 50 people with a recorded birth time and 10-15 independently dated events each (intake step 1b), exact dates preferred. Events files stay outside the repository; counts only in `data/control_tests.json`.
3. **Testing.** `engine.control` (real chart against wrong charts, per rule and pooled), blind checks in choice form (Rule 16), forward statements in the ledger. Re-run the pooled table whenever a chart is added.
4. **Modelling.** Only when there are several hundred dated events: a statistical model over chart features, validated on people it has never seen. Before that it would fit noise.
5. **Reporting.** Every reading's Part 1 quotes the current pooled table and the ledger record.

## What would count as success
A rule or model that beats wrong charts on new people, on precise dated statements, repeatedly. A hit rate is quoted only beside its chance rate. No target figure is promised: outside controlled tests of astrology have found chance-level results, and this project's own figures are the only evidence it will claim.
