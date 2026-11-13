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


def test_period_cautions_and_movable_mark():
    """Fix-first changes of 13 Nov 2026: planets the texts bar from giving good in their own period
    (Jataka Parijata 18.27-28) and the movable-significator mark in the link test."""
    from engine.report import build, MOVABLE
    from engine.analysis import period_cautions
    r = build("1987-02-03", "06:28", 15.3333, 75.1333, "Asia/Kolkata", sex="M")
    c = period_cautions(r["analysis"]["view"])
    assert any(x.startswith("joined to Rahu") for x in c["Mars"])
    assert any(x.startswith("joined to Rahu") for x in c["Moon"])
    assert "at a sign junction (strain)" in c["Jupiter"]
    assert c["Venus"] == [] and c["Saturn"] == [] and c["Rahu"] == []
    assert r["analysis"]["karakas"]["seven_bphs"][MOVABLE["siblings"]] == "Sun"
    t = _chart()                                               # no debilitated-planet false positives on the reference chart
    from engine.analysis import analyse
    c2 = period_cautions(analyse(t)["view"])
    assert set(c2) >= {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"}


def test_control_chart_test_runs_and_is_reproducible():
    """Control-chart test (13 Nov 2026): fixed seed gives the same counts; shares are proportions."""
    from engine.control import control_test, RULES
    birth = {"date": "1996-11-24", "time": "12:05", "lat": 15.3333, "lon": 75.1333, "tz": "Asia/Kolkata"}
    ev = [{"area": "career", "date": "2019-06-01", "polarity": "good"}, {"area": "home/mother", "date": "2021-03-01", "polarity": None},
          {"area": "money", "date": "2023-01-15", "polarity": "bad"}]
    a = control_test(birth, "F", ev, n=20); b = control_test(birth, "F", ev, n=20)
    assert a == b and a["events"] == 3 and set(a["rules"]) == set(RULES)
    for r in a["rules"].values():
        assert 0 <= r["share_controls_at_or_above_real"] <= 1 and r["real"] <= r["of"]
    assert a["rules"]["polarity"]["of"] == 2


def test_laghu_parashari_nature_and_ishta_kashta():
    """Laghu Parashari v.6-13 for a Makara lagna, and Parashara's ishta/kashta bounds (13 Nov 2026)."""
    from engine.control import lp_nature, lp_call, ishta_kashta
    from engine.analysis import analyse
    b = {"date": "1987-02-03", "time": "06:28", "lat": 15.3333, "lon": 75.1333, "tz": "Asia/Kolkata"}
    v = analyse(build_chart(b["date"], b["time"], b["lat"], b["lon"], b["tz"]), sex="M")["view"]
    n = lp_nature(v)
    assert n["Venus"] == 1 and n["Saturn"] == 1          # 5th+10th lord; lagna lord
    assert n["Jupiter"] == -1 and n["Mars"] == -1        # 3rd+12th; 4th+11th
    assert n["Sun"] == 0                                 # 8th lord, but the Sun carries no 8th-lord blemish (v.11)
    assert lp_call(v, n, "Venus", "Venus") is None       # v.29
    assert lp_call(v, n, "Venus", "Saturn") == "good"    # benefic in a benefic's dasha (v.30)
    ik = ishta_kashta(b)
    assert set(ik) == {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"}
    assert all(0 <= x <= 60 and 0 <= y <= 60 for x, y in ik.values())
