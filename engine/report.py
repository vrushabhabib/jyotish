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
from engine.analysis import analyse, View, hfrom, sign_at, dasha_tree, SEVEN, period_cautions
from engine.ashtakavarga import ashtakavarga, house_checks
from engine import transits as T

MOVABLE = {"self/health": "AK", "career": "AmK", "siblings": "BK", "home/mother": "MK", "father/fortune": "PiK",
           "children": "PK", "marriage": "DK"}   # life area -> movable significator, Parashara's list (seven_bphs)
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


from engine import findings as F


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
           "time_sensitivity": time_sensitivity(date, time, lat, lon, tz, window), "window": window,
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
    try:                                       # the two other classical clocks (engine/dashas_classical.py)
        from engine import dashas_classical as DC
        out["kalachakra"] = DC.kalachakra(chart["planets"]["Moon"]["lon"], local)
        st_ = {q: d_["rupas"] for q, d_ in (out["shadbala"].get("planets") or {}).items()}
        out["lifespan_dasha"] = DC.lifespan_dasha(chart, st_) if st_ else None
    except Exception as e:                                    # noqa: BLE001
        out["kalachakra"] = None; out["lifespan_dasha"] = None; out["classical_dasha_error"] = str(e)
    out["findings"] = F.build(out)            # the register a reading is checked against (engine/findings.py)
    out["pending"] = F.pending()
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
        w("\n### 8b. Further combinations from the yoga catalogue (kb/yogas/yogas.json)\n")
        w("Sorted rarest first. 'n/a' in the last column means the combination did not occur once in 4,000 random charts.\n")
        w("| Yoga | Planets | Formed by | Classical result | Cancelled or weakened when | How common |\n|---|---|---|---|---|---|")
        for x in sorted(ex, key=lambda x: _rate("cat", x["id"]) or 0):
            e = cat.get(x["id"], {})
            if x["id"].startswith("nabhasa_sankhya") and any(y["id"].startswith("nabhasa_") and "sankhya" not in y["id"] for y in ex): continue
            w(f"| {e.get('name', x['id'])} | {', '.join(x['planets']) if len(x['planets']) < 7 else 'all seven'} | {x['note'] or e.get('condition', '')[:110]} | "
              f"{e.get('result', '')[:170]} | {e.get('cancellation', '')[:150]} | {_label(_rate('cat', x['id']))} |")
        w(f"\nCoverage: {len(cv['in_analysis']) + len(cv['in_yogas_extra'])} of {cv['catalogue']} catalogued " + "combinations are tested by the engine" + (f"; not tested: {', '.join(cv['not_coded'])}" if cv['not_coded'] else "") + ".\n")
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
        w("\n| Shadbala | Rupas | Required (texts) | Ratio | Rank | As printed by AstroSage / Raman: required, ratio, rank |\n|---|---|---|---|---|---|")
        for p, x in sorted(sb["planets"].items(), key=lambda kv: kv[1].get("rank_text", kv[1].get("rank", 9))):
            w(f"| {p} | {x.get('rupas', 0):.2f} | {x.get('required_text', x.get('required', 0))} | {x.get('ratio_text', x.get('ratio', 0)):.2f} | {x.get('rank_text', x.get('rank', ''))} | "
              f"{x.get('required', 0)}, {x.get('ratio', 0):.2f}, {x.get('rank', '')} |")
        w("\nThe Sun's required strength is 6.5 rupas in the texts (Parashara 27.32-33; Jataka Parijata 2.40) and 5 in Raman's book and AstroSage; the other six agree. "
          "Quote the first three columns in a reading; the last column exists only to cross-check a supplied kundli.")
        try:
            from engine.shadbala import shadbala as _sbf
            i_ = c["input"]; off_ = (i_["local"].utcoffset().total_seconds() / 3600.0) if i_["local"].utcoffset() else 0.0
            sbp = _sbf(i_["date"], i_["time"], i_["lat"], i_["lon"], off_, compat="parashara")
            w("With Parashara's own dignity scale (27.2-3: 20/15/10/4/2 in place of Raman's 22.5/15/7.5/3.75/1.875): " +
              "; ".join(f"{p} {sbp['planets'][p]['rupas']:.2f}" for p in sorted(sbp["planets"], key=lambda q: sbp["planets"][q]["rank_text"])) +
              ". A rank that changes between the two scales is not firm.")
        except Exception as _e:                              # noqa: BLE001
            w(f"(Parashara-scale Shadbala not computed: {_e})")
        if sb.get("unverified"):
            try:                                                      # Parashara's good and bad share of each planet (ch. 28)
                from engine.control import ishta_kashta as _ik
                _b = c["input"]; _v = _ik({"date": _b["date"], "time": _b["time"], "lat": _b["lat"], "lon": _b["lon"], "tz": _b["tz"]})
                w("**Good and bad share of each planet (Parashara ch. 28 v.2-6: ishta = root of exaltation strength x motional strength; kashta = root of the product of their complements; out of 60).** " + "; ".join(f"{p_} {a_:.0f} good / {b_:.0f} bad" for p_, (a_, b_) in _v.items()) + ". Parashara uses these to grade how much good or bad a planet's period carries. Tested 13 Nov 2026 on 25 dated good/bad events from five charts as a direction rule (good when ishta exceeds kashta): 11 right, wrong charts average 11.0 - at chance. Shown for completeness; not a basis for saying a period goes well or badly (antar-event-rules.md, Rule 17).\n")
            except Exception as _e:                                  # noqa: BLE001
                w(f"(Good and bad share not computed: {_e})\n")
            w("\nShadbala was checked against two references (an AstroSage printout and B.V. Raman's standard horoscope). Still unconfirmed: " + "; ".join(sb["unverified"]) + ".")
    else:
        w("\nShadbala: not computed here - take it from the kundli PDF if one is supplied.")
    from engine import rashmi as RSM
    rs = RSM.rashmi(c)
    w("\n**Rays (Parashara ch. 73).** " + "; ".join(f"{p} {x}" for p, x in rs["planets"].items()) + f". Total {rs['total']} - {rs['grade']}. "
      "A scale of means and following, read against the family's own standing (73.19-20); a planet moving toward its exaltation gives its rays more fully (73.21). "
      "Measured over 1,500 random charts the total averages 22; one chart in nine is above 30 and one in twenty below 12 - only those tails say anything.\n")
    age_now = (dt.datetime.now(c["input"]["local"].tzinfo) - c["input"]["local"]).days / 365.25
    sy = RSM.sudarshana_year(c, age_now)
    w(f"**Sudarshana year (Parashara 74.21-26).** Running year {int(age_now) + 1} is ruled by house {sy['house']}: " +
      "; ".join(f"from {k} {RASHI_NAMES[x['sign'] - 1]}" + (f" ({', '.join(x['occupants'])})" if x['occupants'] else " (empty)") for k, x in sy["by"].items()) +
      ". Benefics in its kendras, trines and 8th help; Rahu in it or many malefics harm; malefics in its 3rd, 6th, 11th help. " +
      ("Lagna, Moon and Sun are in three different signs, so the three-ring reading applies (74.19-20)." if sy["applies"] else "Two or more of lagna, Moon and Sun share a sign, so Parashara says to judge from the lagna alone (74.19-20).") + "\n")
    def _liv(ref_sign):
        tl = RASHI_LORD[(ref_sign - 1 + 9) % 12]
        d_ = c["planets"][tl]; nl = RASHI_LORD[varga_rashi((d_["rashi"] - 1) * 30 + d_["deg"], 9) - 1]
        return f"10th lord {tl}, in a navamsa of {nl}"
    w("**Livelihood pointer (Parashara's and Phaladeepika 5.1 method: the lord of the navamsa occupied by the 10th lord, taken from the strongest of lagna, Moon and Sun).** "
      f"From lagna: {_liv(c['lagna']['rashi'])}. From Moon: {_liv(c['planets']['Moon']['rashi'])}. From Sun: {_liv(c['planets']['Sun']['rashi'])}. "
      "Kinds of work by that navamsa lord are listed in kb/sources/phaladeepika/ch05-07.md (5.2-8); where the three agree the pointer is firm.\n")
    from engine import classical as KL2, ephemeris as EPH, ashtakavarga as AVM
    vp = KL2.vimshopaka(c)
    w("**Twenty-point strength over the sixteen divisions (Parashara 7.17-27).** " + "; ".join(f"{p} {x['points']} ({x['grade']})" for p, x in vp.items()) +
      ". Below 5 a planet's period gives nothing of its own, 5-10 little, 10-15 middling, above 15 in full (7.26-27); the text grades dasha results by this. Over 800 random charts 68% of planets are middling, 20% full and 12% small - so only the full and small grades say anything.\n")
    sl = KL2.special_lagnas(c)
    w("**Special lagnas (Parashara 5.2-8).** " + "; ".join(f"{k.replace('_', ' ')} {sl[k]['sign_name']} (house {sl[k]['house']})" for k in ("bhava_lagna", "hora_lagna", "ghati_lagna")) +
      f". Born {sl['hours_from_sunrise']} hours after sunrise. Hora and ghati lagna move a sign in 60 and 24 minutes, so they are usable only with a recorded birth time.\n")
    try:
        avx = AVM.ashtakavarga(c)
        blk = KL2.sav_blocks(avx, c["lagna"]["rashi"]); gm = KL2.good_months(avx)
        w(f"**Combined Ashtakavarga in three parts of life (Parashara 72.9-10).** Houses 1-4: {blk['early']}; 5-8: {blk['middle']}; 9-12: {blk['late']} - the {blk['strongest']} part carries the most points (the three always add to 337; a difference under about ten points is ordinary). "
          f"**Solar months by the Sun's own table (70.19-20):** prefer the Sun in {', '.join(gm['prefer'])} ({gm['prefer_points']} points); avoid new beginnings with the Sun in {', '.join(gm['avoid'])} ({gm['avoid_points']}).\n")
    except Exception as _e:
        w(f"(Ashtakavarga blocks not computed: {_e})\n")
    sd = KL2.spouse_direction(c)
    w(f"**Direction the spouse comes from.** Parashara (7th from Venus, 70.35-36): {sd['parashara']}. Mantreshvara (signs of the 7th lord, Venus and any planet in the 7th, PD 10.12): {', '.join(sd['mantreshvara'])}. " +
      (f"Both name the {sd['both']} (the two texts agree in about 28% of charts)." if sd["both"] else "The two texts do not agree here, so no direction is stated.") + "\n")
    bc = KL2.birth_conditions(c)
    rise_, set_ = EPH.sun_times(c["input"]["jd_ut"], c["input"]["lat"], c["input"]["lon"])
    day_ = rise_ <= c["input"]["jd_ut"] < set_
    w(f"**Birth-time conditions (Parashara ch. 85-92).** Lunar day {bc['tithi']} of 30 ({bc['half']} half), {'day' if day_ else 'night'} birth. " +
      ("A birth for which Parashara prescribes a rite: " + "; ".join(bc["conditions"]) + ". Named only so the family's question can be answered; no harm is stated." if bc["conditions"] else "None of the computed conditions applies.") + "\n")
    sdc = KL2.star_dasha_conditions(c, day_, bc["half"] == "bright")
    w("**Conditional star dashas whose condition is met (Parashara 46.17-43).** " + ("; ".join(sdc) if sdc else "none") + ". Vimshottari remains the chief dasha (46.3, 46.14); the others are cross-checks.\n")
    try:
        from engine import parashara_extra as PX
        ns, mo = PX.nine_states(c), PX.six_moods(c)
        w("**States of the planets (Parashara 45.7-17).** " + "; ".join(
            f"{p}: {ns[p]['state']}" + (", " + ", ".join(ns[p]['also']) if ns[p]['also'] else "") +
            (" - mood " + "/".join(mo[p]['moods']) if mo[p]['moods'] else "") for p in ns) + ". " +
          "'A house gives according to the state of the planet in it' (45.10). In 1,200 random charts 68% of planets are 'glad' and 47% 'hungry', so those two say little; "
          "**ashamed (4%), thirsty (1%), agitated (1%) and proud (11%) are the moods worth a remark.** " +
          ("Hungry or agitated with no glad or proud mood to offset it (45.18, 'harms the house it sits in'): " +
           ", ".join(f"{p} in house {mo[p]['house']}" for p in mo if mo[p]['harms_house']) + " - one planet in seven is in this case." if any(x['harms_house'] for x in mo.values()) else "No planet is hungry or agitated without an offsetting mood.") + "\n")
        ag = PX.argala(c)
        none_ = [h for h in range(1, 13) if not ag[h]["planets"]]
        pure = [h for h in range(1, 13) if ag[h]["kind"] == "benefic"]
        malf = [h for h in range(1, 13) if ag[h]["kind"] == "malefic"]
        w("**Argala - what makes a house's result firm (Parashara 31).** Planets in the 2nd, 4th, 11th and 5th from a house support it unless as many sit in the 12th, 10th, 3rd and 9th. " +
          f"Houses with unobstructed support from benefics only: {pure or 'none'}; from malefics only (31.17: middling): {malf or 'none'}; houses with no unobstructed support: {none_ or 'none'}. " +
          "Four houses in five have some argala and two charts in five have it on the 1st, 5th and 9th together, so only the houses with none, or with benefics alone, are worth a remark. " +
          "The result comes in the period of the planet or sign that forms it (31.9).\n")
        ug = PX.upagrahas(c); gl = ug["gulika_group"]["Gulika"]; md = ug["mandi_group_pd"]["Mandi"]; nl = ug["non_luminous"]; pp = ug["pranapada"]
        w(f"**Gulika and the shadow points (Parashara 3.61-74; Phaladeepika 25).** Gulika by Parashara (the sign rising in Saturn's eighth of the {'day' if ug['day_birth'] else 'night'}): "
          f"{gl['at_start']['sign_name']} (house {gl['at_start']['house']}) at the start of the part, {gl['at_end']['sign_name']} (house {gl['at_end']['house']}) at its end - the verse does not say which. "
          f"Mandi by Mantreshvara's fixed time ({md['ghatis']} ghatis, PD 25.2): {md['sign_name']} (house {md['house']}). " +
          ("All three agree." if len({gl['at_start']['sign'], gl['at_end']['sign'], md['sign']}) == 1 else "They do not all agree, so Gulika's house is uncertain for this chart; where it matters use the sign named twice.") +
          " Read like Saturn (PD 25.18-21); in the 3rd, 6th or 11th it is counted favourable (PD 25.8-14). " +
          "Non-luminous points: " + ", ".join(f"{k} {x['sign_name']} (H{x['house']})" for k, x in nl.items()) +
          f". Pranapada {pp['sign_name']} (house {pp['house']}; " + ("one of the four good places" if pp['good_place'] else "not one of the good places 2, 4, 10, 11") +
          ") - it moves a sign every six minutes, so it means something only for a birth time recorded to the minute. Low weight throughout.\n")
        st = PX.sudarshana_table(c, int(age_now), 12)
        w("**Sudarshana years ahead (Parashara 74.21-26).** " + ("Read all three rings." if st["applies"] else "Read from the lagna only (two of lagna, Moon, Sun share a sign).") +
          " 'helped' = only benefics in the year's sign, 'pressed' = only malefics, by occupation alone; aspects and the lord are judged as for a birth chart.\n")
        w("| Year of life | House | From lagna | From Moon | From Sun |\n|---|---|---|---|---|")
        for rw in st["rows"]:
            cell = lambda x: f"{x['sign']} - {x['tone']}" + (f" ({', '.join(x['occupants'])})" if x['occupants'] else "")
            w(f"| {rw['year_of_life']} | {rw['house']} | {cell(rw['lagna'])} | {cell(rw['Moon'])} | {cell(rw['Sun'])} |")
        w("")
    except Exception as _e:                                  # noqa: BLE001
        w(f"(States, argala, Gulika and Sudarshana table not computed: {_e})\n")
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
    ckb = a["karakas"]["seven_bphs"]
    movable = {area: ckb.get(key) for area, key in MOVABLE.items()}
    for area, (hs, km, kf) in AREAS.items():
        ks_ = kf if sex == "F" else km
        row = []
        for p in PLANET_ORDER:
            l = v.sambandha(p, hs, ks_)
            links[(area, p)] = l
            strong = sum(1 for x in l if x.startswith(("occupies", "owns", "with", "is karaka")))
            cell = f"{strong}+{len(l) - strong}" if l else "-"
            row.append(cell + (" m" if movable.get(area) == p else ""))
        w(f"| {area} | {hs} | {', '.join(ks_)} | " + " | ".join(row) + " |")
    w("\nEach cell is strong+weak links. Strong = occupies the house, owns it, sits with its lord or a karaka, or is the karaka. Weak = aspects or disposes. Read an area into a sub-period only on a strong link, or on two weak ones backed by a transit; a planet that links to every row (common for Saturn, Mars and the nodes) discriminates nothing by itself - see Rule 8.\n")
    w("'m' marks the movable significator of that area by Parashara's own list (BPHS 32.13-16): " + "; ".join(f"{ar_} - {pl_}" for ar_, pl_ in movable.items() if pl_) + ". It is shown, not counted: whether a movable significator alone lets a sub-period deliver its area is under test (antar-event-rules.md, Rule 13) - never state an event on an 'm' alone.\n")
    w("## 11. Vimshottari\n")
    now = a["dasha_now"]
    w("Now: " + " / ".join(f"{d['lord']} (to {_d(d['end'])})" for d in now) + ".\n")
    try:                                                      # every chart: how far the dates move inside the birth-time window
        from engine.chart import build_chart as _bc
        i_ = c["input"]; win = int(r.get("window", 15))
        t0 = dt.datetime.strptime(i_["time"][:5], "%H:%M")
        def _starts(delta):
            t = (t0 + dt.timedelta(minutes=delta)).strftime("%H:%M")
            cc = _bc(i_["date"], t, i_["lat"], i_["lon"], i_["tz"])
            return t, {(m["lord"], ad["lord"]): ad["start"] for m in cc["dasha"]["maha"] for ad in m["antar"]}
        (ta, A), (tb, B) = _starts(-win), _starts(win)
        today_ = r["today"]
        rows = [(m["lord"], ad["lord"], ad["start"]) for m in c["dasha"]["maha"] for ad in m["antar"]
                if (ad["end"].date() if hasattr(ad["end"], "date") else ad["end"]) >= today_][:8]
        shift = abs((A[rows[0][:2]] - B[rows[0][:2]]).days) / 2.0 if rows and rows[0][:2] in A and rows[0][:2] in B else 0
        w(f"**How firm the dates are.** If the birth time is off by {win} minutes either way, every dasha date moves by about {shift:.0f} days "
          f"({shift / 7:.0f} weeks). State dates as a season, not a day, unless the birth time is recorded to the minute; with a wider uncertainty re-run with `--window`.\n")
        w(f"| Sub-period begins | If born {ta} | As given ({i_['time'][:5]}) | If born {tb} |\n|---|---|---|---|")
        for md_, ad_, st_ in rows:
            w(f"| {md_} - {ad_} | {_d(A.get((md_, ad_), st_))} | {_d(st_)} | {_d(B.get((md_, ad_), st_))} |")
        w("")
    except Exception as _e:                                  # noqa: BLE001
        w(f"(Date range across the birth-time window not computed: {_e})\n")
    w("| Mahadasha | Antardasha | From | To | Age | Sub-lord from dasha lord | Check before stating any gain | Areas the antardasha lord is STRONGLY linked to |\n|---|---|---|---|---|---|---|---|")
    caut = period_cautions(v)
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
            w(f"| {md} | {ad} | {_d(s2)} | {_d(e)} | {(s2 - local).days / 365.25:.1f}-{(e - local).days / 365.25:.1f} | {_rel(md, ad)} | {'; '.join(caut[ad]) or '-'} | {', '.join(tags)} |")
    w("\nSub-lord from dasha lord (Parashara ch. 52-60, stated pair by pair for most of the 81 pairs): in a kendra, a trine, the 3rd or the 11th from the dasha lord the sub-period supports; in the 6th, 8th or 12th it obstructs; the 2nd is listed with the supportive places for most pairs. This is weighed together with the sub-lord's own house from the lagna and its dignity.\n")
    w("**Check before stating any gain** (Jataka Parijata 18.27-28, read in the Sanskrit): a debilitated planet, a planet joined to one, a planet joined to Rahu and the lord of a debilitated planet's sign do not give good in their periods, however strong; a planet at a sign junction gives strain. Where this column is not '-', state the planet's houses as the subject of the period and do NOT promise their gain (antar-event-rules.md, Rule 12 - the first miss of the rebuilt system came from skipping this). In this chart: " + ("; ".join(f"{p_} - {', '.join(c_)}" for p_, c_ in caut.items() if c_) or "no planet is affected") + ".\n")
    from engine import classical as KL
    dv = KL.delivery_time(c)
    w("When inside its own period a planet delivers - two classical pointers (by the third of its sign, reversed if retrograde: Parashara 47.3-4; by the rising-type of its sign: 50.88-89). "
      "Where both agree: " + ("; ".join(f"{p} {x['by_third']}" for p, x in dv.items() if x["agree"]) or "none") +
      ". Where they differ (no statement): " + ("; ".join(f"{p} {x['by_third']}/{x['by_rising']}" for p, x in dv.items() if not x["agree"]) or "none") + ".\n")
    try:
        _today = dt.date.today()
        for _lvl, _dl in zip(("Dasha lord", "Sub-period lord"), now[:2]):
            _mt = KL.month_triggers(_dl["lord"]); _tr = KL.dasha_lord_transit(c, _dl["lord"], _today)
            w(f"{_lvl} {_dl['lord']} (Phaladeepika 20.34-38): now passing through {_tr['sign']}, house {_tr['house']} - it {_tr['effect']} that house while there. "
              "Its good tends to arrive with the Sun in " + ", ".join(f"{n} ({m})" for n, m in _mt["good"]) +
              ("; its hardship with the Sun in " + ", ".join(f"{n} ({m})" for n, m in _mt["hard"]) if _mt["hard"] else "") + ". Classical, untested here - tentative.\n")
    except Exception as _e:
        w(f"(dasha-lord transit line not computed: {_e})\n")
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
        if not st["scored"]:
            w("\n**Project track record (data/ledger.jsonl).** None yet: the ledger restarted empty on 13 Nov 2026 with the rebuilt system. "
              "Say so in Part 1. The earlier system's record (24 fully right of 39 questions about the past) is archived and is not this system's record. "
              "Log every checking question and every dated forward statement from this reading.\n")
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


