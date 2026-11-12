# Parashara read in the Sanskrit — verse readings and what they changed

Text: Brihat Parashara Hora Shastra, Sanskrit e-text at sanskritdocuments.org (files par7180, par8190, par9197; prepared by volunteers for personal study and research). Read 12 Nov 2026. The translations below are this project's own, made directly from the Sanskrit. Only verse numbers and a few key words are quoted; the text itself is not reproduced here.

How the reading was done: the verses were retrieved line by line from the site and translated here. The retrieval step passes through an automated reader, so a mis-copied syllable is possible; where a reading decides a rule, the key Sanskrit words are given so it can be checked against the file.

## Chapter 75 — the five great-person yogas (vv. 1-2)
- Reading: Mars and the other four (Mercury, Jupiter, Venus, Saturn), when **strong**, in their **own sign or exaltation**, and in a **kendra**, give in order Ruchaka, Bhadra, Hamsa, Malavya, Shasha. Key words: *svabhocca-gata-kendra-sthaiḥ balibhiḥ*.
- Effect on our rule: confirmed. Two points the catalogue lacked: the planet must also be strong (*balibhiḥ*), and the verse names no Moon-based count. The count from the Moon is a later addition (Phaladeepika and after) and is reported separately as "from Moon only".

## Chapter 79 — renunciation (pravrajya) yogas (vv. 1-15)
- v.2-3: four or more planets, strong, in one place give renunciation; the order is that of the strongest - Sun: ascetic (*tapasvī*), Moon: skull-bearer (*kapālī*), Mars: red-robed, Mercury: single-staff, Jupiter: *yati*, Venus: wheel-bearer, Saturn: *nirgranthika*.
- v.4-5: if those planets are combust the person is only a devotee of that order, not initiated; if combust and weak with a strong Sun, the Sun's order.
- v.6: the lord of the Moon's sign, unaspected by other planets, aspecting Saturn - renunciation according to the stronger of the two.
- v.7: the lord of the Moon's sign weak and aspected by Saturn alone - Saturn's order.
- v.8: Moon in Saturn's drekkana AND in a navamsa of Saturn or Mars, aspected by Saturn - Saturn's order. (The catalogue had "drekkana or navamsa of Saturn or Mars"; the verse requires both.)
- v.9-13: planetary war among the renunciation-givers; the defeated one's vow is abandoned; several equal givers mean several orders taken in their dashas.
- v.14: Jupiter in the 9th with the Moon, Jupiter and lagna aspected by Saturn - if a raja yoga is also present, founder of an order.
- v.15: Saturn in the 9th with no planet aspecting it - if a raja yoga is also present, a king who takes initiation.
- Effect: v.7-8 are now coded (`pravrajya_moon_saturn`); v.14-15 confirmed as coded.
- **Citation error found:** the catalogue cited "BPHS 79.6-8" for *Vish yoga* (Moon with Saturn). Those verses are about renunciation. Parashara has no "Vish yoga" here; it is a later, popular label and is now marked unsourced.

