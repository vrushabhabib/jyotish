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
Scoring: hit = 1, partly = 0.5, miss = 0. Brier score is reported where a confidence was stated.
"""
from __future__ import annotations
import json, os, sys, argparse, datetime as dt
from collections import defaultdict

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "ledger.jsonl")
VAL = {"hit": 1.0, "partly": 0.5, "miss": 0.0}
# Verification rounds done before the ledger existed. Only part of them is itemised in the ledger file, so the
# ledger's own percentage is too rosy until more items are logged. This aggregate is the honest headline.
LEGACY = {"Hoang Anh": (14, 20), "Saira": (5, 14), "Tanzil": (5, 5)}


def load():
    if not os.path.exists(PATH): return []
    return [json.loads(l) for l in open(PATH) if l.strip()]


def save(rows):
    with open(PATH, "w") as f:
        for r in rows: f.write(json.dumps(r, ensure_ascii=False) + "\n")


def add(chart, statement, category="timing", kind="forward", window=None, basis="", confidence=None,
        outcome="open", made=None, note=""):
    rows = load()
    rid = f"{chart}-{len([r for r in rows if r['chart'] == chart]) + 1:03d}"
    rows.append({"id": rid, "chart": chart, "made": made or dt.date.today().isoformat(), "kind": kind,
                 "category": category, "statement": statement, "window": window, "basis": basis,
                 "confidence": confidence, "outcome": outcome,
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
    rows = load() if rows is None else rows
    done = [r for r in rows if r["outcome"] in VAL]
    def agg(key):
        g = defaultdict(list)
        for r in done: g[r[key]].append(VAL[r["outcome"]])
        return {k: {"n": len(x), "rate": round(sum(x) / len(x), 2)} for k, x in sorted(g.items())}
    br = [(r["confidence"] - VAL[r["outcome"]]) ** 2 for r in done if r.get("confidence") is not None]
    lh = sum(a for a, _ in LEGACY.values()); ln = sum(b for _, b in LEGACY.values())
    return {"legacy_record": {"by_chart": {k: f"{a}/{b}" for k, (a, b) in LEGACY.items()}, "hits": lh, "asked": ln, "rate": round(lh / ln, 2),
                              "note": "all verification questions asked up to Oct 2026; only 13 of the 39 are itemised below"},
            "total": len(rows), "scored": len(done), "open": len(rows) - len(done),
            "overall": round(sum(VAL[r["outcome"]] for r in done) / len(done), 2) if done else None,
            "by_category": agg("category"), "by_kind": agg("kind"), "by_chart": agg("chart"),
            "brier": round(sum(br) / len(br), 3) if br else None,
            "open_items": [{k: r[k] for k in ("id", "statement", "window", "basis")} for r in rows if r["outcome"] == "open"]}


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
