"""Yogini, Chara dasha and house cusps against the AstroSage printout for 24 Nov 1996 12:05 Hubli."""
import datetime as dt
from engine.chart import build_chart
from engine import dashas_extra as D, houses as H, ephemeris as E

C = build_chart("1996-11-24", "12:05", 15.3333, 75.1333, "Asia/Kolkata")
B = dt.datetime(1996, 11, 24, 12, 5)


def test_yogini_matches_printout():
    y = D.yogini(C["planets"]["Moon"]["lon"], B)
    assert [p["yogini"] for p in y[:8]] == ["Ulka", "Siddha", "Sankata", "Mangala", "Pingala", "Dhanya", "Bhramari", "Bhadrika"]
    for p, end in zip(y[:8], ["2002-06-28", "2009-06-28", "2017-06-28", "2018-06-28", "2020-06-28", "2023-06-28", "2027-06-28", "2032-06-28"]):
        assert abs((p["end"].date() - dt.date.fromisoformat(end)).days) <= 3


def test_chara_years_and_order():
    so = {p: d["rashi"] for p, d in C["planets"].items()}
    ch = D.chara(C["lagna"]["rashi"], so, B)
    got = [(m["sign"], m["years"]) for m in ch["maha"]]
    assert got == [("Makara", 10), ("Dhanu", 12), ("Vrishchika", 4), ("Tula", 12), ("Kanya", 10), ("Simha", 9),
                   ("Karka", 3), ("Mithuna", 5), ("Vrishabha", 5), ("Mesha", 4), ("Meena", 3), ("Kumbha", 11)]
    assert ch["maha"][3]["start"].year == 2022                                    # Libra from 24 Nov 2022
    assert [a["sign"] for a in ch["maha"][3]["antar"]][:2] == ["Vrishchika", "Dhanu"]      # direct group
    assert [a["sign"] for a in ch["maha"][0]["antar"]][:2] == ["Dhanu", "Vrishchika"]      # reverse group
    assert ch["maha"][0]["antar"][-1]["sign"] == "Makara"


def test_kp_cusps_and_significators():
    jd = E.julday(dt.datetime(1996, 11, 24, 6, 35))
    k = H.kp_chart(jd, 15.3333, 75.1333)
    ref = {1: 297.188889, 2: 333.171667, 3: 6.852778, 4: 35.851944, 5: 61.787778, 6: 87.737222}
    for h, lon in ref.items():
        assert abs(k["cusps"][h]["lon"] - lon) * 60 < 1.0
    assert (k["cusps"][2]["star"], k["cusps"][2]["sub"], k["cusps"][2]["subsub"]) == ("Jupiter", "Rahu", "Moon")
    assert k["planet_significations"]["Jupiter"] == [2, 4, 9, 11, 12]
    assert k["planet_significations"]["Mars"] == [3, 4, 7, 9, 10]


def test_sripati_midpoints():
    jd = E.julday(dt.datetime(1996, 11, 24, 6, 35))
    s = H.sripati(jd, 15.3333, 75.1333)
    assert abs(s[1]["mid"] - 329.986389) < 0.02 and abs(s[2]["begin"] - 346.430278) < 0.02


def test_convergence_and_ledger_run():
    from engine.report import build, markdown
    from engine.convergence import timeline, rashi_aspect
    from engine import ledger
    r = build("1996-11-24", "12:05", 15.3333, 75.1333, "Asia/Kolkata", sex="F")
    t = timeline(r, sex="F")
    assert set(t) == {"marriage", "children", "career", "money", "home/property"}
    assert all(0 <= x["share"] <= 1 for x in t.values())
    assert rashi_aspect(1, 5) and not rashi_aspect(1, 2) and rashi_aspect(3, 6) and not rashi_aspect(3, 4)
    md = markdown(r, "T")
    assert "13a. KP system" in md and "13c. Convergence" in md and "How common" in md
    s = ledger.stats()
    assert s["scored"] >= 39 and s["open"] >= 1 and 0.5 < s["overall_strict"] < 0.8


def test_base_rates_file():
    from engine.baserates import rate
    assert 0.4 < rate("dosha", "Manglik from lagna (6-house list)") < 0.6        # independent estimate: about 50%
    assert rate("yoga", "Dhana yoga") > 0.7                                       # near-universal: weak evidence


def test_yoga_catalogue_coverage():
    from engine.yogas_extra import coverage, detect, catalogue
    from engine.analysis import View
    cv = coverage()
    assert cv["catalogue"] == 181 and len(cv["not_coded"]) == 0
    ids = {x["id"] for x in detect(View(C))}
    assert {"mriti", "kuhu", "daridra_pd"} <= ids                 # 3L Jupiter in 12th, 4L/11L Mars in 8th
    assert ids <= set(catalogue())
    from engine.baserates import rate
    assert 0.2 < rate("cat", "kuhu") < 0.3                         # a lord falls in 3 of 12 houses: 25% by arithmetic


def test_place_lookup_offline():
    from engine.places import resolve
    p = resolve("Hubli")
    assert p and abs(p["lat"] - 15.35) < 0.1 and abs(p["lon"] - 75.13) < 0.1 and p["tz"] == "Asia/Kolkata"
    assert resolve("Hebballi-no-such-village") is None
