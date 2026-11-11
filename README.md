# Jyotish — Vedic Astrology Knowledge Base & Calculation Engine

Parashari base, Lahiri ayanamsa, whole-sign houses. Jaimini and KP are noted where they add a checkable test.

## Quick start
```bash
pip install -q ephem pytest --break-system-packages     # pyswisseph is optional; used automatically when present
python3 -m pytest -q tests                              # all green before any chart is trusted

# one command per chart: a complete worksheet (markdown + JSON)
python3 -m engine.report 1996-11-24 12:05 15.3333 75.1333 Asia/Kolkata --name Tanzil --sex F --out /tmp/ws
python3 -m engine.report --pdf AstroSage.pdf --out /tmp/ws      # reads the PDF, computes, cross-checks

python3 -m engine.store data/charts/<name>_<date>.json          # refresh a stored chart's "computed" block
```

## Engine (`engine/`)
| Module | Does |
|---|---|
| `ephemeris.py` | Planet positions. Swiss Ephemeris if installed, else pyephem. Validated against JPL Horizons. |
| `chart.py` | Lagna, planets, dignity, combustion, 15 divisional charts, Vimshottari. |
| `analysis.py` | Houses from lagna/Moon/Sun, functional nature, avasthas, Jaimini karakas and arudhas, about 40 yogas with weakeners, Manglik (3 definitions, tiered cancellations), Kaal Sarp, Pitru, KP star/sub/sub-sub, special points, link test, 3-level dasha tree. |
| `ashtakavarga.py` | Bhinna and Sarva Ashtakavarga (BPHS tables), kakshya, transit scoring. |
| `shadbala.py` | Shadbala (six strengths) and Bhava Bala; unverified components are listed in the output. |
| `transits.py` | Sign ingress tables, Sade Sati and other Saturn phases, double transit, returns. |
| `astrosage_pdf.py` | Parser for AstroSage kundli PDFs plus cross-check against our own computation. |
| `report.py` | The worksheet: 14 sections, everything above in one document. |
| `houses.py` | Placidus cusps with KP ayanamsa, KP star/sub/sub-sub lords and four-level significators, Sripati Bhava Chalit. All 12 cusps within 0.5 arc-min of AstroSage. |
| `dashas_extra.py` | Yogini, Jaimini Chara (K.N. Rao method) and Ashtottari dashas. Yogini and Chara reproduce the AstroSage tables. |
| `yogas_extra.py` | Detection for the rest of the 160-yoga catalogue (156 of 160 tested), each with the catalogue's result, cancellation and how common it is. |
| `convergence.py` | Months in which 4 of 5 independent timing systems agree on a life area, with a self-check of how often that happens by chance in the same chart. |
| `baserates.py` | Firing rate of every yoga and dosha over 4,000 random charts (`data/base_rates.json`). |
| `ledger.py` | Prediction ledger (`data/ledger.jsonl`): log before the answer is known, score after, report hit rates. |
| `discriminate.py` | For an uncertain birth time: where in the window each divisional lagna changes and which questions separate the segments. |
| `places.py` | Offline place-name lookup (towns above 15,000 people) to latitude, longitude and time zone. |
| `store.py` | Standard `computed` block for files in `data/charts/`. |
| `matching.py` | Ashtakoota and business synastry. |

## Knowledge base (`kb/`)
Start at `kb/index.md`. Intake is `kb/readings/kundli-intake.md`; the reading form is `kb/readings/full-reading-protocol.md`; the in-house calibration rules are `kb/dashas/antar-event-rules.md`. Life-area rule files carry rule IDs with the source actually read; `[UNSOURCED]` and `[MEMORY]` tags mark what was not verified at a primary text.

## Validation record
- 11 Nov 2026: Sun and Jupiter apparent longitudes identical to JPL Horizons to 4 decimals (1996-11-24 06:35 UT). Sarvashtakavarga identical to AstroSage sign by sign. Published ingresses reproduced (Saturn to Mesha 3 Jun 2027; Jupiter to Karka 2 Jun 2026).
- Known bug fixed the same day: the 20 Oct 2026 fallback read positions in the J2000 frame (0.84 arc-min per year from 2000). Charts computed with it before the fix: Saira (dates were about 2 months early) and Tanzil (under 1 week).
- Shadbala (12 Nov 2026): second reference found - B.V. Raman's standard horoscope. With his ayanamsa the engine gives his Sthana bala for all seven planets to 0.1 virupa and his Kala bala to 0.7. Mercury's Saptavargaja, the Hora lord and the dwadasamsa boundaries are therefore ours and Raman's; AstroSage deviates. Cheshta, Drik against Raman, and Yuddha remain unconfirmed.
- Two ephemeris engines (Swiss Ephemeris and pyephem) agree over 400 random dates 1930-2040: planets within 1.6 arc-seconds, Moon 10.5, lagna 8.4. All tests pass on both (`JYOTISH_BACKEND=ephem python3 -m pytest tests`).
- Convergence timing back-test: 2 of 8 known events caught. Experimental.
