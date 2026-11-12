"""The last group of rules from Parashara that the worksheet did not compute (read in the Sanskrit, 12 Nov 2026;
notes in kb/sources/bphs/). Each function names its verses. Everything here is description of the chart -
nothing in this module is a prediction, and none of it has a track record in the project's ledger.

    nine_states(chart)        BPHS 45.7-9    blazing, at ease, glad, calm, poor, distressed, crippled, wicked, angry
    six_moods(chart)          BPHS 45.11-18  ashamed, proud, hungry, thirsty, glad, agitated
    argala(chart)             BPHS 31.2-18   intervention on each house and its obstruction
    upagrahas(chart)          BPHS 3.61-74   the five non-luminous points, Gulika and its companions, Pranapada
    sudarshana_table(chart)   BPHS 74.21-26  the year-by-year table of the three rings
"""
from __future__ import annotations
import datetime as dt
from engine import ephemeris as E
from engine.chart import RASHI_LORD, RASHI_NAMES
from engine.shadbala import compound_rel, natural_rel
from engine.analysis import aspects_sign, EXALT, OWN

SEVEN = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
NINE = SEVEN + ["Rahu", "Ketu"]
MALEFIC = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}
BENEFIC = {"Jupiter", "Venus", "Mercury", "Moon"}
WATERY = {4, 8, 12}                                   # Cancer, Scorpio, Pisces
MALEFIC_SIGNS = {1, 8, 5, 10, 11}                     # signs of Mars, the Sun and Saturn


def _S(chart):
    return {p: chart["planets"][p]["rashi"] for p in NINE}


def _lons(chart):
    return {p: chart["planets"][p]["lon"] for p in SEVEN}


def nine_states(chart):
    """BPHS 45.7-9. The first six go by the sign the planet is in (exactly one applies); the last three are
    added when their own condition holds. 'A house gives results according to the state of the planet in it' (45.10)."""
    S = _S(chart); lons = _lons(chart); out = {}
    for p in SEVEN:
        s = S[p]; lord = RASHI_LORD[s - 1]
        if s == EXALT[p]: base = "blazing (exalted)"
        elif s in OWN[p]: base = "at ease (own sign)"
        else:
            r = compound_rel(p, lord, lons)
            base = {2: "glad (great friend's sign)", 1: "calm (friend's sign)", 0: "poor (neutral sign)"}.get(r, "distressed (enemy's sign)")
        extra = []
        if any(q != p and S[q] == s for q in MALEFIC - {"Sun"}): extra.append("crippled (with a malefic)")
        if s in MALEFIC_SIGNS and s not in OWN[p]: extra.append("wicked (in a malefic's sign)")
        if p != "Sun" and S["Sun"] == s: extra.append("angry (with the Sun)")
        out[p] = {"state": base, "also": extra}
    return out


def six_moods(chart):
    """BPHS 45.11-17. A planet can carry several moods at once ('mixed states give mixed results', 45.19).
    45.18: a hungry or agitated planet harms the house it sits in - returned as 'harms_house'."""
    S = _S(chart); lag = chart["lagna"]["rashi"]; lons = _lons(chart); out = {}
    asp = lambda q, p: q != p and S[q] != S[p] and aspects_sign(q, S[q], S[p])
    for p in SEVEN:
        s = S[p]; house = (s - lag) % 12 + 1; lord = RASHI_LORD[s - 1]
        others = [q for q in SEVEN if q != p]
        enemies = [q for q in others if natural_rel(p, q) < 0]
        friends = [q for q in others if natural_rel(p, q) > 0]
        with_ = lambda q: q != p and S[q] == s
        moods = []
        if house == 5 and any(with_(q) for q in ("Rahu", "Ketu", "Sun", "Saturn", "Mars")): moods.append("ashamed")
        if s == EXALT[p] or chart["planets"][p].get("dignity") == "Moolatrikona": moods.append("proud")
        if (lord != p and natural_rel(p, lord) < 0) or any(with_(q) or asp(q, p) for q in enemies) or with_("Saturn"): moods.append("hungry")
        if s in WATERY and any(asp(q, p) for q in enemies) and not any(asp(b, p) for b in BENEFIC): moods.append("thirsty")
        if (lord != p and natural_rel(p, lord) > 0) or any(with_(q) or asp(q, p) for q in friends) or with_("Jupiter"): moods.append("glad")
        if with_("Sun") and any(asp(m, p) for m in MALEFIC) and any(asp(q, p) for q in enemies): moods.append("agitated")
        out[p] = {"house": house, "moods": moods, "harms_house": bool({"hungry", "agitated"} & set(moods)) and "glad" not in moods and "proud" not in moods}
    return out


