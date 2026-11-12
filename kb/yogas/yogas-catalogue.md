# Yogas catalogue (Parashari, Lahiri, whole-sign)

> **Project calibration.** A yoga counts only at the strength of its planets. In our verified charts, own-sign/exalted planets in the 7th from the Moon (Ruchaka/Shasha from Chandra lagna) showed up as pressure on marriage, not as a blessing; and one dignified occupant did not outvote three malefic influences on the same house.

Total entries: **160** (machine copy: `yogas.json`, same ids). Entries marked `[unverified]` were written from working knowledge of the named text and were not re-read online this session.

## Conventions for the engine
- Houses are whole-sign, counted inclusively from the stated reference (Lagna, Moon, Sun, or a lord's sign). "House 7 from Moon" = the 7th sign from the Moon's sign.
- Kendra = 1/4/7/10; trikona = 1/5/9; dusthana = 6/8/12; upachaya = 3/6/10/11; panaphara = 2/5/8/11; apoklima = 3/6/9/12.
- Natural benefics: Jupiter, Venus, Mercury (when not joined to a malefic), waxing Moon. Natural malefics: Sun, Mars, Saturn, Rahu, Ketu, waning Moon, afflicted Mercury.
- Aspects (Parashari): every planet aspects the 7th sign from itself; Mars also 4th and 8th; Jupiter 5th and 9th; Saturn 3rd and 10th. Rahu/Ketu aspects (5/7/9) are a later convention - flag when used.
- Exaltation / debilitation signs: Sun Aries/Libra; Moon Taurus/Scorpio; Mars Capricorn/Cancer; Mercury Virgo/Pisces; Jupiter Cancer/Capricorn; Venus Pisces/Virgo; Saturn Libra/Aries.
- Unless a rule names Rahu/Ketu, lunar/solar/Nabhasa yogas use only the seven planets Sun..Saturn.
- Every hit should be scored: dignity of each participant, house from Lagna, combustion, aspects received, D9 confirmation, and whether the relevant dasha falls in a usable age. Report weak hits as 'present but weak'.

## Scoring ladder (apply to every yoga)
1. All participants own/exalted, in kendra/trikona, unafflicted, confirmed in D9 -> full.
2. Mixed dignity or one affliction -> partial.
3. Any participant debilitated without bhanga, combust, or in 6/8/12 -> nominal.
4. Three or more independent malefic influences on the house the yoga is supposed to bless -> the afflictions win (project calibration).


## Pancha Mahapurusha (5)

### Ruchaka yoga  `ruchaka`
- **Condition:** Mars in Aries, Scorpio (own) or Capricorn (exalted) AND Mars in house 1/4/7/10 counted from Lagna. (Variant: Phaladeepika ch. 6 and later authors also allow the count from the Moon.)
- **Strength:** The verse requires the planet to be strong (balibhih) as well as in own sign or exaltation in a kendra. The count from the Moon is not in Parashara.
- **Cancellation:** Texts give no formal bhanga; practice treats it as void/weak if the planet is combust, defeated in war, debilitated in navamsa, conjunct or closely aspected by malefics/Rahu-Ketu, or (Phaladeepika tradition) if Sun or Moon are both weak.
- **Result:** Native bold, victorious, commander-like, fond of contest; scarred or ruddy body. BPHS adds region ruled and life span.
- **Source:** BPHS ch. 75 vv.1-2 (Sanskrit text at sanskritdocuments.org, read and translated 12 Nov 2026; see kb/sources/bphs-verse-readings.md)

### Bhadra yoga  `bhadra`
- **Condition:** Mercury in Gemini (own) or Virgo (own/exalted) AND Mercury in house 1/4/7/10 counted from Lagna. (Variant: Phaladeepika ch. 6 and later authors also allow the count from the Moon.)
- **Strength:** The verse requires the planet to be strong (balibhih) as well as in own sign or exaltation in a kendra. The count from the Moon is not in Parashara.
- **Cancellation:** Texts give no formal bhanga; practice treats it as void/weak if the planet is combust, defeated in war, debilitated in navamsa, conjunct or closely aspected by malefics/Rahu-Ketu, or (Phaladeepika tradition) if Sun or Moon are both weak.
- **Result:** Native learned, articulate, sattvic, long-lived, comfortable. BPHS adds region ruled and life span.
- **Source:** BPHS ch. 75 vv.1-2 (Sanskrit text at sanskritdocuments.org, read and translated 12 Nov 2026; see kb/sources/bphs-verse-readings.md)

### Hamsa yoga  `hamsa`
- **Condition:** Jupiter in Sagittarius, Pisces (own) or Cancer (exalted) AND Jupiter in house 1/4/7/10 counted from Lagna. (Variant: Phaladeepika ch. 6 and later authors also allow the count from the Moon.)
- **Strength:** The verse requires the planet to be strong (balibhih) as well as in own sign or exaltation in a kendra. The count from the Moon is not in Parashara.
- **Cancellation:** Texts give no formal bhanga; practice treats it as void/weak if the planet is combust, defeated in war, debilitated in navamsa, conjunct or closely aspected by malefics/Rahu-Ketu, or (Phaladeepika tradition) if Sun or Moon are both weak.
- **Result:** Native righteous, respected, handsome, teacher/adviser status. BPHS adds region ruled and life span.
- **Source:** BPHS ch. 75 vv.1-2 (Sanskrit text at sanskritdocuments.org, read and translated 12 Nov 2026; see kb/sources/bphs-verse-readings.md)

### Malavya yoga  `malavya`
- **Condition:** Venus in Taurus, Libra (own) or Pisces (exalted) AND Venus in house 1/4/7/10 counted from Lagna. (Variant: Phaladeepika ch. 6 and later authors also allow the count from the Moon.)
- **Strength:** The verse requires the planet to be strong (balibhih) as well as in own sign or exaltation in a kendra. The count from the Moon is not in Parashara.
- **Cancellation:** Texts give no formal bhanga; practice treats it as void/weak if the planet is combust, defeated in war, debilitated in navamsa, conjunct or closely aspected by malefics/Rahu-Ketu, or (Phaladeepika tradition) if Sun or Moon are both weak.
- **Result:** Native refined, attractive, learned, vehicles and comforts, happy spouse. BPHS adds region ruled and life span.
- **Source:** BPHS ch. 75 vv.1-2 (Sanskrit text at sanskritdocuments.org, read and translated 12 Nov 2026; see kb/sources/bphs-verse-readings.md)

### Shasha (Sasa) yoga  `shasha`
- **Condition:** Saturn in Capricorn, Aquarius (own) or Libra (exalted) AND Saturn in house 1/4/7/10 counted from Lagna. (Variant: Phaladeepika ch. 6 and later authors also allow the count from the Moon.)
- **Strength:** The verse requires the planet to be strong (balibhih) as well as in own sign or exaltation in a kendra. The count from the Moon is not in Parashara.
- **Cancellation:** Texts give no formal bhanga; practice treats it as void/weak if the planet is combust, defeated in war, debilitated in navamsa, conjunct or closely aspected by malefics/Rahu-Ketu, or (Phaladeepika tradition) if Sun or Moon are both weak.
- **Result:** Native authority over many, organiser, fond of wilds/solitude, takes what belongs to others. BPHS adds region ruled and life span.
- **Source:** BPHS ch. 75 vv.1-2 (Sanskrit text at sanskritdocuments.org, read and translated 12 Nov 2026; see kb/sources/bphs-verse-readings.md)


## Raja yogas (30)

### Chamara yoga  `chamara`
- **Condition:** (a) Lagna lord exalted, in a kendra, aspected by Jupiter; OR (b) two benefics together in house 1, 7, 9 or 10.
- **Cancellation:** None formal.
- **Result:** King or honoured by the king; eloquent, learned, long-lived.
- **Source:** BPHS ch. 36 vv.11-12 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Mridanga yoga  `mridanga`
- **Condition:** Lagna lord strong AND the other planets in kendras/trikonas in own or exalted signs.
- **Cancellation:** Weak Lagna lord.
- **Result:** King or equal to a king, happy.
- **Source:** BPHS 36.17 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/bphs/)

### Shrinatha yoga  `shrinatha`
- **Condition:** 7th lord exalted in the 10th house, and the 10th lord joined by the 9th lord (BPHS 36.18, Sanskrit read 12 Nov 2026).
- **Cancellation:** None formal.
- **Result:** Equal to Indra; great prosperity.
- **Source:** BPHS ch. 36 v.18 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Kurma yoga  `kurma`
- **Condition:** Benefics in houses 5, 6, 7 in own/exalted/friendly signs AND malefics in houses 1, 3, 11 in own/exalted signs.
- **Cancellation:** None formal.
- **Result:** King/leader, virtuous, grateful, happy.
- **Source:** BPHS ch. 36 vv.23-24 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Kusuma yoga  `kusuma`
- **Condition:** Lagna in a fixed sign, Venus in a kendra, Moon in a trine with a benefic, Saturn in house 10.
- **Cancellation:** None formal.
- **Result:** King or equal, charitable, head of clan.
- **Source:** BPHS ch. 36 vv.29-30 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Kalpadruma (Parijata) yoga  `kalpadruma`
- **Condition:** Lagna lord, the lord of its sign, the lord of that one's sign, and the lord of that one's navamsa: each in a kendra, a trine or its own exaltation (BPHS 36.33, Sanskrit read 12 Nov 2026).
- **Cancellation:** Any link in 6/8/12 or debilitated.
- **Result:** Wealthy, king-like, pious, strong, fond of battle yet merciful.
- **Source:** BPHS ch. 36 vv.33-34 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Kendra-Trikona raja yoga  `kendra_trikona_raja`
- **Condition:** A lord of a kendra (1/4/7/10) and a lord of a trikona (1/5/9) are (a) conjunct in one sign, OR (b) in mutual aspect, OR (c) exchange signs. Lagna lord counts as both.
- **Strength:** Rank: 9th+10th > 5th+10th > 9th+4th/7th > others. Stronger in kendra/trikona, in own/exalted signs, repeated in navamsa.
- **Cancellation:** Spoiled when either lord also owns 6/8/12 without redeeming ownership, is debilitated/combust, or the pair sits in 6/8/12; 3rd/11th lord joining dilutes (Laghu Parashari rule, NOT re-read this session (stated from working knowledge of the named text; verify before relying on verse numbers)).
- **Result:** Fame and position 'like a king' in proportion to strength; fructifies in the dasha/antardasha of the two lords.
- **Source:** BPHS ch. 34 vv.11-12 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Yogakaraka (single planet)  `yogakaraka_planet`
- **Condition:** One planet owns both a kendra and a trikona: Mars for Cancer & Leo lagna; Venus for Capricorn & Aquarius; Saturn for Taurus & Libra.
- **Cancellation:** Debilitated, combust or in 6/8/12 it gives little.
- **Result:** That planet alone gives raja-yoga results in its periods.
- **Source:** BPHS ch. 34 v.13 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Rahu/Ketu as yogakaraka  `node_yogakaraka`
- **Condition:** Rahu or Ketu in a kendra AND conjunct/aspected by a trikona lord; or in a trikona AND conjunct/aspected by a kendra lord.
- **Cancellation:** Association with a 6/8/12 lord.
- **Result:** The node gives raja-yoga results in its dasha.
- **Source:** BPHS ch. 34 v.17 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Dharma-Karmadhipati yoga  `dharma_karmadhipati`
- **Condition:** 9th lord and 10th lord conjunct, in mutual aspect, or exchanging signs (9th lord in 10th and 10th lord in 9th).
- **Cancellation:** For lagnas where one of them is also an 8th/11th/12th lord (e.g. Aries: Saturn 10+11; Gemini: Saturn 8+9; Leo: Venus 3+10) the result is mixed.
- **Result:** Highest of the kendra-trikona yogas: rise through one's work in line with dharma; kingdom/high office.
- **Source:** BPHS ch. 39 vv.33-38 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Maha Raja yoga  `maha_raja`
- **Condition:** Lagna lord and 5th lord exchange signs; OR Atmakaraka and Putrakaraka in Lagna/5th in own/exalted sign or aspected by a benefic.
- **Cancellation:** None formal.
- **Result:** Famous and happy.
- **Source:** BPHS ch. 39 vv.6-7 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Lagna lord - 10th lord exchange  `lagna_karma_exchange`
- **Condition:** Lagna lord in house 10 AND 10th lord in house 1.
- **Cancellation:** None formal.
- **Result:** Great royal association; high standing.
- **Source:** BPHS ch. 40 v.13 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Exalted-planet raja yoga  `exalted_count`
- **Condition:** Count planets in exaltation or moolatrikona: 1-3 = king only if born in a ruling family; 4-5 = even a low-born person rises to rule; 6 = emperor.
- **Cancellation:** Exalted planets that are retrograde/combust or in 6/8/12 count less in practice.
- **Result:** Status scaled to the count.
- **Source:** BPHS ch. 39 vv.44-46 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Benefics in kendras, malefics in 3/6/11  `benefic_kendra_malefic_upachaya`
- **Condition:** All benefics in kendras from Lagna AND malefics only in houses 3, 6, 11.
- **Cancellation:** None formal.
- **Result:** Even one of humble birth rises to the throne.
- **Source:** BPHS ch. 39 v.48 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Vargottama Moon aspected by 4+  `moon_vargottama_aspected`
- **Condition:** Moon strong and vargottama (same sign in D1 and D9) AND aspected by four or more planets.
- **Cancellation:** None formal.
- **Result:** Becomes a king.
- **Source:** BPHS ch. 39 v.42 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Akhanda Samrajya yoga  `akhanda_samrajya`
- **Condition:** Jupiter is lord of house 2, 5 or 11 from Lagna (e.g. Taurus lagna: 11th; Leo: 5th; Scorpio: 2nd and 5th; Aquarius: 2nd and 11th - compute from lordship, do not hard-code) AND one of the lords of the 2nd, 9th or 11th is in a kendra from the Moon (Raman: also requires that lord to be strong).
- **Cancellation:** Weak/afflicted Jupiter.
- **Result:** Unbroken, long-lasting authority and wealth.
- **Source:** Phaladeepika 7.25, read in the Sanskrit 12 Nov 2026: one of the lords of the 11th, 9th and 2nd in a kendra from the Moon, with Jupiter as lord of the 2nd, 5th or 11th - 'unbroken sovereignty'

### Moon-Venus 3/11 raja yoga  `venus_moon_3_11`
- **Condition:** Moon and Venus placed in houses 3 and 11 from each other (mutual 3-11) per BPHS wording 'aspecting each other'.
- **Cancellation:** None formal.
- **Result:** Raja yoga.
- **Source:** BPHS ch. 39 v.41 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Raja yoga: 9th lord and Atma-karaka  `rj_ak_l9`
- **Condition:** 9th lord and the Atma-karaka (planet with the most degrees) each in the lagna, 5th or 7th, each joined or aspected by a benefic.
- **Cancellation:** None stated in the verse.
- **Result:** Raja yoga (standing, authority).
- **Source:** BPHS 39.8 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/bphs/)

### Raja yoga: benefics in 2nd, 4th, 5th from lagna lord or Atma-karaka  `rj_benefics_245`
- **Condition:** A benefic in each of the 2nd, 4th and 5th counted from the lagna lord or from the Atma-karaka.
- **Cancellation:** None stated in the verse.
- **Result:** Raja yoga.
- **Source:** BPHS 39.9 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/bphs/)
- **Note:** Engine reading: every one of the three houses must hold a benefic (Moon counted as a benefic).

