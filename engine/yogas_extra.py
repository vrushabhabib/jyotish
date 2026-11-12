"""Detection for the catalogued yogas (kb/yogas/yogas.json) that engine.analysis.yogas does not cover.

Every item returned carries the catalogue id, so the worksheet can quote the catalogue's own wording for
strength, cancellation, result and source. `coverage()` reports which catalogue ids are detected where and
which are still not coded. Conditions follow the catalogue text; where the text has variants the stricter
reading is used and the choice is stated in `note`.
"""
from __future__ import annotations
import json, os
from engine.analysis import (View, SEVEN, KENDRA, TRIKONA, DUSTHANA, UPACHAYA, EXALT, DEBIL, OWN,
                             hfrom, sign_at, aspects_sign, kaal_sarp)
from engine.chart import RASHI_LORD

BEN3, MAL3 = ["Mercury", "Jupiter", "Venus"], ["Sun", "Mars", "Saturn"]
CAT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "kb", "yogas", "yogas.json")
KS = {1: "01_ananta", 2: "02_kulika", 3: "03_vasuki", 4: "04_shankhapala", 5: "05_padma", 6: "06_mahapadma",
      7: "07_takshaka", 8: "08_karkotaka", 9: "09_shankhachuda", 10: "10_ghataka", 11: "11_vishadhara", 12: "12_sheshanaga"}
BHAVA = {1: "avayoga", 2: "nisswa", 3: "mriti", 4: "kuhu", 5: "pamara", 7: "dushkriti", 9: "nirbhagya", 10: "duryoga", 11: "daridra_pd"}
# ids already produced by engine.analysis.yogas / doshas (by its own names)
IN_ANALYSIS = {"ruchaka", "bhadra", "hamsa", "malavya", "shasha", "gajakesari", "sunapha", "anapha", "durudhara", "kemadruma",
               "kemadruma_bhanga_1", "kemadruma_bhanga_2", "kemadruma_bhanga_3", "kemadruma_bhanga_5", "kemadruma_bhanga_6",
               "adhi_chandra", "chandra_mangala", "shakata_lunar", "amala", "vesi", "vasi", "ubhayachari", "budha_aditya",
               "lakshmi", "saraswati", "kendra_trikona_raja", "yogakaraka_planet", "dharma_karmadhipati", "harsha", "sarala",
               "vimala", "dhana_lords", "maha_parivartana", "khala_parivartana", "dainya_parivartana", "guru_chandala",
               "angaraka", "shrapit", "vish", "kaal_sarp", "kaal_sarp_partial", "kala_amrita", "mangal_dosha"}
NOT_CODED = {"kemadruma_bhanga_4": "all planets in kendras - covered by the Kamala nabhasa yoga",
             "kemadruma_bhanga_7": "full-Moon condition is contested; tithi is printed in the worksheet",
             "mridanga": "needs a graded strength test for every planet"
             }


