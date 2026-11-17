# Rule search with a sealed holdout — procedure fixed before it was run (17 Nov 2026)

Hand-picked rules have failed twice. This run searches EVERY simple chart feature instead, under a
procedure fixed here before the search starts. This is the only honest form of "learning".

## Data
The two paired contrasts already built (sportsman-vs-scientist 751 pairs, military-vs-painter 1,882
pairs). Pairs sorted by the first member's birth date; even-numbered pairs = TRAINING, odd = HOLDOUT.
The holdout is opened once, at the end, for the survivors only.

## Features (about 230 per person, all era-safe inside a date-matched pair)
- Each of the 9 planets in each of the 12 houses from the lagna (binary).
- Each of the 9 planets in kendra / trikona / dusthana from the lagna (binary).
- Each planet's house from the Moon in kendra (binary).
- Shadbala ratio of each of the 7 planets (continuous; within a pair, higher vs lower).
- Lagna in each of the 12 signs; Moon in each of the 12 signs (binary).
- Retrograde and combust flags per planet (binary).

## Procedure
1. On TRAINING pairs only: for every feature, count the pairs the feature separates and how often it
   points at group 1; two-sided binomial. A feature survives training only if p < 0.001 there.
2. Survivors are then scored on the HOLDOUT pairs, each alone, same statistic. A rule is REAL only if
   its holdout p < 0.01 in the SAME direction, with at least 53% on 100+ decided pairs.
3. Everything else is reported as what it is: noise. The number of features searched is reported so
   the reader can see how many survivors chance alone would produce (about 0.2 at p<0.001 per contrast).
4. No second pass, no tweaking after seeing the holdout. If nothing survives, that is the result.
