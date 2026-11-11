"""Gochar (transits): sign ingress tables, Sade Sati and other Saturn phases, the double transit of
Jupiter and Saturn (K.N. Rao's timing method), nodal and planetary returns.

All dates are computed from engine.ephemeris, daily resolution (the ingress day is exact to +/-1 day).
"""
from __future__ import annotations
import datetime as dt
from functools import lru_cache
from engine import ephemeris as E
from engine.chart import RASHI_NAMES, RASHI_LORD
from engine.analysis import ASPECTS, hfrom, sign_at


@lru_cache(maxsize=200000)
def _sign(body, ordinal):
    d = dt.datetime.fromordinal(ordinal) + dt.timedelta(hours=6, minutes=30)      # 12:00 IST
    return int(E.body(body, E.julday(d))[0] // 30) + 1


def sign_on(body, day: dt.date):
    return _sign(body, day.toordinal())


def periods(body, start: dt.date, end: dt.date):
    """[(sign 1..12, first day, last day)] for the body's stay in each sign, retrograde re-entries included."""
    step = 7 if body in ("Saturn", "Jupiter", "Rahu", "Ketu") else 1
    out = []; d = start; cur = sign_on(body, d); begin = d
    while d < end:
        nxt = min(d + dt.timedelta(days=step), end)
        s = sign_on(body, nxt)
        if s != cur:
            a = d                                           # refine to the day
            while sign_on(body, a + dt.timedelta(days=1)) == cur:
                a += dt.timedelta(days=1)
            out.append((cur, begin, a)); begin = a + dt.timedelta(days=1); cur = sign_on(body, begin)
            d = begin
        else:
            d = nxt
    out.append((cur, begin, end))
    return out


def saturn_phases(moon_sign, start, end):
    """Sade Sati (12th, 1st, 2nd from Moon), Kantaka/Ardhashtama (4th), Ashtama (8th), with dates."""
    names = {12: "Sade Sati - rising (12th from Moon)", 1: "Sade Sati - peak (over Moon)", 2: "Sade Sati - setting (2nd from Moon)",
             4: "Ardhashtama / Kantaka Shani (4th from Moon)", 8: "Ashtama Shani (8th from Moon)"}
    return [{"phase": names[hfrom(s, moon_sign)], "sign": RASHI_NAMES[s - 1], "from": a, "to": b}
            for s, a, b in periods("Saturn", start, end) if hfrom(s, moon_sign) in names]


def sade_sati_spans(moon_sign, start, end):
    """Whole Sade Sati cycles (first entry into the 12th to final exit from the 2nd)."""
    ph = [p for p in saturn_phases(moon_sign, start, end) if p["phase"].startswith("Sade")]
    spans = []
    for p in ph:
        if spans and (p["from"] - spans[-1][1]).days < 400:
            spans[-1][1] = p["to"]
        else:
            spans.append([p["from"], p["to"]])
    return [(a, b) for a, b in spans]


def _touches(body, tsign, target):
    return tsign == target or hfrom(target, tsign) in ASPECTS[body]


def double_transit(view, house, start, end, include_lord=True, ref=None):
    """Windows when Jupiter and Saturn BOTH occupy or aspect the house (or the sign of its lord).
    K.N. Rao: an event of a house needs this double activation within the running dasha."""
    ref = ref or view.lag
    targets = {sign_at(ref, house)}
    if include_lord:
        targets.add(view.s[RASHI_LORD[sign_at(ref, house) - 1]])
    out = []; d = start; run = None
    while d <= end:
        j, s = sign_on("Jupiter", d), sign_on("Saturn", d)
        hit = [t for t in targets if _touches("Jupiter", j, t)] and [t for t in targets if _touches("Saturn", s, t)]
        both_house = _touches("Jupiter", j, sign_at(ref, house)) and _touches("Saturn", s, sign_at(ref, house))
        if hit:
            if run is None: run = [d, d, both_house]
            run[1] = d; run[2] = run[2] or both_house
        elif run:
            out.append(run); run = None
        d += dt.timedelta(days=3)
    if run: out.append(run)
    return [{"from": a, "to": b, "on_house_itself": h} for a, b, h in out if (b - a).days >= 9]


def house_table(view, body, start, end):
    """Transit periods with the house from lagna and from Moon."""
    moon = view.s["Moon"]
    return [{"sign": RASHI_NAMES[s - 1], "from": a, "to": b, "house": hfrom(s, view.lag), "house_from_moon": hfrom(s, moon)}
            for s, a, b in periods(body, start, end)]


def returns(view, birth: dt.date, upto: dt.date):
    """Sign-level returns of Saturn, Jupiter and Rahu to their natal signs (first entry dates)."""
    out = {}
    for body in ("Saturn", "Jupiter", "Rahu"):
        nat = view.s[body]
        per = periods(body, birth, upto)
        left = next((i for i, x in enumerate(per) if x[0] != nat), len(per))
        hits = [a for s, a, b in per[left:] if s == nat]
        first = []
        for h in hits:
            if not first or (h - first[-1]).days > 700: first.append(h)
        out[body] = first
    return out
