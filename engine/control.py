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
    transit_moon / transit_bav / transit_sav   good/bad from where Jupiter and Saturn are passing on the day: houses
                   from the natal Moon (Phaladeepika 26), their own Ashtakavarga points, the combined points
    polarity_lp    good/bad by Laghu Parashari v.6-13 and 29-38: functional nature of the two lords and whether
                   they are related; table in kb/sources/laghu-parashari/README.md, written before the test was run
    polarity_ishta good/bad by Parashara's own measure (ch. 28): the sub-period lord's good share (ishta) against its
                   bad share (kashta); no call for Rahu and Ketu
    polarity_text  good/bad by Parashara's full sub-period template (ch. 52-60): sub-lord's house from the lagna,
                   its dignity, its house from the dasha lord - one point each; ties make no call

Only counts are printed or saved. Added 13 Nov 2026 (owner's instruction: fix the system for accuracy)."""
from __future__ import annotations
import argparse, datetime as dt, json, random
from engine.chart import build_chart
from engine.analysis import analyse, period_cautions
from engine.report import AREAS, MOVABLE
from engine.ashtakavarga import ashtakavarga
from engine import transits as T

STRONG = ("occupies", "owns", "with", "is karaka")
RULES = ["ad_link", "md_link", "movable", "link_or_mov", "polarity", "link_and_pol", "polarity_text", "polarity_ishta", "polarity_lp", "transit_moon", "transit_bav", "transit_sav", "polarity_natural"]


def _date(x):
    return x.date() if hasattr(x, "date") else x


def _periods(chart, when):
    for m in chart["dasha"]["maha"]:
        for ad in m["antar"]:
            if _date(ad["start"]) <= when < _date(ad["end"]):
                return m["lord"], ad["lord"]
    return None, None


def ishta_kashta(birth):
    """{planet: (ishta, kashta)} for the seven planets, in sixtieths (BPHS 28.2-6)."""
    from zoneinfo import ZoneInfo
    from engine.shadbala import shadbala
    t = dt.datetime.fromisoformat(birth["date"] + "T" + birth["time"][:5]).replace(tzinfo=ZoneInfo(birth.get("tz", "Asia/Kolkata")))
    sb = shadbala(birth["date"], birth["time"][:5], birth["lat"], birth["lon"], t.utcoffset().total_seconds() / 3600)
    pl = sb.get("planets", sb)
    out = {}
    for p, d in pl.items():
        if isinstance(d, dict) and "cheshta" in d and "uchcha" in d.get("sthana", {}):
            u, c = max(0.0, min(60.0, d["sthana"]["uchcha"])), max(0.0, min(60.0, d["cheshta"]))
            out[p] = ((u * c) ** 0.5, ((60 - u) * (60 - c)) ** 0.5)
    return out


def lp_nature(v):
    """Functional nature by Laghu Parashari v.6-13 (kb/sources/laghu-parashari/README.md): +1 benefic, -1 malefic, 0 neutral."""
    from engine.chart import RASHI_LORD
    own = {}
    for h in range(1, 13):
        own.setdefault(v.lord(h), []).append(h)
    nat = {}
    for p, hs in own.items():
        t = 0
        for h in hs:
            if h in (1, 5, 9): t += 1
            elif h in (3, 6, 11): t -= 1
            elif h == 8 and 1 not in hs and p not in ("Sun", "Moon"): t -= 1
        nat[p] = (t > 0) - (t < 0)
    for node in ("Rahu", "Ketu"):
        nat[node] = nat.get(RASHI_LORD[v.s[node] - 1], 0)
    return nat


def lp_call(v, nat, md, ad):
    """Laghu Parashari v.29-38: 'good', 'bad' or None (no call) for the sub-period of ad in the dasha of md."""
    if md == ad:
        return None
    m, a, rel = nat.get(md, 0), nat.get(ad, 0), v.linked(md, ad)
    if m > 0:
        if a > 0 or rel: return "good"
        return "bad" if a < 0 else None
    if m < 0:
        if a < 0: return "bad"
        if a > 0: return None if rel else "bad"
        return "bad" if rel else None
    return "good" if a > 0 else "bad" if a < 0 else None


def score(birth, sex, events):
    """Hits per rule for one chart. Returns ({rule: hits}, {rule: events the rule could be applied to})."""
    c = build_chart(birth["date"], birth["time"], birth["lat"], birth["lon"], birth.get("tz", "Asia/Kolkata"))
    a = analyse(c, sex=sex); v = a["view"]
    caut = period_cautions(v); ck = a["karakas"]["seven_bphs"]
    hits = dict.fromkeys(RULES, 0); base = dict.fromkeys(RULES, 0)
    ik = None; lpn = lp_nature(v); av = ashtakavarga(c)
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
            # Parashara's full template for a sub-period (ch. 52-60): the sub-lord's own house from the lagna, its
            # dignity, and its house from the dasha lord - one point each way. Specified from the text before
            # looking at any result; not tuned. A tie makes no call and is left out of the count.
            P = c["planets"][ad]; h = P["bhava"]; dg = (P.get("dignity") or "").lower(); t = 0
            t += 1 if h in (1, 4, 7, 10, 5, 9, 11) else -1 if h in (6, 8, 12) else 0
            t += 1 if any(w in dg for w in ("exalt", "own", "moola", "friend")) else -1 if (any(w in dg for w in ("debil", "enemy")) or P.get("combust")) else 0
            t += 0 if md == ad else (-1 if n in (6, 8, 12) else 1)
            if t != 0:
                base["polarity_text"] += 1; hits["polarity_text"] += (t > 0) == (pol == "good")
            # Parashara's own measure of a planet's good and bad share (BPHS ch. 28 v.2-6, kb/sources/bphs/ch21-30.md):
            # ishta = root of (exaltation strength x motional strength), kashta = root of the product of their
            # complements to 60. Stated before any result was seen: the period is called good when ishta exceeds
            # kashta. The nodes have neither strength, so no call is made for them.
            # Transit rules (Parashara 72.30-31 and Laghu Jataka 11.15: the particular good and bad comes from
            # planets in transit, read through Ashtakavarga). Three rules, written down before any result:
            #  transit_moon  Jupiter in the 2nd, 5th, 7th, 9th or 11th from the natal Moon = +1, else -1; Saturn in the
            #                3rd, 6th or 11th = +1, else -1 (Phaladeepika 26); sum above 0 good, below 0 bad, 0 no call
            #  transit_bav   (Jupiter's own Ashtakavarga points in the sign it is passing - 4) + the same for Saturn
            #  transit_sav   combined points of Jupiter's sign + Saturn's sign, against the average 56
            js, ss = T.sign_on("Jupiter", when), T.sign_on("Saturn", when)
            moon = v.s["Moon"]
            hj, hs_ = (js - moon) % 12 + 1, (ss - moon) % 12 + 1
            tm = (1 if hj in (2, 5, 7, 9, 11) else -1) + (1 if hs_ in (3, 6, 11) else -1)
            tb = (av["bav"]["Jupiter"][js - 1] - 4) + (av["bav"]["Saturn"][ss - 1] - 4)
            ts = av["sav"][js - 1] + av["sav"][ss - 1] - 56
            for k, val in (("transit_moon", tm), ("transit_bav", tb), ("transit_sav", ts)):
                if val != 0:
                    base[k] += 1; hits[k] += (val > 0) == (pol == "good")
            # Natural benefic / malefic sub-lord (the pattern of Vriddha Yavana Jataka ch. 7; stated before the test):
            # Jupiter, Venus, Mercury, Moon = good; Sun, Mars, Saturn = bad; no call for the nodes.
            if ad in ("Jupiter", "Venus", "Mercury", "Moon", "Sun", "Mars", "Saturn"):
                base["polarity_natural"] += 1
                hits["polarity_natural"] += (ad in ("Jupiter", "Venus", "Mercury", "Moon")) == (pol == "good")
            call = lp_call(v, lpn, md, ad)
            if call:
                base["polarity_lp"] += 1; hits["polarity_lp"] += call == pol
            if ik is None:
                ik = ishta_kashta(birth)
            if ad in ik:
                i_, k_ = ik[ad]
                base["polarity_ishta"] += 1; hits["polarity_ishta"] += (i_ > k_) == (pol == "good")
    return hits, base


def control_test(birth, sex, events, n=500, years_before=6.0, years_after=3.0, seed=1987, raw=False):
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
    if raw:
        return real, base, ctrl
    for k in RULES:
        xs = ctrl[k]
        out[k] = {"real": real[k], "of": base[k], "control_mean": round(sum(xs) / len(xs), 2),
                  "share_controls_at_or_above_real": round(sum(1 for x in xs if x >= real[k]) / len(xs), 3)}
    return {"events": len(events), "exact_dates": sum(1 for e in events if e.get("exact")), "controls": n, "rules": out}


def indicated(birth, sex, area, polarity, start, end):
    """Sub-periods between two dates that the rules point to for an event of this area and direction:
    sub-period lord strongly linked to the area (or its movable significator), and for a 'good' event not placed
    6th/8th/12th from the dasha lord and free of a caution flag; for a 'bad' event one of those present.
    Returns (windows, share): share = the part of the whole span the windows cover = the chance a randomly dated
    event would fall inside. Used to SEAL a statement before the person is asked for a date (Rule 16)."""
    c = build_chart(birth["date"], birth["time"], birth["lat"], birth["lon"], birth.get("tz", "Asia/Kolkata"))
    a = analyse(c, sex=sex); v = a["view"]; caut = period_cautions(v); ck = a["karakas"]["seven_bphs"]
    hs, km, kf = AREAS[area]; ks = kf if sex == "F" else km
    s0, e0 = dt.date.fromisoformat(start), dt.date.fromisoformat(end)
    out, days = [], 0
    for m in c["dasha"]["maha"]:
        for ad in m["antar"]:
            s, e = max(_date(ad["start"]), s0), min(_date(ad["end"]), e0)
            if s >= e:
                continue
            p = ad["lord"]
            link = any(x.startswith(STRONG) for x in v.sambandha(p, hs, ks)) or ck.get(MOVABLE.get(area, "")) == p
            n = 1 if m["lord"] == p else (c["planets"][p]["rashi"] - c["planets"][m["lord"]]["rashi"]) % 12 + 1
            against = n in (6, 8, 12) or bool(caut.get(p))
            ok = link and (polarity is None or (against if polarity == "bad" else not against))
            if ok:
                out.append((m["lord"], p, s.isoformat(), e.isoformat())); days += (e - s).days
    return out, round(days / max((e0 - s0).days, 1), 2)


def pool(cases, n=1000):
    """Several people together. cases: [{"birth":..., "sex":..., "events":[...]}]. For each rule the real hits are
    summed over all charts and compared with the sum of one independent control chart per person, n times.
    Returns the same table shape as control_test. One person's chart can look good or bad by luck; the pooled
    figure is the one to judge a rule by."""
    tot_real = dict.fromkeys(RULES, 0); tot_base = dict.fromkeys(RULES, 0)
    sums = {k: [0] * n for k in RULES}; ev = 0
    for i, c in enumerate(cases):
        real, base, ctrl = control_test(c["birth"], c.get("sex"), c["events"], n=n, seed=1987 + i, raw=True)
        ev += len(c["events"])
        for k in RULES:
            tot_real[k] += real[k]; tot_base[k] += base[k]
            sums[k] = [a + b for a, b in zip(sums[k], ctrl[k])]
    out = {k: {"real": tot_real[k], "of": tot_base[k], "control_mean": round(sum(sums[k]) / n, 2),
               "share_controls_at_or_above_real": round(sum(1 for x in sums[k] if x >= tot_real[k]) / n, 3)} for k in RULES}
    return {"charts": len(cases), "events": ev, "exact_dates": sum(1 for c in cases for e in c["events"] if e.get("exact")),
            "controls": n, "rules": out}


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
