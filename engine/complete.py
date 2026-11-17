"""Completeness check for a spoken script (Rule 25, owner's hard rule of 17 Nov 2026):
a reading is prepared for EVERY aspect of life before any voice sitting - never partly.

    python3 -m engine.complete SCRIPT.md

Prints the aspects the script does not cover and exits 1 if any is missing. An aspect counts as covered when one of
its words appears in a heading line (a line starting with '#' or a bold '**...**' label)."""
from __future__ import annotations
import re, sys

ASPECTS = {
    "self and nature": ["yourself", "nature", "self"],
    "health (general only)": ["health"],
    "education and learning": ["education", "studies", "learning"],
    "work and business": ["work", "business"],
    "partners, staff and opponents": ["partners", "staff", "opponents", "disputes"],
    "money: earning, saving, spending": ["money"],
    "debts and loans": ["debt", "loan", "dues"],
    "investments and speculation": ["invest", "speculation"],
    "property and home": ["property", "home"],
    "vehicles": ["vehicle"],
    "inheritance": ["inheritance", "family wealth"],
    "father": ["father"],
    "mother": ["mother"],
    "brothers and sisters": ["brother", "sister", "sibling"],
    "friends and network": ["friends", "network"],
    "marriage and partner": ["marriage"],
    "children": ["children"],
    "abroad, travel and residence": ["abroad", "travel", "foreign"],
    "standing and name": ["standing", "name", "reputation"],
    "faith and inner life": ["faith", "inner life", "spiritual"],
    "later life": ["later life"],
    "the past, period by period": ["past"],
    "now": ["now"],
    "age by age ahead": ["age by age"],
    "best and hardest periods": ["best", "hardest"],
    "predictions on record": ["prediction"],
    "what the chart cannot say": ["cannot say", "never said"],
}


def missing(text):
    heads = []
    for l in text.splitlines():
        if l.lstrip().startswith("#"):
            heads.append(l.lower())
        else:
            m = re.match(r"\s*[-*]?\s*\*\*([^*]+)\*\*", l)          # a bold label opening a line: only the label counts
            if m: heads.append(m.group(1).lower())
    heads = " \n".join(heads)
    return [a for a, words in ASPECTS.items() if not any(w in heads for w in words)]


def main(argv=None):
    argv = argv or sys.argv[1:]
    m = missing(open(argv[0], encoding="utf-8").read())
    if m:
        print("NOT COMPLETE - aspects with no heading in the script:"); [print("  -", a) for a in m]; sys.exit(1)
    print(f"COMPLETE - all {len(ASPECTS)} aspects have a heading.")


if __name__ == "__main__":
    main()
