"""Everything a reading needs that is derived from the basic chart.

analyse(chart, sex=None) takes the dict from engine.chart.build_chart and adds, without any
interpretation prose:

  panchanga      tithi, paksha, vara (sunrise-based), yoga, karana
  houses         per house: sign, lord, where the lord sits, occupants, every graha aspecting it,
                 planets with / aspecting the lord; the same counted from the Moon and from the Sun
  functional     per planet: houses owned, functional nature for this lagna, yogakaraka, maraka, badhaka
  states         per planet: baladi avastha, sandhi, gandanta, vargottama, combust, retrograde, graha yuddha
  karakas        Jaimini chara karakas (7-karaka scheme, and the 8-karaka scheme with Rahu)
  arudhas        A1..A12 (AL, A7 Darapada, A10, UL = A12 ...), karakamsa
  yogas          list of detected yogas with the planets involved and what weakens each
  doshas         Manglik with every cancellation that applies, Kaal Sarp, Grahan, Guru-Chandala, ...
  points         Beeja / Kshetra sphuta, Indu lagna, Bhrigu bindu
  kp             star / sub / sub-sub lords for planets and the four angles (KP ayanamsa)
  dasha          Vimshottari to three levels + helper dasha_at(date)

Rule sources are cited beside each block. Functions are pure and cheap; nothing here reads the network.
"""
from __future__ import annotations
import datetime as dt
from engine.chart import (RAS, NAK, NAK_LIST, RASHI_NAMES, RASHI_EN, RASHI_LORD, PLANET_ORDER,
                          varga_rashi, rashi_of, deg_in_rashi, nakshatra_of, dignity)
from engine import ephemeris as E

SEVEN = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
NAT_BENEFIC = {"Jupiter", "Venus", "Mercury", "Moon"}
NAT_MALEFIC = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}
KENDRA, TRIKONA, DUSTHANA, UPACHAYA = {1, 4, 7, 10}, {1, 5, 9}, {6, 8, 12}, {3, 6, 10, 11}
# Graha drishti (BPHS ch. 26): all aspect the 7th; Mars 4/8, Jupiter 5/9, Saturn 3/10.
# Rahu/Ketu 5/7/9 is a later convention (not in every BPHS recension) - reported separately as "nodal".
ASPECTS = {"Sun": [7], "Moon": [7], "Mercury": [7], "Venus": [7], "Mars": [4, 7, 8],
           "Jupiter": [5, 7, 9], "Saturn": [3, 7, 10], "Rahu": [5, 7, 9], "Ketu": [5, 7, 9]}
EXALT = {p: RAS["planets"][p]["exalt"]["rashi"] for p in SEVEN}
DEBIL = {p: RAS["planets"][p]["debil"]["rashi"] for p in SEVEN}
OWN = {p: RAS["planets"][p]["own"] for p in SEVEN}


def hfrom(sign, ref):            # house number of `sign` counted from `ref` (both 1..12)
    return (sign - ref) % 12 + 1


def sign_at(ref, house):         # sign that is `house` houses from `ref`
    return (ref - 1 + house - 1) % 12 + 1


def aspects_sign(planet, psign, target):
    return hfrom(target, psign) in ASPECTS[planet]


