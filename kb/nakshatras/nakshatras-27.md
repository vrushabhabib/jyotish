# The 27 nakshatras (compact reference)

Tradition: Parashari, Lahiri ayanamsa. Each nakshatra = 13°20'; each pada = 3°20' = one navamsa. Attribute columns (lord, deity, symbol, gana, yoni, nadi, guna, purushartha, nature) are taken from the project's own `data/nakshatras.json` so the KB and engine agree; traits, professions and health areas are paraphrased consensus of standard nakshatra manuals (see Reliability notes).

## How code should use this file
- `nak_index = floor(moon_longitude / 13.3333) + 1`; `pada = floor((moon_longitude mod 13.3333) / 3.3333) + 1`.
- Navamsa sign of a pada: `SIGNS[((nak_index-1)*4 + (pada-1)) mod 12]` (starts at Aries for Ashwini 1).
- Vargottama padas (D1 sign = D9 sign) are the 1st navamsa of movable signs, the 5th of fixed signs and the 9th of dual signs; they are computed and tagged `[vargottama]` below.
- **Gandanta:** the last pada of Ashlesha, Jyeshtha, Revati and the first pada of Magha, Mula, Ashwini (BPHS ch. 92). Narrow form used by many: within 0°48' of the junction; wide form: the whole 3°20' pada. Abhukta Mula: last 6 ghatis of Jyeshtha + first 8 ghatis of Mula (BPHS ch. 93).
- **Abhijit:** the intercalary 28th star, 6°40' – 10°53'20" Capricorn (last pada of Uttara Ashadha + the first 1/15 of Shravana). Deity Brahma; no Vimshottari lord; ignored in dasha, koota matching and pada/navamsa maths; used in muhurta (Abhijit muhurta around local noon), Sarvatobhadra chakra and 28-star schemes.
- Nature classes and muhurta use: Dhruva/fixed (Rohini, U.Phalguni, U.Ashadha, U.Bhadrapada) for lasting works; Chara/movable (Punarvasu, Swati, Shravana, Dhanishta, Shatabhisha) for travel/vehicles; Ugra/fierce (Bharani, Magha, the three Purvas) for harsh acts; Mishra/mixed (Krittika, Vishakha); Kshipra/swift (Ashwini, Pushya, Hasta) for trade, medicine, travel; Mridu/soft (Mrigashira, Chitra, Anuradha, Revati) for arts, friendship, romance; Tikshna/sharp (Ardra, Ashlesha, Jyeshtha, Mula) for surgery, separation, exorcism.
- Compatibility lines below are computed from two matching rules only: **vedha pairs** (stars that obstruct each other; avoid for marriage) and **yoni enmity** (0 points in Yoni koota). Full matching needs all eight kootas - see the matching KB.
- Pushkara navamsa padas are computed and tagged `[pushkara]` using the common rule: fire signs 7th and 9th navamsa (Libra, Sagittarius); earth signs 3rd and 5th (Pisces, Taurus); air signs 6th and 8th (Pisces, Taurus); water signs 1st and 3rd (Cancer, Virgo). Rule stated from working knowledge of muhurta practice; not re-read this session.

## Master table

