"""Question charts (prashna) - Shatpanchashika and Daivajna Vallabha (kb/sources/other-texts/README.md).

The chart is cast for the moment and place a question is put. The answer is yes / no / no call, with the rule and verse
behind every point. Built 13 Nov 2026 as the project's FAST forward test: each answer is logged to the ledger BEFORE the
outcome is known, with the date by which it will be known, and scored afterwards.

    python3 -m engine.prashna "Will the buyer confirm the order?" --category gain --place Hubli --due 2026-12-15 --log

The moment is taken from the clock when the command runs (or --at "YYYY-MM-DD HH:MM" if it was noted by hand at the time).
The moment must not be chosen for the chart: ask once, when the question actually arises.

VERDICT RULE (fixed here before any question was scored): every point below counts +1 or -1.
    total >= +2 -> YES;  total <= -2 -> NO;  otherwise NO CALL (not scored).
The +-2 threshold is ours; the points are the texts'. Rahu and Ketu are not used - the two texts do not use them.

Never asked or answered (project rule): outcome of an illness, death, widowhood, pregnancy or sex of a child, war.
"""
from __future__ import annotations
import argparse, datetime as dt, sys
from zoneinfo import ZoneInfo
from engine.chart import build_chart, RASHI_LORD, RASHI_NAMES
from engine.analysis import View

HEAD = (3, 5, 6, 7, 8, 11); BACK = (1, 2, 4, 9, 10)               # Brihat Jataka 1.10; Pisces rises both ways
KIND = {0: "movable", 1: "fixed", 2: "dual"}
CATEGORIES = ("general", "gain", "marriage", "lost", "travel", "return")
BANNED = ("illness", "health", "death", "die", "pregnan", "boy or girl", "widow", "war")


def cast(when: dt.datetime, lat, lon, tz):
    c = build_chart(when.strftime("%Y-%m-%d"), when.strftime("%H:%M"), lat, lon, tz)
    return c, View(c)


def judge(c, v: View, category="general"):
    P = c["planets"]; pts = []
    def add(n, text, src): pts.append({"points": n, "text": text, "source": src})
    waxing = (P["Moon"]["lon"] - P["Sun"]["lon"]) % 360 < 180
    ben = ["Mercury", "Jupiter", "Venus"] + (["Moon"] if waxing else [])
    mal = ["Sun", "Mars", "Saturn"] + ([] if waxing else ["Moon"])
    lag = v.lag; kind = KIND[(lag - 1) % 3]
    if lag in HEAD: add(+1, f"{RASHI_NAMES[lag - 1]} rising - a head-rising sign", "Daivajna Vallabha 2.20")
    elif lag in BACK: add(-1, f"{RASHI_NAMES[lag - 1]} rising - a back-rising sign", "Daivajna Vallabha 2.20")
    L = RASHI_LORD[lag - 1]
    if v.s[L] == lag or L in v.aspecting(lag, nodes=False): add(+1, f"lagna lord {L} is in or looks at the lagna", "Daivajna Vallabha 2.2; Shatpanchashika 1.3")
    for p in ben:
        h = v.house(p)
        if h in (1, 4, 7, 10, 5, 9): add(+1, f"benefic {p} in house {h}", "Daivajna Vallabha 2.21")
        elif h in (6, 8, 12): add(-1, f"benefic {p} in house {h}", "Daivajna Vallabha 2.21 (reverse)")
    for p in mal:
        h = v.house(p)
        if h in (3, 6, 11): add(+1, f"malefic {p} in house {h}", "Daivajna Vallabha 2.21")
        elif h in (1, 4, 7, 10, 8): add(-1, f"malefic {p} in house {h}", "Daivajna Vallabha 2.21 (reverse)")
    mh = v.house("Moon"); seen_by = v.aspected_by("Moon", nodes=False) + v.conj("Moon")
    if category == "gain":
        for p in ben:
            if v.house(p) in (11, 3): add(+1, f"benefic {p} in house {v.house(p)} (gain)", "Daivajna Vallabha 3.1")
        if mh in (7, 10, 2, 6, 3, 11) and any(q in ("Mercury", "Jupiter", "Venus") for q in seen_by):
            add(+1, f"Moon in house {mh} seen by a benefic", "Daivajna Vallabha 3.2")
    if category == "marriage":
        if mh in (3, 5, 6, 7, 11) and any(q in ("Sun", "Jupiter", "Mercury") for q in seen_by):
            add(+1, f"Moon in house {mh} seen by Sun, Jupiter or Mercury", "Daivajna Vallabha 12.1, 12.11")
        if any(v.s[q] == lag for q in ("Mercury", "Moon")) and ("Venus" in v.aspecting(lag, nodes=False)):
            add(+1, "Venus looks at Mercury or the Moon in the lagna", "Daivajna Vallabha 12.12")
        add(+1 if v.s["Saturn"] % 2 == 0 else -1, "Saturn in an even sign" if v.s["Saturn"] % 2 == 0 else "Saturn in an odd sign", "Daivajna Vallabha 12.3")
    if category == "lost":
        for p in ("Mercury", "Jupiter", "Venus"):
            if v.house(p) in (2, 3, 11): add(+1, f"benefic {p} in house {v.house(p)} (recovery)", "Daivajna Vallabha 9.12, 9.15")
        if any(v.s[p] == lag for p in mal) and any(q in mal for q in v.aspecting(lag, nodes=False)):
            add(-2, "a malefic rising and seen by a malefic - gone for good", "Daivajna Vallabha 9.16")
    if category in ("travel", "return"):
        for p in ("Mercury", "Jupiter", "Venus"):
            if v.house(p) in (2, 3): add(+1, f"{p} in house {v.house(p)} (the absent one comes)", "Daivajna Vallabha 6.1")
        if kind == "fixed": add(-1, "a fixed sign rising - no movement", "Daivajna Vallabha 4.1")
        elif kind == "movable": add(+1, "a movable sign rising - movement is certain", "Daivajna Vallabha 4.1")
    total = sum(p["points"] for p in pts)
    verdict = "YES" if total >= 2 else "NO" if total <= -2 else "NO CALL"
    state = {"fixed": "a fixed sign rises: the present state does not change (14.12)",
             "movable": "a movable sign rises: the matter moves, quickly (14.12)",
             "dual": "a dual sign rises: half and half, slowly (14.13)"}[kind]
    gap = (v.s["Moon"] - lag) % 12
    between = [p for p in ("Sun", "Mars", "Mercury", "Jupiter", "Venus", "Saturn") if 0 < (v.s[p] - lag) % 12 < gap]
    hints = [state]
    if gap and not between:
        hints.append(f"Moon is {gap} sign(s) from the lagna with no planet between: the text counts that many days (5.12) - a hint, not scored")
    return {"verdict": verdict, "total": total, "points": pts, "lagna": RASHI_NAMES[lag - 1], "lagna_kind": kind,
            "moon_waxing": waxing, "hints": hints, "category": category}


