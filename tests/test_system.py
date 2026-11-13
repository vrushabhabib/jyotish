"""Guards against process mistakes: frozen reference charts, ledger duplicates, draft linter, review record, pipeline gates."""
import datetime as dt, json, os, sys
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools"))
from make_golden import snapshot
from engine import report, findings as F, lint as L, review as R, ledger, pipeline as P

GOLD = json.load(open(os.path.join(os.path.dirname(__file__), "golden", "reference.json")))
R0 = report.build("1987-02-03", "06:28", 15.3333, 75.1333, "Asia/Kolkata", name="t", sex="M")
FS = R0["findings"]


def _days(a, b): return abs((dt.date.fromisoformat(a) - dt.date.fromisoformat(b)).days)


@pytest.mark.parametrize("g", GOLD, ids=[g["birth"][0] for g in GOLD])
def test_engine_output_has_not_drifted_from_the_frozen_reference(g):
    s = snapshot(tuple(g["birth"]))
    assert abs(s["lagna"] - g["lagna"]) < 0.01
    for p, lon in g["planets"].items(): assert abs((s["planets"][p] - lon + 180) % 360 - 180) < 0.003, p
    assert [m[0] for m in s["maha"]] == [m[0] for m in g["maha"]] and all(_days(a[1], b[1]) <= 2 for a, b in zip(s["maha"], g["maha"]))
    assert [k[0] for k in s["kalachakra"]] == [k[0] for k in g["kalachakra"]]
    assert s["sav"] == g["sav"] and s["d9"] == g["d9"]
    assert all(abs(s["rupas"][p] - v) < 0.05 for p, v in g["rupas"].items())
    assert s["finding_ids"] == g["finding_ids"]


def test_ledger_does_not_log_the_same_statement_twice(tmp_path, monkeypatch):
    monkeypatch.setattr(ledger, "PATH", str(tmp_path / "l.jsonl"))
    a = ledger.add("x", "same statement", window="2027-01-01:2027-06-01")
    b = ledger.add("x", "same statement", window="2027-01-01:2027-06-01")
    c = ledger.add("x", "another statement", window="2027-01-01:2027-06-01")
    assert a == b != c and len(ledger.load()) == 2


def test_linter_catches_forbidden_untagged_purity_and_overclaim():
    asp = next(f["id"] for f in FS if f["id"].startswith("ASP."))
    draft = "\n\n".join(["> method: Saturn and the lagna are explained here without a tag.",
                         "Saturn in the 11th brings gains.",
                         f"He will certainly prosper in this period. [F:{asp}]",
                         "She will have two sons and a long life span. [F:H05.judgement]",
                         "Vrushab asked for this reading. [F:H01.judgement]",
                         "The first house has its lord looking at it. [F:H01.judgement]"])
    kinds = [(k, n) for k, n, _, _ in L.lint(FS, draft, requester="Vrushab", subject="Someone Else")[0]]
    assert ("UNTAGGED", 2) in kinds and ("OVERCLAIM", 3) in kinds and ("FORBIDDEN", 4) in kinds and ("PURITY", 5) in kinds
    assert not any(n in (1, 6) for _, n in kinds)


def test_review_record_is_tied_to_the_exact_draft_and_needs_every_paragraph():
    draft = "First claim. [F:H01.judgement]\n\nSecond claim. [F:H07.judgement]"
    assert "H01.judgement" in R.packet(FS, draft) and "Paragraph 2" in R.packet(FS, draft)
    assert not R.record(FS, draft, [{"paragraph": 1, "verdict": "supported"}])["passed"]
    assert not R.record(FS, draft, [{"paragraph": 1, "verdict": "supported"}, {"paragraph": 2, "verdict": "beyond"}])["passed"]
    ok = R.record(FS, draft, [{"paragraph": 1, "verdict": "supported"}, {"paragraph": 2, "verdict": "supported"}])
    assert ok["passed"] and ok["draft"] != R.digest(draft + " edited")


def test_pipeline_blocks_a_step_until_the_one_before_has_passed(tmp_path, monkeypatch):
    monkeypatch.setattr(P, "CASES", str(tmp_path))
    c = P.load("demo")
    with pytest.raises(SystemExit): P._need(c, "gate")
    P._mark(c, "start", True); P._mark(c, "verify", True); P._need(c, "gate")
    P._mark(c, "gate", True, draft="abc"); P._need(c, "send")
    P._mark(c, "verify", False)                       # re-running an earlier step wipes what came after it
    assert "gate" not in P.load("demo")["steps"]
    with pytest.raises(SystemExit): P._need(P.load("demo"), "send")


def test_every_rule_used_by_a_finding_carries_a_text_quality_grade():
    assert all("text_quality" in F.RULES[f["rule"]] for f in FS)
    assert "text:" in F.markdown(FS)