def detect(v: View):
    c = v.c
    H = {p: v.house(p) for p in v.s}
    S = v.s
    out = []
    def add(i, planets=(), note=""):
        out.append({"id": i, "planets": list(planets), "note": note})
    L = {h: v.lord(h) for h in range(1, 13)}
    def mutual_kendra(a, b): return hfrom(S[b], S[a]) in KENDRA
    def touched_by(p, q): return q != p and (S[q] == S[p] or aspects_sign(q, S[q], S[p]))

    # ---- Nabhasa (seven planets, BPHS ch. 35)
    hs = {H[p] for p in SEVEN}; sg = {S[p] for p in SEVEN}
    for name, grp in (("rajju", {1, 4, 7, 10}), ("musala", {2, 5, 8, 11}), ("nala", {3, 6, 9, 12})):
        if sg <= grp: add("nabhasa_" + name, SEVEN)
    if {H[p] for p in BEN3} <= KENDRA and len({H[p] for p in BEN3}) == 3: add("nabhasa_mala", BEN3)
    if {H[p] for p in MAL3} <= KENDRA and len({H[p] for p in MAL3}) == 3: add("nabhasa_sarpa", MAL3)
    for pair in ({1, 4}, {4, 7}, {7, 10}, {10, 1}):
        if hs == pair: add("nabhasa_gada", SEVEN, f"houses {sorted(pair)}")
    if hs == {1, 7}: add("nabhasa_shakata", SEVEN)
    if hs == {4, 10}: add("nabhasa_vihaga", SEVEN)
    if hs <= {1, 5, 9} and len(hs) > 1: add("nabhasa_shringataka", SEVEN)
    for tri in ({2, 6, 10}, {3, 7, 11}, {4, 8, 12}):
        if hs <= tri and len(hs) > 1: add("nabhasa_hala", SEVEN, f"houses {sorted(tri)}")
    bh = {H[p] for p in BEN3 + ["Moon"]}; mh = {H[p] for p in MAL3}
    if bh <= {1, 7} and mh <= {4, 10}: add("nabhasa_vajra", SEVEN)
    if mh <= {1, 7} and bh <= {4, 10}: add("nabhasa_yava", SEVEN)
    if hs == KENDRA: add("nabhasa_kamala", SEVEN)
    if hs <= {2, 5, 8, 11} or hs <= {3, 6, 9, 12}: add("nabhasa_vapi", SEVEN)
    for name, span in (("yupa", {1, 2, 3, 4}), ("ishu", {4, 5, 6, 7}), ("shakti", {7, 8, 9, 10}), ("danda", {10, 11, 12, 1})):
        if hs <= span and len(hs) > 2: add("nabhasa_" + name, SEVEN)
    if len(hs) == 7:                                   # strict reading: one planet in each of seven consecutive houses
        for start in range(1, 13):
            if hs == {(start + k - 1) % 12 + 1 for k in range(7)}:
                nm = {1: "nauka", 4: "koota", 7: "chatra", 10: "chapa"}.get(start, "ardha_chandra")
                add("nabhasa_" + nm, SEVEN, f"houses {start} onward, one planet in each")
    if hs <= {1, 3, 5, 7, 9, 11} and len(hs) >= 4: add("nabhasa_chakra", SEVEN, "all in odd houses")
    if hs <= {2, 4, 6, 8, 10, 12} and len(hs) >= 4: add("nabhasa_samudra", SEVEN, "all in even houses")
    add("nabhasa_sankhya_" + ["gola", "yuga", "shoola", "kedara", "pasha", "dama", "veena"][len(sg) - 1], SEVEN,
        f"seven planets in {len(sg)} signs; applies only when no other nabhasa yoga is present")

    # ---- Kaal Sarp by house
    ks = kaal_sarp(v)
    if ks["full"] and ks["type"] and ks["type"].startswith("Rahu"):
        add("kaal_sarp_" + KS[H["Rahu"]], ["Rahu", "Ketu"], f"Rahu in house {H['Rahu']}")

    # ---- house lords in 6/8/12 (Phaladeepika ch. 6)
    for h, i in BHAVA.items():
        if H[L[h]] in DUSTHANA: add(i, [L[h]], f"{h}L {L[h]} in the {H[L[h]]}th")

    # ---- neecha bhanga, condition by condition
    moon = S["Moon"]
    def kend(p): return H[p] in KENDRA or hfrom(S[p], moon) in KENDRA
    for p in SEVEN:
        if S[p] != DEBIL[p]: continue
        disp = RASHI_LORD[S[p] - 1]; exl = RASHI_LORD[EXALT[p] - 1]
        exin = [q for q in SEVEN if EXALT[q] == S[p]]
        if kend(disp): add("neecha_bhanga_1", [p, disp], f"dispositor {disp} in a kendra")
        if kend(exl): add("neecha_bhanga_2", [p, exl], f"lord of {p}'s exaltation sign ({exl}) in a kendra")
        if kend(disp) and kend(exl): add("neecha_bhanga_3", [p, disp, exl], "both in kendras - strongest grade")
        if aspects_sign(disp, S[disp], S[p]): add("neecha_bhanga_4", [p, disp], f"aspected by its dispositor {disp}")
        if exin and kend(exin[0]): add("neecha_bhanga_5", [p, exin[0]], f"{exin[0]} (exalted in this sign) in a kendra")
        if v.exchange(p, disp): add("neecha_bhanga_6", [p, disp], "exchange with dispositor")
        if c["planets"][p]["D9"] == EXALT[p]: add("neecha_bhanga_7", [p], "exalted in navamsa")
        od = [q for q in SEVEN if q != p and S[q] == DEBIL[q] and aspects_sign(q, S[q], S[p])]
        if od: add("neecha_bhanga_8", [p] + od, "aspected by another debilitated planet")
        if disp != exl and mutual_kendra(disp, exl): add("neecha_bhanga_9", [p, disp, exl], "dispositor and exaltation lord in mutual kendras")
        if kend(p): add("neecha_bhanga_10", [p], "itself in a kendra from lagna or Moon")
        if c["planets"][p].get("retrograde"): add("neecha_bhanga_11", [p], "retrograde")

    # ---- poverty combinations (BPHS ch. 42)
    l1 = L[1]
    marakas = {L[2], L[7]} - {l1}
    for hh in (12, 6):                                  # BPHS 42.2-3: the lord sitting in the lagna is the one touched by a maraka lord
        if H[l1] == hh and H[L[hh]] == 1 and any(touched_by(L[hh], m) for m in {L[2], L[7]} - {L[hh]}):
            add("daridra_1", [l1, L[hh]], f"lagna lord in the {hh}th, {hh}th lord in the lagna touched by a maraka lord")
    if (H["Ketu"] == 1 or S["Ketu"] == moon) and H[l1] == 8: add("daridra_2", [l1, "Ketu"])
    ben_asp = any(touched_by(l1, b) for b in BEN3 if b != l1)
    if H[l1] in DUSTHANA and any(S[m] == S[l1] for m in MAL3 + ["Rahu", "Ketu"] if m != l1) and L[2] in DEBIL and S[L[2]] == DEBIL[L[2]]:
        add("daridra_3", [l1, L[2]], "BPHS 42.5: lagna lord with a malefic in a dusthana, 2nd lord debilitated (enemy sign not tested)")
    elif not ben_asp and any(S[q] == S[l1] for q in {L[6], L[8], L[12], "Saturn"} if q != l1):
        add("daridra_3", [l1], "BPHS 42.6: lagna lord with a dusthana lord or Saturn, no benefic aspect")
    if H[L[5]] == 6 and H[L[9]] == 12 and all(any(touched_by(q, m) for m in {L[2], L[7]} - {q}) for q in (L[5], L[9])):
        add("daridra_4", [L[5], L[9]], "BPHS 42.7: both touched by maraka lords")
    if all(H[b] in DUSTHANA for b in BEN3) and all(H[m] in KENDRA | TRIKONA for m in MAL3): add("daridra_5", BEN3 + MAL3)
    if H["Mars"] == 2 and H["Saturn"] == 2 and not aspects_sign("Mercury", S["Mercury"], S["Mars"]): add("daridra_6", ["Mars", "Saturn"])

    # ---- named yogas
    if all(H[b] in (7, 8) for b in BEN3) and not any(S[m] in {S[b] for b in BEN3} for m in MAL3 + ["Rahu", "Ketu"]):
        add("lagnadhi", BEN3, "BPHS 36.37: benefics in the 7th and 8th from the lagna, free of malefics")
    if all(hfrom(S[b], moon) in UPACHAYA for b in BEN3): add("vasumati", BEN3, "from the Moon")
    elif all(H[b] in UPACHAYA for b in BEN3): add("vasumati", BEN3, "from the lagna (Raman variant)")
    d = hfrom(moon, S["Sun"])
    add("chandra_sun_distance", ["Sun", "Moon"], "Moon in " + ("a kendra from the Sun: low grade" if d in KENDRA else
        "panaphara from the Sun: middle grade" if d in (2, 5, 8, 11) else "apoklima from the Sun: high grade"))
    B4 = BEN3 + ["Moon"]; M5 = MAL3 + ["Rahu", "Ketu"]
    if any(H[b] == 2 for b in B4) and any(H[b] == 12 for b in B4) and not any(H[m] in (2, 12) for m in M5):
        add("shubha_kartari_lagna", [b for b in B4 if H[b] in (2, 12)], "benefics on both sides of the lagna")
    if any(H[m] == 2 for m in M5) and any(H[m] == 12 for m in M5):
        add("ashubha_papa_kartari", [m for m in M5 if H[m] in (2, 12)], "malefics on both sides of the lagna")
    if any(H[b] in KENDRA for b in BEN3) and not any(H[m] in (7, 8) for m in M5):          # BPHS 36.7-8
        add("parvata", [b for b in BEN3 if H[b] in KENDRA], "benefics in kendras, 7th and 8th free of malefics")
    elif l1 != L[12] and mutual_kendra(l1, L[12]): add("parvata", [l1, L[12]], "Raman variant: 1L and 12L in mutual kendras")
    if (L[4] != "Jupiter" and mutual_kendra(L[4], "Jupiter") and v.strong(l1)) or (v.strong(L[4]) and L[4] != L[10] and S[L[4]] == S[L[10]]):
        add("kahala", [L[4], "Jupiter"])
    two_ben = [h for h in (1, 7, 9, 10) if sum(1 for b in BEN3 if H[b] == h) >= 2]
    if (l1 in EXALT and S[l1] == EXALT[l1] and H[l1] in KENDRA and aspects_sign("Jupiter", S["Jupiter"], S[l1])) or two_ben:
        add("chamara", [l1], "two benefics together in house " + str(two_ben[0]) if two_ben else "lagna lord exalted in a kendra, aspected by Jupiter")
    if (v.strong(l1) and L[5] != L[6] and mutual_kendra(L[5], L[6])) or (S[l1] in (1, 4, 7, 10) and S[L[10]] in (1, 4, 7, 10) and v.strong(L[9])):
        add("shankha", [l1, L[5], L[6]])
    if v.strong(L[9]) and all(H[p] in KENDRA for p in ("Venus", "Jupiter", l1)):
        add("bheri", ["Venus", "Jupiter", l1], "BPHS 36.16: Venus, Jupiter and lagna lord in kendras, 9th lord strong")
    elif v.strong(L[9]) and all(any(H[p] == h for p in v.s) for h in (12, 1, 2, 7)):
        add("bheri", [L[9]], "BPHS 36.15: houses 12, 1, 2 and 7 occupied, 9th lord strong")
    if H[L[7]] == 10 and L[7] in EXALT and S[L[7]] == EXALT[L[7]] and L[10] != L[9] and S[L[10]] == S[L[9]]:
        add("shrinatha", [L[7], L[10], L[9]], "BPHS 36.18: 7th lord exalted in the 10th, 10th lord with the 9th lord")
    if (H[L[10]] == 5 and H["Mercury"] in KENDRA and S["Sun"] == 5) or \
       (any(hfrom(S[p], moon) in (5, 9) for p in ("Jupiter", "Mercury")) and H["Mars"] == 11):
        add("sharada", ["Mercury", "Jupiter", "Mars"])
    occ = lambda h: [p for p in SEVEN if H[p] == h]
    if any(H[b] == 1 for b in B4) and any(H[b] == 9 for b in B4) and occ(5) and any(H[m] == 4 for m in MAL3) and any(H[m] == 8 for m in MAL3):
        add("matsya", SEVEN)
    if {H[b] for b in BEN3} <= {5, 6, 7} and {H[m] for m in MAL3} <= {1, 3, 11}: add("kurma", SEVEN, "placement only; dignity not tested")
    if L[2] != L[9] and H[L[2]] == 9 and H[L[9]] == 2 and H[l1] in KENDRA | TRIKONA: add("khadga", [L[2], L[9]])
    if v.lag in (2, 5, 8, 11) and H["Venus"] in KENDRA and H["Moon"] in (5, 9) and any(S[b] == moon for b in BEN3) and H["Saturn"] == 10:
        add("kusuma", ["Venus", "Moon", "Saturn"])
    if H["Jupiter"] in (2, 5) and ((touched_by("Jupiter", "Mercury") and touched_by("Jupiter", "Venus")) or S["Jupiter"] in (2, 3, 6, 7)):
        add("kalanidhi", ["Jupiter", "Mercury", "Venus"], "BPHS 36.31: Jupiter in the 2nd or 5th with Mercury and Venus, or in their signs")
    for i, ref, need in (("hari", S[L[2]], {2, 8, 12}), ("hara", S[L[7]], {4, 8, 9}), ("brahma", S[l1], {4, 10, 11})):
        if {hfrom(S[b], ref) for b in BEN3} == need: add(i, BEN3, "one benefic in each of the three houses")
    for n in ("Rahu", "Ketu"):
        tl = {L[5], L[9]}; kl = {L[4], L[7], L[10]}
        if (H[n] in KENDRA and any(touched_by(n, q) for q in tl)) or (H[n] in (5, 9) and any(touched_by(n, q) for q in kl)):
            add("node_yogakaraka", [n], f"{n} in house {H[n]}")
    if l1 != L[5] and v.exchange(l1, L[5]): add("maha_raja", [l1, L[5]], "1L and 5L exchange")
    if l1 != L[10] and H[l1] == 10 and H[L[10]] == 1: add("lagna_karma_exchange", [l1, L[10]])
    ex = [p for p in SEVEN if S[p] == EXALT[p]]
    if len(ex) >= 2: add("exalted_count", ex, f"{len(ex)} planets exalted")
    if all(H[b] in KENDRA for b in BEN3) and all(H[m] in (3, 6, 11) for m in MAL3): add("benefic_kendra_malefic_upachaya", SEVEN)
    if c["planets"]["Moon"]["D9"] == moon and len(v.aspected_by("Moon", nodes=False)) >= 4: add("moon_vargottama_aspected", ["Moon"])
    if "Jupiter" in (L[2], L[5], L[11]) and any(hfrom(S[L[h]], moon) in KENDRA for h in (2, 9, 11)):
        add("akhanda_samrajya", ["Jupiter"], "Raman additionally requires the kendra lord to be strong")
    if hfrom(S["Venus"], moon) in (3, 11): add("venus_moon_3_11", ["Moon", "Venus"])
    if all(L[h] in EXALT and (S[L[h]] == DEBIL[L[h]] or c["planets"][L[h]].get("combust")) for h in (6, 8, 12)) and v.strong(l1) and \
       (H[l1] == 1 or aspects_sign(l1, S[l1], v.lag)):
        add("viparita_bphs", [L[6], L[8], L[12]])
    pair = {"Venus": ["Mars"], "Mercury": ["Moon", "Mars", "Jupiter"], "Sun": ["Saturn", "Moon", "Jupiter"], "Saturn": ["Sun", "Moon"],
            "Jupiter": ["Mercury"], "Mars": ["Venus"], "Moon": ["Saturn"]}
    if H[L[5]] == 5 and all(H[q] == 11 for q in pair[L[5]]): add("dhana_5_11", [L[5]] + pair[L[5]], "BPHS 41.2-8: all the named planets in the 11th")
    pl = {"Sun": ["Mars", "Jupiter"], "Moon": ["Mercury", "Jupiter"], "Mars": ["Mercury", "Venus", "Saturn"], "Mercury": ["Saturn", "Jupiter"],
          "Jupiter": ["Mercury", "Mars"], "Venus": ["Saturn", "Mercury"], "Saturn": ["Mars", "Jupiter"]}
    if H[l1] == 1 and all(touched_by(l1, q) for q in pl[l1]): add("dhana_lagna_own", [l1] + pl[l1])
    for b in ("Moon", "Jupiter", "Venus", "Mercury"):
        if H[b] == 2 and S[b] == EXALT[b]: add("dhana_benefic_2nd", [b])
    k = l1
    chain = [k]
    for _ in range(2):
        k = RASHI_LORD[S[k] - 1]; chain.append(k)
    chain.append(RASHI_LORD[c["planets"][k]["D9"] - 1])
    if all(H[p] in KENDRA | TRIKONA or S[p] == EXALT.get(p) for p in chain):
        add("kalpadruma", sorted(set(chain)), "BPHS 36.33: each of the four in a kendra, a trine or its exaltation")

    # ---- afflictions
    mal7 = [m for m in M5 if H[m] == 7]
    k7 = []
    if mal7 and not any(aspects_sign(b, S[b], sign_at(v.lag, 7)) for b in BEN3): k7.append(f"{', '.join(mal7)} in the 7th without benefic aspect")
    if H[L[7]] in DUSTHANA: k7.append(f"7L {L[7]} in the {H[L[7]]}th")
    if S[L[7]] == DEBIL.get(L[7]) or c["planets"][L[7]].get("combust"): k7.append(f"7L {L[7]} debilitated or combust")
    if c["planets"]["Venus"].get("combust"): k7.append("Venus combust")
    if k7: add("kalatra_dosha", [L[7], "Venus"], "; ".join(k7))
    # --- BPHS ch. 83 (curses shown by childlessness), translated from the Sanskrit on 12 Nov 2026
    lag_occ = [p for p in v.s if H[p] == 1]
    weak = lambda p: not v.strong(p) and (S[p] == DEBIL.get(p) or H[p] in DUSTHANA or c["planets"][p].get("combust"))
    ss = []
    if H["Rahu"] == 5 and (aspects_sign("Mars", S["Mars"], S["Rahu"]) or S["Rahu"] in (1, 8)):
        ss.append("83.9: Rahu in the 5th aspected by Mars or in Mars's sign")
    if S[L[5]] == S["Rahu"] and H["Saturn"] == 5 and touched_by("Saturn", "Moon"):
        ss.append("83.10: 5th lord with Rahu, Saturn in the 5th joined or aspected by the Moon")
    if S["Jupiter"] == S["Rahu"] and weak(L[5]) and l1 != "Mars" and S[l1] == S["Mars"]:
        ss.append("83.11: Jupiter with Rahu, 5th lord weak, lagna lord with Mars")
    if S["Jupiter"] == S["Mars"] and H["Rahu"] == 1 and H[L[5]] in DUSTHANA:
        ss.append("83.12: Jupiter with Mars, Rahu in the lagna, 5th lord in a dusthana")
    if ss: add("sarpa_shapa", ["Rahu", L[5]], "; ".join(ss))
    ps = []
    mal_in = lambda h: [m for m in M5 if H[m] == h]
    if H["Sun"] == 5 and S["Sun"] == 7 and c["planets"]["Sun"]["D9"] in (10, 11) and mal_in(4) and mal_in(6):
        ps.append("83.20: Sun debilitated in the 5th in Saturn's navamsa, malefics on both sides")
    if L[5] == "Sun" and H["Sun"] in (5, 9) and any(S[m] == S["Sun"] for m in M5 if m != "Sun") and \
       mal_in((H["Sun"] - 2) % 12 + 1) and mal_in(H["Sun"] % 12 + 1):
        ps.append("83.21: Sun as 5th lord in a trine with a malefic and between malefics")
    if S["Jupiter"] == 5 and L[5] != "Sun" and S[L[5]] == S["Sun"] and mal_in(5) and mal_in(1):
        ps.append("83.22: Jupiter in Leo, 5th lord with the Sun, malefics in the 5th and the lagna")
    if H[l1] == 5 and weak(l1) and L[5] != "Sun" and S[L[5]] == S["Sun"] and mal_in(5) and mal_in(1):
        ps.append("83.23: weak lagna lord in the 5th, 5th lord with the Sun, malefics in the 5th and the lagna")
    if {H["Sun"], H["Mars"], H["Saturn"]} <= {1, 5} and {H["Rahu"], H["Jupiter"]} <= {8, 12}:
        ps.append("83.27: Sun, Mars, Saturn in the lagna and 5th; Rahu and Jupiter in the 8th and 12th")
    if ps: add("pitru_dosha", ["Sun", L[5]], "Parashara's father's-curse combination - " + "; ".join(ps))
    # --- BPHS 92.1-5 gandanta, widths from the text: nakshatra junction four nadis (taken as 2 ghatis each side of the
    # junction = about 0d27' of Moon; the looser reading of 4 each side = 0d53' is reported as 'near'); lagna one ghati
    # (taken as half a ghati = 3 degrees each side); Abhukta Mula = last 5 ghatis of Jyeshtha and first 8 of Mula.
    xm = v.lon["Moon"] % 120.0; dm = min(xm, 120.0 - xm)
    if dm <= 2 * 13.3333 / 60: add("gandanta_birth", ["Moon"], f"Moon {dm * 60:.0f}' from a water-fire junction (BPHS 92.3: within two ghatis)")
    elif dm <= 4 * 13.3333 / 60: add("gandanta_birth", ["Moon"], f"Moon {dm * 60:.0f}' from a junction - near; inside only on the looser reading of four ghatis each side")
    ml = v.lon["Moon"]
    if 240 - 5 * 13.3333 / 60 <= ml < 240 + 8 * 13.3333 / 60:
        add("gandanta_birth", ["Moon"], "Abhukta Mula (BPHS 92.5: last 5 ghatis of Jyeshtha, first 8 of Mula)")
    xl = c["lagna"]["lon"] % 120.0; dl = min(xl, 120.0 - xl)
    if dl <= 3.0: add("gandanta_birth", [], f"Lagna {dl:.1f} deg from a water-fire sign junction (BPHS 92.4: within about half a ghati)")
    # --- BPHS 91.1: birth during a solar or lunar eclipse (approximate test: syzygy within 1 degree and the Sun close to a node)
    el0 = (v.lon["Moon"] - v.lon["Sun"]) % 360.0
    nd = min((v.lon["Sun"] - v.lon["Rahu"]) % 180.0, 180.0 - (v.lon["Sun"] - v.lon["Rahu"]) % 180.0)
    if (min(el0, 360 - el0) < 1.0 and nd < 15.0) or (abs(el0 - 180.0) < 1.0 and nd < 10.0):
        add("grahan", ["Sun", "Moon", "Rahu"], "birth at or very near an eclipse (BPHS 91.1) - confirm against an eclipse table")
    # --- BPHS 79.7-8: Saturn's renunciation
    msl = RASHI_LORD[moon - 1]
    onlysat = [q for q in SEVEN if q != msl and touched_by(msl, q)]
    if msl != "Saturn" and weak(msl) and onlysat == ["Saturn"]:
        add("pravrajya_moon_saturn", [msl, "Saturn"], "79.7: weak lord of the Moon's sign aspected by Saturn alone")
    d3, d9 = c["planets"]["Moon"].get("D3"), c["planets"]["Moon"]["D9"]
    if d3 in (10, 11) and d9 in (10, 11, 1, 8) and aspects_sign("Saturn", S["Saturn"], moon):
        add("pravrajya_moon_saturn", ["Moon", "Saturn"], "79.8: Moon in Saturn's drekkana and a navamsa of Saturn or Mars, aspected by Saturn")
    el = (v.lon["Moon"] - v.lon["Sun"]) % 360.0
    if el >= 336: add("amavasya_birth", ["Sun", "Moon"], "new-moon tithi" if el >= 348 else "14th tithi of the dark half")
    if H["Moon"] in DUSTHANA and any(aspects_sign(m, S[m], moon) for m in ("Mars", "Saturn", "Rahu", "Ketu")) and \
       not any(touched_by("Moon", b) for b in BEN3):
        add("balarishta", ["Moon"], f"Moon in the {H['Moon']}th, malefic aspect, no benefic help (infancy indication only)")
    for s in set(S[p] for p in SEVEN):
        grp = [p for p in SEVEN if S[p] == s]
        if len(grp) >= 4: add("pravrajya_4", grp, f"{len(grp)} planets in one sign; strength of each not tested")
    sat = lambda t: aspects_sign("Saturn", S["Saturn"], t)
    if (H["Jupiter"] == 9 and sat(v.lag) and sat(moon) and sat(S["Jupiter"])) or (H["Saturn"] == 9 and not v.aspected_by("Saturn")):
        add("pravrajya_jupiter_9", ["Jupiter", "Saturn"])
    if H["Ketu"] == 12: add("sanyasa_ketu_12", ["Ketu"], "from the lagna")
    return out


