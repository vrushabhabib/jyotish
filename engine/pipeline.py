"""One road for every reading, with a gate at each step (built 13 Nov 2026). A step cannot run until the one before it passed.

    python3 -m engine.pipeline preflight                       # tests on both engines, repo in step with GitHub
    python3 -m engine.pipeline start SLUG DATE TIME LAT LON TZ --name N --sex F|M --window MIN --events-before-chart yes|no --out DIR
    python3 -m engine.pipeline verify SLUG                     # needs scored checking questions in the ledger
    python3 -m engine.pipeline gate SLUG DRAFT.md --verdicts VERDICTS.json [--requester R --subject S]
    python3 -m engine.pipeline send SLUG DRAFT.md --out FINAL.md
    python3 -m engine.pipeline status [SLUG]

The case file data/cases/SLUG.json holds only the state of each step (no dated events), so any later chat can see where a
case stands and what is still owed. Dated events live in the private store (engine/private_store.py), never in this repository.
"""
from __future__ import annotations
import argparse, datetime as dt, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASES = os.path.join(ROOT, "data", "cases")
STEPS = ["start", "verify", "gate", "send"]


def _path(slug): return os.path.join(CASES, f"{slug}.json")


def load(slug):
    return json.load(open(_path(slug))) if os.path.exists(_path(slug)) else {"case": slug, "steps": {}}


def save(c):
    os.makedirs(CASES, exist_ok=True); json.dump(c, open(_path(c["case"]), "w"), indent=1)


def _need(c, step):
    i = STEPS.index(step)
    for prev in STEPS[:i]:
        if not c["steps"].get(prev, {}).get("passed"):
            raise SystemExit(f"BLOCKED: step '{prev}' has not passed for case '{c['case']}'. Run it first.")


def _mark(c, step, passed, **detail):
    c["steps"][step] = {"passed": bool(passed), "at": dt.datetime.now().isoformat(timespec="minutes"), **detail}
    for later in STEPS[STEPS.index(step) + 1:]: c["steps"].pop(later, None)        # anything after a re-run step must be redone
    save(c)


def preflight():
    ok = True
    for env in ({}, {"JYOTISH_BACKEND": "ephem"}):
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "tests"], cwd=ROOT, env={**os.environ, **env}, capture_output=True, text=True)
        line = (r.stdout.strip().splitlines() or ["no output"])[-1]; print(("ephem   " if env else "default ") + line); ok &= r.returncode == 0
    g = subprocess.run(["git", "status", "-sb"], cwd=ROOT, capture_output=True, text=True).stdout.splitlines()
    print("git:", g[0] if g else "?", "| uncommitted files:", max(0, len(g) - 1)); ok &= bool(g) and "ahead" not in g[0] and "behind" not in g[0]
    from engine.findings import pending
    print(f"methods in the texts but not computed: {len(pending())} (printed on every worksheet)")
    print("PREFLIGHT", "PASSED" if ok else "FAILED"); return ok


def start(o):
    from engine import report
    if o.events_before_chart != "yes":
        print("NOTE: dated events were not collected before the chart was shown - any dates this person now gives are anchored and will not count as evidence.")
    r = report.build(o.date, o.time, o.lat, o.lon, o.tz, o.name or o.slug, o.sex, o.window)
    md = report.markdown(r, o.name or o.slug) + report.F.markdown(r["findings"]) + report.other_clocks_md(r)
    os.makedirs(o.out, exist_ok=True); stem = os.path.join(o.out, f"{o.slug}_{o.date}")
    open(stem + ".worksheet.md", "w").write(md); json.dump(report.to_json(r), open(stem + ".computed.json", "w"))
    c = load(o.slug); fs = r["findings"]
    _mark(c, "start", True, computed=stem + ".computed.json", worksheet=stem + ".worksheet.md", window_min=o.window,
          events_before_chart=o.events_before_chart == "yes", findings=len(fs), must=sum(f["weight"] == "must" for f in fs),
          backend=r["chart"]["input"].get("backend"), not_computed=len(r["pending"]))
    print(f"started {o.slug}: {len(fs)} findings ({c['steps']['start']['must']} MUST). Worksheet: {stem}.worksheet.md")


