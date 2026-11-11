"""Parser for AstroSage kundli PDFs ("Big Horoscope" export) -> plain dict.

    from engine.astrosage_pdf import parse, crosscheck
    d = parse("chart.pdf"); print(crosscheck(d))
    python -m engine.astrosage_pdf chart.pdf [--json out.json]

Text comes from `pdftotext -layout` (poppler) run as a subprocess; pdfplumber is
used only if pdftotext is missing.  The PDF is treated as data: nothing in it is
executed.  Every finder works on regex-matched tokens (never fixed columns) and
returns None when its section is absent -- the parser never guesses a value.

VERIFIED on a real file (one 54-page English export, printed 2018):
  birth + avakahada/panchang ("Avkahada Chakra / Basic Details" page), planets
  ("Traditional" page; sign, degree, nakshatra, pada, [R]), chalit table,
  Shodashvarga sign table + bhav table, Shadbala + BhavBala, Ashtakvarga
  (SAV, BAV, Prastharashtakvarga), KP cusps/planets/ruling planets/significators,
  Jaimini karakas + avasthas, Vimshottari maha/antardasha (Lahiri and KP sets),
  Manglik, Kalsarpa, Sade Sati table.
BEST-EFFORT (no sample seen): Sanskrit/abbreviated sign names, degree styles
  other than dd-mm-ss / dd.mm.ss, Hindi-language exports, other AstroSage
  layouts, pdfplumber fallback text, Manglik wordings other than "present in
  Lagna Chart but not in Moon Chart".
NOT PRINTED in this export (always None): combustion flags, arudha padas.
  Pratyantar-dasha pages are indexed in raw_sections but not parsed.
Quirks: the planets table heads its degree column "Latitude" (it is longitude in
sign); dasha dates have 2-digit years (centuries are rebuilt from the birth
year); Rahu/Ketu carry [R] as printed; `house` is the whole-sign house from the
printed "Shodashvarga Bhav Table" (D1 row), not the Chalit bhava.
"""
import datetime as dt
import json
import re
import shutil
import subprocess
import sys

SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio",
         "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
# Prefixes (English, Sanskrit, abbreviations) -> sign index; longest prefix wins.
_SIGN_PREFIX = [
    ("ar", 0), ("mes", 0), ("ta", 1), ("vrisha", 1), ("vrsa", 1), ("ge", 2), ("mit", 2),
    ("can", 3), ("cn", 3), ("kar", 3), ("le", 4), ("sim", 4), ("sin", 4), ("vi", 5), ("kan", 5),
    ("li", 6), ("tu", 6), ("sc", 7), ("vrishc", 7), ("vrisc", 7), ("vrsc", 7), ("vrischi", 7),
    ("sag", 8), ("sg", 8), ("dha", 8), ("cap", 9), ("cp", 9), ("mak", 9), ("aq", 10),
    ("kum", 10), ("pi", 11), ("mee", 11), ("min", 11)]
PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
_PL2 = {"as": "Lagna", "la": "Lagna", "su": "Sun", "mo": "Moon", "ma": "Mars", "me": "Mercury",
        "ju": "Jupiter", "ve": "Venus", "sa": "Saturn", "ra": "Rahu", "ke": "Ketu",
        "ur": "Uranus", "ne": "Neptune", "pl": "Pluto"}
_PLRE = r"(?:ASC|Asc|Lagna|Sun|SUN|Moon|MOON|Mars|MARS|Merc\w*|MERC?|Mer|Jup\w*|JUP\w*|Ven\w*|VEN\w*|" \
        r"Sat\w*|SAT\w*|Rah\w*|Ket\w*|Ura\w*|Ure|Nep\w*|Plu\w*)"
_LORD = r"(SUN|MON|MAR|MER|JUP|VEN|SAT|RAH|KET)"
_DMS = r"\d{1,3}[-°:.]\s?\d{1,2}(?:[-'’′:.]\s?\d{1,2})?[\"”″]?"
DASHA_SEQ = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
DASHA_YRS = dict(zip(DASHA_SEQ, [7, 20, 6, 10, 7, 18, 16, 19, 17]))
_VARGA = [(r"chaturvim|siddh", "D24"), (r"saptavim|bhamsh|nakshatram", "D27"), (r"shodash|kalam", "D16"),
          (r"dwadash|dvadash", "D12"), (r"trimsh", "D30"), (r"khaved", "D40"), (r"akshved", "D45"),
          (r"shasht", "D60"), (r"vimsh", "D20"), (r"chaturth", "D4"), (r"saptam", "D7"),
          (r"navam", "D9"), (r"dasham", "D10"), (r"drek|dresh", "D3"), (r"hora", "D2"),
          (r"lagna|rasi|rashi", "D1")]
_MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]


