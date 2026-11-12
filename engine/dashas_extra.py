"""Yogini, Jaimini Chara (K.N. Rao method) and Ashtottari dashas.

Validated 12 Nov 2026 against the AstroSage printout (tests/test_dashas_extra.py): Yogini period ends, all twelve
Chara mahadasha lengths and the antardasha order. AstroSage prints Aquarius as "-1 Year" for the reference chart,
a missing wrap-around in its own code; the rule gives 11.

Chara rules used (kb/dashas/dasha-systems.md section 4):
  - order of mahadashas: forward from the lagna when the lagna is Aries, Leo, Virgo, Libra, Aquarius or Pisces, else backward;
  - years: count from the sign to its lord (forward for Aries, Taurus, Gemini, Libra, Scorpio, Sagittarius; backward
    for the rest), minus one; lord in the sign = 12; no exaltation/debilitation adjustment (Rao);
  - Scorpio (Mars/Ketu) and Aquarius (Saturn/Rahu): the lord outside the sign; if both outside, the one with more
    companions, then the exalted one, then the one giving more years (the last two are flagged when they decide);
  - antardashas: twelve equal parts, starting from the sign next to the mahadasha sign in the MAHADASHA SIGN'S OWN
    direction, the mahadasha sign itself last (this is what AstroSage prints).
"""
from __future__ import annotations
import datetime as dt

YEAR = 365.25
RASHI = ["Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya", "Tula", "Vrishchika", "Dhanu", "Makara", "Kumbha", "Meena"]
YOGINI = [("Mangala", "Moon", 1), ("Pingala", "Sun", 2), ("Dhanya", "Jupiter", 3), ("Bhramari", "Mars", 4),
          ("Bhadrika", "Mercury", 5), ("Ulka", "Saturn", 6), ("Siddha", "Venus", 7), ("Sankata", "Rahu", 8)]
NAK = 360.0 / 27
SEQ_DIRECT = {0, 4, 5, 6, 10, 11}
COUNT_FWD = {0, 1, 2, 6, 7, 8}
LORD = {0: "Mars", 1: "Venus", 2: "Mercury", 3: "Moon", 4: "Sun", 5: "Mercury", 6: "Venus", 7: ("Mars", "Ketu"),
        8: "Jupiter", 9: "Saturn", 10: ("Saturn", "Rahu"), 11: "Jupiter"}
EXALT = {"Sun": 0, "Moon": 1, "Mars": 9, "Mercury": 5, "Jupiter": 3, "Venus": 11, "Saturn": 6, "Rahu": 1, "Ketu": 7}


def _add(t, years):
    return t + dt.timedelta(days=years * YEAR)