### Raja yoga: malefics in 3rd and 6th from lagna lord or Atma-karaka  `rj_malefics_36`
- **Condition:** A malefic in both the 3rd and the 6th counted from the lagna lord or from the Atma-karaka.
- **Cancellation:** None stated in the verse.
- **Result:** Raja yoga.
- **Source:** BPHS 39.10 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/bphs/)
- **Note:** Engine reading: both houses must hold a malefic (nodes counted).

### Raja yoga: benefic-benefic-malefic-benefic in houses 1-4  `rj_lagna_row`
- **Condition:** A benefic in the lagna, a benefic in the 2nd, a malefic in the 3rd and a benefic in the 4th.
- **Cancellation:** None stated in the verse.
- **Result:** Raja yoga.
- **Source:** BPHS 39.17 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/bphs/)

### Raja yoga: Jupiter in the 9th in own sign  `rj_jupiter_9`
- **Condition:** Jupiter in the 9th house in Sagittarius or Pisces, together with Venus or with the 5th lord.
- **Cancellation:** None stated in the verse.
- **Result:** Raja yoga.
- **Source:** BPHS 39.39 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/bphs/)

### Raja yoga: one benefic exalted in a kendra  `rj_benefic_exalted_kendra`
- **Condition:** Jupiter, Venus or Mercury exalted in a kendra and joined by another benefic.
- **Cancellation:** None stated in the verse.
- **Result:** Raja yoga from a single planet.
- **Source:** BPHS 39.47 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/bphs/)

### 5th lord in the 10th  `rj_5l_10`
- **Condition:** Lord of the 5th house placed in the 10th.
- **Cancellation:** None stated in the verse.
- **Result:** Parashara calls it a raja yoga: comforts, fame.
- **Source:** BPHS 24.58 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/bphs/)
- **Note:** A single lord placement: by arithmetic about one chart in twelve. Never a distinction on its own.

### 9th lord in the 10th  `rj_9l_10`
- **Condition:** Lord of the 9th house placed in the 10th.
- **Cancellation:** None stated in the verse.
- **Result:** A ruler or like one; a minister or commander; virtuous.
- **Source:** BPHS 24.106 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/bphs/)
- **Note:** A single lord placement: about one chart in twelve.

### Raja yoga: Venus with Jupiter and Moon  `rj_venus_ju_moon`
- **Condition:** Venus in the Karakamsa (navamsa sign of the Atma-karaka) or its 5th, or in the lagna or the arudha of the lagna, joined or aspected by both Jupiter and the Moon.
- **Cancellation:** None stated in the verse.
- **Result:** Raja yoga.
- **Source:** BPHS 39.11 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/bphs/)

### Raja yoga: Moon with a benefic in the arudha  `rj_arudha_moon`
- **Condition:** A benefic with the Moon in the arudha of the lagna, Jupiter in the 2nd from it, the arudha aspected by an exalted planet.
- **Cancellation:** None stated in the verse.
- **Result:** Raja yoga.
- **Source:** BPHS 39.16 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/bphs/)

### Raja yoga: arudhas of the lagna and the 7th  `rj_arudha_pair`
- **Condition:** The arudha of the lagna and the arudha of the 7th in mutual kendras, in the 3rd and 11th, or in trines.
- **Cancellation:** None stated in the verse.
- **Result:** Raja yoga; lasting agreement in partnership.
- **Source:** BPHS 39.23 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/bphs/)
- **Note:** Eight of twelve possible distances qualify, so by arithmetic this holds in roughly two charts in three. It is the absence (2nd-12th or 6th-8th) that says something.

### Raja yoga: exalted planet in the arudha  `rj_arudha_exalted`
- **Condition:** The arudha of the lagna occupied by an exalted planet - the Moon especially - or by Jupiter and Venus together, with no adverse argala.
- **Cancellation:** None stated in the verse.
- **Result:** Raja yoga.
- **Source:** BPHS 39.26-27 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/bphs/)
- **Note:** Engine does not test the 'no adverse argala' clause.

### Raja yoga: one planet on the birth, hora and ghati lagnas  `rj_three_lagnas`
- **Condition:** One planet joining or aspecting the birth lagna, the hora lagna and the ghati lagna; stronger when that planet is exalted.
- **Cancellation:** None stated in the verse.
- **Result:** Raja yoga - full, half or quarter by the fullness of the aspect.
- **Source:** BPHS 39.12-15, 39.24 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/bphs/)
- **Note:** Usable only with a recorded birth time: the ghati lagna moves one sign in 24 minutes. Sign aspects only; the divisional-lagna form of the verse is not tested.


## Dhana yogas (8)

### Vasumati (Dhana) yoga  `vasumati`
- **Condition:** All benefics (Mercury, Jupiter, Venus) in upachaya houses 3/6/10/11 counted from the Moon (B.V. Raman also allows from Lagna).
- **Cancellation:** None formal.
- **Result:** Affluence. Two benefics = medium wealth; one = negligible.
- **Source:** BPHS 37.6 ; Brihat Jataka 13.9 (both read in the Sanskrit, 12 Nov 2026)
- **Note:** Varahamihira gives both forms: all benefics in upachaya houses from the lagna - 'very wealthy'; from the Moon - 'wealthy'; two benefics - middling; fewer - little. The lagna form is his own and the stronger one (it was earlier mislabelled a 'Raman variant'). The name Vasumati is Raman's.

### Chandra-Mangala yoga  `chandra_mangala`
- **Condition:** Moon and Mars in the same sign (some authors also accept mutual 7th aspect).
- **Cancellation:** Afflicted (in 6/8/12, with Saturn/Rahu, or Moon debilitated in Scorpio with Mars) it turns to restlessness and conflict with mother.
- **Result:** Earning drive, wealth through trade, sometimes by unscrupulous means; friction with mother/women.
- **Source:** Phaladeepika 18.2, read in the Sanskrit 12 Nov 2026: the verse for Moon with Mars speaks of trade in drink and vessels and hardship to the mother - it does NOT call it a wealth yoga. The 'wealth' reading is later tradition (Raman); treat as low confidence

### Khadga yoga  `khadga`
- **Condition:** 2nd lord and 9th lord exchange signs AND Lagna lord in a kendra or trikona.
- **Cancellation:** None formal.
- **Result:** Wealthy, learned, skilful, grateful, powerful.
- **Source:** BPHS ch. 36 vv.25-26 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Lakshmi yoga  `lakshmi`
- **Condition:** 9th lord in a kendra from Lagna in its own, moolatrikona or exaltation sign AND Lagna lord strong. (Raman variant: Lagna lord strong and 9th lord in own/exalted sign in kendra or trikona.)
- **Cancellation:** Weak Lagna lord; 9th lord combust/afflicted.
- **Result:** Charming, virtuous, kingly wealth, many sons, fame.
- **Source:** BPHS ch. 36 vv.27-28 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Dhana yoga: own-sign planet in 5th with gainer in 11th  `dhana_5_11`
- **Condition:** House 5 is the own sign of planet X and X sits there, with the paired planet(s) in house 11: Venus(5)+Mars(11); Mercury(5)+Moon,Jupiter(11); Sun in Leo(5)+Saturn,Moon,Jupiter(11); Saturn(5)+Sun,Moon(11); Jupiter(5)+Mercury(11); Mars(5)+Venus(11); Moon in Cancer(5)+Saturn(11).
- **Cancellation:** None formal.
- **Result:** Great affluence.
- **Source:** BPHS ch. 41 vv.2-8 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Dhana yoga: own-sign planet in Lagna  `dhana_lagna_own`
- **Condition:** Lagna is the own sign of planet X, X sits in Lagna, and is joined/aspected by: Sun<-Mars,Jupiter; Moon<-Mercury,Jupiter; Mars<-Mercury,Venus,Saturn; Mercury<-Saturn,Jupiter; Jupiter<-Mercury,Mars; Venus<-Saturn,Mercury; Saturn<-Mars,Jupiter.
- **Cancellation:** None formal.
- **Result:** Wealthy.
- **Source:** BPHS ch. 41 vv.9-15 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Dhana yoga by lordship (2/5/9/11)  `dhana_lords`
- **Condition:** Any conjunction, mutual aspect or exchange between lords of 2nd, 5th, 9th and 11th (and Lagna lord). BPHS: 5th and 9th lords and planets joined to them give wealth in their dashas.
- **Cancellation:** Involvement of 6/8/12 lords or debility reduces it.
- **Result:** Wealth in the dashas of the planets involved.
- **Source:** BPHS 41.16 (the 5th and 9th lords and planets joined to them give wealth in their periods) and Phaladeepika 15-16, both read in the Sanskrit 12 Nov 2026

### Exalted benefic in 2nd  `dhana_benefic_2nd`
- **Condition:** Moon, Jupiter, Venus or Mercury exalted and placed in house 2.
- **Cancellation:** None formal.
- **Result:** Wealthy.
- **Source:** BPHS ch. 39 v.18 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)


## Lunar yogas (incl. Kemadruma and every cancellation) (14)

### Gajakesari yoga  `gajakesari`
- **Condition:** Jupiter in house 1/4/7/10 counted from the Moon (BPHS also allows from Lagna), AND Jupiter aspected/joined by benefics, AND Jupiter not debilitated, not combust, not in an enemy sign.
- **Strength:** Best when Jupiter and Moon are in good houses from Lagna (kendra/trikona), Moon waxing, and either is in own/exalted sign.
- **Cancellation:** Fails or is nominal if Jupiter is debilitated, combust, in inimical sign, or Moon is very weak (dark fortnight near Sun) or both sit in 6/8/12 from Lagna. Common in ~1/3 of charts, so never read alone.
- **Result:** Splendour, intelligence, wealth, virtue, favour of rulers.
- **Source:** BPHS ch. 36 vv.3-4 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Sunapha yoga  `sunapha`
- **Condition:** Any of Mars/Mercury/Jupiter/Venus/Saturn in house 2 counted from the Moon. Sun, Rahu, Ketu do not count.
- **Strength:** Benefic occupant > malefic occupant; result coloured by the occupying planet.
- **Cancellation:** None formal; a malefic alone (Mars/Saturn) gives a harsher version.
- **Result:** Self-earned wealth, intelligence, king-like standing.
- **Source:** BPHS ch. 37 vv.7-10 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 13.3-6 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/)

### Anapha yoga  `anapha`
- **Condition:** Any of Mars/Mercury/Jupiter/Venus/Saturn in house 12 counted from the Moon. Sun, Rahu, Ketu do not count.
- **Cancellation:** None formal.
- **Result:** Good health and presence, reputation, pleasures; later-life detachment.
- **Source:** BPHS ch. 37 vv.7-10 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 13.3-6 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/)

### Durudhara yoga  `durudhara`
- **Condition:** Planets (other than Sun, Rahu, Ketu) in BOTH house 2 and house 12 counted from the Moon.
- **Cancellation:** None formal; two malefics flanking = papa-kartari on the Moon, read as pressure on the mind.
- **Result:** Wealth, conveyances, charity, enjoyment.
- **Source:** BPHS ch. 37 vv.7-10 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 13.3-6 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/)

### Kemadruma yoga  `kemadruma`
- **Condition:** No planet (Sun, Rahu, Ketu not counted) in house 2 or house 12 from the Moon, AND no planet conjunct the Moon, AND (BPHS wording) no planet in a kendra from Lagna.
- **Cancellation:** See kemadruma_bhanga_1..7 (each listed separately).
- **Result:** Poverty of support: reproach, penury, dependence, mental distress, unstable residence even if born well.
- **Source:** BPHS ch. 37 vv.11-13 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)
- **Note:** Brihat Jataka 13.3 (read in the Sanskrit): Kemadruma when no planet other than the Sun is in the 2nd or 12th from the Moon - 'not held when a kendra or the Moon is joined by a planet'. He adds that reckoning it by kendra and navamsa is 'said by some, not established'. Definitions differ: Brihat Jataka/Saravali family also require no planet in a kendra from the Moon before calling it Kemadruma. Engine: compute the strict form (2/12/conjunction empty) then test each bhanga. Jataka Parijata 7.71 adds: the Moon in the lagna or the 7th without Jupiter's aspect is also Kemadruma; 7.82: 'where Kemadruma applies, raja yogas come to nothing'.

### Kemadruma bhanga #1  `kemadruma_bhanga_1`
- **Condition:** Kemadruma present AND: A planet (not Rahu/Ketu) in house 1/4/7/10 counted from the Moon.
- **Cancellation:** n/a (this is itself a cancellation)
- **Result:** Kemadruma is cancelled or reduced; some authors (Jataka Parijata tradition) then call it Kalpadruma, giving rise after early hardship.
- **Source:** Brihat Jataka 13.3 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/) - the cancellation is in the root verse; commentators differ on whether the kendra is counted from the lagna or the Moon, so both are tested

### Kemadruma bhanga #2  `kemadruma_bhanga_2`
- **Condition:** Kemadruma present AND: A planet (not Rahu/Ketu) in house 1/4/7/10 counted from Lagna (BPHS builds this into the definition itself).
- **Cancellation:** n/a (this is itself a cancellation)
- **Result:** Kemadruma is cancelled or reduced; some authors (Jataka Parijata tradition) then call it Kalpadruma, giving rise after early hardship.
- **Source:** BPHS ch. 37 vv.11-13 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Kemadruma bhanga #3  `kemadruma_bhanga_3`
- **Condition:** Kemadruma present AND: Moon itself in house 1/4/7/10 from Lagna.
- **Cancellation:** n/a (this is itself a cancellation)
- **Result:** Kemadruma is cancelled or reduced; some authors (Jataka Parijata tradition) then call it Kalpadruma, giving rise after early hardship.
- **Source:** Brihat Jataka 13.3 on one reading of the verse ('when the Moon is in a kendra, or joined by a planet'); Jataka Parijata 7.80 (read in the Sanskrit, 12 Nov 2026; e-text marked 'needs proofreading'; notes in kb/sources/jataka-parijata/) requires Jupiter's aspect as well

### Kemadruma bhanga #4  `kemadruma_bhanga_4`
- **Condition:** Kemadruma present AND: All planets occupying kendras from Lagna (rare).
- **Cancellation:** n/a (this is itself a cancellation)
- **Result:** Kemadruma is cancelled or reduced; some authors (Jataka Parijata tradition) then call it Kalpadruma, giving rise after early hardship.
- **Source:** No verse found in the texts read in Sanskrit (Parashara, Varahamihira, Mantreshvara, Jataka Parijata ch. 7). A modern list item (satyori.com). Low confidence.

### Kemadruma bhanga #5  `kemadruma_bhanga_5`
- **Condition:** Kemadruma present AND: Moon conjunct or aspected by a strong Jupiter (or strong Venus; Mercury if unafflicted).
- **Cancellation:** n/a (this is itself a cancellation)
- **Result:** Kemadruma is cancelled or reduced; some authors (Jataka Parijata tradition) then call it Kalpadruma, giving rise after early hardship.
- **Source:** Jataka Parijata 7.80-81 (read in the Sanskrit, 12 Nov 2026; e-text marked 'needs proofreading'; notes in kb/sources/jataka-parijata/): the Moon in a kendra, or with a benefic, or in her own, exaltation or great friend's navamsa - in each case aspected by Jupiter
- **Note:** Jataka Parijata names Jupiter's aspect only (and Venus in a kendra with Jupiter's aspect). Venus's or Mercury's aspect on the Moon as a cancellation is a modern extension.