# ----------------------------------------------------------------- small helpers
def sign_name(tok):
    """'Scorpion', 'Vrishchika', 'Sc', 'SCO', 8 -> 'Scorpio'; None if unknown."""
    s = str(tok).strip()
    if s.isdigit():
        return SIGNS[int(s) - 1] if 1 <= int(s) <= 12 else None
    s = re.sub(r"[^a-z]", "", s.lower())
    best = max((p for p in _SIGN_PREFIX if s.startswith(p[0])), key=lambda p: len(p[0]), default=None)
    return SIGNS[best[1]] if best and len(s) >= 2 else None


def planet_name(tok):
    """'Satn', 'SAT', 'Sa', 'Merc', 'ASC' -> canonical name; 'Mon' is the Moon."""
    return _PL2.get(re.sub(r"[^a-z]", "", str(tok).lower())[:2])


def dms(s):
    """'27-06-12' / '27°06'12"' / '27:06:12' / '27.05.56' / '27°06'' -> decimal degrees."""
    n = [int(x) for x in re.findall(r"\d+", str(s))[:3]]
    return round(sum(v / 60.0 ** i for i, v in enumerate(n)), 6) if n else None


def _num(s):
    f = float(s)
    return int(f) if f == int(f) and "." not in s else f


def _clock(s):
    """'12 : 5 : 0' / '06.36.05' -> '12:05:00'."""
    n = re.findall(r"\d+", s or "")
    return ":".join("%02d" % int(x) for x in n[:3]) if len(n) >= 2 else None


def _geo(s):
    """'15 : 20 : N' / '75.8.E' / '15°20'N' -> signed decimal degrees."""
    h = re.search(r"[NSEW]", (s or "").upper())
    v = dms(re.sub(r"[NSEWnsew]", " ", s or ""))
    return None if v is None or not h else round(-v if h.group() in "SW" else v, 4)


def _kv(text, label, stop=r"\s{3,}|$"):
    """Value printed after `label` on the same line (labels sit at line start or after a gap)."""
    m = re.search(r"(?:^|\s{2,})(?:%s)\s*(?::|\s)\s*(\S.*?)(?=%s)" % (label, stop), text, re.M)
    return m.group(1).strip() if m else None


def _find(pages, pat, flags=re.I):
    return [(i + 1, p) for i, p in enumerate(pages) if re.search(pat, p, flags)]


def pdf_pages(path):
    """Text of each page (layout preserved)."""
    if shutil.which("pdftotext"):
        out = subprocess.run(["pdftotext", "-layout", str(path), "-"], check=True,
                             capture_output=True).stdout.decode("utf-8", "replace")
        return out.split("\f")
    import pdfplumber  # fallback only; untested layout
    with pdfplumber.open(str(path)) as pdf:
        return [(pg.extract_text(layout=True) or "") for pg in pdf.pages]


# ----------------------------------------------------------------- sections
def _raw_sections(pages):
    out = {}
    for i, p in enumerate(pages):
        heads = re.findall(r"\|\|\s*(.+?)\s*\|\|", p)
        if not heads:  # pages without a ||title||: use first line under the banner
            ls = [l.strip() for l in p.splitlines() if l.strip() and "AstroSage.com" not in l]
            heads = [re.sub(r"\s{2,}", " / ", ls[0])[:60]] if ls else []
        for h in heads:
            out.setdefault(h, []).append(i + 1)
    return out


