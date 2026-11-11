"""Tests for engine.astrosage_pdf against the one real AstroSage export we have.

Runs under pytest or `python -m unittest tests.test_astrosage_pdf`.  The sample is
private and not in the repo: set ASTROSAGE_SAMPLE_PDF, or the default path below
is used; everything that needs it is skipped cleanly when it is missing.
Expected values are the ones PRINTED in the PDF (dd-mm-ss), not rounded notes.
"""
import os
import shutil
import unittest

from engine import astrosage_pdf as A

SAMPLE = os.environ.get(
    "ASTROSAGE_SAMPLE_PDF",
    "/mnt/user-data/attachments/248c584f-379b-52a0-9ee9-8d0937c5f97e/cbc29bb5-Tanzil.pdf")
HAVE = os.path.exists(SAMPLE) and bool(shutil.which("pdftotext"))


class Helpers(unittest.TestCase):
    def test_sign_names(self):
        for tok, want in [("Scorpion", "Scorpio"), ("Vrishchika", "Scorpio"), ("Vrishabha", "Taurus"),
                          ("Mesh", "Aries"), ("Makara", "Capricorn"), ("CAP", "Capricorn"), ("Can", "Cancer"),
                          ("Sc", "Scorpio"), ("Sag", "Sagittarius"), ("Kumbha", "Aquarius"), ("Meena", "Pisces"),
                          ("Simha", "Leo"), ("Tula", "Libra"), ("Dhanu", "Sagittarius"), (10, "Capricorn")]:
            self.assertEqual(A.sign_name(tok), want, tok)
        self.assertIsNone(A.sign_name("Hello"))

    def test_degree_formats(self):
        want = 27 + 6 / 60 + 12 / 3600
        for s in ("27-06-12", "27°06'12\"", "27:06:12", "27.06.12"):
            self.assertAlmostEqual(A.dms(s), want, places=5)
        self.assertAlmostEqual(A.dms("27°06'"), 27.1, places=5)

    def test_planet_names_and_geo(self):
        self.assertEqual([A.planet_name(x) for x in ("ASC", "Satn", "MON", "Merc", "Jupt", "Ra")],
                         ["Lagna", "Saturn", "Moon", "Mercury", "Jupiter", "Rahu"])
        self.assertAlmostEqual(A._geo("15 : 20 : N"), 15.3333, places=3)
        self.assertAlmostEqual(A._geo("75.8.W"), -75.1333, places=3)

    def test_absent_sections_are_none(self):
        d = A.parse_pages(["nothing useful here", ""])
        for k in ("birth", "planets", "vargas", "shadbala", "bhava_bala", "ashtakavarga", "kp", "jaimini",
                  "vimshottari"):
            self.assertIsNone(d[k], k)


