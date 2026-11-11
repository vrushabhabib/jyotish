"""Ephemeris backend with automatic fallback.

Swiss Ephemeris (pyswisseph) is used when it can be imported; otherwise pyephem (libastro, VSOP87).
Both give sidereal Lahiri longitudes. The fallback was validated on 11 Nov 2026 against JPL Horizons (Sun and
Jupiter apparent longitudes identical to 4 decimals) and an AstroSage printout (lagna, Moon, Mars, Saturn,
Rahu within 0.4'; AstroSage's own Sun is 0.5' and its Jupiter 2.8' away from JPL, so those residuals are
AstroSage's). Published ingresses reproduced: Saturn -> Mesha 3 Jun 2027, Jupiter -> Karka 2 Jun 2026.

Public API (identical for both backends):
    BACKEND                      'swisseph' | 'ephem'
    julday(dt_utc)               -> JD (UT)
    ayanamsa(jd)                 -> Lahiri ayanamsa in degrees
    body(name, jd)               -> (sidereal lon, speed deg/day, declination deg)
    angles(jd, lat, lon)         -> (sidereal ascendant, sidereal MC)
    sun_times(jd, lat, lon)      -> (sunrise JD, sunset JD) for the civil day containing jd
Rahu is the MEAN node (the AstroSage / Rashtriya Panchang default); Ketu = Rahu + 180.
"""
from __future__ import annotations
import math, datetime as dt

try:                                    # pragma: no cover - depends on the machine
    import swisseph as swe
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    BACKEND = "swisseph"
except Exception:                       # ImportError or missing ephemeris files
    swe = None
    import ephem
    BACKEND = "ephem"

BODIES = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
_J1900 = 2415020.0                      # ephem.Date epoch (1899-12-31 12:00 UT)


def julday(u: dt.datetime) -> float:
    """JD (UT) from an aware-or-naive UTC datetime."""
    if u.tzinfo is not None:
        u = u.astimezone(dt.timezone.utc).replace(tzinfo=None)
    a = (14 - u.month) // 12
    y = u.year + 4800 - a
    m = u.month + 12 * a - 3
    jdn = u.day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
    return jdn + (u.hour - 12) / 24 + u.minute / 1440 + (u.second + u.microsecond / 1e6) / 86400


def jd_to_datetime(jd: float) -> dt.datetime:
    return dt.datetime(2000, 1, 1, 12) + dt.timedelta(days=jd - 2451545.0)


def ayanamsa(jd: float) -> float:
    if swe:
        return swe.get_ayanamsa_ut(jd)
    # Lahiri anchor as Swiss Ephemeris defines it: JD 2435553.5 (21 Mar 1956) -> 23.245524743 deg
    # (23 deg 15' 00.658" less the nutation of that date); general precession with its secular term,
    # integrated from the anchor (rate taken at the midpoint).
    t_yrs = (jd - 2435553.5) / 365.25
    T_mid = ((jd + 2435553.5) / 2 - 2451545.0) / 36525.0
    return 23.245524743 + t_yrs * (50.2878 + 0.0222 * T_mid) / 3600.0


def obliquity(jd: float) -> float:
    T = (jd - 2451545.0) / 36525.0
    return 23.4392911 - 0.0130042 * T - 1.64e-7 * T * T


def _mean_node_tropical(jd: float) -> float:
    T = (jd - 2451545.0) / 36525.0
    return (125.0445479 - 1934.1362891 * T + 0.0020754 * T * T + T ** 3 / 467441.0) % 360.0


def _ephem_body(name):
    return {"Sun": ephem.Sun, "Moon": ephem.Moon, "Mars": ephem.Mars, "Mercury": ephem.Mercury,
            "Jupiter": ephem.Jupiter, "Venus": ephem.Venus, "Saturn": ephem.Saturn}[name]()


def _ephem_tropical(name, jd):
    """Apparent geocentric ecliptic longitude of date (light-time, aberration and nutation included -
    what Swiss Ephemeris and the JPL Horizons 'observer ecliptic' quantity give) and declination.
    Checked against JPL Horizons for 1996-11-24 06:35 UT: Sun 242.2635 and Jupiter 286.9768, both
    identical to four decimals."""
    b = _ephem_body(name)
    d = ephem.Date(jd - _J1900)
    b.compute(d, epoch=d)
    ra, dec = float(b.g_ra), float(b.g_dec)
    eps = math.radians(obliquity(jd))
    lon = math.degrees(math.atan2(math.sin(ra) * math.cos(eps) + math.tan(dec) * math.sin(eps), math.cos(ra))) % 360.0
    return lon, math.degrees(dec)


