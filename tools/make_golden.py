"""Freeze the engine's output for three INVENTED births (no real person). Run only when a change in output is intended:
    python3 tools/make_golden.py        then commit tests/golden/reference.json with a message saying why it changed."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import report

BIRTHS = [("2000-01-01", "12:00", 28.6139, 77.2090, "Asia/Kolkata", "M"), ("1975-08-17", "03:40", 13.0827, 80.2707, "Asia/Kolkata", "F"),
          ("1992-11-05", "21:15", 19.0760, 72.8777, "Asia/Kolkata", "M")]


def snapshot(b):
    d, t, la, lo, tz, sex = b; r = report.build(d, t, la, lo, tz, name="ref", sex=sex); c = r["chart"]
    return {"birth": list(b), "lagna": round(c["lagna"]["lon"], 3), "planets": {p: round(x["lon"], 3) for p, x in c["planets"].items()},
            "d9": {p: x["D9"] for p, x in c["planets"].items()},
            "maha": [[m["lord"], str(m["start"])[:10]] for m in c["dasha"]["maha"][:6]],
            "kalachakra": [[p["sign"], str(p["start"])[:10]] for p in r["kalachakra"]["periods"][:6]],
            "rupas": {p: round(x["rupas"], 2) for p, x in r["shadbala"]["planets"].items()},
            "sav": r["ashtakavarga"]["sav"], "finding_ids": sorted(f["id"] for f in r["findings"])}


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tests", "golden", "reference.json")
    json.dump([snapshot(b) for b in BIRTHS], open(out, "w"), indent=1); print("wrote", out)
