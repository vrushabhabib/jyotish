# Source policy and audit (set 12 Nov 2026)

## Policy
0. The Sanskrit root text is the source. English renderings, websites and any machine-generated summaries are aids only; where a rule matters it is read in the Sanskrit and the reading is recorded in `sources/`.
1. Only free, openly readable material is used: public-domain texts, works released free by their authors, and websites that anyone can read without payment or login.
2. Nothing locked: no paywalled or licensed databases, no purchased-only books, no scans of in-copyright books uploaded by third parties, no bulk exports that need a licence.
3. If a rule cannot be supported from a free source it is tagged `[UNSOURCED]` or `[MEMORY]` and treated as low confidence. It is not "fixed" by reaching for a locked source.
4. Rules are written in our own words with the verse or page cited. Text is never copied wholesale.
5. Test data comes only from people who gave their details for this project. No third-party database of birth records is used.

## Audit of what the knowledge base cites
| Source | Used for | Status |
|---|---|---|
| Sanskrit root texts (Parashara, Varahamihira, Jaimini, Mantreshwara) | the rules themselves | Public domain (ancient works) |
| P.V.R. Narasimha Rao, "Vedic Astrology: An Integrated Approach" and articles at vedicastrologer.org | Ashtakavarga tables, dashas, vargas, longevity | Free: released by the author on his own site |
| sanskritdocuments.org, Phaladeepika of Mantreshvara: Sanskrit text (phaladIpika.itx) | every Phaladeepika rule in the knowledge base | Free: prepared by volunteers "for personal study and research"; cited and paraphrased only. **Read in the Sanskrit on 12 Nov 2026** (20 of 28 chapters in full, the rest listed in `kb/sources/phaladeepika/README.md`). All numbered citations were confirmed; four were corrected. The website siva.sh, whose machine-made English the citations first came from, is no longer a source for anything |
| saravali.github.io | strength and calculation notes | Free: documentation of an open-source astrology program, licensed CC BY-SA 4.0. It is not a translation of the classical Saravali |
| sanskritdocuments.org, Brihat Parashara Hora Shastra: Sanskrit text of all 97 chapters (par0110 ... par9197) | every Parashara rule in the knowledge base | Free: prepared by volunteers "for personal study and research". Not to be reposted or used commercially - we cite and paraphrase only. **All 97 chapters were read in the Sanskrit on 12 Nov 2026** and recorded verse by verse in `kb/sources/bphs/`; the engine and the rule files were corrected to the text (list in `kb/sources/ANALYSIS.md`) |
| archive.org item "ParasharaHoraSastra" | formerly the BPHS link | **Removed.** Community upload with no licence and no named translator. 14 yoga citations (chapters 75-92) still rest on its English reading and are marked "not yet re-verified"; the Sanskrit for them is free at sanskritdocuments.org |
| enjoylearningsanskrit.com/scriptures/parashara | verse-by-verse BPHS in the life-area files | Free to read online |
| wisdomlib.org, Brihat Jataka (M. D. Neely) | chapter structure only | Free to read with the author's permission; the online pages carry the Sanskrit only, the English is in the paid book and is NOT used |
| Wellcome Collection, Brihat Samhita tr. N. Chidambaram Iyer (1884-85) | not yet used | Public Domain Mark - usable |
| en.wikipedia.org | definitions, cross-checks | Free (CC BY-SA) |
| jagannathhora.com, barbarapijan.com, astrobix.com, onlinejyotish.com and other open websites | modern practice, summaries | Free to read; modern opinion, lower authority than the root texts |
| vedastro.org blog | Raman's worked Shadbala example (numbers only) | Free to read; numbers are facts of a calculation. Raman's book itself is not used |
| sites.google.com/a/astrosage.com/kpastrology | one KP rule | Free to read |
| JPL Horizons (NASA) | validating planet positions | Free, public service |
| Swiss Ephemeris, pyephem, geonamescache, PyJHora (source read, not run) | calculation and cross-checks | Open-source licences |

## Excluded
- Astro-Databank bulk export: needs a licence from its owner. Not requested, not used.
- B.V. Raman's, K.N. Rao's and K.S. Krishnamurti's books: in copyright, no free edition found. Rules attributed to them from secondary pages stay tagged.
- R. Santhanam's and other in-copyright translations of the classics.

## Work this leaves open
- Done 12 Nov 2026: the 14 yoga citations from BPHS chapters 75-92 were re-read in the Sanskrit; see `sources/bphs-verse-readings.md` (4 rules corrected, 1 wrong citation removed).
- Read the rest of Parashara the same way, chapter by chapter, starting with those the life-area files lean on most (marriage ch. 18, children ch. 16, career ch. 21, longevity ch. 43-44, female chart ch. 80).
- Re-read the 41 Phaladeepika citations against the Sanskrit text (the English they rest on is machine-generated).
- Done 12 Nov 2026: Brihat Jataka read in full in the Sanskrit (`kb/sources/brihat-jataka/`); the Nabhasa and Moon yogas are now sourced to its verses.

## What the text itself claims (BPHS 66.10-12, read in the Sanskrit 12 Nov 2026)
Parashara, introducing Ashtakavarga: to settle the length of life and the course of life with certainty "neither Vasishtha nor Brihaspati is able - how much less men, and in the Kali age especially". The science has a general part and a particular part; the particular part is offered to narrow the judgement, not as certainty. The project states its confidence in the same spirit: evidence counts and a logged track record, never a guarantee.

## Added 12 Nov 2026 (evening)
| Source | Used for | Terms |
|---|---|---|
| sanskritdocuments.org `brihajjAtakam.itx` - Brihat Jataka of Varahamihira, Sanskrit | read in full; my translation in `kb/sources/brihat-jataka/` | volunteer e-text "for personal study and research"; the Sanskrit is not stored here |
| sanskritdocuments.org `jAtakapArijAtaH.itx` - Jataka Parijata of Vaidyanatha, Sanskrit | ch. 1-2 and the cited verses; `kb/sources/jataka-parijata/` | same terms; the file is marked "needs proofreading" and has lost pages |

Not available as a clean free Sanskrit text (searched 12 Nov 2026) and therefore not used as sources: **Jaimini's Upadesha Sutras** and **Saravali**. Rules once cited to them through secondary pages keep that tag. Narayana dasha is taught only in modern in-copyright books and is not adopted.

- **Laghu Parashari (Ududaya Pradipa)** - Sanskrit Wikisource, https://sa.wikisource.org/wiki/लघुपाराशरी (free). All 42 verses read 13 Nov 2026; record in `kb/sources/laghu-parashari/README.md`. Not on sanskritdocuments.org.
