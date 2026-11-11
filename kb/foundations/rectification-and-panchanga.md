# Birth time rectification and Panchanga

Sources read in this session:
- **[AS-BTR]** AstroSage KP tutorial on rectification by ruling planets: https://sites.google.com/a/astrosage.com/kpastrology/kp-learning-home/tutorial/birth-time-rectification
- **[SJ]** Sushmajee notes on birth-time correction (D-charts, Gulika, Pranapada): https://mail.sushmajee.com/astrology/misc/birth-time-1.htm
- **[PVR]** P.V.R. Narasimha Rao, *Vedic Astrology: An Integrated Approach*: https://www.vedicastrologer.org/articles/vedic_astro_textbook.pdf
- **[BPHS45]** https://www.barbarapijan.com/bpa/Amsha/avasta_BPHS_ch45_Avasta.htm (ghati-based Shayanadi avastha, relevant to time sensitivity)
- **[MEM]** standard panchanga arithmetic and BPHS shanti chapters (Santhanam vol. 2, approx. ch. 85–96) — from recall; chapter numbers to be verified.
- Project finding (internal): after-the-fact fitting of events to sub-period lords scored 248 candidate charts within half a point of each other.

---

# Part 1 — Birth time rectification

## 1.1 First principle: what actually changes with birth time

