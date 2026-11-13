"""Findings register - so that nothing the engine has computed can be left out of a reading.

Every chart feature the project's sources treat as meaningful is emitted here as a FINDING:
    id      stable identifier, e.g. "H07.judgement", "NR.Venus", "BRK.8L>9L"
    part    which of the 13 parts of the reading it belongs to
    weight  "must" (the reading has to deal with it) or "note" (available, optional)
    text    the plain statement
    rule    key into RULES below (source verse and how far our own tests support it)
    data    the numbers it rests on

Three guarantees, each enforced by a test in tests/test_findings.py:
  1. every finding points to a registered rule (no ad-hoc statements);
  2. every registered rule is either computed here or listed as PENDING, and the pending list is
     printed on every worksheet, so a reading states what was NOT examined;
  3. `check` refuses a draft reading that neither cites nor waives a "must" finding.

A draft cites a finding with the tag [F:id]; it sets one aside with [F:id waived: reason].
`python3 -m engine.findings strip DRAFT.md` removes the tags for the copy that is sent.

Thresholds marked UNSOURCED are ours, not the texts'. Nothing in this module predicts: it lists what is
present. Whether a listed feature may be stated as good/bad is governed by the rule's `status`.
"""
from __future__ import annotations
import json, os, re, sys
from engine.analysis import View, SEVEN, EXALT, DEBIL, hfrom, sign_at, period_cautions
from engine.chart import RASHI_LORD, RASHI_NAMES

try:
    GRID = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "vyj_grid.json"), encoding="utf-8"))["chapters"]
except Exception:                                   # noqa: BLE001 - the register still works without the verse texts
    GRID = {}

BEN3 = ("Mercury", "Jupiter", "Venus")            # Jataka Parijata 11.1 names exactly these three (and the house's own lord)
BEN4 = ("Moon", "Mercury", "Jupiter", "Venus")    # Vriddha Yavana Jataka ch. 9-15, 36
MAL3 = ("Sun", "Mars", "Saturn")
MAL = ("Sun", "Mars", "Saturn", "Rahu", "Ketu")
DUS = (6, 8, 12)
GOODH = (1, 4, 7, 10, 5, 9)
PARTS = {1: "How this was made and checked", 2: "Chart at a glance", 3: "Nature", 4: "Past timeline", 5: "Now",
         6: "Career", 7: "Money and property", 8: "Health", 9: "Family", 10: "Marriage", 11: "Children",
         12: "Long view", 13: "Uncertainties, spiritual, remedies"}
HOUSE_PART = {1: 3, 2: 7, 3: 9, 4: 9, 5: 11, 6: 8, 7: 10, 8: 12, 9: 9, 10: 6, 11: 7, 12: 12}
HOUSE_NAME = {1: "self and body", 2: "money, speech, family", 3: "siblings, courage", 4: "home, mother, comfort, vehicles",
              5: "children, intelligence", 6: "rivals, illness, service", 7: "marriage, partners", 8: "obstacles, hidden matters",
              9: "fortune, father, dharma", 10: "work and standing", 11: "gains", 12: "expenses, foreign, loss"}

