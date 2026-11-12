"""Rules coded from the Sanskrit reading of 12 Nov 2026 (engine/classical.py, engine/rashmi.py)."""
import datetime as dt
from engine.chart import build_chart
from engine import classical as K, rashmi as RS, ashtakavarga as AV

C = build_chart("1990-05-15", "10:30", 18.52, 73.86, "Asia/Kolkata")


def test_vimshopaka_weights_and_bounds():
    assert abs(sum(K.W16.values()) - 20.0) < 1e-9          # BPHS 7.22-23
    v = K.vimshopaka(C)
    assert set(v) == set(K.SEVEN)
    assert all(5.0 <= x["points"] <= 20.0 for x in v.values())   # the scale runs from 5 (great enemy everywhere) to 20


def test_special_lagnas_rates():
    s = K.special_lagnas(C)
    h = s["hours_from_sunrise"]
    assert 0 <= h < 24
    # hora lagna runs twice as fast as bhava lagna, ghati lagna five times (BPHS 5.2-8)
    d_b = (s["bhava_lagna"]["lon"] - s["hora_lagna"]["lon"]) % 360
    assert abs(((-d_b) % 360) - (15.0 * h) % 360) < 0.5
    assert abs(((s["ghati_lagna"]["lon"] - s["bhava_lagna"]["lon"]) % 360) - (60.0 * h) % 360) < 0.5


def test_rays_at_exaltation_and_debilitation():
    c = {"planets": {p: {"rashi": 1, "deg": 0.0, "combust": False} for p in RS.RAYS}}
    c["planets"]["Sun"] = {"rashi": 1, "deg": 10.0, "combust": False}          # exalted at Aries 10
    c["planets"]["Saturn"] = {"rashi": 1, "deg": 20.0, "combust": False}       # debilitated at Aries 20
    r = RS.rashmi(c)["planets"]
    assert r["Sun"] == 10.0 and r["Saturn"] == 0.0                            # BPHS 73.1-2


def test_sav_blocks_add_to_337():
    b = K.sav_blocks(AV.ashtakavarga(C), C["lagna"]["rashi"])
    assert b["early"] + b["middle"] + b["late"] == 337


def test_bphs_variant_keeps_totals():
    a, b = AV.ashtakavarga(C), AV.ashtakavarga(C, "bphs")
    assert sum(a["sav"]) == sum(b["sav"]) == 337
    assert sum(a["bav"]["Moon"]) == sum(b["bav"]["Moon"]) == 49 and sum(b["bav"]["Venus"]) == 52


def test_fruition_shape():
    f = K.fruition(C, 7, dt.date(2020, 1, 1))
    assert set(f) == {"J", "L", "H", "M", "count"} and 0 <= f["count"] <= 4
    assert K.fruition(C, 1, dt.date(2020, 1, 1))["count"] <= 1               # house 1: only Jupiter's trigger applies


def test_birth_conditions_fields():
    b = K.birth_conditions(C)
    assert 1 <= b["tithi"] <= 30 and b["half"] in ("bright", "dark")
