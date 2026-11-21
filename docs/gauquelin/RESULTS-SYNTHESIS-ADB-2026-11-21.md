# Synthesis-mode timing test — results (21 Nov 2026)

Protocol: `PRE-STATED-SYNTHESIS-ADB.md` (commit 91f080e, pushed before collection). Script: `tools/synthesis_adb_test.py`.

## Sample (collected mechanically through the desktop app's built-in browser)
Entries 401-800 of the alphabetical walk of "Family : Relationship : Number of Marriages" on Astro-Databank:
400 pages -> 257 people with Rodden AA/A and a full birth record -> 121 with at least one mapped, dated event
after age 16 (9 events before age 16 dropped - a parsing artefact; scored span starts at 16). Mapped events: 298
(marriage area 163, career 132, home 5... see raw counts in the private file). Records anonymous, kept outside the repo.

Deviation from the protocol, stated: control births were also kept at least 16 years before the first event, so that
every event lies inside the scored span of the control chart too. It rarely binds (controls move -6 to +3 years).

## Result
| Set | Events | Real hits | Wrong-chart average | Share of control draws as good or better | Mean clocks agreeing, real / control |
|---|---|---|---|---|---|
| **Marriage area (PRIMARY)** | 163 | 30 (18.4%) | 30.4 (18.7%) | **0.565** | 2.93 / 2.93 |
| All areas (secondary) | 298 | 71 (23.8%) | 57.9 (19.4%) | 0.045 | 3.51 / 3.52 |

**Primary: null.** On 163 dated marriages and divorces of 121 strangers with recorded birth times, the eight-clock
convergence windows caught exactly as many events as charts cast for the wrong birth moment. The bar was < 0.01.

Secondary (not a result): 0.045 on all areas, driven by career events. Career events in this data come in clusters
(several prizes or releases in one week for one person), which makes them non-independent and inflates the figure;
the average number of agreeing clocks is identical for real and wrong charts (3.51 vs 3.52). Under the protocol this
is reported, not used.

## What it means for readings
Agreement between several timing methods does not by itself time events better than chance on strangers. Synthesis
mode stays as the way of reading (whole chart, joined areas, plain specific language), but its dated windows carry no
tested support: say so once at the start of a reading, and let each person's ledger decide. The per-person calibration
(Rule 26 step 4) remains the only route by which the method could earn weight for one person, and it needs that
person's month-dated events.

Correction found while checking (21 Nov): the first synthesis script for vh-fresh quoted "six methods agree" for the
father window (Nov 2027-Apr 2028) and the main marriage window (Feb 2029-Feb 2030); six clocks voted across each window
but at most five agreed in any one month. The 2034-35 marriage window peaks at six, not seven. Script corrected; the
sheet now prints both numbers. The ledger basis text of vh-fresh-017 and -019 shows the across-window count.

## link_lagna_tie confirmation (pre-registered 17 Nov, same sample, engine.control.pool, 1,000 controls)
| Rule | Real | Of | Control mean | Share of controls as good or better |
|---|---|---|---|---|
| **link_lagna_tie (the only rule under test)** | 32 | 133 | 29.3 | **0.34** - candidate dead (bar < 0.01) |
| ad_link (reported only) | 168 | 298 | 170.1 | 0.61 |
| md_link | 156 | 298 | 167.0 | 0.82 |
| link_or_mov | 178 | 298 | 182.0 | 0.70 |
| pd_link (227 day-dated) | 132 | 227 | 128.5 | 0.34 |
| adpd_link | 82 | 227 | 80.1 | 0.43 |

The 17 Nov exploratory hint was chance, as expected. Every timing rule now tested on 290 strangers in two independent
samples sits at chance, and so does the eight-clock convergence built on them.
