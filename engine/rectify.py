"""Birth-time scan and the three-level period table.

    python3 -m engine.rectify scan DATE T0 T1 LAT LON TZ --sex F [--events EVENTS.json] [--step 4]
    python3 -m engine.rectify fine DATE TIME LAT LON TZ --sex F --from YYYY-MM-DD --to YYYY-MM-DD

Why it exists (Rule 22, 15 Nov 2026). A birth time given from memory ("around noon", "in the afternoon") can be
wrong by hours. Over hours the rising sign changes several times AND the Moon moves far enough to shift every
dasha date by months. A reading made on the stated minute is then a reading of one candidate among several.

`scan` walks the whole window and, for every stretch with the same rising sign, prints
  - the rising sign and the time range,
  - how far the dasha dates stand from those of the stated time,
  - if a private events file is given: how many of the dated events fall in a sub-period whose lord is strongly
    linked to the event's area (the one rule with a faint edge in our tests), as lowest-highest across the stretch,
    and the same for the third-level lord on events dated to the day (Rule 21, untested).
It does NOT choose a time. With fewer than about ten independently dated events the scores of neighbouring
stretches overlap and nothing can be concluded - the output says so.

`fine` lists every third-level period in a date range with the areas each of the three running lords is strongly
linked to, so that a year can be read at all three levels and no level is skipped.

EVENTS.json is the control-test file (engine.control) and stays outside the repository."""
from __future__ import annotations
import argparse, datetime as dt, json
from engine.chart import build_chart
from engine.analysis import analyse, dasha_at
from engine.report import AREAS

STRONG = ("occupies", "owns", "with", "is karaka")
RN = ["Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya", "Tula", "Vrishchika", "Dhanu", "Makara", "Kumbha", "Meena"]


def _strong(v, sex, p, area):
    hs, km, kf = AREAS[area]
    return any(x.startswith(STRONG) for x in v.sambandha(p, hs, kf if sex == "F" else km))


def linked_areas(v, sex, p):
    return [ar for ar in AREAS if _strong(v, sex, p, ar)]


def fine(date, time, lat, lon, tz, sex, start, end):
    """Rows (md, ad, pd, from, to, areas_ad, areas_pd) for every third-level period overlapping start..end."""
    c = build_chart(date, time, lat, lon, tz); a = analyse(c, sex=sex); v = a["view"]
    rows = []
    for md, ms, me, ads in a["dasha_tree"]:
        for ad, s, e, pds in ads:
            for pd, ps, pe, _ in pds:
                if pe.date() <= start or ps.date() >= end: continue
                rows.append({"md": md, "ad": ad, "pd": pd, "from": ps.date(), "to": pe.date(),
                             "areas_ad": linked_areas(v, sex, ad), "areas_pd": linked_areas(v, sex, pd)})
    return rows