# status: text = stated by a source, untested by us (description only) | hint = tested, faint edge |
#         chance = tested, no better than wrong charts (never state as a direction) | frozen = awaiting confirmation on new people |
#         pending = in the texts, NOT yet computed | excluded = read, never used (project rule)
RULES = {
    "state": {"text_quality": "clean", "source": "BPHS 3, 45; Jataka Parijata 2", "status": "text", "what": "dignity, combustion, retrogression, junctions"},
    "scale": {"text_quality": "clean", "source": "Jataka Parijata 7.58, 8.115-116", "status": "text", "what": "share of result by dignity: exalted full, trine sign 3/4, own 1/2, friend 1/4, enemy little, debilitated or combust none"},
    "navamsa_reversal": {"text_quality": "clean", "source": "Jataka Parijata 6.36 (also five places in ch. 18)", "status": "text", "what": "exalted sign with debilitated navamsa gives low results; debilitated sign with exalted navamsa gives good"},
    "house_judgement": {"text_quality": "clean; one verse (11.4) has a gap", "source": "Jataka Parijata 11.1-12", "status": "text", "what": "what builds and what harms each house"},
    "house_degree": {"text_quality": "clean; no scale given", "source": "Jataka Parijata 11.12", "status": "text", "what": "a planet at the house's own degree gives the full result, further away less"},
    "breaker": {"text_quality": "clean; conditions sit in combined verses and are split by us", "source": "Jataka Parijata 6.10, 6.21-24, 6.28, 6.30", "status": "text", "what": "what breaks the chart's promise"},
    "aspect_nature": {"text_quality": "clean; about one verse in twenty damaged", "source": "Vriddha Yavana Jataka ch. 9-15, 36", "status": "frozen", "what": "seen by Moon, Mercury, Jupiter, Venus = good; by Sun, Mars, Saturn = bad (same idea as Rule 18)"},
    "strength_part": {"text_quality": "clean text; THRESHOLDS OURS", "source": "Vriddha Yavana Jataka ch. 17-23 v.41-68", "status": "text", "what": "each separate kind of strength has its own result, present or lacking"},
    "quality_grid": {"text_quality": "about one verse in six damaged", "source": "Vriddha Yavana Jataka ch. 24a-35", "status": "text", "what": "kind of result of a planet in a house by sign dignity, navamsa dignity and division owners"},
    "sources_disagree": {"text_quality": "clean", "source": "Vriddha Yavana Jataka ch. 16, 30 against Jataka Parijata ch. 8 and Brihat Jataka", "status": "text", "what": "the texts give opposite results for this placement"},
    "caution": {"text_quality": "clean", "source": "Jataka Parijata 18.27-28", "status": "text", "what": "check before stating any gain in this planet's period"},
    "yoga": {"text_quality": "mixed - see catalogue tags", "source": "engine catalogue (BPHS, Phaladeepika, Brihat Jataka, Jataka Parijata 7)", "status": "text", "what": "named combination present"},
    "yoga_timing": {"text_quality": "clean", "source": "Garga in Jataka Parijata 7.66", "status": "text", "what": "a yoga pays in the dasha of the strong planet that makes it"},
    "dosha": {"text_quality": "clean", "source": "BPHS 80.47; Jataka Parijata 14.34", "status": "text", "what": "Mars placement for marriage"},
    "link_timing": {"text_quality": "clean", "source": "Jataka Parijata 11.51, 12.2-3, 12.23, 12.110; Vriddha Yavana Jataka 25.31", "status": "hint", "what": "results come in the period of the planet in, looking at, ruling or signifying the house (26 of 37 against 20.4)"},
    "direction": {"text_quality": "our tests", "source": "our own control tests", "status": "chance", "what": "good/bad direction of a period - seven methods at chance; state the subject, not the direction"},
    "time_doubt": {"text_quality": "calculation", "source": "engine", "status": "text", "what": "what changes inside the doubt in the birth time"},
    # --- in the texts, not yet computed: printed on every worksheet -------------------------------------------
    "kalachakra": {"text_quality": "sequences clean after totals check; CONTINUATION RULE OURS", "source": "BPHS 46.52-154; Jataka Parijata 17", "status": "text", "what": "Kalachakra dasha - a second clock, by signs; sensitive to birth time; periods after the first cycle rest on a rule not in the verses"},
    "lifespan_dasha": {"text_quality": "spans clean; SEVERAL CONVENTIONS OURS; one reduction omitted (damaged verse)", "source": "Brihat Jataka 7-8; Vriddha Yavana Jataka 6; Jataka Parijata 5.2-16", "status": "text", "what": "the old dasha built on each planet's share - periods only, experimental, several conventions ours, never a length of life"},
    "prashna": {"text_quality": "clean; +-2 THRESHOLD OURS", "source": "Shatpanchashika; Daivajna Vallabha", "status": "text", "what": "question charts - separate tool: python3 -m engine.prashna (not part of a birth reading)"},
    "second_seventh_from_house": {"text_quality": "clean", "source": "Jataka Parijata 5.50", "status": "chance", "what": "periods of the lords of the 2nd and 7th from any house harm that house - tested 13 Nov 2026: 1 of 4, at chance, far too few cases"},
    "eighth_part": {"text_quality": "DAMAGED method verse; OWNER ORDER UNSOURCED", "source": "Vriddha Yavana Jataka 8.16-129", "status": "chance", "what": "a planet's period judged by the eighth-part of the sign it stands in - tested 13 Nov 2026: 13 of 25 against 11.1 (27% of wrong charts as good), not significant; owner order unsourced"},
    "siblings_3_9_11_7": {"text_quality": "clean", "source": "Jataka Parijata 12.2-3", "status": "chance", "what": "siblings judged from houses 3, 9, 11 and 7 - tested 13 Nov 2026: 4 of 5 against 3.9 for wrong charts, no information (the wider net catches wrong charts too)"},
    "lagna_tie": {"text_quality": "clean", "source": "Jataka Parijata 12.110, 12.130", "status": "chance", "what": "for rank and vehicles the planet must also be tied to the lagna - tested 13 Nov 2026: 4 of 12 against 2.4 (23% of wrong charts as good), not significant"},
    "grid_english": {"source": "Vriddha Yavana Jataka ch. 24a-35", "status": "pending", "what": "the grid verses are stored in Sanskrit (data/vyj_grid.json) and printed on the worksheet; a fixed English wording per verse is not stored - it is read at the time of the reading"},
    "strength_count": {"text_quality": "clean text; THRESHOLDS OURS", "source": "Vriddha Yavana Jataka ch. 17-23", "status": "chance", "what": "count of strength parts as a good/bad rule for a period - tested 13 Nov 2026: 3 of 10 against 5.7 for wrong charts, at chance (thresholds ours)"},
    "house_lords_in_houses_vyj": {"source": "Vriddha Yavana Jataka part two, ch. 40-71", "status": "pending", "what": "not read - searched 13 Nov 2026: no free e-text found; only a printed edition for sale, which the source rule excludes"},
    "saravali": {"source": "Saravali of Kalyanavarman, Nirnaya Sagar Press edition (1928), page text at jainqq.org/pagetext/Saravali/009887/1 to 268", "status": "pending", "what": "FOUND free online 13 Nov 2026, NOT yet read - about 268 pages, needs the browser"},
    "jaimini": {"source": "Jaimini (Upadesha) sutras", "status": "pending", "what": "not read - only manuscript images (UPenn Ms. Coll. 390 items 700, 706) and paid editions found; no clean free text yet"},
    # --- the calendar and the tables (added 13 Nov 2026: a reading may only state what is in the register) -----
    "period_link": {"text_quality": "calculation; link rule ours (antar-event-rules.md Rule 1)", "source": "BPHS 46 (Vimshottari), 52-60 (sub-lord's house from the dasha lord); engine link test", "status": "hint",
                    "what": "which sub-period runs when, and which life areas its lord is strongly linked to - the SUBJECT of the period; faint edge in our tests"},
    "transit": {"text_quality": "calculation; as a good/bad rule our tests put it at chance", "source": "Phaladeepika 26; BPHS 66-72; engine ephemeris", "status": "chance",
                "what": "where Saturn, Jupiter and Rahu pass and when - positions are calculation; never a good/bad forecast"},
    "table": {"text_quality": "calculation", "source": "engine (BPHS 6-7 divisions, 32 karakas, 29 arudhas, 34 lordships, 66-72 Ashtakavarga)", "status": "text",
              "what": "placements and tables computed for the chart - facts of the chart, not judgements"},
    # --- read and never used ----------------------------------------------------------------------------------
    "excluded": {"source": "Jataka Parijata 4, 5.45-123, 6.46-98, 9.45-84; Vriddha Yavana Jataka 28.29-30, 31; Daivajna Vallabha 8, 12.5-10, 13",
                 "status": "excluded", "what": "length of life, time or manner of death, widowhood, sex or number of children, medical statements"},
}


