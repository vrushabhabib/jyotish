# Synthesis-mode timing test on Astro-Databank — fixed before any data is collected (21 Nov 2026, 17:10 IST)

Owner's instruction (21 Nov): "ok do it all" — test whether the convergence of eight clocks (Rule 26,
`engine/synthesis.py`, commit f91aaf4, unchanged) puts real life events inside its windows more often than
wrong charts do. Fixed here BEFORE the first person page of this sample is opened.

## Sample (also serves the pre-registered link_lagna_tie confirmation of 17 Nov)
- Entries 401-800 of the mechanical alphabetical walk of the Astro-Databank category
  "Family : Relationship : Number of Marriages" (the category walked on 17 Nov). Every entry taken in
  order; none skipped for how its chart looks.
- Rodden AA or A only. Anonymous records: birth date, time, UTC offset, coordinates, events. No names stored.
- Events with at least month + year. Area mapping, fixed now (category text of the ADB event line):
  Relationship : Marriage / Divorce / Separation / Engagement / Meet significant person / Begin relationship -> marriage;
  "Birth of child" / "Birth of" first child lines -> children; Work : (any) -> career; Financial : (any) -> money;
  Relocation / Change residence -> home/mother. Death lines and everything else: not used.

## Method under test (exactly as committed; equal weights - no per-person calibration is possible for strangers)
- For the event's area, the selective level is computed on the person's chart over 150 months sampled evenly from
  age 16 to the person's age at the last event + 5 years (cap age 80): the lowest score at which no more than
  34% of months reach it with at least 4 of 8 clocks agreeing.
- HIT = the event's month reaches that level with at least 4 clocks agreeing.
- Controls: 200 wrong-birth charts per person, drawn as in engine.control (birth moved 30 days to 6 years earlier
  or up to 3 years later but at least a month before the first event, random clock time); the same scoring.
- Pooled statistic: total hits across people, real vs each of the 200 pooled control draws (one control chart
  per person per draw). Share of control draws at or above the real total.

## Bars, fixed now
- PRIMARY: marriage-area events. Synthesis mode counts as supported only if the pooled share < 0.01.
- Secondary (reported, not a result): all mapped areas; mean number of agreeing clocks real vs control.
- link_lagna_tie confirmation: as pre-registered on 17 Nov (engine.control.pool, all areas, 1,000 controls,
  bar < 0.01) - run on the same sample if time allows; otherwise reported as not run.
- A null means: convergence of the eight clocks does not time events better than wrong charts on strangers.
  Readings then keep saying that once at the start, and the ledger stays the only judge for a given person.
