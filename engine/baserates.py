"""How often does each yoga / dosha fire in charts chosen at random?

A combination present in most charts carries almost no information about one person. This module measures
the firing rate of everything engine.analysis detects over N random births (dates 1940-2010, any time of
day, Indian latitudes) and stores the result in data/base_rates.json. The worksheet prints the rate next to
each yoga so that common ones are discounted and rare ones stand out.

    python3 -m engine.baserates 4000        # regenerate
"""
from __future__ import annotations
import json, os, random, sys, datetime as dt
from collections import Counter

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "base_rates.json")


def run(n=4000, seed=7):
    from engine.chart import build_chart
    from engine.analysis import analyse
    rnd = random.Random(seed)
    c = Counter(); done = 0
    start = dt.date(1940, 1, 1).toordinal(); span = dt.date(2010, 12, 31).toordinal() - start
    for _ in range(n):
        d = dt.date.fromordinal(start + rnd.randrange(span))
        t = f"{rnd.randrange(24):02d}:{rnd.randrange(60):02d}"
        lat, lon = rnd.uniform(8, 32), rnd.uniform(70, 90)
        try:
            a = analyse(build_chart(d.isoformat(), t, lat, lon, "Asia/Kolkata"), sex="F")
        except Exception:
            continue
        done += 1
        for name in {y["name"] for y in a["yogas"]}:
            c["yoga:" + name] += 1
        from engine.yogas_extra import detect as _det
        for i in {x["id"] for x in _det(a["view"])}:
            c["cat:" + i] += 1
        m = a["doshas"]["manglik"]
        if m["from"]["lagna"]["dosha"]: c["dosha:Manglik from lagna (6-house list)"] += 1
        if m["from"]["lagna"]["bphs"]: c["dosha:Manglik from lagna (BPHS 1,4,7,8,12)"] += 1
        if m["from"]["lagna"]["dosha"] or m["from"]["moon"]["dosha"]: c["dosha:Manglik from lagna or Moon"] += 1
        if m["present"]: c["dosha:Manglik from lagna, Moon or Venus"] += 1
        if m["present"] and not m["cancellations_classical"]: c["dosha:Manglik with no classical cancellation"] += 1
        ks = a["doshas"]["kaal_sarp"]
        if ks["full"]: c["dosha:Kaal Sarp (full)"] += 1
        if ks["full"] or ks["partial"]: c["dosha:Kaal Sarp (full or partial)"] += 1
        if a["doshas"]["pitru"]: c["dosha:Pitru"] += 1
    rates = {k: round(v / done, 4) for k, v in sorted(c.items(), key=lambda kv: -kv[1])}
    out = {"charts": done, "seed": seed, "generated": dt.date.today().isoformat(),
           "note": "share of random charts (births 1940-2010, any hour, lat 8-32N) in which the item is detected by engine.analysis",
           "rates": rates}
    json.dump(out, open(PATH, "w"), indent=1)
    return out


_cache = None
def rate(kind, name):
    """Base rate (0..1) or None. kind = 'yoga' | 'dosha' | 'cat' (catalogue id from yogas_extra)."""
    global _cache
    if _cache is None:
        try: _cache = json.load(open(PATH))["rates"]
        except Exception: _cache = {}
    return _cache.get(f"{kind}:{name}")


def label(r):
    if r is None: return "n/a"
    return f"{r*100:.0f}% of charts - " + ("very common, weak evidence" if r >= 0.4 else "common" if r >= 0.2 else "uncommon" if r >= 0.05 else "rare, worth weight")


if __name__ == "__main__":
    o = run(int(sys.argv[1]) if len(sys.argv) > 1 else 4000)
    print(o["charts"], "charts")
    for k, v in o["rates"].items(): print(f"{v*100:5.1f}%  {k}")
