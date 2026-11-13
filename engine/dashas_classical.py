"""Two classical period systems that were in the texts but not in the engine (built 13 Nov 2026).

1. KALACHAKRA dasha - BPHS 46.52-100, Jataka Parijata ch. 17. Periods of SIGNS, set by the quarter of the Moon's star.
   The sixteen sequences are from our own decoding of BPHS (kb/sources/bphs/ch46-50.md). Three places where the copy was
   damaged (Ashvini-group quarter 2, and one number-word each in Bharani 3 and Rohini 2) are filled so that each sequence
   adds up to the total the text itself states for it (100, 85, 83 or 86 years, BPHS 46.89) - tests/test_classical_dashas.py
   checks all sixteen. Conventions NOT in the verses read, flagged in the output:
     - what follows after the nine signs of the birth quarter (we continue with the next quarter of the zodiac);
     - the order of sub-periods (we start from the dasha sign and follow the same sequence).

2. LIFE-SPAN dasha - Brihat Jataka ch. 7-8, Vriddha Yavana Jataka ch. 6, Jataka Parijata 5.2-16. Each planet (and the lagna)
   rules a period equal to the share of life it "gives". USED FOR PERIODS ONLY: this module never returns or prints a total,
   and the project never states a length of life. Varahamihira himself objects that the spans do not match real lives (BJ 7.7-8).
   Conventions that are ours or from general practice, flagged in the output:
     - when several reductions apply to one planet only the largest is taken;
     - the reduction for a malefic rising (Jataka Parijata 5.11-13) is NOT applied - the verse is damaged in our copy;
     - the lagna's strength is taken as its lord's; sub-period order follows the dasha order.
   Nothing here has been cross-checked against an independent calculation.
"""
from __future__ import annotations
import datetime as dt
from engine.chart import RASHI_LORD, RASHI_NAMES

KC_YEARS = {"Sun": 5, "Moon": 21, "Mars": 7, "Mercury": 9, "Jupiter": 10, "Venus": 16, "Saturn": 4}
KC_SEQ = {("A", 1): [1, 2, 3, 4, 5, 6, 7, 8, 9], ("A", 2): [10, 11, 12, 8, 7, 6, 4, 5, 3], ("A", 3): [2, 1, 12, 11, 10, 9, 1, 2, 3], ("A", 4): [4, 5, 6, 7, 8, 9, 10, 11, 12],
          ("B", 1): [8, 7, 6, 4, 5, 3, 2, 1, 12], ("B", 2): [11, 10, 9, 1, 2, 3, 4, 5, 6], ("B", 3): [7, 8, 9, 10, 11, 12, 8, 7, 6], ("B", 4): [4, 5, 3, 2, 1, 12, 11, 10, 9],
          ("R", 1): [9, 10, 11, 12, 1, 2, 3, 5, 4], ("R", 2): [6, 7, 8, 12, 11, 10, 9, 8, 7], ("R", 3): [6, 5, 4, 3, 2, 1, 9, 10, 11], ("R", 4): [12, 1, 2, 3, 5, 4, 6, 7, 8],
          ("M", 1): [12, 11, 10, 9, 8, 7, 6, 5, 4], ("M", 2): [3, 2, 1, 9, 10, 11, 12, 1, 2], ("M", 3): [3, 5, 4, 6, 7, 8, 12, 11, 10], ("M", 4): [9, 8, 7, 6, 5, 4, 3, 2, 1]}
KC_TOTAL = {("A", 1): 100, ("A", 2): 85, ("A", 3): 83, ("A", 4): 86, ("B", 1): 100, ("B", 2): 85, ("B", 3): 83, ("B", 4): 86,
            ("R", 1): 86, ("R", 2): 83, ("R", 3): 85, ("R", 4): 100, ("M", 1): 86, ("M", 2): 83, ("M", 3): 85, ("M", 4): 100}
KC_GROUP = {}
for g, stars in (("A", (1, 3, 7, 9, 13, 15, 19, 21, 25, 27)), ("B", (2, 8, 14, 20, 26)), ("R", (4, 10, 16, 22)), ("M", (5, 6, 11, 12, 17, 18, 23, 24))):
    for s in stars: KC_GROUP[s] = g
KC_DIRECT = {"A": True, "B": True, "R": False, "M": False}
JUMPS = {(6, 4): "frog jump", (4, 6): "frog jump", (5, 3): "frog jump", (3, 5): "frog jump", (4, 5): "back-going", (5, 4): "back-going",
         (12, 8): "lion's glance", (8, 12): "lion's glance", (9, 1): "lion's glance", (1, 9): "lion's glance"}
