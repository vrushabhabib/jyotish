"""Prediction ledger: every statement that can be checked against life is logged BEFORE the answer is known,
then scored. This is the project's only real measure of predictive accuracy, and the source of the reliability
weights printed in worksheets.

    python3 -m engine.ledger report                      # hit rates by category, kind and basis
    python3 -m engine.ledger add --chart saira --category timing --kind forward \\
        --statement "pregnancy" --window 2027-11-29:2028-02-21 --basis "DT on 5th; Ven-Mars" --confidence 0.3
    python3 -m engine.ledger score <id> hit|partly|miss --note "..."

File: data/ledger.jsonl, one JSON object per line:
  id, chart, made, kind (retro = asked about the past, answered cold | forward = about the future),
  category (timing | description-self | description-other | family-structure | health | other),
  statement, window, basis, confidence (0..1, optional), outcome (open | hit | partly | miss), resolved, note
Scoring: hit = 1, partly = 0.5, miss = 0. Rows with count > 1 are aggregates of older questions whose text was not kept.
Caution: categories of the 2026 legacy rows were assigned after the answers were known ("event-in-sub-period" is the
class the misses fell into), so per-category rates are descriptive only until forward items mature. Brier score is reported where a confidence was stated.
"""
from __future__ import annotations
import json, os, sys, argparse, datetime as dt
from collections import defaultdict

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "ledger.jsonl")
VAL = {"hit": 1.0, "partly": 0.5, "miss": 0.0}


def load():
    if not os.path.exists(PATH): return []
    return [json.loads(l) for l in open(PATH) if l.strip()]


def save(rows):
    with open(PATH, "w") as f:
        for r in rows: f.write(json.dumps(r, ensure_ascii=False) + "\n")


def add(chart, statement, category="timing", kind="forward", window=None, basis="", confidence=None,
        outcome="open", made=None, note="", count=1):
    rows = load()
    rid = f"{chart}-{len([r for r in rows if r['chart'] == chart]) + 1:03d}"
    rows.append({"id": rid, "chart": chart, "made": made or dt.date.today().isoformat(), "kind": kind,
                 "category": category, "statement": statement, "window": window, "basis": basis,
                 "confidence": confidence, "outcome": outcome, "count": count,
                 "resolved": (made or dt.date.today().isoformat()) if outcome != "open" else None, "note": note})
    save(rows); return rid


def score(rid, outcome, note=""):
    rows = load()
    for r in rows:
        if r["id"] == rid:
            r["outcome"], r["resolved"] = outcome, dt.date.today().isoformat()
            if note: r["note"] = note
    save(rows)


def stats(rows=None):
    """Rows may carry 'count' > 1: an aggregate of several questions whose individual text was not recorded."""
    rows = load() if rows is None else rows
    done = [r for r in rows if r["outcome"] in VAL]
    n = lambda rs: sum(r.get("count", 1) for r in rs)
    def rate(rs): return round(sum(VAL[r["outcome"]] * r.get("count", 1) for r in rs) / n(rs), 2) if rs else None
    def strict(rs): return round(sum(r.get("count", 1) for r in rs if r["outcome"] == "hit") / n(rs), 2) if rs else None
    def agg(key):
        g = defaultdict(list)
        for r in done: g[r[key]].append(r)
        return {k: {"n": n(x), "rate": rate(x), "strict": strict(x)} for k, x in sorted(g.items())}
    br = [(r["confidence"] - VAL[r["outcome"]]) ** 2 for r in done if r.get("confidence") is not None]
    opened = [r for r in rows if r["outcome"] == "open"]
    return {"total": n(rows), "scored": n(done), "open": n(opened),
            "overall": rate(done), "overall_strict": strict(done),
            "note": "rate counts a partly-right answer as half; strict counts full hits only",
            "by_category": agg("category"), "by_kind": agg("kind"), "by_chart": agg("chart"),
            "brier": round(sum(br) / len(br), 3) if br else None,
            "open_items": [{k: r[k] for k in ("id", "statement", "window", "basis")} for r in opened]}


def reliability(category):
    """Measured hit rate for a category, or None when fewer than 5 scored items exist."""
    s = stats()["by_category"].get(category)
    return s["rate"] if s and s["n"] >= 5 else None


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("report")
    a = sub.add_parser("add")
    for f in ("chart", "statement", "category", "kind", "window", "basis", "note"): a.add_argument("--" + f, default=None)
    a.add_argument("--confidence", type=float)
    sc = sub.add_parser("score"); sc.add_argument("id"); sc.add_argument("outcome", choices=list(VAL)); sc.add_argument("--note", default="")
    x = ap.parse_args()
    if x.cmd == "add":
        print(add(x.chart, x.statement, x.category or "timing", x.kind or "forward", x.window, x.basis or "", x.confidence, note=x.note or ""))
    elif x.cmd == "score":
        score(x.id, x.outcome, x.note); print("scored", x.id)
    else:
        print(json.dumps(stats(), indent=1, ensure_ascii=False))
