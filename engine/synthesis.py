"""Traditional synthesis mode (Rule 26, 21 Nov 2026).

Owner's complaint: the readings had become lists of hedged, separate points - no joined-up reading of the chart and no
real prediction. This module puts the three things a Jyotishi does back into the engine:

  1. dossier()      every life area judged from ALL its angles together - the house from the rising sign, its lord, its
                    significator, the same house from the Moon, the lord in the navamsa, the house's Ashtakavarga
                    points - with the factors for and against counted, so a verdict comes from the whole chart.
  2. connections()  the joined dots: for every planet, the areas it rules flow into the area it sits in and the areas it
                    looks at (the logic of BPHS ch. 24 - "lord of A in house B"), so one placement links several areas.
  3. timing()       EIGHT clocks vote each month for each area:
                       VMD, VAD, VPD  Vimshottari main / sub / third-level lord strongly linked to the area
                       YOG            Yogini sub-period lord strongly linked
                       CHA            Jaimini Chara sub-period sign on the area's house (or its 7th), or on / aspecting
                                      the area's chara karaka
                       KC             Kalachakra period or sub-period sign falls in the area's house (BPHS 46.131-154)
                       DT             Jupiter and Saturn both occupy or aspect the area's house or its lord's sign
                       MUN            Muntha of the yearly chart (rising sign + completed years) in the area's house
                                      (Tajika rule - NOT in the texts our KB has read; marked so)
                    A month counts as a WINDOW only when enough clocks agree that no more than about a third of all
                    months reach that level (the threshold rises until it is selective - kb Rule 8).
  4. calibrate()    the person's own dated past events are run through every clock; a clock that lit up during real
                    events more than it does on average gets more weight for this chart (capped 0.5-1.5).

Honest frame (said once per reading, not on every line): the scale tests of 17 Nov 2026 found the single timing rules
at chance. Convergence of several clocks is the traditional answer to that; whether it does better is decided only by
the ledger. Every dated window spoken from this module must be logged first (engine.ledger add)."""
from __future__ import annotations
import argparse, datetime as dt, json
from engine.chart import build_chart, RASHI_NAMES, RASHI_LORD, varga_rashi
from engine.analysis import analyse, dasha_at, sign_at, hfrom, house_table, View
from engine.ashtakavarga import ashtakavarga
from engine.report import AREAS
from engine.rectify import _strong
from engine import transits as T, dashas_extra as DX, dashas_classical as DC
from engine.hybrid import template

SYSTEMS = ("VMD", "VAD", "VPD", "YOG", "CHA", "KC", "DT", "MUN")
CK = {"self/health": "AK", "siblings": "BK", "home/mother": "MK", "children": "PK", "marriage": "DK",
      "father/fortune": "PiK", "career": "AmK"}
PLAIN = {"self/health": "yourself", "money": "money", "siblings": "brothers, sisters and own effort", "home/mother": "home, property and mother",
         "children": "children", "marriage": "marriage and partnership", "father/fortune": "father and luck", "career": "work and business",
         "foreign/loss": "abroad and expenses"}
HOUSE_PLAIN = {1: "yourself", 2: "savings and family", 3: "own effort and siblings", 4: "home, property and mother", 5: "children and intelligence",
               6: "debts, disputes and service", 7: "marriage and partners", 8: "obstacles and sudden change", 9: "father and luck",
               10: "work and standing", 11: "gains and friends", 12: "expenses and far-off places"}
MOV, FIX = {1, 4, 7, 10}, {2, 5, 8, 11}
NAT_BEN = ("Jupiter", "Venus", "Mercury", "Moon")
NAT_MAL = ("Sun", "Mars", "Saturn", "Rahu", "Ketu")
GOOD_DIG = ("exalt", "own", "moola", "friend")
BAD_DIG = ("debil", "enemy")


def jaimini_aspect(a, b):
    if a == b: return False
    if a in MOV: return b in FIX and (b - a) % 12 != 1
    if a in FIX: return b in MOV and (a - b) % 12 != 1
    return b not in MOV and b not in FIX