def _birth(pages):
    hit = _find(pages, r"Date of Birth|Basic Details") or _find(pages, r"Time of Birth")
    if not hit:
        return None, None
    t = hit[0][1]
    alltext = "\n".join(pages)
    banner = re.match(r"\s*(\S.*?)\s{3,}Get free chart", t)
    d = re.findall(r"\d+", _kv(t, r"Date of Birth|Date") or "")
    b = {"name": _kv(alltext, "Name", r"\s{2,}|$") or (banner.group(1) if banner else None),
         "sex": _kv(t, "Sex"),
         "date": "%04d-%02d-%02d" % (int(d[2]), int(d[1]), int(d[0])) if len(d) == 3 else None,
         "time": _clock(_kv(t, "Time of Birth")), "weekday": _kv(t, "Day of Birth|Day"),
         "place": _kv(t, "Place of Birth|Place"),
         "lat": _geo(_kv(t, "Latitude")), "lon": _geo(_kv(t, "Longitude")),
         "sunrise": _clock(_kv(t, "Sunrise")), "sunset": _clock(_kv(t, "Sunset")),
         "lmt": _clock(_kv(t, "LMT at Birth")), "gmt": _clock(_kv(t, "GMT at Birth")),
         "julian_day": _kv(t, "Julian Day"), "sidereal_time": _clock(_kv(t, r"Sideral Time|SID"))}
    tz = _kv(t, "Time Zone")
    b["tz"] = float(tz) if tz and re.fullmatch(r"[-+]?\d+(\.\d+)?", tz) else None
    # Ayanamsa: the "Traditional" page prints it cleanly; the basic page wraps value/name
    # onto neighbouring lines, so fall back to a +-2 line window there.
    m = re.search(r"\bAyan\s+(\d{2,3}-\d\d-\d\d)", alltext)
    n = re.search(r"Ayan Type\s+(.+?)(?=\s{2,}|\s+Na[sk]+shatra|$)", alltext, re.M)
    if not m:
        m = re.search(r"Ayanamsa\b(?! Name)[^\n]*\n?[^\n]*?(\d{2,3}-\d\d-\d\d)", t)
    if not n:
        n = re.search(r"\b(Lahiri|Raman|K\.? ?P\.?(?: New| Old)?|Krishnamurti|Yukteshwar)\b"
                      r"(?=[^\n]*\n[^\n]*Ayanamsa Name)|Ayanamsa Name\s+(\S+)", t)
    b["ayanamsa"] = {"name": next((g for g in n.groups() if g), None) if n else None,
                     "text": m.group(1) if m else None, "value": dms(m.group(1)) if m else None}
    # Avakahada chakra + panchang, as printed.
    keys = [("paya", r"Paya(?: \(\w+\))?"), ("varna", "Varna"), ("yoni", "Yoni"), ("gana", "Gana"),
            ("vashya", "Vasya|Vashya"), ("nadi", "Nadi"), ("lagna", r"Lagna(?! Lord)|Asc(?! Lord)"),
            ("lagna_lord", "Lagna Lord|Asc Lord"), ("moon_sign", r"Rasi(?! Lord)|Rashi(?! Lord)"),
            ("moon_sign_lord", "Rasi Lord|Rashi Lord"), ("nakshatra_pada", r"Nakshatra-Pada|Star - Pada"),
            ("nakshatra_lord", "Nakshatra Lord|Star Lord"), ("sun_sign", r"SunSign \(Indian\)"),
            ("tithi", "Tithi"), ("paksha", "Paksha"), ("yoga", "Yoga"), ("karana", "Karan|Karana"),
            ("weekday", "Hindu Week Day"), ("dasha_balance", "Dasa Balance|Bal. Dasa"),
            ("ishtkaal", "Ishtkaal")]
    a = {k: _kv(t, pat) for k, pat in keys}
    m = re.match(r"(.+?)[\s-]+(\d)$", a.get("nakshatra_pada") or "")
    a["nakshatra"], a["pada"] = (m.group(1).strip(), int(m.group(2))) if m else (None, None)
    return b, a


def _planets(pages):
    """'Planetary Positions' rows: name [R] sign dd-mm-ss nakshatra pada."""
    rx = re.compile(r"\b(%s)\s*(\[R\]|\(R\)|-Ret\w*|\bR\b)?\s+([A-Za-z]+)\s+(%s)\s+([A-Za-z][A-Za-z. ]*?)"
                    r"\s*[- ]\s*(\d)\s*$" % (_PLRE, _DMS))
    for no, p in enumerate(pages, 1):
        rows = {}
        for line in p.splitlines():
            m = rx.search(line)
            nm, sg = (planet_name(m.group(1)), sign_name(m.group(3))) if m else (None, None)
            if nm and sg and nm not in rows:
                deg = dms(m.group(4))
                rows[nm] = {"sign": sg, "degree": deg, "degree_text": m.group(4),
                            "longitude": round(SIGNS.index(sg) * 30 + deg, 6),
                            "nakshatra": m.group(5).strip(), "pada": int(m.group(6)),
                            "retrograde": bool(m.group(2)), "combust": None, "house": None, "status": {}}
        if len(rows) >= 8:
            return rows, no
    return None, None


def _chalit(pages):
    """Chalit table: bhava -> start and middle (sign + degree)."""
    rx = re.compile(r"(?:^|\s)(\d{1,2})\s+([A-Za-z]+)\s+(%s)\s+([A-Za-z]+)\s+(%s)\s*$" % (_DMS, _DMS))
    for p in pages:
        out = {}
        for line in p.splitlines():
            m = rx.search(line)
            if m and sign_name(m.group(2)) and sign_name(m.group(4)):
                out[int(m.group(1))] = {"begin_sign": sign_name(m.group(2)), "begin": dms(m.group(3)),
                                        "mid_sign": sign_name(m.group(4)), "mid": dms(m.group(5))}
        if len(out) == 12:
            return out
    return None


def _vargas(pages):
    """Shodashvarga table (signs) and Shodashvarga Bhav table (houses)."""
    hit = _find(pages, r"Shodash\s*varga\s+Table")
    if not hit:
        return None, None
    signs, houses, cols, target = {}, {}, [], None
    for line in hit[0][1].splitlines():
        if re.search(r"Bhav\s+Table", line, re.I):
            target = houses
        elif re.search(r"S\.?\s*N\.?\s+Shodash", line, re.I):
            cols = [planet_name(x) for x in line.split()[2:]]
            target = signs if target is None else target
        else:
            m = re.match(r"\s*\d{1,2}\s+([A-Za-z]+)\s+((?:\d{1,2}\s*)+)$", line)
            d = m and next((v for pat, v in _VARGA if re.search(pat, m.group(1), re.I)), None)
            if d and target is not None and len(m.group(2).split()) == len(cols):
                vals = [int(x) for x in m.group(2).split()]
                target[d] = {c: (sign_name(v) if target is signs else v) for c, v in zip(cols, vals) if c}
    return signs or None, houses or None


