"""Rules taken straight from the two source texts as read in the Sanskrit on 12 Nov 2026
(kb/sources/bphs/, kb/sources/phaladeepika/). Each function names its verses.

    vimshopaka(chart)            BPHS 7.17-27   twenty-point strength over the sixteen divisions
    special_lagnas(chart)        BPHS 5.2-8     bhava, hora and ghati lagna
    delivery_time(chart)         BPHS 47.3-4, 50.88-89   which part of its period a planet delivers in
    sav_blocks(av, lagna)        BPHS 72.9-10   the combined table in three blocks of houses
    good_months(av)              BPHS 70.19-21  solar months to prefer / avoid from the Sun's table
    spouse_direction(chart)      BPHS 70.35-36, PD 10.12
    star_dasha_conditions(chart) BPHS 46.17-43  which conditional star dasha Parashara would apply
    birth_conditions(chart)      BPHS 85, 92.2  births for which a rite is prescribed (named, never with the harm wording)
    fruition(chart, house, day)  PD 10.12-14, 12.25-29, 16.31-32, 35   Mantreshvara's transit triggers
    fruition_windows(...)        the same, scanned over a period
"""
from __future__ import annotations
import datetime as dt
from engine import ephemeris as E
from engine.chart import RASHI_LORD, RASHI_NAMES, varga_rashi
from engine.shadbala import compound_rel, natural_rel

SEVEN = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
# BPHS 7.22-23: weights of the sixteen divisions (sum 20)
W16 = {2: 1, 30: 1, 3: 1, 16: 2, 9: 3, 1: 3.5, 60: 4, 4: .5, 7: .5, 10: .5, 12: .5, 20: .5, 24: .5, 27: .5, 40: .5, 45: .5}
# BPHS 7.24-25
SCORE = {2: 18, 1: 15, 0: 10, -1: 7, -2: 5}
BACK_RISING = {1, 2, 4, 9, 10}          # Aries, Taurus, Cancer, Sagittarius, Capricorn (BPHS 4.6-24; PD 1.8)
BOTH_RISING = {12}
DIRECTION = {1: "east", 5: "east", 9: "east", 2: "south", 6: "south", 10: "south",
             3: "west", 7: "west", 11: "west", 4: "north", 8: "north", 12: "north"}   # PD 1.9


def _lons(chart):
    return {p: chart["planets"][p]["lon"] for p in SEVEN}


def vimshopaka(chart):
    """{planet: {'points': 0..20, 'grade': str}} - own division 20, great friend's 18, friend's 15, neutral 10,
    enemy's 7, great enemy's 5, each times the division's weight / 20. Below 5 no result, to 10 small,
    to 15 middling, above full (7.26-27)."""
    lons = _lons(chart); out = {}
    for p in SEVEN:
        tot = 0.0
        for d, w in W16.items():
            lord = RASHI_LORD[(varga_rashi(lons[p], d) if d > 1 else chart["planets"][p]["rashi"]) - 1]
            s = 20 if lord == p else SCORE[compound_rel(p, lord, lons)]
            tot += w * s / 20.0
        grade = "none" if tot < 5 else "small" if tot < 10 else "middling" if tot < 15 else "full"
        out[p] = {"points": round(tot, 1), "grade": grade}
    return out