def _ord(n): return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


def _dig(c, p):
    d = (c["planets"][p].get("dignity") or "").lower()
    return 1 if any(w in d for w in GOOD_DIG) else -1 if any(w in d for w in BAD_DIG) else 0


# ------------------------------------------------------------------------------------------------ 1. the dossier
def dossier(c, a, av, shad, sex):
    """{area: {'for': [...], 'against': [...], 'net': int, 'verdict': str}} - every angle of the area counted together."""
    v: View = a["view"]; out = {}
    ranks = {p: d.get("rank") for p, d in (shad or {}).items()}
    hm = a["houses_from_moon"]; ck = a["karakas"]["seven_bphs"]
    for area, (hs, km, kf) in AREAS.items():
        fo, ag = [], []
        h = hs[0]; sg = sign_at(v.lag, h); L = v.lord(h); lh = v.house(L)
        pts = av["by_house"][h]
        (fo if pts >= 28 else ag if pts < 25 else []).append(f"house {h} has {pts} points ({'above' if pts >= 28 else 'below'} average)")
        (fo if lh in (1, 4, 7, 10, 5, 9, 11) else ag if lh in (6, 8, 12) else []).append(f"its ruler {L} sits in the house of {HOUSE_PLAIN[lh]}")
        dg = _dig(c, L)
        if dg: (fo if dg > 0 else ag).append(f"its ruler is in a {'friendly or own' if dg > 0 else 'hostile or low'} sign")
        if ranks.get(L): (fo if ranks[L] <= 3 else ag if ranks[L] >= 6 else []).append(f"its ruler ranks {ranks[L]} of 7 in strength")
        for p in v.occupants(sg):
            if p in NAT_BEN: fo.append(f"{p} sits in the house")
            elif p in NAT_MAL and p != L: ag.append(f"{p} sits in the house")
        for p in v.aspecting(sg, nodes=False):
            if p in v.occupants(sg) or p == L: continue
            (fo if p in NAT_BEN else ag).append(f"{p} looks at the house")
        d9 = c["planets"][L].get("D9")
        if d9:
            own9 = RASHI_LORD[d9 - 1] == L
            if own9: fo.append("its ruler is in its own sign in the navamsa")
            if c["planets"][L]["rashi"] == d9: fo.append("its ruler is vargottama (same sign in birth chart and navamsa)")
        mh = hm[h]
        (fo if mh["lord_house"] in (1, 4, 7, 10, 5, 9, 11) else ag if mh["lord_house"] in (6, 8, 12) else []).append(
            f"counted from the Moon, the ruler of this house sits in the {_ord(mh['lord_house'])}")
        if mh["benefic_hits"] > mh["malefic_hits"]: fo.append("from the Moon, kind planets touch this house more than harsh ones")
        elif mh["malefic_hits"] > mh["benefic_hits"]: ag.append("from the Moon, harsh planets touch this house more than kind ones")
        for k in (kf if sex == "F" else km):
            kh = v.house(k); kd = _dig(c, k)
            if kh in (6, 8, 12): ag.append(f"its significator {k} sits in the house of {HOUSE_PLAIN[kh]}")
            elif kh in (1, 4, 7, 10, 5, 9): fo.append(f"its significator {k} sits in the house of {HOUSE_PLAIN[kh]}")
            if kd: (fo if kd > 0 else ag).append(f"its significator {k} is in a {'friendly or own' if kd > 0 else 'hostile or low'} sign")
        bb = sign_at(sg, h)                                  # bhavat bhavam: the house as far from itself
        bl = RASHI_LORD[bb - 1]
        if v.house(bl) in (6, 8, 12): ag.append(f"house-from-house check: the {_ord(hfrom(bb, v.lag))} house's ruler sits in a hard house")
        net = len(fo) - len(ag)
        out[area] = {"for": fo, "against": ag, "net": net,
                     "verdict": "strong" if net >= 3 else "good" if net >= 1 else "mixed" if net >= -1 else "weak" if net >= -3 else "very weak"}
    return out