def _f(out, id_, part, weight, text, rule, **data):
    out.append({"id": id_, "part": part, "weight": weight, "text": text, "rule": rule, "data": data})


def _dig(d):                       # normalise the engine's dignity label
    d = d.lower()
    for k, lab in (("exalt", "exalted"), ("debil", "debilitated"), ("moola", "trine"), ("own", "own"),
                   ("friend", "friend"), ("enemy", "enemy")):
        if k in d: return lab
    return "neutral"


SCALE = {"exalted": "full", "trine": "three quarters", "own": "half", "friend": "a quarter", "neutral": "not stated by the text",
         "enemy": "little", "debilitated": "none"}


def planets(r, out):
    c, a = r["chart"], r["analysis"]; v: View = a["view"]; st = a["states"]
    for p in SEVEN:
        d = c["planets"][p]; s = st[p]; dg = _dig(s["dignity"]); h = v.house(p)
        flags = [k for k in ("retrograde", "combust", "vargottama", "sandhi", "gandanta") if s.get(k)]
        share = "none" if s.get("combust") and p not in ("Venus", "Saturn") and dg != "exalted" else SCALE[dg]
        _f(out, f"P.{p}.state", 2, "must" if dg in ("exalted", "debilitated") or flags else "note",
           f"{p} in {RASHI_NAMES[d['rashi'] - 1]} ({dg} sign), house {h}" + (", " + ", ".join(flags) if flags else "")
           + f". Share of its results by dignity: {share}.", "state", dignity=dg, house=h, flags=flags, share=share)
        # navamsa reversal
        d9 = d["D9"]
        if d["rashi"] == EXALT[p] and d9 == DEBIL[p]:
            _f(out, f"NR.{p}", 2, "must", f"{p} is exalted by sign but its navamsa is its debilitation sign: the text says it gives LOW results, quickly.", "navamsa_reversal", d9=d9)
        elif d["rashi"] == DEBIL[p] and d9 == EXALT[p]:
            _f(out, f"NR.{p}", 2, "must", f"{p} is debilitated by sign but its navamsa is its exaltation sign: the text says it gives GOOD results.", "navamsa_reversal", d9=d9)
        elif (dg == "exalted" and _dig(s.get("d9_dignity") or "") == "enemy") or (dg == "debilitated" and _dig(s.get("d9_dignity") or "") in ("own", "friend")):
            _f(out, f"NR.{p}.partial", 2, "note", f"{p}: sign dignity {dg}, navamsa dignity {_dig(s['d9_dignity'])} - the two pull opposite ways; weigh both (weaker form of the same principle; our extension, not the verse).", "navamsa_reversal")
        # who looks at it
        seen = [q for q in v.aspected_by(p, nodes=False) if q in SEVEN] + [q for q in v.conj(p) if q in SEVEN]
        b = sorted({q for q in seen if q in BEN4}); m = sorted({q for q in seen if q in MAL3})
        if b or m:
            call = "good" if b and not m else "bad" if m and not b else "mixed"
            _f(out, f"ASP.{p}", 2, "note", f"{p} is joined or seen by " + (", ".join(b) or "no natural benefic") + " and by " + (", ".join(m) or "no natural malefic")
               + f" - by the texts' simple rule: {call}. This rule is frozen: not to be stated as a prediction.", "aspect_nature", benefics=b, malefics=m, call=call)
    for p, cs in period_cautions(v).items():
        if cs:
            _f(out, f"C.{p}", 5, "must", f"{p}'s periods: " + "; ".join(cs) + ". Name the houses as the subject; do not promise the gain.", "caution", cautions=cs)
    for a_, b_ in a.get("graha_yuddha") or []:
        _f(out, f"WAR.{a_}.{b_}", 2, "must", f"{a_} and {b_} are within one degree of each other (planetary war).", "state")


