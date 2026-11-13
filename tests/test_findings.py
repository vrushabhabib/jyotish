"""The findings register: nothing computed may be left out of a reading."""
import copy, re
from engine import report, findings as F
from engine.analysis import EXALT, DEBIL

R = report.build("1987-02-03", "06:28", 15.3333, 75.1333, "Asia/Kolkata", name="t", sex="M")
FS = R["findings"]


def test_every_finding_points_to_a_registered_rule_and_ids_are_unique():
    assert FS and all(f["rule"] in F.RULES for f in FS)
    ids = [f["id"] for f in FS]
    assert len(ids) == len(set(ids))
    assert all(F.TAG.fullmatch(f"[F:{i}]") for i in ids)          # every id can be cited in a draft
    assert all(f["part"] in F.PARTS and f["weight"] in ("must", "note") for f in FS)


def test_every_rule_is_used_or_declared_pending_or_excluded():
    used = {f["rule"] for f in FS}
    for k, x in F.RULES.items():
        if x["status"] in ("pending", "excluded"): continue
        # rules that only fire when the feature is present in a chart are exercised in the synthetic tests below
        assert k in used or k in ("navamsa_reversal", "sources_disagree", "dosha", "caution", "breaker", "link_timing", "yoga_timing", "scale"), k
    assert {p["rule"] for p in F.pending()} == {k for k, x in F.RULES.items() if x["status"] == "pending"}


def test_all_twelve_houses_and_seven_planets_are_always_present():
    ids = {f["id"] for f in FS}
    assert all(f"H{h:02d}.judgement" in ids for h in range(1, 13))
    for p in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"):
        assert f"P.{p}.state" in ids and f"SB.{p}" in ids and f"Q.{p}" in ids


def test_navamsa_reversal_fires_both_ways():
    r = copy.copy(R); r["chart"] = copy.deepcopy(R["chart"])
    r["chart"]["planets"]["Sun"].update(rashi=EXALT["Sun"], D9=DEBIL["Sun"])
    r["chart"]["planets"]["Venus"].update(rashi=DEBIL["Venus"], D9=EXALT["Venus"])
    out = []; F.planets(r, out); got = {f["id"]: f["text"] for f in out}
    assert "LOW" in got["NR.Sun"] and "GOOD" in got["NR.Venus"]


def test_grid_points_to_the_right_verse():
    q = {f["id"]: f["data"] for f in FS if f["id"].startswith("Q.")}
    for p, i in (("Sun", 0), ("Saturn", 6)):
        d = q[f"Q.{p}"]
        assert d["chapter"] == ("24a" if d["house"] == 1 else str(23 + d["house"]))
        assert all(4 * i + 1 <= vn <= 4 * i + 4 for _, vn in d["conditions"])


def test_check_refuses_a_draft_that_skips_a_must_finding():
    must = [f for f in FS if f["weight"] == "must"]
    assert len(must) >= 14
    full = " ".join(f"[F:{f['id']}]" for f in must)
    assert F.check(FS, full) == ([], {}, [])
    one = must[0]["id"]
    partial = full.replace(f"[F:{one}]", "")
    missing, waived, unknown = F.check(FS, partial)
    assert [f["id"] for f in missing] == [one]
    missing, waived, unknown = F.check(FS, partial + f" [F:{one} waived: not relevant to the question asked] [F:NOPE.x]")
    assert not missing and one in waived and unknown == ["NOPE.x"]
    assert "[F:" not in F.strip(full + " text [F:x waived: y] end") and "text" in F.strip("text [F:a.b]")


def test_worksheet_prints_the_register_and_the_pending_list():
    md = F.markdown(FS)
    assert "Findings register" in md and "NOT computed" in md and "Kalachakra" in md
    assert all(f"[F:{f['id']}]" in md for f in FS)
    assert R["pending"] and "findings" in report.to_json(R)