# ---------------------------------------------------------------------------------------------- 2. connections
def connections(c, a):
    """Plain sentences joining areas: what each planet's rulership feeds into."""
    v: View = a["view"]; out = []
    for p in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"):
        rules = sorted(v.owns(p)); sits = v.house(p)
        asp = sorted({hfrom(s, v.lag) for s in range(1, 13) if p in v.aspecting(s, nodes=False) and s != v.s[p]})
        with_ = [q for q in v.conj(p) if q != p]
        for h in rules:
            if h == sits:
                out.append({"planet": p, "text": f"{HOUSE_PLAIN[h].capitalize()} is held up by its own ruler, which sits at home.", "from": h, "to": sits})
            else:
                out.append({"planet": p, "text": f"{HOUSE_PLAIN[h].capitalize()} flows into {HOUSE_PLAIN[sits]}"
                            + (f", and touches {', '.join(HOUSE_PLAIN[x] for x in asp)}" if asp else "") + ".", "from": h, "to": sits})
        if len(rules) == 2 and rules[0] != sits and rules[1] != sits:
            out.append({"planet": p, "text": f"{HOUSE_PLAIN[rules[0]].capitalize()} and {HOUSE_PLAIN[rules[1]]} move together - one planet runs both.",
                        "from": rules[0], "to": rules[1]})
        for q in with_:
            if q in ("Rahu", "Ketu"): continue
            qr = v.owns(q)
            for h1 in rules:
                for h2 in qr:
                    if h1 < h2:
                        out.append({"planet": f"{p}+{q}", "text": f"{HOUSE_PLAIN[h1].capitalize()} and {HOUSE_PLAIN[h2]} are tied together (their rulers sit side by side).",
                                    "from": h1, "to": h2})
    seen, uniq = set(), []
    for x in out:
        if x["text"] not in seen: seen.add(x["text"]); uniq.append(x)
    return uniq


# -------------------------------------------------------------------------------------------------- 3. timing
def _at(periods, when, key="antar"):
    for m in periods:
        if m["start"] <= when < m["end"]:
            for x in m.get(key, []):
                if x["start"] <= when < x["end"]:
                    return m, x
            return m, None
    return None, None


def _months(start, end, step=30):
    d = start
    while d < end:
        yield d; d += dt.timedelta(days=step)