def other_clocks_md(r):
    L = ["\n## 16. Two other classical clocks (built 13 Nov 2026) - read the notes before using a date\n"]
    kc = r.get("kalachakra")
    if kc:
        q = kc["quarter"]; RNn = __import__("engine.chart", fromlist=["RASHI_NAMES"]).RASHI_NAMES
        L.append(f"**Kalachakra dasha** (BPHS 46; Jataka Parijata 17). Moon's star {q['star']}, quarter {q['pada']}, {'direct' if q['direct'] else 'reverse'} wheel; "
                 f"body sign {RNn[q['body_sign'] - 1]}, life sign {RNn[q['life_sign'] - 1]}; {q['fraction_elapsed'] * 100:.0f}% of the quarter had passed at birth.\n")
        L.append("| Sign | Lord | House from lagna | From | To | Cycle | Entered by |\n|---|---|---|---|---|---|---|")
        lag = r["chart"]["lagna"]["rashi"]; lim = r["today"].year + 26
        for p in kc["periods"]:
            if p["start"].year > lim: break
            L.append(f"| {p['name']} | {p['lord']} | {(p['sign'] - lag) % 12 + 1} | {p['start'].date()} | {p['end'].date()} | {p['cycle']}{' *' if p['cycle'] > 1 else ''} | {p['jump'] or ''} |")
        L.append("\n\\* cycle 2 or later: continuation rule not in the verses we read.\n")
        L += ["- " + n for n in kc["notes"]]
    ls = r.get("lifespan_dasha")
    if ls:
        L.append("\n**Life-span dasha - periods only** (Brihat Jataka 7-8; Vriddha Yavana Jataka 6). Order of lords: " + ", ".join(ls["order"]) + ".\n")
        if ls["ended_before_date"]:
            L.append("Not usable for this chart at today's date - a limit of the method, nothing about the person.\n")
        else:
            L.append("| Lord | From | To | Reduction applied | Sub-period lords |\n|---|---|---|---|---|")
            for p in ls["periods"]:
                L.append(f"| {p['lord']} | {p['start'].date()} | {'beyond the window' if p['runs_past_window'] else p['end'].date()} | {p['reduction'] or ''} | {', '.join(x['lord'] for x in p['subs'])} |")
        L += ["- " + n for n in ls["notes"]]
    return "\n".join(L) + "\n"


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
    md += F.markdown(r["findings"])
    md += other_clocks_md(r)
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