def fine_markdown(rows, birth_date=None):
    out = ["| Main | Sub | Third level | From | To | Age | Sub-period lord linked to | Third-level lord linked to |", "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        age = f"{(r['from'] - birth_date).days / 365.25:.1f}" if birth_date else ""
        out.append(f"| {r['md']} | {r['ad']} | {r['pd']} | {r['from']:%d %b %Y} | {r['to']:%d %b %Y} | {age} | {', '.join(r['areas_ad']) or '-'} | {', '.join(r['areas_pd']) or '-'} |")
    return "\n".join(out)


def _score(c, a, sex, events):
    v = a["view"]; tree = a["dasha_tree"]; tzi = tree[0][1].tzinfo
    ad_hit = ad_n = pd_hit = pd_n = 0; per = []
    for e in events:
        when = dt.date.fromisoformat(e["date"])
        path = dasha_at(tree, dt.datetime.combine(when, dt.time(12, 0), tzinfo=tzi))
        if len(path) < 2: continue
        adl = _strong(v, sex, path[1]["lord"], e["area"]); ad_n += 1; ad_hit += adl
        pdl = None
        if e.get("exact") and len(path) >= 3:
            pdl = _strong(v, sex, path[2]["lord"], e["area"]); pd_n += 1; pd_hit += pdl
        per.append((path[0]["lord"], path[1]["lord"], path[2]["lord"] if len(path) >= 3 else "", adl, pdl))
    return ad_hit, ad_n, pd_hit, pd_n, per


def scan(date, t0, t1, lat, lon, tz, sex, events=None, step=4, stated=None):
    """Segments of constant rising sign across t0..t1 with dasha shift and (optionally) event-link scores."""
    a0 = dt.datetime.fromisoformat(f"{date}T{t0}"); b0 = dt.datetime.fromisoformat(f"{date}T{t1}")
    ref = None
    if stated:
        cr = build_chart(date, stated, lat, lon, tz); ref = analyse(cr, sex=sex)["dasha_tree"][1][1]
    segs = []; cur = None; t = a0
    while t <= b0:
        hm = t.strftime("%H:%M")
        c = build_chart(date, hm, lat, lon, tz); a = analyse(c, sex=sex)
        lag = c["lagna"]["rashi"]; moon = c["planets"]["Moon"]
        key = (lag, moon["rashi"], moon["nakshatra"])
        if cur is None or key != cur["key"]:
            cur = {"key": key, "from": hm, "to": hm, "lagna": RN[lag - 1], "moon": RN[moon["rashi"] - 1], "star": moon["nakshatra"],
                   "ad": [], "pd": [], "shift": [], "n_ad": 0, "n_pd": 0}
            segs.append(cur)
        cur["to"] = hm
        if ref is not None:
            cur["shift"].append((a["dasha_tree"][1][1] - ref).days)
        if events:
            ah, an, ph, pn, _ = _score(c, a, sex, events)
            cur["ad"].append(ah); cur["pd"].append(ph); cur["n_ad"] = an; cur["n_pd"] = pn
        t += dt.timedelta(minutes=step)
    return segs


def scan_markdown(segs, n_events=0):
    out = ["| Born between | Rising sign | Moon | Dasha dates against the stated time | Events in a linked sub-period | Day-dated events in a linked third-level period |", "|---|---|---|---|---|---|"]
    for s in segs:
        sh = (f"{min(s['shift']):+d} to {max(s['shift']):+d} days" if s["shift"] else "-")
        ad = (f"{min(s['ad'])}-{max(s['ad'])} of {s['n_ad']}" if s["ad"] else "-")
        pd = (f"{min(s['pd'])}-{max(s['pd'])} of {s['n_pd']}" if s["pd"] and s["n_pd"] else "-")
        out.append(f"| {s['from']}-{s['to']} | {s['lagna']} | {s['moon']} ({s['star']}) | {sh} | {ad} | {pd} |")
    out.append("")
    if n_events < 10:
        out.append(f"**Only {n_events} dated events.** With fewer than about ten independently dated events these scores cannot separate one stretch from another; "
                   "the table shows what is possible, it does not choose a time. The scan never chooses a time by itself.")
    else:
        out.append("The scan does not choose a time. A stretch is preferred only if its score stands clear of the others AND the facts that flip with the rising sign agree.")
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scan"); s.add_argument("date"); s.add_argument("t0"); s.add_argument("t1")
    s.add_argument("lat", type=float); s.add_argument("lon", type=float); s.add_argument("tz")
    s.add_argument("--sex", default=None); s.add_argument("--events"); s.add_argument("--step", type=int, default=4); s.add_argument("--stated")
    f = sub.add_parser("fine"); f.add_argument("date"); f.add_argument("time")
    f.add_argument("lat", type=float); f.add_argument("lon", type=float); f.add_argument("tz")
    f.add_argument("--sex", default=None); f.add_argument("--from", dest="start", required=True); f.add_argument("--to", dest="end", required=True)
    x = ap.parse_args(argv)
    if x.cmd == "scan":
        ev = json.load(open(x.events))["events"] if x.events else None
        print(scan_markdown(scan(x.date, x.t0, x.t1, x.lat, x.lon, x.tz, x.sex, ev, x.step, x.stated), len(ev or [])))
    else:
        rows = fine(x.date, x.time, x.lat, x.lon, x.tz, x.sex, dt.date.fromisoformat(x.start), dt.date.fromisoformat(x.end))
        print(fine_markdown(rows, dt.date.fromisoformat(x.date)))


if __name__ == "__main__":
    main()