@unittest.skipUnless(HAVE, "sample AstroSage PDF (or pdftotext) not available")
class Sample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = A.parse(SAMPLE)

    def deg(self, body, sign, text):
        p = self.d["planets"][body]
        self.assertEqual(p["sign"], sign, body)
        self.assertAlmostEqual(p["degree"], A.dms(text), places=4, msg=body)

    def test_birth(self):
        b = self.d["birth"]
        self.assertEqual((b["date"], b["time"], b["place"], b["sex"]), ("1996-11-24", "12:05:00", "Hubli", "Female"))
        self.assertAlmostEqual(b["lat"], 15 + 20 / 60, places=3)
        self.assertAlmostEqual(b["lon"], 75 + 8 / 60, places=3)
        self.assertEqual(b["tz"], 5.5)
        self.assertEqual(b["ayanamsa"]["name"], "Lahiri")
        self.assertAlmostEqual(b["ayanamsa"]["value"], A.dms("23-48-47"), places=4)
        self.assertEqual((b["sunrise"], b["sunset"]), ("06:36:05", "17:56:19"))

    def test_avakahada(self):
        a = self.d["avakahada"]
        want = dict(tithi="Purnima", paksha="Shukla", yoga="Parigha", karana="Vishti", nakshatra="Krittika", pada=1,
                    varna="Kshatriya", vashya="Chatu", yoni="Mesha", gana="Rakshas", nadi="Antya",
                    moon_sign="Aries", lagna="Capricorn", lagna_lord="Sat", nakshatra_lord="Sun")
        self.assertEqual({k: a[k] for k in want}, want)

    def test_planets(self):
        for body, sign, text in [("Lagna", "Capricorn", "27-05-56"), ("Sun", "Scorpio", "08-27-33"),
                                 ("Moon", "Aries", "27-33-49"), ("Mars", "Leo", "19-22-34"),
                                 ("Mercury", "Scorpio", "20-53-53"), ("Jupiter", "Sagittarius", "23-12-37"),
                                 ("Venus", "Libra", "07-41-23"), ("Saturn", "Pisces", "06-51-39"),
                                 ("Rahu", "Virgo", "11-14-08"), ("Ketu", "Pisces", "11-14-08")]:
            self.deg(body, sign, text)
        p = self.d["planets"]
        self.assertEqual((p["Moon"]["nakshatra"], p["Moon"]["pada"]), ("Krittika", 1))
        self.assertTrue(p["Saturn"]["retrograde"])
        self.assertFalse(p["Sun"]["retrograde"])
        self.assertEqual([p[k]["house"] for k in ("Lagna", "Sun", "Moon", "Mars", "Saturn")], [1, 11, 4, 8, 3])
        self.assertIsNone(p["Sun"]["combust"])  # not printed in this export
        self.assertEqual(p["Moon"]["status"]["deeptadi"], "Muditha")

    def test_vargas(self):
        v = self.d["vargas"]
        self.assertEqual(sorted(v, key=lambda k: int(k[1:])),
                         ["D1", "D2", "D3", "D4", "D7", "D9", "D10", "D12", "D16", "D20", "D24", "D27", "D30",
                          "D40", "D45", "D60"])
        for body, rec in self.d["planets"].items():  # D1 row must agree with the planets table
            self.assertEqual(v["D1"][body], rec["sign"], body)
        self.assertEqual((v["D9"]["Lagna"], v["D9"]["Moon"], v["D10"]["Sun"], v["D60"]["Ketu"]),
                         ("Virgo", "Sagittarius", "Virgo", "Capricorn"))

    def test_shadbala_and_bhava_bala(self):
        s, b = self.d["shadbala"], self.d["bhava_bala"]
        self.assertEqual(list(s), ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"])
        self.assertEqual(s["Moon"]["rupas"], 7.93)
        self.assertEqual((s["Moon"]["total"], s["Moon"]["sthana"], s["Moon"]["rank"]), (475.81, 196.94, 2))
        self.assertEqual((s["Saturn"]["drik"], s["Mercury"]["min_required"], s["Sun"]["ratio"]), (-22.4, 7, 1.41))
        self.assertEqual(len(s["Sun"]["rows"]), 25)
        for rec in s.values():  # six totals add up to the printed Shad Bala
            parts = sum(rec[k] for k in ("sthana", "dig", "kala", "cheshta", "naisargika", "drik"))
            self.assertAlmostEqual(parts, rec["total"], delta=0.06)
        self.assertEqual(sorted(b), list(range(1, 13)))
        self.assertEqual((b[7]["total"], b[7]["rupas"], b[7]["rank"], b[5]["drishti"]), (526.81, 8.78, 1, -61.43))

    def test_ashtakavarga(self):
        a = self.d["ashtakavarga"]
        self.assertEqual(list(a["sav"].values()), [27, 27, 35, 24, 29, 36, 29, 30, 19, 29, 25, 27])
        self.assertEqual(a["sav_total"], 337)
        self.assertEqual(len(a["bav"]), 7)
        for i, sign in enumerate(A.SIGNS):
            self.assertEqual(sum(a["bav"][p][sign] for p in a["bav"]), a["sav"][sign])
        for planet, grid in a["prastara"].items():  # each prastara grid sums to its BAV row
            self.assertEqual(len(grid), 8, planet)
            cols = [sum(row[i] for row in grid.values()) for i in range(12)]
            self.assertEqual(cols, list(a["bav"][planet].values()), planet)

    def test_kp(self):
        k = self.d["kp"]
        c7 = k["cusps"][7]
        self.assertEqual((c7["sign"], c7["star_lord"], c7["sub_lord"]), ("Cancer", "Mercury", "Jupiter"))
        self.assertAlmostEqual(c7["degree"], A.dms("27-11-20"), places=4)
        self.assertEqual(len(k["cusps"]), 12)
        self.assertEqual((k["planets"]["Moon"]["star_lord"], k["planets"]["Moon"]["sub_lord"]), ("Sun", "Moon"))
        self.assertEqual(k["ayanamsa"]["name"], "K. P. New")
        self.assertAlmostEqual(k["ayanamsa"]["value"], A.dms("23-43-23"), places=4)
        self.assertEqual(k["house_significators"][10], ["Sun", "Moon", "Mars", "Mercury"])
        self.assertEqual(k["planet_significations"]["Mars"], [3, 4, 7, 9, 10])

    def test_jaimini(self):
        j = self.d["jaimini"]
        self.assertEqual((j["chara_karakas"]["AK"], j["chara_karakas"]["DK"]), ("Moon", "Saturn"))
        self.assertEqual(len(j["chara_karakas"]), 7)
        self.assertIsNone(j["arudha_padas"])

    def test_vimshottari(self):
        v = self.d["vimshottari"]
        bal = v["balance"]
        self.assertEqual((bal["lord"], bal["years"], bal["months"], bal["days"]), ("Sun", 5, 7, 4))
        md = v["mahadashas"]
        self.assertEqual([m["lord"] for m in md],
                         ["Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury", "Ketu", "Venus"])
        self.assertEqual((md[0]["start"], md[0]["end"], md[-1]["end"]), ("1996-11-24", "2002-06-29", "2116-06-29"))
        for m in md:
            self.assertEqual(len(m["antardashas"]), 9, m["lord"])
            self.assertEqual(m["antardashas"][-1]["end"], m["end"], m["lord"])
        self.assertEqual(md[1]["antardashas"][0], {"lord": "Moon", "end": "2003-04-29"})

    def test_doshas(self):
        z = self.d["doshas"]
        self.assertEqual((z["manglik"]["from_lagna"], z["manglik"]["from_moon"]), (True, False))
        self.assertFalse(z["kaal_sarp"]["present"])
        ss = z["sade_sati"]
        self.assertEqual([r["n"] for r in ss], list(range(1, 43)))
        self.assertEqual((ss[0]["start"], ss[0]["end"], ss[0]["phase"], ss[0]["saturn_sign"]),
                         ("1996-02-17", "1998-04-17", "Rising", "Pisces"))
        self.assertEqual((ss[4]["start"], ss[4]["end"], ss[4]["type"]), ("2004-09-06", "2005-01-13", "Small Panoti"))
        self.assertEqual((ss[39]["start"], ss[39]["end"]), ("2102-12-03", "2105-11-29"))
        for r in ss:
            self.assertTrue(r["start"] and r["end"] and r["start"] < r["end"], r)

    def test_raw_sections(self):
        r = self.d["raw_sections"]
        self.assertEqual(r["Shodashvarga Table"], [39])
        self.assertEqual(r["Sadesati Report"], [10, 11, 12, 13])
        self.assertIn(49, next(v for k, v in r.items() if k.startswith("Shadbala")))

    def test_crosscheck(self):
        try:
            cc = A.crosscheck(self.d)
        except ImportError as e:
            self.skipTest("ephemeris backend missing: %s" % e)
        self.assertEqual(set(cc["bodies"]), {"Lagna"} | set(A.PLANETS))
        for body, rec in cc["bodies"].items():
            self.assertLessEqual(abs(rec["diff_arcmin"]), 5.0, body)
        self.assertTrue(cc["vimshottari_balance"]["pass"])
        self.assertTrue(cc["ok"])


if __name__ == "__main__":
    unittest.main()