ARGALA_RESULT = {1: "fame and fortune", 2: "wealth and grain", 3: "happiness from siblings", 4: "house, vehicles, relatives",
                 5: "children and intelligence", 6: "trouble from opponents", 7: "wealth and married happiness", 8: "hardship",
                 9: "rise of fortune", 10: "honour from those in authority", 11: "gains", 12: "heavy expense"}


def argala(chart):
    """BPHS 31. For each house from the lagna: planets in the 2nd, 4th, 11th (and 5th) from it intervene;
    planets in the 12th, 10th, 3rd (and 9th) obstruct, but only when they are not fewer (31.4). Three or more
    malefics in the 3rd make an argala of their own (31.4-5). One planet = weak, two = middling, more = best (31.7).
    Strength of the planets ('weaker', 31.4) is not weighed here - counts only."""
    S = _S(chart); lag = chart["lagna"]["rashi"]; out = {}
    at = lambda sign: [p for p in NINE if S[p] == sign]
    for h in range(1, 13):
        base = (lag - 1 + h - 1) % 12 + 1
        f = lambda n: at((base - 1 + n - 1) % 12 + 1)
        formed, blocked = [], []
        for a, o in ((2, 12), (4, 10), (11, 3), (5, 9)):
            A, O = f(a), f(o)
            if not A: continue
            (blocked if O and len(O) >= len(A) else formed).append({"from": a, "planets": A, "obstructed_by": O})
        m3 = [p for p in f(3) if p in MALEFIC]
        if len(m3) >= 3: formed.append({"from": 3, "planets": m3, "obstructed_by": [], "reverse": True})
        pl = [p for x in formed for p in x["planets"]]
        kind = None
        if pl:
            b = sum(1 for p in pl if p in BENEFIC); m = len(pl) - b
            kind = "benefic" if m == 0 else "malefic" if b == 0 else "mixed"
        out[h] = {"formed": formed, "blocked": blocked, "planets": pl, "kind": kind,
                  "grade": None if not pl else "weak" if len(pl) == 1 else "middling" if len(pl) == 2 else "best",
                  "matter": ARGALA_RESULT[h]}
    out["lagna_5_9_together"] = all(out[h]["planets"] for h in (1, 5, 9))          # 31.18
    return out


_WEEK = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]         # weekday lords from Sunday
# rows Sunday..Saturday; columns Mandi, Yamakantaka, Ardhaprahara, Kala (PD 25.2-4)
PD_GHATI_ROW = [(26, 18, 14, 2), (22, 14, 10, 26), (18, 10, 6, 22), (14, 6, 2, 18), (10, 2, 26, 14), (6, 26, 22, 10), (2, 22, 18, 6)]
_PART_NAME = {"Saturn": "Gulika", "Sun": "Kala", "Mars": "Mrityu", "Jupiter": "Yamaghantaka", "Mercury": "Ardhaprahara"}