| # | Nakshatra | Span (sidereal) | Lord | Deity | Symbol | Gana | Yoni | Nadi | Guna | Purushartha | Nature |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Ashwini | 0°00' Aries – 13°20' Aries | Ketu | Ashwini Kumaras | Horse's head | Deva | Horse (M) | Adi | Rajas | Dharma | Kshipra (swift) |
| 2 | Bharani | 13°20' Aries – 26°40' Aries | Venus | Yama | Yoni / womb | Manushya | Elephant (M) | Madhya | Rajas | Artha | Ugra (fierce) |
| 3 | Krittika | 26°40' Aries – 10°00' Taurus | Sun | Agni | Razor / flame | Rakshasa | Sheep (F) | Antya | Rajas | Kama | Mishra (mixed) |
| 4 | Rohini | 10°00' Taurus – 23°20' Taurus | Moon | Brahma / Prajapati | Cart / chariot | Manushya | Serpent (M) | Antya | Rajas | Moksha | Dhruva (fixed) |
| 5 | Mrigashira | 23°20' Taurus – 6°40' Gemini | Mars | Soma | Deer's head | Deva | Serpent (F) | Madhya | Tamas | Moksha | Mridu (soft) |
| 6 | Ardra | 6°40' Gemini – 20°00' Gemini | Rahu | Rudra | Teardrop / gem | Manushya | Dog (F) | Adi | Tamas | Kama | Tikshna (sharp) |
| 7 | Punarvasu | 20°00' Gemini – 3°20' Cancer | Jupiter | Aditi | Bow and quiver | Deva | Cat (F) | Adi | Sattva | Artha | Chara (movable) |
| 8 | Pushya | 3°20' Cancer – 16°40' Cancer | Saturn | Brihaspati | Cow's udder / lotus | Deva | Sheep (M) | Madhya | Tamas | Dharma | Kshipra (swift) |
| 9 | Ashlesha | 16°40' Cancer – 30°00' Cancer | Mercury | Nagas | Coiled serpent | Rakshasa | Cat (M) | Antya | Sattva | Dharma | Tikshna (sharp) |
| 10 | Magha | 0°00' Leo – 13°20' Leo | Ketu | Pitris | Throne | Rakshasa | Rat (M) | Antya | Tamas | Artha | Ugra (fierce) |
| 11 | Purva Phalguni | 13°20' Leo – 26°40' Leo | Venus | Bhaga | Front legs of bed / hammock | Manushya | Rat (F) | Madhya | Rajas | Kama | Ugra (fierce) |
| 12 | Uttara Phalguni | 26°40' Leo – 10°00' Virgo | Sun | Aryaman | Back legs of bed | Manushya | Cow (M) | Adi | Rajas | Moksha | Dhruva (fixed) |
| 13 | Hasta | 10°00' Virgo – 23°20' Virgo | Moon | Savitar | Hand / fist | Deva | Buffalo (F) | Adi | Rajas | Moksha | Kshipra (swift) |
| 14 | Chitra | 23°20' Virgo – 6°40' Libra | Mars | Vishwakarma / Tvashtar | Bright jewel / pearl | Rakshasa | Tiger (F) | Madhya | Tamas | Kama | Mridu (soft) |
| 15 | Swati | 6°40' Libra – 20°00' Libra | Rahu | Vayu | Young sprout in wind / coral | Deva | Buffalo (M) | Antya | Tamas | Artha | Chara (movable) |
| 16 | Vishakha | 20°00' Libra – 3°20' Scorpio | Jupiter | Indra-Agni | Triumphal archway / potter's wheel | Rakshasa | Tiger (M) | Antya | Sattva | Dharma | Mishra (mixed) |
| 17 | Anuradha | 3°20' Scorpio – 16°40' Scorpio | Saturn | Mitra | Lotus / staff | Deva | Deer (F) | Madhya | Tamas | Dharma | Mridu (soft) |
| 18 | Jyeshtha | 16°40' Scorpio – 30°00' Scorpio | Mercury | Indra | Earring / umbrella / talisman | Rakshasa | Deer (M) | Adi | Sattva | Artha | Tikshna (sharp) |
| 19 | Mula | 0°00' Sagittarius – 13°20' Sagittarius | Ketu | Nirriti | Bunch of roots / lion's tail | Rakshasa | Dog (M) | Adi | Tamas | Kama | Tikshna (sharp) |
| 20 | Purva Ashadha | 13°20' Sagittarius – 26°40' Sagittarius | Venus | Apas | Elephant tusk / fan / winnowing basket | Manushya | Monkey (M) | Madhya | Rajas | Moksha | Ugra (fierce) |
| 21 | Uttara Ashadha | 26°40' Sagittarius – 10°00' Capricorn | Sun | Vishvadevas | Elephant tusk / planks of bed | Manushya | Mongoose (F) | Antya | Rajas | Moksha | Dhruva (fixed) |
| 22 | Shravana | 10°00' Capricorn – 23°20' Capricorn | Moon | Vishnu | Ear / three footprints | Deva | Monkey (F) | Antya | Rajas | Artha | Chara (movable) |
| 23 | Dhanishta | 23°20' Capricorn – 6°40' Aquarius | Mars | Eight Vasus | Drum / flute | Rakshasa | Lion (F) | Madhya | Tamas | Dharma | Chara (movable) |
| 24 | Shatabhisha | 6°40' Aquarius – 20°00' Aquarius | Rahu | Varuna | Empty circle / 100 physicians | Rakshasa | Horse (F) | Adi | Tamas | Dharma | Chara (movable) |
| 25 | Purva Bhadrapada | 20°00' Aquarius – 3°20' Pisces | Jupiter | Aja Ekapada | Front legs of funeral cot / sword | Manushya | Lion (M) | Adi | Sattva | Artha | Ugra (fierce) |
| 26 | Uttara Bhadrapada | 3°20' Pisces – 16°40' Pisces | Saturn | Ahir Budhnya | Back legs of funeral cot / twins | Manushya | Cow (F) | Madhya | Tamas | Kama | Dhruva (fixed) |
| 27 | Revati | 16°40' Pisces – 30°00' Pisces | Mercury | Pushan | Fish / drum | Deva | Elephant (F) | Antya | Sattva | Moksha | Mridu (soft) |

## Per-nakshatra detail

### 1. Ashwini — 0°00' Aries – 13°20' Aries
- **Keys:** lord Ketu; deity Ashwini Kumaras; symbol Horse's head; Deva gana; Horse yoni (M); Adi nadi; Rajas; Dharma; Kshipra (swift).
- **Moon here:** quick, pioneering, helpful, youthful, impatient; healer instinct.
- **Padas:**
  - Pada 1 (Aries rasi → Aries navamsa) [vargottama, gandanta]: initiative, haste, pioneering push.
  - Pada 2 (Aries rasi → Taurus navamsa): steadiness, resources, sensual ease.
  - Pada 3 (Aries rasi → Gemini navamsa): talk, trade, curiosity.
  - Pada 4 (Aries rasi → Cancer navamsa): feeling, nurture, home ties.
- **Professions:** medicine, emergency work, transport, horses/vehicles, sport, start-ups.
- **Health area:** head, brain; injuries from haste.
- **Compatibility:** same-yoni partner star: Shatabhisha. Avoid/check: vedha with Jyeshtha; yoni enemy (Buffalo): Hasta, Swati. Same nadi (Adi) with the partner's star = nadi dosha.
- **Gandanta:** first pada = Pisces-Aries gandanta.

### 2. Bharani — 13°20' Aries – 26°40' Aries
- **Keys:** lord Venus; deity Yama; symbol Yoni / womb; Manushya gana; Elephant yoni (M); Madhya nadi; Rajas; Artha; Ugra (fierce).
- **Moon here:** carries burdens, strong will, sensual, blunt, extremes; sense of duty and restraint.
- **Padas:**
  - Pada 1 (Aries rasi → Leo navamsa): pride, leadership, visibility.
  - Pada 2 (Aries rasi → Virgo navamsa): analysis, service, craft.
  - Pada 3 (Aries rasi → Libra navamsa) [pushkara]: relating, balance, aesthetics.
  - Pada 4 (Aries rasi → Scorpio navamsa): intensity, secrecy, upheaval.