def strengths(r, out):
    sb = r.get("shadbala") or {}
    if "planets" not in sb: return
    for p in SEVEN:
        x = sb["planets"][p]; has, lacks = [], []
        graded = {"nearness to its exaltation degree": x["sthana"]["uchcha"], "direction": x["dig"], "motion": x["cheshta"],
                  "day/night": x["kala"]["nathonnata"], "fortnight": x["kala"]["paksha"]}
        for k, val in graded.items():                       # UNSOURCED thresholds: two thirds / one third of 60
            if val >= 40: has.append(k)
            elif val <= 20: lacks.append(k)
        for k, key in (("year lord", "abda"), ("month lord", "masa"), ("weekday lord", "vara"), ("hour lord", "hora")):
            if x["kala"][key] > 0: has.append(k)
        _f(out, f"SB.{p}", 2, "note", f"{p} strength by part - has: " + (", ".join(has) or "none of the listed") + "; lacks: " + (", ".join(lacks) or "none")
           + f". Total {x['rupas']:.2f} rupas, {x['ratio_text']:.2f} of what the texts require.", "strength_part", has=has, lacks=lacks,
           rupas=round(x["rupas"], 2), ratio=round(x["ratio_text"], 2))


def houses(r, out):
    c, a = r["chart"], r["analysis"]; v: View = a["view"]; st = a["states"]; ldeg = c["lagna"]["lon"] % 30
    for h in range(1, 13):
        sg = sign_at(v.lag, h); L = v.lord(h); up, down, neutral = [], [], []
        lh = v.house(L); ld = _dig(st[L]["dignity"])
        (down if lh in DUS else up if lh in GOODH else neutral).append(f"lord {L} in house {lh}" + (" (11.4)" if lh in DUS else " (11.5)" if lh in GOODH else ""))
        if ld in ("exalted", "trine", "own", "friend"): up.append(f"lord {L} {ld} by sign (11.5)")
        if ld in ("debilitated", "enemy"): down.append(f"lord {L} {ld} by sign (11.7)")
        if st[L].get("combust"): down.append(f"lord {L} combust (11.7)")
        disp = RASHI_LORD[v.s[L] - 1]
        if disp != L:
            dh = v.house(disp); dd = _dig(st[disp]["dignity"]) if disp in SEVEN else "neutral"
            if dh in DUS: down.append(f"the lord's sign-lord {disp} in house {dh} (11.10)")
            elif dd in ("exalted", "own", "friend", "trine"): up.append(f"the lord's sign-lord {disp} {dd} (11.10)")
        occ = v.occupants(sg); near = []
        for p in occ:
            pd = _dig(st[p]["dignity"]) if p in SEVEN else "neutral"
            if p == L: up.append(f"own lord {p} in the house (11.1)")
            elif p in BEN3: up.append(f"{p} in the house (11.1)")
            elif p in MAL: down.append(f"{p} in the house (11.2)")
            else: neutral.append(f"{p} in the house")
            if p in SEVEN and p != L and pd in ("debilitated", "enemy"): down.append(f"{p} there in {pd} sign (11.3)")
            if p in SEVEN and p != L and pd in ("exalted", "trine", "friend"): up.append(f"{p} there in {pd} sign (11.3)")
            if p in SEVEN and p != L and any(x in DUS for x in v.owns(p)) and h not in DUS: down.append(f"{p}, a lord of 6/8/12, sits here (11.4)")
            dist = abs(c["planets"][p]["lon"] % 30 - ldeg)
            near.append((p, round(dist, 1)))
        for p in v.aspecting(sg, nodes=False):
            if p in occ: continue
            if p == L: up.append(f"own lord {p} looks at it (11.1)")
            elif p in BEN3: up.append(f"{p} looks at it (11.1)")
            elif p in MAL3: down.append(f"{p} looks at it (11.2)")
        for k in (5, 9, 4, 7, 10):
            for p in v.occupants(sign_at(sg, k)):
                if p in BEN3: up.append(f"{p} in the {k}th from it (11.6)")
        txt = (f"House {h} ({HOUSE_NAME[h]}), {RASHI_NAMES[sg - 1]}: builds it - " + ("; ".join(up) or "nothing listed")
               + ". Harms it - " + ("; ".join(down) or "nothing listed") + "." + (" Also: " + "; ".join(neutral) + "." if neutral else ""))
        _f(out, f"H{h:02d}.judgement", HOUSE_PART[h], "must", txt, "house_judgement", builds=up, harms=down, lord=L, lord_house=lh)
        if near:
            _f(out, f"H{h:02d}.degree", HOUSE_PART[h], "note", f"House {h}: distance of each planet in it from the house's own degree ({ldeg:.1f} deg of the sign) - "
               + ", ".join(f"{p} {d_} deg" for p, d_ in near) + ". Closer = fuller result; the text gives no scale.", "house_degree", near=near)