def yogini(moon_lon, birth, cycles=3):
    """[{yogini, lord, start, end, antar:[{yogini, lord, start, end}]}] - 36-year cycle."""
    n = int(moon_lon // NAK) + 1
    r = (n + 3) % 8
    i = (r - 1) % 8 if r else 7
    left = 1 - (moon_lon % NAK) / NAK
    out, t = [], birth
    first = True
    for k in range(8 * cycles):
        name, lord, yrs = YOGINI[(i + k) % 8]
        full_start = _add(t, -yrs * (1 - left)) if first else t
        end = _add(full_start, yrs)
        antar, a = [], full_start
        for j in range(8):
            an, al, ay = YOGINI[(i + k + j) % 8]
            ae = _add(a, yrs * ay / 36.0)
            if ae > t:
                antar.append({"yogini": an, "lord": al, "start": max(a, t), "end": ae})
            a = ae
        out.append({"yogini": name, "lord": lord, "years": yrs, "start": t, "end": end, "antar": antar})
        t, first = end, False
    return out


def _chara_years(sign, signs_of, notes, bphs_adjust=False):
    """signs_of: {planet: sign index 0..11}. bphs_adjust: +1 year lord exalted, -1 debilitated (BPHS 46.165)."""
    y, who = _chara_base(sign, signs_of, notes)
    if bphs_adjust and who:
        if signs_of[who] == EXALT[who]: y += 1
        elif signs_of[who] == (EXALT[who] + 6) % 12: y -= 1
    return y


def _chara_base(sign, signs_of, notes):
    lord = LORD[sign]
    who = None
    if isinstance(lord, tuple):
        a, b = lord
        sa, sb = signs_of[a], signs_of[b]
        if sa == sign and sb == sign:
            return 12, None
        if sa == sign: target = sb
        elif sb == sign: target = sa
        elif sa == sb: target = sa
        else:
            comp = lambda p: sum(1 for q, s in signs_of.items() if q != p and s == signs_of[p])
            n = lambda s: ((s - sign) % 12 if sign in COUNT_FWD else (sign - s) % 12)
            nature = lambda s: s % 3          # 0 movable, 1 fixed, 2 dual: rising strength (BPHS 46.163)
            if comp(a) != comp(b):
                target = sa if comp(a) > comp(b) else sb
            elif nature(sa) != nature(sb):
                target = sa if nature(sa) > nature(sb) else sb
                notes.append(f"{RASHI[sign]}: co-lord chosen by strength of sign (BPHS 46.163)")
            elif (EXALT[a] == sa) != (EXALT[b] == sb):
                target = sa if EXALT[a] == sa else sb
                notes.append(f"{RASHI[sign]}: co-lord chosen by exaltation (secondary rule)")
            else:
                target = sa if n(sa) >= n(sb) else sb
                notes.append(f"{RASHI[sign]}: co-lord chosen by larger count (tertiary rule; sources differ)")
        who = a if target == sa else b
    else:
        target, who = signs_of[lord], lord
    if target == sign:
        return 12, who
    return ((target - sign) % 12 if sign in COUNT_FWD else (sign - target) % 12), who


def chara(lagna_sign, signs_of, birth, cycles=1, bphs_adjust=False):
    """lagna_sign and signs_of use 1..12 (engine convention). Returns {'maha': [...], 'notes': [...]}."""
    lag = lagna_sign - 1
    so = {p: s - 1 for p, s in signs_of.items()}
    notes = []
    step = 1 if lag in SEQ_DIRECT else -1
    out, t = [], birth
    for c in range(cycles):
        for k in range(12):
            s = (lag + step * k) % 12
            y = _chara_years(s, so, notes, bphs_adjust)
            if c: y = 12 - y if y != 12 else 12
            end = _add(t, y)
            d = 1 if s in SEQ_DIRECT else -1
            antar, a = [], t
            for j in range(1, 13):
                asg = (s + d * j) % 12
                ae = _add(a, y / 12.0)
                antar.append({"sign": RASHI[asg], "start": a, "end": ae}); a = ae
            out.append({"sign": RASHI[s], "years": y, "start": t, "end": end, "antar": antar})
            t = end
    return {"maha": out, "notes": sorted(set(notes)),
            "method": ("Parashara 46.155-167 with the one-year exaltation/debilitation change of 46.165" if bphs_adjust else
                       "K.N. Rao: no exaltation/debilitation adjustment (BPHS 46.165 gives +1/-1; pass bphs_adjust=True); "
                       "antardasha direction by the mahadasha sign")}


ASHTOTTARI = [("Sun", 6, 4), ("Moon", 15, 3), ("Mars", 8, 4), ("Mercury", 17, 3), ("Saturn", 10, 3),
              ("Jupiter", 19, 3), ("Rahu", 12, 4), ("Venus", 21, 3)]


def ashtottari(moon_lon, birth):
    """Continuous-arc method (P.V.R. Narasimha Rao), arcs starting at Ardra (66d40'). Secondary system only."""
    x = (moon_lon - 5 * NAK) % 360.0
    i, start = 0, 0.0
    while True:
        arc = ASHTOTTARI[i][2] * NAK
        if x < start + arc: break
        start += arc; i += 1
    left = 1 - (x - start) / arc
    out, t = [], birth
    for k in range(8):
        lord, yrs, _ = ASHTOTTARI[(i + k) % 8]
        end = _add(t, yrs * (left if k == 0 else 1))
        out.append({"lord": lord, "years": yrs, "start": t, "end": end}); t = end
    return out


def applicable_ashtottari(rahu_house_from_lagna_lord, rahu_house, day_birth, paksha):
    """The two classical conditions; use the system only as a cross-check when at least one holds."""
    c1 = rahu_house != 1 and rahu_house_from_lagna_lord in (1, 4, 5, 7, 9, 10)
    c2 = (day_birth and paksha.lower().startswith("k")) or ((not day_birth) and paksha.lower().startswith("s"))
    return {"rahu_condition": c1, "paksha_condition": c2, "use": c1 or c2}