def body(name: str, jd: float):
    """(sidereal longitude, speed in deg/day, declination)."""
    if name == "Ketu":
        lon, sp, dec = body("Rahu", jd)
        return (lon + 180.0) % 360.0, sp, -dec
    ay = ayanamsa(jd)
    if swe:
        if name == "Rahu":
            res, _ = swe.calc_ut(jd, swe.MEAN_NODE, swe.FLG_SWIEPH | swe.FLG_SPEED)
            return (res[0] - ay) % 360.0, res[3], 0.0
        pid = {"Sun": swe.SUN, "Moon": swe.MOON, "Mars": swe.MARS, "Mercury": swe.MERCURY,
               "Jupiter": swe.JUPITER, "Venus": swe.VENUS, "Saturn": swe.SATURN}[name]
        res, _ = swe.calc_ut(jd, pid, swe.FLG_SWIEPH | swe.FLG_SPEED)
        eq, _ = swe.calc_ut(jd, pid, swe.FLG_SWIEPH | swe.FLG_EQUATORIAL)
        return (res[0] - ay) % 360.0, res[3], eq[1]
    if name == "Rahu":
        return (_mean_node_tropical(jd) - ay) % 360.0, -0.05295, 0.0
    lon, dec = _ephem_tropical(name, jd)
    h = 0.25                                             # central difference over 12 hours
    a, _ = _ephem_tropical(name, jd - h)
    b, _ = _ephem_tropical(name, jd + h)
    speed = ((b - a + 180.0) % 360.0 - 180.0) / (2 * h)
    return (lon - ay) % 360.0, speed, dec


def _gmst_deg(jd: float) -> float:
    T = (jd - 2451545.0) / 36525.0
    return (280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.000387933 * T * T - T ** 3 / 38710000.0) % 360.0


def angles(jd: float, lat: float, lon: float):
    """(sidereal ascendant, sidereal MC)."""
    ay = ayanamsa(jd)
    if swe:
        _, ascmc = swe.houses(jd, lat, lon, b"W")
        return (ascmc[0] - ay) % 360.0, (ascmc[1] - ay) % 360.0
    ramc = math.radians((_gmst_deg(jd) + lon) % 360.0)
    eps = math.radians(obliquity(jd))
    phi = math.radians(lat)
    asc = math.degrees(math.atan2(math.cos(ramc),
                                  -(math.sin(ramc) * math.cos(eps) + math.tan(phi) * math.sin(eps)))) % 360.0
    mc = math.degrees(math.atan2(math.sin(ramc), math.cos(ramc) * math.cos(eps))) % 360.0
    return (asc - ay) % 360.0, (mc - ay) % 360.0


def sun_times(jd: float, lat: float, lon: float):
    """Sunrise and sunset (JD, UT) bracketing local noon of the day that contains jd.
    Uses the centre of the disc with 34' refraction, the usual panchanga convention."""
    local_noon = round(jd + lon / 360.0) - lon / 360.0      # JD .0 = noon, so nearest integer = local mean noon
    # solve altitude = -0.833 deg by bisection either side of local noon
    def alt(j):
        if swe:
            res, _ = swe.calc_ut(j, swe.SUN, swe.FLG_SWIEPH | swe.FLG_EQUATORIAL)
            ra, dec = math.radians(res[0]), math.radians(res[1])
        else:
            s = ephem.Sun(); s.compute(ephem.Date(j - _J1900), epoch=ephem.Date(j - _J1900))
            ra, dec = float(s.ra), float(s.dec)
        ha = math.radians((_gmst_deg(j) + lon) % 360.0) - ra
        ph = math.radians(lat)
        return math.degrees(math.asin(math.sin(ph) * math.sin(dec) + math.cos(ph) * math.cos(dec) * math.cos(ha)))
    def solve(a, b):
        fa = alt(a) + 0.833
        for _ in range(40):
            m = (a + b) / 2
            fm = alt(m) + 0.833
            if (fa < 0) == (fm < 0):
                a, fa = m, fm
            else:
                b = m
        return (a + b) / 2
    noon = local_noon
    return solve(noon - 0.5, noon), solve(noon, noon + 0.5)


def positions(jd: float, lat: float, lon: float) -> dict:
    """All nine grahas + Lagna + MC in one call."""
    out = {n: dict(zip(("lon", "speed", "dec"), body(n, jd))) for n in BODIES}
    asc, mc = angles(jd, lat, lon)
    out["Lagna"] = {"lon": asc, "speed": 0.0, "dec": 0.0}
    out["MC"] = {"lon": mc, "speed": 0.0, "dec": 0.0}
    return out
