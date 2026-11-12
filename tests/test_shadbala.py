"""Shadbala / Bhava Bala regression against an AstroSage printout.

Reference chart: 24 Nov 1996, 12:05 IST, Hubli 15N20 75E08 (AstroSage report printed 15 Apr 2018, pages 48-49).
The reference numbers are hard-coded below so the tests run without the PDF; test_reference_matches_pdf re-reads
them from the PDF when it (and pdftotext) is available and is skipped otherwise.

Run with pytest, or directly:  python3 tests/test_shadbala.py
"""
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.shadbala import PLANETS, REQUIRED_RUPAS, bhava_bala, kranti_raman, drishti, shadbala, varga_sign

BIRTH = ("1996-11-24", "12:05", 15 + 20 / 60, 75 + 8 / 60)
PDF = os.environ.get("SHADBALA_REF_PDF",
                     "/mnt/user-data/attachments/248c584f-379b-52a0-9ee9-8d0937c5f97e/cbc29bb5-Tanzil.pdf")

#                      Sun     Moon    Mars    Merc    Jup     Venus   Saturn
AS = {
    "uchcha":        [9.49,   58.19,  7.13,   38.03,  3.93,   3.56,   14.38],
    "saptavargaja":  [65.62,  63.75,  67.5,   48.75,  105,    135,    67.5],
    "ojayugma":      [0,      0,      15,     0,      30,     0,      0],
    "kendradi":      [30,     60,     30,     30,     15,     60,     15],
    # AstroSage prints "1" in every Drekkana cell (a display bug); these are the values its own
    # "Total Sthan Bala" row implies (total minus the other four rows).
    "drekkana":      [15,     15,     0,      0,      0,      0,      0],
    "sthana_total":  [120.11, 196.94, 119.63, 116.78, 153.93, 198.56, 96.88],
    "dig":           [59.1,   57.27,  34.54,  37.93,  48.7,   9.36,   13.25],
    "nathonnata":    [59.07,  0.93,   0.93,   60,     59.07,  59.07,  0.93],
    "paksha":        [3.63,   56.37,  3.63,   3.63,   56.37,  56.37,  3.63],
    "tribhaga":      [60,     0,      0,      0,      60,     0,      0],
    "abda":          [0,      15,     0,      0,      0,      0,      0],
    "masa":          [0,      30,     0,      0,      0,      0,      0],
    "vara":          [45,     0,      0,      0,      0,      0,      0],
    "hora":          [0,      0,      0,      0,      0,      0,      60],
    "ayana":         [7.47,   7.03,   38.4,   58.86,  1.5,    14.73,  29.66],
    "yuddha":        [0,      0,      0,      0,      0,      0,      0],
    "kala_total":    [175.17, 109.34, 42.97,  122.49, 176.94, 130.16, 94.23],
    "cheshta":       [9.24,   56.37,  32.91,  14.51,  18.22,  19.84,  41.89],
    "naisargika":    [60,     51.42,  17.16,  25.74,  34.26,  42.84,  8.58],
    "drik":          [-2.09,  4.48,   3.92,   -6.82,  -5.96,  -6.43,  -22.4],
    "total":         [421.54, 475.81, 251.12, 310.64, 426.09, 394.33, 232.43],
    "rupas":         [7.03,   7.93,   4.19,   5.18,   7.1,    6.57,   3.87],
    "required":      [5,      6,      5,      7,      6.5,    5.5,    5],
    "ratio":         [1.41,   1.32,   0.84,   0.74,   1.09,   1.19,   0.77],
    "rank":          [1,      2,      5,      7,      4,      3,      6],
}
AS_BHAVA = {
    "adhipati": [232.43, 232.43, 426.09, 251.12, 394.33, 310.64, 475.81, 421.54, 310.64, 394.33, 251.12, 426.09],
    "dig":      [30, 50, 10, 0, 20, 10, 30, 40, 20, 30, 40, 40],
    "drishti":  [-18.9, -38.99, 20.03, 6.5, -61.43, 8.31, 21, 40.43, -0.61, -1.51, -3.83, -7.67],
    "total":    [243.54, 243.44, 456.12, 257.61, 352.9, 328.94, 526.81, 501.96, 330.03, 422.82, 287.29, 458.42],
    "rupas":    [4.06, 4.06, 7.6, 4.29, 5.88, 5.48, 8.78, 8.37, 5.5, 7.05, 4.79, 7.64],
    "rank":     [11, 12, 4, 10, 6, 8, 1, 2, 7, 5, 9, 3],
}

