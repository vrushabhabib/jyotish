"""Offline place lookup: name -> latitude, longitude, time zone.

Uses the geonamescache package (GeoNames cities with population above 15,000, bundled data, no network) and
timezonefinder when installed. Villages are not in it: for those pass a plus code or coordinates, or the
nearest town (within about 30 km the lagna moves by at most about a quarter of a degree).

    python3 -m engine.places Hubli
    python3 -m engine.places "Karimnagar" IN
"""
from __future__ import annotations
import sys, unicodedata

ALIASES = {"hubli": "hubballi", "bangalore": "bengaluru", "bombay": "mumbai", "madras": "chennai", "calcutta": "kolkata",
           "belgaum": "belagavi", "mysore": "mysuru", "mangalore": "mangaluru", "poona": "pune", "saigon": "ho chi minh city",
           "gulbarga": "kalaburagi", "bijapur": "vijayapura", "shimoga": "shivamogga", "tumkur": "tumakuru", "baroda": "vadodara",
           "trivandrum": "thiruvananthapuram", "cochin": "kochi", "pondicherry": "puducherry", "benares": "varanasi", "banaras": "varanasi"}


def _norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower().strip()
    return " ".join(s.replace(",", " ").split())


def lookup(name, country=None, limit=5):
    """Candidates sorted by population: [{name, country, admin, lat, lon, tz, population}]. Empty list if unknown."""
    try:
        import geonamescache
    except ImportError as e:                                  # pragma: no cover
        raise RuntimeError("pip install geonamescache --break-system-packages") from e
    key = _norm(name.split(",")[0]); key = ALIASES.get(key, key)
    out = []
    for c in geonamescache.GeonamesCache().get_cities().values():
        names = {_norm(c["name"])} | {_norm(a) for a in c.get("alternatenames", []) if a}
        if key in names and (country is None or c["countrycode"] == country.upper()):
            out.append({"name": c["name"], "country": c["countrycode"], "admin": c.get("admin1code"),
                        "lat": round(float(c["latitude"]), 4), "lon": round(float(c["longitude"]), 4),
                        "tz": c.get("timezone"), "population": c.get("population", 0)})
    out.sort(key=lambda x: -x["population"])
    return out[:limit]


def resolve(name, country=None):
    """Best single match or None. More than one candidate in different countries is reported in 'ambiguous'."""
    c = lookup(name, country)
    if not c: return None
    best = dict(c[0]); best["ambiguous"] = [f"{x['name']}, {x['country']}" for x in c[1:] if x["country"] != c[0]["country"]]
    return best


if __name__ == "__main__":
    for x in lookup(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None): print(x)