class View:
    """Convenience accessors over a chart dict."""
    def __init__(self, chart):
        self.c = chart
        self.lag = chart["lagna"]["rashi"]
        self.s = {p: chart["planets"][p]["rashi"] for p in PLANET_ORDER}
        self.lon = {p: chart["planets"][p]["lon"] for p in PLANET_ORDER}

    def house(self, p, ref=None):
        return hfrom(self.s[p], ref or self.lag)

    def lord(self, h, ref=None):
        return RASHI_LORD[sign_at(ref or self.lag, h) - 1]

    def owns(self, p, ref=None):
        return [h for h in range(1, 13) if self.lord(h, ref) == p]

    def occupants(self, sign):
        return [p for p in PLANET_ORDER if self.s[p] == sign]

    def aspecting(self, sign, nodes=True):
        return [p for p in PLANET_ORDER if (nodes or p not in ("Rahu", "Ketu"))
                and aspects_sign(p, self.s[p], sign)]

    def conj(self, p):
        return [q for q in PLANET_ORDER if q != p and self.s[q] == self.s[p]]

    def aspected_by(self, p, nodes=True):
        return [q for q in self.aspecting(self.s[p], nodes) if q != p]

    def mutual_aspect(self, a, b):
        return aspects_sign(a, self.s[a], self.s[b]) and aspects_sign(b, self.s[b], self.s[a])

    def exchange(self, a, b):
        return a != b and RASHI_LORD[self.s[a] - 1] == b and RASHI_LORD[self.s[b] - 1] == a

    def linked(self, a, b):
        """Parashari sambandha between two planets: conjunction, mutual aspect or exchange."""
        return a != b and (self.s[a] == self.s[b] or self.mutual_aspect(a, b) or self.exchange(a, b))

    def strong(self, p):
        return p in SEVEN and (self.s[p] == EXALT[p] or self.s[p] in OWN[p])

    def sambandha(self, p, houses=(), karakas=(), nodes=True):
        """Does planet p connect to any of these houses / their lords / these karakas?
        Returns the list of concrete links (empty = no link). See kb/dashas/antar-event-rules.md Rule 1."""
        out = []
        for h in houses:
            sg = sign_at(self.lag, h); L = self.lord(h)
            if self.s[p] == sg: out.append(f"occupies {h}")
            if p == L: out.append(f"owns {h}")
            elif L in self.conj(p): out.append(f"with {h}L {L}")
            if (nodes or p not in ("Rahu", "Ketu")) and aspects_sign(p, self.s[p], sg): out.append(f"aspects {h}")
            if p != L and aspects_sign(p, self.s[p], self.s[L]): out.append(f"aspects {h}L {L}")
            if p in SEVEN and p != L and RASHI_LORD[self.s[L] - 1] == p: out.append(f"disposes {h}L {L}")
        for k in karakas:
            if p == k: out.append(f"is karaka {k}")
            elif self.s[p] == self.s[k]: out.append(f"with karaka {k}")
            elif aspects_sign(p, self.s[p], self.s[k]): out.append(f"aspects karaka {k}")
            elif p in SEVEN and RASHI_LORD[self.s[k] - 1] == p: out.append(f"disposes karaka {k}")
        return out


# --------------------------------------------------------------------------- panchanga
TITHI = ["Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi", "Saptami", "Ashtami", "Navami",
         "Dashami", "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi"]
YOGA = ["Vishkumbha", "Priti", "Ayushman", "Saubhagya", "Shobhana", "Atiganda", "Sukarma", "Dhriti", "Shula", "Ganda",
        "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra", "Siddhi", "Vyatipata", "Variyana", "Parigha", "Shiva",
        "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma", "Indra", "Vaidhriti"]
KARANA_MOV = ["Bava", "Balava", "Kaulava", "Taitila", "Gara", "Vanija", "Vishti"]
VARA = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
VARA_LORD = {"Sunday": "Sun", "Monday": "Moon", "Tuesday": "Mars", "Wednesday": "Mercury",
             "Thursday": "Jupiter", "Friday": "Venus", "Saturday": "Saturn"}


