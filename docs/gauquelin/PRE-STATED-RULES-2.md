# Gauquelin test 2: military men vs painters — rules fixed before any chart was cast

Written and pushed 17 Nov 2026, before the engine was run on any A3/A4 birth. This contrast the texts
name directly: Mars rules commanders and soldiers (BPHS, Phaladeepika, Brihat Jataka ch. on profession);
Venus rules the arts. Data: g5 repo raw files 902gdA3y.html (3,046 military men) and 902gdA4y.html
(2,720 painters), columns verified 400/400 against the maintainer's own conversion of A1.

## Design
Same as test 1: each military man paired by birth date alone with the nearest unused painter (<=730 days);
each rule must say which of the two is the military man; accuracy vs 50%, two-sided binomial p.
Bar for a result: accuracy >= 53% AND p < 0.001 (eight rules at once). Direction fixed now.

## Rules (military = the Mars side, painter = the Venus side)
1. R1 higher Mars shadbala ratio -> military
2. R2 lower Venus shadbala ratio -> military
3. R3 Mars in a kendra from lagna; tie -> R1
4. R4 Venus in a kendra from lagna -> painter; tie -> R2
5. R5 10th lord from lagna: Mars -> military, Venus -> painter, else no call
6. R6 10th lord from the Moon, same reading
7. R7 dignity: Mars own/exalted -> military, Venus own/exalted -> painter; both or neither -> no call
8. R8 combined: (Mars ratio - Venus ratio) higher -> military

Limits as in test 1 (rounded register times; whole-sign houses; registration-habit caveat).