class Clocks:
    def __init__(self, date, time, lat, lon, tz, sex):
        self.c = c = build_chart(date, time, lat, lon, tz); self.a = a = analyse(c, sex=sex); self.v = v = a["view"]
        self.sex = sex; self.av = ashtakavarga(c); self.local = c["input"]["local"]; self.tz = self.local.tzinfo
        naive = self.local.replace(tzinfo=None)
        self.yog = DX.yogini(c["planets"]["Moon"]["lon"], naive, cycles=3)
        self.cha = DX.chara(c["lagna"]["rashi"], {p: d["rashi"] for p, d in c["planets"].items()}, naive, cycles=2)["maha"]
        self.kc = DC.kalachakra(c["planets"]["Moon"]["lon"], self.local)
        self.ck = a["karakas"]["seven_bphs"]
        self.link = {ar: {p: _strong(v, sex, p, ar) for p in v.s} for ar in AREAS}
        self._tr = {}

    def transit(self, d):
        if d not in self._tr: self._tr[d] = (T.sign_on("Jupiter", d), T.sign_on("Saturn", d))
        return self._tr[d]

    def votes(self, d):
        """{area: {system: bool}} and the month's Vimshottari path."""
        c, v = self.c, self.v; when = dt.datetime.combine(d, dt.time(12), tzinfo=self.tz); naive = when.replace(tzinfo=None)
        path = dasha_at(self.a["dasha_tree"], when)
        md, ad, pd = (path + [{"lord": None}] * 3)[:3]
        _, ya = _at(self.yog, naive); _, ca = _at(self.cha, naive)
        kp, ks = DC.kalachakra_at(self.kc, when)
        j, s = self.transit(d)
        age = int((d - self.local.date()).days // 365.25)
        mun = (c["lagna"]["rashi"] - 1 + age) % 12 + 1
        cs = RASHI_NAMES.index(ca["sign"]) + 1 if ca else None
        out = {}
        for ar, (hs, km, kf) in AREAS.items():
            hsigns = {sign_at(v.lag, h) for h in hs}
            L = self.link[ar]
            kar = self.ck.get(CK.get(ar, ""), None); ksign = v.s[kar] if kar else None
            lsigns = hsigns | {v.s[RASHI_LORD[x - 1]] for x in hsigns}
            out[ar] = {
                "VMD": bool(md["lord"] and L[md["lord"]]), "VAD": bool(ad["lord"] and L[ad["lord"]]), "VPD": bool(pd["lord"] and L[pd["lord"]]),
                "YOG": bool(ya and L[ya["lord"]]),
                "CHA": bool(cs and (cs in hsigns or any((cs - x) % 12 == 6 for x in hsigns) or (ksign and (cs == ksign or jaimini_aspect(cs, ksign))))),
                "KC": bool(kp and (kp["sign"] in hsigns or (ks and ks["sign"] in hsigns))),
                "DT": any(T._touches("Jupiter", j, t) for t in lsigns) and any(T._touches("Saturn", s, t) for t in lsigns),
                "MUN": mun in hsigns}
        return out, (md["lord"], ad["lord"], pd["lord"]), (j, s)

    def tone(self, path, js):
        """Tradition's direction for the month (Parashara template for the sub- and third-level lords + Jupiter/Saturn
        own-Ashtakavarga points in their transit signs). Labelled; our own tests put such calls at chance."""
        md, ad, pd = path; t = 0
        if ad: t += template(self.c, ad, md)[0]
        if pd: t += (template(self.c, pd, ad)[0] > 0) - (template(self.c, pd, ad)[0] < 0)
        j, s = js
        bj, bs = self.av["bav"]["Jupiter"][j - 1], self.av["bav"]["Saturn"][s - 1]
        t += (bj >= 5) - (bj <= 2) + (bs >= 4) - (bs <= 2)
        return t


def series(cl: Clocks, start, end, weights=None):
    w = weights or {}
    rows = []
    for d in _months(start, end):
        vs, path, js = cl.votes(d)
        rows.append({"date": d, "votes": vs, "path": path, "tone": cl.tone(path, js),
                     "score": {ar: round(sum(w.get(ar, {}).get(k, 1.0) * x for k, x in vv.items()), 2) for ar, vv in vs.items()}})
    return rows


def windows(rows, area, max_share=0.34, min_systems=4):
    """Lowest threshold at which no more than max_share of months qualify, and at least min_systems clocks agree."""
    sc = sorted({r["score"][area] for r in rows}, reverse=True)
    level = None
    for lv in sorted(sc):
        n = sum(1 for r in rows if r["score"][area] >= lv and sum(r["votes"][area].values()) >= min_systems)
        if n / len(rows) <= max_share:
            level = lv; break
    if level is None: return [], None, 0.0
    hit = [r for r in rows if r["score"][area] >= level and sum(r["votes"][area].values()) >= min_systems]
    share = len(hit) / len(rows)
    out, run = [], None
    for r in rows:
        ok = r["score"][area] >= level and sum(r["votes"][area].values()) >= min_systems
        if ok:
            if run is None: run = {"from": r["date"], "to": r["date"], "systems": set(), "peak": 0, "tone": [], "paths": set()}
            run["to"] = r["date"] + dt.timedelta(days=29); run["peak"] = max(run["peak"], sum(r["votes"][area].values()))
            run["systems"] |= {k for k, x in r["votes"][area].items() if x}; run["tone"].append(r["tone"]); run["paths"].add("-".join(x or "" for x in r["path"][:2]))
        elif run:
            out.append(run); run = None
    if run: out.append(run)
    for x in out:
        t = sum(x["tone"]) / len(x["tone"]); x["tone"] = "favourable" if t >= 1.5 else "difficult" if t <= -1.5 else "mixed"
        x["systems"] = sorted(x["systems"]); x["paths"] = sorted(x["paths"])
    return out, level, round(share, 3)


# ------------------------------------------------------------------------------------------------ 4. calibrate
def calibrate(cl: Clocks, events):
    """events: [{'area', 'from', 'to', 'label'}] (dates ISO). Per system: vote rate inside the person's real event spans
    vs the vote rate for the same area over adult life. Returns weights {area: {system: w}} and the table."""
    birth = cl.local.date(); life0 = birth + dt.timedelta(days=int(365.25 * 16)); today = dt.date.today()
    base_rows = series(cl, life0, today)
    base = {ar: {k: sum(r["votes"][ar][k] for r in base_rows) / len(base_rows) for k in SYSTEMS} for ar in AREAS}
    table, pooled = [], {k: [0, 0.0] for k in SYSTEMS}
    for e in events:
        f, t = dt.date.fromisoformat(e["from"]), dt.date.fromisoformat(e["to"])
        rs = [r for r in base_rows if f <= r["date"] <= t] or series(cl, f, t + dt.timedelta(days=1))
        row = {"label": e["label"], "area": e["area"], "months": len(rs), "rates": {}}
        for k in SYSTEMS:
            rate = sum(r["votes"][e["area"]][k] for r in rs) / len(rs)
            row["rates"][k] = (round(rate, 2), round(base[e["area"]][k], 2))
            pooled[k][0] += rate; pooled[k][1] += base[e["area"]][k]
        table.append(row)
    lift = {k: (round(pooled[k][0] / pooled[k][1], 2) if pooled[k][1] else None) for k in SYSTEMS}
    wt = {k: (max(0.5, min(1.5, 1 + (lift[k] - 1) / 2)) if lift[k] is not None else 1.0) for k in SYSTEMS}
    return {ar: dict(wt) for ar in AREAS}, {"events": table, "lift": lift, "weights": wt, "base_rows": base_rows}


def caught(rows_all, area, level, e, min_systems=4):
    f, t = dt.date.fromisoformat(e["from"]), dt.date.fromisoformat(e["to"])
    rs = [r for r in rows_all if f <= r["date"] <= t]
    return any(r["score"][area] >= level and sum(r["votes"][area].values()) >= min_systems for r in rs), len(rs)


# --------------------------------------------------------------------------------------------------- report
def run(date, time, lat, lon, tz, sex, events=None, years=12, start=None):
    cl = Clocks(date, time, lat, lon, tz, sex)
    from engine.shadbala import shadbala
    off = (cl.local.utcoffset() or dt.timedelta(0)).total_seconds() / 3600
    try: shad = shadbala(date, time, lat, lon, off)["planets"]
    except Exception: shad = {}                                    # noqa: BLE001
    start = start or dt.date.today(); end = start + dt.timedelta(days=int(365.25 * years))
    weights, cal = (calibrate(cl, events) if events else (None, None))
    fwd = series(cl, start, end, weights)
    out = {"dossier": dossier(cl.c, cl.a, cl.av, shad, sex), "connections": connections(cl.c, cl.a), "calibration": cal,
           "windows": {}, "start": start, "end": end, "birth": cl.local.date()}
    for ar in AREAS:
        ws, lv, sh = windows(fwd, ar)
        out["windows"][ar] = {"windows": ws, "level": lv, "share": sh}
    if cal:
        past = series(cl, cl.local.date() + dt.timedelta(days=int(365.25 * 16)), dt.date.today(), weights)
        chk = []
        for e in events:
            ws, lv, sh = windows(past, e["area"])
            ok, n = caught(past, e["area"], lv, e) if lv is not None else (False, 0)
            chance = 1 - (1 - sh) ** max(n, 1)
            chk.append({"label": e["label"], "caught": ok, "months": n, "share": sh, "chance": round(min(chance, 1.0), 2),
                        "informative": chance <= 0.5})
        cal["check"] = chk
    return out


def markdown(res):
    b = res["birth"]; age = lambda d: (d - b).days / 365.25
    L = ["# Synthesis sheet - traditional reading with convergence timing (Rule 26)\n",
         "> method: eight clocks vote each month; a window needs at least four agreeing and is selective (no more than about a third of months). "
         "Tone = Parashara's template + transit points (tradition's call; untested). Log every window before speaking it.\n",
         "## 1. Each area, judged from every angle\n", "| Area | Verdict | For | Against |", "|---|---|---|---|"]
    for ar, d in res["dossier"].items():
        L.append(f"| {PLAIN[ar]} | {d['verdict']} ({len(d['for'])} for, {len(d['against'])} against) | {'; '.join(d['for']) or '-'} | {'; '.join(d['against']) or '-'} |")
    L += ["\n## 2. How the areas are joined\n"] + [f"- {x['text']} *({x['planet']})*" for x in res["connections"]]
    cal = res["calibration"]
    if cal:
        L += ["\n## 3. Calibration on the person's own past\n", "| Event | Months | " + " | ".join(SYSTEMS) + " |", "|---|---|" + "---|" * len(SYSTEMS)]
        for e in cal["events"]:
            L.append(f"| {e['label']} ({PLAIN[e['area']]}) | {e['months']} | " + " | ".join(f"{a_:.2f} / {b_:.2f}" for a_, b_ in (e["rates"][k] for k in SYSTEMS)) + " |")
        L.append("| lift (event rate / normal rate) | | " + " | ".join(str(cal["lift"][k]) for k in SYSTEMS) + " |")
        L.append("| weight used | | " + " | ".join(f"{cal['weights'][k]:.2f}" for k in SYSTEMS) + " |")
        L.append("\nCells: share of months the clock voted for that area during the event / over adult life.\n")
        if cal.get("check"):
            L += ["| Event | Inside a window? | Chance of that by luck |", "|---|---|---|"]
            for x in cal["check"]:
                L.append(f"| {x['label']} | {'yes' if x['caught'] else 'no'} | {x['chance']:.0%}" + ("" if x["informative"] else " - span too wide to test anything") + " |")
            if not any(x["informative"] for x in cal["check"]):
                L.append("\nNone of these events is dated finely enough to test the clocks: a span of a year or more contains a window by luck. "
                         "Day- or month-dated events (wedding, company registration, passport stamps, offer letters) are needed; until then the weights are weak.")
    L += ["\n## 4. Forward windows (selective; each must be logged before it is spoken)\n",
          "| Area | From | To | Age | Clocks agreeing | Tone | Vimshottari | Months at this level |", "|---|---|---|---|---|---|---|---|"]
    for ar, d in res["windows"].items():
        for w in d["windows"]:
            L.append(f"| {PLAIN[ar]} | {w['from']:%b %Y} | {w['to']:%b %Y} | {age(w['from']):.1f}-{age(w['to']):.1f} | {w['peak']} of 8 ({', '.join(w['systems'])}) | {w['tone']} | {', '.join(w['paths'])} | {d['share']:.0%} |")
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("date"); ap.add_argument("time"); ap.add_argument("lat", type=float); ap.add_argument("lon", type=float); ap.add_argument("tz")
    ap.add_argument("--sex", default="M"); ap.add_argument("--events"); ap.add_argument("--years", type=int, default=12); ap.add_argument("--out")
    x = ap.parse_args(argv)
    ev = json.load(open(x.events)) if x.events else None
    md = markdown(run(x.date, x.time, x.lat, x.lon, x.tz, x.sex, ev, x.years))
    if x.out: open(x.out, "w").write(md)
    print(md)


if __name__ == "__main__":
    main()
