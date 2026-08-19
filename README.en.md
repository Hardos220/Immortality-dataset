# Who Wants to Live Forever

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22002817.svg)](https://doi.org/10.5281/zenodo.22002817)
[![Licence: CC BY 4.0](https://img.shields.io/badge/Licence-CC%20BY%204.0-blue.svg)](LICENSE)

By **Maksim Elisov** · Telegram channel [@im_mortalist](https://t.me/im_mortalist)

> 🇷🇺 **Эта страница по-английски.** Русская версия — **[README.md](README.md)**

**An open database of public attitudes to life extension, immortality, longevity
and healthy living.** 185 sources, 2404 numeric indicators, measurements for
109 countries and cross-national studies covering up to 183 countries. Attitude
measurements span 1973–2026; demographic series begin in 1751.

The data come with an interactive showcase of 37 original charts, in Russian and
English:

**[open the showcase →](https://hardos220.github.io/Immortality-dataset/)**

`index.html` is self-contained: no external dependencies, works from a local
folder and offline.

---

## Why this exists

Public opinion on life extension has been measured for decades, but the results
are not comparable with one another. The same question, asked in different ways,
yields between 19 % and 77 % agreement in the United States. National surveys use
different thresholds (“live forever”, “live to 100”, “to 120 in good health”),
different answer formats and different assumptions about health. No harmonised
international instrument exists.

This database is an attempt to bring scattered measurements into a single
traceable table, to show where the data are comparable and where they are not,
and to mark the blank spaces on the map. **It is an aggregator, not a primary
source:** every row leads back to its original publication.

### The key finding

“How many people want to live longer” falls **sevenfold** depending on what
exactly is being measured:

| What is measured | Value | Source |
|---|---|---|
| “Living long is a good thing” (value) | 69.7 % | Japan, N = 19,800 |
| “I want to live forever” (desire) | 37.4 % | 25 countries, N = 14,000 |
| Brain transplant into a clone is acceptable (intention) | 30 % | Russia, N = 1,600 |
| Would consider cryonics for myself (admission) | 22 % | Germany, N = 1,000 |
| “I would take rapamycin” (a specific means) | 10 % | Netherlands, N = 178 |
| Healthy lifestyle on five criteria (measured behaviour) | 9.7 % | Russia, 60k households |

The main collapse happens not at the end of the scale but at its beginning:
between the value judgement and “I want to live forever” the share almost halves
at the very first tightening of wording — one that still costs the respondent
nothing.

The cleanest check of this gap is not between people but **within one person**.
In NHANES, physical activity was measured twice in the same 3,370 participants:
**23 %** meet the guideline by questionnaire, **0.3 %** by accelerometer.

The same pattern reproduces **within a single country** — see the Russian ladder
on the “Ladder” tab of the showcase.

---

## What is in the repository

```
├── index.html                 showcase: 37 charts, 10 tabs, works offline
├── CITATION.cff               how to cite (machine-readable, CFF 1.2.0)
├── .zenodo.json               metadata for depositing in Zenodo
├── CHANGELOG.md               version history, line by line
├── LICENSE                    full text of CC BY 4.0
├── NOTICE.md                  licensor’s notice: citation form and scope of rights
├── emblem.jpg                 dataset emblem, also the social-card image
├── .gitignore                 what stays out of the repository
├── data/
│   ├── findings.csv           2404 indicators (international format)
│   ├── findings_ru.csv        the same for Russian Excel (; and comma)
│   ├── sources.csv            185 sources with URLs and tiers
│   ├── sources_ru.csv         the same for Russian Excel
│   ├── coverage.csv           coverage matrix: country × topic
│   ├── coverage.json          the same for the showcase
│   ├── who_healthspan.csv     WHO: life against healthy life, 183 countries
│   ├── codebook.en.md         every field described, and the COMPARABILITY RULES
│   └── codebook.md            the same in Russian
├── docs/
│   ├── limitations.en.md      what these data do not show — IN ENGLISH
│   ├── methodology.en.md      how the data were collected — IN ENGLISH
│   ├── limitations.md         ─┐ the same two documents
│   ├── methodology.md         ─┘ in Russian
│   └── duplicates_review.md   pairs “one value under two names”, awaiting review
└── scripts/
    ├── validate.py            dataset integrity check — runs here
    ├── vocab.py               closed vocabularies: access, genre, unit codes
    ├── build_dataset.py       ─┐
    ├── build_artifact.py       ├ a description of how the set is built: these
    └── archive_version.py     ─┘ run from the working repository, not from here
```

Of the scripts shipped with the dataset, `validate.py` works on its own — it
checks exactly the CSV files you downloaded:

```
python scripts/validate.py
```

The other three describe how the set was produced and need working files that are
not part of it. Run from here, they say so and exit without an error.

**On the language of the documentation.** In English: this README,
`CITATION.cff`, `NOTICE.md`, the Zenodo record,
[`docs/limitations.en.md`](docs/limitations.en.md) — read that one before
publishing anything from these data — and
[`docs/methodology.en.md`](docs/methodology.en.md) and
[`data/codebook.en.md`](data/codebook.en.md). Only the changelog stays in
Russian. Field names, codes and vocabularies are English throughout.

## Formats

Files without a suffix are the **international format**: comma separator, decimal
point, UTF-8 with BOM. They open directly:

```python
import pandas as pd
df = pd.read_csv("data/findings.csv")
```

```r
df <- read.csv("data/findings.csv", encoding = "UTF-8")
```

Files with the `_ru` suffix are for the Russian locale of Excel: `;` separator,
decimal comma.

## Quick start

```python
import pandas as pd

df = pd.read_csv("data/findings.csv")

# how many people say they want to live forever, by country
df[df.indicator == "want_live_forever"][
    ["country_en", "year_start", "value_min", "n_sample", "source_name"]
]

# everything on Russia
df[df.country_iso3 == "RUS"]

# representative sources only
df[df.source_tier == "T1"]
```

---

## Before you use the numbers

Three rules, without which these data are easy to misread. In full — in
[`data/codebook.en.md`](data/codebook.en.md).

1. **Percentages from different rows do not add up and often do not compare.**
   Only indicators sharing the same value of `indicator` are comparable.
   “Do you want to live forever” and “do you want to live to 100” are different
   constructs, not two estimates of one quantity.

2. **Always carry `n_sample`, `year_start` and `source_name` along with the
   figure.** A number without a sample size and a year means nothing.

3. **Watch the `value_type` field.** `range` means the primary source gave a range
   (`value_min`–`value_max`) rather than a point estimate; `lower_bound` means only
   the lower limit is known.

Separately: rows with `source_tier = T3` come from non-probability samples and do
not generalise to a population.

---

## How to cite

```
Elisov, M. (2026). Who Wants to Live Forever: an aggregated database of public
attitudes to life extension, immortality and healthy lifestyle
(version 1.1.1) [Data set]. Zenodo. CC BY 4.0.
https://doi.org/10.5281/zenodo.22002817
```

```bibtex
@dataset{elisov2026immortality,
  author    = {Elisov, Maksim},
  orcid     = {0009-0001-3097-2703},
  title     = {Who Wants to Live Forever: an aggregated database of public
               attitudes to life extension, immortality and healthy lifestyle},
  year      = {2026},
  version   = {1.1.1},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.22002817},
  url       = {https://doi.org/10.5281/zenodo.22002817},
  license   = {CC BY 4.0}
}
```

The DOI `10.5281/zenodo.22002817` is permanent: it always resolves to the latest
version, and that is the one to cite. Each individual version also has its own
DOI, shown on its Zenodo record page.

When citing a specific figure, cite **its primary source** from `sources.csv` as
well — this database aggregates measurements made by others, it does not produce
its own.

## Licence

[CC BY 4.0](LICENSE) — free use, including commercial, with attribution. `LICENSE`
holds the full legal text.

[`NOTICE.md`](NOTICE.md) is the licensor’s notice: the required form of
attribution, the scope of the licence and the disclaimer of warranties. It is
issued under section 3(a) of the licence and forms part of the terms of
distribution; it introduces no additional restrictions.

In short: the licence covers the **collection, systematisation, calculations,
texts and visualisation**. Rights in the primary data belong to their holders —
ВЦИОМ, Левада-Центр, Росстат, Pew Research Center, Ipsos, the UN, the WHO,
Eurostat and the other organisations listed in the source registry.

## Author

**Maksim Elisov** — data collection, analysis, graphics
Telegram channel [@im_mortalist](https://t.me/im_mortalist) ·
[@Hardos220](https://t.me/Hardos220) ·
ORCID [0009-0001-3097-2703](https://orcid.org/0009-0001-3097-2703) ·
maksimelisov2003@gmail.com

Corrections, remarks and pointers to sources I have missed are welcome — open an
issue or write directly.
