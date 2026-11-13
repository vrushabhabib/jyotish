"""Draft linter - the mistakes a checker of findings cannot see (built 13 Nov 2026).

    python3 -m engine.lint DIR/name.computed.json DRAFT.md [--requester "Vrushab"] [--subject "Name"]

Fails (exit 1) on:
  FORBIDDEN   wording about length of life, death, widowhood, childlessness, a child's sex or number, or a medical diagnosis
  PURITY      the requester's name in a reading written for someone else
  UNTAGGED    a sentence that makes a chart claim (names a planet, house, dasha, yoga or sign) with no [F:id] tag in its paragraph
  OVERCLAIM   a sentence worded as a prediction ("will", "is going to", "definitely") resting only on findings whose
              evidence is 'frozen' or 'chance'
Warns on:
  DATE        a date or year in a sentence with no birth-time caveat anywhere in the draft
Lines inside a block that starts with "> method:" are exempt (Part 1 and Part 13 explain methods and limits).
"""
from __future__ import annotations
import json, re, sys
from engine.findings import RULES, TAG

FORBIDDEN = [r"\blife ?span\b", r"\blongevity\b", r"\bwill (?:die|pass away)\b", r"\bdeath of\b", r"\bearly death\b", r"\bwidow(?:ed|hood|er)?\b",
             r"\bchildless\b", r"\bno children\b", r"\b(?:a|one|two|three|\d+) (?:sons?|daughters?)\b", r"\b(?:boy|girl) child\b", r"\bmiscarriage\b",
             r"\b(?:cancer|diabetes|tumou?r|stroke|heart attack|infertil\w+|depression|schizophreni\w+|epileps\w+)\b", r"\byears? (?:to|left to) live\b"]
CLAIM = re.compile(r"\b(Sun|Moon|Mars|Mercury|Jupiter|Venus|Saturn|Rahu|Ketu|lagna|ascendant|dasha|sub-period|antardasha|yoga|navamsa|"
                   r"(?:1st|2nd|3rd|[4-9]th|1[0-2]th) (?:house|lord)|house \d+|Mesha|Vrishabha|Mithuna|Karka|Simha|Kanya|Tula|Vrishchika|Dhanu|Makara|Kumbha|Meena|"
                   r"Aries|Taurus|Gemini|Cancer|Leo|Virgo|Libra|Scorpio|Sagittarius|Capricorn|Aquarius|Pisces)\b")
PREDICT = re.compile(r"\b(will|is going to|are going to|definitely|certainly|guaranteed|is sure to)\b", re.I)
DATE = re.compile(r"\b(19|20)\d\d\b")


def lint(findings, text, requester=None, subject=None):
    by_id = {f["id"]: f for f in findings}; errs, warns = [], []
    paras = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    caveat = bool(re.search(r"birth[- ]time|time of birth", text, re.I))
    for n, para in enumerate(paras, 1):
        if para.lstrip().lower().startswith("> method:"): continue
        tags = [m.group(1) for m in TAG.finditer(para) if not m.group(2)]
        plain = TAG.sub("", para)
        for pat in FORBIDDEN:
            m = re.search(pat, plain, re.I)
            if m: errs.append(("FORBIDDEN", n, m.group(0), plain.strip()[:110]))
        if requester and subject and requester.lower() not in subject.lower() and re.search(r"\b" + re.escape(requester) + r"\b", plain, re.I):
            errs.append(("PURITY", n, requester, plain.strip()[:110]))
        if plain.lstrip().startswith("#"): continue
        if CLAIM.search(plain) and not tags and not re.search(r"\[F:[^\]]+waived:", para):
            errs.append(("UNTAGGED", n, CLAIM.search(plain).group(0), plain.strip()[:110]))
        if tags and PREDICT.search(plain):
            st = {RULES[by_id[t]["rule"]]["status"] for t in tags if t in by_id}
            if st and st <= {"frozen", "chance"}:
                errs.append(("OVERCLAIM", n, PREDICT.search(plain).group(0), plain.strip()[:110]))
        if DATE.search(plain) and not caveat:
            warns.append(("DATE", n, DATE.search(plain).group(0), plain.strip()[:110]))
    return errs, warns[:1]


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("computed"); ap.add_argument("draft"); ap.add_argument("--requester"); ap.add_argument("--subject")
    o = ap.parse_args(argv)
    errs, warns = lint(json.load(open(o.computed))["findings"], open(o.draft, encoding="utf-8").read(), o.requester, o.subject)
    for k, n, w, s in warns: print(f"warning {k} paragraph {n}: '{w}' - no birth-time caveat anywhere in the draft | {s}")
    for k, n, w, s in errs: print(f"{k} paragraph {n}: '{w}' | {s}")
    print(f"{len(errs)} error(s), {len(warns)} warning(s)")
    return 1 if errs else 0


if __name__ == "__main__":
    raise SystemExit(main())
