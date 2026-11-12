"""Shadbala (six-fold planetary strength) and Bhava Bala.

Follows BPHS ch. 27 as worked out in B.V. Raman, "Graha and Bhava Balas", with the variant
choices that reproduce an AstroSage printout (birth 24 Nov 1996 12:05 IST, Hubli) -- see
tests/test_shadbala.py for the reference numbers and tolerances, and VARIANTS below for each choice.

All strengths are in virupas (shashtiamsas); 60 virupas = 1 rupa.

API
    shadbala(date_str, time_str, lat, lon, tz_off=5.5, compat=None)  -> dict
    bhava_bala(date_str, time_str, lat, lon, tz_off=5.5, compat=None) -> dict
    compat="astrosage" additionally reproduces two AstroSage quirks that are NOT classical rules
    (see ASTROSAGE_QUIRKS); leave it None for normal use.
CLI
    python3 -m engine.shadbala YYYY-MM-DD HH:MM LAT LON [TZ_OFFSET] [--astrosage]

Sources consulted (formulas are the classical ones; the URL is where each was cross-read):
    [BPHS]   Brihat Parasara Hora Sastra ch. 27 (Santhanam tr.)  https://archive.org/details/ParasharaHoraSastra
    [RAMAN]  B.V. Raman, Graha and Bhava Balas                    https://archive.org/details/GrahaAndBhavaBalas
    [PVR]    P.V.R. Narasimha Rao, Vedic Astrology: An Integrated Approach (free textbook)
             https://www.vedicastrologer.org/articles/  (Shadbala chapter; Jagannatha Hora option notes)
    [VM]     https://varahamihira.blogspot.com/2004/07/strength-of-planets-shadbala-i.html
             (Sarajit Poddar's summary: sthana / kala bala rules, Sun cheshta = ayana, Moon cheshta = paksha)
    [PYJH]   https://github.com/naturalstupid/PyJHora/blob/main/src/jhora/horoscope/chart/strength.py
             (open-source re-implementation of Raman's book: his Table I ahargana base "1951 -> 174 days",
              the weekday offset for abda/masa lords, and the full-strength Mercury/Jupiter rule in bhava drishti)
"""
from __future__ import annotations

import datetime as dt
import math

from engine import ephemeris as eph

PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
SIGN_LORD = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]

# What was chosen where software differs, and why (each reproduces the AstroSage reference chart).
VARIANTS = {
    "saptavargaja": "Raman scale 45/30/22.5/15/7.5/3.75/1.875; moolatrikona = the whole moolatrikona SIGN and only "
                    "in D1 (degree ranges ignored; own sign in the other six vargas = 30); compound (panchadha) "
                    "friendship taken from the rasi chart for every varga; Parashara hora (Leo/Cancer); "
                    "trimsamsa lords mapped to their odd/even sign",
    "kendradi": "by whole-sign house from the lagna sign",
    "dig": "arc from the weak point (true MC / IC / lagna / descendant), /3",
    "nathonnata": "measured from true local midnight (midpoint of sunset..sunrise), i.e. noon = (sunrise+sunset)/2",
    "paksha": "Moon-Sun elongation/3 for benefics, complement for malefics; Moon's own value plain per BPHS 27.10-11 (doubled only with compat='raman'); "
              "Mercury malefic when it is in the same sign as a natural malefic; Moon always benefic here",
    "tribhaga": "day/night divided in three from actual sunrise/sunset; Jupiter always 60",
    "abda_masa": "Raman's ahargana (his Table I count: 174 on 31 Dec 1951), 360-day years and 30-day months; "
                 "lord index = (years*3 + 1) resp. (months*2 + 1) mod 7 counted from Tuesday",
    "vara": "weekday reckoned from sunrise",
    "hora": "24 one-hour horas from sunrise, first = weekday lord [RAMAN]",
    "ayana": "kranti from Raman's 15-degree bhuja table (362,703,1002,1238,1388,1440 arc-min) of the tropical "
             "longitude, i.e. latitude ignored; (24 +/- kranti)/48*60; Mercury always +; Sun doubled",
    "cheshta": "Sun: (tropical longitude + 90) reduced to 0..180, /3.  Moon: = paksha bala.  "
               "Others: cheshta kendra = seeghrocha - (mean + true)/2, reduced, /3",
    "drik": "BPHS drishti-pinda curve with Mars/Jupiter/Saturn special aspects; (benefic - malefic)/4 for "
            "every planet, Mercury and Jupiter included",
    "naisargika": "exact sevenths of 60 (AstroSage prints them rounded to 8.58 steps, <= 0.03 off)",
    "bhava": "lord by lagna-sign whole-sign count; dig by the sign class of the Sripati bhava-madhya; drishti on "
             "the bhava-madhya with Mercury and Jupiter at full strength and the other five at one quarter [RAMAN]",
}

