"""Rules coded from Parashara ch. 3, 31, 39, 42, 45, 74 and Phaladeepika 25 (engine/parashara_extra.py)."""
from engine.chart import build_chart
from engine import parashara_extra as X

C = build_chart("1987-02-03", "06:28", 15.36, 75.12, "Asia/Kolkata")          # Monday night (before sunrise on Tuesday)


def test_nine_states_one_base_state_each():
    ns = X.nine_states(C)
    assert set(ns) == set(X.SEVEN)
    assert ns["Jupiter"]["state"].startswith("at ease")                       # Jupiter in Pisces, own sign
    assert all(x["state"].split(" (")[0] in ("blazing", "at ease", "glad", "calm", "poor", "distressed") for x in ns.values())


def test_six_moods_rules():
    mo = X.six_moods(C)
    assert "glad" in mo["Moon"]["moods"]                                      # with Jupiter
    assert all(set(x["moods"]) <= {"ashamed", "proud", "hungry", "thirsty", "glad", "agitated"} for x in mo.values())
    assert not mo["Moon"]["harms_house"]


def test_argala_counts_and_obstruction():
    ag = X.argala(C)
    for h in range(1, 13):
        for f in ag[h]["formed"]:
            assert f.get("reverse") or len(f["obstructed_by"]) < len(f["planets"])     # BPHS 31.4: fewer obstructors do not count
        for b in ag[h]["blocked"]:
            assert len(b["obstructed_by"]) >= len(b["planets"])
        assert (ag[h]["grade"] is None) == (not ag[h]["planets"])


def test_non_luminous_points_close_on_the_sun():
    u = X.upagrahas(C); sun = C["planets"]["Sun"]["lon"]
    assert abs((u["non_luminous"]["Upaketu"]["lon"] + 30.0 - sun + 180) % 360 - 180) < 0.02   # BPHS 3.65: one sign more gives back the Sun
    assert abs((u["non_luminous"]["Dhuma"]["lon"] - sun) % 360 - 133.333) < 0.02


def test_gulika_part_by_weekday_and_mandi_near_its_end():
    u = X.upagrahas(C)
    assert u["day_birth"] is False
    assert u["gulika_group"]["Gulika"]["part"] == 2                           # Monday night starts from Venus (fifth from the Moon), then Saturn
    assert u["mandi_group_pd"]["Mandi"]["ghatis"] == 6                        # PD 25.2: Friday's figure, the fifth lord from Monday
    g = u["gulika_group"]["Gulika"]; m = u["mandi_group_pd"]["Mandi"]["lon"]
    span = (g["at_end"]["lon"] - g["at_start"]["lon"]) % 360
    assert 0 < (m - g["at_start"]["lon"]) % 360 < span                        # Mandi lies inside Saturn's part, near its end
    d = build_chart("2024-06-15", "12:00", 15.36, 75.12, "Asia/Kolkata")      # a Saturday, by day
    ud = X.upagrahas(d)
    assert ud["day_birth"] and ud["gulika_group"]["Gulika"]["part"] == 1 and ud["mandi_group_pd"]["Mandi"]["ghatis"] == 2


def test_sudarshana_table_cycles_every_twelve_years():
    t = X.sudarshana_table(C, 39, 13)["rows"]
    assert t[0]["house"] == 4 and t[12]["house"] == 4 and t[0]["lagna"]["sign"] == t[12]["lagna"]["sign"]
    assert X.sudarshana_table(C, 39)["applies"] is False                      # lagna and Sun share Capricorn


def test_activity_states_are_named():
    a = X.activity_states(C)
    assert len(a) == 9 and all(v in X.SHAYANADI for v in a.values())


def test_sun_required_strength_follows_the_texts():
    from engine.shadbala import shadbala
    sb = shadbala("1987-02-03", "06:28", 15.36, 75.12)["planets"]
    assert sb["Sun"]["required"] == 5.0 and sb["Sun"]["required_text"] == 6.5          # Raman/AstroSage vs BPHS 27.32, JP 2.40
    assert abs(sb["Sun"]["ratio_text"] - sb["Sun"]["rupas"] / 6.5) < 1e-9
    assert sorted(x["rank_text"] for x in sb.values()) == list(range(1, 8))
    ps = shadbala("1987-02-03", "06:28", 15.36, 75.12, compat="parashara")["planets"]
    assert any(abs(ps[p]["rupas"] - sb[p]["rupas"]) > 0.01 for p in sb)                # BPHS 27.2-3 scale changes some totals


def test_new_yoga_ids_are_catalogued():
    from engine.analysis import analyse
    from engine.yogas_extra import detect, catalogue, coverage
    ids = {x["id"] for x in detect(analyse(C, sex="M")["view"])}
    assert ids <= set(catalogue()) and coverage()["not_coded"] == {}
    assert {"rj_arudha_pair", "dhana_loss_dasha"} <= ids
