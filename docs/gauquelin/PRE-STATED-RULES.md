# Gauquelin profession test — rules fixed before any chart was cast

Written and pushed 17 Nov 2026, before the engine was run on any Gauquelin birth.

## Data
Open Gauquelin Database as shipped in github.com/tig12/g5, files `data/db/init/lerrcp-marked/A1.csv`
(2,087 sports champions) and `A2.csv` (3,643 scientists and physicians). Times are civil-register
times with the UTC offset already resolved by the g5 maintainer. Public historical figures; no one is asked anything.

## Design
- Era is a confound (sportsmen centre on the 1920s, scientists on the 1870s). Each sportsman is
  paired, by birth date alone and before any chart is computed, with the unused scientist born
  nearest in time, within 730 days; unmatched rows are dropped.
- For each pair, each rule must say which of the two is the sportsman. Accuracy against 50%,
  two-sided binomial p. Rules were NOT tuned on this data; none of it has ever been seen by the engine.
- Classical category mapping, stated now: the texts have no "athlete"; the nearest classical type is
  the man of valour and physical force (Mars). Scientists and physicians map to the learned
  professions (Mercury and Jupiter). This mapping is the weakest link and is fixed here, in advance.

## The rules (direction fixed in advance; sportsman = the Mars side)
1. R1 Mars strength: the one with the higher Mars shadbala ratio is the sportsman.
2. R2 Mars angular: Mars in a kendra (house 1, 4, 7, 10 from lagna); if tied, higher Mars shadbala.
3. R3 Gauquelin zones (the published "Mars effect", stated as he stated it): Mars in the 12th or 9th
   whole-sign house from the lagna; tie-break as R2.
4. R4 Mercury strength: the one with the LOWER Mercury shadbala ratio is the sportsman.
5. R5 Jupiter strength: the one with the LOWER Jupiter shadbala ratio is the sportsman.
6. R6 Tenth lord: 10th lord from lagna is Mars → sportsman; Mercury or Jupiter → scientist; else no call.
7. R7 Tenth from the Moon, same reading as R6.
8. R8 Combined: (Mars ratio) − max(Mercury ratio, Jupiter ratio); higher → sportsman.

## What counts as a result
A rule is interesting only if p < 0.001 (eight rules are being tested at once) AND the accuracy edge
is at least 53% on 900+ pairs. Anything weaker is reported as chance.

## Stated limits
- Rounded register times (often to the hour) blur the lagna; this lowers power and is accepted.
- Time-of-day registration habits may differ by profession and era; date-matching does not remove
  this. If a lagna-based rule alone fires, this artefact is the first suspect and will be said so.
- A null here is a null for THESE rules on THIS contrast, not a verdict on every rule in the texts.
