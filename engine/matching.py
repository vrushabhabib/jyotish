"""
Kundli Milan — Ashtakoota (36 gunas) for marriage, plus a business-partnership synastry check.

ashtakoota(chart_a, chart_b) -> dict of 8 kootas with points and total.
business_synastry(chart_a, chart_b) -> structured findings (no score — Parashari has no canonical
business score; we surface the factors an astrologer weighs and let the interpreter conclude).
"""
from __future__ import annotations
import json, os
from .chart import build_chart, RASHI_LORD, NAK_LIST, RAS

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
NAK = json.load(open(os.path.join(DATA, "nakshatras.json")))
ENEMY_YONI = {frozenset(p) for p in NAK["yoni_enmity"]["enemies"]}
PLANETS = RAS["planets"]

VARNA_RANK = {"Brahmin": 4, "Kshatriya": 3, "Vaishya": 2, "Shudra": 1}
GANA_TABLE = {("Deva", "Deva"): 6, ("Manushya", "Manushya"): 6, ("Rakshasa", "Rakshasa"): 6,
              ("Deva", "Manushya"): 6, ("Manushya", "Deva"): 5,
              ("Deva", "Rakshasa"): 1, ("Rakshasa", "Deva"): 0,
              ("Manushya", "Rakshasa"): 0, ("Rakshasa", "Manushya"): 0}
VASHYA_GROUPS = ["Chatushpada", "Manava", "Jalachara", "Vanachara", "Keeta"]


def _nak(chart): return next(n for n in NAK_LIST if n["name"] == chart["janma_nakshatra"])
def _rashi(chart): return RAS["rashis"][chart["moon_rashi"] - 1]

def _vashya_of(chart):
    v = _rashi(chart)["vashya"]
    if "/" in v:  # Dhanu / Makara split at 15°
        first, second = [s.strip().split(" ")[0] for s in v.split("/")]
        return first if chart["planets"]["Moon"]["deg"] < 15 else second
    return v

def _relation(p1, p2):
    if p1 == p2: return "same"
    if p2 in PLANETS[p1]["friends"]: return "friend"
    if p2 in PLANETS[p1]["enemies"]: return "enemy"
    return "neutral"


