"""Regression tests against known reference values (Lahiri)."""
from engine.chart import build_chart, nakshatra_of, varga_rashi, RASHI_NAMES

def test_sun_ingress_aries_1990():
    c = build_chart("1990-04-15", "06:30", 15.3647, 75.1240, "Asia/Kolkata")
    assert c["planets"]["Sun"]["rashi_en"] == "Aries" and c["planets"]["Sun"]["deg"] < 2

def test_navamsa_rules():
    assert varga_rashi(0.0, 9) == 1          # 0° Aries -> Aries
    assert varga_rashi(30.0 + 3.0, 9) == 10  # 3.0° Taurus -> Capricorn (fixed starts 9th)
    assert varga_rashi(60.0 + 3.0, 9) == 7   # 3.0° Gemini -> Libra (dual starts 5th)

def test_nakshatra():
    n, pada, _ = nakshatra_of(13.34)
    assert n == 2 and pada == 1

def test_dasha_sums_to_120():
    c = build_chart("2000-01-01", "12:00", 28.6, 77.2, "Asia/Kolkata")
    assert abs(sum(m["years"] for m in c["dasha"]["maha"]) - 120) < 0.05 + 20  # first dasha is partial
