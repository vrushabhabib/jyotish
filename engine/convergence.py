"""Convergence timeline: in which months do independent timing systems agree on the same life area?

Five votes per area per month:
  V-MD  Vimshottari mahadasha lord has a strong link to the area (occupies/owns/with lord or karaka/is karaka)
  V-AD  Vimshottari antardasha lord has a strong link
  YOG   Yogini sub-period lord has a strong link
  CHA   Chara sub-period sign holds or aspects (Jaimini sign aspect) the area's chara karaka, or is the house sign / its 7th
  DT    Jupiter and Saturn both touch the house or its lord's sign (double transit)
A window is reported when at least `need` of the 5 agree. The module also reports how many of all sampled
months reach that level: if most months qualify, the window says nothing (kb Rule 8) and that is printed.
"""
from __future__ import annotations
import datetime as dt
from engine.analysis import View, sign_at, dasha_at
from engine import transits as T

AREAS = {  # houses, karakas (male), karakas (female), chara karaka
    "marriage": ((7,), ("Venus",), ("Jupiter", "Venus"), "DK"),
    "children": ((5,), ("Jupiter",), ("Jupiter",), "PK"),
    "career": ((10,), ("Sun", "Saturn", "Mercury"), ("Sun", "Saturn", "Mercury"), "AmK"),
    "money": ((2, 11), ("Jupiter",), ("Jupiter",), None),
    "home/property": ((4,), ("Mars", "Moon"), ("Mars", "Moon"), "MK"),
}
STRONG = ("occupies", "owns", "with", "is karaka")
MOV, FIX = {1, 4, 7, 10}, {2, 5, 8, 11}


def rashi_aspect(a, b):
    """Jaimini sign aspect, signs 1..12."""
    if a == b: return False
    if a in MOV: return b in FIX and (b - a) % 12 != 1
    if a in FIX: return b in MOV and (a - b) % 12 != 1
    return b not in MOV and b not in FIX


def _strong(v, p, hs, ks):
    return any(x.startswith(STRONG) for x in v.sambandha(p, hs, ks))


def _at(periods, when, key="antar"):
    for m in periods:
        if m["start"] <= when < m["end"]:
            for a in m[key]:
                if a["start"] <= when < a["end"]:
                    return m, a
            return m, None
    return None, None


def timeline(r, sex=None, years=15, need=4):
    """r = engine.report.build(...) result. Returns {area: {'windows': [...], 'share': float, 'static': [...]}}."""
    a = r["analysis"]; v: View = a["view"]
    RN = {n: i + 1 for i, n in enumerate(["Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya", "Tula", "Vrishchika", "Dhanu", "Makara", "Kumbha", "Meena"])}
    today = r["today"]; ck = a["karakas"]["seven"]
    tz = r["chart"]["input"]["local"].tzinfo
    out = {}
    for area, (hs, km, kf, ckey) in AREAS.items():
        ks = kf if sex == "F" else km
        ok = {p: _strong(v, p, hs, ks) for p in v.s}
        csigns = {sign_at(v.lag, h) for h in hs} | {sign_at(v.lag, (h + 5) % 12 + 1) for h in hs}
        kar_sign = v.s[ck[ckey]] if ckey else None
        dts = []
        for h in hs:
            dts += T.double_transit(v, h, today, today + dt.timedelta(days=int(365.25 * years)))
        rows, d = [], today
        while d < today + dt.timedelta(days=int(365.25 * years)):
            when = dt.datetime.combine(d, dt.time(12))
            vim = dasha_at(a["dasha_tree"], when.replace(tzinfo=tz))
            md, ad = vim[0]["lord"], vim[1]["lord"]
            ym, ya = _at(r["yogini"], when)
            cm, ca = _at(r["chara"]["maha"], when)
            cs = RN[ca["sign"]] if ca else None
            votes = {"V-MD": ok[md], "V-AD": ok[ad], "YOG": bool(ya) and ok[ya["lord"]],
                     "CHA": bool(cs) and (cs in csigns or (kar_sign is not None and (cs == kar_sign or rashi_aspect(cs, kar_sign)))),
                     "DT": any(w["from"] <= d <= w["to"] for w in dts)}
            rows.append((d, sum(votes.values()), votes, f"{md}-{ad}", ya["yogini"] if ya else "-", ca["sign"] if ca else "-"))
            d += dt.timedelta(days=30)
        top = max(x[1] for x in rows)
        level = need if top >= need else top           # no month reaches `need`: report the best level reached instead
        wins, run = [], None
        for d, n, votes, vd, yg, ch in rows:
            if level and n >= level:
                if run is None: run = {"from": d, "to": d, "peak": n, "systems": set(), "vimshottari": set()}
                run["to"] = d; run["peak"] = max(run["peak"], n)
                run["systems"] |= {k for k, x in votes.items() if x}; run["vimshottari"].add(vd)
            elif run:
                wins.append(run); run = None
        if run: wins.append(run)
        for w in wins:
            w["systems"] = sorted(w["systems"]); w["vimshottari"] = sorted(w["vimshottari"])
        share = sum(1 for x in rows if level and x[1] >= level) / len(rows)
        out[area] = {"windows": wins, "share": round(share, 3), "need": need, "level": level,
                     "strong_planets": [p for p, x in ok.items() if x],
                     "discriminates": share <= 0.35}
    return out