def grid(r, out):
    """Vriddha Yavana Jataka ch. 24a-35: which of the twelve conditions each planet meets in its house, with the verse to read."""
    c, a = r["chart"], r["analysis"]; v: View = a["view"]; st = a["states"]
    for i, p in enumerate(SEVEN):
        d = c["planets"][p]; h = v.house(p); ch = "24a" if h == 1 else str(23 + h); base = 4 * i
        dg = _dig(st[p]["dignity"]); d9 = _dig(st[p]["d9_dignity"] or "")
        six = [d["rashi"], d["D2"], d["D3"], d["D9"], d["D12"], d["D30"]]
        nb = sum(1 for s_ in six if RASHI_LORD[s_ - 1] in BEN4)
        cond = []
        if dg == "exalted": cond.append(("exalted sign", base + 1))
        if d["D9"] == EXALT[p]: cond.append(("exalted navamsa", base + 1))
        if nb == 6: cond.append(("all six divisions benefic-owned", base + 1))
        if dg == "debilitated": cond.append(("debilitated sign", base + 2))
        if d["D9"] == DEBIL[p]: cond.append(("debilitated navamsa", base + 2))
        if nb == 0: cond.append(("all six divisions malefic-owned", base + 2))
        if dg == "friend": cond.append(("friend's sign", base + 3))
        if d9 == "friend": cond.append(("friend's navamsa", base + 3))
        if st[p].get("vargottama"): cond.append(("same sign in navamsa (vargottama)", base + 3))
        if dg == "enemy": cond.append(("enemy's sign", base + 4))
        if d9 == "enemy": cond.append(("enemy's navamsa", base + 4))
        if dg == "trine": cond.append(("own trine sign", base + 4))
        verses = {}
        for _, vn in cond:
            vv = (GRID.get(ch) or {}).get(str(vn))
            if vv: verses[f"{ch}.{vn}"] = vv["text"] + (" [damaged in the e-text]" if vv["damaged"] else "")
        txt = (f"{p} in house {h}: " + ("; ".join(f"{n} - see Vriddha Yavana Jataka {ch}.{vn}" for n, vn in cond) if cond
                                        else "none of the twelve conditions of the text applies (own or neutral sign has no verse)")
               + f". Benefic-owned divisions: {nb} of 6.")
        if h == 8: txt += " The text's chapter for the 8th house is on the manner of death - not stored, not used."
        elif h == 5: txt += " The text's chapter for the 5th house is on children - not stored; never state number, sex or loss of children."
        elif verses: txt += " Sanskrit (each line has three clauses, in the order sign / navamsa / divisions; take the clause for the condition met): " + " || ".join(f"{k}: {t}" for k, t in verses.items())
        if h == 7 and verses: txt += " These are the classical wordings about a spouse - soften, and never state them as fact about a real person."
        _f(out, f"Q.{p}", HOUSE_PART[h], "note", txt, "quality_grid", house=h, chapter=ch, conditions=cond, benefic_divisions=nb, verses=verses)


def breakers(r, out):
    c, a = r["chart"], r["analysis"]; v: View = a["view"]; st = a["states"]; sb = (r.get("shadbala") or {}).get("planets") or {}
    rup = lambda p: sb[p]["rupas"] if p in sb else None
    def stronger(x, y, id_, words):
        if x == y or rup(x) is None: return
        if rup(x) > rup(y):
            _f(out, id_, 12, "must", f"{words}: {x} {rup(x):.2f} rupas against {y} {rup(y):.2f}. One condition of a combined poverty verse - the text lists it among what weakens the chart's promise; on its own it is a weight, not a verdict.", "breaker", a=x, b=y)
    stronger(v.lord(8), v.lord(9), "BRK.8L>9L", "The 8th lord is stronger than the 9th lord (6.28)")
    stronger(v.lord(12), v.lord(1), "BRK.12L>1L", "The 12th lord is stronger than the lagna lord (6.30)")
    l11 = v.lord(11)
    if st[l11].get("combust") and v.house(l11) not in (1, 4, 7, 10):
        _f(out, "BRK.11L.combust", 7, "must", f"The 11th lord {l11} is combust and outside the angles (6.28).", "breaker")
    l1 = v.lord(1)
    if v.lord(8) != l1 and v.lord(8) in v.aspected_by(l1) and rup(l1) is not None and sb[l1]["ratio_text"] < 1:
        _f(out, "BRK.1L.seen.by.8L", 3, "must", f"The lagna lord {l1} is below required strength and is looked at by the 8th lord {v.lord(8)} (6.21).", "breaker")
    if st["Jupiter"].get("combust"):
        _f(out, "BRK.Jupiter.combust", 12, "must", "Jupiter is combust (6.21).", "breaker")
    weak3 = [p for p in SEVEN if p != "Sun" and (st[p].get("combust") or _dig(st[p]["dignity"]) == "debilitated")]
    if len(weak3) >= 3:
        _f(out, "BRK.three.weak", 12, "must", "Three or more planets debilitated or combust: " + ", ".join(weak3) + " (6.24).", "breaker", planets=weak3)
    md = c["planets"]["Moon"]["deg"]; ms = c["planets"]["Moon"]["rashi"]; kind = (ms - 1) % 3     # 0 movable, 1 fixed, 2 dual
    weakpart = (kind == 0 and md >= 20) or (kind == 1 and md < 10) or (kind == 2 and 10 <= md < 20)
    if weakpart and not [p for p in v.aspecting(v.lag, nodes=False)]:
        _f(out, "BRK.Moon.part", 12, "must", "The Moon is in the weak third of its sign (end of a movable, start of a fixed or middle of a dual sign) and no planet looks at the lagna (6.10). "
           "The text adds 'and the Moon weak' - check its strength line.", "breaker")


DISAGREE = {("Mars", 10): "Vriddha Yavana Jataka 16.34 gives a bad result; Jataka Parijata 8.90 and Brihat Jataka give power and fame",
            ("Jupiter", 6): "Vriddha Yavana Jataka 16.54 gives many enemies and illness; Jataka Parijata 8.77 gives victory over rivals (and low vigour); our rule reads it as overcoming rivals",
            ("Venus", 6): "Vriddha Yavana Jataka 16.66 and Jataka Parijata 8.77 give a bad result; Jataka Parijata 8.67 makes it good when Venus is ahead of the Sun",
            ("Sun", 7): "Vriddha Yavana Jataka 30.1-4 is unfavourable for marriage in every condition, even exalted; other texts are milder",
            ("Mercury", 5): "Vriddha Yavana Jataka 16.41 gives few children and low vigour; Jataka Parijata 8.72 gives children, learning and fame",
            ("Mercury", 6): "Vriddha Yavana Jataka 16.42 gives many enemies; Jataka Parijata 8.76 gives a taste for debate and learning"}