## Chapter 83 — curses from a former birth, shown as loss of children
- v.7: Jupiter, lagna lord, 7th lord and 5th lord all weak - childlessness.
- v.8: Sun, Mars, Rahu, Saturn strong in the 5th while the significators of children are weak - childlessness.
- Serpent curse (*sarpa-śāpa*): v.9 Rahu in the 5th aspected by Mars, or in Mars's sign; v.10 5th lord with Rahu AND Saturn in the 5th joined or aspected by the Moon; v.11 Jupiter with Rahu, 5th lord without strength, lagna lord with Mars; v.12 Jupiter with Mars, Rahu in the lagna, 5th lord in a bad house; v.13 Mercury as 5th lord in Mars's navamsa with Mars, lagna with Rahu and Mandi.
- Father's curse (*pitṛ-śāpa*): v.20 Sun in the 5th, debilitated, in Saturn's navamsa, cruel planets on both sides; v.21 Sun as 5th lord in a trine with a malefic, between malefics, aspected by a malefic; v.22 Jupiter in the Sun's sign, 5th lord with the Sun, malefics in the 5th and lagna; v.23 weak lagna lord in the 5th, 5th lord with the Sun, malefics in the 5th and lagna; v.24 lord of the father's house in the 5th or 5th lord in the 10th, malefics in the 5th and lagna; v.25 Mars as lord of the father's house with the 5th lord, malefics in lagna, 5th and father's house; v.26 father's-house lord in a bad house, Jupiter in a malefic's sign, 5th and lagna lords with malefics; v.27 Sun, Mars, Saturn in lagna and 5th, Rahu and Jupiter in the 8th and 12th.
- Effect on our rules - two real corrections:
  1. **Serpent curse:** the engine fired on "5th lord with Rahu" alone. The verse (v.10) also needs Saturn in the 5th joined or aspected by the Moon. Fixed.
  2. **Pitru dosha:** the engine's test (Sun with Rahu, Saturn or Ketu, or an afflicted 9th) fires in 61% of random charts and is **not Parashara's**. His father's-curse combinations are narrow, all tied to the 5th house and to children. The engine now tests those (v.20-23, 27) under the catalogue entry and labels the old test "popular definition, not in Parashara".
- Guardrail: these verses speak of loss of children. In a reading they are stated only as "the classical texts flag difficulty with children", never literally, and never unprompted.

## Chapters 86-87 — birth at new moon and on the dark 14th
- 86.1: for those born at new moon (*darśa*), poverty of the parents; a pacification rite follows.
- 87.1-3: the dark 14th tithi in six parts - first part harmless; then father, mother, maternal uncle, the family line, and wealth or self.
- Effect: confirmed as catalogued. The new-moon verse promises only hardship for the parents.

## Chapter 91 — birth during an eclipse
- 91.1: for those born at the time of a solar or lunar eclipse - illness, hardship, poverty, danger to life; rites follow.
- Effect: **Parashara's condition is an actual eclipse at birth.** The catalogue's "Sun or Moon in the same sign as Rahu or Ketu" is the popular widening and is now labelled so. The engine tests for birth at or near an eclipse.

## Chapter 92 — gandanta
- 92.1: three kinds - of tithi, nakshatra and lagna.
- 92.2: tithi gandanta: four nadis around the junction of a Purna tithi (5, 10, 15) and the Nanda that follows (6, 11, 1).
- 92.3: nakshatra gandanta: four nadis at Revati-Ashwini, Ashlesha-Magha, Jyeshtha-Mula.
- 92.4: lagna gandanta: one ghati at the Pisces-Aries, Cancer-Leo and Scorpio-Sagittarius junctions.
- 92.5: Abhukta Mula: at the Jyeshtha-Mula junction, five and eight ghatis respectively.
- Effect: **the engine's window was far too wide.** It used 3°20' of the Moon either side of the junction; four nadis is about 0°27' either side (0°53' on the loosest reading). Fixed, with Abhukta Mula added. The lagna window (about 3° either side) was already close.