- **Professions:** obstetrics, hospitality, entertainment, judiciary, undertakers, finance.
- **Health area:** head/face, reproductive organs.
- **Compatibility:** same-yoni partner star: Revati. Avoid/check: vedha with Anuradha; yoni enemy (Lion): Dhanishta, Purva Bhadrapada. Same nadi (Madhya) with the partner's star = nadi dosha.

### 3. Krittika — 26°40' Aries – 10°00' Taurus
- **Keys:** lord Sun; deity Agni; symbol Razor / flame; Rakshasa gana; Sheep yoni (F); Antya nadi; Rajas; Kama; Mishra (mixed).
- **Moon here:** sharp, critical, proud, protective, good appetite; cuts through.
- **Padas:**
  - Pada 1 (Aries rasi → Sagittarius navamsa) [pushkara]: principle, teaching, aim.
  - Pada 2 (Taurus rasi → Capricorn navamsa): duty, structure, ambition.
  - Pada 3 (Taurus rasi → Aquarius navamsa): ideas, networks, detachment.
  - Pada 4 (Taurus rasi → Pisces navamsa) [pushkara]: imagination, surrender, compassion.
- **Professions:** military, fire/metal work, cooking, surgery, teaching, criticism.
- **Health area:** face, eyes, neck; fevers, digestion.
- **Compatibility:** same-yoni partner star: Pushya. Avoid/check: vedha with Vishakha; yoni enemy (Monkey): Purva Ashadha, Shravana. Same nadi (Antya) with the partner's star = nadi dosha.

### 4. Rohini — 10°00' Taurus – 23°20' Taurus
- **Keys:** lord Moon; deity Brahma / Prajapati; symbol Cart / chariot; Manushya gana; Serpent yoni (M); Antya nadi; Rajas; Moksha; Dhruva (fixed).
- **Moon here:** attractive, steady, loves comfort and beauty, possessive, fertile mind.
- **Padas:**
  - Pada 1 (Taurus rasi → Aries navamsa): initiative, haste, pioneering push.
  - Pada 2 (Taurus rasi → Taurus navamsa) [vargottama, pushkara]: steadiness, resources, sensual ease.
  - Pada 3 (Taurus rasi → Gemini navamsa): talk, trade, curiosity.
  - Pada 4 (Taurus rasi → Cancer navamsa): feeling, nurture, home ties.
- **Professions:** agriculture, fashion, food, banking, arts, hospitality, real estate.
- **Health area:** face, mouth, throat, tonsils.
- **Compatibility:** same-yoni partner star: Mrigashira. Avoid/check: vedha with Swati; yoni enemy (Mongoose): Uttara Ashadha. Same nadi (Antya) with the partner's star = nadi dosha.

### 5. Mrigashira — 23°20' Taurus – 6°40' Gemini
- **Keys:** lord Mars; deity Soma; symbol Deer's head; Deva gana; Serpent yoni (F); Madhya nadi; Tamas; Moksha; Mridu (soft).
- **Moon here:** searching, gentle, curious, restless, suspicious; fond of travel.
- **Padas:**
  - Pada 1 (Taurus rasi → Leo navamsa): pride, leadership, visibility.
  - Pada 2 (Taurus rasi → Virgo navamsa): analysis, service, craft.
  - Pada 3 (Gemini rasi → Libra navamsa): relating, balance, aesthetics.
  - Pada 4 (Gemini rasi → Scorpio navamsa): intensity, secrecy, upheaval.
- **Professions:** research, textiles, music, writing, sales, travel, forestry.
- **Health area:** chin, throat, vocal cords, shoulders.
- **Compatibility:** same-yoni partner star: Rohini. Avoid/check: vedha with Chitra, Dhanishta; yoni enemy (Mongoose): Uttara Ashadha. Same nadi (Madhya) with the partner's star = nadi dosha.

### 6. Ardra — 6°40' Gemini – 20°00' Gemini
- **Keys:** lord Rahu; deity Rudra; symbol Teardrop / gem; Manushya gana; Dog yoni (F); Adi nadi; Tamas; Kama; Tikshna (sharp).
- **Moon here:** intense, analytical, stormy feelings, transformation through loss, sharp speech.
- **Padas:**
  - Pada 1 (Gemini rasi → Sagittarius navamsa): principle, teaching, aim.
  - Pada 2 (Gemini rasi → Capricorn navamsa): duty, structure, ambition.
  - Pada 3 (Gemini rasi → Aquarius navamsa): ideas, networks, detachment.
  - Pada 4 (Gemini rasi → Pisces navamsa) [pushkara]: imagination, surrender, compassion.
- **Professions:** software/engineering, pharmacy, research, surgery, electrical work, crisis jobs.
- **Health area:** shoulders, arms, lungs; nervous strain.
- **Compatibility:** same-yoni partner star: Mula. Avoid/check: vedha with Shravana; yoni enemy (Deer): Anuradha, Jyeshtha. Same nadi (Adi) with the partner's star = nadi dosha.

### 7. Punarvasu — 20°00' Gemini – 3°20' Cancer
- **Keys:** lord Jupiter; deity Aditi; symbol Bow and quiver; Deva gana; Cat yoni (F); Adi nadi; Sattva; Artha; Chara (movable).
- **Moon here:** returns to good, generous, simple, philosophical, home-loving, repeats and renews.
- **Padas:**
  - Pada 1 (Gemini rasi → Aries navamsa): initiative, haste, pioneering push.
  - Pada 2 (Gemini rasi → Taurus navamsa) [pushkara]: steadiness, resources, sensual ease.
  - Pada 3 (Gemini rasi → Gemini navamsa) [vargottama]: talk, trade, curiosity.
  - Pada 4 (Cancer rasi → Cancer navamsa) [vargottama, pushkara]: feeling, nurture, home ties.
