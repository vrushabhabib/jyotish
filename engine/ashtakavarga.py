"""Ashtakavarga: Bhinnashtakavarga (BAV) for the seven grahas and Sarvashtakavarga (SAV).

Benefic places are the standard table (B.V. Raman, 'Ashtakavarga System of Prediction'; identical to
AstroSage). Totals: Sun 48, Moon 49, Mars 39, Mercury 54, Jupiter 56, Venus 52, Saturn 39 = 337.
Validated 11 Nov 2026 against an AstroSage printout (all 12 SAV values identical).

BPHS ch. 66 read in the Sanskrit (sanskritdocuments.org par6170.itx, 12 Nov 2026): the per-house counts of
Sun, Mars, Mercury, Jupiter and Saturn agree in all twelve houses. Three cells differ in that recension, with
the same totals: Moon's table - Jupiter gives in the 2nd (not the 12th) and the Moon gives in the 9th where
the standard table has Mars; Venus's table - Mars gives in the 4th (not the 5th). variant="bphs" applies them.

Brihat Jataka ch. 9 read in the Sanskrit (brihajjAtakam.itx, 12 Nov 2026): all seven tables decoded from the
verses agree with the standard table below in every cell. So the default is Varahamihira's table and the three
differing cells are Parashara's recension - two old texts, not an error in either.

Reading thresholds (BPHS 72.3-4, read in the Sanskrit): a sign with more than 30 is good, 25 to 30 middling,
below 25 weak. 72.30-31: plain transit is looked at only until the ashtakavarga is available.
In a planet's own BAV, 4 is neutral, 5+ good and 3 or fewer poor for its transit through that sign.
"""
from engine.chart import RASHI_NAMES

REFS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Lagna"]
BAV_RULES = {
 "Sun":     {"Sun": [1,2,4,7,8,9,10,11], "Moon": [3,6,10,11], "Mars": [1,2,4,7,8,9,10,11], "Mercury": [3,5,6,9,10,11,12],
             "Jupiter": [5,6,9,11], "Venus": [6,7,12], "Saturn": [1,2,4,7,8,9,10,11], "Lagna": [3,4,6,10,11,12]},
 "Moon":    {"Sun": [3,6,7,8,10,11], "Moon": [1,3,6,7,10,11], "Mars": [2,3,5,6,9,10,11], "Mercury": [1,3,4,5,7,8,10,11],
             "Jupiter": [1,4,7,8,10,11,12], "Venus": [3,4,5,7,9,10,11], "Saturn": [3,5,6,11], "Lagna": [3,6,10,11]},
 "Mars":    {"Sun": [3,5,6,10,11], "Moon": [3,6,11], "Mars": [1,2,4,7,8,10,11], "Mercury": [3,5,6,11],
             "Jupiter": [6,10,11,12], "Venus": [6,8,11,12], "Saturn": [1,4,7,8,9,10,11], "Lagna": [1,3,6,10,11]},
 "Mercury": {"Sun": [5,6,9,11,12], "Moon": [2,4,6,8,10,11], "Mars": [1,2,4,7,8,9,10,11], "Mercury": [1,3,5,6,9,10,11,12],
             "Jupiter": [6,8,11,12], "Venus": [1,2,3,4,5,8,9,11], "Saturn": [1,2,4,7,8,9,10,11], "Lagna": [1,2,4,6,8,10,11]},
 "Jupiter": {"Sun": [1,2,3,4,7,8,9,10,11], "Moon": [2,5,7,9,11], "Mars": [1,2,4,7,8,10,11], "Mercury": [1,2,4,5,6,9,10,11],
             "Jupiter": [1,2,3,4,7,8,10,11], "Venus": [2,5,6,9,10,11], "Saturn": [3,5,6,12], "Lagna": [1,2,4,5,6,7,9,10,11]},
 "Venus":   {"Sun": [8,11,12], "Moon": [1,2,3,4,5,8,9,11,12], "Mars": [3,5,6,9,11,12], "Mercury": [3,5,6,9,11],
             "Jupiter": [5,8,9,10,11], "Venus": [1,2,3,4,5,8,9,10,11], "Saturn": [3,4,5,8,9,10,11], "Lagna": [1,2,3,4,5,8,9,11]},
 "Saturn":  {"Sun": [1,2,4,7,8,10,11], "Moon": [3,6,11], "Mars": [3,5,6,10,11,12], "Mercury": [6,8,9,10,11,12],
             "Jupiter": [5,6,11,12], "Venus": [6,11,12], "Saturn": [3,5,6,11], "Lagna": [1,3,4,6,10,11]},
}
TOTALS = {"Sun": 48, "Moon": 49, "Mars": 39, "Mercury": 54, "Jupiter": 56, "Venus": 52, "Saturn": 39}
KAKSHYA = ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon", "Lagna"]   # 3 deg 45 min each, in this order


