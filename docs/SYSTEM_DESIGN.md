# System design - how a reading is made so that nothing present is missed (13 Nov 2026)

## The pipeline
1. **Intake** - birth data, the real doubt in the birth time, and 10-15 dated life events collected BEFORE any chart statement (kb/readings/kundli-intake.md).
2. **Compute** - `python3 -m engine.report ... --out DIR`. One command; no position, date or strength is ever worked out by hand. Two independent ephemeris engines must agree.
3. **Register** - the worksheet ends with section 15, the FINDINGS REGISTER (`engine/findings.py`). Every feature the sources treat as meaningful is a numbered line with its source verse and an evidence word. The same list is in `*.computed.json`.
4. **Verify** - questions about the past, one at a time; control test on the dated events; results into the ledger.
5. **Draft** - each statement in the draft cites the finding it rests on: `[F:H07.judgement]`. A finding that does not matter for this reading is set aside in the open: `[F:Y.Anapha waived: present in a third of all charts]`.
6. **Check** - `python3 -m engine.findings check DIR/name.computed.json DRAFT.md`. It exits with an error while any MUST finding is neither cited nor waived, or a tag matches nothing. A reading is not sent until this passes.
7. **Send** - `python3 -m engine.findings strip DRAFT.md` removes the tags. Forward statements go to the ledger first.

## Why this cannot silently drop information
- A feature that is computed but not in the register: caught by tests (every house and planet must appear; every registered rule must be used, pending or excluded).
- A feature in the register but not in the reading: caught by `check`.
- A method that exists in the texts but not in the engine: listed in the register's "NOT computed" block on every worksheet, and repeated in Part 13 of the reading.
- A statement in the reading with no finding behind it: it has no tag; the reviewer looks for untagged claims.
- A rule pushed further than the evidence: every line carries text / hint / frozen / chance.

## What the register holds today
| Group | ID pattern | Source |
|---|---|---|
| State and dignity of each planet, share of result | `P.<planet>.state` | BPHS; JP 7.58, 8.115-116 |
| Navamsa reversal | `NR.<planet>` | JP 6.36 |
| Who looks at each planet | `ASP.<planet>` | VYJ ch. 9-15 (frozen) |
| Strength by part | `SB.<planet>` | VYJ ch. 17-23 |
| What builds and harms each of the 12 houses | `H01..H12.judgement`, `.degree` | JP 11.1-12 |
| Kind of result of a planet in its house, with verse number | `Q.<planet>` | VYJ ch. 24a-35 |
| What weakens the chart's promise | `BRK.*` | JP ch. 6 |
| Placements where the texts disagree | `DIS.<planet>.<house>` | VYJ 16, 30 v. JP 8 |
| Cautions on a planet's periods | `C.<planet>` | JP 18.27-28 |
| Named combinations, with when they pay | `Y.*` | catalogue; JP 7.66 |
| Method notes that must be quoted | `T.birth-time`, `M.direction` | our tests |

## Build list (status)
| Item | Status |
|---|---|
| Findings register, check, strip, tests | DONE 13 Nov 2026 |
| Navamsa reversal, dignity scale, house judgement with sign-lord step and degree distance, promise-breakers, strength by part, quality grid pointers, source disagreements | DONE (in the register) |
| Kalachakra dasha (`engine/dashas_classical.py`; worksheet section 16) | DONE 13 Nov 2026 - all 16 sequences checked against the totals the text states; periods after the first cycle rest on a rule not in the verses |
| Life-span dasha, periods only | DONE - experimental; several conventions ours; not cross-checked |
| Question-chart module (`python3 -m engine.prashna`) with clock time stamp, fixed verdict rule and ledger logging | DONE - no question scored yet |
| Grid verses stored (`data/vyj_grid.json`, Sanskrit, 10 chapters; children and death chapters deliberately not stored) and printed in the register | DONE - a fixed English wording per verse is NOT stored |
| Candidate timing rules (Rule 19: five rules) | DONE - pre-stated, pushed, then tested: all at chance |
| Intake of new people (`data/intake/EVENTS_FORM.md`, `python3 -m engine.intake check/run/status`) | TOOL DONE - the people are still needed: 0 of 25 good/bad events |
| Strength-part count and eighth-part rule | pending - not tested |
| Vriddha Yavana Jataka part two; Jaimini; Saravali | not read |

## What this does not do
It makes the reading complete and traceable. It does not make it more accurate: accuracy is measured only by the ledger and the control tests, and those still say that the subject of a period has a faint edge and the direction has none.