### Kemadruma bhanga #6  `kemadruma_bhanga_6`
- **Condition:** Kemadruma present AND: Moon in own sign (Cancer) or exaltation (Taurus). Some call this only partial relief.
- **Cancellation:** n/a (this is itself a cancellation)
- **Result:** Kemadruma is cancelled or reduced; some authors (Jataka Parijata tradition) then call it Kalpadruma, giving rise after early hardship.
- **Source:** Jataka Parijata 7.81 (read in the Sanskrit, 12 Nov 2026; e-text marked 'needs proofreading'; notes in kb/sources/jataka-parijata/) - but only together with Jupiter's aspect

### Kemadruma bhanga #7  `kemadruma_bhanga_7`
- **Condition:** Kemadruma present AND: Full or near-full Moon (around the 15th tithi); the most contested condition. Later commentaries add: Moon conjunct the Lagna lord.
- **Cancellation:** n/a (this is itself a cancellation)
- **Result:** Kemadruma is cancelled or reduced; some authors (Jataka Parijata tradition) then call it Kalpadruma, giving rise after early hardship.
- **Source:** No verse found in the texts read in Sanskrit (Parashara, Varahamihira, Mantreshvara, Jataka Parijata ch. 7). A modern list item (satyori.com). Low confidence.

### Adhi yoga (Chandradhi)  `adhi_chandra`
- **Condition:** Benefics (Mercury, Jupiter, Venus) in houses 6, 7 and 8 counted from the Moon (all three houses, or the benefics distributed among them).
- **Strength:** Count how many of the three benefics participate and their dignity: 3 strong = top grade.
- **Cancellation:** Weak if the benefics are combust/debilitated or malefics share those houses.
- **Result:** King, minister or army chief according to strength (full / medium / low).
- **Source:** BPHS ch. 37 v.5 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 13.2 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/)

### Moon's house-position from Sun  `chandra_sun_distance`
- **Condition:** Moon in kendra (1/4/7/10) from Sun = low; in panaphara (2/5/8/11) = medium; in apoklima (3/6/9/12) = high.
- **Cancellation:** n/a
- **Result:** Grades wealth, intelligence and skill: little / middling / excellent.
- **Source:** BPHS ch. 37 v.1 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 13.1 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/)


## Solar yogas (4)

### Vesi yoga  `vesi`
- **Condition:** A planet other than the Moon (and not Rahu/Ketu) in house 2 counted from the Sun.
- **Cancellation:** Malefic occupant reverses the result.
- **Result:** Balanced outlook, truthful, somewhat indolent, modest wealth.
- **Source:** BPHS ch. 38 vv.1-4 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Vasi (Vosi) yoga  `vasi`
- **Condition:** A planet other than the Moon (and not Rahu/Ketu) in house 12 counted from the Sun.
- **Cancellation:** Malefic occupant reverses the result.
- **Result:** Skilful, charitable, learned, famous.
- **Source:** BPHS ch. 38 vv.1-4 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Ubhayachari yoga  `ubhayachari`
- **Condition:** Planets other than the Moon in BOTH house 2 and house 12 counted from the Sun.
- **Cancellation:** Malefics on both sides = hemmed Sun (papa-kartari): reverse.
- **Result:** King or equal to a king; well-built, tolerant.
- **Source:** BPHS ch. 38 vv.1-4 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Budha-Aditya (Nipuna) yoga  `budha_aditya`
- **Condition:** Sun and Mercury in the same sign.
- **Cancellation:** Practice: void when Mercury is deeply combust (within ~3 deg; working band 3-14 deg apart preferred), or the pair is in 6/8/12 or in Mercury's/Sun's debilitation.
- **Result:** Intelligence, skill, good reputation.
- **Source:** Phaladeepika 18.1 (Sun with Mercury: skilled, intelligent, famous, happy), read in the Sanskrit 12 Nov 2026. Present in about half of all charts - never a distinction
- **Note:** Mercury is never more than ~28 deg from the Sun, so this occurs in a large share of charts. Low weight.


## Parivartana (exchange) (3)

### Maha parivartana yoga  `maha_parivartana`
- **Condition:** Two planets occupy each other's signs AND both houses are among {1,2,4,5,7,9,10,11} (28 possible pairs).
- **Cancellation:** Weak if either planet is debilitated by the exchange (e.g. Sun-Venus across Libra) or combust.
- **Result:** Wealth, status, benefits of both houses; the two houses work as one.
- **Source:** Phaladeepika 6.32-34 (66 exchanges: 28 maha, 8 khala, 30 dainya), read in the Sanskrit 12 Nov 2026

### Khala parivartana yoga  `khala_parivartana`
- **Condition:** Two planets occupy each other's signs AND one of the two houses is the 3rd while the other is among {1,2,4,5,7,9,10,11} (8 possible pairs).
- **Cancellation:** None formal.
- **Result:** Fluctuating temperament and fortune: sometimes well-behaved and prosperous, sometimes harsh and in difficulty.
- **Source:** Phaladeepika 6.32-33, read in the Sanskrit 12 Nov 2026

### Dainya parivartana yoga  `dainya_parivartana`
- **Condition:** Two planets occupy each other's signs AND at least one of the two houses is 6, 8 or 12 (30 possible pairs).
- **Cancellation:** If BOTH houses are dusthanas (6-8, 6-12, 8-12) many read it as viparita (good).
- **Result:** Foolishness, trouble from enemies, ill health, obstacles to the non-dusthana house.
- **Source:** Phaladeepika 6.32-33, read in the Sanskrit 12 Nov 2026


## Viparita raja yogas (4)

### Dusthana-lord raja yoga (BPHS)  `viparita_bphs`
- **Condition:** Lords of 6th, 8th and 12th debilitated/in inimical signs or combust, while Lagna lord in own/exalted sign aspects Lagna.
- **Cancellation:** Strong dusthana lords.
- **Result:** Becomes a king.
- **Source:** BPHS ch. 39 vv.19-21, 28 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Harsha yoga  `harsha`
- **Condition:** Lord of house 6 placed in house 6, 8 or 12 from Lagna (most authors: best when in its own dusthana or another dusthana, alone, without a non-dusthana lord).
- **Cancellation:** Diluted when the dusthana lord is joined by a kendra/trikona lord (it then damages that lord), or when it also owns a good house (e.g. Jupiter for Leo: 5th+8th).
- **Result:** Fortunate, sturdy, defeats enemies, avoids sin, wealth, fame, sons (v.63).
- **Source:** Phaladeepika ch. 6 vv.57-70 (Sanskrit e-text sanskritdocuments.org phaladIpika.itx, read 12 Nov 2026 - see kb/sources/phaladeepika/)
- **Note:** Formation rule (v.57) is terse on the page read; the house-lord-in-dusthana reading is the standard commentary.

### Sarala yoga  `sarala`
- **Condition:** Lord of house 8 placed in house 6, 8 or 12 from Lagna (most authors: best when in its own dusthana or another dusthana, alone, without a non-dusthana lord).
- **Cancellation:** Diluted when the dusthana lord is joined by a kendra/trikona lord (it then damages that lord), or when it also owns a good house (e.g. Jupiter for Leo: 5th+8th).
- **Result:** Long-lived, resolute, fearless, prosperous, learned, defeats rivals (v.65).
- **Source:** Phaladeepika ch. 6 vv.57-70 (Sanskrit e-text sanskritdocuments.org phaladIpika.itx, read 12 Nov 2026 - see kb/sources/phaladeepika/)
- **Note:** Formation rule (v.57) is terse on the page read; the house-lord-in-dusthana reading is the standard commentary.

### Vimala yoga  `vimala`
- **Condition:** Lord of house 12 placed in house 6, 8 or 12 from Lagna (most authors: best when in its own dusthana or another dusthana, alone, without a non-dusthana lord).
- **Cancellation:** Diluted when the dusthana lord is joined by a kendra/trikona lord (it then damages that lord), or when it also owns a good house (e.g. Jupiter for Leo: 5th+8th).
- **Result:** Frugal, saves wealth, independent, kind, respected (v.69).
- **Source:** Phaladeepika ch. 6 vv.57-70 (Sanskrit e-text sanskritdocuments.org phaladIpika.itx, read 12 Nov 2026 - see kb/sources/phaladeepika/)
- **Note:** Formation rule (v.57) is terse on the page read; the house-lord-in-dusthana reading is the standard commentary.


## Neecha bhanga (each condition separately) (12)

### Neecha bhanga condition #1  `neecha_bhanga_1`
- **Condition:** A planet is in its debilitation sign AND: Lord of the sign where the planet is debilitated (its dispositor) is in house 1/4/7/10 from Lagna OR from the Moon.
- **Strength:** Count how many conditions hold; 2+ classical conditions (1-4) = real. A cancelled debility is still not equal to exaltation.
- **Cancellation:** Bhanga itself fails in practice if: the dispositor is also debilitated, the planet is combust, or the planet sits in 6/8/12 (then relief only, no raja yoga).
- **Result:** Debility is cancelled; with conditions 1-4 the texts promise raja-yoga-level rise, usually after early struggle.
- **Source:** Phaladeepika 7.26, 7.29 (Sanskrit e-text sanskritdocuments.org phaladIpika.itx, read 12 Nov 2026 - see kb/sources/phaladeepika/) ; Jataka Parijata 7.23 (read in the Sanskrit, 12 Nov 2026; e-text marked 'needs proofreading'; notes in kb/sources/jataka-parijata/)

### Neecha bhanga condition #2  `neecha_bhanga_2`
- **Condition:** A planet is in its debilitation sign AND: Lord of the debilitated planet's EXALTATION sign is in house 1/4/7/10 from Lagna OR from the Moon.
- **Strength:** Count how many conditions hold; 2+ classical conditions (1-4) = real. A cancelled debility is still not equal to exaltation.
- **Cancellation:** Bhanga itself fails in practice if: the dispositor is also debilitated, the planet is combust, or the planet sits in 6/8/12 (then relief only, no raja yoga).
- **Result:** Debility is cancelled; with conditions 1-4 the texts promise raja-yoga-level rise, usually after early struggle.
- **Source:** Phaladeepika 7.26, 7.29 (Sanskrit e-text sanskritdocuments.org phaladIpika.itx, read 12 Nov 2026 - see kb/sources/phaladeepika/) ; Jataka Parijata 7.23 (read in the Sanskrit, 12 Nov 2026; e-text marked 'needs proofreading'; notes in kb/sources/jataka-parijata/)

### Neecha bhanga condition #3  `neecha_bhanga_3`
- **Condition:** A planet is in its debilitation sign AND: BOTH of the above (dispositor and exaltation-sign lord) are in kendras: strongest grade ('emperor honoured by kings').
- **Strength:** Count how many conditions hold; 2+ classical conditions (1-4) = real. A cancelled debility is still not equal to exaltation.
- **Cancellation:** Bhanga itself fails in practice if: the dispositor is also debilitated, the planet is combust, or the planet sits in 6/8/12 (then relief only, no raja yoga).
- **Result:** Debility is cancelled; with conditions 1-4 the texts promise raja-yoga-level rise, usually after early struggle.
- **Source:** Phaladeepika 7.27, 7.30 (Sanskrit e-text sanskritdocuments.org phaladIpika.itx, read 12 Nov 2026 - see kb/sources/phaladeepika/)

### Neecha bhanga condition #4  `neecha_bhanga_4`
- **Condition:** A planet is in its debilitation sign AND: The debilitated planet is aspected by the lord of the sign it occupies; stronger if the debilitated planet is NOT in house 6/8/12.
- **Strength:** Count how many conditions hold; 2+ classical conditions (1-4) = real. A cancelled debility is still not equal to exaltation.
- **Cancellation:** Bhanga itself fails in practice if: the dispositor is also debilitated, the planet is combust, or the planet sits in 6/8/12 (then relief only, no raja yoga).
- **Result:** Debility is cancelled; with conditions 1-4 the texts promise raja-yoga-level rise, usually after early struggle.
- **Source:** Phaladeepika 7.28 (Sanskrit e-text sanskritdocuments.org phaladIpika.itx, read 12 Nov 2026 - see kb/sources/phaladeepika/)