BPHS_VARIANT = {("Moon", "Jupiter"): [1,2,4,7,8,10,11], ("Moon", "Moon"): [1,3,6,7,9,10,11],
                ("Moon", "Mars"): [2,3,5,6,10,11], ("Venus", "Mars"): [3,4,6,9,11,12]}


def ashtakavarga(chart, variant="standard"):
    """Returns {'bav': {planet: [12 bindus, Aries..Pisces]}, 'sav': [12], 'by_house': {...}, 'contributors': {...}}
    variant="bphs" uses the three cells of the Sanskrit recension that differ from the standard table."""
    pos = {p: chart["planets"][p]["rashi"] for p in REFS[:-1]}
    pos["Lagna"] = chart["lagna"]["rashi"]
    bav, contrib = {}, {}
    for planet, rules in BAV_RULES.items():
        row = [0] * 12
        who = [[] for _ in range(12)]
        for ref, places in rules.items():
            if variant == "bphs": places = BPHS_VARIANT.get((planet, ref), places)
            for h in places:
                sg = (pos[ref] - 1 + h - 1) % 12
                row[sg] += 1; who[sg].append(ref)
        assert sum(row) == TOTALS[planet]
        bav[planet] = row; contrib[planet] = who
    sav = [sum(bav[p][i] for p in bav) for i in range(12)]
    lag = chart["lagna"]["rashi"]
    by_house = {h: sav[(lag - 1 + h - 1) % 12] for h in range(1, 13)}
    return {"bav": bav, "sav": sav, "sav_by_sign": dict(zip(RASHI_NAMES, sav)), "by_house": by_house, "contributors": contrib}


def house_checks(av):
    """The standard SAV comparisons (Raman, ch. on Sarvashtakavarga)."""
    h = av["by_house"]; out = []
    out.append(("11th > 10th (gain exceeds effort)", h[11] > h[10]))
    out.append(("11th > 12th (income exceeds expense)", h[11] > h[12]))
    out.append(("1st > 12th and 2nd > 12th (keeps what is earned)", h[1] > h[12] and h[2] > h[12]))
    out.append(("lagna >= 28 (constitution average or better)", h[1] >= 28))
    strong = [k for k, x in h.items() if x > 30]; weak = [k for k, x in h.items() if x < 25]
    return {"checks": out, "strong_houses": strong, "weak_houses": weak}


def transit_score(av, planet, sign, deg=None):
    """Bindus the transiting planet has in that sign (0-8), SAV of the sign, and whether the kakshya lord
    at that degree contributed a bindu (finer timing inside the sign)."""
    out = {"bav": av["bav"][planet][sign - 1] if planet in av["bav"] else None, "sav": av["sav"][sign - 1]}
    if deg is not None and planet in av["bav"]:
        k = KAKSHYA[min(int(deg // 3.75), 7)]
        out["kakshya_lord"] = k; out["kakshya_bindu"] = k in av["contributors"][planet][sign - 1]
    return out
