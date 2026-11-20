import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_business_synastry_is_labelled_unsourced():
    from engine.chart import build_chart
    from engine.matching import business_synastry
    a = build_chart("1987-02-03", "06:28", 15.3333, 75.1333, "Asia/Kolkata", "x")
    b = build_chart("1985-11-27", "08:00", 15.3333, 75.1333, "Asia/Kolkata", "x")
    r = business_synastry(a, b)
    assert "UNSOURCED" in r["source"]
    assert any(f.get("shared") for f in r["factors"])