_SB_KEYS = [("sthana", r"total\s+sthan"), ("dig", r"total\s+dig"), ("kala", r"total\s+kala"),
            ("cheshta", r"total\s+che"), ("naisargika", r"naisarg"), ("drik", r"total\s+drik"),
            ("total", r"total\s+shad"), ("rupas", r"rupas"), ("min_required", r"minimum"),
            ("ratio", r"ratio"), ("rank", r"rank")]
_BB_KEYS = [("adhipati", r"adhipati"), ("dig", r"dig"), ("drishti", r"drishti"),
            ("total", r"total\s+bhav\s+bala"), ("rupas", r"rupas"), ("rank", r"rank")]


def _bala(pages):
    """Shadbala (label + 7 numbers per row) and BhavBala (label + 12 numbers)."""
    hit = _find(pages, r"Shad\s*bala\s+Table|Bhav\s*Bala\s+Table")
    if not hit:
        return None, None
    sb, bb, cols = {}, {}, PLANETS[:7]
    for line in hit[0][1].splitlines():
        heads = [planet_name(x) for x in line.split()]
        if len(heads) == 7 and all(heads):
            cols = heads  # column order as printed
        m = re.match(r"\s*([A-Za-z][A-Za-z ]*?)\s+((?:-?\d+(?:\.\d+)?\s*)+)$", line)
        vals = m.group(2).split() if m else []
        if len(vals) == 7:
            for c, v in zip(cols, vals):
                sb.setdefault(c, {"rows": {}})["rows"][m.group(1)] = _num(v)
        elif len(vals) == 12:
            for h, v in enumerate(vals, 1):
                bb.setdefault(h, {"rows": {}})["rows"][m.group(1)] = _num(v)
    for table, keys in ((sb, _SB_KEYS), (bb, _BB_KEYS)):
        for rec in table.values():  # canonical aliases next to the as-printed rows
            for k, pat in keys:
                rec[k] = next((v for lab, v in rec["rows"].items() if re.search(pat, lab, re.I)), None)
    return sb or None, bb or None


def _ashtakavarga(pages):
    """SAV + BAV from the Ashtakvarga table; prastara grids from the Prasthar page."""
    out, order = None, ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Lagna"]
    rx = re.compile(r"\b(%s|Total)\s+((?:\d{1,2}\s+){11}\d{1,2})\s*$" % _PLRE)
    for p in pages:
        rows = {}
        for line in p.splitlines():
            m = rx.search(line)
            if m:
                rows.setdefault(planet_name(m.group(1)) if m.group(1) != "Total" else "Total",
                                [int(x) for x in m.group(2).split()])
        if "Total" in rows and len(rows) >= 8:
            out = {"sav": dict(zip(SIGNS, rows.pop("Total"))),
                   "bav": {k: dict(zip(SIGNS, v)) for k, v in rows.items() if k}, "prastara": None}
            out["sav_total"] = sum(out["sav"].values())
            break
    hit = _find(pages, r"Prasth?ar\s*ashtak")
    if hit:
        pr, cur = {}, []
        for line in hit[0][1].splitlines():
            names = line.split()
            if names and all(n in order[:7] for n in names):  # title line: one or two tables
                cur = [(m.group(), m.start()) for m in re.finditer(r"[A-Za-z]+", line)]
                continue
            line = re.sub(r"Total\s*(?:\d+\s+){11}\d+", lambda m: " " * len(m.group()), line)
            ms = list(re.finditer(r"(?:\b(Su|Mo|Ma|Me|Ju|Ve|Sa|As|La)\s+)?((?:[01]\s+){12})(\d{1,2})\b", line))
            for i, m in enumerate(ms):
                if not cur:
                    break
                # side-by-side tables: 2 matches -> left/right; 1 match -> decide by the right title column
                side = i if len(ms) == len(cur) else int(len(cur) > 1 and m.start(2) > cur[1][1])
                tab = pr.setdefault(cur[side][0], {})
                # pdftotext sometimes drops a row label to the next line: use the fixed row order
                lab = planet_name(m.group(1)) if m.group(1) else order[len(tab)] if len(tab) < 8 else None
                if lab and lab not in tab:
                    tab[lab] = [int(x) for x in m.group(2).split()]
        if pr:
            out = out or {"sav": None, "bav": None, "sav_total": None}
            out["prastara"] = pr
    return out