def special_lagnas(chart):
    """Bhava lagna (one sign per 5 ghatis), hora lagna (per 2.5 ghatis), ghati lagna (per ghati), each counted
    from the Sun's longitude at sunrise (5.2-8)."""
    i = chart["input"]; jd = i["jd_ut"]
    rise, _set = E.sun_times(jd, i["lat"], i["lon"])
    if jd < rise:                                   # born before sunrise: count from the previous sunrise
        rise, _ = E.sun_times(jd - 1.0, i["lat"], i["lon"])
    hours = (jd - rise) * 24.0
    sun0 = E.body("Sun", rise)[0]
    out = {}
    for name, per_hour in (("bhava_lagna", 15.0), ("hora_lagna", 30.0), ("ghati_lagna", 75.0)):
        lon = (sun0 + hours * per_hour) % 360.0
        sg = int(lon // 30) + 1
        out[name] = {"lon": round(lon, 2), "sign": sg, "sign_name": RASHI_NAMES[sg - 1],
                     "house": (sg - chart["lagna"]["rashi"]) % 12 + 1}
    out["hours_from_sunrise"] = round(hours, 2)
    return out


def delivery_time(chart):
    """Two independent classical pointers to the part of its own period in which a planet gives:
    by the third of the sign it is in, reversed when retrograde (47.3-4), and by the rising-type of its sign -
    head-rising start, both-ways middle, back-rising end (50.88-89). 'agree' marks where both say the same."""
    out = {}
    for p, d in chart["planets"].items():
        third = ("start", "middle", "end")[min(2, int(d["deg"] // 10))]
        if d.get("retrograde"): third = {"start": "end", "middle": "middle", "end": "start"}[third]
        rising = "end" if d["rashi"] in BACK_RISING else "middle" if d["rashi"] in BOTH_RISING else "start"
        out[p] = {"by_third": third, "by_rising": rising, "agree": third == rising}
    return out


def sav_blocks(av, lagna_sign):
    """Houses 1-4, 5-8, 9-12 = the three parts of life (72.9-10): totals of the combined table."""
    sav = av["sav"]; h = lambda n: sav[(lagna_sign - 1 + n - 1) % 12]
    b = [sum(h(n) for n in rng) for rng in (range(1, 5), range(5, 9), range(9, 13))]
    return {"early": b[0], "middle": b[1], "late": b[2], "strongest": ("early", "middle", "late")[b.index(max(b))]}


def good_months(av):
    """Signs with the most and the fewest points in the Sun's own table: the solar months to prefer and to
    avoid for auspicious beginnings (70.19-20)."""
    row = av["bav"]["Sun"]; hi, lo = max(row), min(row)
    return {"prefer": [RASHI_NAMES[i] for i, x in enumerate(row) if x == hi], "prefer_points": hi,
            "avoid": [RASHI_NAMES[i] for i, x in enumerate(row) if x == lo], "avoid_points": lo}


def spouse_direction(chart):
    """Directions named by the texts: the sign of the 7th from Venus and its trines (BPHS 70.35-36); the signs of
    the 7th lord, of Venus and of a planet in the 7th (PD 10.12). A direction named by both carries more weight."""
    P = chart["planets"]; lag = chart["lagna"]["rashi"]
    s7 = (lag - 1 + 6) % 12 + 1; l7 = RASHI_LORD[s7 - 1]
    bphs = DIRECTION[(P["Venus"]["rashi"] - 1 + 6) % 12 + 1]
    pd = {DIRECTION[P[l7]["rashi"]], DIRECTION[P["Venus"]["rashi"]]} | {DIRECTION[d["rashi"]] for d in P.values() if d["rashi"] == s7}
    return {"parashara": bphs, "mantreshvara": sorted(pd), "both": bphs if bphs in pd else None}


def star_dasha_conditions(chart, day_birth, bright_half):
    """Which of Parashara's conditional star dashas has its condition met (46.17-43). Vimshottari is 'the chief'
    in every case (46.3, 46.14); the others are cross-checks only."""
    P = chart["planets"]; lag = chart["lagna"]["rashi"]; out = []
    ll = RASHI_LORD[lag - 1]
    rahu_from_ll = (P["Rahu"]["rashi"] - P[ll]["rashi"]) % 12 + 1
    if P["Rahu"]["rashi"] != lag and rahu_from_ll in (1, 4, 5, 7, 9, 10): out.append("Ashtottari (Rahu in a kendra or trine from the lagna lord, not in the lagna)")
    if (day_birth and not bright_half) or (not day_birth and bright_half): out.append("Ashtottari (day birth in the dark half / night birth in the bright half)")
    lag_lon = chart["lagna"]["lon"]
    lag_hora_sun = (int((lag_lon % 30) // 15) == 0) == (lag % 2 == 1)
    if (lag_hora_sun and bright_half) or (not lag_hora_sun and not bright_half): out.append("Shodashottari (lagna in the Sun's hora in the bright half / the Moon's in the dark half)")
    if RASHI_LORD[varga_rashi(lag_lon, 9) - 1] == "Venus": out.append("Dwadashottari (lagna in a navamsa of Venus)")
    if varga_rashi(lag_lon, 9) == lag: out.append("Shatabdika (lagna vargottama)")
    l10 = RASHI_LORD[(lag - 1 + 9) % 12]
    if P[l10]["rashi"] == (lag - 1 + 9) % 12 + 1: out.append("Chaturashiti (10th lord in the 10th)")
    l7 = RASHI_LORD[(lag - 1 + 6) % 12]
    if P[ll]["rashi"] == (lag - 1 + 6) % 12 + 1 or P[l7]["rashi"] == lag: out.append("Dwisaptati (lagna lord in the 7th or 7th lord in the lagna)")
    if P["Sun"]["rashi"] == lag: out.append("Shashtihayani (Sun in the lagna)")
    if (day_birth and lag_hora_sun) or (not day_birth and not lag_hora_sun): out.append("Shattrimshat (day birth with the Sun's hora rising / night birth with the Moon's)")
    return out


def birth_conditions(chart):
    """Conditions of BPHS ch. 85 and 92.2 that can be computed from the chart. Returned as neutral labels; the
    worksheet prints them as 'a birth for which Parashara prescribes a rite' and never the harm wording."""
    i = chart["input"]; jd = i["jd_ut"]
    sun, moon = chart["planets"]["Sun"]["lon"], chart["planets"]["Moon"]["lon"]
    el = (moon - sun) % 360.0
    tithi = int(el // 12) + 1                       # 1..30, 16-30 dark half
    frac = (el % 12) / 12.0
    out = []
    if tithi == 30: out.append("new-moon birth (ch. 86)")
    if tithi == 29: out.append("dark-fourteenth birth, part %d of 6 (ch. 87; the first part is called good)" % (int(frac * 6) + 1))
    karana = int(el // 6)                           # 0..59
    if karana >= 1 and karana <= 56 and (karana - 1) % 7 == 6: out.append("Vishti (Bhadra) karana (ch. 88)")
    if chart["planets"]["Sun"]["deg"] < 1.0 or chart["planets"]["Sun"]["deg"] > 29.0: out.append("within about a day of the Sun's entry into a sign (ch. 90)")
    # lunar-day junction: between a Purna day (5, 10, 15 / 20, 25, 30) and the next - four nadis = 1/15 of a lunar day, taken half each side
    near_end, near_start = frac > 1 - 1 / 30.0, frac < 1 / 30.0
    if (tithi % 5 == 0 and near_end) or (tithi % 5 == 1 and near_start): out.append("lunar-day junction (92.2)")
    yoga = int(((sun + moon) % 360.0) // (360.0 / 27)) + 1
    if yoga in (17, 27): out.append("Vyatipata / Vaidhriti yoga (ch. 88)")
    return {"tithi": tithi, "half": "bright" if tithi <= 15 else "dark", "conditions": out}


# ---------------------------------------------------------------------------------------------------------
# Mantreshvara's transit triggers for the fruition of a house
# ---------------------------------------------------------------------------------------------------------
_TRINE = (0, 4, 8)


def _sidereal_sign(body, day):
    jd = E.julday(dt.datetime(day.year, day.month, day.day, 6, 30, tzinfo=dt.timezone.utc))
    return int(E.body(body, jd)[0] // 30) + 1


def fruition(chart, house, day, ref="lagna"):
    """Which of the classical triggers hold on `day` for `house` counted from the lagna (or ref='moon').
    J  Jupiter in a trine of the sign or navamsa sign of the house lord            (PD 16.32; 10.14; 12.29)
    L  the lagna lord in a trine of the house lord's sign, or in the house itself  (PD 16.31; 10.13)
    H  the house lord in a trine of the lagna lord's sign, or in the lagna         (PD 16.31)
    M  the two lords in one sign or in opposite signs in transit                   (PD 16.35)
    Returns {'J':bool,'L':bool,'H':bool,'M':bool,'count':n}. Same-planet cases (house 1, or one planet owning
    both) count L, H and M as not applicable (False)."""
    P = chart["planets"]
    base = chart["lagna"]["rashi"] if ref == "lagna" else P["Moon"]["rashi"]
    hs = (base - 1 + house - 1) % 12 + 1
    hl, ll = RASHI_LORD[hs - 1], RASHI_LORD[base - 1]
    s_hl, n_hl = P[hl]["rashi"], varga_rashi(P[hl]["lon"], 9)
    js = _sidereal_sign("Jupiter", day)
    J = (js - s_hl) % 12 in _TRINE or (js - n_hl) % 12 in _TRINE
    L = H = M = False
    if hl != ll:
        ls, hsn = _sidereal_sign(ll, day), _sidereal_sign(hl, day)
        L = (ls - s_hl) % 12 in _TRINE or ls == hs
        H = (hsn - P[ll]["rashi"]) % 12 in _TRINE or hsn == base
        M = (ls - hsn) % 12 in (0, 6)
    return {"J": J, "L": L, "H": H, "M": M, "count": J + L + H + M}


def fruition_windows(chart, house, start, end, need=3, step_days=7, ref="lagna"):
    """Stretches between start and end in which at least `need` of the four triggers hold together.
    [(from, to, peak_count)]. EXPERIMENTAL: classical, not validated - see kb/sources/ANALYSIS.md."""
    out, cur, d = [], None, start
    while d <= end:
        n = fruition(chart, house, d, ref)["count"]
        if n >= need:
            cur = [cur[0], d, max(cur[2], n)] if cur else [d, d, n]
        elif cur:
            out.append(tuple(cur)); cur = None
        d += dt.timedelta(days=step_days)
    if cur: out.append(tuple(cur))
    return out
