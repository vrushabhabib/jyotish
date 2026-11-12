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
    # cross-check systems: KP (Placidus), Bhava Chalit (Sripati), Yogini and Jaimini Chara dashas
    from engine import houses as H, dashas_extra as DX
    jd = chart["input"]["jd_ut"]
    naive = local.replace(tzinfo=None)
    out["kp"] = H.kp_chart(jd, lat, lon)
    bh = H.sripati(jd, lat, lon)
    out["chalit"] = {"bhavas": bh, "shifted": {p: (d["bhava"], H.chalit_house(d["lon"], bh)) for p, d in chart["planets"].items()
                                              if H.chalit_house(d["lon"], bh) != d["bhava"]}}
    out["yogini"] = DX.yogini(chart["planets"]["Moon"]["lon"], naive, cycles=3)
    out["chara"] = DX.chara(chart["lagna"]["rashi"], {p: d["rashi"] for p, d in chart["planets"].items()}, naive)
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
    w("'Parashara says' is his own verdict for this lagna (BPHS 34.19-44, read in Sanskrit); where it differs from the rule-based column, his verdict wins.\n")
    w("| Graha | Owns | Nature by the general rules | Parashara says | Notes |\n|---|---|---|---|---|")
    for p, f in a["functional"]["planets"].items():
        ps = (f.get("parashara") or "not named") + (", yoga-giver" if f.get("parashara_yoga_giver") else "") + (", death-inflicting" if f.get("parashara_maraka") else "")
        w(f"| {p} | {f['owns']} | {f['nature']} | {ps} | {'; '.join(f['notes'] + (['maraka'] if f['maraka'] else []) + (['badhaka lord'] if f['badhaka'] else []))} |")
    w(f"\nBadhaka house: {a['functional']['badhaka_house']}. {a['functional'].get('parashara_note', '')}\n")
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
    from engine.baserates import rate as _rate, label as _label
    w("The last column is how often the same combination appears in 4,000 random charts. Anything above 40% says almost nothing about one person.\n")
    w("| Yoga | Type | Planets | Formation | Weakened by | How common |\n|---|---|---|---|---|---|")
    for y in a["yogas"]:
        w(f"| {y['name']} | {y['category']} | {', '.join(y['planets'])} | {y['note']} | {y['weakened_by']} | {_label(_rate('yoga', y['name']))} |")
    try:
        from engine.yogas_extra import detect as _det, catalogue as _cat, coverage as _cov
        ex = _det(v); cat = _cat(); cv = _cov()
        w("\n### 8b. Further combinations from the 160-yoga catalogue (kb/yogas/yogas.json)\n")
        w("Sorted rarest first. 'n/a' in the last column means the combination did not occur once in 4,000 random charts.\n")
        w("| Yoga | Planets | Formed by | Classical result | Cancelled or weakened when | How common |\n|---|---|---|---|---|---|")
        for x in sorted(ex, key=lambda x: _rate("cat", x["id"]) or 0):
            e = cat.get(x["id"], {})
            if x["id"].startswith("nabhasa_sankhya") and any(y["id"].startswith("nabhasa_") and "sankhya" not in y["id"] for y in ex): continue
            w(f"| {e.get('name', x['id'])} | {', '.join(x['planets']) if len(x['planets']) < 7 else 'all seven'} | {x['note'] or e.get('condition', '')[:110]} | "
              f"{e.get('result', '')[:170]} | {e.get('cancellation', '')[:150]} | {_label(_rate('cat', x['id']))} |")
        w(f"\nCoverage: {len(cv['in_analysis']) + len(cv['in_yogas_extra'])} of {cv['catalogue']} catalogued combinations are tested by the engine; not tested: {', '.join(cv['not_coded'])}.\n")
    except Exception as e:                                    # noqa: BLE001
        w(f"\n(catalogue yogas failed: {e})\n")
    if a.get("sex") == "F":
        try:
            from engine.yogas_extra import husband_by_seventh as _hb
            hb = _hb(v)
            w(f"**Husband by the 7th house (BPHS 80.22-25, low confidence):** 7th sign ruled by {hb['seventh_sign_lord']} - {hb['by_sign']}; "
              f"7th navamsa ruled by {hb['navamsa_lord']} - {hb['by_navamsa']} (time-sensitive). The stronger of the two prevails.\n")
        except Exception:                                     # noqa: BLE001
            pass
    m = a["doshas"]["manglik"]; ks = a["doshas"]["kaal_sarp"]
    w(f"\n**Manglik:** {m['verdict']}. Mars is in house {m['from']['lagna']['mars_house']} from lagna, {m['from']['moon']['mars_house']} from Moon, "
      f"{m['from']['venus']['mars_house']} from Venus. Classical cancellations: {'; '.join(m['cancellations_classical']) or 'none'}. Also claimed: {'; '.join(m['cancellations_claimed']) or 'none'}. Base rate: {m['base_rate']}. {m['matching_note']}.  ")
    w(f"**Kaal Sarp:** {'full - ' + ks['type'] if ks['full'] else 'partial (one planet outside: ' + ', '.join(ks['planets_outside']) + ')' if ks['partial'] else 'no'}.  ")
    w(f"**Pitru dosha, popular definition (NOT Parashara's; found in about 61% of charts, so almost no weight):** {'; '.join(a['doshas']['pitru']) or 'none'}. "
      "Parashara's own father's-curse combinations (BPHS 83.20-27) are tested in section 8b under 'Pitru dosha'.\n")
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
            w("\nShadbala was checked against two references (an AstroSage printout and B.V. Raman's standard horoscope). Still unconfirmed: " + "; ".join(sb["unverified"]) + ".")
    else:
        w("\nShadbala: not computed here - take it from the kundli PDF if one is supplied.")
    from engine import rashmi as RSM
    rs = RSM.rashmi(c)
    w("\n**Rays (Parashara ch. 73).** " + "; ".join(f"{p} {x}" for p, x in rs["planets"].items()) + f". Total {rs['total']} - {rs['grade']}. "
      "A scale of means and following, read against the family's own standing (73.19-20); a planet moving toward its exaltation gives its rays more fully (73.21). "
      "By construction a random chart averages about 24, so only a total well above 30 or below 18 says anything.\n")
    age_now = (dt.datetime.now(c["input"]["local"].tzinfo) - c["input"]["local"]).days / 365.25
    sy = RSM.sudarshana_year(c, age_now)
    w(f"**Sudarshana year (Parashara 74.21-26).** Running year {int(age_now) + 1} is ruled by house {sy['house']}: " +
      "; ".join(f"from {k} {RASHI_NAMES[x['sign'] - 1]}" + (f" ({', '.join(x['occupants'])})" if x['occupants'] else " (empty)") for k, x in sy["by"].items()) +
      ". Benefics in its kendras, trines and 8th help; Rahu in it or many malefics harm; malefics in its 3rd, 6th, 11th help. " +
      ("Lagna, Moon and Sun are in three different signs, so the three-ring reading applies (74.19-20)." if sy["applies"] else "Two or more of lagna, Moon and Sun share a sign, so Parashara says to judge from the lagna alone (74.19-20).") + "\n")
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
    w("| Mahadasha | Antardasha | From | To | Age | Sub-lord from dasha lord | Areas the antardasha lord is STRONGLY linked to |\n|---|---|---|---|---|---|---|")
    P_ = c["planets"]
    def _rel(md, ad):
        if md == ad: return "same"
        n = (P_[ad]["rashi"] - P_[md]["rashi"]) % 12 + 1
        return f"house {n} - " + ("adverse" if n in (6, 8, 12) else "supportive" if n in (1, 3, 4, 5, 7, 9, 10, 11) else "mostly supportive")
    local = c["input"]["local"]
    for md, ms, me, ads in a["dasha_tree"]:
        if me <= local or (ms - local).days / 365.25 > 100: continue
        for ad, s, e, _ in ads:
            if e <= local: continue
            s2 = max(s, local)
            tags = [ar_ for ar_ in AREAS if any(x.startswith(("occupies", "owns", "with", "is karaka")) for x in links[(ar_, ad)])]
            w(f"| {md} | {ad} | {_d(s2)} | {_d(e)} | {(s2 - local).days / 365.25:.1f}-{(e - local).days / 365.25:.1f} | {_rel(md, ad)} | {', '.join(tags)} |")
    w("\nSub-lord from dasha lord (Parashara ch. 52-60, stated pair by pair for most of the 81 pairs): in a kendra, a trine, the 3rd or the 11th from the dasha lord the sub-period supports; in the 6th, 8th or 12th it obstructs; the 2nd is listed with the supportive places for most pairs. This is weighed together with the sub-lord's own house from the lagna and its dignity.\n")
    third = lambda p: ("start", "middle", "end")[min(2, int(P_[p]["deg"] // 10))]
    flip = {"start": "end", "middle": "middle", "end": "start"}
    w("When inside its own period a planet delivers (Parashara 47.3-4, by the third of the sign it is in; reversed when retrograde): " +
      "; ".join(f"{p} {flip[third(p)] if P_[p].get('retrograde') else third(p)}" for p in PLANET_ORDER) + ".\n")
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
    # ---- cross-check systems
    RN = ["Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya", "Tula", "Vrishchika", "Dhanu", "Makara", "Kumbha", "Meena"]
    def dm(x): return f"{RN[int(x // 30)]} {int(x % 30)}\u00b0{int((x % 30 % 1) * 60):02d}'"
    kp = r.get("kp")
    if kp:
        w("\n## 13a. KP system (Placidus cusps, KP ayanamsa) - a separate system, never mixed with whole-sign judgement\n")
        w("| Cusp | Longitude | Sign lord | Star | Sub | Sub-sub | Occupants | Significators (in star of occupants / occupants / in star of owner / owner) |\n|---|---|---|---|---|---|---|---|")
        for h, c in kp["cusps"].items():
            s = kp["house_significators"][h]
            w(f"| {h} | {dm(c['lon'])} | {c['sign_lord']} | {c['star']} | {c['sub']} | {c['subsub']} | {', '.join(s['B_occupants']) or '-'} | "
              f"{', '.join(s['A_in_star_of_occupants']) or '-'} / {', '.join(s['B_occupants']) or '-'} / {', '.join(s['C_in_star_of_owner']) or '-'} / {s['D_owner'][0]} |")
        w("\nHouses each planet signifies: " + "; ".join(f"{p} {v_}" for p, v_ in kp["planet_significations"].items()) + ".  ")
        subs = {h: kp["cusps"][h]["sub"] for h in (2, 5, 7, 10, 11)}
        w("Cuspal sub-lord tests (the sub-lord of the cusp must signify the houses named): "
          f"marriage - 7th sub-lord {subs[7]} signifies {kp['planet_significations'][subs[7]]} (needs 2, 7 or 11); "
          f"children - 5th sub-lord {subs[5]} signifies {kp['planet_significations'][subs[5]]} (needs 2, 5 or 11); "
          f"career - 10th sub-lord {subs[10]} signifies {kp['planet_significations'][subs[10]]} (needs 2, 6, 10 or 11); "
          f"gains - 11th sub-lord {subs[11]} signifies {kp['planet_significations'][subs[11]]}.\n")
    chl = r.get("chalit")
    if chl:
        sh = chl["shifted"]
        w("**Bhava Chalit (Sripati).** " + ("Planets that fall in a different house than by whole sign: " +
          "; ".join(f"{p} {a_}->{b_}" for p, (a_, b_) in sh.items()) + ". Treat their house results as shared between the two houses." if sh
          else "No planet changes house.") + "\n")
    yg, ch = r.get("yogini"), r.get("chara")
    if yg and ch:
        now = dt.datetime.combine(r["today"], dt.time())
        w("## 13b. Second and third dasha systems (cross-check for Vimshottari)\n")
        w("An event window is trusted more when Vimshottari, Yogini and Chara all point to the same area in the same years.\n")
        w("| Yogini | Lord | From | To | Sub-periods now |\n|---|---|---|---|---|")
        for y in yg:
            if y["end"] < now - dt.timedelta(days=365 * 3) or y["start"] > now + dt.timedelta(days=365 * 15): continue
            cur = "; ".join(f"{a_['yogini']} to {_d(a_['end'])}" for a_ in y["antar"] if y["start"] <= now < y["end"] and a_["end"] > now)
            w(f"| {y['yogini']} | {y['lord']} | {_d(y['start'])} | {_d(y['end'])} | {cur} |")
        w("\n| Chara dasha sign | Years | From | To | Sub-periods now |\n|---|---|---|---|---|")
        for m in ch["maha"]:
            cur = "; ".join(f"{a_['sign']} to {_d(a_['end'])}" for a_ in m["antar"] if m["start"] <= now < m["end"] and a_["end"] > now)
            w(f"| {m['sign']} | {m['years']} | {_d(m['start'])} | {_d(m['end'])} | {cur} |")
        w(f"\nMethod: {ch['method']}. " + (" ".join(ch["notes"]) if ch["notes"] else "") + "\n")
    try:
        from engine.convergence import timeline as _tl
        from engine import ledger as _lg
        tl = _tl(r, sex=a.get("sex"))
        w("## 13c. Convergence - months where independent timing systems agree\n")
        w("Five votes per area: Vimshottari main lord, Vimshottari sub-lord, Yogini sub-lord, Chara sub-sign, Jupiter-Saturn double transit. "
          "A window needs 4 of 5. 'Share' is the part of the next 15 years that reaches the same level: above about a third, the test does not discriminate for this chart and the window carries little weight. "
          "EXPERIMENTAL: in the back-test of 12 Nov 2026 (data/convergence_backtest.json) only 2 of 8 known past events fell in a 4-of-5 month. Use these windows as one input, state them as tentative, and log each one in the ledger.\n")
        w("| Area | Window | Votes | Systems agreeing | Vimshottari | Share of all months | Verdict |\n|---|---|---|---|---|---|---|")
        for area, x in tl.items():
            verdict = "usable" if x["discriminates"] and x["level"] >= x["need"] else "weak: best level only " + str(x["level"]) + " of 5" if x["level"] < x["need"] else "does not discriminate"
            if not x["windows"]:
                w(f"| {area} | none | - | - | - | {x['share']*100:.0f}% | {verdict} |")
            for k in x["windows"][:8]:
                w(f"| {area} | {_d(k['from'])} - {_d(k['to'])} | {k['peak']} | {', '.join(k['systems'])} | {', '.join(k['vimshottari'])} | {x['share']*100:.0f}% | {verdict} |")
        st = _lg.stats()
        if st["scored"]:
            w(f"\n**Project track record (data/ledger.jsonl).** {st['scored']} verification questions scored: {st['overall_strict']*100:.0f}% fully right, "
              f"{st['overall']*100:.0f}% counting a partly-right answer as half. By chart: " +
              ", ".join(f"{k} {x['strict']*100:.0f}% (n={x['n']})" for k, x in st["by_chart"].items()) + ". By kind of statement: " +
              "; ".join(f"{k} {x['strict']*100:.0f}% (n={x['n']})" for k, x in st["by_category"].items()) +
              f". Every scored item is about the past, asked cold; {st['open']} forward prediction(s) open, none matured yet. "
              "Log every dated forward statement with `python3 -m engine.ledger add` before a reading is sent.\n")
    except Exception as e:                                    # noqa: BLE001
        w(f"\n(convergence section failed: {e})\n")
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
    ap.add_argument("birth", nargs="*", help="DATE TIME LAT LON TZ   or   DATE TIME PLACE")
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
    elif len(o.birth) == 3:                                   # DATE TIME "Place name" - offline lookup
        from engine.places import resolve
        pl = resolve(o.birth[2])
        if not pl:
            raise SystemExit(f"Place '{o.birth[2]}' is not in the offline list (towns above 15,000 people). Give LAT LON TZ, or the nearest town.")
        date, time, lat, lon, tz = o.birth[0], o.birth[1], pl["lat"], pl["lon"], pl["tz"]
        name, sex = o.name, o.sex
        print(f"place: {pl['name']}, {pl['country']} {lat} {lon} {tz}" + (f"  (other matches: {pl['ambiguous']})" if pl["ambiguous"] else ""))
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