### Neecha bhanga condition #5  `neecha_bhanga_5`
- **Condition:** A planet is in its debilitation sign AND: The planet that gets EXALTED in the sign of debilitation (e.g. Sun for a planet in Aries) is in a kendra from Lagna or Moon.
- **Strength:** Count how many conditions hold; 2+ classical conditions (1-4) = real. A cancelled debility is still not equal to exaltation.
- **Cancellation:** Bhanga itself fails in practice if: the dispositor is also debilitated, the planet is combust, or the planet sits in 6/8/12 (then relief only, no raja yoga).
- **Result:** Debility is cancelled; with conditions 1-4 the texts promise raja-yoga-level rise, usually after early struggle.
- **Source:** No verse found in the texts read in Sanskrit (Parashara, Varahamihira, Mantreshvara, Jataka Parijata ch. 7). A modern list item (K.S. Charak's list, via a Wikipedia mirror). Low confidence.

### Neecha bhanga condition #6  `neecha_bhanga_6`
- **Condition:** A planet is in its debilitation sign AND: The debilitated planet exchanges signs with its dispositor.
- **Strength:** Count how many conditions hold; 2+ classical conditions (1-4) = real. A cancelled debility is still not equal to exaltation.
- **Cancellation:** Bhanga itself fails in practice if: the dispositor is also debilitated, the planet is combust, or the planet sits in 6/8/12 (then relief only, no raja yoga).
- **Result:** Debility is cancelled; with conditions 1-4 the texts promise raja-yoga-level rise, usually after early struggle.
- **Source:** No verse found in the texts read in Sanskrit (Parashara, Varahamihira, Mantreshvara, Jataka Parijata ch. 7). A modern list item (K.S. Charak's list). Low confidence.

### Neecha bhanga condition #7  `neecha_bhanga_7`
- **Condition:** A planet is in its debilitation sign AND: The debilitated planet is exalted in navamsa (D9).
- **Strength:** Count how many conditions hold; 2+ classical conditions (1-4) = real. A cancelled debility is still not equal to exaltation.
- **Cancellation:** Bhanga itself fails in practice if: the dispositor is also debilitated, the planet is combust, or the planet sits in 6/8/12 (then relief only, no raja yoga).
- **Result:** Debility is cancelled; with conditions 1-4 the texts promise raja-yoga-level rise, usually after early struggle.
- **Source:** Jataka Parijata 7.30 (read in the Sanskrit, 12 Nov 2026; e-text marked 'needs proofreading'; notes in kb/sources/jataka-parijata/): 'two, three or four planets in debilitation, in good sixtieth-parts or in their own exaltation navamsa'
- **Note:** The verse speaks of two to four debilitated planets together; applying it to a single planet is an extension. 

### Neecha bhanga condition #8  `neecha_bhanga_8`
- **Condition:** A planet is in its debilitation sign AND: The debilitated planet is aspected by another debilitated planet.
- **Strength:** Count how many conditions hold; 2+ classical conditions (1-4) = real. A cancelled debility is still not equal to exaltation.
- **Cancellation:** Bhanga itself fails in practice if: the dispositor is also debilitated, the planet is combust, or the planet sits in 6/8/12 (then relief only, no raja yoga).
- **Result:** Debility is cancelled; with conditions 1-4 the texts promise raja-yoga-level rise, usually after early struggle.
- **Source:** No verse found in the texts read in Sanskrit (Parashara, Varahamihira, Mantreshvara, Jataka Parijata ch. 7). A modern list item (K.S. Charak's list; contested). Low confidence.

### Neecha bhanga condition #9  `neecha_bhanga_9`
- **Condition:** A planet is in its debilitation sign AND: Dispositor and exaltation-sign lord are in mutual kendras from each other.
- **Strength:** Count how many conditions hold; 2+ classical conditions (1-4) = real. A cancelled debility is still not equal to exaltation.
- **Cancellation:** Bhanga itself fails in practice if: the dispositor is also debilitated, the planet is combust, or the planet sits in 6/8/12 (then relief only, no raja yoga).
- **Result:** Debility is cancelled; with conditions 1-4 the texts promise raja-yoga-level rise, usually after early struggle.
- **Source:** No verse found in the texts read in Sanskrit (Parashara, Varahamihira, Mantreshvara, Jataka Parijata ch. 7). A modern list item (attributed online to Phaladeepika, but not in Phaladeepika 7.26-30 as read). Low confidence.

### Neecha bhanga condition #10  `neecha_bhanga_10`
- **Condition:** A planet is in its debilitation sign AND: The debilitated planet itself sits in a kendra from Lagna or Moon.
- **Strength:** Count how many conditions hold; 2+ classical conditions (1-4) = real. A cancelled debility is still not equal to exaltation.
- **Cancellation:** Bhanga itself fails in practice if: the dispositor is also debilitated, the planet is combust, or the planet sits in 6/8/12 (then relief only, no raja yoga).
- **Result:** Debility is cancelled; with conditions 1-4 the texts promise raja-yoga-level rise, usually after early struggle.
- **Source:** Modern popular rule; NOT found in the Phaladeepika verses read

### Neecha bhanga condition #11  `neecha_bhanga_11`
- **Condition:** A planet is in its debilitation sign AND: The debilitated planet is retrograde (treated as 'like exalted').
- **Strength:** Count how many conditions hold; 2+ classical conditions (1-4) = real. A cancelled debility is still not equal to exaltation.
- **Cancellation:** Bhanga itself fails in practice if: the dispositor is also debilitated, the planet is combust, or the planet sits in 6/8/12 (then relief only, no raja yoga).
- **Result:** Debility is cancelled; with conditions 1-4 the texts promise raja-yoga-level rise, usually after early struggle.
- **Source:** Phaladeepika 4.4 and 9.20, read in the Sanskrit 12 Nov 2026: a retrograde planet with bright rays is strong even in debilitation and gives the result of exaltation

### Neecha bhanga #12 (navamsa lord, Jataka Parijata)  `neecha_bhanga_12`
- **Condition:** A planet is in its debilitation sign AND the lord of the navamsa it occupies is in a kendra or trine AND the lagna is a movable sign, or the lagna lord is in a movable sign or navamsa.
- **Cancellation:** n/a (this is itself a cancellation)
- **Result:** A powerful ruler, says the verse; in practice: the debilitation is offset.
- **Source:** Jataka Parijata 7.24 (read in the Sanskrit, 12 Nov 2026; e-text marked 'needs proofreading'; notes in kb/sources/jataka-parijata/)
- **Note:** Depends on the planet's navamsa and, in one form, the lagna lord's navamsa - check the birth-time sensitivity table.


## Other named yogas and modern doshas (incl. Kaal Sarp) (35)

### Lagnadhi yoga  `lagnadhi`
- **Condition:** Benefics in the 7th and 8th from the lagna, free of malefic aspect and conjunction (BPHS 36.37, Sanskrit read 12 Nov 2026).
- **Cancellation:** Any malefic conjunction/aspect on those benefics.
- **Result:** A great, learned person, happy.
- **Source:** BPHS ch. 36 v.37 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Amala yoga  `amala`
- **Condition:** Only benefic(s) (Jupiter, Venus, Mercury, waxing Moon) in house 10 counted from Lagna or from the Moon; no malefic there.
- **Cancellation:** A malefic in or aspecting the 10th spoils it.
- **Result:** Lasting fame, clean reputation, charity, respect of rulers.
- **Source:** BPHS ch. 36 vv.5-6 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Shubha (Subha) yoga  `shubha_kartari_lagna`
- **Condition:** A benefic in Lagna, OR benefics in both house 2 and house 12 from Lagna (shubha-kartari).
- **Cancellation:** Malefic there instead = Ashubha yoga.
- **Result:** Eloquent, virtuous, charming.
- **Source:** BPHS ch. 36 vv.1-2 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Parvata yoga  `parvata`
- **Condition:** Benefics in kendras from Lagna AND houses 7 and 8 empty or occupied by benefics only. (Raman variant: Lagna lord and 12th lord in mutual kendras.)
- **Cancellation:** Malefic in 7th/8th.
- **Result:** Wealthy, eloquent, charitable, leader of a town.
- **Source:** BPHS ch. 36 vv.7-8 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)
- **Note:** Re-read 12 Nov 2026: benefics in kendras, 7th and 8th empty or holding only benefics (vv.7-8).

### Kahala yoga  `kahala`
- **Condition:** (a) 4th lord and Jupiter in mutual kendras AND Lagna lord strong; OR (b) 4th lord in own/exalted sign conjunct the 10th lord.
- **Cancellation:** Weak Lagna lord.
- **Result:** Energetic, commands a force, heads villages.
- **Source:** BPHS ch. 36 vv.9-10 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Shankha yoga  `shankha`
- **Condition:** (a) Lagna lord strong AND 5th and 6th lords in mutual kendras; OR (b) Lagna lord and 10th lord in a movable sign AND 9th lord strong.
- **Cancellation:** Weak Lagna/9th lord.
- **Result:** Wealth, spouse, sons, piety, long life.
- **Source:** BPHS ch. 36 vv.13-14 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Bheri yoga  `bheri`
- **Condition:** (a) houses 12, 1, 2 and 7 occupied AND 9th lord strong (v.15); OR (b) Venus, Jupiter and the Lagna lord each in a kendra from the Lagna AND 9th lord strong (v.16).
- **Cancellation:** Weak 9th lord.
- **Result:** Wealth, spouse and sons, fame, royal standing.
- **Source:** BPHS ch. 36 vv.15-16 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)
- **Note:** Re-read 12 Nov 2026 at sanskritdocuments.org: variant (b) is kendras from the Lagna, not mutual kendras.

### Sharada yoga  `sharada`
- **Condition:** (a) 10th lord in house 5, Mercury in a kendra, Sun strong in Leo; OR (b) Jupiter or Mercury in a trine from the Moon AND Mars in house 11.
- **Cancellation:** None formal.
- **Result:** Wealth, learning, sons, favour of rulers, ascetic bent.
- **Source:** BPHS ch. 36 vv.19-20 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Matsya yoga  `matsya`
- **Condition:** Benefics in houses 1 and 9, mixed planets in house 5, malefics in houses 4 and 8.
- **Cancellation:** None formal.
- **Result:** Astrologer, kind, virtuous, learned, famous.
- **Source:** BPHS ch. 36 vv.21-22 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Kalanidhi yoga  `kalanidhi`
- **Condition:** Jupiter in the 2nd or 5th, joined or aspected by Mercury and Venus, or placed in a sign of Mercury or Venus (BPHS 36.31).
- **Cancellation:** None formal.
- **Result:** Virtuous, honoured by rulers, learned, free of disease.
- **Source:** BPHS ch. 36 vv.31-32 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Hari yoga (Trimurti)  `hari`
- **Condition:** Benefics in houses 2, 8 and 12 counted from the sign occupied by the 2nd lord.
- **Cancellation:** None formal.
- **Result:** Happy, learned, wealthy, with sons.
- **Source:** BPHS ch. 36 vv.35-36 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Hara yoga (Trimurti)  `hara`
- **Condition:** Benefics in houses 4, 8 and 9 counted from the sign occupied by the 7th lord.
- **Cancellation:** None formal.
- **Result:** Happy, learned, wealthy, with sons.
- **Source:** BPHS ch. 36 vv.35-36 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Brahma yoga (Trimurti)  `brahma`
- **Condition:** Benefics in houses 4, 10 and 11 counted from the sign occupied by the Lagna lord.
- **Cancellation:** None formal.
- **Result:** Happy, learned, wealthy, with sons.
- **Source:** BPHS ch. 36 vv.35-36 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Saraswati yoga  `saraswati`
- **Condition:** Jupiter, Venus and Mercury each in a kendra (1/4/7/10), trikona (5/9) or house 2 from Lagna (together or separately) AND Jupiter in own, exalted or friendly sign.
- **Cancellation:** Jupiter weak/combust; any of the three debilitated or combust.
- **Result:** Learning, poetry, authorship, fame, good family.
- **Source:** Phaladeepika 6.26-27, read in the Sanskrit 12 Nov 2026 (kb/sources/phaladeepika/ch05-07.md)

### Guru-Chandala yoga  `guru_chandala`
- **Condition:** Jupiter and Rahu in the same sign (some include Jupiter-Ketu, and Rahu's aspect on Jupiter).
- **Cancellation:** Mild if Jupiter is in own/exalted sign (Sagittarius, Pisces, Cancer), stronger in degrees than Rahu, or aspected by benefics; tighter orb = stronger.
- **Result:** Unorthodox beliefs, break with teachers/tradition, poor judgment in ethics; in good dignity: unconventional teacher, foreign learning.
- **Source:** Not found in Parashara or Phaladeepika as read in the Sanskrit (12 Nov 2026); a later name. Low confidence

### Angaraka yoga  `angaraka`
- **Condition:** Mars and Rahu in the same sign (some include Mars-Ketu).
- **Cancellation:** Mild if Mars is in own/exalted sign or aspected by Jupiter; worst in houses 1, 4, 7, 8, 12.
- **Result:** Anger, accidents, litigation, conflicts with siblings; in upachaya houses gives fighting capacity.
- **Source:** Not found in Parashara or Phaladeepika as read in the Sanskrit (12 Nov 2026); a modern name. Low confidence

### Shrapit (Shapit) dosha  `shrapit`
- **Condition:** Saturn and Rahu in the same sign (some extend to Saturn aspected by Rahu).
- **Cancellation:** Jupiter's aspect; Saturn in own/exalted sign.
- **Result:** Delays, repeated obstacles described as a 'curse' from a past life; delayed marriage/children depending on house.
- **Source:** Modern practice. The only classical base for 'curses' is BPHS ch. 83 (shapa yogas centred on the 5th house), which does NOT define this conjunction as a curse.

### Vish (Visha) yoga  `vish`
- **Condition:** Moon and Saturn in the same sign. Wider variants: Saturn aspecting the Moon (3rd/7th/10th aspect), or Moon in Saturn's nakshatra with Saturn in Moon's.
- **Cancellation:** Mild when Moon is waxing/strong, in Taurus/Cancer, when Saturn is yogakaraka (Taurus/Libra lagna), or Jupiter aspects.
- **Result:** Melancholy, emotional restraint, delayed comforts, distance from mother; also discipline and endurance. Classical texts read Moon-Saturn as a renunciation factor (BPHS 79 vv.6-8).
- **Source:** Not in Parashara. The earlier citation of BPHS ch. 79 vv.6-8 was wrong: those verses concern renunciation. Popular modern label. [UNSOURCED]

### Grahan (eclipse) dosha  `grahan`
- **Condition:** Parashara (BPHS 91.1): birth at the time of an actual solar or lunar eclipse. Popular widening, not in Parashara: Sun or Moon in the same sign as Rahu or Ketu.
- **Cancellation:** Wide orb, luminary in own/exalted sign, Jupiter's aspect reduce it.
- **Result:** Weakens what the luminary stands for (Sun: father, vitality, authority; Moon: mother, mind).
- **Source:** BPHS ch. 91 v.1 (Sanskrit text at sanskritdocuments.org, read and translated 12 Nov 2026; see kb/sources/bphs-verse-readings.md)

### Kaal Sarp (Kala Sarpa) yoga  `kaal_sarp`
- **Condition:** All seven planets Sun..Saturn lie in the half of the zodiac going from Rahu to Ketu (zodiacal order), no planet in the other half. Strict form (B.V. Raman): Lagna must also be inside the same half. Compute by longitude, not only by sign.
- **Cancellation:** Broken if (1) any one planet is outside the arc, (2) Lagna is outside (Raman), (3) a planet is conjunct Rahu or Ketu in the same sign, esp. beyond the node's degree, (4) practice: strong Jupiter/Venus/Moon in a kendra or an exalted/own-sign planet inside. Raman: exalted well-placed Mercury nullifies.
- **Result:** Popular: struggle, delays, sudden reversals till the early 40s. Raman: it does not cancel other yogas nor shorten life; no single yoga makes or mars a chart.
- **Source:** No classical verse: absent from Parashara, Varahamihira, Mantreshvara and Jataka Parijata as read in the Sanskrit (keyword search of the last, 12 Nov 2026). Modern definition from https://www.barbarapijan.com/bpa/Graha/Rahu/Kala_Sarpa_Yoga.htm (quoting B.V. Raman) ; https://jagannathhora.com/kaal-sarp-dosha-complete-guide/
- **Note:** DEBATE: not found in BPHS, Brihat Jataka, Saravali or Phaladeepika. Raman notes it is absent in Varahamihira; K.N. Rao has called it a manufactured concept. The classical 'Sarpa yoga' is a different Nabhasa yoga (malefics in three kendras) and BPHS 83 'Sarpa shapa' concerns Rahu and the 5th house. Engine: report as 'modern, low weight'.

### Ananta Kaal Sarp  `kaal_sarp_01_ananta`
- **Condition:** Kaal Sarp condition holds AND Rahu in house 1, Ketu in house 7 from Lagna.
- **Cancellation:** Same as kaal_sarp.
- **Result:** Popular reading: stress falls on the self, health, marriage axis. The type shows which houses the nodal axis activates, not good vs bad.
- **Source:** No classical verse: absent from Parashara, Varahamihira, Mantreshvara and Jataka Parijata as read in the Sanskrit (keyword search of the last, 12 Nov 2026). Modern definition from https://www.barbarapijan.com/bpa/Graha/Rahu/Kala_Sarpa_Yoga.htm ; https://jagannathhora.com/kaal-sarp-dosha-complete-guide/
- **Note:** Names are modern (from the eight/twelve Nagas); no classical text lists them.

### Kulika Kaal Sarp  `kaal_sarp_02_kulika`
- **Condition:** Kaal Sarp condition holds AND Rahu in house 2, Ketu in house 8 from Lagna.
- **Cancellation:** Same as kaal_sarp.
- **Result:** Popular reading: stress falls on the family wealth, speech, longevity axis. The type shows which houses the nodal axis activates, not good vs bad.
- **Source:** No classical verse: absent from Parashara, Varahamihira, Mantreshvara and Jataka Parijata as read in the Sanskrit (keyword search of the last, 12 Nov 2026). Modern definition from https://www.barbarapijan.com/bpa/Graha/Rahu/Kala_Sarpa_Yoga.htm ; https://jagannathhora.com/kaal-sarp-dosha-complete-guide/
- **Note:** Names are modern (from the eight/twelve Nagas); no classical text lists them.

### Vasuki Kaal Sarp  `kaal_sarp_03_vasuki`
- **Condition:** Kaal Sarp condition holds AND Rahu in house 3, Ketu in house 9 from Lagna.
- **Cancellation:** Same as kaal_sarp.
- **Result:** Popular reading: stress falls on the courage, siblings, fortune axis. The type shows which houses the nodal axis activates, not good vs bad.
- **Source:** No classical verse: absent from Parashara, Varahamihira, Mantreshvara and Jataka Parijata as read in the Sanskrit (keyword search of the last, 12 Nov 2026). Modern definition from https://www.barbarapijan.com/bpa/Graha/Rahu/Kala_Sarpa_Yoga.htm ; https://jagannathhora.com/kaal-sarp-dosha-complete-guide/
- **Note:** Names are modern (from the eight/twelve Nagas); no classical text lists them.

### Shankhapala Kaal Sarp  `kaal_sarp_04_shankhapala`
- **Condition:** Kaal Sarp condition holds AND Rahu in house 4, Ketu in house 10 from Lagna.
- **Cancellation:** Same as kaal_sarp.
- **Result:** Popular reading: stress falls on the home, mother, career axis. The type shows which houses the nodal axis activates, not good vs bad.
- **Source:** No classical verse: absent from Parashara, Varahamihira, Mantreshvara and Jataka Parijata as read in the Sanskrit (keyword search of the last, 12 Nov 2026). Modern definition from https://www.barbarapijan.com/bpa/Graha/Rahu/Kala_Sarpa_Yoga.htm ; https://jagannathhora.com/kaal-sarp-dosha-complete-guide/
- **Note:** Names are modern (from the eight/twelve Nagas); no classical text lists them.

### Padma Kaal Sarp  `kaal_sarp_05_padma`
- **Condition:** Kaal Sarp condition holds AND Rahu in house 5, Ketu in house 11 from Lagna.
- **Cancellation:** Same as kaal_sarp.
- **Result:** Popular reading: stress falls on the children, intellect, gains axis. The type shows which houses the nodal axis activates, not good vs bad.
- **Source:** No classical verse: absent from Parashara, Varahamihira, Mantreshvara and Jataka Parijata as read in the Sanskrit (keyword search of the last, 12 Nov 2026). Modern definition from https://www.barbarapijan.com/bpa/Graha/Rahu/Kala_Sarpa_Yoga.htm ; https://jagannathhora.com/kaal-sarp-dosha-complete-guide/
- **Note:** Names are modern (from the eight/twelve Nagas); no classical text lists them.

### Mahapadma Kaal Sarp  `kaal_sarp_06_mahapadma`
- **Condition:** Kaal Sarp condition holds AND Rahu in house 6, Ketu in house 12 from Lagna.
- **Cancellation:** Same as kaal_sarp.
- **Result:** Popular reading: stress falls on the enemies, disease, expenses axis. The type shows which houses the nodal axis activates, not good vs bad.
- **Source:** No classical verse: absent from Parashara, Varahamihira, Mantreshvara and Jataka Parijata as read in the Sanskrit (keyword search of the last, 12 Nov 2026). Modern definition from https://www.barbarapijan.com/bpa/Graha/Rahu/Kala_Sarpa_Yoga.htm ; https://jagannathhora.com/kaal-sarp-dosha-complete-guide/
- **Note:** Names are modern (from the eight/twelve Nagas); no classical text lists them.

### Takshaka Kaal Sarp  `kaal_sarp_07_takshaka`
- **Condition:** Kaal Sarp condition holds AND Rahu in house 7, Ketu in house 1 from Lagna.
- **Cancellation:** Same as kaal_sarp.
- **Result:** Popular reading: stress falls on the marriage, partnerships, self axis. The type shows which houses the nodal axis activates, not good vs bad.
- **Source:** No classical verse: absent from Parashara, Varahamihira, Mantreshvara and Jataka Parijata as read in the Sanskrit (keyword search of the last, 12 Nov 2026). Modern definition from https://www.barbarapijan.com/bpa/Graha/Rahu/Kala_Sarpa_Yoga.htm ; https://jagannathhora.com/kaal-sarp-dosha-complete-guide/
- **Note:** Names are modern (from the eight/twelve Nagas); no classical text lists them.

### Karkotaka Kaal Sarp  `kaal_sarp_08_karkotaka`
- **Condition:** Kaal Sarp condition holds AND Rahu in house 8, Ketu in house 2 from Lagna.
- **Cancellation:** Same as kaal_sarp.
- **Result:** Popular reading: stress falls on the longevity, inheritance, family wealth axis. The type shows which houses the nodal axis activates, not good vs bad.
- **Source:** No classical verse: absent from Parashara, Varahamihira, Mantreshvara and Jataka Parijata as read in the Sanskrit (keyword search of the last, 12 Nov 2026). Modern definition from https://www.barbarapijan.com/bpa/Graha/Rahu/Kala_Sarpa_Yoga.htm ; https://jagannathhora.com/kaal-sarp-dosha-complete-guide/
- **Note:** Names are modern (from the eight/twelve Nagas); no classical text lists them.

### Shankhachuda Kaal Sarp  `kaal_sarp_09_shankhachuda`
- **Condition:** Kaal Sarp condition holds AND Rahu in house 9, Ketu in house 3 from Lagna.
- **Cancellation:** Same as kaal_sarp.
- **Result:** Popular reading: stress falls on the fortune, father, effort axis. The type shows which houses the nodal axis activates, not good vs bad.
- **Source:** No classical verse: absent from Parashara, Varahamihira, Mantreshvara and Jataka Parijata as read in the Sanskrit (keyword search of the last, 12 Nov 2026). Modern definition from https://www.barbarapijan.com/bpa/Graha/Rahu/Kala_Sarpa_Yoga.htm ; https://jagannathhora.com/kaal-sarp-dosha-complete-guide/
- **Note:** Names are modern (from the eight/twelve Nagas); no classical text lists them.

### Ghataka Kaal Sarp  `kaal_sarp_10_ghataka`
- **Condition:** Kaal Sarp condition holds AND Rahu in house 10, Ketu in house 4 from Lagna.
- **Cancellation:** Same as kaal_sarp.
- **Result:** Popular reading: stress falls on the career, status, home axis. The type shows which houses the nodal axis activates, not good vs bad.
- **Source:** No classical verse: absent from Parashara, Varahamihira, Mantreshvara and Jataka Parijata as read in the Sanskrit (keyword search of the last, 12 Nov 2026). Modern definition from https://www.barbarapijan.com/bpa/Graha/Rahu/Kala_Sarpa_Yoga.htm ; https://jagannathhora.com/kaal-sarp-dosha-complete-guide/
- **Note:** Names are modern (from the eight/twelve Nagas); no classical text lists them.

### Vishadhara Kaal Sarp  `kaal_sarp_11_vishadhara`
- **Condition:** Kaal Sarp condition holds AND Rahu in house 11, Ketu in house 5 from Lagna.
- **Cancellation:** Same as kaal_sarp.
- **Result:** Popular reading: stress falls on the gains, elder siblings, children axis. The type shows which houses the nodal axis activates, not good vs bad.
- **Source:** No classical verse: absent from Parashara, Varahamihira, Mantreshvara and Jataka Parijata as read in the Sanskrit (keyword search of the last, 12 Nov 2026). Modern definition from https://www.barbarapijan.com/bpa/Graha/Rahu/Kala_Sarpa_Yoga.htm ; https://jagannathhora.com/kaal-sarp-dosha-complete-guide/
- **Note:** Names are modern (from the eight/twelve Nagas); no classical text lists them.

### Sheshanaga Kaal Sarp  `kaal_sarp_12_sheshanaga`
- **Condition:** Kaal Sarp condition holds AND Rahu in house 12, Ketu in house 6 from Lagna.
- **Cancellation:** Same as kaal_sarp.
- **Result:** Popular reading: stress falls on the expenses, sleep, foreign, enemies axis. The type shows which houses the nodal axis activates, not good vs bad.
- **Source:** No classical verse: absent from Parashara, Varahamihira, Mantreshvara and Jataka Parijata as read in the Sanskrit (keyword search of the last, 12 Nov 2026). Modern definition from https://www.barbarapijan.com/bpa/Graha/Rahu/Kala_Sarpa_Yoga.htm ; https://jagannathhora.com/kaal-sarp-dosha-complete-guide/
- **Note:** Names are modern (from the eight/twelve Nagas); no classical text lists them.

### Partial (Anshik) Kaal Sarp  `kaal_sarp_partial`
- **Condition:** All planets but one are inside the Rahu->Ketu half, OR a planet is conjunct a node in the same sign.
- **Cancellation:** By definition already weakened; many traditions treat it as fully cancelled.
- **Result:** Diluted version; the one outside planet often becomes the life's outlet.
- **Source:** No classical verse: absent from Parashara, Varahamihira, Mantreshvara and Jataka Parijata as read in the Sanskrit (keyword search of the last, 12 Nov 2026). Modern definition from https://www.barbarapijan.com/bpa/Graha/Rahu/Kala_Sarpa_Yoga.htm ; https://jagannathhora.com/kaal-sarp-dosha-complete-guide/

### Kala Amrita yoga  `kala_amrita`
- **Condition:** All seven planets in the half from Ketu to Rahu (planets moving toward Ketu).
- **Cancellation:** Same breakers as Kaal Sarp.
- **Result:** Most astrologers do not count it; some treat it as a milder or spiritual variant.
- **Source:** No classical verse: absent from Parashara, Varahamihira, Mantreshvara and Jataka Parijata as read in the Sanskrit (keyword search of the last, 12 Nov 2026). Modern definition from https://www.barbarapijan.com/bpa/Graha/Rahu/Kala_Sarpa_Yoga.htm

### Spender: lagna lord aspecting the 12th  `vyaya_lord_aspect`
- **Condition:** The lagna lord aspects the 12th house.
- **Cancellation:** None stated in the verse.
- **Result:** A spender.
- **Source:** BPHS 42.15 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/bphs/)
- **Note:** Engine tests the lagna form only.


## Arishta / Daridra / classical doshas (30)

### Shakata yoga (Moon-Jupiter)  `shakata_lunar`
- **Condition:** The Moon in house 6, 8 or 12 counted from Jupiter (that is, Jupiter in the 2nd, 6th or 8th from the Moon); cancelled when the Moon is in a kendra from the lagna (Phaladeepika 6.14, Sanskrit read 12 Nov 2026).
- **Cancellation:** Cancelled if the Moon is in a kendra (1/4/7/10) from Lagna. Some also cancel if Jupiter is in own/exalted sign.
- **Result:** Fortunes rise and fall like a cart wheel; periodic loss of standing.
- **Source:** Phaladeepika 6.14 and 6.17, read in the Sanskrit 12 Nov 2026
- **Note:** Do not confuse with the Nabhasa Shakata (all planets in houses 1 and 7). Jataka Parijata 7.108 (read in the Sanskrit): Jupiter in the 6th or 8th from the Moon AND not in a kendra from the lagna - it does not include the 12th, and the kendra test is on Jupiter.

### Ashubha yoga / Papa-kartari  `ashubha_papa_kartari`
- **Condition:** A malefic in Lagna, OR malefics in both house 2 and house 12 from Lagna. (Generalised: any house/planet flanked by malefics on both sides is hemmed.)
- **Cancellation:** A benefic in or aspecting the hemmed house eases it.
- **Result:** Sensual, sinful, enjoys others' wealth; the hemmed house suffers.
- **Source:** BPHS ch. 36 vv.1-2 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Avayoga  `avayoga`
- **Condition:** Lord of house 1 placed in house 6, 8 or 12 from Lagna; OR house 1 itself occupied/aspected by malefics with its lord weak.
- **Cancellation:** Eased when the lord is strong (own/exalted) or aspected by a benefic; verse 70 reverses the whole set when good-house lords are strong in kendra/trikona and dusthana lords are weak in dusthanas.
- **Result:** Obscure, poor, short-lived, humiliated, unstable position (v.58).
- **Source:** Phaladeepika ch. 6 vv.57-70 (Sanskrit e-text sanskritdocuments.org phaladIpika.itx, read 12 Nov 2026 - see kb/sources/phaladeepika/)
- **Note:** Formation rule (v.57) is terse on the page read; the house-lord-in-dusthana reading is the standard commentary.

### Nisswa yoga  `nisswa`
- **Condition:** Lord of house 2 placed in house 6, 8 or 12 from Lagna; OR house 2 itself occupied/aspected by malefics with its lord weak.
- **Cancellation:** Eased when the lord is strong (own/exalted) or aspected by a benefic; verse 70 reverses the whole set when good-house lords are strong in kendra/trikona and dusthana lords are weak in dusthanas.
- **Result:** Harsh speech, no family wealth, poor teeth/eyes, enemies take wealth (v.59).
- **Source:** Phaladeepika ch. 6 vv.57-70 (Sanskrit e-text sanskritdocuments.org phaladIpika.itx, read 12 Nov 2026 - see kb/sources/phaladeepika/)
- **Note:** Formation rule (v.57) is terse on the page read; the house-lord-in-dusthana reading is the standard commentary.

### Mriti yoga  `mriti`
- **Condition:** Lord of house 3 placed in house 6, 8 or 12 from Lagna; OR house 3 itself occupied/aspected by malefics with its lord weak.
- **Cancellation:** Eased when the lord is strong (own/exalted) or aspected by a benefic; verse 70 reverses the whole set when good-house lords are strong in kendra/trikona and dusthana lords are weak in dusthanas.
- **Result:** Overpowered by enemies, no brothers, little strength or shame (v.60).
- **Source:** Phaladeepika ch. 6 vv.57-70 (Sanskrit e-text sanskritdocuments.org phaladIpika.itx, read 12 Nov 2026 - see kb/sources/phaladeepika/)
- **Note:** Formation rule (v.57) is terse on the page read; the house-lord-in-dusthana reading is the standard commentary.

### Kuhu yoga  `kuhu`
- **Condition:** Lord of house 4 placed in house 6, 8 or 12 from Lagna; OR house 4 itself occupied/aspected by malefics with its lord weak.
- **Cancellation:** Eased when the lord is strong (own/exalted) or aspected by a benefic; verse 70 reverses the whole set when good-house lords are strong in kendra/trikona and dusthana lords are weak in dusthanas.
- **Result:** Loss of mother, vehicles, home, comforts, friends (v.61).
- **Source:** Phaladeepika ch. 6 vv.57-70 (Sanskrit e-text sanskritdocuments.org phaladIpika.itx, read 12 Nov 2026 - see kb/sources/phaladeepika/)
- **Note:** Formation rule (v.57) is terse on the page read; the house-lord-in-dusthana reading is the standard commentary.

### Pamara yoga  `pamara`
- **Condition:** Lord of house 5 placed in house 6, 8 or 12 from Lagna; OR house 5 itself occupied/aspected by malefics with its lord weak.
- **Cancellation:** Eased when the lord is strong (own/exalted) or aspected by a benefic; verse 70 reverses the whole set when good-house lords are strong in kendra/trikona and dusthana lords are weak in dusthanas.
- **Result:** Hard life, deceit, loss/lack of children, irreligious (v.62).
- **Source:** Phaladeepika ch. 6 vv.57-70 (Sanskrit e-text sanskritdocuments.org phaladIpika.itx, read 12 Nov 2026 - see kb/sources/phaladeepika/)
- **Note:** Formation rule (v.57) is terse on the page read; the house-lord-in-dusthana reading is the standard commentary.

### Dushkriti yoga  `dushkriti`
- **Condition:** Lord of house 7 placed in house 6, 8 or 12 from Lagna; OR house 7 itself occupied/aspected by malefics with its lord weak.
- **Cancellation:** Eased when the lord is strong (own/exalted) or aspected by a benefic; verse 70 reverses the whole set when good-house lords are strong in kendra/trikona and dusthana lords are weak in dusthanas.
- **Result:** Loss of spouse, drawn to others' partners, urinary/venereal ailments, scorned by kin (v.64).
- **Source:** Phaladeepika ch. 6 vv.57-70 (Sanskrit e-text sanskritdocuments.org phaladIpika.itx, read 12 Nov 2026 - see kb/sources/phaladeepika/)
- **Note:** Formation rule (v.57) is terse on the page read; the house-lord-in-dusthana reading is the standard commentary.

### Nirbhagya yoga  `nirbhagya`
- **Condition:** Lord of house 9 placed in house 6, 8 or 12 from Lagna; OR house 9 itself occupied/aspected by malefics with its lord weak.
- **Cancellation:** Eased when the lord is strong (own/exalted) or aspected by a benefic; verse 70 reverses the whole set when good-house lords are strong in kendra/trikona and dusthana lords are weak in dusthanas.
- **Result:** Loses patrimony, disrespects elders, destitute (v.66).
- **Source:** Phaladeepika ch. 6 vv.57-70 (Sanskrit e-text sanskritdocuments.org phaladIpika.itx, read 12 Nov 2026 - see kb/sources/phaladeepika/)
- **Note:** Formation rule (v.57) is terse on the page read; the house-lord-in-dusthana reading is the standard commentary.

### Duryoga  `duryoga`
- **Condition:** Lord of house 10 placed in house 6, 8 or 12 from Lagna; OR house 10 itself occupied/aspected by malefics with its lord weak.
- **Cancellation:** Eased when the lord is strong (own/exalted) or aspected by a benefic; verse 70 reverses the whole set when good-house lords are strong in kendra/trikona and dusthana lords are weak in dusthanas.
- **Result:** Labour bears little fruit, low regard, lives abroad (v.67).
- **Source:** Phaladeepika ch. 6 vv.57-70 (Sanskrit e-text sanskritdocuments.org phaladIpika.itx, read 12 Nov 2026 - see kb/sources/phaladeepika/)
- **Note:** Formation rule (v.57) is terse on the page read; the house-lord-in-dusthana reading is the standard commentary.

### Daridra yoga (Phaladeepika)  `daridra_pd`
- **Condition:** Lord of house 11 placed in house 6, 8 or 12 from Lagna; OR house 11 itself occupied/aspected by malefics with its lord weak.
- **Cancellation:** Eased when the lord is strong (own/exalted) or aspected by a benefic; verse 70 reverses the whole set when good-house lords are strong in kendra/trikona and dusthana lords are weak in dusthanas.
- **Result:** Heavy debt, harsh, poor, ear ailments, serves others (v.68).
- **Source:** Phaladeepika ch. 6 vv.57-70 (Sanskrit e-text sanskritdocuments.org phaladIpika.itx, read 12 Nov 2026 - see kb/sources/phaladeepika/)
- **Note:** Formation rule (v.57) is terse on the page read; the house-lord-in-dusthana reading is the standard commentary.

### Daridra: Lagna lord / dusthana lord swap  `daridra_1`
- **Condition:** Lagna lord in house 12 (or 6) AND the 12th (or 6th) lord in Lagna, aspected/joined by a maraka (2nd/7th) lord.
- **Cancellation:** Benefic aspect; strong Lagna lord.
- **Result:** Penniless.
- **Source:** BPHS ch. 42 vv.2-3 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Daridra: Ketu with Lagna/Moon, Lagna lord in 8th  `daridra_2`
- **Condition:** Ketu in Lagna or with the Moon AND Lagna lord in house 8.
- **Cancellation:** None formal.
- **Result:** Penniless.
- **Source:** BPHS ch. 42 v.4 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Daridra: afflicted Lagna lord in dusthana  `daridra_3`
- **Condition:** Lagna lord with malefics in 6/8/12, OR Lagna lord with a 6/8/12 lord or Saturn, with no benefic aspect.
- **Cancellation:** Benefic aspect.
- **Result:** Indigent.
- **Source:** BPHS ch. 42 vv.5-6 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Daridra: 5th and 9th lords in 6th and 12th  `daridra_4`
- **Condition:** 5th lord in house 6 and 9th lord in house 12, aspected by maraka lords.
- **Cancellation:** None formal.
- **Result:** Penniless.
- **Source:** BPHS ch. 42 vv.7-8 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Daridra: benefics in bad houses, malefics in good  `daridra_5`
- **Condition:** Benefics in 6/8/12 (inauspicious houses) AND malefics in kendras/trikonas.
- **Cancellation:** None formal.
- **Result:** Indigent; distress even over food.
- **Source:** BPHS ch. 42 v.12 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Daridra: Mars+Saturn in 2nd  `daridra_6`
- **Condition:** Mars and Saturn both in house 2 (unless aspected by Mercury, which reverses it to great wealth). Also: Sun in 2nd aspected by Saturn; Saturn in 2nd aspected by Sun.
- **Cancellation:** Mercury's aspect on the 2nd; Sun in 2nd unaspected by Saturn gives riches.
- **Result:** Wealth destroyed.
- **Source:** BPHS ch. 42 vv.16-18 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf)

