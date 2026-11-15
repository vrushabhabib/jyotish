"""Hybrid reading sheet (Rule 24, 15 Nov 2026): every period at three levels with a SUBJECT, the TRADITION'S VERDICT
and a HOLD line, in plain words and with the person's age - ready to be read aloud.

    python3 -m engine.hybrid DATE TIME LAT LON TZ --sex F --from YYYY-MM-DD --to YYYY-MM-DD [--fine-from D --fine-to D]

Owner's instruction: a reading without a prediction has no point. So the sheet predicts - and labels each line by what
stands behind it, so that the ledger can score it later:
  SUBJECT   areas of life the running planet is strongly linked to (link test; faint edge in our tests)
  VERDICT   favourable / mixed / difficult by Parashara's sub-period template (BPHS ch. 52-60): the planet's house from
            the rising sign, its dignity, its house from the longer period's planet - one point each. Tradition's call;
            in our own tests such calls have so far scored at chance. Third level: the same template counted from the
            sub-period planet (our extension - BPHS 61 goes by the planet's natural character only).
  HOLD      Rule 24 (pre-stated, untested): what is BEGUN in an area while the running sub-period planet is linked to
            that area tends to hold; what is begun in an area it is not linked to tends not to hold, and endings in
            that area fall in such periods.
Nothing here states length of life, death, illness, or the number or sex of children."""
from __future__ import annotations
import argparse, datetime as dt
from engine.chart import build_chart
from engine.analysis import analyse, period_cautions
from engine.report import AREAS
from engine.rectify import linked_areas

PLAIN = {"self/health": "herself and her health", "money": "money", "siblings": "brothers and sisters", "home/mother": "home and mother",
         "children": "children", "marriage": "relationship and marriage", "father/fortune": "father and luck", "career": "work",
         "foreign/loss": "foreign places and expenses"}
WORD = {1: "favourable", 0: "mixed", -1: "difficult"}


def template(c, lord, upper):
    """Parashara's three points for `lord` under the longer period's planet `upper`. Returns (score, reasons)."""
    P = c["planets"][lord]; h = P["bhava"]; dg = (P.get("dignity") or "").lower(); t = 0; why = []
    a = 1 if h in (1, 4, 7, 10, 5, 9, 11) else -1 if h in (6, 8, 12) else 0
    t += a; why.append(f"house {h} " + ("(+)" if a > 0 else "(-)" if a < 0 else "(0)"))
    b = 1 if any(w in dg for w in ("exalt", "own", "moola", "friend")) else -1 if (any(w in dg for w in ("debil", "enemy")) or P.get("combust")) else 0
    t += b; why.append(("combust" if P.get("combust") else dg or "neutral") + (" (+)" if b > 0 else " (-)" if b < 0 else " (0)"))
    if upper != lord:
        n = (P["rashi"] - c["planets"][upper]["rashi"]) % 12 + 1
        d = -1 if n in (6, 8, 12) else 1
        t += d; why.append(f"{n} from {upper} " + ("(+)" if d > 0 else "(-)"))
    return t, why


def rows(date, time, lat, lon, tz, sex, start, end, fine_start=None, fine_end=None):
    c = build_chart(date, time, lat, lon, tz); a = analyse(c, sex=sex); v = a["view"]; caut = period_cautions(v)
    local = c["input"]["local"]; out = []
    age = lambda d: (d - local.date()).days / 365.25
    for md, ms, me, ads in a["dasha_tree"]:
        for ad, s, e, pds in ads:
            if e.date() <= start or s.date() >= end or e <= local: continue
            t, why = template(c, ad, md); la = linked_areas(v, sex, ad)
            r = {"level": 2, "md": md, "ad": ad, "from": max(s, local).date(), "to": e.date(), "age": (age(max(s, local).date()), age(e.date())),
                 "subject": la, "score": t, "verdict": WORD[(t > 0) - (t < 0)], "why": why, "caution": caut.get(ad) or [],
                 "holds": la, "not_hold": [x for x in AREAS if x not in la], "fine": []}
            for pd, ps, pe, _ in pds:
                if fine_start and fine_end and pe.date() > fine_start and ps.date() < fine_end:
                    t3, why3 = template(c, pd, ad)
                    r["fine"].append({"pd": pd, "from": ps.date(), "to": pe.date(), "age": age(ps.date()), "subject": linked_areas(v, sex, pd),
                                      "score": t3, "verdict": WORD[(t3 > 0) - (t3 < 0)], "why": why3})
            out.append(r)
    return out


def _pl(xs): return ", ".join(PLAIN[x] for x in xs) or "no area in particular"


def markdown(rs):
    o = []
    for r in rs:
        o.append(f"### {r['from']:%b %Y} to {r['to']:%b %Y} - age {r['age'][0]:.1f} to {r['age'][1]:.1f}  ({r['md']} long period, {r['ad']} sub-period)")
        o.append(f"- **Subject:** {_pl(r['subject'])}.")
        o.append(f"- **Tradition's verdict:** {r['verdict']} ({'; '.join(r['why'])})." + (f" Caution: {'; '.join(r['caution'])}." if r["caution"] else ""))
        o.append(f"- **Hold line:** what begins now in {_pl(r['holds'])} tends to hold; what begins in {_pl([x for x in r['not_hold'] if x in ('marriage', 'career', 'home/mother', 'money', 'foreign/loss')])} tends not to.")
        if r["fine"]:
            o.append("- **Shorter stretches inside it:**")
            for f in r["fine"]:
                o.append(f"  - {f['from']:%d %b %Y} to {f['to']:%d %b %Y} (age {f['age']:.1f}), {f['pd']}: {_pl(f['subject'])} - {f['verdict']}")
        o.append("")
    return "\n".join(o)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("date"); ap.add_argument("time"); ap.add_argument("lat", type=float); ap.add_argument("lon", type=float); ap.add_argument("tz")
    ap.add_argument("--sex", default=None); ap.add_argument("--from", dest="start", required=True); ap.add_argument("--to", dest="end", required=True)
    ap.add_argument("--fine-from"); ap.add_argument("--fine-to")
    x = ap.parse_args(argv); D = dt.date.fromisoformat
    print(markdown(rows(x.date, x.time, x.lat, x.lon, x.tz, x.sex, D(x.start), D(x.end), D(x.fine_from) if x.fine_from else None, D(x.fine_to) if x.fine_to else None)))


if __name__ == "__main__":
    main()