# AstroSage behaviours that look like implementation quirks rather than rules.  Only applied with compat="astrosage".
ASTROSAGE_QUIRKS = {
    "dwadasamsa_boundary": "D12 part is taken from degrees.minutes read as a decimal number (27 deg 33' -> 27.33), so a "
                           "planet up to ~0.4 deg past a 2.5-degree boundary stays in the previous dwadasamsa. Inferred "
                           "from the printed Shodashvarga table (Moon 27Ar34 -> Aquarius, Venus 7Li41 -> Sagittarius).",
    "hora_previous": "Hora bala goes to the lord of the hora BEFORE the one running at birth (birth 5h29m after "
                     "sunrise on a Sunday = Jupiter's hora, AstroSage credits Saturn). CONJECTURE from one chart.",
}

# ----------------------------------------------------------------------------------------------
# small helpers
# ----------------------------------------------------------------------------------------------

def _norm(x):
    return x % 360.0


def _arc(a, b):
    """Shortest arc between two longitudes, 0..180."""
    d = abs(a - b) % 360.0
    return 360.0 - d if d > 180.0 else d


def _sign(lon):
    return int(_norm(lon) // 30)


def _jd(date_str, time_str, tz_off):
    local = dt.datetime.fromisoformat(f"{date_str}T{time_str}")
    return eph.julday(local - dt.timedelta(hours=tz_off))


# ----------------------------------------------------------------------------------------------
# vargas  [BPHS ch. 6; cross-read in PVR ch. on divisional charts]
# ----------------------------------------------------------------------------------------------

def varga_sign(lon, d, compat=None):
    """Sign index (0 = Mesha) of a longitude in the divisional chart D-d (d in 1,2,3,7,9,12,30)."""
    lon = _norm(lon)
    s, deg = int(lon // 30), lon % 30
    if d == 12 and compat == "astrosage":
        deg = int(deg) + int((deg % 1) * 60 + 1e-9) / 100.0
    odd = s % 2 == 0                        # Mesha, Mithuna ... are odd signs
    if d == 1:
        return s
    if d == 2:                               # Parashara hora: odd sign 1st half Sun (Simha), 2nd Moon (Karka)
        first = deg < 15
        return 4 if (odd == first) else 3
    if d == 3:
        return (s + 4 * int(deg // 10)) % 12
    if d == 7:
        k = int(deg // (30 / 7))
        return (s + k) % 12 if odd else (s + 6 + k) % 12
    if d == 9:
        k = int(deg // (30 / 9))
        start = [0, 9, 6, 3][s % 4]         # fire->Mesha, earth->Makara, air->Tula, water->Karka
        return (start + k) % 12
    if d == 12:
        return (s + int(deg // 2.5)) % 12
    if d == 30:
        # odd: 5 Mars, 5 Saturn, 8 Jupiter, 7 Mercury, 5 Venus ; even: 5 Venus, 7 Mercury, 8 Jupiter, 5 Saturn, 5 Mars
        if odd:
            for lim, sg in ((5, 0), (10, 10), (18, 8), (25, 2), (30, 6)):
                if deg < lim:
                    return sg
        else:
            for lim, sg in ((5, 1), (12, 5), (20, 11), (25, 9), (30, 7)):
                if deg < lim:
                    return sg
    raise ValueError(d)


# ----------------------------------------------------------------------------------------------
# friendships  [BPHS ch. 3 sl. 55-58; table also printed in the AstroSage report]
# ----------------------------------------------------------------------------------------------
_F = {  # natural friends / enemies; anything else is neutral
    "Sun": (("Moon", "Mars", "Jupiter"), ("Venus", "Saturn")),
    "Moon": (("Sun", "Mercury"), ()),
    "Mars": (("Sun", "Moon", "Jupiter"), ("Mercury",)),
    "Mercury": (("Sun", "Venus"), ("Moon",)),
    "Jupiter": (("Sun", "Moon", "Mars"), ("Mercury", "Venus")),
    "Venus": (("Mercury", "Saturn"), ("Sun", "Moon")),
    "Saturn": (("Mercury", "Venus"), ("Sun", "Moon", "Mars")),
}


def natural_rel(p, q):
    fr, en = _F[p]
    return 1 if q in fr else (-1 if q in en else 0)


def temporal_rel(p, q, lons):
    """+1 if q is in the 2,3,4,10,11,12th sign from p in the rasi chart, else -1."""
    h = (_sign(lons[q]) - _sign(lons[p])) % 12 + 1
    return 1 if h in (2, 3, 4, 10, 11, 12) else -1


def compound_rel(p, q, lons):
    """-2 adhisatru .. +2 adhimitra."""
    return natural_rel(p, q) + temporal_rel(p, q, lons)


# ----------------------------------------------------------------------------------------------
# 1. STHANA BALA   [BPHS 27.1-6; RAMAN ch. 3]
# ----------------------------------------------------------------------------------------------
EXALT = {"Sun": 10.0, "Moon": 33.0, "Mars": 298.0, "Mercury": 165.0, "Jupiter": 95.0, "Venus": 357.0, "Saturn": 200.0}
# moolatrikona: sign index, from deg, to deg (the degree range is informational; see VARIANTS["saptavargaja"])
MOOLA = {"Sun": (4, 0, 20), "Moon": (1, 3, 30), "Mars": (0, 0, 12), "Mercury": (5, 15, 20),
         "Jupiter": (8, 0, 10), "Venus": (6, 0, 15), "Saturn": (10, 0, 20)}
_SV_SCALE = {2: 22.5, 1: 15.0, 0: 7.5, -1: 3.75, -2: 1.875}
SAPTAVARGA = (1, 2, 3, 7, 9, 12, 30)


def uchcha_bala(p, lon):
    return _arc(lon, EXALT[p] + 180.0) / 3.0


def saptavargaja_bala(p, lons, detail=None, compat=None):
    total = 0.0
    for d in SAPTAVARGA:
        sg = varga_sign(lons[p], d, compat)
        lord = SIGN_LORD[sg]
        if d == 1 and sg == MOOLA[p][0]:
            v = 45.0
        elif lord == p:
            v = 30.0
        else:
            v = _SV_SCALE[compound_rel(p, lord, lons)]
        if detail is not None:
            detail[f"D{d}"] = v
        total += v
    return total


def ojayugma_bala(p, lon):
    """Moon and Venus gain in even sign / even navamsa, the rest in odd; 15 each."""
    want_even = p in ("Moon", "Venus")
    v = 0.0
    for d in (1, 9):
        even = varga_sign(lon, d) % 2 == 1
        if even == want_even:
            v += 15.0
    return v


def kendradi_bala(p, lon, lagna):
    h = (_sign(lon) - _sign(lagna)) % 12 + 1
    return 60.0 if h in (1, 4, 7, 10) else (30.0 if h in (2, 5, 8, 11) else 15.0)


def drekkana_bala(p, lon):
    """Male (Sun, Mars, Jupiter) 1st decanate, neuter (Mercury, Saturn) 2nd, female (Moon, Venus) 3rd."""
    k = int((lon % 30) // 10)
    want = 0 if p in ("Sun", "Mars", "Jupiter") else (1 if p in ("Mercury", "Saturn") else 2)
    return 15.0 if k == want else 0.0


# ----------------------------------------------------------------------------------------------
# 2. DIG BALA   [BPHS 27.7-7.5; RAMAN ch. 4]
# ----------------------------------------------------------------------------------------------

def dig_bala(p, lon, lagna, mc):
    """Arc from the point of zero strength, /3.  Sun, Mars strong on MC; Moon, Venus on IC;
    Mercury, Jupiter on lagna; Saturn on the descendant."""
    weak = {"Sun": mc + 180, "Mars": mc + 180, "Moon": mc, "Venus": mc,
            "Mercury": lagna + 180, "Jupiter": lagna + 180, "Saturn": lagna}[p]
    return _arc(lon, weak) / 3.0


# ----------------------------------------------------------------------------------------------
# 3. KALA BALA   [BPHS 27.8-20; RAMAN ch. 5]
# ----------------------------------------------------------------------------------------------
WEEKDAY_LORD = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]       # 0 = Sunday
HORA_SEQ = ["Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars"]            # descending speed order
KRANTI_TABLE = [0, 362, 703, 1002, 1238, 1388, 1440]                                  # arc-min at bhuja 0,15..90 [RAMAN]
RAMAN_AHARGANA_EPOCH_JDN = 2433838          # civil JDN on which Raman's Table I count is 0 (31 Dec 1951 -> 174) [PYJH]


def _civil_jdn(jd_ut, tz_off):
    """Julian day number of the local civil date."""
    return int(math.floor(jd_ut + tz_off / 24.0 + 0.5))


def kranti_raman(trop_lon):
    """Declination of the ecliptic point (deg, signed) by linear interpolation in Raman's table."""
    trop_lon = _norm(trop_lon)
    bhuja = trop_lon % 180.0
    if bhuja > 90.0:
        bhuja = 180.0 - bhuja
    i = min(int(bhuja // 15), 5)
    k = KRANTI_TABLE[i] + (KRANTI_TABLE[i + 1] - KRANTI_TABLE[i]) * (bhuja - 15 * i) / 15.0
    return (k / 60.0) * (1 if trop_lon < 180.0 else -1)


def is_benefic(p, lons, moon_rule="always"):
    """Natural benefic / malefic for Paksha and Drik bala."""
    if p in ("Jupiter", "Venus"):
        return True
    if p in ("Sun", "Mars", "Saturn"):
        return False
    if p == "Moon":
        if moon_rule == "always":
            return True
        return _norm(lons["Moon"] - lons["Sun"]) < 180.0 if moon_rule == "waxing" else \
            90.0 <= _norm(lons["Moon"] - lons["Sun"]) <= 270.0
    # Mercury: malefic when joined (same sign) with a natural malefic
    for m in ("Sun", "Mars", "Saturn", "Rahu", "Ketu"):
        if m in lons and _sign(lons[m]) == _sign(lons["Mercury"]):
            return False
    return True


def day_context(jd, lat, lon, tz_off):
    """Sunrise/sunset bracketing the birth, day/night flag, fraction elapsed, weekday from sunrise."""
    rise, sset = eph.sun_times(jd, lat, lon)
    if jd < rise:                                   # before sunrise: belongs to the previous Hindu day
        prise, pset = eph.sun_times(jd - 1.0, lat, lon)
        ctx = dict(is_day=False, start=pset, end=rise, day_rise=prise)
    elif jd < sset:
        ctx = dict(is_day=True, start=rise, end=sset, day_rise=rise)
    else:
        nrise, _ = eph.sun_times(jd + 1.0, lat, lon)
        ctx = dict(is_day=False, start=sset, end=nrise, day_rise=rise)
    ctx["frac"] = (jd - ctx["start"]) / (ctx["end"] - ctx["start"])
    ctx["sunrise"], ctx["sunset"] = rise, sset
    # civil weekday (local zone) of the sunrise that began this Hindu day
    ctx["jdn"] = _civil_jdn(ctx["day_rise"], tz_off)
    ctx["weekday"] = (ctx["jdn"] + 1) % 7              # 0 = Sunday
    ctx["hours_from_sunrise"] = (jd - ctx["day_rise"]) * 24.0
    # true local noon / midnight from the sunrise-sunset midpoint
    noon = (rise + sset) / 2.0
    ctx["from_midnight_deg"] = 180.0 - min(abs(jd - noon), 1.0 - abs(jd - noon)) * 360.0
    return ctx


def nathonnata_bala(p, ctx):
    unnata = ctx["from_midnight_deg"] / 3.0            # 60 at noon, 0 at midnight
    if p == "Mercury":
        return 60.0
    return unnata if p in ("Sun", "Jupiter", "Venus") else 60.0 - unnata


def paksha_bala(p, lons):
    el = _arc(lons["Moon"], lons["Sun"]) / 3.0
    return el if is_benefic(p, lons) else 60.0 - el


def tribhaga_bala(p, ctx):
    if p == "Jupiter":
        return 60.0
    part = min(int(ctx["frac"] * 3), 2)
    lord = (("Mercury", "Sun", "Saturn") if ctx["is_day"] else ("Moon", "Venus", "Mars"))[part]
    return 60.0 if p == lord else 0.0


def abda_masa_lords(ctx):
    """Year and month lords from Raman's ahargana [RAMAN ch. 5; constants as transcribed in PYJH].
    The savana year has 360 days and the month 30; successive year lords advance 3 weekdays and successive
    month lords 2.  Raman: (ahargana // 360) * 3 + 1 and (ahargana // 30) * 2 + 1, each mod 7, the remainder
    counted with 0 = Tuesday.  The ahargana is taken for the Hindu day (sunrise to sunrise) of birth."""
    ahar = ctx["jdn"] - RAMAN_AHARGANA_EPOCH_JDN
    abda = WEEKDAY_LORD[(((ahar // 360) * 3 + 1) % 7 + 2) % 7]
    masa = WEEKDAY_LORD[(((ahar // 30) * 2 + 1) % 7 + 2) % 7]
    return abda, masa, ahar


def hora_lord(ctx, compat=None):
    h = int(ctx["hours_from_sunrise"])
    if compat == "astrosage":
        h -= 1                                          # ASTROSAGE_QUIRKS["hora_previous"]
    return HORA_SEQ[(HORA_SEQ.index(WEEKDAY_LORD[ctx["weekday"]]) + h) % 7]


def ayana_bala(p, lon, ay):
    k = kranti_raman(lon + ay)
    if p == "Mercury":
        v = (24.0 + abs(k)) * 1.25
    elif p in ("Moon", "Saturn"):
        v = (24.0 - k) * 1.25
    else:
        v = (24.0 + k) * 1.25
    return 2.0 * v if p == "Sun" else v


DISC_DIAMETER = {"Mars": 9.4, "Mercury": 6.6, "Jupiter": 190.4, "Venus": 16.6, "Saturn": 158.0}   # arc-sec [RAMAN]


def yuddha_bala(lons, partial):
    """Planetary war between two of Mars..Saturn within 1 degree [BPHS 27.20; RAMAN ch. 5].
    The difference of their strengths so far (sthana + dig + kala up to hora), divided by the difference of
    disc diameters, is added to the winner (the one with the lower longitude, i.e. to the north in Raman's
    simplification) and taken from the loser."""
    out = {p: 0.0 for p in PLANETS}
    ps = ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    for i, a in enumerate(ps):
        for b in ps[i + 1:]:
            if _arc(lons[a], lons[b]) < 1.0:
                diff = abs(partial[a] - partial[b]) / abs(DISC_DIAMETER[a] - DISC_DIAMETER[b])
                win, lose = (a, b) if _norm(lons[b] - lons[a]) < 180.0 else (b, a)
                out[win] += diff
                out[lose] -= diff
    return out


# ----------------------------------------------------------------------------------------------
# 4. CHESHTA BALA   [BPHS 27.21-23; RAMAN ch. 6; PVR for the Sun/Moon convention]
# ----------------------------------------------------------------------------------------------
_MEAN = {  # tropical mean longitudes, deg and deg/Julian century from J2000 (Meeus, Astronomical Algorithms ch. 31)
    "Sun": (280.46646, 36000.76983), "Mercury": (252.250906, 149474.0722491), "Venus": (181.979801, 58519.2130302),
    "Mars": (355.433, 19141.6964471), "Jupiter": (34.351519, 3036.3027748), "Saturn": (50.077444, 1223.5110686),
}


def mean_longitude(name, jd):
    l0, rate = _MEAN[name]
    return _norm(l0 + rate * (jd - 2451545.0) / 36525.0)


def cheshta_bala(p, lons, jd, ay, paksha_moon):
    if p == "Sun":
        return _arc(lons["Sun"] + ay + 90.0, 0.0) / 3.0
    if p == "Moon":
        return paksha_moon
    msun = mean_longitude("Sun", jd) - ay
    if p in ("Mercury", "Venus"):
        mean, seeghra = msun, mean_longitude(p, jd) - ay
    else:
        mean, seeghra = mean_longitude(p, jd) - ay, msun
    true = lons[p]
    # average of mean and true along the shorter arc
    avg = mean + ((true - mean + 180.0) % 360.0 - 180.0) / 2.0
    return _arc(seeghra, avg) / 3.0


# ----------------------------------------------------------------------------------------------
# 5. NAISARGIKA BALA   [BPHS 27.24]
# ----------------------------------------------------------------------------------------------
NAISARGIKA = {p: 60.0 * k / 7.0 for k, p in enumerate(["Saturn", "Mars", "Mercury", "Jupiter", "Venus", "Moon", "Sun"], 1)}

# ----------------------------------------------------------------------------------------------
# 6. DRIK BALA   [BPHS ch. 26 (drishti), 27.25; RAMAN ch. 7]
# ----------------------------------------------------------------------------------------------

def drishti(aspector, from_lon, to_lon, special=True):
    """Aspect strength in virupas (0..60) cast by `aspector` at from_lon on the point to_lon."""
    a = _norm(to_lon - from_lon)
    if a < 30:
        v = 0.0
    elif a < 60:
        v = (a - 30) / 2
    elif a < 90:
        v = (a - 60) + 15
    elif a < 120:
        v = (120 - a) / 2 + 30
    elif a < 150:
        v = 150 - a
    elif a < 180:
        v = (a - 150) * 2
    elif a < 300:
        v = (300 - a) / 2
    else:
        v = 0.0
    if special:
        if aspector == "Mars" and (90 <= a < 120 or 210 <= a < 240):
            v += 15
        elif aspector == "Jupiter" and (120 <= a < 150 or 240 <= a < 270):
            v += 30
        elif aspector == "Saturn" and (60 <= a < 90 or 270 <= a < 300):
            v += 45
    return v


def drik_bala(p, lons):
    s = 0.0
    for q in PLANETS:
        if q == p:
            continue
        v = drishti(q, lons[q], lons[p])
        s += v if is_benefic(q, lons) else -v
    return s / 4.0


# ----------------------------------------------------------------------------------------------
# assembly
# ----------------------------------------------------------------------------------------------
REQUIRED_RUPAS = {"Sun": 5.0, "Moon": 6.0, "Mars": 5.0, "Mercury": 7.0, "Jupiter": 6.5, "Venus": 5.5, "Saturn": 5.0}


def _chart(date_str, time_str, lat, lon, tz_off):
    jd = _jd(date_str, time_str, tz_off)
    pos = eph.positions(jd, lat, lon)
    lons = {k: v["lon"] for k, v in pos.items()}
    return jd, eph.ayanamsa(jd), lons, pos


def shadbala(date_str, time_str, lat, lon, tz_off=5.5, compat=None):
    """Six-fold strength of the seven planets.

    Returns {"planets": {name: {...components..., "total", "rupas", "required", "ratio", "rank"}},
             "order": [strongest..weakest by ratio], "context": {...}, "variants": VARIANTS, "unverified": [...]}.
    """
    jd, ay, lons, pos = _chart(date_str, time_str, lat, lon, tz_off)
    lagna, mc = lons["Lagna"], lons["MC"]
    ctx = day_context(jd, lat, lon, tz_off)
    abda, masa, ahar = abda_masa_lords(ctx)
    vara = WEEKDAY_LORD[ctx["weekday"]]
    hora = hora_lord(ctx, compat)
    paksha_moon = paksha_bala("Moon", lons)

    out, partial = {}, {}
    for p in PLANETS:
        sv_detail = {}
        sth = {
            "uchcha": uchcha_bala(p, lons[p]),
            "saptavargaja": saptavargaja_bala(p, lons, sv_detail, compat),
            "ojayugma": ojayugma_bala(p, lons[p]),
            "kendradi": kendradi_bala(p, lons[p], lagna),
            "drekkana": drekkana_bala(p, lons[p]),
        }
        kala = {
            "nathonnata": nathonnata_bala(p, ctx),
            # BPHS 27.10-11 (read in Sanskrit 12 Nov 2026) gives the Moon the plain value. Raman doubles it and his
            # worked example needs the doubling: use compat="raman" to reproduce him.
            "paksha": paksha_bala(p, lons) * (2.0 if p == "Moon" and compat == "raman" else 1.0),
            "tribhaga": tribhaga_bala(p, ctx),
            "abda": 15.0 if p == abda else 0.0,
            "masa": 30.0 if p == masa else 0.0,
            "vara": 45.0 if p == vara else 0.0,
            "hora": 60.0 if p == hora else 0.0,
            "ayana": ayana_bala(p, lons[p], ay),
        }
        d = {"sthana": sth, "sthana_total": sum(sth.values()), "saptavarga_detail": sv_detail,
             "dig": dig_bala(p, lons[p], lagna, mc), "kala": kala}
        partial[p] = d["sthana_total"] + d["dig"] + sum(kala.values())
        out[p] = d
    yud = yuddha_bala(lons, partial)
    for p in PLANETS:
        d = out[p]
        d["kala"]["yuddha"] = yud[p]
        d["kala_total"] = sum(d["kala"].values())
        d["cheshta"] = cheshta_bala(p, lons, jd, ay, paksha_moon)
        d["naisargika"] = NAISARGIKA[p]
        d["drik"] = drik_bala(p, lons)
        d["total"] = d["sthana_total"] + d["dig"] + d["kala_total"] + d["cheshta"] + d["naisargika"] + d["drik"]
        d["rupas"] = d["total"] / 60.0
        d["required"] = REQUIRED_RUPAS[p]
        d["ratio"] = d["rupas"] / d["required"]
        d["longitude"] = lons[p]
        d["retrograde"] = pos[p]["speed"] < 0
    order = sorted(PLANETS, key=lambda q: -out[q]["ratio"])
    for i, p in enumerate(order, 1):
        out[p]["rank"] = i
    return {
        "planets": out,
        "order": order,
        "context": {"jd": jd, "ayanamsa": ay, "lagna": lagna, "mc": mc, "is_day": ctx["is_day"],
                    "sunrise_jd": ctx["sunrise"], "sunset_jd": ctx["sunset"], "abda_lord": abda, "masa_lord": masa,
                    "vara_lord": vara, "hora_lord": hora, "ahargana": ahar, "backend": eph.BACKEND},
        "variants": VARIANTS,
        "compat": compat,
        "quirks_applied": dict(ASTROSAGE_QUIRKS) if compat == "astrosage" else {},
        "resolved": RESOLVED,
        "unverified": list(UNVERIFIED),
    }


# Settled on 12 Nov 2026 against a second, independent reference: B.V. Raman's "standard horoscope"
# (16 Oct 1918, 2:20 pm, 13N 77E35, Raman ayanamsa), component totals as reproduced at vedastro.org.
# With Raman's ayanamsa this engine gives his Sthana bala for all seven planets to 0.1 virupa and his Kala bala
# to 0.7 once the Moon's paksha bala is doubled. See tests/test_shadbala_raman.py.
RESOLVED = [
    "sthana.saptavargaja (incl. Mercury) and the dwadasamsa boundaries: identical to Raman's example; the AstroSage "
    "figures that differ (Mercury 48.75; shifted D12 for Moon and Venus) are AstroSage's own deviations",
    "kala.hora: the lord of the running hora, as Raman's example requires (Moon there); AstroSage credits the previous hora",
    "kala.paksha: Parashara's verse (BPHS 27.10-11) does not double the Moon's value, and AstroSage follows it; Raman doubles "
    "it and his example needs that (compat='raman'). Default = Parashara",
    "sthana.saptavargaja scale: the engine uses Raman's 45/30/22.5/15/7.5/3.75/1.875 (matches both references); Parashara's "
    "verse (BPHS 27.2-3) reads 45/30/20/15/10/4/2 - a known difference, see kb/sources/bphs/ch21-30.md",
    "kala.abda / masa / vara / tribhaga / nathonnata / ayana: reproduced on both reference charts",
]
# Still not confirmed against an independent reference.
UNVERIFIED = [
    "cheshta[Mars,Mercury,Jupiter,Venus,Saturn]: Raman's kendra formula with modern mean elements; agrees with "
    "AstroSage to about 1.5 virupas, not checked against Raman's own figures (the published copy is unreliable there)",
    "drik: agrees with AstroSage to 0.03 virupa; Raman's own drik figures could not be reproduced from the published copy",
    "kala.yuddha: no planetary war in either reference chart, formula untested",
]


# ----------------------------------------------------------------------------------------------
# BHAVA BALA   [BPHS 27.26-29; RAMAN ch. 9]
# ----------------------------------------------------------------------------------------------

def bhava_madhyas(lagna, mc):
    """Sripati house mid-points: trisect lagna->IC, IC->desc, etc."""
    ic, desc = _norm(mc + 180), _norm(lagna + 180)
    pts = [lagna, ic, desc, mc]
    out = []
    for i in range(4):
        a, b = pts[i], pts[(i + 1) % 4]
        step = _norm(b - a) / 3.0
        out += [_norm(a + k * step) for k in range(3)]
    return out


def _sign_class(lon):
    """nara / chatushpada / jalachara / keeta for a bhava-madhya [RAMAN ch. 9]."""
    s, deg = _sign(lon), _norm(lon) % 30
    if s in (2, 5, 6, 10) or (s == 8 and deg < 15):
        return "nara"
    if s in (0, 1, 4) or (s == 8 and deg >= 15) or (s == 9 and deg < 15):
        return "chatushpada"
    if s in (3, 11) or (s == 9 and deg >= 15):
        return "jalachara"
    return "keeta"                                  # Vrishchika


def bhava_dig_bala(house, madhya):
    zero = {"nara": 7, "chatushpada": 4, "jalachara": 10, "keeta": 1}[_sign_class(madhya)]
    d = abs(house - zero)
    return (12 - d if d > 6 else d) * 10.0


def bhava_drishti_bala(madhya, lons):
    """Aspects on the bhava-madhya: benefic minus malefic; Mercury and Jupiter count in full, the others a quarter."""
    s = 0.0
    for q in PLANETS:
        v = drishti(q, lons[q], madhya) * (1.0 if q in ("Mercury", "Jupiter") else 0.25)
        s += v if is_benefic(q, lons) else -v
    return s


def bhava_bala(date_str, time_str, lat, lon, tz_off=5.5, compat=None, _sb=None):
    """Strength of the twelve houses: lord's shadbala + bhava dig bala + bhava drishti bala."""
    sb = _sb or shadbala(date_str, time_str, lat, lon, tz_off, compat)
    jd, ay, lons, pos = _chart(date_str, time_str, lat, lon, tz_off)
    lagna, mc = lons["Lagna"], lons["MC"]
    mids = bhava_madhyas(lagna, mc)
    houses = {}
    for h in range(1, 13):
        lord = SIGN_LORD[(_sign(lagna) + h - 1) % 12]
        m = mids[h - 1]
        d = {"madhya": m, "lord": lord, "adhipati": sb["planets"][lord]["total"],
             "dig": bhava_dig_bala(h, m), "drishti": bhava_drishti_bala(m, lons)}
        d["total"] = d["adhipati"] + d["dig"] + d["drishti"]
        d["rupas"] = d["total"] / 60.0
        houses[h] = d
    order = sorted(houses, key=lambda k: -houses[k]["total"])
    for i, h in enumerate(order, 1):
        houses[h]["rank"] = i
    return {"houses": houses, "order": order, "unverified": list(BHAVA_UNVERIFIED)}


BHAVA_UNVERIFIED = [
    "adhipati: inherits every unverified item of the lord's shadbala total",
    "other bhava-bala terms sometimes added by other software (planets in the bhava, day/night rising signs) are "
    "not used - AstroSage's total is adhipati + dig + drishti only",
]

# ----------------------------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------------------------
_ROWS = [("Uchcha", ("sthana", "uchcha")), ("Saptavargaja", ("sthana", "saptavargaja")),
         ("Ojayugma", ("sthana", "ojayugma")), ("Kendradi", ("sthana", "kendradi")),
         ("Drekkana", ("sthana", "drekkana")), ("STHANA total", ("sthana_total",)), ("DIG", ("dig",)),
         ("Nathonnata", ("kala", "nathonnata")), ("Paksha", ("kala", "paksha")), ("Tribhaga", ("kala", "tribhaga")),
         ("Abda", ("kala", "abda")), ("Masa", ("kala", "masa")), ("Vara", ("kala", "vara")),
         ("Hora", ("kala", "hora")), ("Ayana", ("kala", "ayana")), ("Yuddha", ("kala", "yuddha")),
         ("KALA total", ("kala_total",)), ("CHESHTA", ("cheshta",)), ("NAISARGIKA", ("naisargika",)),
         ("DRIK", ("drik",)), ("TOTAL virupas", ("total",)), ("Rupas", ("rupas",)), ("Required", ("required",)),
         ("Ratio", ("ratio",)), ("Rank", ("rank",))]


def _get(d, path):
    for k in path:
        d = d[k]
    return d


def format_tables(sb, bb):
    lines = [f"{'':15s}" + "".join(f"{p[:7]:>9s}" for p in PLANETS)]
    for label, path in _ROWS:
        vals = [_get(sb["planets"][p], path) for p in PLANETS]
        fmt = "{:9d}" if label == "Rank" else "{:9.2f}"
        lines.append(f"{label:15s}" + "".join(fmt.format(v) for v in vals))
    c = sb["context"]
    lines.append(f"\nLords: abda {c['abda_lord']}, masa {c['masa_lord']}, vara {c['vara_lord']}, hora {c['hora_lord']}"
                 f"   ({'day' if c['is_day'] else 'night'} birth, backend {c['backend']})")
    lines.append("Strength order: " + " > ".join(sb["order"]))
    if sb["unverified"]:
        lines.append("Unverified against AstroSage:")
        lines += ["  - " + u for u in sb["unverified"]]
    lines.append(f"\n{'Bhava':15s}" + "".join(f"{h:8d}" for h in range(1, 13)))
    for label, key in (("Adhipati", "adhipati"), ("Dig", "dig"), ("Drishti", "drishti"), ("TOTAL", "total"),
                       ("Rupas", "rupas"), ("Rank", "rank")):
        fmt = "{:8d}" if key == "rank" else "{:8.2f}"
        lines.append(f"{label:15s}" + "".join(fmt.format(bb["houses"][h][key]) for h in range(1, 13)))
    lines += ["  - " + u for u in bb["unverified"]]
    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    _compat = "astrosage" if "--astrosage" in sys.argv else None
    a = [x for x in sys.argv if x != "--astrosage"]
    if len(a) < 5:
        sys.exit("usage: python3 -m engine.shadbala YYYY-MM-DD HH:MM LAT LON [TZ_OFFSET_HOURS] [--astrosage]")
    tz = float(a[5]) if len(a) > 5 else 5.5
    _sb = shadbala(a[1], a[2], float(a[3]), float(a[4]), tz, _compat)
    print(format_tables(_sb, bhava_bala(a[1], a[2], float(a[3]), float(a[4]), tz, _compat, _sb=_sb)))
