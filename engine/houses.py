"""House cusps: Placidus (used by KP) and Sripati (Bhava Chalit), plus KP significators.

Validated 12 Nov 2026 against the AstroSage printout in tests/test_houses.py (all 12 KP cusps and the
Sripati mid-points). Whole-sign houses remain the basis of every Parashari judgement in this project;
these cusps are for KP analysis and for the Chalit cross-check only.
"""
from __future__ import annotations
import math
from engine import ephemeris as E

SIGN_LORD = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]
DASHA_SEQ = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
DASHA_YRS = {"Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7, "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17}
NAK = 360.0 / 27


def kp_ayanamsa(jd):
    """KP 'New' ayanamsa (the AstroSage default): 22d22'16.4" at 1900.0 plus 50.2388475" a year."""
    years = (jd - 2415020.0) / 365.2422
    return (22 + 22 / 60 + 16.4 / 3600) + years * 50.2388475 / 3600


def _lon_of_ra(ra, eps):
    return math.degrees(math.atan2(math.sin(ra), math.cos(ra) * math.cos(eps))) % 360.0


def placidus_tropical(jd, lat, lon):
    """Twelve tropical Placidus cusps (index 0 = cusp 1)."""
    eps = math.radians(E.obliquity(jd))
    phi = math.radians(lat)
    ramc = (E._gmst_deg(jd) + lon) % 360.0
    r = math.radians(ramc)
    asc = math.degrees(math.atan2(math.cos(r), -(math.sin(r) * math.cos(eps) + math.tan(phi) * math.sin(eps)))) % 360.0
    mc = math.degrees(math.atan2(math.sin(r), math.cos(r) * math.cos(eps))) % 360.0

    def cusp(offset, frac, diurnal):
        ra = math.radians(ramc + offset)
        for _ in range(60):
            lam = math.radians(_lon_of_ra(ra, eps))
            dec = math.asin(math.sin(eps) * math.sin(lam))
            x = max(-1.0, min(1.0, math.tan(phi) * math.tan(dec)))
            ad = math.degrees(math.asin(x))
            new = ramc + frac * (90 + ad) if diurnal else ramc + 180 - frac * (90 - ad)
            new = math.radians(new)
            if abs(new - ra) < 1e-10:
                break
            ra = new
        return _lon_of_ra(ra, eps)

    c = [0.0] * 12
    c[0], c[9] = asc, mc
    c[10] = cusp(30, 1 / 3, True)
    c[11] = cusp(60, 2 / 3, True)
    c[1] = cusp(120, 2 / 3, False)
    c[2] = cusp(150, 1 / 3, False)
    for i, j in ((6, 0), (3, 9), (4, 10), (5, 11), (7, 1), (8, 2)):
        c[i] = (c[j] + 180.0) % 360.0
    return c


def kp_cusps(jd, lat, lon):
    ay = kp_ayanamsa(jd)
    return [(x - ay) % 360.0 for x in placidus_tropical(jd, lat, lon)]


def sripati(jd, lat, lon):
    """Bhava Chalit (Sripati): mid-points by trisecting the asc-MC arcs, beginnings half-way between
    mid-points. Lahiri sidereal. Returns [{house, begin, mid}]."""
    asc, mc = E.angles(jd, lat, lon)
    ic, desc = (mc + 180) % 360, (asc + 180) % 360
    mids = [0.0] * 12
    for start, a, b in ((0, asc, ic), (3, ic, desc), (6, desc, mc), (9, mc, asc)):
        arc = (b - a) % 360.0
        for k in range(3):
            mids[start + k] = (a + arc * k / 3) % 360.0
    out = []
    for i in range(12):
        prev = mids[i - 1]
        begin = (prev + ((mids[i] - prev) % 360.0) / 2) % 360.0
        out.append({"house": i + 1, "begin": begin, "mid": mids[i]})
    return out


def chalit_house(lon, bhavas):
    for i in range(12):
        a, b = bhavas[i]["begin"], bhavas[(i + 1) % 12]["begin"]
        if (lon - a) % 360.0 < (b - a) % 360.0:
            return i + 1
    return 12


def lords(lon, levels=3):
    """Sign lord is separate; this gives star / sub / sub-sub lords of a longitude in the zodiac it is given in."""
    n = int(lon // NAK)
    star = DASHA_SEQ[n % 9]
    out = [star]
    pos, span, start = lon - n * NAK, NAK, DASHA_SEQ.index(star)
    for _ in range(levels - 1):
        i = start
        while True:
            w = span * DASHA_YRS[DASHA_SEQ[i % 9]] / 120.0
            if pos < w - 1e-12:
                break
            pos -= w; i += 1
        out.append(DASHA_SEQ[i % 9]); span, start = w, i % 9
    return out


def kp_chart(jd, lat, lon):
    """KP view: cusps with sign/star/sub lords, planets with house (Placidus) and lords, four-level significators."""
    ay_l, ay_k = E.ayanamsa(jd), kp_ayanamsa(jd)
    cusps = kp_cusps(jd, lat, lon)
    shift = ay_l - ay_k
    pos = E.positions(jd, lat, lon)
    planets = {}
    for p in E.BODIES:
        x = (pos[p]["lon"] + shift) % 360.0
        h = next(i + 1 for i in range(12) if (x - cusps[i]) % 360.0 < (cusps[(i + 1) % 12] - cusps[i]) % 360.0)
        st, sub, ss = lords(x)
        planets[p] = {"lon": x, "house": h, "sign_lord": SIGN_LORD[int(x // 30)], "star": st, "sub": sub, "subsub": ss}
    cz = {}
    for i, x in enumerate(cusps):
        st, sub, ss = lords(x)
        cz[i + 1] = {"lon": x, "sign_lord": SIGN_LORD[int(x // 30)], "star": st, "sub": sub, "subsub": ss}
    owner = {p: [h for h in cz if cz[h]["sign_lord"] == p] for p in E.BODIES}
    occ = {h: [p for p in E.BODIES if planets[p]["house"] == h] for h in cz}
    house_sig = {}
    for h in cz:
        own = cz[h]["sign_lord"]
        house_sig[h] = {
            "A_in_star_of_occupants": [p for p in E.BODIES if planets[p]["star"] in occ[h]],
            "B_occupants": occ[h],
            "C_in_star_of_owner": [p for p in E.BODIES if planets[p]["star"] == own],
            "D_owner": [own]}
    planet_sig = {}
    for p in E.BODIES:
        st = planets[p]["star"]
        hs = [planets[st]["house"]] + [planets[p]["house"]] + owner[st] + owner[p]
        planet_sig[p] = sorted(set(hs))
    return {"ayanamsa": ay_k, "cusps": cz, "planets": planets, "house_significators": house_sig,
            "planet_significations": planet_sig}
