"""Rule 21/22 (15 Nov 2026): third-level table and the birth-time scan. Invented birth, no real person."""
import datetime as dt
from engine import rectify as R
from engine.control import RULES, score

B = ("1990-01-01", "10:00", 12.97, 77.59, "Asia/Kolkata")


def test_fine_rows_are_continuous_and_cover_the_range():
    rows = R.fine(*B, "F", dt.date(2020, 1, 1), dt.date(2023, 1, 1))
    assert rows and rows[0]["from"] <= dt.date(2020, 1, 1) and rows[-1]["to"] >= dt.date(2023, 1, 1)
    for a, b in zip(rows, rows[1:]):
        assert abs((b["from"] - a["to"]).days) <= 1
    assert all(set(r["areas_pd"]) <= set(R.AREAS) for r in rows)


def test_scan_finds_a_change_of_rising_sign_and_never_chooses():
    segs = R.scan(B[0], "08:00", "13:00", *B[2:], "F", step=10, stated="10:00")
    assert len({s["lagna"] for s in segs}) >= 2
    assert any(abs(x) > 20 for s in segs for x in s["shift"])          # hours of doubt move the dasha dates by weeks
    md = R.scan_markdown(segs, 0)
    assert "does not choose a time" in md and "Only 0 dated events" in md


def test_third_level_rules_are_scored_only_on_day_dated_events():
    assert "pd_link" in RULES and "adpd_link" in RULES
    ev = [{"area": "career", "date": "2015-06-01", "exact": False}, {"area": "career", "date": "2016-03-10", "exact": True}]
    hits, base = score({"date": B[0], "time": B[1], "lat": B[2], "lon": B[3], "tz": B[4]}, "F", ev)
    assert base["ad_link"] == 2 and base["pd_link"] == 1 and base["adpd_link"] == 1
    assert hits["adpd_link"] <= hits["pd_link"] <= 1


def test_hybrid_sheet_gives_subject_verdict_and_hold_line_for_every_period():
    from engine import hybrid as H
    rs = H.rows(*B, "F", dt.date(2018, 1, 1), dt.date(2026, 1, 1), dt.date(2024, 1, 1), dt.date(2025, 1, 1))
    assert rs and all(r["verdict"] in ("favourable", "mixed", "difficult") for r in rs)
    assert any(r["fine"] for r in rs) and all(set(r["holds"]) | set(r["not_hold"]) == set(H.AREAS) for r in rs)
    md = H.markdown(rs)
    assert "Tradition's verdict" in md and "Hold line" in md and "age" in md
    assert "hold_rule" in RULES


def test_completeness_check_names_what_a_script_leaves_out():
    from engine import complete as C
    assert "vehicles" in C.missing("# Work and business\n## Money\n")
    full = "\n".join("## " + words[0] for words in C.ASPECTS.values())
    assert C.missing(full) == []