def _kp(pages, birth_date):
    hit = [h for h in _find(pages, r"KP System|Nakshatra Nadi|Krishnamurti") if "Cusp" in h[1]]
    if not hit:
        return None
    t = hit[0][1]
    a = re.search(r"\bAyan\s+(\d{2,3}-\d\d-\d\d)", t)
    n = re.search(r"Ayan Type\s+(.+?)(?=\s{2,}|\s+Na[sk]+shatra|$)", t, re.M)
    kp = {"ayanamsa": {"name": n.group(1).strip() if n else None, "text": a.group(1) if a else None,
                       "value": dms(a.group(1)) if a else None},
          "cusps": {}, "planets": {}, "ruling_planets": {}, "house_significators": {}, "planet_significations": {}}
    tail = r"\s+(%s)\s+%s\s+%s\s+%s\s+%s\b" % (_DMS, _LORD, _LORD, _LORD, _LORD)
    part = None
    for line in t.splitlines():
        part = "h" if "Significators of Houses" in line else "p" if "Planet Signification" in line else part
        m = re.search(r"(?<![\d/(])\b(\d{1,2})" + tail, line) or re.search(r"\b(%s)" % _PLRE + tail, line)
        if m:
            lon = dms(m.group(2))
            rec = {"longitude": lon, "sign": SIGNS[int(lon // 30) % 12], "degree": round(lon % 30, 6),
                   "sign_lord": planet_name(m.group(3)), "star_lord": planet_name(m.group(4)),
                   "sub_lord": planet_name(m.group(5)), "sub_sub_lord": planet_name(m.group(6))}
            if m.group(1).isdigit():
                kp["cusps"][int(m.group(1))] = rec
            else:
                kp["planets"][planet_name(m.group(1))] = rec
        m = re.search(r"\b(Lagna|Moon)\s+%s\s+%s\s+%s\s*$" % (_LORD, _LORD, _LORD), line)
        if m:
            kp["ruling_planets"][m.group(1)] = dict(zip(("sign_lord", "star_lord", "sub_lord"),
                                                        map(planet_name, m.groups()[1:])))
        m = re.search(r"Day Lord\s+%s" % _LORD, line)
        if m:
            kp["ruling_planets"]["Day Lord"] = planet_name(m.group(1))
        m = part == "h" and re.search(r"(?:^|\s{2,})(\d{1,2})\s{2,}((?:(?:SU|MO|MA|ME|JU|VE|SA|RA|KE)\s*)+)$", line)
        if m:
            kp["house_significators"][int(m.group(1))] = [planet_name(x) for x in m.group(2).split()]
        m = part == "p" and re.search(r"\b(%s)\s{2,}((?:\d{1,2}\s*)+)$" % _PLRE, line)
        if m:
            kp["planet_significations"][planet_name(m.group(1))] = [int(x) for x in m.group(2).split()]
    kp["vimshottari"] = _dasha_blocks(t, birth_date)
    return kp if len(kp["cusps"]) == 12 else None


def _jaimini(pages, planets):
    """Karaka table (Sthir / Chara columns); the same rows carry the Avastha table."""
    hit = _find(pages, r"Karak\s+Sthir|Chara\s*Karak|J[ai]+mini")
    if not hit:
        return None
    names = {"atm": "AK", "ama": "AmK", "bhr": "BK", "mat": "MK", "put": "PK", "gna": "GK", "dar": "DK", "pit": "PiK"}
    chara, sthira = {}, {}
    rx = re.compile(r"(?:^|\s)(Atma|Amatya|Bhratru|Matr\w*|Putra|Pitr\w*|Gnati|Dara)\w*\s+(%s)\s+(%s)"
                    r"(?:\s+(%s)\s+(\w+)\s+(\w+)\s+(\w+))?" % (_PLRE, _PLRE, _PLRE))
    for no, t in hit:
        for m in rx.finditer(t):
            k = names[m.group(1)[:3].lower()]
            sthira[k], chara[k] = planet_name(m.group(2)), planet_name(m.group(3))
            if m.group(4) and planets and planet_name(m.group(4)) in planets:
                planets[planet_name(m.group(4))]["status"].update(
                    jagrat=m.group(5), baladi=m.group(6), deeptadi=m.group(7))
        if chara:
            return {"chara_karakas": chara, "sthira_karakas": sthira, "arudha_padas": None, "page": no}
    return None


def _full_date(d, m, yy, not_before):
    """Expand a 2-digit year to the first matching date on/after `not_before`."""
    for y in range(not_before.year - not_before.year % 100 + yy, not_before.year + 201, 100):
        try:
            if dt.date(y, m, d) >= not_before:
                return dt.date(y, m, d)
        except ValueError:
            return None
    return None


def _dasha_blocks(text, birth_date):
    """Vimshottari blocks: 'SUN -6 Years' / 'dd/mm/yy - dd/mm/yy' / antardasha end dates.
    Blocks sit three abreast, so cells are matched per line and routed to the column whose
    next expected antardasha lord they name (the antardasha order is fixed)."""
    drx = r"(\d{1,2})/\s*(\d{1,2})/\s*(\d{2})"
    md, cur = {}, []
    for line in text.splitlines():
        heads = re.findall(_LORD + r"\s*-\s*(\d+)\s*Years?", line)
        if heads:
            cur = [planet_name(h[0]) for h in heads]
            for h in heads:
                md.setdefault(planet_name(h[0]), {"years": int(h[1]), "range": None, "ad": []})
            continue
        ranges = re.findall(drx + r"\s*-\s*" + drx, line)
        if ranges and cur:
            for lord, r in zip(cur, ranges):
                md[lord]["range"] = [int(x) for x in r]
            continue
        col = 0
        for m in re.finditer(r"\b" + _LORD + r"\s+" + drx + r"(?!\d)", line):
            lord = planet_name(m.group(1))
            for c in range(col, len(cur)):
                want = DASHA_SEQ[(DASHA_SEQ.index(cur[c]) + len(md[cur[c]]["ad"])) % 9]
                if lord == want and len(md[cur[c]]["ad"]) < 9:
                    md[cur[c]]["ad"].append((lord, [int(x) for x in m.groups()[1:]]))
                    col = c + 1
                    break
    md = {k: v for k, v in md.items() if v["range"]}
    if len(md) < 9 or not birth_date:
        return None
    # Start with the lord whose printed start is the birth date; then chain centuries forward.
    b = dt.date.fromisoformat(birth_date)
    first = next((k for k, v in md.items() if v["range"][:3] == [b.day, b.month, b.year % 100]), None)
    if not first:
        return None
    out, floor = [], b
    for i in range(9):
        lord = DASHA_SEQ[(DASHA_SEQ.index(first) + i) % 9]
        r = md[lord]["range"]
        start, end = _full_date(r[0], r[1], r[2], floor), None
        end = start and _full_date(r[3], r[4], r[5], start)
        if not end:
            return None
        # antardashas are printed as END dates; the first maha's begin before birth
        prev = dt.date(end.year - DASHA_YRS[lord], end.month, min(end.day, 28)) - dt.timedelta(days=3)
        ads = []
        for al, (d, m, yy) in md[lord]["ad"]:
            e = _full_date(d, m, yy, prev)
            if not e:
                break
            ads.append({"lord": al, "end": e.isoformat()})
            prev = e
        out.append({"lord": lord, "years": md[lord]["years"], "start": start.isoformat(),
                    "end": end.isoformat(), "antardashas": ads})
        floor = end
    return out


def _vimshottari(pages, birth_date, skip_page):
    alltext = "\n".join(pages)
    m = re.search(r"(?:Bal\.?\s*Dasa|Dasa Balance)\s*:?\s*([A-Za-z]+)\s+(\d+)\s*Y\s+(\d+)\s*M\s+(\d+)\s*D", alltext)
    bal = m and {"lord": planet_name(m.group(1)), "years": int(m.group(2)), "months": int(m.group(3)),
                 "days": int(m.group(4)), "text": " ".join(m.group(0).split())}
    for no, p in enumerate(pages, 1):  # first non-KP page that carries full blocks
        md = None if no == skip_page else _dasha_blocks(p, birth_date)
        if md:
            return {"balance": bal or None, "mahadashas": md, "page": no}
    return {"balance": bal, "mahadashas": None, "page": None} if bal else None


def _doshas(pages):
    out = {"manglik": None, "kaal_sarp": None, "sade_sati": None}
    hit = _find(pages, r"Manglik|Mangal Dosha")
    if hit:
        t = " ".join(hit[0][1].split())
        res = re.search(r"Hence[^.]*\.", t)
        pos = re.search(r"placed in (\w+) house from Lagna.*?Moon chart Mangal is placed in\s+(\w+) house", t)
        r, flags = (res.group(0) if res else ""), {}
        for k in ("Lagna", "Moon"):  # "... present in Lagna Chart but not in Moon Chart."
            m = re.search(r"(not\s+)?(?:present\s+)?in\s+(?:both\s+)?(?:\w+\s+(?:Chart\s+)?and\s+)?%s\s+Chart" % k, r, re.I)
            flags[k] = None if not m else not (m.group(1) or re.search(r"not present|free from|absent", r, re.I))
        out["manglik"] = {"result": r or None, "from_lagna": flags["Lagna"], "from_moon": flags["Moon"],
                          "mars_house_from_lagna": pos.group(1) if pos else None,
                          "mars_house_from_moon": pos.group(2) if pos else None}
    hit = _find(pages, r"Kal\s*sarpa?\s+(Dosh|Yog)")
    m = hit and re.search(r"Result\s*:\s*(.+)", hit[0][1])
    if m:
        txt = m.group(1).strip()
        out["kaal_sarp"] = {"result": txt, "present": not re.search(r"free from|not present|\bno\b", txt, re.I)}
    rows = []
    for no, p in _find(pages, r"Sade\s*sati"):
        lines = [l for l in p.splitlines() if l.strip()]
        for i, line in enumerate(lines):
            m = re.match(r"\s*(\d{1,3})\s+(Sade\s*Sati|Small\s+Panoti|Panoti|Dhaiya)\s+([A-Za-z]+)\s+(.*)$", line)
            if not m or not sign_name(m.group(3)):
                continue
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            if not re.fullmatch(r"[\s\d,A-Za-z]*\d[\s\d,]*", nxt) or re.match(r"\s*\d+\s+(Sade|Small)", nxt):
                nxt = ""  # only pure date remainders count as a wrapped second line
            ph = re.search(r"Rising|Peak|Setting", m.group(4) + " " + nxt)
            # dates wrap inside their own column: each 'Month DD, YYYY' borrows what it lacks from line 2
            frags, extra = [], re.findall(r"\d+", nxt)
            for tok in re.findall(r"[A-Za-z]+|\d+", re.sub(r"Rising|Peak|Setting", "", m.group(4))):
                if tok[:3].lower() in _MONTHS and not tok.isdigit():
                    frags.append([tok])
                elif frags:
                    frags[-1].append(tok)
            dates = []
            for f in frags[:2]:
                while len(f) < 3 and extra:
                    f.append(extra.pop(0))
                try:
                    dates.append(dt.date(int(f[2]), _MONTHS.index(f[0][:3].lower()) + 1, int(f[1])).isoformat())
                except (ValueError, IndexError):
                    dates.append(None)
            rows.append({"n": int(m.group(1)), "type": " ".join(m.group(2).split()), "saturn_sign": sign_name(m.group(3)),
                         "start": dates[0] if dates else None, "end": dates[1] if len(dates) > 1 else None,
                         "phase": ph.group(0) if ph else None, "page": no})
    out["sade_sati"] = rows or None
    return out


# ----------------------------------------------------------------- public API
def parse_pages(pages, source=None):
    """Parse a list of page texts (as produced by `pdftotext -layout`)."""
    birth, avak = _birth(pages)
    planets, ppage = _planets(pages)
    vargas, varga_houses = _vargas(pages)
    if planets and varga_houses and "D1" in varga_houses:
        for k, rec in planets.items():
            rec["house"] = varga_houses["D1"].get(k)
    shadbala, bhava_bala = _bala(pages)
    bdate = birth and birth.get("date")
    kp = _kp(pages, bdate)
    kp_page = next((i + 1 for i, p in enumerate(pages) if kp and re.search(r"KP System|Nakshatra Nadi", p)), None)
    return {"source": source, "pages": len(pages), "birth": birth, "avakahada": avak, "planets": planets,
            "chalit": _chalit(pages), "vargas": vargas, "varga_houses": varga_houses,
            "shadbala": shadbala, "bhava_bala": bhava_bala, "ashtakavarga": _ashtakavarga(pages), "kp": kp,
            "jaimini": _jaimini(pages, planets), "vimshottari": _vimshottari(pages, bdate, kp_page),
            "doshas": _doshas(pages), "raw_sections": _raw_sections(pages)}


def parse(pdf_path):
    return parse_pages(pdf_pages(pdf_path), source=str(pdf_path))


def crosscheck(parsed, tolerance_arcmin=5.0, warn_arcmin=1.0):
    """Recompute longitudes with engine.ephem_chart and compare with the printed ones.
    A body fails above `tolerance_arcmin` and is listed in `warnings` above `warn_arcmin`."""
    from engine.ephem_chart import build, vimshottari  # lazy: parser itself needs no ephemeris
    b, pl = parsed.get("birth") or {}, parsed.get("planets") or {}
    if not pl or None in (b.get("date"), b.get("time"), b.get("lat"), b.get("lon")):
        return {"ok": False, "error": "birth data or planets missing"}
    tz = b["tz"] if b.get("tz") is not None else 5.5
    calc = build(b["date"], b["time"], b["lat"], b["lon"], tz)
    out = {"bodies": {}, "warnings": [], "tolerance_arcmin": tolerance_arcmin, "warn_arcmin": warn_arcmin,
           "ayanamsa": {"pdf": (b.get("ayanamsa") or {}).get("value"), "computed": round(calc["_ayanamsa"], 5)}}
    for k in ["Lagna"] + PLANETS:
        if k in pl:
            diff = ((calc[k] - pl[k]["longitude"] + 180) % 360 - 180) * 60
            out["bodies"][k] = {"pdf": pl[k]["longitude"], "computed": round(calc[k], 4),
                                "diff_arcmin": round(diff, 2), "pass": abs(diff) <= tolerance_arcmin,
                                "warn": abs(diff) > warn_arcmin}
            if abs(diff) > warn_arcmin:
                out["warnings"].append("%s differs by %+.2f arc-min" % (k, diff))
    bal = (parsed.get("vimshottari") or {}).get("balance")
    if bal:
        pdf_y = bal["years"] + bal["months"] / 12.0 + bal["days"] / 365.25
        res = {"pdf_lord": bal["lord"], "pdf_years": round(pdf_y, 4)}
        for tag, moon in (("computed", calc["Moon"]), ("from_pdf_moon", pl.get("Moon", {}).get("longitude"))):
            if moon is not None:
                lord, yrs, _ = vimshottari(moon, dt.datetime.fromisoformat(b["date"] + "T" + b["time"]))
                res[tag] = {"lord": lord, "years": round(yrs, 4), "diff_days": round((yrs - pdf_y) * 365.25, 1)}
        # Moon arc -> dasha time: 800' of nakshatra = lord_years, so the same arc-minute yardstick
        # applies; +16 days because the printed balance is whole days built from 30-day months.
        lim = DASHA_YRS.get(bal["lord"], 0) * 365.25 * tolerance_arcmin / 800.0 + 16
        res["pass"] = res.get("computed", {}).get("lord") == bal["lord"] and abs(res["computed"]["diff_days"]) <= lim
        out["vimshottari_balance"] = res
    out["ok"] = all(v["pass"] for v in out["bodies"].values()) and out.get("vimshottari_balance", {}).get("pass", True)
    return out


def _fmt(deg):
    s = int(round(deg * 3600))
    return "%02d°%02d'%02d\"" % (s // 3600, s % 3600 // 60, s % 60)


def summary(d):
    """Compact human-readable summary used by the CLI."""
    b, L = d.get("birth") or {}, []
    L.append("%s (%s)  %s %s  %s  lat %s lon %s  tz %s  ayanamsa %s %s" % (
        b.get("name"), b.get("sex"), b.get("date"), b.get("time"), b.get("place"), b.get("lat"), b.get("lon"),
        b.get("tz"), (b.get("ayanamsa") or {}).get("name"), (b.get("ayanamsa") or {}).get("text")))
    a = d.get("avakahada") or {}
    L.append("Panchang: tithi %s (%s), yoga %s, karana %s, nakshatra %s-%s, gana %s, nadi %s, yoni %s" % (
        a.get("tithi"), a.get("paksha"), a.get("yoga"), a.get("karana"), a.get("nakshatra"), a.get("pada"),
        a.get("gana"), a.get("nadi"), a.get("yoni")))
    for k, p in (d.get("planets") or {}).items():
        L.append("  %-8s %-11s %s  %-14s p%s  H%-2s %s" % (k, p["sign"], _fmt(p["degree"]), p["nakshatra"],
                                                         p["pada"], p["house"], "R" if p["retrograde"] else ""))
    av = d.get("ashtakavarga") or {}
    if av.get("sav"):
        L.append("SAV: %s = %s" % (" ".join(str(v) for v in av["sav"].values()), av["sav_total"]))
    if d.get("shadbala"):
        L.append("Shadbala (rupas): " + ", ".join("%s %s" % (k, v["rupas"]) for k, v in d["shadbala"].items()))
    v = d.get("vimshottari") or {}
    if v.get("balance"):
        L.append("Vimshottari balance: %s" % v["balance"]["text"])
    for m in v.get("mahadashas") or []:
        L.append("  %-8s %s -> %s" % (m["lord"], m["start"], m["end"]))
    j, dz = d.get("jaimini") or {}, d.get("doshas") or {}
    if j:
        L.append("Chara karakas: " + ", ".join("%s %s" % kv for kv in j["chara_karakas"].items()))
    L.append("Manglik: %s | Kaal sarp: %s | Sade sati rows: %s" % (
        (dz.get("manglik") or {}).get("result"), (dz.get("kaal_sarp") or {}).get("result"),
        len(dz.get("sade_sati") or [])))
    present = [k for k in ("birth", "avakahada", "planets", "chalit", "vargas", "shadbala", "bhava_bala",
                           "ashtakavarga", "kp", "jaimini", "vimshottari") if d.get(k)]
    L.append("Sections parsed: " + ", ".join(present))
    return "\n".join(L)


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help"):
        print("usage: python -m engine.astrosage_pdf file.pdf [--json out.json]")
        return 2
    d = parse(argv[0])
    print(summary(d))
    if "--json" in argv:
        with open(argv[argv.index("--json") + 1], "w") as fh:
            json.dump(d, fh, indent=1, ensure_ascii=False)
    try:
        cc = crosscheck(d)
        for k, v in cc.get("bodies", {}).items():
            print("  check %-8s %+8.2f'  %s" % (k, v["diff_arcmin"], "FAIL" if not v["pass"] else "warn" if v["warn"] else "ok"))
        print("Crosscheck:", "PASS" if cc.get("ok") else "FAIL", cc.get("vimshottari_balance", cc.get("error", "")))
    except ImportError as e:  # ephemeris backend not installed
        print("Crosscheck skipped:", e)
    return 0


if __name__ == "__main__":
    sys.exit(main())