### Sarpa shapa (serpent curse)  `sarpa_shapa`
- **Condition:** Any of: (83.9) Rahu in the 5th aspected by Mars, or in Mars's sign; (83.10) 5th lord with Rahu AND Saturn in the 5th joined or aspected by the Moon; (83.11) Jupiter with Rahu, 5th lord weak, lagna lord with Mars; (83.12) Jupiter with Mars, Rahu in the lagna, 5th lord in the 6th/8th/12th; (83.13) Mercury as 5th lord in Mars's navamsa with Mars, lagna holding Rahu and Mandi (not tested: Mandi is not computed).
- **Cancellation:** Remedy prescribed, not a cancellation: Naga worship, charity (vv.17-19).
- **Result:** Difficulty in having or keeping children.
- **Source:** BPHS ch. 83 vv.9-13 (Sanskrit text at sanskritdocuments.org, read and translated 12 Nov 2026; see kb/sources/bphs-verse-readings.md)

### Pitru dosha / Pitru shapa  `pitru_dosha`
- **Condition:** Parashara's father's curse (all concern children): (83.20) Sun debilitated in the 5th in Saturn's navamsa with malefics on both sides; (83.21) Sun as 5th lord in a trine with a malefic, between malefics, aspected by a malefic; (83.22) Jupiter in Leo, 5th lord with the Sun, malefics in the 5th and lagna; (83.23) weak lagna lord in the 5th, 5th lord with the Sun, malefics in the 5th and lagna; (83.24-26) combinations of the father's-house lord (not tested); (83.27) Sun, Mars, Saturn in lagna and 5th with Rahu and Jupiter in the 8th and 12th. Popular definition, NOT in Parashara and present in about 61% of charts: Sun with Rahu, Ketu or Saturn, or an afflicted 9th house.
- **Cancellation:** Benefic (Jupiter) aspect on Sun/9th; strong 9th lord. Remedy in text: shraddha at Gaya, feeding, charity (vv.31-33).
- **Result:** Classical: obstruction to children due to father's/ancestors' displeasure. Popular: generic family obstacles.
- **Source:** BPHS ch. 83 vv.20-27 (Sanskrit text at sanskritdocuments.org, read and translated 12 Nov 2026; see kb/sources/bphs-verse-readings.md)
- **Note:** The popular definition is far wider than the classical one; flag which one fired.