- **Professions:** teaching, writing, counselling, travel/import-export, architecture, housing.
- **Health area:** ears, throat, lungs, chest.
- **Compatibility:** same-yoni partner star: Ashlesha. Avoid/check: vedha with Uttara Ashadha; yoni enemy (Rat): Magha, Purva Phalguni. Same nadi (Adi) with the partner's star = nadi dosha.

### 8. Pushya — 3°20' Cancer – 16°40' Cancer
- **Keys:** lord Saturn; deity Brihaspati; symbol Cow's udder / lotus; Deva gana; Sheep yoni (M); Madhya nadi; Tamas; Dharma; Kshipra (swift).
- **Moon here:** nourishing, dutiful, conservative, patient; best star for most undertakings (not marriage).
- **Padas:**
  - Pada 1 (Cancer rasi → Leo navamsa): pride, leadership, visibility.
  - Pada 2 (Cancer rasi → Virgo navamsa) [pushkara]: analysis, service, craft.
  - Pada 3 (Cancer rasi → Libra navamsa): relating, balance, aesthetics.
  - Pada 4 (Cancer rasi → Scorpio navamsa): intensity, secrecy, upheaval.
- **Professions:** advisers, clergy, dairy/food, public service, teaching, care work.
- **Health area:** lungs, stomach, ribs.
- **Compatibility:** same-yoni partner star: Krittika. Avoid/check: vedha with Purva Ashadha; yoni enemy (Monkey): Purva Ashadha, Shravana. Same nadi (Madhya) with the partner's star = nadi dosha.

### 9. Ashlesha — 16°40' Cancer – 30°00' Cancer
- **Keys:** lord Mercury; deity Nagas; symbol Coiled serpent; Rakshasa gana; Cat yoni (M); Antya nadi; Sattva; Dharma; Tikshna (sharp).
- **Moon here:** perceptive, secretive, hypnotic, shrewd, clings; cutting when hurt.
- **Padas:**
  - Pada 1 (Cancer rasi → Sagittarius navamsa): principle, teaching, aim.
  - Pada 2 (Cancer rasi → Capricorn navamsa): duty, structure, ambition.
  - Pada 3 (Cancer rasi → Aquarius navamsa): ideas, networks, detachment.
  - Pada 4 (Cancer rasi → Pisces navamsa) [gandanta]: imagination, surrender, compassion.
- **Professions:** psychology, poisons/pharma, law, politics, occult, intelligence work.
- **Health area:** stomach, oesophagus, joints, nerves.
- **Compatibility:** same-yoni partner star: Punarvasu. Avoid/check: vedha with Mula; yoni enemy (Rat): Magha, Purva Phalguni. Same nadi (Antya) with the partner's star = nadi dosha.
- **Gandanta:** last pada = Cancer-Leo gandanta.

### 10. Magha — 0°00' Leo – 13°20' Leo
- **Keys:** lord Ketu; deity Pitris; symbol Throne; Rakshasa gana; Rat yoni (M); Antya nadi; Tamas; Artha; Ugra (fierce).
- **Moon here:** regal, tradition- and ancestor-minded, generous, proud, commanding.
- **Padas:**
  - Pada 1 (Leo rasi → Aries navamsa) [gandanta]: initiative, haste, pioneering push.
  - Pada 2 (Leo rasi → Taurus navamsa): steadiness, resources, sensual ease.
  - Pada 3 (Leo rasi → Gemini navamsa): talk, trade, curiosity.
  - Pada 4 (Leo rasi → Cancer navamsa): feeling, nurture, home ties.
- **Professions:** administration, heritage/history, politics, law, family business heads.
- **Health area:** heart, back, spine.
- **Compatibility:** same-yoni partner star: Purva Phalguni. Avoid/check: vedha with Revati; yoni enemy (Cat): Punarvasu, Ashlesha. Same nadi (Antya) with the partner's star = nadi dosha.
- **Gandanta:** first pada = Cancer-Leo gandanta.

### 11. Purva Phalguni — 13°20' Leo – 26°40' Leo
- **Keys:** lord Venus; deity Bhaga; symbol Front legs of bed / hammock; Manushya gana; Rat yoni (F); Madhya nadi; Rajas; Kama; Ugra (fierce).
- **Moon here:** pleasure-loving, charming, creative, sociable, vain, needs rest.
- **Padas:**
  - Pada 1 (Leo rasi → Leo navamsa) [vargottama]: pride, leadership, visibility.
  - Pada 2 (Leo rasi → Virgo navamsa): analysis, service, craft.
  - Pada 3 (Leo rasi → Libra navamsa) [pushkara]: relating, balance, aesthetics.
  - Pada 4 (Leo rasi → Scorpio navamsa): intensity, secrecy, upheaval.
- **Professions:** arts, entertainment, luxury goods, weddings/events, hospitality, teaching arts.
- **Health area:** heart, spine, reproductive organs.
- **Compatibility:** same-yoni partner star: Magha. Avoid/check: vedha with Uttara Bhadrapada; yoni enemy (Cat): Punarvasu, Ashlesha. Same nadi (Madhya) with the partner's star = nadi dosha.