def ashtakoota(boy, girl):
    nb, ng = _nak(boy), _nak(girl)
    rb, rg = _rashi(boy), _rashi(girl)
    out = {}

    # 1 Varna (1): girl's varna should be <= boy's
    out["varna"] = {"max": 1, "points": 1 if VARNA_RANK[rg["varna"]] <= VARNA_RANK[rb["varna"]] else 0,
                    "detail": f"boy {rb['varna']}, girl {rg['varna']}"}

    # 2 Vashya (2)
    vb, vg = _vashya_of(boy), _vashya_of(girl)
    if vb == vg: pts = 2
    elif {vb, vg} in ({"Chatushpada", "Manava"}, {"Jalachara", "Manava"}): pts = 1   # partial control
    elif {vb, vg} in ({"Chatushpada", "Vanachara"}, {"Manava", "Keeta"}): pts = 0.5   # hostile-ish
    elif {vb, vg} == {"Vanachara", "Manava"}: pts = 0
    else: pts = 1
    out["vashya"] = {"max": 2, "points": pts, "detail": f"boy {vb}, girl {vg}"}

    # 3 Tara (3): count from girl's nak to boy's and vice versa, mod 9; 3,5,7 are bad
    def tara(a, b):
        c = ((b["n"] - a["n"]) % 27) + 1
        t = c % 9 or 9
        return t not in (3, 5, 7)
    good = tara(ng, nb) + tara(nb, ng)
    out["tara"] = {"max": 3, "points": {2: 3, 1: 1.5, 0: 0}[good], "detail": f"{good}/2 counts auspicious"}

    # 4 Yoni (4)
    yb, yg = nb["yoni"], ng["yoni"]
    if yb == yg: pts = 4
    elif frozenset((yb, yg)) in ENEMY_YONI: pts = 0
    else: pts = 2   # standard tables have 1/2/3 gradations; 2 is the neutral default
    out["yoni"] = {"max": 4, "points": pts, "detail": f"boy {yb}({nb['yoni_gender']}), girl {yg}({ng['yoni_gender']})"}

    # 5 Graha Maitri (5): relationship between rashi lords
    lb, lg = rb["lord"], rg["lord"]
    r1, r2 = _relation(lb, lg), _relation(lg, lb)
    if lb == lg or (r1 == "friend" and r2 == "friend"): pts = 5
    elif {r1, r2} == {"friend", "neutral"}: pts = 4
    elif r1 == r2 == "neutral": pts = 3
    elif {r1, r2} == {"friend", "enemy"}: pts = 1
    elif {r1, r2} == {"neutral", "enemy"}: pts = 0.5
    else: pts = 0
    out["graha_maitri"] = {"max": 5, "points": pts, "detail": f"{lb}→{lg}: {r1}; {lg}→{lb}: {r2}"}

    # 6 Gana (6)
    out["gana"] = {"max": 6, "points": GANA_TABLE[(nb["gana"], ng["gana"])], "detail": f"boy {nb['gana']}, girl {ng['gana']}"}

    # 7 Bhakoot / Rashi (7): distance between moon signs; 2/12, 5/9, 6/8 are 0
    d1 = (rg["n"] - rb["n"]) % 12 + 1
    d2 = (rb["n"] - rg["n"]) % 12 + 1
    bad = {(2, 12), (12, 2), (5, 9), (9, 5), (6, 8), (8, 6)}
    pts = 0 if (d1, d2) in bad else 7
    # Bhakoot dosha cancellation: same rashi lord, or lords are friends
    cancelled = pts == 0 and (lb == lg or _relation(lb, lg) == "friend")
    out["bhakoot"] = {"max": 7, "points": 7 if cancelled else pts, "detail": f"{d1}/{d2}" + (" — dosha cancelled (lords friendly)" if cancelled else "")}

    # 8 Nadi (8): same nadi = 0 (Nadi dosha), else 8
    same = nb["nadi"] == ng["nadi"]
    # Cancellation: same rashi but different nakshatra, or same nakshatra but different rashi, etc.
    nadi_cancel = same and ((rb["n"] == rg["n"] and nb["n"] != ng["n"]) or (nb["n"] == ng["n"] and rb["n"] != rg["n"]))
    out["nadi"] = {"max": 8, "points": 8 if (not same or nadi_cancel) else 0,
                   "detail": f"boy {nb['nadi']}, girl {ng['nadi']}" + (" — same (Nadi dosha)" if same and not nadi_cancel else "") + (" — cancelled" if nadi_cancel else "")}

    total = sum(k["points"] for k in out.values())
    verdict = ("Excellent" if total >= 32 else "Very good" if total >= 25 else "Acceptable" if total >= 18 else "Not recommended without remedies")
    doshas = [k for k in ("bhakoot", "nadi", "gana") if out[k]["points"] == 0]
    return {"kootas": out, "total": total, "max": 36, "verdict": verdict, "zero_kootas": doshas}


def manglik_compat(a, b):
    """Manglik matching: both or neither is fine; one-sided is a flag unless cancelled."""
    ma, mb = a["manglik"]["lagna"]["is_manglik"], b["manglik"]["lagna"]["is_manglik"]
    return {"a": ma, "b": mb, "matched": ma == mb,
            "note": "Both/neither Manglik — compatible" if ma == mb else "One-sided Mangal dosha — check cancellations (Mars in own/exalted sign, Jupiter aspect, Mars in 1/4/7/8/12 from Lagna in Aries/Scorpio/Cancer/Capricorn etc.)"}


def _house_from(chart, ref_rashi, planet):
    return (chart["planets"][planet]["rashi"] - ref_rashi) % 12 + 1


