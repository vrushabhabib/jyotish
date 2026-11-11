"""Regression tests for the v2 engine (ephemeris fallback, analysis, ashtakavarga, transits).
Reference values: JPL Horizons, an AstroSage printout (chart verified 5/5 against the native's life),
and published panchang ingress dates."""
import datetime as dt
from engine import ephemeris as E
from engine.chart import build_chart
from engine.analysis import analyse, kp_lords
from engine.ashtakavarga import ashtakavarga
from engine import transits as T

JD = E.julday(dt.datetime(1996, 11, 24, 6, 35))          # 12:05 IST


def _chart():
    return build_chart("1996-11-24", "12:05", 15.3333, 75.1333, "Asia/Kolkata", "Hubli")


def test_apparent_longitudes_match_jpl_horizons():
    ay = E.ayanamsa(JD)
    assert abs((E.body("Sun", JD)[0] + ay) % 360 - 242.2634861) < 0.002
    assert abs((E.body("Jupiter", JD)[0] + ay) % 360 - 286.9767995) < 0.002


def test_lahiri_ayanamsa_j2000():
    assert abs(E.ayanamsa(2451545.0) - 23.8571) < 0.001   # Swiss Ephemeris Lahiri at J2000


def test_against_astrosage_printout():
    c = _chart()
    assert c["lagna"]["rashi_name"] == "Makara" and abs(c["lagna"]["lon"] - 297.0989) < 0.02
    ref = {"Moon": 27.5636, "Mars": 139.3761, "Saturn": 336.8608, "Rahu": 161.2356, "Venus": 187.6897}
    for p, x in ref.items():
        assert abs(c["planets"][p]["lon"] - x) < 0.02, p
    assert c["planets"]["Saturn"]["retrograde"] and c["planets"]["Mercury"]["combust"]


def test_sunrise():
    sr, ss = E.sun_times(JD, 15.3333, 75.1333)
    ist = lambda j: E.jd_to_datetime(j) + dt.timedelta(hours=5.5)
    assert abs((ist(sr) - dt.datetime(1996, 11, 24, 6, 36, 5)).total_seconds()) < 30
    assert abs((ist(ss) - dt.datetime(1996, 11, 24, 17, 56, 19)).total_seconds()) < 30


def test_sarvashtakavarga_matches_astrosage():
    av = ashtakavarga(_chart())
    assert av["sav"] == [27, 27, 35, 24, 29, 36, 29, 30, 19, 29, 25, 27]
    assert av["bav"]["Jupiter"] == [2, 5, 5, 6, 6, 5, 3, 5, 4, 3, 8, 4]
    assert av["bav"]["Saturn"] == [3, 4, 5, 3, 4, 4, 4, 3, 2, 3, 2, 2]


def test_panchanga_karakas_arudhas_kp():
    a = analyse(_chart(), "F")
    pg = a["panchanga"]
    assert pg["tithi"] == "Shukla Purnima" and pg["yoga"] == "Parigha" and pg["karana"] == "Vishti" and pg["vara"] == "Sunday"
    assert a["karakas"]["seven"] == {"AK": "Moon", "AmK": "Jupiter", "BK": "Mercury", "MK": "Mars", "PK": "Sun", "GK": "Venus", "DK": "Saturn"}
    assert a["arudhas"]["AL"]["sign"] == "Vrishabha" and a["arudhas"]["A7"]["sign"] == "Tula" and a["arudhas"]["UL"]["sign"] == "Kanya"
    assert a["kp"]["cusp7"] == ["Mercury", "Jupiter", "Venus"]            # AstroSage KP: star Mercury, sub Jupiter, sub-sub Venus


def test_yogas_and_doshas():
    a = analyse(_chart(), "F")
    names = [y["name"] for y in a["yogas"]]
    for must in ("Malavya (Mahapurusha)", "Vimala (Viparita)", "Budha-Aditya", "Anapha", "Dainya Parivartana"):
        assert must in names, must
    assert a["doshas"]["manglik"]["from"]["lagna"]["mars_house"] == 8 and a["doshas"]["manglik"]["cancellations"]
    assert not a["doshas"]["kaal_sarp"]["full"]


def test_dasha_balance():
    a = analyse(_chart(), "F")
    first = a["dasha_tree"][0]
    assert first[0] == "Sun"
    assert abs((first[2] - dt.datetime(2002, 6, 29, tzinfo=first[2].tzinfo)).days) <= 3      # AstroSage: Sun ends 29 Jun 2002


def test_published_ingresses():
    D = dt.date
    sat = {(s, a) for s, a, b in T.periods("Saturn", D(2025, 1, 1), D(2027, 12, 31))}
    assert any(s == 12 and abs((a - D(2025, 3, 29)).days) <= 1 for s, a in sat)       # Saturn -> Meena 29 Mar 2025
    assert any(s == 1 and abs((a - D(2027, 6, 3)).days) <= 1 for s, a in sat)         # Saturn -> Mesha 3 Jun 2027
    jup = {(s, a) for s, a, b in T.periods("Jupiter", D(2025, 1, 1), D(2026, 12, 31))}
    assert any(s == 3 and abs((a - D(2025, 5, 14)).days) <= 1 for s, a in jup)        # Jupiter -> Mithuna 14 May 2025
    assert any(s == 4 and abs((a - D(2026, 6, 2)).days) <= 1 for s, a in jup)         # Jupiter -> Karka 2 Jun 2026


def test_kp_subdivision_sums():
    assert kp_lords(0.0 - 5.8 / 60) == ["Ketu", "Ketu", "Ketu"]                         # 0 Aries KP = Ketu/Ketu/Ketu
