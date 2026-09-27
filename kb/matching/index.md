# Kundli Milan — marriage, business, family

## A. Marriage (Ashtakoota / Guna Milan, North Indian, 36 points)
Computed by `engine/matching.py`. Order of weight:

| Koota | Max | Tests | Zero means |
|---|---|---|---|
| Varna | 1 | Spiritual/ego compatibility; girl's varna ≤ boy's | Ego clash (minor) |
| Vashya | 2 | Mutual attraction/control between Moon-sign classes | One dominates |
| Tara | 3 | Nakshatra count both ways; 3/5/7 (Vipat, Pratyari, Naidhana) bad | Health/fortune drain |
| Yoni | 4 | Sexual/instinctive compatibility (animal + gender) | Enemy yonis — intimacy friction |
| Graha Maitri | 5 | Friendship of Moon-sign lords — temperament, mental rapport | Opposing temperaments |
| Gana | 6 | Deva/Manushya/Rakshasa — nature | Rakshasa × Deva/Manushya — deep conflict |
| Bhakoot | 7 | Moon-sign distance — 6/8 (Shadashtak: health/death), 2/12 (Dwirdwadash: finance), 5/9 (Navpancham: progeny) | Structural dosha |
| Nadi | 8 | Adi/Madhya/Antya — health of progeny, genetic; same nadi = dosha | Nadi dosha — heaviest |

**Score reading**: <18 not recommended · 18–24 acceptable · 25–32 very good · 33–36 excellent. **But**: a 30/36 with Nadi dosha or Bhakoot 0 and no cancellation is worse than a 22 with all kootas non-zero. Nadi dosha is the one matchmakers most commonly refuse on; Bhakoot next.

**Nadi dosha cancellations**: same rashi different nakshatra; same nakshatra different rashi; same nakshatra different pada (some); Moon-sign lords same or friends and Bhakoot passes; either partner's Moon in own/exalted with Jupiter aspect. **Bhakoot cancellation**: rashi lords same/friendly; both Moons in the same navamsa lord's signs.

## B. Beyond guna milan — what a good astrologer actually checks (the score is 30% of the decision)
1. **Manglik status both sides** — match or cancel. One-sided uncancelled Mangal dosha, esp. from lagna in 7th/8th, is a harder stop than a low guna score.
2. **7th house of each chart** — sign, lord placement/dignity, malefics in 7th, 7L in 6/8/12, Venus (m) / Jupiter (f) condition, D9 lagna and 7th. Each chart must *individually* promise a stable marriage before comparison means anything.
3. **Longevity & health** — 8th house, lagna strength, marakas; classical check that one partner's chart does not show widowhood periods (Saturn/Mars/Rahu in 7th/8th, 7L in 8th) uncancelled.
4. **Dasha overlap** — both partners' upcoming 10–15 years. Avoid marriage at dasha sandhi. If one enters Rahu/Saturn dasha of a 6/8/12 lord as the other enters Venus/Jupiter of a good lord, expect asymmetry.
5. **Synastry** (chart-to-chart): boy's 7L sign vs girl's Moon/lagna; Venus of one on Moon/lagna of other (attraction); Saturn of one on Moon/lagna/Venus of other (restriction, or durability if benign); Rahu of one on 7th of other (obsession/foreignness); Jupiter of one on lagna/7th/Moon of other (protection). Lagnas in 1/7, 3/11, 5/9 from each other are harmonious; 6/8 and 2/12 are not.
6. **Progeny** — 5th houses, Jupiter, D7 of both.
7. **Family** — 2nd (family), 4th (home/mother-in-law dynamics), 9th (father-in-law, dharma).
8. **Rectification caution** — guna milan is Moon-based; a Moon within 2° of a rashi/nakshatra boundary makes the whole score unreliable. Flag it.

## C. South Indian Dashakoota (10 kootas, Tamil/Kerala practice)
Dina (Tara), Gana, Mahendra (progeny; boy's star 4/7/10/13/16/19/22/25 from girl's), Stree-Deergha (boy's star >13 from girl's), Yoni, Rasi (Bhakoot), Rasyadhipati (Graha Maitri), Vashya, Rajju (most important — same rajju = widowhood risk; Pada/Kati/Ura/Kantha/Shiro), Vedha (specific enemy star pairs). Weights vary; Rajju and Vedha are pass/fail.

## D. Business partnership
No classical koota system — traditional astrologers use the following (implemented as factors in `business_synastry`):
- **Each chart alone**: 7th house (partnerships) and 7L must be sound; 2/11 for wealth; 10 for execution; Mercury (trade) and Jupiter (capital/wisdom) dignity; 6th for competition/debt tolerance; 8th afflicted = sudden reversals, litigation.
- **Between charts**: lagnas 3/11 or 5/9 or 1/7 apart = complementary; 6/8 = friction; 2/12 = one funds, other drains. Lagna lords friendly. One's benefics (Jupiter/Venus/Mercury/Moon) falling in the other's 11th/2nd/10th = mutual gain. One's Saturn on the other's Moon/lagna = control/burden (can also be "the disciplined one" if the pair needs it). One's Rahu on the other's 7th/10th/2nd = ambition-driven but risk of deception. Mars-Mars in 6/8 = quarrels.
- **Role fit**: the stronger 10th/Sun = face/CEO; stronger 2nd/Mercury/Jupiter = finance; stronger 3rd/Mars = operations/sales; stronger 4th = property/infra; stronger 9th/12th/Rahu = foreign markets.
- **Timing**: both in supportive dashas (lords of 1/2/5/9/10/11 or yogakaraka) at formation; incorporate on a Mercury/Jupiter-hora muhurta, avoid Rahu kaal and Bhadra.
- **Exit signals**: one partner entering an 8L/12L or afflicted Rahu dasha while the venture is young.

## E. Family / parent–child / sibling
- Parent–child: parent's 5th/9th vs child's lagna/Moon; child's 4th (mother) / 9th (father) condition; mutual Moon distances (1/7, 3/11, 5/9 harmonious). Same-nadi between parent and child is *not* a dosha.
- Siblings: 3rd (younger) / 11th (elder) of each; Mars condition.
- Joint family / in-laws: 4th (spouse's 10th = in-laws' status), 8th (in-laws' wealth), 2nd (family).
