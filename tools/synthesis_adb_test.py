"""Synthesis-mode timing test on Astro-Databank (protocol: docs/gauquelin/PRE-STATED-SYNTHESIS-ADB.md).

    python3 tools/synthesis_adb_test.py SAMPLE.json [--controls 200]

SAMPLE.json (kept outside the repo): [[date, time, utc_offset_h, lat, lon, sex, [[area, y, m, d], ...]], ...]
area codes: M marriage, C children, W career, F money, H home/mother. d = 0 when only the month is known."""
from __future__ import annotations
import argparse, datetime as dt, json, random, statistics
from engine import synthesis as S

AREA = {"M": "marriage", "C": "children", "W": "career", "F": "money", "H": "home/mother"}


def utc(date, time, off):
    t = dt.datetime.fromisoformat(f"{date}T{time}") - dt.timedelta(hours=off)
    return t.strftime("%Y-%m-%d"), t.strftime("%H:%M")


def score_chart(date, time, lat, lon, sex, events):
    """events: [(area_name, date)]. Returns (hits per area-set, clocks per event)."""
    cl = S.Clocks(date, time, lat, lon, "UTC", sex)
    b = cl.local.date()
    last = max(d for _, d in events)
    a0 = b + dt.timedelta(days=int(365.25 * 16))
    a1 = min(last + dt.timedelta(days=int(365.25 * 5)), b + dt.timedelta(days=int(365.25 * 80)))
    span = (a1 - a0).days
    sample = [a0 + dt.timedelta(days=int(span * i / 150)) for i in range(150)]
    sv = [cl.votes(d)[0] for d in sample]
    out = []
    for area, d in events:
        sc = sorted({sum(v[area].values()) for v in sv})
        level = None
        for lv in sc:
            n = sum(1 for v in sv if sum(v[area].values()) >= lv and sum(v[area].values()) >= 4)
            if n / len(sv) <= 0.34:
                level = lv; break
        ev = sum(cl.votes(d)[0][area].values())
        hit = level is not None and ev >= level and ev >= 4
        out.append((area, hit, ev))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument("sample"); ap.add_argument("--controls", type=int, default=200); ap.add_argument("--seed", type=int, default=2611)
    x = ap.parse_args(argv)
    rng = random.Random(x.seed)
    people, dropped = [], 0
    for date, time, off, lat, lon, sex, evs in json.load(open(x.sample)):
        bd = dt.date.fromisoformat(date)
        es = []
        for a, y, m, d in evs:
            if a not in AREA: continue
            ed = dt.date(y, m, d or 15)
            if (ed - bd).days < 365.25 * 16: dropped += 1; continue          # before the scored span (age 16)
            es.append((AREA[a], ed))
        if es: people.append((date, time, off, lat, lon, sex, es))
    real = {"marriage": [0, 0], "all": [0, 0]}; real_clocks = {"marriage": [], "all": []}
    ctrl_tot = {"marriage": [0] * x.controls, "all": [0] * x.controls}; ctrl_clocks = {"marriage": [], "all": []}
    for date, time, off, lat, lon, sex, es in people:
        ud, ut = utc(date, time, off)
        r = score_chart(ud, ut, lat, lon, sex, es)
        for area, hit, ev in r:
            for k in ("all",) + (("marriage",) if area == "marriage" else ()):
                real[k][0] += hit; real[k][1] += 1; real_clocks[k].append(ev)
        b0 = dt.datetime.fromisoformat(f"{ud}T{ut}"); first = min(d for _, d in es)
        hi = min(3 * 365.25, (first - b0.date()).days - 30 - 365.25 * 16); lo = -6 * 365.25
        for i in range(x.controls):
            while True:
                o = rng.uniform(lo, hi)
                if abs(o) >= 30: break
            t = b0 + dt.timedelta(days=o, minutes=rng.uniform(0, 1440))
            rc = score_chart(t.strftime("%Y-%m-%d"), t.strftime("%H:%M"), lat, lon, sex, es)
            for area, hit, ev in rc:
                ctrl_tot["all"][i] += hit
                if i < 20: ctrl_clocks["all"].append(ev)
                if area == "marriage":
                    ctrl_tot["marriage"][i] += hit
                    if i < 20: ctrl_clocks["marriage"].append(ev)
    res = {"people": len(people), "events_dropped_before_16": dropped, "controls": x.controls}
    for k in ("marriage", "all"):
        h, n = real[k]; cs = ctrl_tot[k]
        res[k] = {"events": n, "real_hits": h, "real_rate": round(h / n, 3), "control_mean_hits": round(statistics.mean(cs), 2),
                  "control_rate": round(statistics.mean(cs) / n, 3),
                  "share_controls_at_or_above_real": round(sum(1 for c in cs if c >= h) / len(cs), 3),
                  "mean_clocks_real": round(statistics.mean(real_clocks[k]), 2), "mean_clocks_control": round(statistics.mean(ctrl_clocks[k]), 2)}
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
