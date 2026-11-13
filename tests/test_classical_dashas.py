"""Kalachakra and life-span dashas, question charts, intake."""
import datetime as dt, json
from zoneinfo import ZoneInfo
from engine import report, prashna, intake
from engine.chart import RASHI_LORD
from engine.dashas_classical import KC_SEQ, KC_TOTAL, KC_YEARS, KC_GROUP, kalachakra, kalachakra_at, lifespan_dasha

R = report.build("1987-02-03", "06:28", 15.3333, 75.1333, "Asia/Kolkata", name="t", sex="M")
C = R["chart"]


def test_every_kalachakra_sequence_adds_up_to_the_total_the_text_states():
    assert len(KC_SEQ) == 16 and len(KC_GROUP) == 27
    for k, seq in KC_SEQ.items():
        assert len(seq) == 9 and sum(KC_YEARS[RASHI_LORD[s - 1]] for s in seq) == KC_TOTAL[k], k
    assert sorted(set(KC_TOTAL.values())) == [83, 85, 86, 100]               # BPHS 46.89


def test_kalachakra_periods_are_continuous_and_subperiods_fill_each_period():
    kc = kalachakra(C["planets"]["Moon"]["lon"], C["input"]["local"])
    ps = kc["periods"]
    assert ps[0]["start"] == C["input"]["local"] and all(a["end"] == b["start"] for a, b in zip(ps, ps[1:]))
    for p in ps[1:6]:
        assert p["subs"][0]["start"] == p["start"] and abs((p["subs"][-1]["end"] - p["end"]).total_seconds()) < 2
        assert abs((p["end"] - p["start"]).days / 365.25 - KC_YEARS[p["lord"]]) < 0.01
    first_cycle = sum((p["end"] - p["start"]).days for p in ps if p["cycle"] == 1) / 365.25
    q = kc["quarter"]; total = KC_TOTAL[(q["group"], q["pada"])]
    assert abs(first_cycle - total * (1 - q["fraction_elapsed"])) < 0.05           # balance at birth
    assert kalachakra_at(kc, dt.datetime(2026, 11, 13, tzinfo=ZoneInfo("Asia/Kolkata")))[0] is not None


def test_lifespan_dasha_gives_periods_but_never_a_total():
    st = {q: d["rupas"] for q, d in R["shadbala"]["planets"].items()}
    ls = lifespan_dasha(C, st, when=dt.datetime(2026, 11, 13, tzinfo=ZoneInfo("Asia/Kolkata")))
    assert set(ls["order"]) == {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Lagna"}
    assert ls["order"][0] in ("Lagna", "Sun", "Moon")                              # Brihat Jataka 8.1
    assert not any(k in ls for k in ("total", "years", "span", "length"))
    ps = ls["periods"]; assert ps[0]["start"] == C["input"]["local"]
    assert all(a["end"] == b["start"] for a, b in zip(ps, ps[1:]))
    assert all(p["start"].year <= 2026 + 26 for p in ps)                           # nothing printed beyond the window


def test_question_chart_verdict_follows_the_fixed_rule_and_bans_excluded_subjects():
    when = dt.datetime(2026, 11, 13, 19, 10, tzinfo=ZoneInfo("Asia/Kolkata"))
    j = prashna.ask("Will the order be confirmed?", "gain", 15.35, 75.13, "Asia/Kolkata", "2026-12-01", when)
    assert j["total"] == sum(p["points"] for p in j["points"]) and all(p["source"] for p in j["points"])
    assert j["verdict"] == ("YES" if j["total"] >= 2 else "NO" if j["total"] <= -2 else "NO CALL")
    assert j["lagna_kind"] in ("movable", "fixed", "dual")
    for q in ("Will he recover from the illness?", "Is it a boy or girl?"):
        try: prashna.ask(q, "general", 15.35, 75.13, "Asia/Kolkata", "2026-12-01", when); assert False
        except SystemExit: pass


def test_intake_rejects_dates_given_after_the_chart_was_shown():
    d = {"name": "new person", "sex": "F", "collected_before_chart_shown": False,
         "birth": {"date": "1990-01-01", "time": "10:00", "lat": 15.0, "lon": 75.0},
         "events": [{"area": "career", "date": "2015-06-15", "polarity": "good", "exact": False}]}
    errs, warns = intake.validate(d); assert any("collected_before_chart_shown" in e for e in errs)
    d["collected_before_chart_shown"] = True; d["events"][0]["area"] = "nonsense"
    assert any("area" in e for e in intake.validate(d)[0])
    d["events"][0]["area"] = "career"; errs, warns = intake.validate(d); assert not errs and warns


def test_worksheet_carries_both_clocks_and_stored_verses():
    assert R["kalachakra"] and R["lifespan_dasha"]
    ids = {f["id"]: f for f in R["findings"]}
    assert "K.kalachakra" in ids and "K.lifespan" in ids
    assert "Kalachakra dasha" in report.other_clocks_md(R)
    g = json.load(open("data/vyj_grid.json"))["chapters"]
    assert "28" not in g and "31" not in g and len(g["33"]) == 28                 # children and death chapters are not stored