YEAR = 365.25
PADA = 360 / 108


def _yrs(sign): return KC_YEARS[RASHI_LORD[sign - 1]]


def kalachakra(moon_lon, birth, horizon_years=110):
    """Sign periods from birth. Returns {'quarter': {...}, 'periods': [{sign, start, end, cycle, jump, subs:[...]}], 'notes': [...]}"""
    idx = int((moon_lon % 360) // PADA); frac = ((moon_lon % 360) % PADA) / PADA
    t = birth; out = []; cyc = 0; elapsed_first = None
    while (t - birth).days < horizon_years * YEAR:
        star, pada = idx // 4 + 1, idx % 4 + 1; key = (KC_GROUP[star], pada); seq = KC_SEQ[key]; total = KC_TOTAL[key]
        skip = frac * total if cyc == 0 else 0.0
        if cyc == 0: elapsed_first = skip
        acc = 0.0
        for i, sg in enumerate(seq):
            y = _yrs(sg); a0, a1 = acc, acc + y; acc = a1
            if a1 <= skip: continue
            start = t; length = a1 - max(a0, skip); end = start + dt.timedelta(days=length * YEAR)
            full_start = start - dt.timedelta(days=(max(a0, skip) - a0) * YEAR)
            subs = []; s0 = full_start
            for j in range(9):
                sub = seq[(i + j) % 9]; sl = y * _yrs(sub) / total
                s1 = s0 + dt.timedelta(days=sl * YEAR)
                if s1 > start: subs.append({"sign": sub, "start": max(s0, start), "end": s1})
                s0 = s1
            prev = out[-1]["sign"] if out else (seq[i - 1] if i else None)
            out.append({"sign": sg, "name": RASHI_NAMES[sg - 1], "lord": RASHI_LORD[sg - 1], "start": start, "end": end, "cycle": cyc + 1,
                        "jump": JUMPS.get((prev, sg)) if prev else None, "subs": subs})
            t = end
        idx = (idx + 1) % 108; cyc += 1
    q0 = int((moon_lon % 360) // PADA); star, pada = q0 // 4 + 1, q0 % 4 + 1; key = (KC_GROUP[star], pada)
    seq = KC_SEQ[key]; d = KC_DIRECT[key[0]]
    return {"quarter": {"star": star, "pada": pada, "group": key[0], "direct": d, "sequence": seq,
                        "body_sign": seq[0] if d else seq[-1], "life_sign": seq[-1] if d else seq[0], "fraction_elapsed": round(frac, 4)},
            "periods": out,
            "notes": ["Sensitive to birth time: the Moon moves one star-quarter in about 6 hours, and the balance shifts by up to "
                      f"{KC_TOTAL[key] / (PADA / 13.18 * 24 * 60):.2f} years per minute of birth time.",
                      "Periods marked cycle 2 or later rest on a continuation rule that is NOT in the verses we read.",
                      "Order of sub-periods is our convention. Sub-period lengths follow Jataka Parijata 17.107-108.",
                      "The text's reading: the sign's house from the lagna gives the subject and direction (BPHS 46.131-154); untested by us."]}


def kalachakra_at(kc, when):
    for p in kc["periods"]:
        if p["start"] <= when < p["end"]:
            sub = next((s for s in p["subs"] if s["start"] <= when < s["end"]), None)
            return p, sub
    return None, None


# ---------------------------------------------------------------------------------------------- life-span dasha
PINDA = {"Sun": 19, "Moon": 25, "Mars": 15, "Mercury": 12, "Jupiter": 15, "Venus": 21, "Saturn": 20}       # Brihat Jataka 7.1
EX_LON = {"Sun": 10, "Moon": 33, "Mars": 298, "Mercury": 165, "Jupiter": 95, "Venus": 357, "Saturn": 200}  # exaltation points
BENEFIC = ("Moon", "Mercury", "Jupiter", "Venus")
CUT_BY_HOUSE = {12: 1.0, 11: 1 / 2, 10: 1 / 3, 9: 1 / 4, 8: 1 / 5, 7: 1 / 6}                                # Jataka Parijata 5.9


def lifespan_dasha(chart, strength, when=None, ahead_years=25):
    """Periods of the life-span dasha that fall between birth and `when` + ahead_years. NEVER returns the total.
    strength: {planet: rupas} (Shadbala). Returns {'order': [...], 'periods': [...], 'notes': [...], 'ended': bool}"""
    P = chart["planets"]; lag = chart["lagna"]; lsign = lag["rashi"]
    birth = chart["input"]["local"]; when = when or dt.datetime.now(birth.tzinfo)
    house = lambda sign, ref: (sign - ref) % 12 + 1
    share, why = {}, {}
    by_sign = {}
    for p in PINDA: by_sign.setdefault(P[p]["rashi"], []).append(p)
    for p, yrs in PINDA.items():
        d = (P[p]["lon"] - EX_LON[p]) % 360; arc = 360 - d if d < 180 else d          # Jataka Parijata 5.4-5
        base = yrs * arc / 360
        cuts = {}
        dg = P[p]["dignity"].lower()
        if "enemy" in dg and p != "Mars" and not P[p].get("retrograde"): cuts["enemy's sign"] = 1 / 3
        if P[p].get("combust") and p not in ("Venus", "Saturn"): cuts["combust"] = 1 / 2
        h = house(P[p]["rashi"], lsign)
        if h in CUT_BY_HOUSE:
            mates = by_sign[P[p]["rashi"]]
            if len(mates) == 1 or p == max(mates, key=lambda q: strength.get(q, 0)):
                cuts[f"house {h}"] = CUT_BY_HOUSE[h] * (0.5 if p in BENEFIC else 1.0)
        cut = max(cuts.values()) if cuts else 0.0
        share[p] = base * (1 - cut); why[p] = max(cuts, key=cuts.get) if cuts else None
    share["Lagna"] = (lag["lon"] % 30) / (30 / 9)                                      # navamsas risen = years
    st = dict(strength); st["Lagna"] = strength.get(RASHI_LORD[lsign - 1], 0)
    sign_of = {p: P[p]["rashi"] for p in PINDA}; sign_of["Lagna"] = lsign
    first = max(("Lagna", "Sun", "Moon"), key=lambda q: st.get(q, 0))
    grp = lambda q: {1: 0, 4: 0, 7: 0, 10: 0, 2: 1, 5: 1, 8: 1, 11: 1}.get(house(sign_of[q], sign_of[first]), 2)
    rest = sorted((q for q in share if q != first), key=lambda q: (grp(q), -st.get(q, 0), -share[q]))
    order = [first] + rest
    lim = when + dt.timedelta(days=ahead_years * YEAR); t = birth; out = []; ended = True
    for q in order:
        end = t + dt.timedelta(days=share[q] * YEAR)
        w = {}
        for r in order:                                                               # Brihat Jataka 8.3-4
            hh = house(sign_of[r], sign_of[q])
            w[r] = 1.0 if r == q else 1 / 2 if hh == 1 else 1 / 3 if hh in (5, 9) else 1 / 4 if hh in (4, 8) else 1 / 7 if hh == 7 else 0.0
        tot = sum(w.values()); subs = []; s0 = t
        for r in [q] + [x for x in order if x != q]:
            if not w[r]: continue
            s1 = s0 + dt.timedelta(days=share[q] * w[r] / tot * YEAR); subs.append({"lord": r, "start": s0, "end": s1}); s0 = s1
        if t <= lim:
            out.append({"lord": q, "start": t, "end": min(end, lim) if end > lim else end, "runs_past_window": end > lim,
                        "reduction": why.get(q), "subs": [s for s in subs if s["start"] <= lim]})
        if end > when: ended = False
        t = end
        if t > lim: break
    return {"order": order, "periods": out, "ended_before_date": ended,
            "notes": ["Periods only. No total is computed for display and no length of life is ever stated (project rule; Varahamihira's own objection, Brihat Jataka 7.7-8).",
                      "If the sequence has run out before the date asked, the method is simply not usable for this chart - it says nothing about the person.",
                      "Only the largest single reduction is applied to a planet; the malefic-rising reduction is not applied (damaged verse); the lagna's strength is taken as its lord's; sub-period order is ours.",
                      "Not cross-checked against any independent calculation. Untested by our control test."]}


def lifespan_at(ls, when):
    for p in ls["periods"]:
        if p["start"] <= when < p["end"] or (p["runs_past_window"] and p["start"] <= when):
            return p, next((s for s in p["subs"] if s["start"] <= when < s["end"]), None)
    return None, None
