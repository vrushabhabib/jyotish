"""Partner-promise gate. MUST run before any Ashtakoota score or match verdict.

Why (20 Oct 2026): Vrushab x Pooja was called a "good match" on ~24/36 while
Vrushab's strongest, life-verified marriage signature (partner from outside his
community/country, life abroad) was never tested. Ashtakoota compares two Moons;
it does not say whether the candidate is the spouse either chart describes.

Order enforced: (1) each chart's partner signatures, (2) real-world facts about
the couple, (3) unmet signatures stated FIRST, (4) only then score + timing.
verdict_allowed stays False until every REQUIRED_FACT is supplied.
"""

SIGNS = ["Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya",
         "Tula", "Vrishchika", "Dhanu", "Makara", "Kumbha", "Meena"]
LORDS = dict(zip(SIGNS, ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
                         "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]))
FOREIGN_D9 = {"Dhanu", "Meena", "Kumbha", "Vrishchika"}

REQUIRED_FACTS = ["same_community", "same_region", "same_country",
                  "residence_after_marriage", "age_gap_years", "professions"]


def _house(lagna, sign):
    return (SIGNS.index(sign) - SIGNS.index(lagna)) % 12 + 1


def _aspects(planet, from_h, to_h):
    d = (to_h - from_h) % 12 + 1
    return d == 7 or {"Mars": d in (4, 8), "Jupiter": d in (5, 9), "Saturn": d in (3, 10),
                      "Rahu": d in (5, 9), "Ketu": d in (5, 9)}.get(planet, False)


def partner_signatures(chart):
    lagna, P = chart["lagna"], chart["planets"]
    h = {p: _house(lagna, v["sign"]) for p, v in P.items()}
    l7 = LORDS[SIGNS[(SIGNS.index(lagna) + 6) % 12]]
    karaka = chart.get("spouse_karaka", "Venus")  # "Jupiter" for a woman's chart
    out = []
    for node in ("Rahu", "Ketu"):
        if node not in P:
            continue
        if l7 in P and P[node]["sign"] == P[l7]["sign"]:
            out.append(("outside_circle", f"7L {l7} with {node} ({abs(P[node].get('deg',0)-P[l7].get('deg',0)):.1f} deg)"))
        if h[node] == 7:
            out.append(("outside_circle", f"{node} in 7th"))
        elif _aspects(node, h[node], 7):
            out.append(("outside_circle", f"{node} aspects 7th"))
        if karaka in P and karaka != l7 and P[node]["sign"] == P[karaka]["sign"]:
            out.append(("outside_circle", f"karaka {karaka} with {node}"))
    for p in {l7, karaka}:
        if p in P and h[p] in (9, 12):
            out.append(("abroad_distance", f"{p} in house {h[p]}"))
    d9 = chart.get("d9", {})
    if d9.get(l7) in FOREIGN_D9:
        out.append(("abroad_distance", f"D9 7L {l7} in {d9[l7]}"))
    for line in chart.get("past_pattern", []):
        out.append(("verified_history", line))
    return out


def gate(chart_a, chart_b, facts):
    missing = [k for k in REQUIRED_FACTS if k not in facts]
    report = {"missing_facts": missing, "verdict_allowed": not missing, "persons": {}}
    for name, ch in (("A", chart_a), ("B", chart_b)):
        themes = {}
        for t, e in partner_signatures(ch):
            themes.setdefault(t, []).append(e)
        unmet = []
        if themes.get("outside_circle") and facts.get("same_community") and facts.get("same_region"):
            unmet.append("outside_circle")
        if themes.get("abroad_distance") and facts.get("residence_after_marriage") == ch.get("home_country", "India"):
            unmet.append("abroad_distance")
        n = len(themes.get("outside_circle", [])) + len(themes.get("abroad_distance", []))
        strength = ("very strong" if themes.get("verified_history") and n >= 3 else
                    "strong" if n >= 3 else "moderate" if n == 2 else "weak")
        report["persons"][name] = {"themes": themes, "unmet": unmet, "strength": strength}
    hard = [p for p in report["persons"].values() if p["unmet"] and p["strength"] in ("strong", "very strong")]
    report["promise_fit"] = ("UNMET - say this first; a points score cannot override it" if hard else
                             "partial" if any(p["unmet"] for p in report["persons"].values()) else "met")
    return report


if __name__ == "__main__":
    import json
    vrushab = {"lagna": "Makara", "home_country": "India",
               "planets": {"Moon": {"sign": "Meena", "deg": 19.1}, "Rahu": {"sign": "Meena", "deg": 17.0},
                           "Ketu": {"sign": "Kanya", "deg": 17.0}, "Venus": {"sign": "Dhanu", "deg": 4.0},
                           "Mars": {"sign": "Meena", "deg": 10.0}, "Jupiter": {"sign": "Meena", "deg": 0.1},
                           "Saturn": {"sign": "Vrishchika", "deg": 25.0}, "Sun": {"sign": "Makara", "deg": 20.0},
                           "Mercury": {"sign": "Kumbha", "deg": 5.0}},
               "d9": {"Moon": "Dhanu"},
               "past_pattern": ["every serious relationship with someone of another background/country (verified Oct 2026)"]}
    pooja = {"lagna": "Mithuna", "spouse_karaka": "Jupiter", "home_country": "India",
             "planets": {"Moon": {"sign": "Simha", "deg": 16.6}, "Jupiter": {"sign": "Simha", "deg": 11.0},
                         "Rahu": {"sign": "Dhanu", "deg": 9.1}, "Ketu": {"sign": "Mithuna", "deg": 9.1},
                         "Mars": {"sign": "Meena", "deg": 10.3}, "Saturn": {"sign": "Makara", "deg": 24.5},
                         "Sun": {"sign": "Mesha", "deg": 27.0}, "Venus": {"sign": "Mesha", "deg": 17.9},
                         "Mercury": {"sign": "Mesha", "deg": 6.2}}}
    facts = {"same_community": True, "same_region": True, "same_country": True,
             "residence_after_marriage": "India", "age_gap_years": 5, "professions": ["business", "corporate"]}
    print(json.dumps(gate(vrushab, pooja, facts), indent=1))