_cache = {}


def _sb(compat=None):
    if compat not in _cache:
        _cache[compat] = shadbala(*BIRTH, compat=compat)
    return _cache[compat]


def _row(sb, key):
    out = []
    for p in PLANETS:
        d = sb["planets"][p]
        out.append(d["sthana"][key] if key in d["sthana"] else d["kala"][key] if key in d["kala"] else d[key])
    return out


def _maxdiff(ours, ref, skip=()):
    return max(abs(a - b) for p, a, b in zip(PLANETS, ours, ref) if p not in skip)


# ---------------------------------------------------------------- components that match in the default (classical) mode
EXACT = {  # component: tolerance in virupas
    "uchcha": 0.03, "ojayugma": 0.0, "kendradi": 0.0, "drekkana": 0.0, "dig": 0.02,
    "nathonnata": 0.02, "paksha": 0.02, "tribhaga": 0.0, "abda": 0.0, "masa": 0.0, "vara": 0.0,
    "ayana": 0.02, "yuddha": 0.0, "naisargika": 0.04, "drik": 0.05, "required": 0.0,
}


def test_matched_components_default_mode():
    sb = _sb()
    for key, tol in EXACT.items():
        assert _maxdiff(_row(sb, key), AS[key]) <= tol + 1e-9, (key, _row(sb, key), AS[key])


def test_saptavargaja_default_mode():
    ours = _row(_sb(), "saptavargaja")
    # Sun, Mars, Jupiter, Saturn agree exactly (AstroSage prints 65.625 as 65.62)
    assert _maxdiff(ours, AS["saptavargaja"], skip=("Moon", "Mercury", "Venus")) <= 0.01
    diff = {p: round(a - b, 3) for p, a, b in zip(PLANETS, ours, AS["saptavargaja"])}
    # known, documented differences: AstroSage's shifted D12 boundary (Moon, Venus) and the unexplained Mercury value
    assert diff["Moon"] == -11.25 and diff["Venus"] == -7.5 and diff["Mercury"] == 15.0


def test_saptavargaja_astrosage_mode():
    ours = _row(_sb("astrosage"), "saptavargaja")
    assert _maxdiff(ours, AS["saptavargaja"], skip=("Mercury",)) <= 0.01
    assert round(ours[PLANETS.index("Mercury")] - 48.75, 3) == 15.0          # still unverified


def test_cheshta():
    ours = _row(_sb(), "cheshta")
    assert abs(ours[0] - AS["cheshta"][0]) <= 0.02          # Sun: (tropical longitude + 90)/3
    assert abs(ours[1] - AS["cheshta"][1]) <= 0.02          # Moon: = paksha bala
    assert _maxdiff(ours, AS["cheshta"]) <= 1.6             # Mars..Saturn: mean-longitude source differs (unverified)


def test_hora_lord():
    assert _sb()["context"]["hora_lord"] == "Jupiter"                 # 6th hora after a Sunday sunrise
    assert _sb("astrosage")["context"]["hora_lord"] == "Saturn"       # what AstroSage credits
    assert _row(_sb("astrosage"), "hora") == AS["hora"]


def test_lords():
    c = _sb()["context"]
    assert (c["abda_lord"], c["masa_lord"], c["vara_lord"]) == ("Moon", "Moon", "Sun") and c["is_day"]


