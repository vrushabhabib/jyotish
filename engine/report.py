"""One command that turns birth data (or an AstroSage PDF) into the complete reading worksheet.

    python -m engine.report 1996-11-24 12:05 15.3333 75.1333 Asia/Kolkata --name Tanzil --sex F
    python -m engine.report --pdf kundli.pdf            # birth data read from the PDF, then cross-checked
    options: --window 10   minutes either side of the birth time to scan for sign changes (default 15)
             --out DIR     write <name>_<date>.worksheet.md and .computed.json there

The worksheet is the fixed pre-computation the reading protocol asks for (kb/readings/full-reading-protocol.md):
nothing in it is interpretation. Every reading starts from it, so no factor is found by hand or missed.
"""
from __future__ import annotations
import argparse, datetime as dt, json, os, sys
from zoneinfo import ZoneInfo
from engine.chart import build_chart, RASHI_NAMES, RASHI_EN, RASHI_LORD, PLANET_ORDER, varga_rashi
from engine.analysis import analyse, View, hfrom, sign_at, dasha_tree, SEVEN
from engine.ashtakavarga import ashtakavarga, house_checks
from engine import transits as T

AREAS = {   # life area -> (houses, karakas male, karakas female)
    "self/health":   ((1, 6, 8), ["Sun"], ["Sun"]),
    "money":         ((2, 11), ["Jupiter"], ["Jupiter"]),
    "siblings":      ((3, 11), ["Mars"], ["Mars"]),
    "home/mother":   ((4,), ["Moon"], ["Moon"]),
    "children":      ((5,), ["Jupiter"], ["Jupiter"]),
    "marriage":      ((7,), ["Venus"], ["Jupiter", "Venus"]),
    "father/fortune": ((9,), ["Sun"], ["Sun"]),
    "career":        ((10, 6), ["Saturn", "Sun"], ["Saturn", "Sun"]),
    "foreign/loss":  ((12,), ["Rahu"], ["Rahu"]),
}
VARGA_USE = {2: "wealth", 3: "siblings", 4: "property", 7: "children", 9: "marriage / inner strength", 10: "career",
             12: "parents", 16: "vehicles/comfort", 20: "spiritual", 24: "education", 27: "strengths", 30: "misfortune/health",
             40: "maternal legacy", 45: "paternal legacy", 60: "past karma (needs exact time)"}


def _d(x):
    return x.strftime("%d %b %Y") if hasattr(x, "strftime") else str(x)


def time_sensitivity(date, time, lat, lon, tz, window=15):
    """Scan +/- window minutes: when do the lagna and the divisional lagnas change sign?"""
    base = dt.datetime.fromisoformat(f"{date}T{time}")
    rows = []; prev = None
    for m in range(-window, window + 1):
        t = base + dt.timedelta(minutes=m)
        c = build_chart(t.strftime("%Y-%m-%d"), t.strftime("%H:%M"), lat, lon, tz)
        L = c["lagna"]["lon"]
        key = tuple(varga_rashi(L, n) if n > 1 else c["lagna"]["rashi"] for n in (1, 9, 10, 7, 12, 3))
        if key != prev:
            rows.append((t.strftime("%H:%M"), key)); prev = key
    return rows


def build(date, time, lat, lon, tz, name="native", sex=None, window=15, years_ahead=25, place=""):
    chart = build_chart(date, time, lat, lon, tz, place)
    a = analyse(chart, sex)
    v: View = a["view"]
    av = ashtakavarga(chart)
    local = chart["input"]["local"]
    today = dt.datetime.now(local.tzinfo).date()
    birth = local.date()
    horizon = today + dt.timedelta(days=int(365.25 * years_ahead))
    moon = v.s["Moon"]
    out = {"chart": chart, "analysis": a, "ashtakavarga": av, "av_checks": house_checks(av),
           "time_sensitivity": time_sensitivity(date, time, lat, lon, tz, window),
           "saturn_phases": T.saturn_phases(moon, birth, horizon),
           "sade_sati": T.sade_sati_spans(moon, birth, horizon),
           "transits": {b: T.house_table(v, b, today - dt.timedelta(days=400), horizon) for b in ("Saturn", "Jupiter", "Rahu")},
           "double_transit": {h: T.double_transit(v, h, today - dt.timedelta(days=365 * 3), horizon) for h in (7, 5, 10, 4, 2)},
           "returns": T.returns(v, birth, horizon), "today": today}
    try:
        from engine.shadbala import shadbala as _sb          # optional module
        off = (local.utcoffset() or dt.timedelta(0)).total_seconds() / 3600
        out["shadbala"] = _sb(date, time, lat, lon, off)
    except Exception as e:                                    # noqa: BLE001 - report, never crash the worksheet
        out["shadbala"] = {"error": str(e)}
    return out


