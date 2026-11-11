"""Fallback natal chart via pyephem (libastro) + Lahiri ayanamsa.
Use when pyswisseph will not build. Thin wrapper kept for backward compatibility; the real work is in engine/ephemeris.py.
Validation lives in tests/test_engine_v2.py (JPL Horizons, AstroSage, published ingresses).
Usage: python3 engine/ephem_chart.py YYYY-MM-DD HH:MM LAT LON   (IST assumed)
"""
import math, datetime as dt
import ephem

RASHI = ["Mesha","Vrishabha","Mithuna","Karka","Simha","Kanya","Tula","Vrishchika","Dhanu","Makara","Kumbha","Meena"]
LORD  = ["Mars","Venus","Mercury","Moon","Sun","Mercury","Venus","Mars","Jupiter","Saturn","Saturn","Jupiter"]
NAK = ["Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra","Punarvasu","Pushya","Ashlesha",
"Magha","P.Phalguni","U.Phalguni","Hasta","Chitra","Swati","Vishakha","Anuradha","Jyeshtha",
"Mula","P.Ashadha","U.Ashadha","Shravana","Dhanishta","Shatabhisha","P.Bhadrapada","U.Bhadrapada","Revati"]
NAK_LORD = ["Ketu","Venus","Sun","Moon","Mars","Rahu","Jupiter","Saturn","Mercury"]*3
DASHA_YRS = {"Ketu":7,"Venus":20,"Sun":6,"Moon":10,"Mars":7,"Rahu":18,"Jupiter":16,"Saturn":19,"Mercury":17}
DASHA_SEQ = ["Ketu","Venus","Sun","Moon","Mars","Rahu","Jupiter","Saturn","Mercury"]

def lahiri_ayanamsa(jd):
    # SE Lahiri anchor: t0 = JD 2435553.5, ayan 23.2501828 deg; precession rate with secular term
    t_yrs = (jd - 2435553.5)/365.25
    T = (jd - 2451545.0)/36525.0
    rate = 50.2878 + 0.0222*T  # arcsec/yr
    return 23.2501828 + t_yrs*rate/3600.0

def ecl_lon(body, obs):
    body.compute(obs)
    return math.degrees(ephem.Ecliptic(body).lon)

def obliquity(jd):
    T=(jd-2451545.0)/36525.0
    return 23.4392911 - 0.0130042*T

def ascendant_tropical(obs, jd):
    ramc = float(obs.sidereal_time())
    eps = math.radians(obliquity(jd))
    phi = float(obs.lat)
    # asc = atan2( cos(RAMC), -(sin(RAMC)cos(eps)+tan(phi)sin(eps)) ), from 0 Aries
    return math.degrees(math.atan2(math.cos(ramc), -(math.sin(ramc)*math.cos(eps)+math.tan(phi)*math.sin(eps)))) % 360.0

def fmt(lon):
    r=int(lon//30); d=lon%30
    nidx=int(lon//(360/27)); pada=int((lon%(360/27))//(360/108))+1
    return f"{RASHI[r]:11s} {int(d):2d}°{int((d%1)*60):02d}' {NAK[nidx]:13s} p{pada}"

def build(date_str, time_str, lat, lon, tz_off=5.5):
    """Sidereal (Lahiri) longitudes for the nine grahas and the lagna.

    FIXED 11 Nov 2026: this used to read ephem.Ecliptic(body) in the J2000 frame instead of the
    ecliptic of date, so every planet was off by the precession since 2000 (about 0.84' per year:
    +8' for a 1990 birth, -22' for a 2026 transit). It now delegates to engine.ephemeris, which was
    validated against an AstroSage printout to under 0.5 arc-minute. The lagna was never affected.
    """
    import os, sys
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    from engine import ephemeris as E
    local = dt.datetime.fromisoformat(f"{date_str}T{time_str}")
    jd = E.julday(local - dt.timedelta(hours=tz_off))
    pos = E.positions(jd, float(lat), float(lon))
    out = {n: pos[n]["lon"] for n in E.BODIES}
    out["Lagna"] = pos["Lagna"]["lon"]
    out["_ayanamsa"] = E.ayanamsa(jd)
    out["_jd"] = jd
    return out

def vimshottari(moon_lon, birth_dt):
    nidx=int(moon_lon//(360/27))
    lord=NAK_LORD[nidx]
    frac_elapsed=(moon_lon%(360/27))/(360/27)
    bal_years=DASHA_YRS[lord]*(1-frac_elapsed)
    rows=[]; start=birth_dt; i=DASHA_SEQ.index(lord)
    end=start+dt.timedelta(days=bal_years*365.2425)
    rows.append((lord,start,end)); start=end
    for k in range(1,9):
        l=DASHA_SEQ[(i+k)%9]
        end=start+dt.timedelta(days=DASHA_YRS[l]*365.2425)
        rows.append((l,start,end)); start=end
    return lord, bal_years, rows

if __name__=="__main__":
    import sys
    date,time,lat,lon=sys.argv[1],sys.argv[2],float(sys.argv[3]),float(sys.argv[4])
    ch=build(date,time,lat,lon)
    print(f"Ayanamsa (Lahiri): {ch['_ayanamsa']:.4f}°")
    for p in ["Lagna","Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn","Rahu","Ketu"]:
        print(f"{p:8s} {ch[p]:8.3f}  {fmt(ch[p])}")
    lord,bal,rows=vimshottari(ch["Moon"],dt.datetime.fromisoformat(f"{date}T{time}"))
    print(f"\nMoon dasha lord at birth: {lord}, balance {bal:.2f} yrs")
    for l,s,e in rows: print(f"  {l:8s} {s.date()} -> {e.date()}")
