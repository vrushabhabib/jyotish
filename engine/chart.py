"""
Vedic natal chart builder.

build_chart(date, time, lat, lon, tz) -> dict with:
  lagna, planets (sidereal longitudes, rashi, degree, nakshatra, pada, retrograde, combust,
  dignity), whole-sign bhavas, D9/D10/D7/D2/D3/D12, Vimshottari dasha (maha + antar),
  moon sign, Sade Sati status, Manglik check.

Ayanamsa: Lahiri (Chitrapaksha) — the Indian government / Rashtriya Panchang standard.
House system: Whole Sign (Parashari). Bhava chalit (Sripati) is also computed for reference.
"""
from __future__ import annotations
import json, os, datetime as dt
from zoneinfo import ZoneInfo
import swisseph as swe

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
NAK = json.load(open(os.path.join(DATA, "nakshatras.json")))
RAS = json.load(open(os.path.join(DATA, "rashis.json")))

PLANET_IDS = {
    "Sun": swe.SUN, "Moon": swe.MOON, "Mars": swe.MARS, "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER, "Venus": swe.VENUS, "Saturn": swe.SATURN, "Rahu": swe.MEAN_NODE,
}
PLANET_ORDER = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
RASHI_NAMES = [r["name"] for r in RAS["rashis"]]
RASHI_EN = [r["en"] for r in RAS["rashis"]]
RASHI_LORD = [r["lord"] for r in RAS["rashis"]]
NAK_LIST = NAK["nakshatras"]

# Combustion orbs (degrees from Sun), standard Parashari values
COMBUST_ORB = {"Moon": 12, "Mars": 17, "Mercury": 14, "Jupiter": 11, "Venus": 10, "Saturn": 15}

swe.set_sid_mode(swe.SIDM_LAHIRI)


# ---------- helpers ----------
def norm(x): return x % 360.0