def markdown(r, name="native"):
    c, a, av = r["chart"], r["analysis"], r["ashtakavarga"]
    v: View = a["view"]; sex = a["sex"]
    P = c["planets"]; L = []; w = L.append
    inp = c["input"]
    w(f"# Worksheet - {name}\n")
    w(f"Born {inp['date']} {inp['time']} ({inp['tz']}), {inp['place'] or ''} {inp['lat']:.4f}N {inp['lon']:.4f}E. "
      f"Lahiri {inp['ayanamsa_lahiri']:.4f}, whole-sign houses, backend `{inp['backend']}`. Sex: {sex or 'not given'}. "
      f"Age {a['age']}. Computed {r['today']}.\n")
    pg = a["panchanga"]
    w(f"**Panchanga.** {pg['vara']} (lord {pg['vara_lord']}) - {pg['tithi']} (tithi {pg['tithi_no']}) - {pg['nakshatra']} pada {pg['pada']} - "
      f"yoga {pg['yoga']} - karana {pg['karana']} - sunrise {pg['sunrise']}, sunset {pg['sunset']} - {'day' if pg['day_birth'] else 'night'} birth.\n")
    w("## 1. Birth-time sensitivity\n")
    w("| From | D1 lagna | D9 | D10 | D7 | D12 | D3 |\n|---|---|---|---|---|---|---|")
    for t, k in r["time_sensitivity"]:
        w(f"| {t} | " + " | ".join(RASHI_NAMES[x - 1] for x in k) + " |")
    w("\nA row starts where any of these lagnas changes. Findings resting on a lagna that changes inside the stated time uncertainty must be marked uncertain.\n")
    w("## 2. Planets\n")
    w("| Graha | Sign | Deg | House | Nakshatra-pada | Star lord | Dignity | D9 (dignity) | Avastha | Flags |\n|---|---|---|---|---|---|---|---|---|---|")
    lag = c["lagna"]
    w(f"| Lagna | {lag['rashi_name']} | {lag['deg_dms']} | 1 | {lag['nakshatra']} | | | {RASHI_NAMES[lag['vargas']['D9'] - 1]} | | |")
    for p in PLANET_ORDER:
        d, s = P[p], a["states"][p]
        fl = [k for k, on in (("R", s["retrograde"]), ("combust", s["combust"]), ("vargottama", s["vargottama"]),
                              ("sandhi", s["sandhi"]), ("gandanta", s["gandanta"])) if on]
        w(f"| {p} | {d['rashi_name']} | {d['deg_dms']} | {d['bhava']} | {d['nakshatra']}-{d['pada']} | {d['nak_lord']} | {d['dignity']} | "
          f"{RASHI_NAMES[d['D9'] - 1]} ({s['d9_dignity'] or '-'}) | {s['baladi'] or '-'} | {', '.join(fl)} |")
    if a["graha_yuddha"]:
        w(f"\nGraha yuddha (within 1 deg): {a['graha_yuddha']}")
    w("\n## 3. Rulerships and functional nature\n")
    w("| Graha | Owns | Nature for this lagna | Notes |\n|---|---|---|---|")
    for p, f in a["functional"]["planets"].items():
        w(f"| {p} | {f['owns']} | {f['nature']} | {'; '.join(f['notes'] + (['maraka'] if f['maraka'] else []) + (['badhaka lord'] if f['badhaka'] else []))} |")
    w(f"\nBadhaka house: {a['functional']['badhaka_house']}.\n")
    for title, key in (("## 4. Houses from the lagna", "houses"), ("## 5. Houses from the Moon", "houses_from_moon")):
        w(title + "\n")
        w("| H | Sign | Lord -> house (dignity) | Occupants | Aspected by | Nodes aspect | Lord with | Lord aspected by | SAV |\n|---|---|---|---|---|---|---|---|---|")
        ref = v.lag if key == "houses" else v.s["Moon"]
        for h, x in a[key].items():
            sav = av["sav"][sign_at(ref, h) - 1]
            w(f"| {h} | {x['sign']} | {x['lord']} -> {x['lord_house']} ({x['lord_dignity']}) | {', '.join(x['occupants'])} | {', '.join(x['aspected_by'])} | "
              f"{', '.join(x['aspected_by_nodes'])} | {', '.join(x['lord_with'])} | {', '.join(x['lord_aspected_by'])} | {sav} |")
        w("")
    w("## 6. Divisional charts\n")
    ns = (2, 3, 4, 7, 9, 10, 12, 16, 20, 24, 27, 30, 60)
    w("| Varga (use) | Lagna | " + " | ".join(p[:3] for p in PLANET_ORDER) + " |\n|---|---|" + "---|" * 9)
    for n in ns:
        w(f"| D{n} ({VARGA_USE[n]}) | {RASHI_NAMES[lag['vargas'][f'D{n}'] - 1]} | " + " | ".join(RASHI_NAMES[P[p][f'D{n}'] - 1][:5] for p in PLANET_ORDER) + " |")
    w("\nD30 here is the Parashari trimsamsa sign. Divisional lagnas are only as good as the birth time (section 1).\n")
    w("## 7. Jaimini\n")
    ck = a["karakas"]
    w("Chara karakas (7-scheme): " + ", ".join(f"{k} {p}" for k, p in ck["seven"].items()) + ".  ")
    w("8-scheme with Rahu: " + ", ".join(f"{k} {p}" for k, p in ck["eight"].items()) + ".  ")
    w(f"Karakamsa: {a['karakamsa']['sign']} (house {a['karakamsa']['house_d1']} of D1).\n")
    ar = a["arudhas"]
    w("| Pada | Sign | House | Occupants |\n|---|---|---|---|")
    for k in ("AL", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11", "UL"):
        w(f"| {k} | {ar[k]['sign']} | {ar[k]['house']} | {', '.join(ar[k]['occupants'])} |")
    w(f"\n2nd from UL: {ar['UL_2nd']['sign']} (lord {ar['UL_2nd']['lord']}; occupants {ar['UL_2nd']['occupants']}; aspected by {ar['UL_2nd']['aspected_by']}). "
      f"8th from UL: {ar['UL_8th']['sign']} (occupants {ar['UL_8th']['occupants']}).\n")
    w("## 8. Yogas and afflictions detected\n")
    w("| Yoga | Type | Planets | Formation | Weakened by |\n|---|---|---|---|---|")
    for y in a["yogas"]:
        w(f"| {y['name']} | {y['category']} | {', '.join(y['planets'])} | {y['note']} | {y['weakened_by']} |")
    m = a["doshas"]["manglik"]; ks = a["doshas"]["kaal_sarp"]
    w(f"\n**Manglik:** {m['verdict']}. Mars is in house {m['from']['lagna']['mars_house']} from lagna, {m['from']['moon']['mars_house']} from Moon, "
      f"{m['from']['venus']['mars_house']} from Venus. Classical cancellations: {'; '.join(m['cancellations_classical']) or 'none'}. Also claimed: {'; '.join(m['cancellations_claimed']) or 'none'}. Base rate: {m['base_rate']}.  ")
    w(f"**Kaal Sarp:** {'full - ' + ks['type'] if ks['full'] else 'partial (one planet outside: ' + ', '.join(ks['planets_outside']) + ')' if ks['partial'] else 'no'}.  ")
    w(f"**Pitru indications:** {'; '.join(a['doshas']['pitru']) or 'none'}.\n")
    w("## 9. Strength\n")
    w("Sarvashtakavarga by house: " + ", ".join(f"H{h} {x}" for h, x in av["by_house"].items()) + ".  ")
    w("Checks: " + "; ".join(f"{t}: {'yes' if ok else 'NO'}" for t, ok in r["av_checks"]["checks"]) + ".  ")
    w(f"Strong houses (30+): {r['av_checks']['strong_houses']}; weak (25 or less): {r['av_checks']['weak_houses']}.\n")
    w("| BAV | " + " | ".join(n[:4] for n in RASHI_NAMES) + " |\n|---|" + "---|" * 12)
    for p, row in av["bav"].items():
        w(f"| {p} | " + " | ".join(str(x) for x in row) + " |")
    w(f"| **SAV** | " + " | ".join(str(x) for x in av["sav"]) + " |")
    sb = r.get("shadbala") or {}
    if "planets" in sb:
        w("\n| Shadbala | Rupas | Required | Ratio | Rank |\n|---|---|---|---|---|")
        for p, x in sorted(sb["planets"].items(), key=lambda kv: kv[1].get("rank", 9)):
            w(f"| {p} | {x.get('rupas', 0):.2f} | {x.get('required', 0)} | {x.get('ratio', 0):.2f} | {x.get('rank', '')} |")
        if sb.get("unverified"):
            w(f"\nShadbala components not yet verified against a reference: {sb['unverified']}.")
    else:
        w("\nShadbala: not computed here - take it from the kundli PDF if one is supplied.")
    pt = a["points"]
    w(f"\n**Special points.** Beeja sphuta {pt['beeja_sphuta']['sign']} ({pt['beeja_sphuta']['sign_parity']}) / navamsa {pt['beeja_sphuta']['navamsa']} ({pt['beeja_sphuta']['navamsa_parity']}); "
      f"Kshetra sphuta {pt['kshetra_sphuta']['sign']} ({pt['kshetra_sphuta']['sign_parity']}) / navamsa {pt['kshetra_sphuta']['navamsa']} ({pt['kshetra_sphuta']['navamsa_parity']}); "
      f"Indu lagna {pt['indu_lagna']['sign']} (house {pt['indu_lagna']['house']}); Bhrigu bindu {pt['bhrigu_bindu']['sign']} (house {pt['bhrigu_bindu']['house']}).\n")
    kp = a["kp"]
    w("**KP star / sub / sub-sub.** " + "; ".join(f"{k}: {'/'.join(x)}" for k, x in kp.items()) + ".\n")
    w("## 10. Link test - which planets can deliver which life area\n")
    w("A sub-period delivers an area only if its lord appears in that row (kb/dashas/antar-event-rules.md, Rule 1).\n")
    w("| Area | Houses | Karakas | " + " | ".join(p[:3] for p in PLANET_ORDER) + " |\n|---|---|---|" + "---|" * 9)
    links = {}
    for area, (hs, km, kf) in AREAS.items():
        ks_ = kf if sex == "F" else km
        row = []
        for p in PLANET_ORDER:
            l = v.sambandha(p, hs, ks_)
            links[(area, p)] = l
            strong = sum(1 for x in l if x.startswith(("occupies", "owns", "with", "is karaka")))
            row.append(f"{strong}+{len(l) - strong}" if l else "-")
        w(f"| {area} | {hs} | {', '.join(ks_)} | " + " | ".join(row) + " |")
    w("\nEach cell is strong+weak links. Strong = occupies the house, owns it, sits with its lord or a karaka, or is the karaka. Weak = aspects or disposes. Read an area into a sub-period only on a strong link, or on two weak ones backed by a transit; a planet that links to every row (common for Saturn, Mars and the nodes) discriminates nothing by itself - see Rule 8.\n")
    w("## 11. Vimshottari\n")
    now = a["dasha_now"]
    w("Now: " + " / ".join(f"{d['lord']} (to {_d(d['end'])})" for d in now) + ".\n")
    w("| Mahadasha | Antardasha | From | To | Age | Areas the antardasha lord is STRONGLY linked to |\n|---|---|---|---|---|---|")
    local = c["input"]["local"]
    for md, ms, me, ads in a["dasha_tree"]:
        if me <= local or (ms - local).days / 365.25 > 100: continue
        for ad, s, e, _ in ads:
            if e <= local: continue
            s2 = max(s, local)
            tags = [ar_ for ar_ in AREAS if any(x.startswith(("occupies", "owns", "with", "is karaka")) for x in links[(ar_, ad)])]
            w(f"| {md} | {ad} | {_d(s2)} | {_d(e)} | {(s2 - local).days / 365.25:.1f}-{(e - local).days / 365.25:.1f} | {', '.join(tags)} |")
    cur_md = next((x for x in a["dasha_tree"] if x[1] <= dt.datetime.now(local.tzinfo) < x[2]), None)
    if cur_md:
        w("\nPratyantardashas of the running and next two antardashas:\n")
        nowdt = dt.datetime.now(local.tzinfo); shown = 0
        for ad, s, e, pds in cur_md[3]:
            if e <= nowdt or shown >= 3: continue
            shown += 1
            w(f"- **{cur_md[0]}-{ad}** ({_d(s)} - {_d(e)}): " + "; ".join(f"{p} from {_d(ps)}" for p, ps, pe, _ in pds))
    w("\n## 12. Saturn phases from the Moon\n")
    w("Sade Sati cycles: " + "; ".join(f"{_d(x)} - {_d(y)}" for x, y in r["sade_sati"]) + ".\n")
    w("| Phase | Saturn in | From | To |\n|---|---|---|---|")
    for p in r["saturn_phases"]:
        w(f"| {p['phase']} | {p['sign']} | {_d(p['from'])} | {_d(p['to'])} |")
    w("\n## 13. Transits ahead\n")
    for b in ("Saturn", "Jupiter", "Rahu"):
        w(f"**{b}**\n\n| Sign | From | To | House | From Moon | SAV | Own BAV |\n|---|---|---|---|---|---|---|")
        for t in r["transits"][b][:40]:
            si = RASHI_NAMES.index(t["sign"])
            bav = av["bav"][b][si] if b in av["bav"] else "-"
            w(f"| {t['sign']} | {_d(t['from'])} | {_d(t['to'])} | {t['house']} | {t['house_from_moon']} | {av['sav'][si]} | {bav} |")
        w("")
    w("**Double transit of Jupiter and Saturn** (house or its lord; * = on the house itself)\n")
    for h, wins in r["double_transit"].items():
        w(f"- House {h}: " + ("; ".join(f"{_d(x['from'])} - {_d(x['to'])}{'*' if x['on_house_itself'] else ''}" for x in wins[:14]) or "none in range"))
    rt = r["returns"]
    w("\n**Returns (first entry to the natal sign).** " + "; ".join(f"{b}: {', '.join(_d(x) for x in ds[:4])}" for b, ds in rt.items()) + ".\n")
    return "\n".join(L)


def to_json(r):
    def clean(o):
        if isinstance(o, dict): return {str(k): clean(x) for k, x in o.items() if k not in ("view", "dasha_tree", "contributors")}
        if isinstance(o, (list, tuple)): return [clean(x) for x in o]
        if isinstance(o, (dt.datetime, dt.date)): return o.isoformat()
        if isinstance(o, float): return round(o, 4)
        return o if isinstance(o, (str, int, bool, type(None))) else str(o)
    return clean(r)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("birth", nargs="*", help="DATE TIME LAT LON TZ")
    ap.add_argument("--pdf"); ap.add_argument("--name", default="native"); ap.add_argument("--sex")
    ap.add_argument("--window", type=int, default=15); ap.add_argument("--out")
    o = ap.parse_args(argv)
    check = None
    if o.pdf:
        from engine.astrosage_pdf import parse, crosscheck
        pdf = parse(o.pdf); b = pdf["birth"]
        date, time, lat, lon = b["date"], b["time"][:5], b["lat"], b["lon"]
        tz = "Asia/Kolkata" if abs((b.get("tz_offset") or 5.5) - 5.5) < 0.01 else o.birth[0] if o.birth else "UTC"
        name = o.name if o.name != "native" else (b.get("name") or "native"); sex = o.sex or (b.get("sex") or "")[:1].upper() or None
        check = crosscheck(pdf)
    else:
        date, time, lat, lon, tz = o.birth[0], o.birth[1], float(o.birth[2]), float(o.birth[3]), o.birth[4]
        name, sex = o.name, o.sex
    r = build(date, time, float(lat), float(lon), tz, name, sex, o.window)
    md = markdown(r, name)
    if check:
        md += "\n## 14. Cross-check against the supplied PDF\n\n```\n" + json.dumps(check, indent=1, default=str)[:3000] + "\n```\n"
    if o.out:
        os.makedirs(o.out, exist_ok=True)
        stem = os.path.join(o.out, f"{name.lower().replace(' ', '-')}_{date}")
        open(stem + ".worksheet.md", "w").write(md)
        json.dump(to_json(r), open(stem + ".computed.json", "w"))
        print("wrote", stem + ".worksheet.md", "and .computed.json")
    else:
        print(md)


if __name__ == "__main__":
    main()