| Quantity | Rate of change | Time to change state |
|---|---|---|
| Lagna degree | ~1° per 4 min (varies 2–6 min with sign and latitude) | sign: ~2 h (1–3 h) |
| D9 lagna (3°20') | | ~13 min |
| D10 lagna (3°) | | ~12 min |
| D12 lagna (2°30') | | ~10 min |
| D3 lagna (10°) | | ~40 min |
| D7 lagna (4°17') | | ~17 min |
| D60 lagna (0°30') | | ~2 min |
| KP ascendant sub (40'–2°13') | | ~2.5–9 min |
| Moon longitude | ~0.55' per minute of time | nakshatra pada: ~6 h |
| Vimshottari dates | shift = 0.55'/800' × MD years per minute ≈ **0.25 days × (MD years) per minute of birth time** | Venus MD: 5 days/min, ~10 months per hour; Sun MD: 1.5 days/min |
| Other planets' signs/houses from Moon | effectively fixed within a day | — |

Consequence: inside a window of an hour or two, **dasha dates barely move** (weeks to months) and planets do not change sign. What changes is the lagna and therefore every house lordship and the divisional lagnas. Any rectification method therefore discriminates only through lagna-dependent facts. A method that scores candidates by "did a suitable sub-period lord run at the event date" is reading the same dasha table for every candidate and then choosing a house rationale afterwards — which is why it cannot separate candidates.

## 1.2 Why post-hoc event fitting fails (the project result, explained)

- With MD/AD/PD there are three lords per date; each planet owns 1–2 houses, occupies one, aspects 1–3, has a star lord with its own houses, and has natural significations. Some link to any given event almost always exists. Adding a deeper level (PD, sookshma) multiplies the free choices instead of adding evidence.
- The scorer is not blind: the event is known first and the justification is found second.
- So flat scores across 248 candidates are the expected outcome. It shows the scoring rule has no discriminating power; it does not show that all candidates are equally good.

Minimum conditions for an event-based method to carry information:
1. **Rules fixed before looking at candidates**: one event type → one predeclared set of houses/karakas (e.g. marriage = 7th lord, planets in 7th, Venus, D9 lagna lord; nothing else).
2. **Lagna-dependent tests only** (house lordship of the running MD/AD lords from each candidate lagna; divisional lagna placement), since that is all that differs.
3. **A chance baseline**: compute the same score for control candidates (other lagnas, shuffled event dates). A candidate is preferred only if it beats the control distribution by a clear margin.
4. **MD and AD level only** for scoring; PD and below only as a tie-break and labelled as such.
5. **Count misses**: events that the rule says should not have happened in that period count against the candidate.
6. Prefer **many dated, hard events** (marriage, births of children, death of parents, major relocation, career start/breaks, accidents/surgeries). Fewer than about 6–8 events cannot separate adjacent lagnas reliably.

## 1.3 Methods, with what each can and cannot resolve

| Method | What it uses | Can resolve | Cannot resolve / weakness | Discriminating? |
|---|---|---|---|---|
| **Lagna sign from life pattern** | Whole-sign lordships vs broad life facts (profession type, marriage timing band, number of siblings/children, parents' fortunes, body/temperament) | Choice among the 2–3 lagna signs inside a wide window (hours) | Nothing finer than ~2 h; descriptive traits are vague and prone to flattering fits | Moderate, if facts are hard and rules fixed first |
| **Event-based dasha matching (pre-registered)** | MD/AD lords' house lordship from each candidate lagna at dated events, per 1.2 | Lagna sign; sometimes D9/D10 lagna (10–15 min) if many events | Minute-level time; anything when rules are chosen after the fact | Yes only under 1.2 conditions; otherwise **no** (project result) |
| **Divisional-chart checks** — D3 siblings, D7 children, D9 spouse/marriage, D10 career, D12 parents [SJ; MEM] | Does the varga lagna and its lord fit the known facts (number/sex of siblings, elder vs younger, parents' death order, spouse traits)? | In principle 10–40 min bands (the span of one varga lagna) | Each varga lagna gives only ~9–12 options per sign, and the trait rules are loose; sibling-count rules disagree between texts; modern small families give little data | Weak to moderate; best as a veto (reject candidates that flatly contradict a fact) |
| **Physical traits / temperament from lagna, navamsa lagna** | Build, complexion, face, manner | Sometimes separates two adjacent lagna signs | Highly subjective; ethnicity and age dominate | Weak |
| **Tattwa shodhana** [MEM] | Five-element cycle running from sunrise; birth of a male/female is supposed to fall in particular tattvas/antar-tattvas | Claims minute-level correction | Durations, starting element and gender rule differ between authors; allowed slots recur every few minutes, so some allowed slot is always near any time | **No** — it selects the nearest "allowed" slot, it does not test anything |
| **Kunda (lagna × 81)** [MEM] | Kunda = (lagna longitude × 81) mod 360; its nakshatra should be the janma nakshatra or its 10th/19th (trinal) star | Claims ~40-second precision | A valid slot ~40 s wide recurs every ~1°29' of lagna ≈ 6 minutes (3 of 27 stars qualify → 1/9 of all times pass). Any stated time is within ~3 min of a "valid" one | **No** on its own; it is a rounding convention |
| **Navamsa–dwadasamsa / Moon-lagna relations** [MEM] | Rules such as: lagna (or navamsa lagna) should be in trine/7th to the Moon's sign or navamsa, or to the sign of the Moon's dispositor | 10–15 min bands | Several alternative relations are allowed, so most windows contain a pass | Weak |
| **Gulika/Mandi check** [SJ] | Gulika (from weekday portions of day/night) should be in 1, 2, 5, 7, 9 or 10 from lagna or Moon for a human birth | Lagna sign level | Six of twelve positions pass from either of two references | Very weak |
| **Pranapada** [SJ] | Pranapada lagna (moves one sign per ~6 min: time since sunrise in vighatis / 15, added to the Sun shifted to the movable sign in trine) must be in a trine (some: also 7th) from lagna | Claims ±1–1.5 min | A valid configuration recurs every ~6–8 minutes | **No** on its own (same structure as Kunda) |
| **Pre-natal epoch** (Western; Sepharial/Bailey) | Moon at conception = ascendant/descendant at birth and vice versa, ~273 days before | Claims minute-level | Assumes an unverifiable conception moment; multiple solutions (regular/irregular epochs) | **No** independent validation |
| **KP ruling planets** [AS-BTR] | Asc sign/star/sub lords must come from the ruling planets at the moment of judgement; cusp sub lords must agree with known events | Outputs a time to the minute | RP step depends on when the astrologer looks; 5–7 of 9 planets qualify. Only the cuspal yes/no checks use facts about the native | RP step: no. Cuspal fact checks: moderate, as vetoes |
| **Documentary evidence** | Hospital record, birth certificate time, family diary, tithi/weekday/"before sunrise" recollection, festival association | Often ±5–15 min, or at least the half-day | Rounded times; clock vs LMT/IST/war-time confusion | **Yes — strongest**; always exhaust this first |

Summary of what is actually discriminating: (1) documents and recollections that pin the clock time or the lagna-independent facts; (2) lagna-sign selection against hard life facts with pre-fixed rules; (3) divisional lagna and KP cuspal checks used as vetoes against known facts; (4) pre-registered MD/AD-lordship scoring with a control baseline. Tattwa, Kunda, Pranapada, Gulika, pre-natal epoch and ruling planets are **fine-tuning conventions**: they will always return an answer near the input time and cannot tell a right time from a wrong one.

## 1.4 Recommended procedure for the engine

1. Record the source and stated precision of the birth time (hospital record / parent memory / rounded hour / unknown).
2. Compute the **stability report** for the stated time ± uncertainty: does the lagna sign change? D9/D10/D7/D12 lagna? Moon nakshatra or pada? Any planet sign? Vimshottari MD/AD dates shift by how many days? Anything that does not change across the window can be read with confidence; say so explicitly.
3. If the lagna sign is stable across the window: do not rectify; read the D1 and qualify varga and KP statements by their stability.
4. If two or three lagna signs are possible: list hard dated events and structural facts, apply pre-declared rules to each candidate, report scores **with the control baseline**, and state the margin. If the margin is small, report "undetermined between X and Y" and give both readings.
5. Use Kunda/Pranapada/tattwa only if the user asks for a conventional "rectified" time, and label the result "conventional adjustment, not evidence".

## 1.5 When only the date, or a time window, is known

- **Date only (24 h unknown)**: lagna unknown; all house-based statements are unavailable.
  - Reliable: signs of Sun, Mars, Mercury, Jupiter, Venus, Saturn, Rahu/Ketu (check for an ingress that day); tithi/yoga ranges; weekday (mind the sunrise rule).
  - Moon: moves ~12–15° in the day. Compute Moon at 00:00 and 24:00 local; report whether the sign and nakshatra are fixed or which two are possible. The Moon changes nakshatra on most days and sign on about 2 days in 5.
  - Use **Chandra lagna** (Moon sign as lagna) and **Surya lagna** charts for house judgement; give Vimshottari as a range (start-of-day and end-of-day balances; the uncertainty is up to one nakshatra fraction ≈ the daily Moon motion / 13°20' of the first MD).
  - Do not cast a "noon chart" lagna as if real; a noon chart is only a midpoint for planetary positions.
  - Narrowing questions that cost nothing: day or night? before or after sunrise? morning/afternoon/evening? any remembered tithi, festival, or "lamps were being lit"? Each halves the window. Then apply 1.4 step 4 over the remaining candidate lagnas ([SJ]: once Moon sign and its drekkana are known, about 4 lagnas remain to test).
- **Time window (e.g. "between 9 and 10")**: run the stability report across the window; if the lagna changes inside it, test both; quote D9/D10-dependent results only if stable.
- Always report which statements are window-independent.

---

# Part 2 — Panchanga

All longitudes sidereal (Lahiri) unless noted; tithi, karana and yoga depend only on Sun/Moon differences or sums — tithi and karana are ayanamsa-independent, yoga is not.

## 2.1 Vedic day, Vara and Hora
- The day (vara) runs **sunrise to next sunrise**. A birth at 03:00 on civil Tuesday belongs to Monday. This is the commonest source of weekday/"date" confusion in family records.
- Weekday lords: Sunday Sun, Monday Moon, Tuesday Mars, Wednesday Mercury, Thursday Jupiter, Friday Venus, Saturday Saturn.
- **Hora**: 24 horas from sunrise to next sunrise. Hora 1 lord = day lord; each following lord is the next in the order Sun → Venus → Mercury → Moon → Saturn → Jupiter → Mars → Sun… (descending orbital period: Saturn, Jupiter, Mars, Sun, Venus, Mercury, Moon, cyclic). Two conventions for length: 12 equal parts of the day + 12 equal parts of the night (unequal "planetary hours"), or 24 equal 60-minute horas from sunrise. Shadbala's Hora bala follows the same choice — keep one.
- Birth interpretation: day lord and hora lord colour the temperament; a strong day lord supports vitality. Minor factor.

## 2.2 Tithi
`elong = (Moon − Sun) mod 360`; `tithi_index = floor(elong / 12)` (0–29); number 1–30.
- 1–15 = Shukla Pratipada … Purnima (15); 16–30 = Krishna Pratipada … Amavasya (30).
- Fraction elapsed = `(elong mod 12) / 12`.
- Names: Pratipada, Dwitiya, Tritiya, Chaturthi, Panchami, Shashthi, Saptami, Ashtami, Navami, Dashami, Ekadashi, Dwadashi, Trayodashi, Chaturdashi, Purnima/Amavasya.
- Groups: Nanda (1, 6, 11), Bhadra (2, 7, 12), Jaya (3, 8, 13), Rikta (4, 9, 14), Purna (5, 10, 15/30). Rikta tithis are the difficult ones.
- Tithi lords (Kalaprakashika scheme, as in [PVR]; verify): 1 & 9 Sun, 2 & 10 Moon, 3 & 11 Mars, 4 & 12 Mercury, 5 & 13 Jupiter, 6 & 14 Venus, 7 & 15 Saturn, 8 Rahu, Amavasya Rahu.
- Interpretation: Shukla paksha birth favours outward growth and a strong Moon; Krishna paksha an inward temperament; the Moon's paksha bala is the measurable form of this.

## 2.3 Nakshatra
`nak_index = floor(Moon / 13°20')` (0–26, Ashwini = 0); pada = `floor((Moon mod 13°20') / 3°20') + 1`. The birth star fixes Vimshottari, Yogini, name syllable, gana/yoni/nadi for matching.

## 2.4 Yoga (nitya yoga)
`yoga_index = floor(((Sun + Moon) mod 360) / 13°20')` (0–26).
Order: 1 Vishkambha, 2 Priti, 3 Ayushman, 4 Saubhagya, 5 Shobhana, 6 Atiganda, 7 Sukarma, 8 Dhriti, 9 Shula, 10 Ganda, 11 Vriddhi, 12 Dhruva, 13 Vyaghata, 14 Harshana, 15 Vajra, 16 Siddhi, 17 Vyatipata, 18 Variyan, 19 Parigha, 20 Shiva, 21 Siddha, 22 Sadhya, 23 Shubha, 24 Shukla, 25 Brahma, 26 Indra, 27 Vaidhriti.
Inauspicious: Vishkambha, Atiganda, Shula, Ganda, Vyaghata, Vajra, Vyatipata, Parigha, Vaidhriti (Vyatipata and Vaidhriti the worst).

## 2.5 Karana (half-tithi)
`k = floor(elong / 6)` (0–59).
- k = 0 → Kimstughna (fixed)
- k = 1…56 → movable karanas cycling: `["Bava","Balava","Kaulava","Taitila","Gara","Vanija","Vishti"][(k − 1) mod 7]`
- k = 57 → Shakuni, 58 → Chatushpada, 59 → Naga (fixed)

**Vishti (Bhadra)** occurs at k = 7, 14, 21, 28, 35, 42, 49, 56, i.e. 2nd half of Shukla 4, 1st half of Shukla 8, 2nd half of Shukla 11, 1st half of Purnima, 2nd half of Krishna 3, 1st half of Krishna 7, 2nd half of Krishna 10, 1st half of Krishna 14. Vishti and the four fixed karanas are inauspicious for beginnings; a Vishti birth is traditionally said to give a harsh, combative, enterprising temperament.

## 2.6 Inauspicious births and shanti [MEM — BPHS vol. 2 closing chapters, approx. ch. 85–96 in Santhanam's numbering; verify numbers]

| Condition | Definition | Traditional indication | Remedy named in the tradition |
|---|---|---|---|
| Amavasya (Darsha) | tithi 30 (Sun–Moon conjunction within 12°) | Hardship to parents, poverty unless strong benefics | Darsha shanti: worship of Sun and Moon, homa, gifts |
| Krishna Chaturdashi | tithi 29, split into 6 equal parts | 1st part auspicious; 2nd danger to father; 3rd to mother; 4th to maternal uncle; 5th to the family line; 6th loss of wealth / to self | Rudra/Shiva worship and homa |
| Vishti (Bhadra) karana; bad yogas (Vyatipata, Vaidhriti, Parigha, Vajra, Vyaghata, Ganda, Atiganda, Shula) | 2.4, 2.5 | Obstacles, health | Shanti for the yoga/karana deity; charity |
| Same nakshatra as a parent or sibling (Eka-nakshatra) | janma nakshatra equal | Harm to one of the two | Nakshatra shanti |
| Sankranti birth | Sun changing sign that day (close to ingress) | Poverty, hardship | Sankranti shanti, Navagraha homa |
| Eclipse birth | Solar/lunar eclipse in progress | Illness, danger | Worship of the eclipse nakshatra lord, Sun/Moon and Rahu |
| Gandanta | Tithi gandanta (junctions of Purna and Nanda tithis: 15→1, 5→6, 10→11), nakshatra gandanta (Revati→Ashwini, Ashlesha→Magha, Jyeshtha→Mula), lagna gandanta (Pisces→Aries, Cancer→Leo, Scorpio→Sagittarius) — traditionally 2 ghatis (nakshatra), 1 ghati (tithi), half ghati (lagna) each side | Danger to child or parents depending on which side | Gandanta shanti (go-dana, homa) after the prescribed interval |
| Abhukta Mula | End of Jyeshtha / start of Mula (narrow band; 1–2 ghatis each side, authors differ) | Father should not see the child for a period; by Mula pada: 1st father, 2nd mother, 3rd wealth, 4th auspicious | Mula shanti on the return of the nakshatra (27th day) |
| Jyeshtha / Ashlesha end | Final padas | Elder sibling / mother-in-law indications | Nakshatra shanti |
| Trikha (daughter after three sons, or son after three daughters) | birth order | Family difficulty | Shanti |
| Unusual delivery | — | — | Shanti |

Engine stance: compute and report these as traditional flags with their definitions; present the indications as "the tradition says", do not predict harm to named relatives from them alone, and mention that shanti is a ritual prescription.

## 2.7 Using festivals and panchanga to confirm a birth date

Families often remember the panchanga better than the civil date ("born on Ugadi", "two days after Diwali", "on Ekadashi in Shravana", "Tuesday before sunrise").
- A lunar month + paksha + tithi (+ weekday) identifies a civil date within a given year almost uniquely; adding the nakshatra makes it certain. Compute the tithi/nakshatra/weekday for the claimed civil date and compare; a mismatch of one day usually means the before-sunrise or midnight convention.
- **Month naming**: Amanta (month ends at new moon) in Karnataka, Maharashtra, Gujarat, Andhra, Telangana, Goa; Purnimanta (ends at full moon) in North India. Krishna-paksha dates carry different month names in the two systems (e.g. Diwali amavasya = Ashwina amanta = Kartika purnimanta).
- **Solar calendars** (Tamil, Malayalam, Bengali, Odia, Assamese, Punjabi) name months by the Sun's sidereal sign; a "date in Chithirai/Medam" gives the Sun's sign and approximate degree directly.
- Festival ↔ panchanga keys: Ugadi/Gudi Padwa = Chaitra Shukla 1; Rama Navami = Chaitra Shukla 9; Akshaya Tritiya = Vaishakha Shukla 3; Guru Purnima = Ashadha Purnima; Nag Panchami = Shravana Shukla 5; Raksha Bandhan = Shravana Purnima; Janmashtami = Shravana Krishna 8 (amanta) at midnight; Ganesh Chaturthi = Bhadrapada Shukla 4; Navaratri = Ashwina Shukla 1–9; Dasara = Ashwina Shukla 10; Diwali (Lakshmi puja) = Ashwina Amavasya (amanta); Kartika Purnima; Makara Sankranti = Sun enters sidereal Capricorn (≈14–15 Jan); Maha Shivaratri = Magha Krishna 14 (amanta); Holi = Phalguna Purnima.
- The festival day is decided by which tithi prevails at a specified time (sunrise for most; midday for Rama Navami and Ganesh Chaturthi; pradosha/evening for Diwali; midnight for Janmashtami and Shivaratri; moonrise for Karva Chauth/Sankashti), so the festival can fall a day before or after the "tithi at sunrise" date, and regional almanacs sometimes differ by a day. Adhika (intercalary) months shift everything by a month in some years.
- Old records may use Shaka or Vikrama Samvat years and samvatsara names (60-year Jupiter cycle; North and South Indian samvatsara counts differ).

---

## Implementation notes

- One sunrise function for the whole engine (decide: centre vs upper limb, refraction, altitude). Panchanga weekday, hora, tribhaga, ghati, Gulika and Pranapada all depend on it.
- Time standards: convert historic Indian civil times correctly (IST from 1906 but uneven adoption; Bombay Time until 1955; Calcutta Time until 1948; war-time +1 h in 1942–45; LMT before standardisation). An unhandled 30–60 minute offset is larger than anything rectification techniques claim to fix.
- Tithi/karana/yoga at birth instant are simple; "tithi of the day" for festival matching needs the tithi at local sunrise and tithi end-times (root-find on elong crossing multiples of 12°).
- Gandanta/Abhukta Mula bands: implement in arc (degrees) and in time (ghatis of the Moon's actual motion); authors use both.
- Krishna Chaturdashi sixths: divide the actual tithi duration (start to end times), not a fixed 24 h.
- Stability report (1.4 step 2): evaluate chart at window start, end and every sign/varga/nakshatra/sub boundary crossing inside the window; output a table of intervals.
- Rectification scorer: implement the control baseline (same scoring on shuffled event dates and on all 12 lagnas) and report z-score or rank, never the raw score alone.
- Date-only mode: skip all lagna-dependent modules; emit Moon range, Chandra-lagna reading, dasha ranges.
- Kunda helper (if offered): `kunda = (lagna_lon * 81) % 360`; allowed if nakshatra(kunda) ∈ {janma, janma+9, janma+18 mod 27}; return nearest earlier and later passing times and say plainly that a passing time exists within ~3 minutes of any input.

## Reliability notes

- Rates and time-to-change figures in 1.1 are arithmetic (Moon ≈ 13.2°/day; one nakshatra = 800'); they are averages — the lagna speed varies by sign and latitude.
- The Kunda periodicity argument (1/9 of times pass, recurring ~every 6 minutes) is arithmetic from the method's own definition; the method definition itself is from recall and has variants (some compare the Kunda sign with the Moon sign instead).
- Tattwa shodhana: I could not find, in a source read this session, an agreed table of tattva durations, starting element per weekday, or the male/female rule; versions differ (e.g. 6/12/18/24/30-minute ascending-descending cycle of 90 minutes). No exact table is given here on purpose.
- Gulika and Pranapada rules are as read on [SJ]; that page's weekday table was garbled, so Gulika segment numbers should be taken from BPHS ch. 3 before coding.
- BPHS chapter numbers for the inauspicious-birth shanti chapters and the per-part indications (Krishna Chaturdashi sixths, Mula padas) are from recall; verify against Santhanam vol. 2.
- Tithi-lord scheme and festival timing rules follow common almanac practice; regional almanacs (Drik vs Vakya) can differ by a day.
- No rectification technique in the Jyotisha literature has been validated blind. The project's own test is consistent with that: use documentary evidence first, lagna-level discrimination with controls second, and label everything finer as convention.