def ask(question, category, lat, lon, tz, due, when=None, log=False, asker="prashna"):
    if category not in CATEGORIES: raise SystemExit(f"category must be one of {CATEGORIES}")
    if any(b in question.lower() for b in BANNED):
        raise SystemExit("Not asked: illness outcome, death, widowhood, pregnancy or a child's sex, and war are excluded by the project's rules.")
    when = when or dt.datetime.now(ZoneInfo(tz))
    c, v = cast(when, lat, lon, tz); j = judge(c, v, category)
    j.update(question=question, asked_at=when.isoformat(timespec="minutes"), place=(lat, lon, tz), due=due)
    if log:
        from engine import ledger
        basis = f"prashna {j['asked_at']} {RASHI_NAMES[v.lag - 1]} rising; total {j['total']:+d}: " + "; ".join(f"{p['points']:+d} {p['text']}" for p in j["points"])
        row = ledger.add(asker, f"{question} -> {j['verdict']}", category="prashna-" + category, kind="prashna" if j["verdict"] != "NO CALL" else "prashna-nocall",
                         window=f"{when.date().isoformat()}:{due}", basis=basis[:900], confidence=0.5)
        j["ledger_id"] = row.get("id") if isinstance(row, dict) else row
    return j


def text(j):
    L = [f"Question: {j['question']}", f"Asked: {j['asked_at']} at {j['place'][0]}, {j['place'][1]} ({j['place'][2]}); outcome known by {j['due']}",
         f"Rising: {j['lagna']} ({j['lagna_kind']}); Moon {'waxing' if j['moon_waxing'] else 'waning'}", ""]
    for p in j["points"]: L.append(f"  {p['points']:+d}  {p['text']}  [{p['source']}]")
    L += ["", f"Total {j['total']:+d}  ->  {j['verdict']}", ""] + ["Note: " + h for h in j["hints"]]
    L.append("This is a test of the method, logged before the outcome. Our record for question charts is whatever `python3 -m engine.ledger report` shows - nothing else.")
    if j.get("ledger_id"): L.append(f"Logged as {j['ledger_id']}. Score later with: python3 -m engine.ledger score {j['ledger_id']} hit|miss")
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("question"); ap.add_argument("--category", default="general", choices=CATEGORIES)
    ap.add_argument("--place"); ap.add_argument("--lat", type=float); ap.add_argument("--lon", type=float); ap.add_argument("--tz", default="Asia/Kolkata")
    ap.add_argument("--due", required=True, help="date by which the outcome will be known, YYYY-MM-DD")
    ap.add_argument("--at", help='moment the question was put, "YYYY-MM-DD HH:MM" local; default = now')
    ap.add_argument("--log", action="store_true"); ap.add_argument("--asker", default="prashna")
    o = ap.parse_args(argv)
    lat, lon, tz = o.lat, o.lon, o.tz
    if o.place:
        from engine.places import resolve
        pl = resolve(o.place)
        if not pl: raise SystemExit(f"Place '{o.place}' not found; give --lat --lon --tz")
        lat, lon, tz = pl["lat"], pl["lon"], pl["tz"]
    if lat is None or lon is None: raise SystemExit("give --place or --lat and --lon")
    dt.date.fromisoformat(o.due)
    when = dt.datetime.strptime(o.at, "%Y-%m-%d %H:%M").replace(tzinfo=ZoneInfo(tz)) if o.at else None
    print(text(ask(o.question, o.category, lat, lon, tz, o.due, when, o.log, o.asker)))


if __name__ == "__main__":
    main()
