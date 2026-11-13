"""Intake of dated life events from a NEW person - the data that decides whether any rule is real.

    python3 -m engine.intake check  PRIVATE/name_events.json          # validate the file
    python3 -m engine.intake run    PRIVATE/name_events.json --n 1000 # control test; counts only saved, tagged 'confirmation'
    python3 -m engine.intake status                                   # how far the confirmation set has got

The events file stays OUTSIDE the repository. Format:
  {"name": "...", "sex": "F|M", "collected_before_chart_shown": true,
   "birth": {"date": "YYYY-MM-DD", "time": "HH:MM", "lat": .., "lon": .., "tz": "Asia/Kolkata", "time_doubt_min": 10},
   "events": [{"area": "career", "date": "YYYY-MM-DD", "polarity": "good|bad|null", "exact": true, "from_document": false}]}
People entered here are the CONFIRMATION SET for the frozen rules (antar-event-rules.md, Rules 18-19): target 25+ good/bad
events from people who are not among the first five. Form to send: data/intake/EVENTS_FORM.md
"""
from __future__ import annotations
import argparse, datetime as dt, json, os, sys
from engine.report import AREAS

LOG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "control_tests.json")
FIRST_FIVE = ("vrushab", "dhananjay", "hoang", "saira", "tanzil")
TARGET = 25


def validate(d):
    errs, warns = [], []
    b = d.get("birth") or {}
    for k in ("date", "time", "lat", "lon"):
        if k not in b: errs.append(f"birth.{k} missing")
    try: dt.date.fromisoformat(b.get("date", "")); dt.time.fromisoformat(b.get("time", "")[:5])
    except ValueError: errs.append("birth date or time not in YYYY-MM-DD / HH:MM")
    if d.get("collected_before_chart_shown") is not True:
        errs.append("collected_before_chart_shown must be true - dates given after seeing the chart are anchored and do not count")
    ev = d.get("events") or []
    if len(ev) < 10: warns.append(f"only {len(ev)} events; 10-15 asked for")
    for i, e in enumerate(ev, 1):
        if e.get("area") not in AREAS: errs.append(f"event {i}: area '{e.get('area')}' not one of {sorted(AREAS)}")
        try:
            when = dt.date.fromisoformat(e.get("date", ""))
            if b.get("date") and when <= dt.date.fromisoformat(b["date"]): errs.append(f"event {i}: before birth")
            if when > dt.date.today(): errs.append(f"event {i}: in the future")
        except ValueError: errs.append(f"event {i}: date must be YYYY-MM-DD (use the 15th for a known month, 1 July for a known year, and set exact false)")
        if e.get("polarity") not in ("good", "bad", None): errs.append(f"event {i}: polarity must be good, bad or null")
        if "exact" not in e: warns.append(f"event {i}: 'exact' not given, treated as false")
    if any(n in (d.get("name") or "").lower() for n in FIRST_FIVE): warns.append("this name is one of the first five - not part of the confirmation set")
    return errs, warns


def status():
    rows = json.load(open(LOG)) if os.path.exists(LOG) else []
    conf = [r for r in rows if r.get("set") == "confirmation"]
    n = sum(r.get("polarity_events", 0) for r in conf)
    return {"people": len(conf), "good_bad_events": n, "target": TARGET, "reached": n >= TARGET}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=("check", "run", "status")); ap.add_argument("file", nargs="?"); ap.add_argument("--n", type=int, default=1000)
    o = ap.parse_args(argv)
    if o.cmd == "status":
        s = status(); print(f"Confirmation set: {s['people']} people, {s['good_bad_events']} good/bad events of the {s['target']} needed" + (" - REACHED: score the frozen rules on this set alone" if s["reached"] else "")); return 0
    d = json.load(open(o.file)); errs, warns = validate(d)
    for w in warns: print("warning:", w)
    for e in errs: print("ERROR:", e)
    if errs: return 1
    print(f"ok: {len(d['events'])} events, {sum(1 for e in d['events'] if e.get('polarity'))} good/bad, {sum(1 for e in d['events'] if e.get('exact'))} exact")
    if o.cmd == "run":
        from engine.control import control_test, markdown
        res = control_test(d["birth"], d.get("sex"), d["events"], n=o.n)
        print(markdown(res, "confirmation chart"))
        rows = json.load(open(LOG)) if os.path.exists(LOG) else []
        is_new = not any(n in (d.get("name") or "").lower() for n in FIRST_FIVE)
        rows.append({"chart": f"confirmation person {sum(1 for r in rows if r.get('set') == 'confirmation') + 1}" if is_new else "one of the first five",
                     "set": "confirmation" if is_new else "first five", "run": dt.date.today().isoformat(), "events": len(d["events"]),
                     "polarity_events": sum(1 for e in d["events"] if e.get("polarity")), "controls": o.n, "rules": res.get("rules", res)})
        json.dump(rows, open(LOG, "w"), indent=1); print("counts saved (no names, no dates).", status())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
