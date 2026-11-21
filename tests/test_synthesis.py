import datetime as dt
from engine import synthesis as S

B = ("1987-02-03", "06:28", 15.35, 75.13, "Asia/Kolkata")


def test_ordinal():
    assert [S._ord(n) for n in (1, 2, 3, 4, 11, 12, 21)] == ["1st", "2nd", "3rd", "4th", "11th", "12th", "21st"]


def test_windows_are_selective_and_need_four_clocks():
    res = S.run(*B, "M", years=10, start=dt.date(2027, 1, 1))
    for ar, d in res["windows"].items():
        assert d["share"] <= 0.34, ar
        for w in d["windows"]:
            assert w["peak"] >= 4 and w["tone"] in ("favourable", "mixed", "difficult")


def test_dossier_counts_every_angle_and_connections_join_areas():
    res = S.run(*B, "M", years=1, start=dt.date(2027, 1, 1))
    d = res["dossier"]["money"]
    assert d["net"] == len(d["for"]) - len(d["against"]) and d["verdict"]
    texts = " ".join(x["text"] for x in res["connections"])
    assert "move together" in texts                      # one planet ruling two houses is reported as a joined pair


def test_wide_spans_are_flagged_as_untestable():
    ev = [{"area": "career", "from": "2008-01-01", "to": "2011-01-01", "label": "wide"}]
    res = S.run(*B, "M", events=ev, years=1, start=dt.date(2027, 1, 1))
    assert res["calibration"]["check"][0]["informative"] is False
