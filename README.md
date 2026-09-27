# Jyotish — Vedic Astrology Knowledge Base & Calculation Engine

Two halves:

1. **`engine/`** — Python. Turns birth data (date, time, place) into a full Vedic chart:
   sidereal positions (Lahiri), lagna, whole-sign bhavas, nakshatra/pada, vargas (D9, D10, D7, D2…),
   Vimshottari dasha, Ashtakoota guna milan, Manglik and other dosha checks, Sade Sati.
   Uses Swiss Ephemeris (`pyswisseph`).

2. **`kb/`** — Markdown + JSON. The interpretation rules an agent reads: planets, rashis, bhavas,
   nakshatras, yogas, doshas, dashas, transits, matchmaking (marriage + business), remedies.

Everything is Parashari by default; Jaimini/KP noted where they differ.

## Quick start
```bash
pip install -r requirements.txt
python -m engine.chart 1990-04-15 06:30 Hubballi 15.3647 75.1240 Asia/Kolkata
python -m engine.matching      # demo: ashtakoota + business synastry on two sample charts
python -m pytest tests
```

## Layout
```
engine/   chart.py (ephemeris, vargas, dasha, doshas)   matching.py (ashtakoota, business synastry)
data/     nakshatras.json  rashis.json (rashis + planets + karakas)
kb/       index.md = reading protocol; one folder per domain
tests/    regression tests
```

## Roadmap
- engine: Shadbala, Ashtakavarga, Bhava Chalit cusps, geocoding (place name → lat/lon/tz), Jaimini karakas, KP sub-lords
- kb: per-planet files (9), per-nakshatra files (27), per-lagna files (12), varga interpretation, muhurta
- agent: reader prompt that takes engine JSON + kb and produces a reading; two-chart mode for marriage/business