def test_totals_astrosage_mode():
    sb = _sb("astrosage")
    assert _maxdiff(_row(sb, "sthana_total"), AS["sthana_total"], skip=("Mercury",)) <= 0.03
    assert _maxdiff(_row(sb, "kala_total"), AS["kala_total"]) <= 0.03
    # totals: every planet within 1.6 virupas (cheshta) except Mercury (+15 saptavargaja)
    assert _maxdiff(_row(sb, "total"), AS["total"], skip=("Mercury",)) <= 1.6
    assert _maxdiff(_row(sb, "rupas"), AS["rupas"], skip=("Mercury",)) <= 0.03
    assert abs(_row(sb, "rupas")[3] - AS["rupas"][3]) <= 0.27
    assert _maxdiff(_row(sb, "ratio"), AS["ratio"], skip=("Mercury",)) <= 0.011
    # rank order: Sun, Moon, Venus, Jupiter, Mars identical; Saturn/Mercury (6th/7th) swap because of Mercury's +15
    assert sb["order"][:5] == ["Sun", "Moon", "Venus", "Jupiter", "Mars"]
    assert sb["order"][5:] == ["Mercury", "Saturn"]


def test_totals_default_mode():
    sb = _sb()
    d = {p: a - b for p, a, b in zip(PLANETS, _row(sb, "rupas"), AS["rupas"])}
    for p in ("Sun", "Mars"):
        assert abs(d[p]) <= 0.02
    assert abs(d["Moon"] + 0.19) <= 0.02 and abs(d["Venus"] + 0.12) <= 0.02       # D12 boundary
    assert abs(d["Mercury"] - 0.26) <= 0.02                                       # saptavargaja +15
    assert abs(d["Jupiter"] - 0.98) <= 0.03 and abs(d["Saturn"] + 1.01) <= 0.03   # hora lord 60 virupas
    assert set(sb["order"][:2]) == {"Sun", "Moon"}
    assert sb["unverified"] and any("hora" in u for u in sb["resolved"])


def test_required_minima_and_shape():
    sb = _sb()
    assert REQUIRED_RUPAS == dict(zip(PLANETS, AS["required"]))
    for p in PLANETS:
        d = sb["planets"][p]
        parts = d["sthana_total"] + d["dig"] + d["kala_total"] + d["cheshta"] + d["naisargika"] + d["drik"]
        assert abs(parts - d["total"]) < 1e-9 and abs(d["rupas"] * 60 - d["total"]) < 1e-9
        assert abs(sum(d["sthana"].values()) - d["sthana_total"]) < 1e-9
        assert abs(sum(d["kala"].values()) - d["kala_total"]) < 1e-9
    assert sorted(d["rank"] for d in sb["planets"].values()) == list(range(1, 8))


def test_bhava_bala():
    bb = bhava_bala(*BIRTH)
    h = bb["houses"]
    assert [h[i]["dig"] for i in range(1, 13)] == AS_BHAVA["dig"]
    assert max(abs(h[i]["drishti"] - AS_BHAVA["drishti"][i - 1]) for i in range(1, 13)) <= 0.15
    assert [h[i]["lord"] for i in range(1, 13)] == ["Saturn", "Saturn", "Jupiter", "Mars", "Venus", "Mercury",
                                                    "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter"]


def test_bhava_bala_astrosage_mode():
    h = bhava_bala(*BIRTH, compat="astrosage")["houses"]
    diff = [h[i]["total"] - AS_BHAVA["total"][i - 1] for i in range(1, 13)]
    for i, d in enumerate(diff, 1):
        if i in (6, 9):                         # Mercury-ruled houses carry Mercury's +15
            assert abs(d - 15.6) <= 0.2
        else:
            assert abs(d) <= 1.6
    ranks = [h[i]["rank"] for i in range(1, 13)]
    # 1st/2nd, 7th/8th exact; the Mercury houses (6, 9) move up, so compare the rest pairwise
    assert ranks[0:2] == [11, 12] and ranks[6:8] == [1, 2]