def verify(o):
    from engine import ledger
    c = load(o.slug); _need(c, "verify")
    rows = [r for r in ledger.load() if r["chart"] == o.slug]
    # Two different questions, kept apart (audit 13 Nov 2026): cold answers about the past confirm the CHART;
    # sealed blind statements test the TIMING RULES. Mixing them hid both figures.
    done = lambda k: [r for r in rows if r.get("kind") == k and r.get("outcome") not in ("open", None)]
    rate_of = lambda rs: (sum(r["outcome"] == "hit" for r in rs) + 0.5 * sum(r["outcome"] == "partly" for r in rs)) / len(rs) if rs else 0.0
    scored, blind = done("past"), done("blind")
    rate = rate_of(scored)
    ok = len(scored) >= o.min
    _mark(c, "verify", ok, scored=len(scored), rate=round(rate, 2), confirmed=rate >= 0.7, blind_scored=len(blind), blind_rate=round(rate_of(blind), 2))
    print(f"{len(scored)} checking questions scored, {rate*100:.0f}% right." + ("" if ok else f" BLOCKED: at least {o.min} are needed.")
          + ("" if rate >= 0.7 or not ok else " Below 70%: say so and limit the reading to timing of periods."))
    if blind:
        print(f"Sealed blind statements scored: {len(blind)}, {rate_of(blind)*100:.0f}% right - quote this beside any dated statement.")
    return ok


def gate(o):
    from engine import findings as F, lint as L, review as R
    c = load(o.slug); _need(c, "gate")
    fs = json.load(open(c["steps"]["start"]["computed"]))["findings"]; text = open(o.draft, encoding="utf-8").read()
    missing, waived, unknown = F.check(fs, text)
    errs, warns = L.lint(fs, text, o.requester, o.subject)
    rev = R.record(fs, text, json.load(open(o.verdicts))) if o.verdicts else {"passed": False, "not_reviewed": "no verdicts file"}
    for f in missing: print(f"  MISSING [F:{f['id']}] {f['text'][:120]}")
    for u in unknown: print(f"  UNKNOWN tag [F:{u}]")
    for k, n, w, s in errs: print(f"  {k} paragraph {n}: '{w}' | {s}")
    if not rev["passed"]: print("  REVIEW not passed:", {k: v for k, v in rev.items() if k in ("not_reviewed", "not_supported")})
    ok = not missing and not unknown and not errs and rev["passed"]
    _mark(c, "gate", ok, draft=R.digest(text), missing=len(missing), waived=len(waived), lint_errors=len(errs), review_passed=rev["passed"])
    print("GATE", "PASSED" if ok else "FAILED"); return ok


def send(o):
    from engine import findings as F, review as R, ledger
    c = load(o.slug); _need(c, "send")
    text = open(o.draft, encoding="utf-8").read()
    if R.digest(text) != c["steps"]["gate"]["draft"]:
        raise SystemExit("BLOCKED: the draft has changed since it passed the gate. Run the gate again.")
    fwd = [r for r in ledger.load() if r["chart"] == o.slug and r.get("kind") == "forward"]
    open(o.out, "w", encoding="utf-8").write(F.strip(text))
    _mark(c, "send", True, final=o.out, forward_statements_logged=len(fwd))
    print(f"final copy written to {o.out} (tags removed). Forward statements in the ledger for this case: {len(fwd)}"
          + ("" if fwd else " - if the reading contains any dated forward statement, log it now."))


def status(slug=None):
    names = [slug] if slug else sorted(f[:-5] for f in os.listdir(CASES) if f.endswith(".json")) if os.path.isdir(CASES) else []
    if not names: print("no cases yet")
    for n in names:
        c = load(n); done = [s for s in STEPS if c["steps"].get(s, {}).get("passed")]
        nxt = next((s for s in STEPS if s not in done), None)
        print(f"{n}: passed {', '.join(done) or 'nothing'}; next: {nxt or 'complete'}")
        if slug: print(json.dumps(c["steps"], indent=1))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter); sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("preflight")
    s = sub.add_parser("start"); s.add_argument("slug"); s.add_argument("date"); s.add_argument("time"); s.add_argument("lat", type=float); s.add_argument("lon", type=float); s.add_argument("tz")
    s.add_argument("--name"); s.add_argument("--sex"); s.add_argument("--window", type=int, required=True); s.add_argument("--events-before-chart", choices=("yes", "no"), required=True); s.add_argument("--out", required=True)
    v = sub.add_parser("verify"); v.add_argument("slug"); v.add_argument("--min", type=int, default=8)
    g = sub.add_parser("gate"); g.add_argument("slug"); g.add_argument("draft"); g.add_argument("--verdicts"); g.add_argument("--requester"); g.add_argument("--subject")
    d = sub.add_parser("send"); d.add_argument("slug"); d.add_argument("draft"); d.add_argument("--out", required=True)
    t = sub.add_parser("status"); t.add_argument("slug", nargs="?")
    o = ap.parse_args(argv)
    if o.cmd == "preflight": return 0 if preflight() else 1
    if o.cmd == "start": start(o); return 0
    if o.cmd == "verify": return 0 if verify(o) else 1
    if o.cmd == "gate": return 0 if gate(o) else 1
    if o.cmd == "send": send(o); return 0
    status(o.slug); return 0


if __name__ == "__main__":
    raise SystemExit(main())