## Summary of this pass
| Checked | Result |
|---|---|
| 14 yoga citations from chapters 75-92 | all re-read in Sanskrit |
| Confirmed as catalogued | 9 |
| Rule corrected | 4 (serpent curse, Pitru dosha, gandanta width, Saturn's renunciation) |
| Citation wrong | 1 (Vish yoga is not in chapter 79) |

## Chapter 80 — the female chart (*strī-jātaka*), vv. 1-52 of 55, read 12 Nov 2026
- v.2-4: results for women are judged as for men; the special points are: her body from the lagna, **childbirth from the 5th**, the husband's fortune from the 7th, widowhood from the 8th; what cannot apply to a woman is said of her husband.
  - Effect: settles a conflict recorded in the children file. Parashara reads a woman's children from the 5th house. The 9th-house method belongs to other schools.
- v.5-7: lagna and Moon in even signs - feminine nature and good qualities, more so with benefic aspect; in odd signs - masculine bearing, and ill-natured if aspected by malefics; mixed gives mixed; the stronger of lagna and Moon decides.
- v.17: 7th house weak, empty and unaspected by benefics - a husband of little worth; a movable sign there - he lives away from home.
- v.18: Sun in the 7th - left by the husband; Mars - early widowhood; Saturn aspected by malefics - marriage very late or not at all.
- v.19: **malefics in the 7th** - widowhood; benefics there - husband lives and she is virtuous; mixed planets - she marries again.
  - **Citation error found:** the marriage file quoted this verse as "benefics in a woman's 8th are protective" and listed it as a conflict with vv.26-33. The verse is about the 7th house (*asta*). There is no conflict: benefics in the 7th are good; vv.26-33 treat every planet in the 8th as unfavourable.
- v.22-25: the husband is described by the **sign on the 7th house or its navamsa**: Mars's - fond of women, quick-tempered; Mercury's - learned, skilled in arts; Jupiter's - all good qualities, self-controlled; Venus's - fortunate, handsome, liked by women; **Saturn's sign or navamsa - old and dull**; the Sun's - very gentle, hard-working; Cancer or its navamsa - attractive, amorous, soft; mixed - by the stronger of sign and navamsa.
  - Effect on a failed project rule: "Saturn with the 7th lord means an older husband" was tested and failed. That was never Parashara's rule. His is: the 7th house falling in Saturn's sign (Capricorn, Aquarius) or Saturn's navamsa. The engine now prints this reading for female charts; it stays low confidence until tested.
- v.26-33: each planet in the 8th of a woman's chart is given a harsh result. Never stated literally in a reading.
- v.34, 38-41: childlessness and loss-of-children combinations (Moon and Venus in the lagna with Saturn and Mars and an afflicted 5th; Sun and Moon in the 8th in own signs; lagna in a sign of Saturn or Mars holding Moon and Venus with malefic aspect; and others). Recorded; not volunteered.
- v.43-46: *Viṣa-kanyā*: birth under Ashlesha, Krittika or Shatabhisha on a Sunday, Saturday or Tuesday on a Bhadra tithi (2nd, 7th, 12th), or a second chart pattern; **cancelled** when the 7th lord or a benefic is in the 7th from the lagna or from the Moon.
- v.47: **Mars in the lagna, 12th, 4th, 7th or 8th, without the aspect or company of a benefic** - the husband's life is harmed. Key words: *lagne vyaye sukhe vāpi saptame cāṣṭame kuje, śubha-dṛg-yoga-hīne*.
  - Effect: confirms the engine exactly - Parashara's Mangal dosha is houses 1, 4, 7, 8, 12 (the 2nd house is a southern addition), and the one cancellation in the verse is a benefic's aspect or conjunction.
- v.48: the same combination in a man's chart harms the wife.
- v.49: when a woman with this combination marries a man who has it, the combination is broken.
  - Effect: the "both partners have it" cancellation is Parashara's own. The engine had it under later claims; it is now classical and belongs in the matching protocol.
- v.52: Mars, Mercury, Jupiter and Venus strong with an even sign rising - learned in many disciplines.
- Not yet read: vv.8-14 (trimsamsa results), 53-55.

## Running total (12 Nov 2026)
| | Count |
|---|---|
| Parashara chapters read in Sanskrit | 75, 79, 80 (most), 83 (part), 86, 87, 91, 92 |
| Rules corrected | 5 (serpent curse, Pitru dosha, gandanta width, Saturn's renunciation, mutual Mangal cancellation) |
| Wrong citations found | 2 (Vish yoga at 79.6-8; "benefics in the 8th" at 80.19) |
| Project rules explained | 1 ("Saturn with 7th lord = older spouse" was never the classical rule) |
| Could not open | par1120.pdf (chapters 11-20: marriage ch. 18, children ch. 16) - site error on that file |