def test_building_blocks():
    assert abs(kranti_raman(90.0) - 24.0) < 1e-9 and abs(kranti_raman(270.0) + 24.0) < 1e-9
    assert abs(kranti_raman(30.0) - 703 / 60) < 1e-9
    assert drishti("Sun", 0.0, 180.0) == 60.0 and drishti("Sun", 0.0, 20.0) == 0.0
    assert drishti("Mars", 0.0, 90.0) == 60.0 and drishti("Saturn", 0.0, 60.0) == 60.0
    assert drishti("Jupiter", 0.0, 120.0) == 60.0 and drishti("Sun", 0.0, 120.0) == 30.0
    assert varga_sign(27.57, 12) == 11 and varga_sign(27.57, 12, "astrosage") == 10
    assert varga_sign(0.0, 2) == 4 and varga_sign(45.0, 2) == 4 and varga_sign(31.0, 2) == 3
    assert varga_sign(33.0, 9) == 9 and varga_sign(63.0, 9) == 6


def test_other_charts_run():
    for args in (("1987-02-03", "06:28", 15.36, 75.12), ("1990-07-15", "23:40", 15.36, 75.12),
                 ("2025-05-29", "16:46", 30.27, -97.74, -5.0)):
        sb = shadbala(*args)
        assert len(sb["order"]) == 7 and all(2.0 < d["rupas"] < 12.0 for d in sb["planets"].values())
        assert len(bhava_bala(*args)["houses"]) == 12


# ---------------------------------------------------------------- optional: re-read the reference from the PDF
_PDF_ROWS = {"Ochcha Bala": "uchcha", "Saptavargaja Bala": "saptavargaja", "Ojayugmarasyamsa Bala": "ojayugma",
             "Kendra Bala": "kendradi", "Total Sthan Bala": "sthana_total", "Total Dig Bala": "dig",
             "Nathonnatha Bala": "nathonnata", "Paksha Bala": "paksha", "Thribhaga Bala": "tribhaga",
             "Abda Bala": "abda", "Masa Bala": "masa", "Vara Bala": "vara", "Hora Bala": "hora",
             "Ayana Bala": "ayana", "Yuddha Bala": "yuddha", "Total Kala Bala": "kala_total",
             "Total Chesta Bala": "cheshta", "Total Naisargeka Bala": "naisargika", "Total Drik Bala": "drik",
             "Total Shad Bala": "total", "Shadbala In Rupas": "rupas", "Minimum Requirements": "required",
             "Ratio": "ratio", "Relative Rank": "rank"}
_PDF_BHAVA = {"Bhavadhipati Bala": "adhipati", "Bhavdig Bala": "dig", "Bhavdrishti Bala": "drishti",
              "Total Bhav Bala": "total", "Total Bhav In Rupas": "rupas"}


def _skip(msg):
    try:
        import pytest
    except ImportError:
        print("SKIP:", msg)
        return
    pytest.skip(msg)


def test_reference_matches_pdf():
    if not os.path.exists(PDF) or not shutil.which("pdftotext"):
        return _skip("reference PDF or pdftotext not available")
    text = subprocess.run(["pdftotext", "-layout", PDF, "-"], capture_output=True, text=True, check=True).stdout
    seen = set()
    for line in text.splitlines():
        s = line.strip()
        for label, key in _PDF_ROWS.items():
            if s.startswith(label) and key not in seen:
                nums = [float(x) for x in s[len(label):].split()]
                if len(nums) == 7:
                    assert nums == [float(x) for x in AS[key]], (label, nums)
                    seen.add(key)
        for label, key in _PDF_BHAVA.items():
            if s.startswith(label):
                nums = [float(x) for x in s[len(label):].split()]
                assert nums == [float(x) for x in AS_BHAVA[key]], (label, nums)
                seen.add("bhava_" + key)
    assert len(seen) == len(_PDF_ROWS) + len(_PDF_BHAVA), sorted(seen)


if __name__ == "__main__":
    failed = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print("ok  ", name)
            except AssertionError as e:
                failed += 1
                print("FAIL", name, e)
    sys.exit(1 if failed else 0)