_cat = None
def catalogue():
    global _cat
    if _cat is None:
        _cat = {x["id"]: x for x in json.load(open(CAT))}
    return _cat


def coverage():
    ids = set(catalogue())
    import inspect, re
    coded = set(re.findall(r'add\("([a-z0-9_]+)"', inspect.getsource(detect)))
    coded |= {"nabhasa_" + n for n in ("rajju", "musala", "nala", "yupa", "ishu", "shakti", "danda", "nauka", "koota", "chatra", "chapa", "ardha_chandra")}
    coded |= {"nabhasa_sankhya_" + n for n in ("gola", "yuga", "shoola", "kedara", "pasha", "dama", "veena")}
    coded |= {"kaal_sarp_" + n for n in KS.values()} | set(BHAVA.values()) | {"hari", "hara", "brahma"}
    return {"catalogue": len(ids), "in_analysis": sorted(ids & IN_ANALYSIS), "in_yogas_extra": sorted(ids & coded - IN_ANALYSIS),
            "not_coded": {i: NOT_CODED.get(i, "no reason recorded") for i in sorted(ids - coded - IN_ANALYSIS)}}


if __name__ == "__main__":
    cv = coverage()
    print(cv["catalogue"], "catalogued;", len(cv["in_analysis"]), "in analysis;", len(cv["in_yogas_extra"]), "here; not coded:", cv["not_coded"])


