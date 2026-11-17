# Rule search with sealed holdout — result (17 Nov 2026)

Procedure fixed in PRE-STATED-SEARCH.md before the run. 193 features per person, every simple chart
fact: each planet in each house from the lagna, kendra/trikona/dusthana, kendra from the Moon,
retrogression, combustion, shadbala of all seven, lagna sign, Moon sign.

| Contrast | Pairs | Training survivors (p<0.001; chance expects ~0.2) | Holdout verdict |
|---|---|---|---|
| sportsmen vs scientists | 751 | 1 (Venus in the 3rd) | collapsed: 45.3%, p=0.45 |
| military vs painters | 1,882 | 0 | - |

The one training survivor is exactly the false positive the arithmetic predicts from searching 193
features, and it scored WORSE than chance on the sealed half. On the larger contrast nothing survived
even training.

## What this establishes
It is no longer "we have not found the right rule." The machine looked at every simple rule there is,
on the largest recorded-time dataset in existence, with the honest train-then-holdout method. For
profession, the information is not in the chart. No amount of further rule-crafting on this data can
change that; only a different question (timing of dated life events - Astro-Databank) remains open.