### 12. Uttara Phalguni — 26°40' Leo – 10°00' Virgo
- **Keys:** lord Sun; deity Aryaman; symbol Back legs of bed; Manushya gana; Cow yoni (M); Adi nadi; Rajas; Moksha; Dhruva (fixed).
- **Moon here:** helpful, reliable, patron-like, contractual, principled, sometimes stubborn.
- **Padas:**
  - Pada 1 (Leo rasi → Sagittarius navamsa) [pushkara]: principle, teaching, aim.
  - Pada 2 (Virgo rasi → Capricorn navamsa): duty, structure, ambition.
  - Pada 3 (Virgo rasi → Aquarius navamsa): ideas, networks, detachment.
  - Pada 4 (Virgo rasi → Pisces navamsa) [pushkara]: imagination, surrender, compassion.
- **Professions:** social work, HR, administration, contracts/marriage services, healing.
- **Health area:** lower spine, intestines, liver.
- **Compatibility:** same-yoni partner star: Uttara Bhadrapada. Avoid/check: vedha with Purva Bhadrapada; yoni enemy (Tiger): Chitra, Vishakha. Same nadi (Adi) with the partner's star = nadi dosha.

### 13. Hasta — 10°00' Virgo – 23°20' Virgo
- **Keys:** lord Moon; deity Savitar; symbol Hand / fist; Deva gana; Buffalo yoni (F); Adi nadi; Rajas; Moksha; Kshipra (swift).
- **Moon here:** skilful hands, clever, witty, industrious, controlling, good at trade.
- **Padas:**
  - Pada 1 (Virgo rasi → Aries navamsa): initiative, haste, pioneering push.
  - Pada 2 (Virgo rasi → Taurus navamsa) [pushkara]: steadiness, resources, sensual ease.
  - Pada 3 (Virgo rasi → Gemini navamsa): talk, trade, curiosity.
  - Pada 4 (Virgo rasi → Cancer navamsa): feeling, nurture, home ties.
- **Professions:** crafts, surgery, massage, stationery/printing, trade, astrology, magic/sleight.
- **Health area:** hands, bowels, intestines.
- **Compatibility:** same-yoni partner star: Swati. Avoid/check: vedha with Shatabhisha; yoni enemy (Horse): Ashwini, Shatabhisha. Same nadi (Adi) with the partner's star = nadi dosha.

### 14. Chitra — 23°20' Virgo – 6°40' Libra
- **Keys:** lord Mars; deity Vishwakarma / Tvashtar; symbol Bright jewel / pearl; Rakshasa gana; Tiger yoni (F); Madhya nadi; Tamas; Kama; Mridu (soft).
- **Moon here:** artistic, exact, elegant, charismatic, argumentative, builder.
- **Padas:**
  - Pada 1 (Virgo rasi → Leo navamsa): pride, leadership, visibility.
  - Pada 2 (Virgo rasi → Virgo navamsa) [vargottama]: analysis, service, craft.
  - Pada 3 (Libra rasi → Libra navamsa) [vargottama]: relating, balance, aesthetics.
  - Pada 4 (Libra rasi → Scorpio navamsa): intensity, secrecy, upheaval.
- **Professions:** architecture, design, jewellery, engineering, fashion, photography.
- **Health area:** kidneys, lower abdomen, forehead.
- **Compatibility:** same-yoni partner star: Vishakha. Avoid/check: vedha with Mrigashira, Dhanishta; yoni enemy (Cow): Uttara Phalguni, Uttara Bhadrapada. Same nadi (Madhya) with the partner's star = nadi dosha.

### 15. Swati — 6°40' Libra – 20°00' Libra
- **Keys:** lord Rahu; deity Vayu; symbol Young sprout in wind / coral; Deva gana; Buffalo yoni (M); Antya nadi; Tamas; Artha; Chara (movable).
- **Moon here:** independent, flexible, polite, self-made, restless like wind; learns by moving.
- **Padas:**
  - Pada 1 (Libra rasi → Sagittarius navamsa): principle, teaching, aim.
  - Pada 2 (Libra rasi → Capricorn navamsa): duty, structure, ambition.
  - Pada 3 (Libra rasi → Aquarius navamsa): ideas, networks, detachment.
  - Pada 4 (Libra rasi → Pisces navamsa) [pushkara]: imagination, surrender, compassion.
- **Professions:** trade, travel, diplomacy, sales, aviation, law, independent business.
- **Health area:** kidneys, skin, bladder; gas/wind.
- **Compatibility:** same-yoni partner star: Hasta. Avoid/check: vedha with Rohini; yoni enemy (Horse): Ashwini, Shatabhisha. Same nadi (Antya) with the partner's star = nadi dosha.

### 16. Vishakha — 20°00' Libra – 3°20' Scorpio
- **Keys:** lord Jupiter; deity Indra-Agni; symbol Triumphal archway / potter's wheel; Rakshasa gana; Tiger yoni (M); Antya nadi; Sattva; Dharma; Mishra (mixed).
- **Moon here:** goal-fixed, ambitious, competitive, jealous, eloquent; success after patience.
- **Padas:**
  - Pada 1 (Libra rasi → Aries navamsa): initiative, haste, pioneering push.
  - Pada 2 (Libra rasi → Taurus navamsa) [pushkara]: steadiness, resources, sensual ease.
  - Pada 3 (Libra rasi → Gemini navamsa): talk, trade, curiosity.
  - Pada 4 (Scorpio rasi → Cancer navamsa) [pushkara]: feeling, nurture, home ties.
- **Professions:** politics, law, liquor/fermentation, manufacturing, preaching, research.
- **Health area:** lower abdomen, bladder, pancreas, hormones.
- **Compatibility:** same-yoni partner star: Chitra. Avoid/check: vedha with Krittika; yoni enemy (Cow): Uttara Phalguni, Uttara Bhadrapada. Same nadi (Antya) with the partner's star = nadi dosha.

