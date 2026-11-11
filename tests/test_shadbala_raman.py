"""Second, independent Shadbala reference: B.V. Raman's standard horoscope (Graha and Bhava Balas),
16 Oct 1918, 2:20 pm IST, 13N 77E35, with Raman's ayanamsa. Component totals as reproduced at
https://vedastro.org/blog/Graha-Bhava-Balas-Part-12-Total-Planetary-Strength.html (read 12 Nov 2026).
Cheshta and Drik from that page are not used: the page prints a Cheshta of 63.4, above the maximum of 60."""
from engine import ephemeris as E
from engine.shadbala import shadbala

P = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
STHANA = [198.0, 126.5, 172.1, 279.5, 157.6, 178.2, 177.3]
DIG = [48.1, 31.6, 55.1, 21.1, 11.5, 15.2, 58.0]
KALA = [103.0, 202.0, 30.2, 192.8, 211.2, 115.5, 117.0]


def _run():
    E.set_ayanamsa("raman")
    try:
        return shadbala("1918-10-16", "14:20", 13.0, 77.5833, 5.5)
    finally:
        E.set_ayanamsa("lahiri")


def test_sthana_bala_identical_to_raman():
    r = _run()
    for p, ref in zip(P, STHANA):
        assert abs(r["planets"][p]["sthana_total"] - ref) <= 0.15, (p, r["planets"][p]["sthana_total"], ref)


def test_dig_and_kala_bala_match_raman():
    r = _run()
    for p, d, k in zip(P, DIG, KALA):
        assert abs(r["planets"][p]["dig"] - d) <= 0.7, (p, "dig")
        assert abs(r["planets"][p]["kala_total"] - k) <= 0.8, (p, "kala", r["planets"][p]["kala_total"], k)


def test_hora_lord_is_running_hora():
    assert _run()["context"]["hora_lord"] == "Moon"
