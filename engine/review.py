"""Independent second pass on a reading (built 13 Nov 2026).

    python3 -m engine.review packet DIR/name.computed.json DRAFT.md > PACKET.md     # what the reviewer gets
    python3 -m engine.review record DIR/name.computed.json DRAFT.md VERDICTS.json   # store the reviewer's verdicts

The packet lists every paragraph of the draft next to the full text of the findings it cites - and nothing else: not the
worksheet, not the conversation, not the writer's reasoning. A reviewer who has not seen the draft being written marks each
paragraph: "supported", "goes beyond the finding" or "contradicts the finding", with one line why.
VERDICTS.json = [{"paragraph": 3, "verdict": "supported|beyond|contradicts", "why": "..."}]
A reading passes review only when every paragraph that cites a finding is marked "supported". The record is tied to the exact
draft by its hash, so an edited draft has to be reviewed again.
"""
from __future__ import annotations
import hashlib, json, re, sys
from engine.findings import TAG, RULES


def paragraphs(text):
    out = []
    for n, p in enumerate([p for p in re.split(r"\n\s*\n", text) if p.strip()], 1):
        tags = [m.group(1) for m in TAG.finditer(p) if not m.group(2)]
        if tags: out.append((n, TAG.sub("", p).strip(), tags))
    return out


def digest(text): return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def packet(findings, text):
    by = {f["id"]: f for f in findings}
    L = ["# Review packet", "", "For each paragraph say: supported / beyond / contradicts, and one line why. Judge ONLY against the findings printed under it. "
         "'Evidence' tells how strongly it may be worded: text = 'the texts say'; hint = faint edge; frozen or chance = must not be worded as a prediction.", f"Draft id: {digest(text)}", ""]
    for n, plain, tags in paragraphs(text):
        L += [f"## Paragraph {n}", plain, "", "Findings cited:"]
        for t in tags:
            f = by.get(t)
            L.append(f"- [{t}] {f['text']} (evidence: {RULES[f['rule']]['status']})" if f else f"- [{t}] NO SUCH FINDING")
        L.append("")
    return "\n".join(L)


def record(findings, text, verdicts):
    need = {n for n, _, _ in paragraphs(text)}; got = {v["paragraph"]: v for v in verdicts}
    missing = sorted(need - set(got)); bad = [v for v in verdicts if v["paragraph"] in need and v["verdict"] != "supported"]
    return {"draft": digest(text), "paragraphs": len(need), "reviewed": len(need) - len(missing), "not_reviewed": missing,
            "not_supported": bad, "passed": not missing and not bad}


def main(argv=None):
    argv = argv or sys.argv[1:]
    if len(argv) < 3 or argv[0] not in ("packet", "record"): print(__doc__); return 2
    fs = json.load(open(argv[1]))["findings"]; text = open(argv[2], encoding="utf-8").read()
    if argv[0] == "packet": print(packet(fs, text)); return 0
    r = record(fs, text, json.load(open(argv[3]))); print(json.dumps(r, indent=1)); return 0 if r["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