def panchanga(chart):
    sun, moon = chart["planets"]["Sun"]["lon"], chart["planets"]["Moon"]["lon"]
    el = (moon - sun) % 360
    t = int(el // 12)                         # 0..29
    paksha = "Shukla" if t < 15 else "Krishna"
    name = "Purnima" if t == 14 else "Amavasya" if t == 29 else TITHI[t % 15]
    k = int(el // 6)                          # 0..59 half-tithis
    if k == 0: karana = "Kimstughna"
    elif k >= 57: karana = ["Shakuni", "Chatushpada", "Naga"][k - 57]
    else: karana = KARANA_MOV[(k - 1) % 7]
    yoga = YOGA[int(((sun + moon) % 360) // (360 / 27))]
    inp = chart["input"]
    local = inp["local"]
    jd = inp["jd_ut"]
    sunrise, sunset = E.sun_times(jd, inp["lat"], inp["lon"])
    civil = local.date()
    vedic_day = civil - dt.timedelta(days=1) if jd < sunrise else civil     # Vedic day runs sunrise to sunrise
    vara = VARA[vedic_day.weekday()]
    off = local.utcoffset() or dt.timedelta(0)
    fmt = lambda j: (E.jd_to_datetime(j) + off).strftime("%H:%M:%S")
    return {"tithi_no": t + 1, "tithi": f"{paksha} {name}", "paksha": paksha, "moon_phase_deg": round(el, 2),
            "vara": vara, "vara_lord": VARA_LORD[vara], "yoga": yoga, "karana": karana,
            "sunrise": fmt(sunrise), "sunset": fmt(sunset), "day_birth": sunrise <= jd < sunset,
            "nakshatra": chart["janma_nakshatra"], "pada": chart["planets"]["Moon"]["pada"]}


# --------------------------------------------------------------------------- houses
def house_table(v: View, ref=None):
    ref = ref or v.lag
    out = {}
    for h in range(1, 13):
        sg = sign_at(ref, h); L = RASHI_LORD[sg - 1]
        asp = v.aspecting(sg)
        out[h] = {"sign": RASHI_NAMES[sg - 1], "sign_en": RASHI_EN[sg - 1], "lord": L,
                  "lord_house": hfrom(v.s[L], ref), "lord_sign": RASHI_NAMES[v.s[L] - 1],
                  "lord_dignity": v.c["planets"][L]["dignity"],
                  "occupants": v.occupants(sg),
                  "aspected_by": [p for p in asp if p not in ("Rahu", "Ketu")],
                  "aspected_by_nodes": [p for p in asp if p in ("Rahu", "Ketu")],
                  "lord_with": v.conj(L), "lord_aspected_by": v.aspected_by(L),
                  "malefic_hits": sum(1 for p in set(v.occupants(sg)) | set(asp) if p in NAT_MALEFIC),
                  "benefic_hits": sum(1 for p in set(v.occupants(sg)) | set(asp) if p in ("Jupiter", "Venus", "Mercury"))}
    return out


def functional(v: View):
    """Functional nature per BPHS ch. 34 (Yogakarakadhyaya): trikona lords auspicious; 3/6/11 lords
    inauspicious; kendra lords neutralise (benefics lose, malefics lose); 2nd/12th lords follow their
    other house and company; 8th lord inauspicious (the blemish is waived for the lagna lord and,
    by the usual reading, for Sun and Moon)."""
    quality = (v.lag - 1) % 3                       # 0 movable, 1 fixed, 2 dual
    badhaka_house = {0: 11, 1: 9, 2: 7}[quality]
    out = {}
    for p in SEVEN:
        owns = v.owns(p)
        tri = [h for h in owns if h in (5, 9)]
        ken = [h for h in owns if h in (4, 7, 10)]
        score, notes = 0, []
        if 1 in owns: score += 2; notes.append("lagna lord")
        if tri: score += 2; notes.append("trikona lord")
        if any(h in (3, 6, 11) for h in owns): score -= 2; notes.append("3/6/11 lord")
        if 8 in owns and 1 not in owns and p not in ("Sun", "Moon"): score -= 2; notes.append("8th lord")
        if ken and not tri and 1 not in owns:
            notes.append("kendra lord: natural benefic loses benefit (kendradhipati)" if p in NAT_BENEFIC
                         else "kendra lord: natural malefic loses malice")
        yk = bool(tri and ken)
        if yk: score += 2; notes.append("YOGAKARAKA (kendra + trikona)")
        nature = "benefic" if score >= 2 else "malefic" if score <= -2 else "mixed/neutral"
        out[p] = {"owns": owns, "nature": nature, "yogakaraka": yk,
                  "maraka": [h for h in owns if h in (2, 7)], "badhaka": badhaka_house in owns, "notes": notes}
    return {"planets": out, "badhaka_house": badhaka_house}


# --------------------------------------------------------------------------- planet states
def baladi(sign, deg):
    """Baladi avastha, BPHS ch. 45: odd signs infant/youth/adolescent(full)/old/dead per 6 degrees; even reversed."""
    names = ["Bala (infant, 1/4)", "Kumara (youth, 1/2)", "Yuva (prime, full)", "Vriddha (old, minimal)", "Mrita (dead, nil)"]
    i = min(int(deg // 6), 4)
    return names[i] if sign % 2 == 1 else names[4 - i]


def states(v: View):
    out = {}
    for p in PLANET_ORDER:
        d = v.c["planets"][p]
        sg, deg = d["rashi"], d["deg"]
        st = {"dignity": d["dignity"], "retrograde": d.get("retrograde", False), "combust": d.get("combust", False),
              "baladi": baladi(sg, deg) if p in SEVEN else None,
              "vargottama": d["D9"] == sg,
              "sandhi": deg < 1 or deg > 29,
              "gandanta": (sg in (4, 8, 12) and deg >= 30 - 10 / 3) or (sg in (1, 5, 9) and deg <= 10 / 3),
              "d9_dignity": dignity(p, (d["D9"] - 1) * 30 + 15).replace(" (deep)", "") if p in SEVEN else None,
              "dispositor": RASHI_LORD[sg - 1], "nak_lord": d["nak_lord"]}
        out[p] = st
    five = ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    wars = []
    for i, a in enumerate(five):
        for b in five[i + 1:]:
            if abs((v.lon[a] - v.lon[b] + 180) % 360 - 180) < 1:
                wars.append((a, b))
    return out, wars


# --------------------------------------------------------------------------- Jaimini
def chara_karakas(v: View):
    """Jaimini chara karakas by degree within sign. 7-karaka scheme (Sun..Saturn), the one K.N. Rao
    uses; the 8-karaka scheme adds Rahu counted backwards (30 - degree) and inserts Pitrikaraka."""
    deg = {p: v.lon[p] % 30 for p in SEVEN}
    seven = sorted(SEVEN, key=lambda p: -deg[p])
    deg8 = dict(deg); deg8["Rahu"] = 30 - v.lon["Rahu"] % 30
    eight = sorted(deg8, key=lambda p: -deg8[p])
    return {"seven": dict(zip(["AK", "AmK", "BK", "MK", "PK", "GK", "DK"], seven)),
            "eight": dict(zip(["AK", "AmK", "BK", "MK", "PiK", "PK", "GK", "DK"], eight))}


def arudha(v: View, h):
    """Arudha pada: count from the house to its lord, then the same again from the lord.
    Exception (BPHS ch. 29): if the result is the house itself or its 7th, take the 10th from it."""
    sg = sign_at(v.lag, h); L = RASHI_LORD[sg - 1]
    a = sign_at(v.s[L], hfrom(v.s[L], sg))
    if hfrom(a, sg) in (1, 7):
        a = sign_at(a, 10)
    return a


def arudhas(v: View):
    out = {}
    for h in range(1, 13):
        a = arudha(v, h)
        out[f"A{h}"] = {"sign": RASHI_NAMES[a - 1], "house": hfrom(a, v.lag), "occupants": v.occupants(a)}
    out["AL"], out["UL"] = out["A1"], out["A12"]
    ul = arudha(v, 12)
    out["UL_2nd"] = {"sign": RASHI_NAMES[sign_at(ul, 2) - 1], "occupants": v.occupants(sign_at(ul, 2)),
                     "aspected_by": v.aspecting(sign_at(ul, 2)), "lord": RASHI_LORD[sign_at(ul, 2) - 1]}
    out["UL_8th"] = {"sign": RASHI_NAMES[sign_at(ul, 8) - 1], "occupants": v.occupants(sign_at(ul, 8))}
    return out


# --------------------------------------------------------------------------- yogas
def yogas(v: View):
    Y = []
    def add(name, cat, planets, note="", weak=""):
        Y.append({"name": name, "category": cat, "planets": planets, "note": note, "weakened_by": weak})
    moon = v.s["Moon"]
    def flaws(p):
        d = v.c["planets"][p]; f = []
        if d.get("combust"): f.append("combust")
        if v.s[p] in (v.s["Rahu"], v.s["Ketu"]): f.append("on the Rahu-Ketu axis")
        if v.house(p) in DUSTHANA: f.append(f"in the {v.house(p)}th")
        if p in SEVEN and v.s[p] == DEBIL[p]: f.append("debilitated")
        return ", ".join(f)

    # Pancha Mahapurusha (BPHS ch. 75): own/exalted sign in a kendra from the lagna. From the Moon = weaker variant.
    for p, nm in [("Mars", "Ruchaka"), ("Mercury", "Bhadra"), ("Jupiter", "Hamsa"), ("Venus", "Malavya"), ("Saturn", "Shasha")]:
        if v.strong(p):
            if v.house(p) in KENDRA:
                add(f"{nm} (Mahapurusha)", "mahapurusha", [p], f"{p} own/exalted in house {v.house(p)}", flaws(p))
            elif v.house(p, moon) in KENDRA:
                add(f"{nm} from Moon only", "mahapurusha-chandra", [p],
                    f"{p} own/exalted in house {v.house(p, moon)} from Moon - weaker; in the 7th from Moon it has shown up as pressure on marriage (project calibration)", flaws(p))
    # Lunar yogas (BPHS ch. 37; Phaladeepika ch. 6)
    jm = v.house("Jupiter", moon)
    if jm in KENDRA:
        add("Gajakesari", "lunar", ["Jupiter", "Moon"], f"Jupiter in house {jm} from Moon", flaws("Jupiter"))
    others = [p for p in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"]]
    second = [p for p in others if v.house(p, moon) == 2]
    twelfth = [p for p in others if v.house(p, moon) == 12]
    with_moon = [p for p in others if v.s[p] == moon]
    if second and twelfth: add("Durudhara", "lunar", second + twelfth, "planets both sides of the Moon")
    elif second: add("Sunapha", "lunar", second, "planet in 2nd from Moon")
    elif twelfth: add("Anapha", "lunar", twelfth, "planet in 12th from Moon")
    elif not with_moon:
        cancel = []
        if v.house("Moon") in KENDRA: cancel.append("Moon in a kendra from lagna")
        if any(v.house(p, moon) in KENDRA for p in others): cancel.append("a planet in a kendra from Moon")
        if "Jupiter" in v.aspected_by("Moon"): cancel.append("Jupiter aspects Moon")
        add("Kemadruma" + (" (cancelled)" if cancel else ""), "arishta", ["Moon"], "no planet in 2nd/12th from Moon or with it", "; ".join(cancel))
    adhi = [p for p in ("Mercury", "Jupiter", "Venus") if v.house(p, moon) in (6, 7, 8)]
    if len(adhi) >= 2:
        add("Adhi yoga" + ("" if len(adhi) == 3 else " (partial)"), "lunar", adhi, "benefics in 6/7/8 from Moon")
    if v.s["Moon"] == v.s["Mars"] or v.mutual_aspect("Moon", "Mars"):
        add("Chandra-Mangala", "dhana", ["Moon", "Mars"], "conjunction" if v.s["Moon"] == v.s["Mars"] else "mutual aspect")
    js = v.house("Moon", v.s["Jupiter"])
    if js in (6, 8, 12):
        add("Shakata" + (" (cancelled: Moon in kendra from lagna)" if v.house("Moon") in KENDRA else ""), "arishta",
            ["Moon", "Jupiter"], f"Moon in house {js} from Jupiter")
    # Solar yogas
    sun = v.s["Sun"]
    s2 = [p for p in others if v.house(p, sun) == 2]; s12 = [p for p in others if v.house(p, sun) == 12]
    if s2 and s12: add("Ubhayachari", "solar", s2 + s12)
    elif s2: add("Vesi", "solar", s2)
    elif s12: add("Vasi", "solar", s12)
    if v.s["Sun"] == v.s["Mercury"]:
        add("Budha-Aditya", "solar", ["Sun", "Mercury"], "", "Mercury combust" if v.c["planets"]["Mercury"].get("combust") else "")
    # Amala (Phaladeepika 6): a natural benefic in the 10th from lagna or Moon
    for ref, nm in ((v.lag, "lagna"), (moon, "Moon")):
        b = [p for p in ("Jupiter", "Venus", "Mercury") if v.house(p, ref) == 10]
        if b: add(f"Amala (from {nm})", "other", b, "benefic in the 10th")
    # Raja yogas: kendra lord + trikona lord linked (BPHS ch. 39-41)
    kl = {v.lord(h) for h in (1, 4, 7, 10)}; tl = {v.lord(h) for h in (1, 5, 9)}
    seen = set()
    for a in kl:
        for b in tl:
            if a != b and frozenset((a, b)) not in seen and v.linked(a, b):
                seen.add(frozenset((a, b)))
                how = "conjunction" if v.s[a] == v.s[b] else "exchange" if v.exchange(a, b) else "mutual aspect"
                nm = "Dharma-Karmadhipati" if {a, b} == {v.lord(9), v.lord(10)} else "Raja yoga (kendra-trikona)"
                add(nm, "raja", [a, b], f"{a} ({v.owns(a)}) + {b} ({v.owns(b)}) by {how}", "; ".join(x for x in (flaws(a), flaws(b)) if x))
    for p in SEVEN:
        o = v.owns(p)
        if any(h in (4, 7, 10) for h in o) and any(h in (5, 9) for h in o):
            add("Yogakaraka", "raja", [p], f"{p} owns {o}; placed in house {v.house(p)} ({v.c['planets'][p]['dignity']})", flaws(p))
    # Viparita raja (Phaladeepika 6.56-62): 6L/8L/12L in 6/8/12
    for h, nm in ((6, "Harsha"), (8, "Sarala"), (12, "Vimala")):
        L = v.lord(h)
        if v.house(L) in DUSTHANA:
            add(f"{nm} (Viparita)", "viparita", [L], f"{h}L in the {v.house(L)}th")
    # Parivartana (exchange), classified per Phaladeepika: Maha / Khala (3rd) / Dainya (6, 8, 12)
    for i, a in enumerate(SEVEN):
        for b in SEVEN[i + 1:]:
            if v.exchange(a, b):
                ha, hb = v.house(a), v.house(b)
                kind = "Dainya" if {ha, hb} & DUSTHANA else "Khala" if 3 in (ha, hb) else "Maha"
                add(f"{kind} Parivartana", "parivartana", [a, b], f"houses {hb} and {ha} exchange lords")
    # Dhana yogas: links among lords of 1, 2, 5, 9, 11 (BPHS ch. 41)
    dl = {h: v.lord(h) for h in (1, 2, 5, 9, 11)}
    pairs = set()
    for h1 in dl:
        for h2 in dl:
            if h1 < h2 and dl[h1] != dl[h2] and v.linked(dl[h1], dl[h2]):
                pairs.add((h1, h2))
    for h1, h2 in sorted(pairs):
        add("Dhana yoga", "dhana", [dl[h1], dl[h2]], f"{h1}L {dl[h1]} linked with {h2}L {dl[h2]}",
            "; ".join(x for x in (flaws(dl[h1]), flaws(dl[h2])) if x))
    for h in (2, 11):
        L = v.lord(h)
        if v.house(L) in (2, 5, 9, 11): add("Dhana (placement)", "dhana", [L], f"{h}L in the {v.house(L)}th", flaws(L))
    nl = v.lord(9)
    if v.strong(nl) and v.house(nl) in KENDRA | TRIKONA and v.house(v.lord(1)) not in DUSTHANA:
        add("Lakshmi", "dhana", [nl], "9L own/exalted in kendra/trikona, lagna lord not in a dusthana")
    good = KENDRA | TRIKONA | {2}
    if all(v.house(p) in good for p in ("Jupiter", "Venus", "Mercury")) and \
            (v.strong("Jupiter") or v.c["planets"]["Jupiter"]["dignity"].startswith("Friend")):
        add("Saraswati", "other", ["Jupiter", "Venus", "Mercury"], "all three in kendra/trikona/2nd with Jupiter strong")
    # Neecha bhanga (Phaladeepika 7.26-30; BPHS)
    for p in SEVEN:
        if v.s[p] == DEBIL[p]:
            disp = RASHI_LORD[v.s[p] - 1]
            exl = RASHI_LORD[EXALT[p] - 1]
            ex_here = [q for q in SEVEN if EXALT[q] == v.s[p]]
            c = []
            for q, lab in [(disp, "lord of the debilitation sign"), (exl, "lord of its exaltation sign")] + [(q, "planet exalted in that sign") for q in ex_here]:
                if q == p: continue
                if v.house(q) in KENDRA: c.append(f"{lab} ({q}) in a kendra from lagna")
                if v.house(q, moon) in KENDRA: c.append(f"{lab} ({q}) in a kendra from Moon")
            if disp in v.conj(p) or disp in v.aspected_by(p): c.append(f"joined/aspected by its dispositor {disp}")
            if v.exchange(p, disp): c.append("exchange with dispositor")
            if v.c["planets"][p]["D9"] == EXALT[p]: c.append("exalted in navamsa")
            add("Neecha bhanga" if c else "Debilitated, no cancellation", "neecha-bhanga" if c else "weakness", [p], "; ".join(c))
    # Afflicting conjunctions (same sign; orb given so the reader can weigh it)
    def orb(a, b): return round(abs((v.lon[a] - v.lon[b] + 180) % 360 - 180), 1)
    for a, b, nm in [("Jupiter", "Rahu", "Guru-Chandala"), ("Jupiter", "Ketu", "Guru-Chandala (Ketu)"), ("Mars", "Rahu", "Angaraka"),
                     ("Saturn", "Rahu", "Shrapit"), ("Moon", "Saturn", "Vish / Punarphoo"), ("Sun", "Rahu", "Grahan (Sun-Rahu)"),
                     ("Sun", "Ketu", "Grahan (Sun-Ketu)"), ("Moon", "Rahu", "Grahan (Moon-Rahu)"), ("Moon", "Ketu", "Grahan (Moon-Ketu)"),
                     ("Mars", "Saturn", "Mars-Saturn (Yama)"), ("Sun", "Saturn", "Sun-Saturn")]:
        if v.s[a] == v.s[b]:
            add(nm, "affliction", [a, b], f"same sign, {orb(a, b)} deg apart, house {v.house(a)}")
    return Y


# --------------------------------------------------------------------------- doshas
def manglik(v: View, age=None, south=True):
    """Mangal (Kuja) dosha. Three definitions are reported separately (kb/life-areas/marriage-spouse.md, KD-01..03):
    BPHS ch.80 v.47 = Mars in 1,4,7,8,12; southern = 2,4,7,8,12; software union = 1,2,4,7,8,12.
    Counted from lagna, Moon and Venus. Cancellations are split in two tiers: 'classical' (benefic joining or
    aspecting Mars - the only one with a BPHS basis - and Mars in own/exalted sign) and 'claimed' (the long,
    mutually conflicting later lists). Base rate: about half of all charts have it from lagna alone and three
    quarters from lagna or Moon, so on its own it says very little."""
    union = {1, 2, 4, 7, 8, 12}
    houses = union if south else {1, 4, 7, 8, 12}
    res = {}
    for nm, ref in (("lagna", v.lag), ("moon", v.s["Moon"]), ("venus", v.s["Venus"])):
        h = v.house("Mars", ref)
        res[nm] = {"mars_house": h, "dosha": h in houses, "bphs": h in {1, 4, 7, 8, 12}, "southern": h in {2, 4, 7, 8, 12}}
    ms, h = v.s["Mars"], v.house("Mars")
    classical, claimed = [], []
    ben = [b for b in ("Jupiter", "Venus", "Mercury", "Moon") if b in v.conj("Mars") or b in v.aspected_by("Mars")]
    if ben: classical.append("benefic joins/aspects Mars: " + ", ".join(ben) + " (BPHS 80.47)")
    if ms in (1, 8): classical.append("Mars in own sign")
    if ms == 10: classical.append("Mars exalted")
    if ms in (5, 11): claimed.append("Mars in Leo/Aquarius")
    if ms in (1, 4, 7, 10) and ms not in (1, 10): claimed.append("Mars in a movable sign")
    if "Venus" in v.conj("Mars") and h == 2: claimed.append("Venus with Mars in the 2nd")
    table = {2: (3, 6), 12: (2, 7), 4: (1, 8), 7: (4, 10), 8: (9, 12)}
    if h in table and ms in table[h]: claimed.append(f"Mars in house {h} in {RASHI_EN[ms - 1]} (house-sign exception; lists disagree)")
    if v.lag in (1, 8): claimed.append("Mars is lagna lord")
    if v.lag in (4, 5): claimed.append("Mars is yogakaraka for this lagna")
    if v.house("Saturn") in (1, 4, 7, 8, 12): claimed.append("Saturn in 1/4/7/8/12 (equivalent affliction, used in matching)")
    if age is not None and age >= 28: claimed.append("native past 28 (one source; another calls it a myth)")
    any_dosha = any(r["dosha"] for r in res.values())
    verdict = ("none" if not any_dosha else "present but cancelled (classical ground)" if classical
               else "present; only later-list mitigations apply" if claimed else "present")
    return {"from": res, "present": any_dosha, "cancellations": classical + claimed,
            "cancellations_classical": classical, "cancellations_claimed": claimed,
            "base_rate": "about 50% of charts from lagna, 75% from lagna or Moon - weak evidence alone",
            "verdict": verdict}


def kaal_sarp(v: View):
    ra = v.lon["Rahu"]
    arc = [(v.lon[p] - ra) % 360 for p in SEVEN]
    one = all(a < 180 for a in arc); other = all(a > 180 for a in arc)
    side_a = [p for p, a in zip(SEVEN, arc) if a < 180]; side_b = [p for p in SEVEN if p not in side_a]
    outside = min(side_a, side_b, key=len)
    return {"full": one or other, "type": "Rahu leads (Kaal Sarp)" if other else "Ketu leads (Kaal Amrita)" if one else None,
            "partial": len(outside) == 1, "planets_outside": outside,
            "note": "Not in BPHS/Phaladeepika; a later doctrine. A planet with Rahu/Ketu or one planet outside the arc breaks it."}


def pitru(v: View):
    hits = []
    if v.s["Sun"] in (v.s["Rahu"], v.s["Ketu"], v.s["Saturn"]): hits.append("Sun with Rahu/Ketu/Saturn")
    ninth = sign_at(v.lag, 9)
    mal = [p for p in ("Rahu", "Ketu", "Saturn", "Mars") if v.s[p] == ninth]
    if mal: hits.append(f"{', '.join(mal)} in the 9th")
    if v.house(v.lord(9)) in DUSTHANA: hits.append("9th lord in 6/8/12")
    return hits


# --------------------------------------------------------------------------- special points
def points(v: View):
    def sph(*ps):
        x = sum(v.lon[p] for p in ps) % 360
        sg = rashi_of(x); nv = varga_rashi(x, 9)
        return {"lon": round(x, 2), "sign": RASHI_NAMES[sg - 1], "sign_parity": "odd" if sg % 2 else "even",
                "navamsa": RASHI_NAMES[nv - 1], "navamsa_parity": "odd" if nv % 2 else "even"}
    kala = {"Sun": 30, "Moon": 16, "Mars": 6, "Mercury": 8, "Jupiter": 10, "Venus": 12, "Saturn": 1}
    tot = (kala[v.lord(9)] + kala[v.lord(9, v.s["Moon"])]) % 12 or 12
    indu = sign_at(v.s["Moon"], tot)
    bb = (v.lon["Rahu"] + ((v.lon["Moon"] - v.lon["Rahu"]) % 360) / 2) % 360
    return {"beeja_sphuta": sph("Sun", "Venus", "Jupiter"),      # male fertility: odd sign + odd navamsa favourable
            "kshetra_sphuta": sph("Moon", "Mars", "Jupiter"),    # female fertility: even sign + even navamsa favourable
            "indu_lagna": {"sign": RASHI_NAMES[indu - 1], "house": hfrom(indu, v.lag), "occupants": v.occupants(indu)},
            "bhrigu_bindu": {"lon": round(bb, 2), "sign": RASHI_NAMES[rashi_of(bb) - 1], "house": hfrom(rashi_of(bb), v.lag)}}


# --------------------------------------------------------------------------- KP
KP_OFFSET = 5.8 / 60     # KP (Krishnamurti) ayanamsa is ~5'48" smaller than Lahiri, so KP longitudes are that much larger
ORDER = NAK["vimshottari_order"]; YEARS = NAK["vimshottari_years"]


def kp_lords(lon_lahiri, levels=3):
    """Star, sub and sub-sub lord: a nakshatra (800') is divided in Vimshottari proportion starting from
    its own lord; each sub is divided again the same way (KP Reader I)."""
    x = (lon_lahiri + KP_OFFSET) % 360
    span = 360 / 27
    n = int(x // span); pos = x - n * span
    lords = [NAK_LIST[n]["lord"]]
    cur, width = lords[0], span
    for _ in range(levels - 1):
        i = ORDER.index(cur); acc = 0.0
        for k in range(9):
            L = ORDER[(i + k) % 9]; w = width * YEARS[L] / 120
            if pos < acc + w or k == 8:
                pos -= acc; width = w; cur = L; lords.append(L); break
            acc += w
    return lords


def kp(v: View):
    out = {p: kp_lords(v.lon[p]) for p in PLANET_ORDER}
    asc, mc = v.c["lagna"]["lon"], v.c["lagna"]["mc"]
    for nm, x in (("cusp1", asc), ("cusp7", asc + 180), ("cusp10", mc), ("cusp4", mc + 180)):
        out[nm] = kp_lords(x % 360)
    return out


# --------------------------------------------------------------------------- dasha
def dasha_tree(moon_lon, birth, levels=3, year=365.25):
    """Vimshottari periods as nested lists of (lord, start, end, children)."""
    n, _, frac = nakshatra_of(moon_lon)
    first = NAK_LIST[n - 1]["lord"]
    start0 = birth - dt.timedelta(days=YEARS[first] * frac * year)

    def split(lord, start, span_days, depth):
        out = []; i = ORDER.index(lord); t = start
        for k in range(9):
            L = ORDER[(i + k) % 9]; d = span_days * YEARS[L] / 120
            kids = split(L, t, d, depth + 1) if depth + 1 < levels else []
            out.append((L, t, t + dt.timedelta(days=d), kids)); t += dt.timedelta(days=d)
        return out
    tree = []; t = start0; i = ORDER.index(first)
    for k in range(9):
        L = ORDER[(i + k) % 9]; d = YEARS[L] * year
        tree.append((L, t, t + dt.timedelta(days=d), split(L, t, d, 1) if levels > 1 else [])); t += dt.timedelta(days=d)
    return tree


def dasha_at(tree, when):
    path = []; level = tree
    while level:
        hit = next((x for x in level if x[1] <= when < x[2]), None)
        if not hit: break
        path.append({"lord": hit[0], "start": hit[1], "end": hit[2]}); level = hit[3]
    return path


# --------------------------------------------------------------------------- master
def analyse(chart, sex=None, when=None):
    v = View(chart)
    local = chart["input"]["local"]
    when = when or dt.datetime.now(local.tzinfo)
    age = (when - local).days / 365.25
    st, wars = states(v)
    tree = dasha_tree(chart["planets"]["Moon"]["lon"], local, 3)
    ck = chara_karakas(v)
    ak = ck["seven"]["AK"]
    karakamsa = chart["planets"][ak]["D9"]
    doshas = {"manglik": manglik(v, age), "kaal_sarp": kaal_sarp(v), "pitru": pitru(v)}
    return {"view": v, "panchanga": panchanga(chart),
            "houses": house_table(v), "houses_from_moon": house_table(v, v.s["Moon"]),
            "houses_from_sun": house_table(v, v.s["Sun"]),
            "functional": functional(v), "states": st, "graha_yuddha": wars,
            "karakas": ck, "karakamsa": {"sign": RASHI_NAMES[karakamsa - 1], "house_d1": hfrom(karakamsa, v.lag)},
            "arudhas": arudhas(v), "yogas": yogas(v), "doshas": doshas, "points": points(v), "kp": kp(v),
            "dasha_tree": tree, "dasha_now": dasha_at(tree, when), "age": round(age, 1), "sex": sex}
