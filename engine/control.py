"""Control-chart test: does a person's real chart explain their dated life events better than wrong charts do?

    python3 -m engine.control EVENTS.json --n 500 [--save]

EVENTS.json (kept OUTSIDE the repository - it holds dated personal events):
    {"name": "x", "sex": "M", "birth": {"date": "YYYY-MM-DD", "time": "HH:MM", "lat": .., "lon": .., "tz": "Asia/Kolkata"},
     "events": [{"area": "career", "date": "YYYY-MM-DD", "polarity": "good"|"bad"|null, "exact": true|false}, ...]}
Areas are the rows of the worksheet's link test (engine.report.AREAS).

Method. Each rule the readings rely on is applied to the real chart and to N control charts - the same events,
the same place, but a birth moment drawn at random within a few years of the real one. A rule that carries
information about this person scores clearly higher on the real chart than on the controls. The figure that
matters is "share of control charts scoring at least as high as the real chart": near 50% means the rule says
nothing about this person; under about 5% would be worth attention - and with a handful of events even that is
weak evidence.

Rules scored (all taken from the worksheet, nothing new):
    ad_link        the running sub-period lord is STRONGLY linked to the event's area (link test, Rule 1)
    md_link        the running main-period lord is strongly linked to it
    movable        the sub-period lord is the area's movable significator (Rule 13 - under test)
    link_or_mov    ad_link or movable
    polarity       events marked good/bad only: good = sub-lord not in the 6th/8th/12th from the dasha lord and no
                   caution flag (Jataka Parijata 18.27-28); bad = one of those present
    link_and_pol   ad_link and polarity together (what a dated statement of gain or loss actually rests on)

Only counts are printed or saved. Added 13 Nov 2026 (owner's instruction: fix the system for accuracy)."""
from __future__ import annotations
import argparse, datetime as dt, json, random
from engine.chart import build_chart
from engine.analysis import analyse, period_cautions
from engine.report import AREAS, MOVABLE

STRONG = ("occupies", "owns", "with", "is karaka")
RULES = ["ad_link", "md_link", "movable", "link_or_mov", "polarity", "link_and_pol"]


def _date(x):
    return x.date() if hasattr(x, "date") else x


def _periods(chart, when):
    for m in chart["dasha"]["maha"]:
        for ad in m["antar"]:
            if _date(ad["start"]) <= when < _date(ad["end"]):
                return m["lord"], ad["lord"]
    return None, None


def score(birth, sex, events):
    """Hits per rule for one chart. Returns ({rule: hits}, {rule: events the rule could be applied to})."""
    c = build_chart(birth["date"], birth["time"], birth["lat"], birth["lon"], birth.get("tz", "Asia/Kolkata"))
    a = analyse(c, sex=sex); v = a["view"]
    caut = period_cautions(v); ck = a["karakas"]["seven_bphs"]
    hits = dict.fromkeys(RULES, 0); base = dict.fromkeys(RULES, 0)
    for e in events:
        when = dt.date.fromisoformat(e["date"])
        md, ad = _periods(c, when)
        if ad is None:
            continue
        hs, km, kf = AREAS[e["area"]]
        ks = kf if sex == "F" else km
        strong = lambda p: any(x.startswith(STRONG) for x in v.sambandha(p, hs, ks))
        adl, mdl = strong(ad), strong(md)
        mov = ck.get(MOVABLE.get(e["area"], "")) == ad
        for k, val in (("ad_link", adl), ("md_link", mdl), ("movable", mov), ("link_or_mov", adl or mov)):
            base[k] += 1; hits[k] += bool(val)
        pol = e.get("polarity")
        if pol in ("good", "bad"):
            n = 1 if md == ad else (c["planets"][ad]["rashi"] - c["planets"][md]["rashi"]) % 12 + 1
            against = n in (6, 8, 12) or bool(caut.get(ad))
            ok = (not against) if pol == "good" else against
            for k, val in (("polarity", ok), ("link_and_pol", ok and adl)):
                base[k] += 1; hits[k] += bool(val)
    return hits, base


def control_test(birth, sex, events, n=500, years_before=6.0, years_after=3.0, seed=1987):
    """Real chart against n control charts. Control births fall between `years_before` before and `years_after`
    after the real birth, never later than a month before the earliest event, never within 30 days of the real one."""
    rng = random.Random(seed)
    real, base = score(birth, sex, events)
    b0 = dt.datetime.fromisoformat(birth["date"] + "T" + birth["time"][:5])
    first = min(dt.date.fromisoformat(e["date"]) for e in events)
    hi = min(years_after * 365.25, (first - b0.date()).days - 30)
    lo = -years_before * 365.25
    ctrl = {k: [] for k in RULES}
    done = 0
    while done < n:
        off = rng.uniform(lo, hi)
        if abs(off) < 30:
            continue
        t = b0 + dt.timedelta(days=off, minutes=rng.uniform(0, 1440))
        h, _ = score({**birth, "date": t.strftime("%Y-%m-%d"), "time": t.strftime("%H:%M")}, sex, events)
        for k in RULES:
            ctrl[k].append(h[k])
        done += 1
    out = {}
    for k in RULES:
        xs = ctrl[k]
        out[k] = {"real": real[k], "of": base[k], "control_mean": round(sum(xs) / len(xs), 2),
                  "share_controls_at_or_above_real": round(sum(1 for x in xs if x >= real[k]) / len(xs), 3)}
    return {"events": len(events), "exact_dates": sum(1 for e in events if e.get("exact")), "controls": n, "rules": out}


def markdown(res, name="chart"):
    L = [f"Control-chart test - {name}: {res['events']} dated events ({res['exact_dates']} with an exact date), "
         f"{res['controls']} control charts.\n",
         "| Rule | Real chart | Control average | Controls scoring as high or higher |", "|---|---|---|---|"]
    for k in RULES:
        r = res["rules"][k]
        L.append(f"| {k} | {r['real']} of {r['of']} | {r['control_mean']} | {r['share_controls_at_or_above_real'] * 100:.0f}% |")
    L.append("\nNear 50% in the last column = the rule says nothing about this person. Under about 5% would deserve "
             "attention, and with so few events even that is weak evidence.")
    return "\n".join(L)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("events"); ap.add_argument("--n", type=int, default=500); ap.add_argument("--save", action="store_true")
    x = ap.parse_args()
    d = json.load(open(x.events))
    res = control_test(d["birth"], d.get("sex"), d["events"], n=x.n)
    print(markdown(res, d.get("name", "chart")))
    if x.save:                                   # counts only - never the events themselves
        import os
        p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "control_tests.json")
        allr = json.load(open(p)) if os.path.exists(p) else []
        allr.append({"chart": d.get("name", "chart"), "run": dt.date.today().isoformat(), **res})
        json.dump(allr, open(p, "w"), indent=1)