def upagrahas(chart):
    """BPHS 3.61-74.
    Non-luminous points (61-65): Dhuma = Sun + 133d20'; Vyatipata = 360 - Dhuma; Parivesha = Vyatipata + 180;
    Indrachapa = 360 - Parivesha; Upaketu = Indrachapa + 16d40'.
    Gulika and companions (66-70): the day (sunrise-sunset) or night in eight parts, ruled in weekday order from the
    lord of the day (night: from the fifth lord), the eighth part lordless; the sign rising in Saturn's part is Gulika.
    The verse does not say which moment of the part - both the start and the end are returned. Mantreshvara
    (PD 25.2-4) does say: fixed ghatis that fall just before the end of the part - returned as 'mandi_group_pd'.
    Pranapada (71-74): time since sunrise in vighatis / 15 = signs, added to the Sun (movable sign), to the 9th from
    the Sun (fixed) or the 5th (dual). It moves one sign every six minutes: usable only with a rectified time."""
    i = chart["input"]; jd = i["jd_ut"]; lat, lon = i["lat"], i["lon"]; lag = chart["lagna"]["rashi"]
    def pt(x):
        x %= 360.0; sg = int(x // 30) + 1
        return {"lon": round(x, 2), "sign": sg, "sign_name": RASHI_NAMES[sg - 1], "house": (sg - lag) % 12 + 1}
    sun = chart["planets"]["Sun"]["lon"]
    dhuma = sun + 133 + 20 / 60.0; vy = 360 - dhuma; pari = vy + 180; indra = 360 - pari; upak = indra + 16 + 40 / 60.0
    out = {"non_luminous": {"Dhuma": pt(dhuma), "Vyatipata": pt(vy), "Parivesha": pt(pari), "Indrachapa": pt(indra), "Upaketu": pt(upak)}}
    rise, sset = E.sun_times(jd, lat, lon)
    if jd < rise:                                       # before sunrise: the night of the previous Vedic day
        prise, pset = E.sun_times(jd - 1.0, lat, lon)
        start, end, day, ref_rise = pset, rise, False, prise
    elif jd < sset:
        start, end, day, ref_rise = rise, sset, True, rise
    else:
        nrise, _ = E.sun_times(jd + 1.0, lat, lon)
        start, end, day, ref_rise = sset, nrise, False, rise
    local_rise = E.jd_to_datetime(ref_rise) + (i["local"].utcoffset() or dt.timedelta(0))
    wd = (local_rise.weekday() + 1) % 7                  # Monday=0 -> index in _WEEK (Sunday=0)
    first = wd if day else (wd + 4) % 7
    part = (end - start) / 8.0
    parts = {}
    for k in range(7):
        lord = _WEEK[(first + k) % 7]
        if lord in _PART_NAME:
            a0 = E.angles(start + k * part, lat, lon)[0]; a1 = E.angles(start + (k + 1) * part, lat, lon)[0]
            parts[_PART_NAME[lord]] = {"part": k + 1, "at_start": pt(a0), "at_end": pt(a1)}
    out["gulika_group"] = parts; out["day_birth"] = day
    # Phaladeepika 25.2-4 (letter-number code decoded 12 Nov 2026): ghatis after sunrise, for a 30-ghati day, at which
    # each point rises on Sunday..Saturday; scaled to the real length of the day; by night counted from sunset
    # starting with the fifth weekday lord. These fall just before the END of the planet's eighth-part.
    row = PD_GHATI_ROW[wd if day else (wd + 4) % 7]
    out["mandi_group_pd"] = {nm: dict(pt(E.angles(start + (end - start) * g / 30.0, lat, lon)[0]), ghatis=g)
                             for nm, g in zip(("Mandi", "Yamakantaka", "Ardhaprahara", "Kala"), row)}
    since = (jd - ref_rise) * 86400.0                    # seconds since sunrise; one vighati = 24 s
    signs = since / 24.0 / 15.0
    ss = chart["planets"]["Sun"]["rashi"]
    add = 0 if ss % 3 == 1 else 240 if ss % 3 == 2 else 120
    pp = pt(sun + add + signs * 30.0)
    pp["good_place"] = pp["house"] in (2, 4, 10, 11)     # 3.74
    out["pranapada"] = pp
    return out


def sudarshana_table(chart, from_age, years=12):
    """BPHS 74.21-26: each year of life belongs to one house, counted in turn from the lagna, the Moon and the Sun.
    Returns one row per year with the sign and its occupants in each ring. 74.3-5: the three rings are read
    together only when lagna, Moon and Sun are in three different signs."""
    refs = {"lagna": chart["lagna"]["rashi"], "Moon": chart["planets"]["Moon"]["rashi"], "Sun": chart["planets"]["Sun"]["rashi"]}
    rows = []
    for age in range(int(from_age), int(from_age) + years):
        h = age % 12 + 1; row = {"year_of_life": age + 1, "house": h}
        for k, s in refs.items():
            sg = (s - 1 + h - 1) % 12 + 1
            occ = [p for p in NINE if chart["planets"][p]["rashi"] == sg]
            ben = [p for p in occ if p in BENEFIC]; mal = [p for p in occ if p in MALEFIC]
            row[k] = {"sign": RASHI_NAMES[sg - 1], "occupants": occ,
                      "tone": "helped" if ben and not mal else "pressed" if mal and not ben else "mixed" if occ else "empty"}
        rows.append(row)
    return {"rows": rows, "applies": len(set(refs.values())) == 3}


SHAYANADI = ["lying down", "sitting", "eyes and hands", "shining", "going", "coming", "in assembly", "arriving",
             "eating", "wishing to dance", "eager", "sleeping"]


def activity_states(chart):
    """BPHS 45.30-39: twelve activity states. (star number of the planet x planet's number x its navamsa number in
    the sign) + birth star + ghati of birth + lagna number, divided by 12; remainder 1 = lying down ... 0 = sleeping.
    NOT used in readings and not printed in the worksheet: the verse's 'ghati' can be read as elapsed or running
    (this function takes the running one), the result changes every 24 minutes of birth time, and the three
    sub-states need the first sound of the person's name."""
    i = chart["input"]; jd = i["jd_ut"]
    rise, _ = E.sun_times(jd, i["lat"], i["lon"])
    if jd < rise: rise, _ = E.sun_times(jd - 1.0, i["lat"], i["lon"])
    ghati = int((jd - rise) * 60.0) + 1
    moon_star = int(chart["planets"]["Moon"]["lon"] // (360.0 / 27)) + 1
    out = {}
    for n, p in enumerate(SEVEN + ["Rahu", "Ketu"], 1):
        lon = chart["planets"][p]["lon"]
        star = int(lon // (360.0 / 27)) + 1; nav = int((lon % 30) // (30.0 / 9)) + 1
        r = (star * n * nav + moon_star + ghati + chart["lagna"]["rashi"]) % 12
        out[p] = SHAYANADI[(r - 1) % 12]
    return out