def business_synastry(a, b):
    """Factors an astrologer weighs for business partnership. Each item: factor, finding, weight (+/-)."""
    F = []
    la, lb = a["lagna"]["rashi"], b["lagna"]["rashi"]
    # 1. Lagna-to-Lagna relation (7th / 11th / 3rd from each other is supportive; 6/8 is friction)
    d = (lb - la) % 12 + 1
    F.append({"factor": "Lagna to Lagna", "finding": f"B's lagna is {d}th from A's",
              "weight": +2 if d in (7, 11, 3, 5, 9) else -2 if d in (6, 8, 12) else 0})
    # 2. Lagna lord friendship
    rel = _relation(a["lagna"]["lord"], b["lagna"]["lord"])
    F.append({"factor": "Lagna lords", "finding": f"{a['lagna']['lord']} & {b['lagna']['lord']}: {rel}",
              "weight": {"same": 2, "friend": 2, "neutral": 0, "enemy": -2}[rel]})
    # 3. 7th house (partnership) and its lord, each chart
    for tag, c in (("A", a), ("B", b)):
        h7 = c["bhavas"][7]; l7 = h7["lord_in_bhava"]
        malef = [p for p in h7["occupants"] if p in ("Saturn", "Mars", "Rahu", "Ketu", "Sun")]
        F.append({"factor": f"{tag}: 7th house", "finding": f"lord {h7['lord']} in {l7}; occupants {h7['occupants'] or '—'}",
                  "weight": (-1 if l7 in (6, 8, 12) else +1) + (-1 if malef else 0)})
    # 4. Mutual 11th (gains) — B's planets falling in A's 11th and vice versa
    for tag, x, y in (("A gains from B", a, b), ("B gains from A", b, a)):
        hits = [p for p in ("Jupiter", "Venus", "Mercury", "Moon") if _house_from(y, x["lagna"]["rashi"], p) == 11]
        F.append({"factor": tag, "finding": f"partner benefics in 11th: {hits or '—'}", "weight": len(hits)})
    # 5. Saturn of one on Moon/Lagna of the other (friction / control)
    for tag, x, y in (("A's Saturn on B", a, b), ("B's Saturn on A", b, a)):
        sat = x["planets"]["Saturn"]["rashi"]
        hit = sat in (y["moon_rashi"], y["lagna"]["rashi"])
        F.append({"factor": tag, "finding": "Saturn conjoins partner's Moon/Lagna" if hit else "clear", "weight": -2 if hit else 0})
    # 6. Mercury (commerce) & Jupiter (wealth) dignity in each
    for tag, c in (("A", a), ("B", b)):
        for p in ("Mercury", "Jupiter"):
            dg = c["planets"][p]["dignity"]
            F.append({"factor": f"{tag}: {p}", "finding": dg,
                      "weight": 1 if dg.startswith(("Exalted", "Own", "Moolatrikona")) else -1 if dg.startswith("Debilitated") else 0})
    # 7. Dasha alignment: are both in growth-oriented dashas now?
    for tag, c in (("A", a), ("B", b)):
        md = c["dasha"]["current_maha"]
        lord = md["lord"] if md else "?"
        lord_house = c["planets"][lord]["bhava"] if md else None
        F.append({"factor": f"{tag}: current dasha", "finding": f"{lord} maha, dasha lord in house {lord_house}",
                  "weight": 1 if lord_house in (1, 2, 5, 9, 10, 11) else -1 if lord_house in (6, 8, 12) else 0})
    score = sum(f["weight"] for f in F)
    return {"factors": F, "net": score,
            "read": "Supportive" if score >= 4 else "Mixed — workable with clear roles" if score >= 0 else "Friction likely — define exit terms"}


if __name__ == "__main__":
    a = build_chart("1990-04-15", "06:30", 15.3647, 75.1240, "Asia/Kolkata", "Hubballi")
    b = build_chart("1992-11-02", "21:15", 21.0285, 105.8542, "Asia/Ho_Chi_Minh", "Hanoi")
    m = ashtakoota(a, b)
    for k, v in m["kootas"].items():
        print(f"{k:<13} {v['points']:>4}/{v['max']}  {v['detail']}")
    print(f"TOTAL {m['total']}/36 — {m['verdict']}; zero kootas: {m['zero_kootas']}")
    print(manglik_compat(a, b)["note"])
    print()
    bs = business_synastry(a, b)
    for f in bs["factors"]:
        print(f"{f['weight']:+d}  {f['factor']:<22} {f['finding']}")
    print("NET", bs["net"], "—", bs["read"])
