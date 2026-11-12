"""Rays (rashmi) of the planets and the Sudarshana year - BPHS ch. 73 and 74, read from the Sanskrit
(sanskritdocuments.org par7180.itx, 12 Nov 2026).

73.1-3: at its exaltation point the Sun has 10 rays, Moon 9, Mars 5, Mercury 5, Jupiter 7, Venus 8, Saturn 5;
at its debilitation point none; between, in proportion: (distance from the debilitation point, taken the short
way, in signs) x rays / 6. The further multipliers of 73.4-6 are introduced by the text as "said by others" and
are not applied. 73.6: a planet set in the Sun's rays has none - except Venus and Saturn.
The grades of 73.8-18 are a scale of means and following, "according to the standing of the family" (73.19-20).

74.21-26: in the Sudarshana wheel each house from the lagna, the Moon and the Sun rules one year in turn
(the first year the 1st house, the thirteenth year the 1st again)."""
import json, os

_P = json.load(open(os.path.join(os.path.dirname(__file__), "..", "data", "rashis.json")))["planets"]
RAYS = {"Sun": 10, "Moon": 9, "Mars": 5, "Mercury": 5, "Jupiter": 7, "Venus": 8, "Saturn": 5}
GRADES = [(5, "1-5: very small means"), (10, "6-10: small means, a carrier of others' loads"), (11, "11: little money, few children"),
          (12, "12: little money"), (13, "13: (an unfavourable grade)"), (14, "14: upright, supports the family"),
          (15, "15: learned, first in the family, wealthy"), (20, "16-20: head of the clan, many dependants"),
          (23, "21-23: supports about fifty people; generous, happy"), (30, "24-30: wealthy, valued by those in power"),
          (40, "31-40: supports a hundred to a thousand people"), (50, "41-50: a ruler's standing"), (99, "above 50: the highest standing")]


def rashmi(chart):
    out, total = {}, 0.0
    for p, full in RAYS.items():
        d = chart["planets"][p]
        lon = (d["rashi"] - 1) * 30 + d["deg"]
        deb = (_P[p]["debil"]["rashi"] - 1) * 30 + _P[p]["debil"]["deg"]
        arc = (lon - deb) % 360
        if arc > 180: arc = 360 - arc
        r = arc / 30.0 * full / 6.0
        if d.get("combust") and p not in ("Venus", "Saturn"): r = 0.0
        out[p] = round(r, 2); total += r
    grade = next(g for lim, g in GRADES if total <= lim + 1e-9 or lim == 99)
    return {"planets": out, "total": round(total, 1), "grade": grade}


def sudarshana_year(chart, age_years):
    """House (1..12) ruling the running year and its sign from lagna, Moon and Sun."""
    h = int(age_years) % 12 + 1
    refs = {"lagna": chart["lagna"]["rashi"], "Moon": chart["planets"]["Moon"]["rashi"], "Sun": chart["planets"]["Sun"]["rashi"]}
    res = {}
    for k, s in refs.items():
        sg = (s - 1 + h - 1) % 12 + 1
        res[k] = {"sign": sg, "occupants": [p for p, d in chart["planets"].items() if d["rashi"] == sg]}
    distinct = len(set(refs.values()))
    return {"house": h, "by": res, "applies": distinct == 3}