### 17. Anuradha — 3°20' Scorpio – 16°40' Scorpio
- **Keys:** lord Saturn; deity Mitra; symbol Lotus / staff; Deva gana; Deer yoni (F); Madhya nadi; Tamas; Dharma; Mridu (soft).
- **Moon here:** devoted friend, organiser, travels far from birthplace, sensitive, hungry.
- **Padas:**
  - Pada 1 (Scorpio rasi → Leo navamsa): pride, leadership, visibility.
  - Pada 2 (Scorpio rasi → Virgo navamsa) [pushkara]: analysis, service, craft.
  - Pada 3 (Scorpio rasi → Libra navamsa): relating, balance, aesthetics.
  - Pada 4 (Scorpio rasi → Scorpio navamsa) [vargottama]: intensity, secrecy, upheaval.
- **Professions:** organisations, diplomacy, foreign trade, mining, statistics, occult, music.
- **Health area:** bladder, genitals, rectum, hips.
- **Compatibility:** same-yoni partner star: Jyeshtha. Avoid/check: vedha with Bharani; yoni enemy (Dog): Ardra, Mula. Same nadi (Madhya) with the partner's star = nadi dosha.

### 18. Jyeshtha — 16°40' Scorpio – 30°00' Scorpio
- **Keys:** lord Mercury; deity Indra; symbol Earring / umbrella / talisman; Rakshasa gana; Deer yoni (M); Adi nadi; Sattva; Artha; Tikshna (sharp).
- **Moon here:** senior/eldest role, protective, proud, secretive, capable in crisis, few friends.
- **Padas:**
  - Pada 1 (Scorpio rasi → Sagittarius navamsa): principle, teaching, aim.
  - Pada 2 (Scorpio rasi → Capricorn navamsa): duty, structure, ambition.
  - Pada 3 (Scorpio rasi → Aquarius navamsa): ideas, networks, detachment.
  - Pada 4 (Scorpio rasi → Pisces navamsa) [gandanta]: imagination, surrender, compassion.
- **Professions:** police/military command, administration, occult, surgery, insurance, unions.
- **Health area:** colon, genitals, ovaries, neck.
- **Compatibility:** same-yoni partner star: Anuradha. Avoid/check: vedha with Ashwini; yoni enemy (Dog): Ardra, Mula. Same nadi (Adi) with the partner's star = nadi dosha.
- **Gandanta:** last pada = Scorpio-Sagittarius gandanta (Abhukta Mula with Mula 1).

### 19. Mula — 0°00' Sagittarius – 13°20' Sagittarius
- **Keys:** lord Ketu; deity Nirriti; symbol Bunch of roots / lion's tail; Rakshasa gana; Dog yoni (M); Adi nadi; Tamas; Kama; Tikshna (sharp).
- **Moon here:** goes to the root, destroys to rebuild, philosophical, blunt, losses then wisdom.
- **Padas:**
  - Pada 1 (Sagittarius rasi → Aries navamsa) [gandanta]: initiative, haste, pioneering push.
  - Pada 2 (Sagittarius rasi → Taurus navamsa): steadiness, resources, sensual ease.
  - Pada 3 (Sagittarius rasi → Gemini navamsa): talk, trade, curiosity.
  - Pada 4 (Sagittarius rasi → Cancer navamsa): feeling, nurture, home ties.
- **Professions:** research, medicine/herbs, philosophy, law, demolition, genetics, preaching.
- **Health area:** hips, thighs, sciatic nerve.
- **Compatibility:** same-yoni partner star: Ardra. Avoid/check: vedha with Ashlesha; yoni enemy (Deer): Anuradha, Jyeshtha. Same nadi (Adi) with the partner's star = nadi dosha.
- **Gandanta:** first pada = Scorpio-Sagittarius gandanta.

### 20. Purva Ashadha — 13°20' Sagittarius – 26°40' Sagittarius
- **Keys:** lord Venus; deity Apas; symbol Elephant tusk / fan / winnowing basket; Manushya gana; Monkey yoni (M); Madhya nadi; Rajas; Moksha; Ugra (fierce).
- **Moon here:** invincible mood, persuasive, proud, loves water, will not yield.
- **Padas:**
  - Pada 1 (Sagittarius rasi → Leo navamsa): pride, leadership, visibility.
  - Pada 2 (Sagittarius rasi → Virgo navamsa): analysis, service, craft.
  - Pada 3 (Sagittarius rasi → Libra navamsa) [pushkara]: relating, balance, aesthetics.
  - Pada 4 (Sagittarius rasi → Scorpio navamsa): intensity, secrecy, upheaval.
- **Professions:** law/debate, shipping/water trades, media, motivation, arts, refining.
- **Health area:** thighs, hips, kidneys.
- **Compatibility:** same-yoni partner star: Shravana. Avoid/check: vedha with Pushya; yoni enemy (Sheep): Krittika, Pushya. Same nadi (Madhya) with the partner's star = nadi dosha.

### 21. Uttara Ashadha — 26°40' Sagittarius – 10°00' Capricorn
- **Keys:** lord Sun; deity Vishvadevas; symbol Elephant tusk / planks of bed; Manushya gana; Mongoose yoni (F); Antya nadi; Rajas; Moksha; Dhruva (fixed).
- **Moon here:** lasting victory, principled, responsible, late bloomer, leader by merit.
- **Padas:**
  - Pada 1 (Sagittarius rasi → Sagittarius navamsa) [vargottama, pushkara]: principle, teaching, aim.
  - Pada 2 (Capricorn rasi → Capricorn navamsa) [vargottama]: duty, structure, ambition.
  - Pada 3 (Capricorn rasi → Aquarius navamsa): ideas, networks, detachment.
  - Pada 4 (Capricorn rasi → Pisces navamsa) [pushkara]: imagination, surrender, compassion.