### Kalatra dosha (7th-house affliction)  `kalatra_dosha`
- **Condition:** Any of: malefics (Mars/Saturn/Rahu/Ketu/Sun) in house 7 without benefic aspect; 7th lord in 6/8/12 or debilitated/combust; Venus hemmed between malefics, combust, or with Mars/Saturn/Rahu; 7th house hemmed by malefics. Check from Lagna, Moon and Venus.
- **Strength:** PROJECT CALIBRATION: one dignified occupant does not outvote three malefic influences on the 7th.
- **Cancellation:** Benefic aspect (Jupiter) on 7th/7th lord/Venus; strong 7th lord; same pattern in the partner's chart.
- **Result:** Delay, discord, separation or ill-health of spouse in proportion to how many factors repeat.
- **Source:** Aggregated from Phaladeepika 10.2-4, 7, 15 and BPHS ch. 18, both read in the Sanskrit 12 Nov 2026; loss wordings are never stated

### Mangal (Kuja) dosha  `mangal_dosha`
- **Condition:** Mars in house 1, 2, 4, 7, 8 or 12 counted from Lagna; also checked from Moon and Venus. North Indian lists use 1/4/7/8/12; South Indian lists add 2.
- **Cancellation:** Commonly listed: Mars in own/exalted sign (Aries, Scorpio, Capricorn); Mars conjunct/aspected by Jupiter; Mars in 2nd in Gemini/Virgo, 12th in Taurus/Libra, 4th in Aries/Scorpio, 7th in Cancer/Capricorn, 8th in Sagittarius/Pisces; partner has equal dosha.
- **Result:** Friction, delay or danger in marriage.
- **Source:** BPHS 80.47-49, read in the Sanskrit 12 Nov 2026: Mars in the 1st, 4th, 7th, 8th or 12th from the lagna without a benefic's aspect or company; broken when both partners have it. The 2nd house and the counts from Moon and Venus are later practice
- **Note:** Exception lists vary widely between regions; treat as matching practice, not Parashari doctrine. The list that counts the 2nd house and leaves out the lagna (2, 12, 7, 4, 8) is Jataka Parijata 14.34 (read in the Sanskrit), with the same both-partners cancellation (14.36). Counting from the Moon or Venus has no verse in any text read.

### Gandanta birth  `gandanta_birth`
- **Condition:** BPHS 92.1-5: nakshatra gandanta = four nadis at the Revati-Ashwini, Ashlesha-Magha and Jyeshtha-Mula junctions (about 0d27' of the Moon either side; 0d53' on the loosest reading); lagna gandanta = one ghati at the Pisces-Aries, Cancer-Leo, Scorpio-Sagittarius junctions (about 3 degrees either side); Abhukta Mula = last 5 ghatis of Jyeshtha and first 8 of Mula; tithi gandanta = four nadis at the junction of tithis 5/6, 10/11, 15/1 (not tested).
- **Cancellation:** Shanti rites prescribed; in practice strength of Moon/Lagna lord and benefic aspect.
- **Result:** Risk to child or a parent in early life per text; modern reading: a knot to be untied around the junction's themes.
- **Source:** BPHS ch. 92 vv.1-5 (Sanskrit text at sanskritdocuments.org, read and translated 12 Nov 2026; see kb/sources/bphs-verse-readings.md)

### Amavasya / Krishna Chaturdashi birth  `amavasya_birth`
- **Condition:** Birth on new-moon tithi (Sun-Moon within 12 deg, dark side) or on the 14th tithi of the dark fortnight (divided into six parts; first part harmless).
- **Cancellation:** Shanti prescribed.
- **Result:** Poverty or harm to a specified relative per the part of the tithi.
- **Source:** BPHS ch. 86 v.1 and ch. 87 vv.1-3 (Sanskrit text at sanskritdocuments.org, read and translated 12 Nov 2026; see kb/sources/bphs-verse-readings.md)

### Balarishta (infant affliction)  `balarishta`
- **Condition:** Moon in house 6, 8 or 12 from Lagna aspected by malefics with no benefic aspect (several variants).
- **Cancellation:** Benefic aspect on Moon; strong Lagna lord in kendra; Jupiter strong in Lagna/kendra; waxing Moon in benefic varga.
- **Result:** Danger in infancy; today read as early-childhood ill-health.
- **Source:** BPHS ch. 9-10, read in the Sanskrit 12 Nov 2026. Chapter 9 is never used; the cancellations of 10.2-4 and 10.9 are usable in their positive form

### Daridra: malefic in the lagna touched by a maraka lord  `daridra_7`
- **Condition:** A malefic in the lagna, other than the 9th or 10th lord, joined or aspected by the 2nd or 7th lord.
- **Cancellation:** Not applied to a malefic that is the 9th or 10th lord (the verse's own exception).
- **Result:** Pressure on means.
- **Source:** BPHS 42.8 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/bphs/)

### Daridra: dispositors of the 6th, 8th, 12th lords in dusthanas  `daridra_8`
- **Condition:** The lords of the signs in which the 6th, 8th and 12th lords sit are themselves in the 6th, 8th or 12th, with malefic aspect or company.
- **Cancellation:** None stated in the verse.
- **Result:** Pressure on means.
- **Source:** BPHS 42.9 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/bphs/)

### Daridra: lord of the Moon's navamsa and the marakas  `daridra_9`
- **Condition:** The lord of the navamsa sign of the Moon is with a maraka lord (2nd or 7th lord) or in the 2nd or 7th house.
- **Cancellation:** None stated in the verse.
- **Result:** Pressure on means.
- **Source:** BPHS 42.10 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/bphs/)
- **Note:** Depends on the Moon's navamsa: changes about every 6 hours of birth time.

### Daridra: lagna lord and lagna-navamsa lord in dusthanas  `daridra_10`
- **Condition:** The lagna lord and the lord of the lagna's navamsa both in the 6th, 8th or 12th, joined or aspected by a maraka lord.
- **Cancellation:** None stated in the verse.
- **Result:** Pressure on means.
- **Source:** BPHS 42.11 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/bphs/)
- **Note:** Birth-time sensitive: the lagna's navamsa changes about every 13 minutes.

### Loss of money in a planet's own period  `dhana_loss_dasha`
- **Condition:** A planet joined with the lord of the 6th, 8th or 12th and not aspected by the 5th or 9th lord.
- **Cancellation:** Aspect of the 5th or 9th lord removes it (the verse's own condition).
- **Result:** Loss of money in that planet's own dasha - a timing note, not a standing condition.
- **Source:** BPHS 42.13 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/bphs/)

### Daridra: lagna lord aspecting the 8th and 12th  `daridra_11`
- **Condition:** The lagna lord (or the lord of the Atma-karaka's sign, counted from the Atma-karaka) aspects both the 8th and the 12th.
- **Cancellation:** None stated in the verse.
- **Result:** Without wealth.
- **Source:** BPHS 42.14 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/bphs/)
- **Note:** Engine tests the lagna form only.


## Pravrajya / Sanyasa (4)

