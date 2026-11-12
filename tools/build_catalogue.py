"""Rebuild the entry sections of kb/yogas/yogas-catalogue.md from kb/yogas/yogas.json (the single source of truth).
The head of the document (conventions, scoring ladder) and its tail (disagreements, reliability notes, corrections)
are kept as written.   python3 tools/build_catalogue.py
"""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "..", "kb", "yogas", "yogas.json"); M = os.path.join(HERE, "..", "kb", "yogas", "yogas-catalogue.md")
HEAD = [("mahapurusha", "Pancha Mahapurusha"), ("raja", "Raja yogas"), ("dhana", "Dhana yogas"),
        ("lunar", "Lunar yogas (incl. Kemadruma and every cancellation)"), ("solar", "Solar yogas"),
        ("parivartana", "Parivartana (exchange)"), ("viparita", "Viparita raja yogas"),
        ("neecha-bhanga", "Neecha bhanga (each condition separately)"),
        ("other", "Other named yogas and modern doshas (incl. Kaal Sarp)"),
        ("arishta", "Arishta / Daridra / classical doshas"), ("sanyasa", "Pravrajya / Sanyasa"), ("nabhasa", "Nabhasa yogas")]

def main():
    y = json.load(open(J)); md = open(M).read()
    a = md.index("## Pancha Mahapurusha"); b = md.index("## Tradition disagreements worth encoding")
    out = []
    for cat, title in HEAD:
        items = [e for e in y if e["category"] == cat]
        out.append(f"## {title} ({len(items)})\n")
        for e in items:
            out.append(f"### {e['name']}  `{e['id']}`")
            for label, key in (("Condition", "condition"), ("Strength", "strength"), ("Cancellation", "cancellation"),
                               ("Result", "result"), ("Source", "source"), ("Note", "notes")):
                if e.get(key): out.append(f"- **{label}:** {e[key]}")
            out.append("")
        out.append("")
    assert sum(1 for e in y if e["category"] in dict(HEAD)) == len(y), "a category has no heading"
    open(M, "w").write(md[:a] + "\n".join(out) + md[b:])
    print(len(y), "entries written")

if __name__ == "__main__":
    main()