- **Professions:** government, law, military, science, estate management, pioneering work.
- **Health area:** thighs, knees, skin, bones.
- **Compatibility:** same-yoni partner star: . Avoid/check: vedha with Punarvasu; yoni enemy (Serpent): Rohini, Mrigashira. Same nadi (Antya) with the partner's star = nadi dosha.
- **Abhijit:** pada 4 (6°40'–10°00' Capricorn) belongs to Abhijit in 28-star schemes.

### 22. Shravana — 10°00' Capricorn – 23°20' Capricorn
- **Keys:** lord Moon; deity Vishnu; symbol Ear / three footprints; Deva gana; Monkey yoni (F); Antya nadi; Rajas; Artha; Chara (movable).
- **Moon here:** listens and learns, organised, well-travelled, teacher, careful with reputation.
- **Padas:**
  - Pada 1 (Capricorn rasi → Aries navamsa): initiative, haste, pioneering push.
  - Pada 2 (Capricorn rasi → Taurus navamsa) [pushkara]: steadiness, resources, sensual ease.
  - Pada 3 (Capricorn rasi → Gemini navamsa): talk, trade, curiosity.
  - Pada 4 (Capricorn rasi → Cancer navamsa): feeling, nurture, home ties.
- **Professions:** teaching, media/audio, counselling, travel, religion, telecom, languages.
- **Health area:** ears, knees, lymph, skin.
- **Compatibility:** same-yoni partner star: Purva Ashadha. Avoid/check: vedha with Ardra; yoni enemy (Sheep): Krittika, Pushya. Same nadi (Antya) with the partner's star = nadi dosha.
- **Abhijit:** the first 0°53'20" of Shravana (10°00'–10°53'20" Capricorn) belongs to Abhijit in 28-star schemes.

### 23. Dhanishta — 23°20' Capricorn – 6°40' Aquarius
- **Keys:** lord Mars; deity Eight Vasus; symbol Drum / flute; Rakshasa gana; Lion yoni (F); Madhya nadi; Tamas; Dharma; Chara (movable).
- **Moon here:** wealth and rhythm, ambitious, generous, argumentative, marital friction noted.
- **Padas:**
  - Pada 1 (Capricorn rasi → Leo navamsa): pride, leadership, visibility.
  - Pada 2 (Capricorn rasi → Virgo navamsa): analysis, service, craft.
  - Pada 3 (Aquarius rasi → Libra navamsa): relating, balance, aesthetics.
  - Pada 4 (Aquarius rasi → Scorpio navamsa): intensity, secrecy, upheaval.
- **Professions:** music, real estate, sport, military, surgery, engineering, finance.
- **Health area:** knees, ankles, back, limbs.
- **Compatibility:** same-yoni partner star: Purva Bhadrapada. Avoid/check: vedha with Mrigashira, Chitra; yoni enemy (Elephant): Bharani, Revati. Same nadi (Madhya) with the partner's star = nadi dosha.

### 24. Shatabhisha — 6°40' Aquarius – 20°00' Aquarius
- **Keys:** lord Rahu; deity Varuna; symbol Empty circle / 100 physicians; Rakshasa gana; Horse yoni (F); Adi nadi; Tamas; Dharma; Chara (movable).
- **Moon here:** solitary healer, secretive, truthful, stubborn, scientific; '100 physicians'.
- **Padas:**
  - Pada 1 (Aquarius rasi → Sagittarius navamsa): principle, teaching, aim.
  - Pada 2 (Aquarius rasi → Capricorn navamsa): duty, structure, ambition.
  - Pada 3 (Aquarius rasi → Aquarius navamsa) [vargottama]: ideas, networks, detachment.
  - Pada 4 (Aquarius rasi → Pisces navamsa) [pushkara]: imagination, surrender, compassion.
- **Professions:** medicine, pharma, astronomy/astrology, electricity, IT, aviation, research.
- **Health area:** calves, ankles, circulation, heart rhythm.
- **Compatibility:** same-yoni partner star: Ashwini. Avoid/check: vedha with Hasta; yoni enemy (Buffalo): Hasta, Swati. Same nadi (Adi) with the partner's star = nadi dosha.

### 25. Purva Bhadrapada — 20°00' Aquarius – 3°20' Pisces
- **Keys:** lord Jupiter; deity Aja Ekapada; symbol Front legs of funeral cot / sword; Manushya gana; Lion yoni (M); Adi nadi; Sattva; Artha; Ugra (fierce).
- **Moon here:** fiery idealist, two-faced intensity, ascetic or extreme, eloquent, penance.
- **Padas:**
  - Pada 1 (Aquarius rasi → Aries navamsa): initiative, haste, pioneering push.
  - Pada 2 (Aquarius rasi → Taurus navamsa) [pushkara]: steadiness, resources, sensual ease.
  - Pada 3 (Aquarius rasi → Gemini navamsa): talk, trade, curiosity.
  - Pada 4 (Pisces rasi → Cancer navamsa) [pushkara]: feeling, nurture, home ties.
- **Professions:** occult, mortuary, steel/weapons, radical politics, astrology, finance.
- **Health area:** ankles, feet, sides/ribs, liver.
- **Compatibility:** same-yoni partner star: Dhanishta. Avoid/check: vedha with Uttara Phalguni; yoni enemy (Elephant): Bharani, Revati. Same nadi (Adi) with the partner's star = nadi dosha.