HUSBAND_BY_7TH = {"Mars": "fond of women, quick-tempered", "Mercury": "learned, skilled in arts, intelligent",
                  "Jupiter": "all good qualities, self-controlled", "Venus": "fortunate, handsome, well liked by women",
                  "Saturn": "old and dull", "Sun": "very gentle, hard-working", "Moon": "attractive, amorous, soft"}


def husband_by_seventh(v: View):
    """BPHS 80.22-25 (female charts): the husband described by the sign on the 7th house and by its navamsa.
    Low confidence; descriptions of other people are the project's weakest category."""
    seventh = sign_at(v.lag, 7)
    lon7 = (v.c["lagna"]["lon"] + 180.0) % 360.0
    s = int(lon7 // 30); part = int((lon7 % 30) // (30 / 9))
    start = s if s % 3 == 0 else (s + 8) % 12 if s % 3 == 1 else (s + 4) % 12
    nav = (start + part) % 12 + 1
    ls, ln = RASHI_LORD[seventh - 1], RASHI_LORD[nav - 1]
    return {"seventh_sign_lord": ls, "by_sign": HUSBAND_BY_7TH[ls], "navamsa_lord": ln, "by_navamsa": HUSBAND_BY_7TH[ln],
            "source": "BPHS 80.22-25; birth-time sensitive (the navamsa of the 7th changes about every 13 minutes)"}