def rashi_of(lon):            # 1..12
    return int(norm(lon) // 30) + 1

def deg_in_rashi(lon): return norm(lon) % 30

def nakshatra_of(lon):        # (index 1..27, pada 1..4, fraction traversed 0..1)
    span = 360 / 27
    x = norm(lon)
    i = int(x // span)
    frac = (x - i * span) / span
    pada = int(frac * 4) + 1
    return i + 1, pada, frac

def dms(x):
    d = int(x); m = int((x - d) * 60); s = round(((x - d) * 60 - m) * 60)
    return f"{d}°{m:02d}'{s:02d}\""

def to_jd_utc(date_str, time_str, tz):
    local = dt.datetime.fromisoformat(f"{date_str}T{time_str}").replace(tzinfo=ZoneInfo(tz))
    u = local.astimezone(dt.timezone.utc)
    return swe.julday(u.year, u.month, u.day, u.hour + u.minute / 60 + u.second / 3600), local


# ---------- dignity ----------
def dignity(planet, lon):
    p = RAS["planets"][planet]
    r, d = rashi_of(lon), deg_in_rashi(lon)
    if r == p["exalt"]["rashi"]:
        return "Exalted (deep)" if abs(d - p["exalt"]["deg"]) < 1 else "Exalted"
    if r == p["debil"]["rashi"]:
        return "Debilitated (deep)" if abs(d - p["debil"]["deg"]) < 1 else "Debilitated"
    if r == p["mool"]["rashi"] and p["mool"]["from"] <= d <= p["mool"]["to"]:
        return "Moolatrikona"
    if r in p["own"]:
        return "Own sign"
    lord = RASHI_LORD[r - 1]
    if lord in p["friends"]: return "Friend's sign"
    if lord in p["enemies"]: return "Enemy's sign"
    return "Neutral sign"


# ---------- vargas ----------
def varga_rashi(lon, n):
    """Generic Parashari divisional sign for D-n (n in 2,3,4,7,9,10,12,16,20,24,27,30,40,45,60).
    Implements the standard rules from BPHS for the common vargas."""
    r = rashi_of(lon); d = deg_in_rashi(lon)
    part = int(d // (30 / n))                   # 0..n-1
    odd = (r % 2 == 1)
    if n == 9:                                  # Navamsa: movable start self, fixed 9th, dual 5th
        start = {0: r, 1: r + 8, 2: r + 4}[(r - 1) % 3]
        return (start - 1 + part) % 12 + 1
    if n == 2:                                  # Hora: odd -> Leo(Sun) first half, Cancer second; even reverse
        return (5 if part == 0 else 4) if odd else (4 if part == 0 else 5)
    if n == 3:                                  # Drekkana: 1st, 5th, 9th from sign
        return (r - 1 + part * 4) % 12 + 1
    if n == 4:                                  # Chaturthamsa: 1st,4th,7th,10th
        return (r - 1 + part * 3) % 12 + 1
    if n == 7:                                  # Saptamsa: odd from self, even from 7th
        start = r if odd else r + 6
        return (start - 1 + part) % 12 + 1
    if n == 10:                                 # Dasamsa: odd from self, even from 9th
        start = r if odd else r + 8
        return (start - 1 + part) % 12 + 1
    if n == 12:                                 # Dwadasamsa: from self
        return (r - 1 + part) % 12 + 1
    if n == 16:                                 # Shodasamsa: movable Aries, fixed Leo, dual Sag
        start = {0: 1, 1: 5, 2: 9}[(r - 1) % 3]
        return (start - 1 + part) % 12 + 1
    if n == 20:                                 # Vimsamsa: movable Aries, fixed Sag, dual Leo
        start = {0: 1, 1: 9, 2: 5}[(r - 1) % 3]
        return (start - 1 + part) % 12 + 1
    if n == 24:                                 # Chaturvimsamsa: odd Leo, even Cancer
        start = 5 if odd else 4
        return (start - 1 + part) % 12 + 1
    if n == 27:                                 # Bhamsa: fire Aries, earth Cancer, air Libra, water Cap
        start = {0: 1, 1: 4, 2: 7, 3: 10}[(r - 1) % 4]
        return (start - 1 + part) % 12 + 1
    if n == 30:                                 # Trimsamsa (unequal): odd 5/5/8/7/5 Mars,Sat,Jup,Merc,Ven
        if odd:
            bounds = [(5, 1), (10, 11), (18, 9), (25, 3), (30, 7)]
        else:
            bounds = [(5, 2), (12, 6), (20, 12), (25, 10), (30, 8)]
        for lim, sign in bounds:
            if d < lim: return sign
        return bounds[-1][1]
    if n == 40:                                 # Khavedamsa: odd Aries, even Libra
        start = 1 if odd else 7
        return (start - 1 + part) % 12 + 1
    if n == 45:                                 # Akshavedamsa: movable Aries, fixed Leo, dual Sag
        start = {0: 1, 1: 5, 2: 9}[(r - 1) % 3]
        return (start - 1 + part) % 12 + 1
    if n == 60:                                 # Shashtiamsa: from self
        return (r - 1 + part) % 12 + 1
    raise ValueError(n)


# ---------- dasha ----------
def vimshottari(moon_lon, birth_local, levels=2):
    """Returns list of maha dashas (with antar dashas if levels>=2) as dicts with start/end datetimes."""
    order = NAK["vimshottari_order"]; years = NAK["vimshottari_years"]
    n, _, frac = nakshatra_of(moon_lon)
    lord = NAK_LIST[n - 1]["lord"]
    idx = order.index(lord)
    balance = years[lord] * (1 - frac)          # years remaining of first dasha
    YEAR = 365.25
    out = []
    t = birth_local
    first = True
    for k in range(9):
        L = order[(idx + k) % 9]
        span = balance if first else years[L]
        start, end = t, t + dt.timedelta(days=span * YEAR)
        md = {"lord": L, "start": start, "end": end, "years": round(span, 3)}
        if levels >= 2:
            # antardashas: proportional; if first, skip the elapsed portion
            ants = []
            a_t = start - dt.timedelta(days=(years[L] - span) * YEAR) if first else start
            for j in range(9):
                A = order[(order.index(L) + j) % 9]
                a_span = years[L] * years[A] / 120
                a_s, a_e = a_t, a_t + dt.timedelta(days=a_span * YEAR)
                if a_e > start:
                    ants.append({"lord": A, "start": max(a_s, start), "end": a_e})
                a_t = a_e
            md["antar"] = ants
        out.append(md)
        t = end; first = False
    return out

def current_dasha(dashas, when):
    for md in dashas:
        if md["start"] <= when < md["end"]:
            ad = next((a for a in md.get("antar", []) if a["start"] <= when < a["end"]), None)
            return md, ad
    return None, None


# ---------- main ----------
def build_chart(date_str, time_str, lat, lon_geo, tz, place=""):
    jd, local = to_jd_utc(date_str, time_str, tz)
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
    ayan = swe.get_ayanamsa_ut(jd)

    # Lagna & cusps (tropical from swe, then subtract ayanamsa)
    cusps, ascmc = swe.houses(jd, lat, lon_geo, b'W')
    lagna = norm(ascmc[0] - ayan)
    mc = norm(ascmc[1] - ayan)
    lagna_rashi = rashi_of(lagna)

    planets = {}
    for name in PLANET_ORDER:
        if name == "Ketu":
            L = norm(planets["Rahu"]["lon"] + 180); speed = planets["Rahu"]["speed"]
        else:
            res, _ = swe.calc_ut(jd, PLANET_IDS[name], flags)
            L, speed = res[0], res[3]
        r = rashi_of(L); n, pada, _ = nakshatra_of(L)
        planets[name] = {
            "lon": L, "speed": speed, "rashi": r, "rashi_name": RASHI_NAMES[r - 1], "rashi_en": RASHI_EN[r - 1],
            "deg": deg_in_rashi(L), "deg_dms": dms(deg_in_rashi(L)),
            "nakshatra": NAK_LIST[n - 1]["name"], "nak_lord": NAK_LIST[n - 1]["lord"], "pada": pada,
            "retrograde": speed < 0 and name not in ("Sun", "Moon"),
            "bhava": (r - lagna_rashi) % 12 + 1,
            "dignity": dignity(name, L),
        }
    # combustion
    sun = planets["Sun"]["lon"]
    for p, orb in COMBUST_ORB.items():
        d = abs((planets[p]["lon"] - sun + 180) % 360 - 180)
        planets[p]["combust"] = d < orb
    # vargas
    for n in (2, 3, 7, 9, 10, 12, 30, 60):
        for p in PLANET_ORDER:
            planets[p][f"D{n}"] = varga_rashi(planets[p]["lon"], n)
    lagna_vargas = {f"D{n}": varga_rashi(lagna, n) for n in (2, 3, 7, 9, 10, 12, 30, 60)}

    # bhavas (whole sign)
    bhavas = {}
    for h in range(1, 13):
        r = (lagna_rashi - 1 + h - 1) % 12 + 1
        bhavas[h] = {"rashi": r, "rashi_name": RASHI_NAMES[r - 1], "lord": RASHI_LORD[r - 1],
                     "occupants": [p for p in PLANET_ORDER if planets[p]["bhava"] == h]}
    for h in bhavas:
        lord = bhavas[h]["lord"]
        bhavas[h]["lord_in_bhava"] = planets[lord]["bhava"]

    # dasha
    dashas = vimshottari(planets["Moon"]["lon"], local)
    now = dt.datetime.now(ZoneInfo(tz))
    md, ad = current_dasha(dashas, now)

    # moon-based
    moon_rashi = planets["Moon"]["rashi"]
    # Sade Sati now: Saturn transit in 12th, 1st, 2nd from Moon
    sat_now, _ = swe.calc_ut(swe.julday(now.year, now.month, now.day, now.hour), swe.SATURN, flags)
    sat_r = rashi_of(sat_now[0]); rel = (sat_r - moon_rashi) % 12
    sade_sati = {0: "Sade Sati — 2nd phase (peak, Saturn on Moon)", 11: "Sade Sati — 1st phase (rising)",
                 1: "Sade Sati — 3rd phase (setting)", 3: "Ardhashtama Shani (4th from Moon)",
                 7: "Ashtama Shani (8th from Moon)"}.get(rel, "No Sade Sati / Dhaiya")

    # Manglik (from Lagna, Moon, Venus): Mars in 1,2,4,7,8,12
    def manglik_from(ref_r):
        h = (planets["Mars"]["rashi"] - ref_r) % 12 + 1
        return h in (1, 2, 4, 7, 8, 12), h
    mk = {k: manglik_from(v) for k, v in {"lagna": lagna_rashi, "moon": moon_rashi, "venus": planets["Venus"]["rashi"]}.items()}

    return {
        "input": {"date": date_str, "time": time_str, "tz": tz, "lat": lat, "lon": lon_geo, "place": place,
                  "jd_ut": jd, "ayanamsa_lahiri": ayan},
        "lagna": {"lon": lagna, "rashi": lagna_rashi, "rashi_name": RASHI_NAMES[lagna_rashi - 1],
                  "deg_dms": dms(deg_in_rashi(lagna)), "nakshatra": NAK_LIST[nakshatra_of(lagna)[0] - 1]["name"],
                  "lord": RASHI_LORD[lagna_rashi - 1], "vargas": lagna_vargas, "mc": mc},
        "planets": planets,
        "bhavas": bhavas,
        "moon_rashi": moon_rashi, "janma_nakshatra": planets["Moon"]["nakshatra"],
        "dasha": {"maha": dashas, "current_maha": md, "current_antar": ad},
        "sade_sati_now": sade_sati,
        "manglik": {k: {"is_manglik": v[0], "mars_house": v[1]} for k, v in mk.items()},
    }


def print_chart(c):
    print(f"Birth: {c['input']['date']} {c['input']['time']} {c['input']['tz']}  {c['input']['place']}")
    print(f"Ayanamsa (Lahiri): {c['input']['ayanamsa_lahiri']:.4f}°")
    L = c["lagna"]
    print(f"Lagna: {L['rashi_name']} {L['deg_dms']}  ({L['nakshatra']})  lord {L['lord']}   D9 lagna: {RASHI_NAMES[L['vargas']['D9']-1]}")
    print(f"Moon sign: {RASHI_NAMES[c['moon_rashi']-1]}   Janma nakshatra: {c['janma_nakshatra']}")
    print("\nPlanet     Rashi         Deg        Nakshatra-pada     H   D9          Dignity         R/C")
    for p, d in c["planets"].items():
        flags = ("R" if d["retrograde"] else "") + ("C" if d.get("combust") else "")
        print(f"{p:<10} {d['rashi_name']:<13} {d['deg_dms']:<10} {d['nakshatra']+'-'+str(d['pada']):<18} {d['bhava']:<3} {RASHI_NAMES[d['D9']-1]:<11} {d['dignity']:<15} {flags}")
    print("\nBhavas (whole sign):")
    for h, b in c["bhavas"].items():
        print(f"  {h:>2} {b['rashi_name']:<12} lord {b['lord']:<8} (in {b['lord_in_bhava']:>2})  {', '.join(b['occupants'])}")
    print("\nVimshottari Maha Dashas:")
    for md in c["dasha"]["maha"]:
        print(f"  {md['lord']:<8} {md['start']:%Y-%m-%d} → {md['end']:%Y-%m-%d}")
    cm, ca = c["dasha"]["current_maha"], c["dasha"]["current_antar"]
    if cm:
        print(f"\nNow: {cm['lord']} maha / {ca['lord'] if ca else '?'} antar (antar ends {ca['end']:%Y-%m-%d})" if ca else f"\nNow: {cm['lord']} maha")
    print(f"Saturn now: {c['sade_sati_now']}")
    m = c["manglik"]
    print(f"Manglik: lagna={m['lagna']['is_manglik']} (Mars in {m['lagna']['mars_house']}), moon={m['moon']['is_manglik']}, venus={m['venus']['is_manglik']}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 6:
        print("usage: python -m engine.chart YYYY-MM-DD HH:MM PLACE LAT LON TZ"); sys.exit(1)
    date, time, place, lat, lon, tz = sys.argv[1:7]
    print_chart(build_chart(date, time, float(lat), float(lon), tz, place))