### 26. Uttara Bhadrapada — 3°20' Pisces – 16°40' Pisces
- **Keys:** lord Saturn; deity Ahir Budhnya; symbol Back legs of funeral cot / twins; Manushya gana; Cow yoni (F); Madhya nadi; Tamas; Kama; Dhruva (fixed).
- **Moon here:** deep, calm, controlled anger, wise, charitable, kundalini star, endurance.
- **Padas:**
  - Pada 1 (Pisces rasi → Leo navamsa): pride, leadership, visibility.
  - Pada 2 (Pisces rasi → Virgo navamsa) [pushkara]: analysis, service, craft.
  - Pada 3 (Pisces rasi → Libra navamsa): relating, balance, aesthetics.
  - Pada 4 (Pisces rasi → Scorpio navamsa): intensity, secrecy, upheaval.
- **Professions:** yoga/meditation, charity, counselling, research, import-export, poetry.
- **Health area:** feet, shins, sides of the body.
- **Compatibility:** same-yoni partner star: Uttara Phalguni. Avoid/check: vedha with Purva Phalguni; yoni enemy (Tiger): Chitra, Vishakha. Same nadi (Madhya) with the partner's star = nadi dosha.

### 27. Revati — 16°40' Pisces – 30°00' Pisces
- **Keys:** lord Mercury; deity Pushan; symbol Fish / drum; Deva gana; Elephant yoni (F); Antya nadi; Sattva; Moksha; Mridu (soft).
- **Moon here:** gentle, nourishing, protective of travellers and animals, dreamy, completes cycles.
- **Padas:**
  - Pada 1 (Pisces rasi → Sagittarius navamsa): principle, teaching, aim.
  - Pada 2 (Pisces rasi → Capricorn navamsa): duty, structure, ambition.
  - Pada 3 (Pisces rasi → Aquarius navamsa): ideas, networks, detachment.
  - Pada 4 (Pisces rasi → Pisces navamsa) [vargottama, gandanta]: imagination, surrender, compassion.
- **Professions:** travel, shipping, hospitality, orphan/animal care, arts, time-keeping, clergy.
- **Health area:** feet, toes, abdomen, lymph.
- **Compatibility:** same-yoni partner star: Bharani. Avoid/check: vedha with Magha; yoni enemy (Lion): Dhanishta, Purva Bhadrapada. Same nadi (Antya) with the partner's star = nadi dosha.
- **Gandanta:** last pada = Pisces-Aries gandanta.

## Rules
| Rule | Condition (checkable) | Result | Source |
|---|---|---|---|
| Vimshottari start | Dasha lord at birth = lord of Moon's nakshatra; balance = (1 - fraction of nakshatra traversed) x lord's years | Sets the whole dasha sequence | BPHS ch. 46 (Vimshottari), standard |
| Tara bala | count = ((transit_or_day_star - birth_star) mod 9) + 1; 1 Janma, 2 Sampat, 3 Vipat, 4 Kshema, 5 Pratyari, 6 Sadhaka, 7 Naidhana/Vadha, 8 Mitra, 9 Parama Mitra | 3, 5, 7 unfavourable; 2, 4, 6, 8, 9 favourable; 1 mixed | Muhurta tradition (see transits.md) |
| Gandanta | Moon or Lagna in the last pada of a water sign or first pada of a fire sign | Birth dosha needing care/shanti | BPHS ch. 92-94 (read this session) |
| Nadi dosha | Bride and groom stars share the same nadi (Adi/Madhya/Antya) | 0 of 8 points; classic exceptions: same rasi different star, same star different pada | Ashtakoota practice |
| Vedha (star obstruction) | The two birth stars form a vedha pair (table computed above) | Avoid for marriage | Dashakoota practice |
| Gana | Deva-Deva, Manushya-Manushya best; Deva-Rakshasa / Manushya-Rakshasa poor | 0-6 points | Ashtakoota practice |
| Janma-nakshatra transit | A slow malefic (Saturn, Rahu, Ketu, Mars) transiting the birth star, or the 10th and 19th from it (same lord) | Health/mind pressure period | Phaladeepika ch. 26 vv.26-29 (read this session) |

## Reliability notes
- **Classical / computed:** spans, padas and navamsa signs (pure arithmetic); Vimshottari lords; gandanta and Abhukta Mula (BPHS ch. 92-94, read this session); gana, yoni, nadi tables (standard Ashtakoota tables, taken from the project's own data file - not re-verified against a printed panchanga this session).
- **Traditional but varying between books:** deities and symbols are stable; purushartha (dharma/artha/kama/moksha), guna and 'nature' assignments differ slightly between authors. The values here follow the project data file.
- **Modern manuals, not classical verses:** the personality sketches, profession lists and body-part lists. They are consensus paraphrase of 20th-century nakshatra literature (e.g. the style of Dennis Harness, Prash Trivedi, Bepin Behari) written from working knowledge, not from a page read this session. Brihat Jataka ch. 16 gives the short classical Moon-in-star results; it has been read in the Sanskrit and all 27 are translated in `kb/sources/brihat-jataka/ch01-28.md` - they override the sketches here where they differ.
- **Pada nuance** is generated from the navamsa sign's general flavour, not from a text. Use it as a prompt, not a verdict.
- **Pushkara tags** are computed from the commonly taught rule (two navamsas per sign by element); the rule was not re-read in a source this session.
- **Not sourced:** a classical verse-level description for each pada; classical nakshatra-to-profession lists.
