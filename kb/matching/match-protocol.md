# Matrimonial profile & match protocol (v2, 20 Oct 2026)

Why: the Vrushab x Pooja and Vrushab x Sindhura first verdicts were made from the Ashtakoota score alone and missed the strongest, life-verified feature of Vrushab's chart (partner from outside his circle/country). Ashtakoota compares Moons for temperament only. It never tests whether a candidate is the partner either chart describes. Vrushab: "You need to be very careful when you're giving verdicts... every time there is a comparison, go in very detail. Build it into the program."

The process has TWO stages. Never merge them.

## Stage 1 — when a biodata/chart is received: the candidate's own profile (no comparison)
1. Extract every field from the biodata (name, father, DOB, time, place, gotra, education, job, rashi, nakshatra, pada, nadi, gana, yoni, any chart image). Do NOT store phone numbers or addresses.
2. Compute the chart; check it against the biodata (rashi, nakshatra, pada, nadi, gana, yoni, chart image house-by-house). Report match or mismatch.
3. Birth-time sensitivity: distance of lagna and Moon to the next sign/nakshatra/pada, in minutes. Flag anything under ~15 min, and state what changes (e.g. Manglik status).
4. Personal profile in plain language: personality (lagna, Moon, Sun), career & money, family, marriage (her partner description from 7th, 7L, Jupiter/Venus, DK, D9 7th, UL/A7 — this feeds Stage 2), children, health, current period and marriage windows with dates.
5. Save `data/charts/<name>_<date>.json` (repo) and `/people/<name>.md` (project memory).
6. End with: "Say when you want the comparison with your chart."

## Stage 2 — only when Vrushab asks: comparison with his chart
Order is fixed; weights in brackets.

A. **His chart's partner description [highest weight].** From his file `data/charts/vrushab_1987-02-03.json`: 7L Moon with Rahu at 2 deg in 3rd; Rahu aspects 7th; Venus (marriage karaka, yogakaraka) in 12th; D9 Moon Sagittarius; DK Jupiter own sign with 7L; 7th from Moon Virgo with Ketu; UL Gemini (6th). Reads: wife from outside his circle (community/region/country), married life with a foreign link, met through network not family arrangement (A7 in 11th with Saturn), marriage through contest/paperwork (UL 6th). Verified: every serious past relationship followed this. Rated VERY STRONG.
B. **Her chart's partner description** (from Stage 1 step 4), rated strong/moderate/weak.
C. **Fact intake — ask, never guess** (do not ask or record caste names; "same circle / outside circle" is enough):
   - Same community/circle as Vrushab, or outside it?
   - How did the proposal come — family reference, network, own meeting?
   - Region, language, country of origin.
   - Where would they live after marriage? (Vrushab, 20 Oct 2026: most probably India, business mostly here; Vietnam probably travel only.)
   - Age gap; her profession and whether it is foreign-facing.
   No verdict until these are answered.
D. **Signature test.** For each signature in A and B: MET / PARTLY / UNMET, with the fact that decides it. A family-reference proposal from his own circle, living in India, = UNMET for his Rahu-on-7L and Venus-12th signatures.
E. **Ashtakoota** — all 8 kootas with points, every dosha, every cancellation rule tested and named; Manglik from lagna, Moon, Venus with cancellations; birth-time sensitivity of her Moon/lagna.
F. **Inter-chart contacts** — her planets in his houses and his in hers; exclude contacts shared by everyone born within the same few weeks (slow planets: Jupiter, Saturn, Rahu/Ketu) or say they are generic.
G. **Timing overlap** — his windows (now–Jun 2027 deliberate; Apr–Oct 2028 cleanest; Sep 2030–Oct 2031 strongest by transit) vs hers.
H. **Verdict grid** (state the row):
   | Signature fit | Score | Verdict |
   | met | pass | strong match |
   | met | fail | fits the stars, fails tradition — weigh with care |
   | unmet | pass | gets along, but not the partner the chart describes — low fit |
   | unmet | fail | not a match |
I. **Plain-language summary** for a layman: two questions — "Is she the kind of person your stars describe?" and "Would you get along day to day?" — then the issues and the timing, then the one-line verdict.

## Results on file (20 Oct 2026)
- Pooja Kalburgi: same circle (stated), would live in India → his signatures UNMET, her Rahu-in-7th UNMET; Ashtakoota ~24/36 pass (Nadi clean, Bhakoot cancelled) → LOW FIT.
- Sindhura Bachwal: same circle via family reference (stated) → UNMET; her chart's distance/abroad signature unmet if living in India; Ashtakoota ~12.5/36 fail (Nadi + Bhakoot uncancelled); lagna 8 min from Vrishchika (Manglik if later) → NOT A MATCH.