def disagreements(r, out):
    v: View = r["analysis"]["view"]
    for (p, h), why in DISAGREE.items():
        if v.house(p) == h:
            _f(out, f"DIS.{p}.{h}", HOUSE_PART[h], "must", f"{p} in house {h}: the texts disagree. {why}. Say so; do not pick one silently.", "sources_disagree")


def _common(name):
    """Share of 4,000 random charts with the same combination (engine.baserates), as words."""
    try:
        from engine.baserates import rate, label
        x = rate("yoga", name)
        return label(x) if x is not None else "not measured"
    except Exception:                                         # noqa: BLE001
        return "not measured"


def named(r, out):
    a = r["analysis"]; v: View = a["view"]; seen = {}
    for y in a.get("yogas") or []:
        n = seen.get(y["name"], 0); seen[y["name"]] = n + 1
        slug = re.sub(r"[^A-Za-z0-9]+", "-", y["name"]).strip("-") + (f"-{n + 1}" if n else "")
        makers = [p for p in y.get("planets") or [] if p in SEVEN]
        strong = [p for p in makers if v.strong(p)]
        _f(out, f"Y.{slug}", 12, "must", f"{y['name']}" + (f" ({', '.join(y.get('planets') or [])})" if y.get("planets") else "") + (f": {y['note']}" if y.get("note") else "")
           + (f". Weakened by: {y['weakened_by']}" if y.get("weakened_by") else "")
           + (f". When: in the dasha of its strong maker ({', '.join(strong)})" if strong else ". When: its makers are not strong by sign - the text ties the result to a strong maker's dasha")
           + f". How common: {_common(y['name'])}.", "yoga", makers=makers, strong=strong)
    m = (a.get("doshas") or {}).get("manglik") or {}
    if m.get("present"):
        _f(out, "D.Mars.marriage", 10, "must", "Mars placement counted for marriage is present; cancellations found: " + ("; ".join(m.get("cancellations_classical") or []) or "none in the texts") + ".", "dosha")
    ts = r.get("time_sensitivity")
    if ts:
        win = r.get("window")
        yrs = {"Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7, "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17}
        first = r["chart"]["dasha"]["maha"][0]["lord"]
        per_min = yrs[first] * 365.25 / (360 / 27) * (13.176 / 1440)      # days of dasha shift per minute of birth time (mean Moon)
        _f(out, "T.birth-time", 1, "must", f"Birth-time sensitivity, scanned {win} minutes either side of the stated time: " + (
            "no lagna or divisional lagna (D1, D9, D10, D7, D12, D3) changes inside that doubt" if len(ts) <= 1 else
            "a lagna or divisional lagna changes at " + ", ".join(str(x[0]) for x in ts[1:]) + " - findings resting on it are uncertain")
           + f". Dasha dates move by about {per_min:.1f} days for each minute of error in the birth time, so dates are given as seasons. Quote this before any date.", "time_doubt")
    _f(out, "M.direction", 1, "must", "Our own tests: the SUBJECT of a period has a faint edge (26 of 37 against 20.4 for wrong charts); good/bad DIRECTION is at chance on every method tried. "
       "State subjects; mark any direction as unsupported.", "direction")


def other_clocks(r, out):
    import datetime as dt
    c = r["chart"]; now = dt.datetime.now(c["input"]["local"].tzinfo)
    kc = r.get("kalachakra")
    if kc:
        from engine.dashas_classical import kalachakra_at
        p, sub = kalachakra_at(kc, now)
        if p:
            h = (p["sign"] - c["lagna"]["rashi"]) % 12 + 1
            _f(out, "K.kalachakra", 5, "note", f"Kalachakra dasha now: {p['name']} (house {h} from the lagna - {HOUSE_NAME[h]}), {p['start'].date()} to {p['end'].date()}"
               + (f"; sub-period {RASHI_NAMES[sub['sign'] - 1]} to {sub['end'].date()}" if sub else "")
               + (f"; entered by a {p['jump']}" if p.get("jump") else "")
               + (". This period lies AFTER the birth quarter's own nine signs, so it rests on a continuation rule that is not in the verses we read" if p["cycle"] > 1 else "")
               + ". The text reads the sign's house as the subject; as a good/bad rule it is untested or at chance - see the control table.", "kalachakra", sign=p["sign"], house=h, cycle=p["cycle"])
    ls = r.get("lifespan_dasha")
    if ls:
        from engine.dashas_classical import lifespan_at
        p, sub = lifespan_at(ls, now)
        if p:
            _f(out, "K.lifespan", 5, "note", f"Life-span dasha (periods only) now: {p['lord']}, from {p['start'].date()}" + (f"; sub-period {sub['lord']} to {sub['end'].date()}" if sub else "")
               + ". Experimental: several conventions are ours and it has not been cross-checked. No length of life is ever derived from it.", "lifespan_dasha", lord=p["lord"])
        else:
            _f(out, "K.lifespan", 5, "note", "Life-span dasha: not usable for this chart at this date. This is a limit of the method (Varahamihira's own objection, Brihat Jataka 7.7-8) and says nothing about the person.", "lifespan_dasha")


def pending():
    return [{"rule": k, **x} for k, x in RULES.items() if x["status"] == "pending"]


