"""Birth-time discrimination: which facts change across an uncertain time window?

    python3 -m engine.discriminate 1990-04-04 09:00 10:00 15.4854 75.1297 Asia/Kolkata

Splits the window into segments inside which lagna, D9 lagna, D10 lagna, D7 lagna and the Moon's
nakshatra-pada are constant, and lists the start month of each mahadasha and of the running sub-periods at
the two ends. The reader then asks only questions whose answers differ between segments. Things that do NOT
change in the window (planet signs, most yogas) cannot help rectify the time and are not asked.
"""
from __future__ import annotations
import sys, datetime as dt
from engine.chart import build_chart

RN = ["Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya", "Tula", "Vrishchika", "Dhanu", "Makara", "Kumbha", "Meena"]
ASK = {
    "lagna": "body type, temperament, and every house: ask sibling order, mother's role, career drive - facts that flip between the two rising signs",
    "D9": "marriage and spouse description: ask how the spouse was met and the spouse's nature (low reliability, see ledger)",
    "D10": "line of work: ask employed or own business, field of work",
    "D7": "children: ask number and sex order of children if any",
    "moon_pada": "dasha sequence itself changes: ask for the year of two major life changes",
}


def _key(c):
    lg = c["lagna"]
    return {"lagna": lg["rashi"], "D9": lg["vargas"]["D9"], "D10": lg["vargas"]["D10"], "D7": lg["vargas"]["D7"],
            "moon_pada": (c["planets"]["Moon"]["nakshatra"], c["planets"]["Moon"]["pada"])}


def segments(date, t0, t1, lat, lon, tz):
    a = dt.datetime.fromisoformat(f"{date}T{t0}"); b = dt.datetime.fromisoformat(f"{date}T{t1}")
    segs, cur, t = [], None, a
    while t <= b:
        c = build_chart(date, t.strftime("%H:%M"), lat, lon, tz)
        k = _key(c)
        if cur is None or k != cur["key"]:
            changed = [x for x in k if cur and k[x] != cur["key"][x]]
            cur = {"from": t.strftime("%H:%M"), "to": t.strftime("%H:%M"), "key": k, "changed": changed}
            segs.append(cur)
        cur["to"] = t.strftime("%H:%M")
        t += dt.timedelta(minutes=1)
    ends = {}
    for label, tt in (("start", t0), ("end", t1)):
        c = build_chart(date, tt, lat, lon, tz)
        ends[label] = [(m["lord"], str(m["start"])[:7]) for m in c["dasha"]["maha"][:6]]
    shift = None
    try:
        y0, m0 = map(int, ends["start"][1][1].split("-")); y1, m1 = map(int, ends["end"][1][1].split("-"))
        shift = abs((y0 * 12 + m0) - (y1 * 12 + m1))
    except Exception: pass
    return {"segments": segs, "dasha_starts": ends, "dasha_shift_months": shift}


def markdown(res):
    L = ["| From | To | Lagna | D9 lagna | D10 lagna | D7 lagna | Moon star-pada | What changed here |", "|---|---|---|---|---|---|---|---|"]
    for s in res["segments"]:
        k = s["key"]
        L.append(f"| {s['from']} | {s['to']} | {RN[k['lagna']-1]} | {RN[k['D9']-1]} | {RN[k['D10']-1]} | {RN[k['D7']-1]} | {k['moon_pada'][0]} {k['moon_pada'][1]} | {', '.join(s['changed']) or '-'} |")
    L.append("")
    L.append(f"Dasha start months move by about {res['dasha_shift_months']} months across the window. "
             "Start of window: " + ", ".join(f"{l} {m}" for l, m in res["dasha_starts"]["start"]) + ". End of window: " +
             ", ".join(f"{l} {m}" for l, m in res["dasha_starts"]["end"]) + ".")
    kinds = sorted({c for s in res["segments"] for c in s["changed"]})
    L.append("\nQuestions that can separate the segments:")
    for k in kinds: L.append(f"- {k}: {ASK[k]}")
    if res["dasha_shift_months"]:
        L.append("- dasha months: ask for the MONTH of a sharp life change near a mahadasha start; each month narrows the time by about "
                 f"{round(60 * 1 / max(res['dasha_shift_months'], 1))} minutes per hour of window")
    return "\n".join(L)


if __name__ == "__main__":
    d, t0, t1, lat, lon = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]), float(sys.argv[5])
    tz = sys.argv[6] if len(sys.argv) > 6 else "Asia/Kolkata"
    print(markdown(segments(d, t0, t1, lat, lon, tz)))