### Pravrajya (four-planet) yoga  `pravrajya_4`
- **Condition:** Four or more planets (Sun..Saturn) strong and together in one sign/house. The strongest decides the order: Sun-tapasvi, Moon-kapali, Mars-red-robed, Mercury-staff-bearer, Jupiter-yati/teacher order, Venus-chakra-bearer/wanderer, Saturn-naked ascetic.
- **Cancellation:** If the planets are combust the person only reveres the order without initiation (v.4); if the deciding planet is defeated in planetary war the person abandons it (v.10).
- **Result:** Renunciation or a monastic/ascetic way of life; with raja yoga present, a founder/leader instead.
- **Source:** BPHS ch. 79 vv.2-5 (Sanskrit text at sanskritdocuments.org, read and translated 12 Nov 2026; see kb/sources/bphs-verse-readings.md)

### Pravrajya (Moon-Saturn) yoga  `pravrajya_moon_saturn`
- **Condition:** (79.7) Lord of the Moon's sign weak and aspected by Saturn alone; OR (79.8) Moon in Saturn's drekkana AND in a navamsa of Saturn or Mars, AND aspected by Saturn.
- **Cancellation:** Benefic aspect on the Moon; strong Moon-sign lord.
- **Result:** Takes to Saturn's (austere) order; in modern life: withdrawal, austerity, late or no marriage.
- **Source:** BPHS ch. 79 vv.6-8 (Sanskrit text at sanskritdocuments.org, read and translated 12 Nov 2026; see kb/sources/bphs-verse-readings.md)

### Pravrajya with raja yoga  `pravrajya_jupiter_9`
- **Condition:** Jupiter in house 9 AND Lagna, Moon and Jupiter all aspected by Saturn; OR Saturn in house 9 unaspected.
- **Cancellation:** None formal.
- **Result:** Founder of a school/philosophy; or initiation before/instead of kingship. Without a raja yoga: a religious wanderer.
- **Source:** BPHS ch. 79 vv.14-15 (Sanskrit text at sanskritdocuments.org, read and translated 12 Nov 2026; see kb/sources/bphs-verse-readings.md)

### Moksha indicator (Ketu in 12th)  `sanyasa_ketu_12`
- **Condition:** Ketu in house 12 from Lagna or from the Karakamsa, esp. with/aspected by benefics.
- **Cancellation:** None formal.
- **Result:** Inclination to liberation practices.
- **Source:** Later tradition. BPHS ch. 33 (Karakamsa, read in the Sanskrit 12 Nov 2026) gives results for Ketu in the Karakamsa and in its 2nd, 3rd and 4th, not the 12th from the lagna. Low confidence


## Nabhasa yogas (32)

### Rajju yoga (Nabhasa)  `nabhasa_rajju`
- **Condition:** Using the seven planets Sun..Saturn only (no Rahu/Ketu): all in movable signs (Aries, Cancer, Libra, Capricorn).
- **Strength:** Said to operate through life, not only in specific dashas. Most are rare; weight by how exactly the pattern holds.
- **Cancellation:** Nabhasa yogas have no bhanga. Precedence: if an Akriti/Asraya/Dala yoga is present, the Sankhya yoga is ignored; Asraya is ignored if an Akriti yoga coincides (Varahamihira).
- **Result:** Fond of travel, earns abroad, restless, cruel.
- **Source:** BPHS ch. 35 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 12.2-19 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/) - definitions confirmed

### Musala yoga (Nabhasa)  `nabhasa_musala`
- **Condition:** Using the seven planets Sun..Saturn only (no Rahu/Ketu): all in fixed signs (Taurus, Leo, Scorpio, Aquarius).
- **Strength:** Said to operate through life, not only in specific dashas. Most are rare; weight by how exactly the pattern holds.
- **Cancellation:** Nabhasa yogas have no bhanga. Precedence: if an Akriti/Asraya/Dala yoga is present, the Sankhya yoga is ignored; Asraya is ignored if an Akriti yoga coincides (Varahamihira).
- **Result:** Honoured, wealthy, steady, many sons.
- **Source:** BPHS ch. 35 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 12.2-19 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/) - definitions confirmed

### Nala yoga (Nabhasa)  `nabhasa_nala`
- **Condition:** Using the seven planets Sun..Saturn only (no Rahu/Ketu): all in dual signs (Gemini, Virgo, Sagittarius, Pisces).
- **Strength:** Said to operate through life, not only in specific dashas. Most are rare; weight by how exactly the pattern holds.
- **Cancellation:** Nabhasa yogas have no bhanga. Precedence: if an Akriti/Asraya/Dala yoga is present, the Sankhya yoga is ignored; Asraya is ignored if an Akriti yoga coincides (Varahamihira).
- **Result:** Uneven build, shrewd, accumulates money, helps kin.
- **Source:** BPHS ch. 35 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 12.2-19 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/) - definitions confirmed

### Mala (Srik) yoga (Nabhasa)  `nabhasa_mala`
- **Condition:** Using the seven planets Sun..Saturn only (no Rahu/Ketu): benefics (Mercury, Jupiter, Venus) occupy three kendras from Lagna. Moon not considered.
- **Strength:** Said to operate through life, not only in specific dashas. Most are rare; weight by how exactly the pattern holds.
- **Cancellation:** Nabhasa yogas have no bhanga. Precedence: if an Akriti/Asraya/Dala yoga is present, the Sankhya yoga is ignored; Asraya is ignored if an Akriti yoga coincides (Varahamihira).
- **Result:** Happy, comforts, vehicles, many partners.
- **Source:** BPHS ch. 35 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 12.2-19 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/) - definitions confirmed

### Sarpa yoga (Nabhasa)  `nabhasa_sarpa`
- **Condition:** Using the seven planets Sun..Saturn only (no Rahu/Ketu): malefics (Sun, Mars, Saturn) occupy three kendras from Lagna. Moon not considered.
- **Strength:** Said to operate through life, not only in specific dashas. Most are rare; weight by how exactly the pattern holds.
- **Cancellation:** Nabhasa yogas have no bhanga. Precedence: if an Akriti/Asraya/Dala yoga is present, the Sankhya yoga is ignored; Asraya is ignored if an Akriti yoga coincides (Varahamihira).
- **Result:** Crooked, cruel, poor, dependent.
- **Source:** BPHS ch. 35 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 12.2-19 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/) - definitions confirmed
- **Note:** This is the classical 'Sarpa yoga' - unrelated to Kaal Sarp.

### Gada yoga (Nabhasa)  `nabhasa_gada`
- **Condition:** Using the seven planets Sun..Saturn only (no Rahu/Ketu): all in two successive kendras (1&4, 4&7, 7&10 or 10&1).
- **Strength:** Said to operate through life, not only in specific dashas. Most are rare; weight by how exactly the pattern holds.
- **Cancellation:** Nabhasa yogas have no bhanga. Precedence: if an Akriti/Asraya/Dala yoga is present, the Sankhya yoga is ignored; Asraya is ignored if an Akriti yoga coincides (Varahamihira).
- **Result:** Effortful earner, ritual-minded, wealthy, learned.
- **Source:** BPHS ch. 35 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 12.2-19 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/) - definitions confirmed

### Shakata yoga (Nabhasa)  `nabhasa_shakata`
- **Condition:** Using the seven planets Sun..Saturn only (no Rahu/Ketu): all in houses 1 and 7.
- **Strength:** Said to operate through life, not only in specific dashas. Most are rare; weight by how exactly the pattern holds.
- **Cancellation:** Nabhasa yogas have no bhanga. Precedence: if an Akriti/Asraya/Dala yoga is present, the Sankhya yoga is ignored; Asraya is ignored if an Akriti yoga coincides (Varahamihira).
- **Result:** Sickly, poor, lives by carts/transport, dull, ordinary spouse.
- **Source:** BPHS ch. 35 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 12.2-19 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/) - definitions confirmed

### Vihaga (Pakshi) yoga (Nabhasa)  `nabhasa_vihaga`
- **Condition:** Using the seven planets Sun..Saturn only (no Rahu/Ketu): all in houses 4 and 10.
- **Strength:** Said to operate through life, not only in specific dashas. Most are rare; weight by how exactly the pattern holds.
- **Cancellation:** Nabhasa yogas have no bhanga. Precedence: if an Akriti/Asraya/Dala yoga is present, the Sankhya yoga is ignored; Asraya is ignored if an Akriti yoga coincides (Varahamihira).
- **Result:** Wanderer, messenger, quarrelsome.
- **Source:** BPHS ch. 35 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 12.2-19 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/) - definitions confirmed
- **Note:** The BPHS e-text read prints '9th and 10th'; Brihat Jataka and the Wikipedia table give 4th and 10th - use 4 & 10.

### Shringataka yoga (Nabhasa)  `nabhasa_shringataka`
- **Condition:** Using the seven planets Sun..Saturn only (no Rahu/Ketu): all in houses 1, 5 and 9.
- **Strength:** Said to operate through life, not only in specific dashas. Most are rare; weight by how exactly the pattern holds.
- **Cancellation:** Nabhasa yogas have no bhanga. Precedence: if an Akriti/Asraya/Dala yoga is present, the Sankhya yoga is ignored; Asraya is ignored if an Akriti yoga coincides (Varahamihira).
- **Result:** Fond of contest, happy, dear to rulers, good spouse.
- **Source:** BPHS ch. 35 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 12.2-19 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/) - definitions confirmed

### Hala yoga (Nabhasa)  `nabhasa_hala`
- **Condition:** Using the seven planets Sun..Saturn only (no Rahu/Ketu): all in one of the non-lagna trine sets: {2,6,10} or {3,7,11} or {4,8,12}.
- **Strength:** Said to operate through life, not only in specific dashas. Most are rare; weight by how exactly the pattern holds.
- **Cancellation:** Nabhasa yogas have no bhanga. Precedence: if an Akriti/Asraya/Dala yoga is present, the Sankhya yoga is ignored; Asraya is ignored if an Akriti yoga coincides (Varahamihira).
- **Result:** Farmer, big eater, poor, servant, troubled.
- **Source:** BPHS ch. 35 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 12.2-19 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/) - definitions confirmed

### Vajra yoga (Nabhasa)  `nabhasa_vajra`
- **Condition:** Using the seven planets Sun..Saturn only (no Rahu/Ketu): benefics in houses 1 and 7 AND malefics in houses 4 and 10.
- **Strength:** Said to operate through life, not only in specific dashas. Most are rare; weight by how exactly the pattern holds.
- **Cancellation:** Nabhasa yogas have no bhanga. Precedence: if an Akriti/Asraya/Dala yoga is present, the Sankhya yoga is ignored; Asraya is ignored if an Akriti yoga coincides (Varahamihira).
- **Result:** Happy at start and end of life, valiant.
- **Source:** BPHS ch. 35 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 12.2-19 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/) - definitions confirmed
- **Note:** Varahamihira notes Vajra/Yava can hardly occur (Mercury/Venus cannot be 4 signs from the Sun) and lists them out of respect for earlier authors.

### Yava yoga (Nabhasa)  `nabhasa_yava`
- **Condition:** Using the seven planets Sun..Saturn only (no Rahu/Ketu): malefics in houses 1 and 7 AND benefics in houses 4 and 10.
- **Strength:** Said to operate through life, not only in specific dashas. Most are rare; weight by how exactly the pattern holds.
- **Cancellation:** Nabhasa yogas have no bhanga. Precedence: if an Akriti/Asraya/Dala yoga is present, the Sankhya yoga is ignored; Asraya is ignored if an Akriti yoga coincides (Varahamihira).
- **Result:** Happy in mid-life, pious, charitable, steady.
- **Source:** BPHS ch. 35 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 12.2-19 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/) - definitions confirmed

### Kamala (Padma) yoga (Nabhasa)  `nabhasa_kamala`
- **Condition:** Using the seven planets Sun..Saturn only (no Rahu/Ketu): all distributed in the four kendras 1, 4, 7, 10.
- **Strength:** Said to operate through life, not only in specific dashas. Most are rare; weight by how exactly the pattern holds.
- **Cancellation:** Nabhasa yogas have no bhanga. Precedence: if an Akriti/Asraya/Dala yoga is present, the Sankhya yoga is ignored; Asraya is ignored if an Akriti yoga coincides (Varahamihira).
- **Result:** Famous, virtuous, long-lived, king-like.
- **Source:** BPHS ch. 35 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 12.2-19 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/) - definitions confirmed

### Vapi yoga (Nabhasa)  `nabhasa_vapi`
- **Condition:** Using the seven planets Sun..Saturn only (no Rahu/Ketu): all in panaphara houses {2,5,8,11} or all in apoklima houses {3,6,9,12}.
- **Strength:** Said to operate through life, not only in specific dashas. Most are rare; weight by how exactly the pattern holds.
- **Cancellation:** Nabhasa yogas have no bhanga. Precedence: if an Akriti/Asraya/Dala yoga is present, the Sankhya yoga is ignored; Asraya is ignored if an Akriti yoga coincides (Varahamihira).
- **Result:** Hoards wealth, steady comforts, sons.
- **Source:** BPHS ch. 35 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 12.2-19 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/) - definitions confirmed

### Yupa yoga (Nabhasa)  `nabhasa_yupa`
- **Condition:** Using the seven planets Sun..Saturn only (no Rahu/Ketu): all within houses 1, 2, 3, 4.
- **Strength:** Said to operate through life, not only in specific dashas. Most are rare; weight by how exactly the pattern holds.
- **Cancellation:** Nabhasa yogas have no bhanga. Precedence: if an Akriti/Asraya/Dala yoga is present, the Sankhya yoga is ignored; Asraya is ignored if an Akriti yoga coincides (Varahamihira).
- **Result:** Self-knowledge, ritual, vows, charitable.
- **Source:** BPHS ch. 35 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 12.2-19 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/) - definitions confirmed

### Ishu (Shara) yoga (Nabhasa)  `nabhasa_ishu`
- **Condition:** Using the seven planets Sun..Saturn only (no Rahu/Ketu): all within houses 4, 5, 6, 7.
- **Strength:** Said to operate through life, not only in specific dashas. Most are rare; weight by how exactly the pattern holds.
- **Cancellation:** Nabhasa yogas have no bhanga. Precedence: if an Akriti/Asraya/Dala yoga is present, the Sankhya yoga is ignored; Asraya is ignored if an Akriti yoga coincides (Varahamihira).
- **Result:** Maker of arrows/weapons, jailer, hunter-like trades.
- **Source:** BPHS ch. 35 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 12.2-19 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/) - definitions confirmed

### Shakti yoga (Nabhasa)  `nabhasa_shakti`
- **Condition:** Using the seven planets Sun..Saturn only (no Rahu/Ketu): all within houses 7, 8, 9, 10.
- **Strength:** Said to operate through life, not only in specific dashas. Most are rare; weight by how exactly the pattern holds.
- **Cancellation:** Nabhasa yogas have no bhanga. Precedence: if an Akriti/Asraya/Dala yoga is present, the Sankhya yoga is ignored; Asraya is ignored if an Akriti yoga coincides (Varahamihira).
- **Result:** Lazy or unsuccessful, long-lived, skilled in war, steady.
- **Source:** BPHS ch. 35 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 12.2-19 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/) - definitions confirmed

### Danda yoga (Nabhasa)  `nabhasa_danda`
- **Condition:** Using the seven planets Sun..Saturn only (no Rahu/Ketu): all within houses 10, 11, 12, 1.
- **Strength:** Said to operate through life, not only in specific dashas. Most are rare; weight by how exactly the pattern holds.
- **Cancellation:** Nabhasa yogas have no bhanga. Precedence: if an Akriti/Asraya/Dala yoga is present, the Sankhya yoga is ignored; Asraya is ignored if an Akriti yoga coincides (Varahamihira).
- **Result:** Loses sons/spouse, poor, serves the low, estranged from kin.
- **Source:** BPHS ch. 35 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 12.2-19 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/) - definitions confirmed