def timeline(r, out):
    """The calendar and the tables as findings, so that a reading cannot state a period, a transit or a divisional
    placement that the register does not hold (audit of 13 Nov 2026)."""
    import datetime as dt
    from engine.report import AREAS, MOVABLE
    from engine.analysis import period_cautions
    c, a = r["chart"], r["analysis"]; v = a.get("view"); tree = a.get("dasha_tree")
    if v is None or not tree: return
    local = c["input"]["local"]; now = dt.datetime.now(local.tzinfo); P = c["planets"]; lag = c["lagna"]["rashi"]
    d = lambda x: x.strftime("%d %b %Y")
    ck = a["karakas"]["seven_bphs"]; caut = period_cautions(v)
    strong = lambda p, ar: any(x.startswith(("occupies", "owns", "with", "is karaka")) for x in v.sambandha(p, AREAS[ar][0], AREAS[ar][2] if a.get("sex") == "F" else AREAS[ar][1]))
    def rel(md, ad):
        if md == ad: return "same planet"
        n = (P[ad]["rashi"] - P[md]["rashi"]) % 12 + 1
        return f"sub-lord in house {n} from the dasha lord - " + ("the texts call this obstructing" if n in (6, 8, 12) else "the texts call this supporting" if n != 2 else "listed as mostly supporting")
    for md, ms, me, ads in tree:
        for ad, s, e, pds in ads:
            if e <= local or (s - local).days > 365.25 * 90: continue      # fixed horizon by age, so the id list does not drift with the calendar
            s2 = max(s, local); part = 4 if e <= now else 5 if s <= now else 12
            areas = [ar for ar in AREAS if strong(ad, ar)]
            _f(out, f"V.{md}-{ad}", part, "note", f"{md}-{ad}: {d(s2)} to {d(e)} (age {(s2 - local).days / 365.25:.1f} to {(e - local).days / 365.25:.1f}); {rel(md, ad)}; "
               f"sub-lord strongly linked to: {', '.join(areas) or 'no area'}; check before stating any gain: {'; '.join(caut[ad]) or 'nothing flagged'}. "
               "Subject of the period only; good/bad direction is not supported by our tests.", "period_link", md=md, ad=ad)
            if s <= now < e and pds:
                _f(out, "V.now.months", 5, "note", f"Shorter periods inside the running {md}-{ad}: " + "; ".join(f"{x[0]} from {d(x[1])}" for x in pds) + f"; ends {d(e)}. Dates move with the birth time.", "period_link")
    for ar, (hs, km, kf) in AREAS.items():
        ps = [p for p in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu") if strong(p, ar)]
        mv = next((p for p, role in [(ck.get(MOVABLE.get(ar, "")), 1)] if p), None)
        _f(out, f"L.{ar.split('/')[0]}", 2, "note", f"Link test, {ar} (houses {', '.join(map(str, hs))}): planets strongly linked - {', '.join(ps) or 'none'}" + (f"; movable significator {mv} (shown, not counted)" if mv else "") + ".", "period_link")
    for pl, rows in (r.get("transits") or {}).items():
        near = [x for x in rows if str(x["to"]) >= str(now.date() - dt.timedelta(days=200)) and str(x["from"]) <= str(now.date() + dt.timedelta(days=int(365.25 * 5)))]
        if near:
            _f(out, f"TR.{pl}", 5, "note", f"{pl} passes: " + "; ".join(f"{x['sign']} (house {x['house']}, {x['house_from_moon']} from the Moon) {x['from']} to {x['to']}" for x in near)
               + ". Positions only: transit rules for good or bad scored at chance in our tests.", "transit")
    ph = [x for x in (r.get("saturn_phases") or []) if str(x["to"]) >= str(now.date() - dt.timedelta(days=1500)) and str(x["from"]) <= str(now.date() + dt.timedelta(days=int(365.25 * 9)))]
    if ph:
        _f(out, "TR.Saturn.phases", 5, "note", "Saturn's phases counted from the Moon: " + "; ".join(f"{x['phase']} in {x['sign']} {x['from']} to {x['to']}" for x in ph)
           + ". A calendar fact; the popular reading of these years as bad is not tested here.", "transit")
    av = r.get("ashtakavarga") or {}; chk = r.get("av_checks") or {}
    if av.get("by_house"):
        bh = av["by_house"]; bh = bh if isinstance(bh, dict) else dict(enumerate(bh, 1))
        _f(out, "AV.houses", 2, "note", "Combined Ashtakavarga points by house: " + ", ".join(f"H{k} {bh[k]}" for k in sorted(bh, key=int)) + ". Checks: "
           + "; ".join(f"{t} - {'yes' if ok else 'NO'}" for t, ok in chk.get("checks", [])) + f". Strong houses (30+): {chk.get('strong_houses')}; weak (25 or less): {chk.get('weak_houses')}.", "table")
    fn = (a.get("functional") or {}).get("planets", {})
    if fn:
        _f(out, "FN.lords", 2, "note", "Lordships for this lagna (Parashara's own verdict where he gives one): " + "; ".join(
            f"{p} owns {x['owns']} - {x.get('parashara') or x['nature']}" + (", yoga-giver" if x.get("parashara_yoga_giver") or x.get("yogakaraka") else "") for p, x in fn.items()) + ".", "table")
    _f(out, "JM.karakas", 2, "note", "Movable significators (seven-planet scheme): " + ", ".join(f"{k} {p}" for k, p in a["karakas"]["seven"].items()) + ".", "table")
    ar_ = a.get("arudhas") or {}
    if ar_:
        _f(out, "JM.arudhas", 2, "note", "Arudha padas: " + "; ".join(f"{k} in {x.get('sign')} (house {x.get('house')}" + (", with " + ", ".join(x["occupants"]) if x.get("occupants") else "") + ")"
           for k, x in ar_.items() if isinstance(x, dict) and x.get("sign") and x.get("house")) + ". These rest on the lagna and move with it.", "table")
    try:
        from engine.chart import varga_rashi as varga_sign
        ts = r.get("time_sensitivity") or []
        for n, use in ((9, "marriage and inner strength"), (10, "work")):
            L0 = varga_sign(c["lagna"]["lon"], n)
            pos = "; ".join(f"{p} house {(varga_sign(P[p]['lon'], n) - L0) % 12 + 1}" for p in P)
            _f(out, f"VG.D{n}", 2, "note", f"D{n} ({use}): lagna {RASHI_NAMES[L0 - 1]}; {pos}. The divisional lagna depends on the birth time - see the sensitivity table (rows: {len(ts)}).", "table")
    except Exception:                                         # noqa: BLE001 - the tables are an aid, never a blocker
        pass
    pn = a.get("panchanga") or {}
    if pn:
        _f(out, "PN.birth", 2, "note", f"Birth: {pn.get('vara')}, {pn.get('tithi')}, Moon's star {pn.get('nakshatra')} quarter {pn.get('pada')}, {'day' if pn.get('day_birth') else 'night'} birth "
           f"(sunrise {pn.get('sunrise')}).", "table")


def build(r):
    out = []
    for fn in (planets, strengths, houses, grid, breakers, disagreements, named, other_clocks, timeline):
        fn(r, out)
    ids = [f["id"] for f in out]
    assert len(ids) == len(set(ids)), "duplicate finding id: " + ", ".join(sorted({i for i in ids if ids.count(i) > 1}))
    return out


TAG = re.compile(r"\[F:([A-Za-z0-9_.>\-]+)(\s+waived:\s*[^\]]+)?\]")


def check(findings, draft_text):
    """Return (missing, waived, unknown): must-findings neither cited nor waived; waived ones; tags that match no finding."""
    cited, waived = set(), {}
    for m in TAG.finditer(draft_text):
        if m.group(2): waived[m.group(1)] = m.group(2).split(":", 1)[1].strip()
        else: cited.add(m.group(1))
    known = {f["id"] for f in findings}
    missing = [f for f in findings if f["weight"] == "must" and f["id"] not in cited and f["id"] not in waived]
    return missing, waived, sorted((cited | set(waived)) - known)


def strip(text):
    return re.sub(r"[ \t]*" + TAG.pattern, "", text)


def markdown(findings):
    L = ["\n## 15. Findings register - every one marked MUST has to be dealt with in the reading\n",
         "Cite a finding in the draft as `[F:id]`, or set it aside as `[F:id waived: reason]`. Before sending run "
         "`python3 -m engine.findings check WORKSHEET.json DRAFT.md`; it lists every MUST finding the draft has not touched. "
         "`... strip DRAFT.md` removes the tags. The 'evidence' word says how far a line may be pushed: "
         "text = stated by a source, untested by us; hint = faint edge in our tests; frozen = not to be used as a prediction; chance = never state as a direction.\n"]
    for part in sorted(PARTS):
        rows = [f for f in findings if f["part"] == part]
        if not rows: continue
        L.append(f"\n**Part {part} - {PARTS[part]}**\n")
        for f in sorted(rows, key=lambda x: (x["weight"] != "must", x["id"])):
            ru = RULES[f["rule"]]
            L.append(f"- {'MUST' if f['weight'] == 'must' else 'note'} `[F:{f['id']}]` {f['text']} _(source: {ru['source']}; text: {ru.get('text_quality', 'n/a')}; evidence: {ru['status']})_")
    L.append("\n**In the texts but NOT computed for this chart - say so in Part 13**\n")
    for p in pending():
        L.append(f"- {p['what']} _({p['source']})_")
    ex = RULES["excluded"]
    L.append(f"\n**Read and never used, by rule:** {ex['what']} _({ex['source']})_\n")
    return "\n".join(L)


def main(argv=None):
    argv = argv or sys.argv[1:]
    if len(argv) >= 2 and argv[0] == "strip":
        sys.stdout.write(strip(open(argv[1], encoding="utf-8").read())); return 0
    if len(argv) >= 3 and argv[0] == "check":
        fs = json.load(open(argv[1], encoding="utf-8"))["findings"]
        missing, waived, unknown = check(fs, open(argv[2], encoding="utf-8").read())
        must = sum(1 for f in fs if f["weight"] == "must")
        print(f"{must} MUST findings; {must - len(missing)} dealt with ({len(waived)} of them waived); {len(missing)} NOT dealt with.")
        for f in missing: print(f"  MISSING [F:{f['id']}] (Part {f['part']}) {f['text'][:150]}")
        for w, why in waived.items(): print(f"  waived  [F:{w}] - {why}")
        for u in unknown: print(f"  UNKNOWN tag [F:{u}] - no such finding in this worksheet")
        return 1 if missing or unknown else 0
    if len(argv) >= 2 and argv[0] == "list":
        for f in json.load(open(argv[1], encoding="utf-8"))["findings"]: print(f"{f['weight']:4} [F:{f['id']}] {f['text']}")
        return 0
    print(__doc__); return 2


if __name__ == "__main__":
    raise SystemExit(main())
