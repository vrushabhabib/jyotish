"""Completeness check for a spoken script (Rule 25, owner's hard rule of 17 Nov 2026):
a reading is prepared for EVERY aspect of life before any voice sitting - never partly.

    python3 -m engine.complete SCRIPT.md

Prints the aspects the script does not cover and exits 1 if any is missing. An aspect counts as covered when one of
its words appears in a heading line (a line starting with '#' or a bold '**...**' label).

Rule 27 (owner's hard rule of 22 Nov 2026) - BALANCE: a reading is never a list of problems. Every life-area section
('## ' heading) must carry four labelled parts: **The good**, **The challenge**, **Why** (the chart reason in plain
words) and **How** (what to do with it). `--balance` (and the default run) reports sections missing any of them.
Sections that are not life areas (the honest note, method, tables, predictions, never-said) are exempt."""
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


PARTS = {"the good": r"\*\*the good", "the challenge": r"\*\*the challenge", "why": r"\*\*why", "how": r"\*\*how"}
EXEMPT = ("said once", "honest", "method", "how this script", "checked", "predictions on record", "never said", "cannot say",
          "quick answers", "when", "the past", "age by age", "best and hardest", "right now", "the picture", "verdict", "in short",
          "at a glance", "how this was made")


def unbalanced(text):
    """[(section heading, [missing parts])] for life-area sections lacking any of the four balance parts."""
    out, cur, body = [], None, []
    def flush():
        if cur is None: return
        h = cur.lower()
        if any(e in h for e in EXEMPT): return
        b = "\n".join(body).lower()
        miss = [k for k, rx in PARTS.items() if not re.search(rx, b)]
        if miss: out.append((cur, miss))
    for l in text.splitlines():
        if l.startswith("## "):
            flush(); cur, body = l[3:].strip(), []
        elif cur is not None:
            body.append(l)
    flush()
    return out


def main(argv=None):
    argv = argv or sys.argv[1:]
    text = open(argv[0], encoding="utf-8").read()
    bal = unbalanced(text)
    if "--balance" not in argv:
        m = missing(text)
        if m:
            print("NOT COMPLETE - aspects with no heading in the script:"); [print("  -", a) for a in m]
        else:
            print(f"COMPLETE - all {len(ASPECTS)} aspects have a heading.")
    else:
        m = []
    if bal:
        print("NOT BALANCED (Rule 27) - sections missing The good / The challenge / Why / How:")
        for h, miss in bal: print(f"  - {h}: missing {', '.join(miss)}")
    else:
        print("BALANCED - every life-area section has the good, the challenge, why and how.")
    if m or bal: sys.exit(1)


if __name__ == "__main__":
    main()