### Nauka yoga (Nabhasa)  `nabhasa_nauka`
- **Condition:** Using the seven planets Sun..Saturn only (no Rahu/Ketu): all in the seven consecutive houses 1-7 (one in each, per strict reading).
- **Strength:** Said to operate through life, not only in specific dashas. Most are rare; weight by how exactly the pattern holds.
- **Cancellation:** Nabhasa yogas have no bhanga. Precedence: if an Akriti/Asraya/Dala yoga is present, the Sankhya yoga is ignored; Asraya is ignored if an Akriti yoga coincides (Varahamihira).
- **Result:** Earns by water, wealthy, famous, miserly.
- **Source:** BPHS ch. 35 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 12.2-19 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/) - definitions confirmed

### Koota yoga (Nabhasa)  `nabhasa_koota`
- **Condition:** Using the seven planets Sun..Saturn only (no Rahu/Ketu): all in the seven consecutive houses 4-10.
- **Strength:** Said to operate through life, not only in specific dashas. Most are rare; weight by how exactly the pattern holds.
- **Cancellation:** Nabhasa yogas have no bhanga. Precedence: if an Akriti/Asraya/Dala yoga is present, the Sankhya yoga is ignored; Asraya is ignored if an Akriti yoga coincides (Varahamihira).
- **Result:** Liar, jailer, poor, lives in hills/forts.
- **Source:** BPHS ch. 35 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 12.2-19 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/) - definitions confirmed

### Chatra yoga (Nabhasa)  `nabhasa_chatra`
- **Condition:** Using the seven planets Sun..Saturn only (no Rahu/Ketu): all in the seven consecutive houses 7-1.
- **Strength:** Said to operate through life, not only in specific dashas. Most are rare; weight by how exactly the pattern holds.
- **Cancellation:** Nabhasa yogas have no bhanga. Precedence: if an Akriti/Asraya/Dala yoga is present, the Sankhya yoga is ignored; Asraya is ignored if an Akriti yoga coincides (Varahamihira).
- **Result:** Kind, helps many, long-lived, happy at start and end.
- **Source:** BPHS ch. 35 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 12.2-19 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/) - definitions confirmed

### Chapa (Dhanus) yoga (Nabhasa)  `nabhasa_chapa`
- **Condition:** Using the seven planets Sun..Saturn only (no Rahu/Ketu): all in the seven consecutive houses 10-4.
- **Strength:** Said to operate through life, not only in specific dashas. Most are rare; weight by how exactly the pattern holds.
- **Cancellation:** Nabhasa yogas have no bhanga. Precedence: if an Akriti/Asraya/Dala yoga is present, the Sankhya yoga is ignored; Asraya is ignored if an Akriti yoga coincides (Varahamihira).
- **Result:** Liar, thief-like, wanders in forests, happy in mid-life.
- **Source:** BPHS ch. 35 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 12.2-19 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/) - definitions confirmed

### Ardha-Chandra yoga (Nabhasa)  `nabhasa_ardha_chandra`
- **Condition:** Using the seven planets Sun..Saturn only (no Rahu/Ketu): all in seven consecutive houses starting from a non-kendra house (2, 3, 5, 6, 8, 9, 11 or 12).
- **Strength:** Said to operate through life, not only in specific dashas. Most are rare; weight by how exactly the pattern holds.
- **Cancellation:** Nabhasa yogas have no bhanga. Precedence: if an Akriti/Asraya/Dala yoga is present, the Sankhya yoga is ignored; Asraya is ignored if an Akriti yoga coincides (Varahamihira).
- **Result:** Army leader, handsome, strong, gems and gold.
- **Source:** BPHS ch. 35 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 12.2-19 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/) - definitions confirmed

### Chakra yoga (Nabhasa)  `nabhasa_chakra`
- **Condition:** Using the seven planets Sun..Saturn only (no Rahu/Ketu): all in the six odd houses 1, 3, 5, 7, 9, 11.
- **Strength:** Said to operate through life, not only in specific dashas. Most are rare; weight by how exactly the pattern holds.
- **Cancellation:** Nabhasa yogas have no bhanga. Precedence: if an Akriti/Asraya/Dala yoga is present, the Sankhya yoga is ignored; Asraya is ignored if an Akriti yoga coincides (Varahamihira).
- **Result:** Emperor; kings bow to him.
- **Source:** BPHS ch. 35 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 12.2-19 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/) - definitions confirmed

### Samudra yoga (Nabhasa)  `nabhasa_samudra`
- **Condition:** Using the seven planets Sun..Saturn only (no Rahu/Ketu): all in the six even houses 2, 4, 6, 8, 10, 12.
- **Strength:** Said to operate through life, not only in specific dashas. Most are rare; weight by how exactly the pattern holds.
- **Cancellation:** Nabhasa yogas have no bhanga. Precedence: if an Akriti/Asraya/Dala yoga is present, the Sankhya yoga is ignored; Asraya is ignored if an Akriti yoga coincides (Varahamihira).
- **Result:** Many gems, wealth, pleasures, steady.
- **Source:** BPHS ch. 35 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 12.2-19 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/) - definitions confirmed

### Gola [Sankhya] yoga (Nabhasa)  `nabhasa_sankhya_gola`
- **Condition:** Using the seven planets Sun..Saturn only (no Rahu/Ketu): the seven planets occupy exactly 1 sign(s).
- **Strength:** Said to operate through life, not only in specific dashas. Most are rare; weight by how exactly the pattern holds.
- **Cancellation:** Nabhasa yogas have no bhanga. Precedence: if an Akriti/Asraya/Dala yoga is present, the Sankhya yoga is ignored; Asraya is ignored if an Akriti yoga coincides (Varahamihira).
- **Result:** Poor, sorrowful, ignorant, wanderer.
- **Source:** BPHS ch. 35 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 12.2-19 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/) - definitions confirmed

### Yuga [Sankhya] yoga (Nabhasa)  `nabhasa_sankhya_yuga`
- **Condition:** Using the seven planets Sun..Saturn only (no Rahu/Ketu): the seven planets occupy exactly 2 sign(s).
- **Strength:** Said to operate through life, not only in specific dashas. Most are rare; weight by how exactly the pattern holds.
- **Cancellation:** Nabhasa yogas have no bhanga. Precedence: if an Akriti/Asraya/Dala yoga is present, the Sankhya yoga is ignored; Asraya is ignored if an Akriti yoga coincides (Varahamihira).
- **Result:** Heretic, poor, shunned, sonless.
- **Source:** BPHS ch. 35 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 12.2-19 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/) - definitions confirmed

### Shoola [Sankhya] yoga (Nabhasa)  `nabhasa_sankhya_shoola`
- **Condition:** Using the seven planets Sun..Saturn only (no Rahu/Ketu): the seven planets occupy exactly 3 sign(s).
- **Strength:** Said to operate through life, not only in specific dashas. Most are rare; weight by how exactly the pattern holds.
- **Cancellation:** Nabhasa yogas have no bhanga. Precedence: if an Akriti/Asraya/Dala yoga is present, the Sankhya yoga is ignored; Asraya is ignored if an Akriti yoga coincides (Varahamihira).
- **Result:** Sharp, cruel, poor, brave, wounded, famed in fight.
- **Source:** BPHS ch. 35 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 12.2-19 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/) - definitions confirmed

### Kedara [Sankhya] yoga (Nabhasa)  `nabhasa_sankhya_kedara`
- **Condition:** Using the seven planets Sun..Saturn only (no Rahu/Ketu): the seven planets occupy exactly 4 sign(s).
- **Strength:** Said to operate through life, not only in specific dashas. Most are rare; weight by how exactly the pattern holds.
- **Cancellation:** Nabhasa yogas have no bhanga. Precedence: if an Akriti/Asraya/Dala yoga is present, the Sankhya yoga is ignored; Asraya is ignored if an Akriti yoga coincides (Varahamihira).
- **Result:** Farmer, truthful, happy, helps many.
- **Source:** BPHS ch. 35 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 12.2-19 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/) - definitions confirmed

### Pasha [Sankhya] yoga (Nabhasa)  `nabhasa_sankhya_pasha`
- **Condition:** Using the seven planets Sun..Saturn only (no Rahu/Ketu): the seven planets occupy exactly 5 sign(s).
- **Strength:** Said to operate through life, not only in specific dashas. Most are rare; weight by how exactly the pattern holds.
- **Cancellation:** Nabhasa yogas have no bhanga. Precedence: if an Akriti/Asraya/Dala yoga is present, the Sankhya yoga is ignored; Asraya is ignored if an Akriti yoga coincides (Varahamihira).
- **Result:** Skilled, talkative, many servants, risk of bondage.
- **Source:** BPHS ch. 35 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 12.2-19 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/) - definitions confirmed

### Dama (Damini) [Sankhya] yoga (Nabhasa)  `nabhasa_sankhya_dama`
- **Condition:** Using the seven planets Sun..Saturn only (no Rahu/Ketu): the seven planets occupy exactly 6 sign(s).
- **Strength:** Said to operate through life, not only in specific dashas. Most are rare; weight by how exactly the pattern holds.
- **Cancellation:** Nabhasa yogas have no bhanga. Precedence: if an Akriti/Asraya/Dala yoga is present, the Sankhya yoga is ignored; Asraya is ignored if an Akriti yoga coincides (Varahamihira).
- **Result:** Helps others, wealth by fair means, famous, many sons.
- **Source:** BPHS ch. 35 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 12.2-19 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/) - definitions confirmed

### Veena (Vallaki) [Sankhya] yoga (Nabhasa)  `nabhasa_sankhya_veena`
- **Condition:** Using the seven planets Sun..Saturn only (no Rahu/Ketu): the seven planets occupy exactly 7 sign(s).
- **Strength:** Said to operate through life, not only in specific dashas. Most are rare; weight by how exactly the pattern holds.
- **Cancellation:** Nabhasa yogas have no bhanga. Precedence: if an Akriti/Asraya/Dala yoga is present, the Sankhya yoga is ignored; Asraya is ignored if an Akriti yoga coincides (Varahamihira).
- **Result:** Fond of music and dance, skilful, leader, happy.
- **Source:** BPHS ch. 35 (free English rendering at sanskritdocuments.org, re-read 12 Nov 2026, https://sanskritdocuments.org/doc_z_misc_sociology_astrology/horaashaastraEng34-45-gu.pdf) ; Brihat Jataka 12.2-19 (read in the Sanskrit, 12 Nov 2026; notes in kb/sources/brihat-jataka/) - definitions confirmed

## Tradition disagreements worth encoding
- **Mahapurusha reference point.** BPHS ch. 75 counts kendras from Lagna only. Phaladeepika and later practice also count from the Moon. Engine: tag `from_lagna` vs `from_moon`; the Moon-based one gets lower weight and, in the 7th from Moon, the project calibration above.
- **Kemadruma.** BPHS folds 'no planet in a kendra from Lagna' into the definition; the Varahamihira line makes kendra occupation a cancellation. Outcome is the same for code, but report which bhanga applied.
- **Gajakesari.** BPHS wants benefic association and an unafflicted Jupiter; the popular version ('Jupiter in a kendra from Moon') is true for about a third of all people.
- **Viparita.** Phaladeepika: 6th/8th/12th lord in any dusthana. Stricter schools want it in its own or another dusthana with no good-house lord involved. BPHS 39 states it as dusthana lords being weak.
- **Neecha bhanga.** Only conditions 1-4 are in the Phaladeepika verses read. Navamsa exaltation, aspect by another debilitated planet, retrograde and 'in a kendra itself' are later additions.
- **Vajra / Yava.** The page read from the BPHS e-text joins the two halves with 'or'; Brihat Jataka requires both halves. Use 'and'.
- **Kaal Sarp.** Not classical. Keep it in the report as a modern pattern with low weight and always show what breaks it.
- **Shrapit / Angaraka / Vish / Guru-Chandala / Grahan as 'doshas'.** The conjunctions are real and classical texts describe them, but the dosha names, the fear attached and the paid remedies are modern.

## Reliability notes
**Classical consensus (read this session in the cited e-texts):** Pancha Mahapurusha (BPHS 75); Sunapha/Anapha/Durudhara/Kemadruma, Adhi, Vasumati (BPHS 37); Vesi/Vasi/Ubhayachari (BPHS 38); the BPHS 36 group (Gajakesari, Amala, Parvata, Kahala, Chamara, Shankha, Bheri, Mridanga, Shrinatha, Sharada, Matsya, Kurma, Khadga, Lakshmi, Kusuma, Kalanidhi, Kalpadruma, Hari-Hara-Brahma, Lagnadhi); kendra-trikona raja yoga and yogakaraka (BPHS 34, 39, 40); dhana and daridra sets (BPHS 41, 42); the 32 Nabhasa yogas (BPHS 35, cross-checked with the Wikipedia table that cites Brihat Jataka 12); pravrajya (BPHS 79); shapa yogas and birth doshas (BPHS 83, 85-94); the twelve Phaladeepika house-lord yogas incl. Harsha/Sarala/Vimala (results read at 6.58-70; formation per standard commentary); neecha bhanga 1-4 (Phaladeepika 7.26-30).

**Checked against the Sanskrit on 12 Nov 2026:** Saraswati, lunar Shakata, Budha-Aditya, Akhanda Samrajya, Maha/Khala/Dainya parivartana and Balarishta now carry their verse numbers. Chandra-Mangala as a wealth yoga, Guru-Chandala and Angaraka are **not** in Parashara or Phaladeepika as read and stay low confidence.

**Secondary web sources used (treat as pointers, not authority):** Wikipedia (Nabhasa; Neechabhanga via an IPFS mirror, which itself flags uneven attributions), barbarapijan.com (for Raman's statements on Kaal Sarp), jagannathhora.com, satyori.com (Kemadruma bhanga list without text attributions).

**Modern internet lore (keep, but label):** Kaal Sarp and its 12 names; Shrapit, Angaraka, Vish, Guru-Chandala and Grahan as named 'doshas'; the wide popular Pitru dosha; neecha bhanga by retrogression or by the planet's own kendra position; degree bands for Budha-Aditya; the long Mangal dosha exception lists.

**Could not access:** P.V.R. Narasimha Rao's textbook PDF (vedicastrologer.org blocked from this environment), B.V. Raman's book text, K.N. Rao's own articles on Kaal Sarp, Saravali and Jataka Parijata primary text.

## Corrections from the Sanskrit (12 Nov 2026)
Fourteen entries citing Parashara chapters 75-92 were re-read in the Sanskrit. `yogas.json` carries the corrected conditions and `kb/sources/bphs-verse-readings.md` the verse readings; where this file differs, those two win. Corrected: serpent curse (needs Saturn in the 5th with the Moon, not just the 5th lord with Rahu), Pitru dosha (Parashara's version is narrow and about children; the common one is not his), gandanta (window about 0d27', not 3d20'), Saturn's renunciation (drekkana AND navamsa), eclipse birth (an actual eclipse), Vish yoga (not in Parashara at all).

