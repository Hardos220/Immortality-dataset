# Codebook

A description of the fields and — more importantly — the rules by which these
numbers may and may not be compared with one another.

> 🇷🇺 Русская версия — [`codebook.md`](codebook.md)

## Files

| File | What is inside | Format |
|---|---|---|
| `findings.csv` | 2404 numeric indicators, one row = one statistic | comma, decimal point |
| `findings_ru.csv` | the same | `;`, decimal comma |
| `sources.csv` | 185 sources | comma |
| `sources_ru.csv` | the same | `;` |
| `coverage.csv` | the “country × topic” matrix | comma |

Encoding throughout is UTF-8 with BOM, line ending CRLF.

---

## findings.csv — fields

| Field | Type | Description |
|---|---|---|
| `finding_id` | string | Unique identifier, `F###`. Stable across versions |
| `source_id` | string | Reference to `sources.csv`, `N###` |
| `topic` | code | Thematic block: `D1`–`D5`, `E`, `M` (see below) |
| `topic_label` | string | The block spelled out, in Russian |
| `indicator` | snake_case | **The key field.** Machine name of the indicator. Same name = comparable values |
| `country_raw` | string | As recorded in the source (in Russian) |
| `country_en` | string | English name |
| `country_iso3` | ISO 3166-1 alpha-3 | Country code. Empty for aggregates. **`GBR` covers three different entities** — United Kingdom, England, England and Wales: historical life tables have narrower coverage than the country. Grouping by `country_iso3` mixes them; to tell them apart, use `country_en` |
| `geo_scope` | code | `national` — one country · `multi` — several · `global` — the world · `region` — a union (the EU) · `community` — a non-population sample |
| `year_start` | year | Start of the period of data collection (not of publication). Empty in one row — F238, child mortality “before 1800”: only the upper bound is known, and it is in `year_end` |
| `year_end` | year | End of the period. For a point measurement it equals `year_start` |
| `n_sample` | integer | Sample size. Empty if not published |
| `n_note` | string | Sample size in words, where it is not a number (“60000 households”, for example) |
| `subgroup` | string | Subgroup: `все` (all), `мужчины` (men), `женщины` (women), an age band and so on |
| `value_min` | number | The value, or the lower bound of a range |
| `value_max` | number | The upper bound. For a point estimate it equals `value_min` |
| `value_type` | code | `point` · `range` · `lower_bound` · `upper_bound` |
| `unit` | code | Unit of measurement (see below) |
| `question_short` | string | Short wording of the question or indicator |
| `note` | string | Comment, a warning about comparability, a link to related findings |
| `question_type` | code | WHAT is measured: value, expectation, willingness, intention, behaviour, statistics |
| `technology_type` | code | Which means the indicator refers to |
| `response_type` | code | Answer format: binary, ordinal, continuous, count, index |
| `framing` | code | An additional proviso in the wording of the question |
| `ladder_step` | 0–4 | Rung of the “ladder of commitment”, 0 — outside the ladder |
| `ci_low`, `ci_high` | number | Interval bounds **as the source published them**. Empty if no interval was published. They must not be computed from the sample size: that would be our estimate, not the author’s |
| `sd` | number | Standard deviation. Kept apart from the interval bounds: the `ci_low`/`ci_high` pair never holds a deviation |
| `uncertainty` | code | What the uncertainty is: `ci95` · `ui95` · `sd` · `range` · `iqr`. Empty — the source gives none |
| `is_projection` | 0/1 | The value refers to the future or to a scenario, not to a measurement that took place. **Forecasts must not be mixed with observations in one series** |
| `is_derived` | 0/1 | The value was computed by the compiler, not taken verbatim from the source |
| `verification` | code | **How we know the figure is what it is.** `primary` — independently checked against the primary publication · `corroborated` — checked against the cited publication, or confirmed by two independent secondary accounts · `from_primary` — entered from the primary document during extraction, with no separate check · `secondary` — from a second-hand account, not checked · `pending` — not checked · `failed` — checked and did not match |
| `verified_on` | date | When the check was done. Required for `primary`, `corroborated` and `failed` |

> **On `from_primary`.** Having the primary document and having checked a specific
> figure against it are different things. A row entered while working through an
> article is marked `from_primary`, not `primary`: the primary text was at hand,
> but this particular value was not independently re-checked. Conflating the two
> would overstate the reliability of the database. If you need only re-checked
> values: `df[df.verification.isin(["primary", "corroborated"])]`.

| Field | Type | Description |
|---|---|---|
| `source_name` | string | Organisation and title of the source |
| `source_year` | year | Year the source was published |
| `source_url` | URL | Link to the primary source. Empty for compilations — the reason is stated in the registry’s `notes` |
| `source_doi` | DOI | Digital object identifier of the publication, where there is one |
| `source_tier` | code | `T1` · `T2` · `T3` (see below) |
| `source_access` | code | What exactly we had: `microdata` · `full` · `partial` · `abstract` · `blocked` · `secondary` · `derived` |
| `source_license` | code | Terms of re-use of the primary data. For long life-expectancy series this is not a formality: Our World in Data and STMF may lawfully be republished, the raw Human Mortality Database and IDL may not |
| `source_peer_review` | code | `peer_reviewed` · `preprint` · `conference` · `official` · `grey` · `media`. There are preprints and abstracts in the database, and they must not be presented on a par with articles |

### Thematic blocks (`topic`)

| Code | Topic | Rows |
|---|---|---:|
| `D1` | Desire for immortality, belief in an afterlife, fear of death | 557 |
| `D2` | Desired and expected lifespan; the age at which old age begins | 216 |
| `D3` | Attitudes to life-extension technologies and to fighting ageing | 332 |
| `D4` | Demography and population statistics: life expectancy, healthy life expectancy, the long-lived, limits | 630 |
| `D5` | Healthy living, population health, the wellness economy | 472 |
| `E` | Cryonics, digital immortality, longevity markets | 120 |
| `M` | Sample composition: share of men, share with a degree and the like. These are survey metadata, not a measurement of attitudes — such rows do not enter the coverage matrix | 77 |

### Units (`unit`)

| Code | Meaning | Rows |
|---|---|---:|
| `pct` | per cent | 1599 |
| `years` | years | 463 |
| `scale_score` | mean score on a scale | 91 |
| `count` | a count of objects | 81 |
| `ratio` | a ratio | 48 |
| `persons` | people | 48 |
| `litres` | litres | 22 |
| `years_per_year` | years per year | 11 |
| `pct_change` | change in per cent | 8 |
| `billion_usd` | billion US dollars | 7 |
| `years_per_decade` | years per decade | 6 |
| `rmb` | yuan | 6 |
| `grams_per_day` | grams per day | 6 |
| `trillion_usd` | trillion US dollars | 3 |
| `usd` | US dollars | 2 |
| `per100k` | per 100,000 population | 1 |
| `million_usd` | million US dollars | 1 |
| `index` | an index value | 1 |

### Source tier (`source_tier`)

| Tier | What it means |
|---|---|
| `T1` | A representative sample or official statistics; direct measurement on the subject |
| `T2` | An adjacent subject, a commercial survey, or a limited methodology |
| `T3` | A non-probability sample, industry analysis, reference publications. **Does not generalise to a population** |

### `source_access` — what was at hand

What was at hand when the value was entered. The same field is called `access` in `sources.csv`.

| Code | Meaning | Rows |
|---|---|---:|
| `full` | the primary source was obtained in full | 1819 |
| `partial` | part was obtained: an abstract, an excerpt, some tables | 361 |
| `microdata` | microdata were obtained and the value computed from them | 172 |
| `secondary` | there was no primary source; the value comes from a second-hand account | 51 |
| `derived` | a derived summary assembled within this project | 1 |

## Question typology

Every row is coded on four attributes. The tables below are rebuilt from the data
themselves by `scripts_build/build_codebook_tables.py`, and the row counts in them
are the actual ones. A code absent from a table is absent from the dataset: the
script fails if it meets an undescribed one.

**Coding was done by indicator name, but it does not always agree.** The intent
was that one and the same `indicator` gets one code. In practice this does not
hold everywhere — a value under one name may belong to a different measurement.
Divergences by field: `ladder_step` — 16 names, `question_type` — 12,
`response_type` — 11, `topic` — 9, `technology_type` — 6, `framing` — 6,
`unit` — 2. For instance `want_live_forever` occurs both on rung 1 and on rung 0.
**So filtering by a coding attribute rather than by `indicator` is not
permissible:** the coding describes a row, while comparability is set by
`indicator`.

### `question_type` — what exactly is measured

What kind of quantity the row carries.

| Code | Meaning | Rows |
|---|---|---:|
| `value` | A value, a conviction, a preference. This also covers **self-assessment** of one’s own way of life: that is a statement about oneself, not observed behaviour | 1624 |
| `behavior` | Observed or measured behaviour, not an account of it | 200 |
| `population_stat` | Population statistics: a quantity independent of respondents’ opinions | 200 |
| `belief` | A belief about how the world is arranged: whether an afterlife exists, whether science will defeat ageing | 190 |
| `willingness` | Willingness to do something under stated conditions | 70 |
| `expectation` | A forecast about oneself: how long I shall live, when my health will fail. **Not a desire** | 59 |
| `attitude` | An attitude to the subject — approval, acceptability, justifiability — without any commitment to act | 52 |
| `knowledge` | Awareness: does the respondent know of the subject at all | 6 |
| `intention` | An intention stated as a decision, not as willingness under a condition | 3 |

### `technology_type` — which means it refers to

Which means of life extension is in question.

| Code | Meaning | Rows |
|---|---|---:|
| `none` | The question is not about a technology | 1888 |
| `lifestyle` | Way of life: diet, movement, giving up the harmful | 262 |
| `cryonics` | Cryonics | 90 |
| `cloning` | Cloning of cells, tissues, organs and the body | 57 |
| `digital` | Digital immortality, mind uploading | 51 |
| `medical` | A medical intervention or procedure | 20 |
| `genetic` | Intervention in the genome, gene therapy | 17 |
| `device` | A device or gadget: a wearable sensor, an instrument | 10 |
| `pharmacological` | A drug: rapamycin, metformin, a pill | 6 |
| `augmentation` | Augmentation: an implant, a prosthesis, enhancement | 3 |

### `framing` — the proviso in the wording

What proviso is set in the question itself. Wording decides a great deal: see rule 1 below.

| Code | Meaning | Rows |
|---|---|---:|
| `none` | There is no proviso in the wording | 2272 |
| `population_wide` | The quantity refers to the population as a whole, not to those who answered the question | 100 |
| `financial_cost` | The question names a price or a monetary cost | 13 |
| `health_guaranteed` | The question promises preserved health or youth | 6 |
| `condition` | The question sets another condition — availability, safety, absence of side effects | 4 |
| `consent` | A wording about consent: would allow, would permit | 3 |
| `cognitive_loss` | A condition about loss of memory or of reason | 2 |
| `dissent` | A wording about refusal: would ban, would not permit | 2 |
| `no_health_guarantee` | The question states explicitly that health is not guaranteed | 1 |
| `burden_to_family` | A condition that a long life will burden those close to the respondent | 1 |

### `response_type` — the answer format

How the respondent’s answer is arranged.

| Code | Meaning | Rows |
|---|---|---:|
| `continuous` | A measured quantity, not a choice among options | 993 |
| `binary` | Yes or no | 877 |
| `ordinal` | Ordered gradations without a numeric scale | 270 |
| `categorical` | A choice among listed options, more than two | 112 |
| `count` | A count of objects | 97 |
| `likert` | Agreement on a Likert scale, from “strongly agree” to “strongly disagree” | 28 |
| `index` | The value of a composite index | 21 |
| `probability` | An estimate of the probability of an event | 6 |

## The ladder of commitment (`ladder_step`)

The central construct of the database, put into operational form: the rungs are
ranked **by the price of the commitment** a person takes on.

| Rung | Name | What it means | Indicators |
|---|---|---|---|
| 1 | value | State a position. The price is zero | 187 |
| 2 | willingness | Agree to a specific means, hypothetically | 44 |
| 3 | intention | State a plan of action | 3 |
| 4 | action | Perform an act, including an irreversible one | 52 |
| 0 | outside the ladder | Population statistics and **expectations** | 156 |

### Why expectation is placed outside the ladder

An expectation (“how long will I live”) is **a forecast about the world, not a
commitment**. Someone who expects to reach 90 has bound themselves to nothing;
someone who has signed a cryonics contract has. They cannot go on one scale.

This distinction has a practical consequence. The ageing panels — HRS, SHARE,
ELSA, CHARLS and the Gateway to Global Aging that unites them — measure
**subjective survival probability**, that is, expectation. These are the largest
and best data formally close to the subject of this database, and that is exactly
why they are regularly mistaken for a measurement of the desire to live longer.
They are not that.

### How to use the rungs

```python
import pandas as pd
df = pd.read_csv("data/findings.csv")

# the whole ladder, comparable rungs only
ladder = df[df.ladder_step > 0]

# compare words and deeds within one topic
ladder[ladder.technology_type == "cryonics"].groupby("ladder_step").value_min.describe()
```

### What the coding itself revealed

The coding was meant as a convenience, but produced a finding of its own.

1. **The “intention” rung is nearly empty: 9 indicators of 417.** Between
   hypothetical willingness and a completed act lies a layer the field barely
   measures. This is the largest methodological blank in the database. The only
   full measurement is the meta-analysis by Rhodes and de Bruijn 2013
   (N = 3,899 from 10 studies): of those who intended to take up physical
   activity, **36 % never started**, while the reverse transition is almost
   absent — among those who did not intend to, only **2 %** started. The gap is
   one-sided.
2. **Almost nobody varies the wording.** The proviso “with health preserved”
   occurs in 6 indicators, the opposite proviso in 1. And it is exactly the
   health proviso that reverses the result: without it the share wanting a long
   life falls sharply. The field rests on a distinction it hardly ever tests
   experimentally.
3. **The value layer outweighs everything else put together**: 275 indicators
   against 133 on the “willingness” and “action” rungs combined. The field most
   readily measures what costs the respondent nothing.
4. **“Action” outweighs “willingness” in volume — 75 indicators against 58 — and
   is better traceable: T1 stands on 57 of 75 against 31 of 58.** But almost all
   of that measured behaviour is in the area of healthy living (67 indicators):
   official statistics, cohort observation, meta-analyses. Irreversible action in
   the proper sense — a signed cryonics contract — rests, for the whole database,
   on **one** indicator, and that one comes from a community survey rather than a
   provider’s count. The lowest edge of the ladder is held up by the weakest data
   in the whole set.

   For cryonics, however, the ladder assembles in full and shows a collapse of
   four orders of magnitude within a single topic: 47 % have heard of cryonics,
   about 20 % are willing in principle, 6 % intend to, 5 % have signed a contract
   within the LessWrong community — and of the order of 0.00006 % of the world
   population by providers’ counts. The gap is created not by the last rung but by
   the move from willingness to intention and on to the irreversible step.

## Comparability rules

This is the principal section of the codebook. Ignoring these rules will give you
formally correct but meaningless conclusions.

### 1. Only the same `indicator` may be compared

Rows sharing an `indicator` measure the same thing and are comparable across
countries and years. Rows with different `indicator` values are **different
constructs**, even when they sound alike.

Example: `want_live_forever` and `want_live_to_100` are not two estimates of one
quantity. In the United States the first gives 19–33 %, the second 29–77 %. This
is not a contradiction in the data but two different thresholds.

### 2. Known non-comparable pairs

| Pair | Why they cannot be compared |
|---|---|
| `zozh_adherence_objective` (9.7 %) vs `zozh_selfreport_always` (53 %) | An objective criterion of five simultaneous conditions vs self-report. The gap is **partly definitional**: a conjunction of five requirements each passed by 60 % mechanically yields ≈7.8 % |
| `sports_participation` Russia (60.3 %) vs `insufficient_physical_activity` world (31.3 %) | Administrative reporting by the Ministry of Sport vs the standardised WHO criterion (150 min/week). Different definitions and different sources |
| `longevity_is_good` Japan (68.8 %) vs `want_live_to_100` Japan (28.2 %) | A general value placed on longevity vs a specific threshold; different samples (all adults vs ages 77–81) |
| `want_live_to_100` United States 2016 (77 %) vs 2025 (29 %) | Different pollsters and scales: a direct binary question vs a distribution of desired age. The difference is instrumental, not a trend |

### 3. Ranges and bounds

Always check `value_type`:

- `point` — a point estimate, `value_min` = `value_max`;
- `range` — the primary source gave a range; use both bounds, and when computing,
  take the midpoint and state the uncertainty;
- `lower_bound` — only the lower bound is known (`value_max` is empty);
- `upper_bound` — only the upper.

### 4. Confidence intervals are not everywhere

`ci_low`, `ci_high` and `sd` are filled in **only where the source published the
interval itself** — that is 26 rows of 2 404. The `uncertainty` field says what
was published: `ci95`, `ui95`, `iqr`, `sd` or `range`. Carry such bounds along
with the value and **do not recompute them**: for complex samples they account for
the design, whereas a formula based on sample size does not.

For the remaining rows there is no interval in the data. If you need one, compute
it from `n_sample`: ±1.96·√(p(1−p)/n) — and bear in mind that for quota-based
online panels this is a lower bound: the real error exceeds the computed one by
the design effect.

### 5. Overlap with the earlier phase of the project

Some sources overlap with an earlier corpus; `sources.csv` marks this in the
`overlap_phase1` field. In quantitative synthesis, count such indicators once.

### 6. A skew in the sample of countries

Russia and the United States account for 56.9 % of all national indicators — more
than half, not “almost half”. This is a property of the availability of sources,
not of the subject. Check any statement of the form “in the world people think
such-and-such” against this skew — see `coverage.csv` and the “Coverage map” tab
of the showcase.

---

## who_healthspan.csv — life against healthy life

A reference table for **183 countries**, exported directly from the WHO Global
Health Observatory. It is kept apart from `findings.csv` deliberately: it is
machine statistics for every country at once, and poured into the main dataset it
would swamp the survey data the database exists for.

| Field | Description |
|---|---|
| `country_iso3` | Country code |
| `country_en` | Name |
| `year_hale`, `hale_years` | Year and value of healthy life expectancy |
| `year_le`, `life_expectancy_years` | Year and value of overall life expectancy |
| `gap_years` | The gap: how many years a person lives in poor health |
| `gap_share_pct` | The same gap as a share of the whole life |

### What is visible at once

The median gap worldwide is **9.3 years**, with a spread from **6.5** to **12.5**.
But the distribution is arranged unexpectedly: **the gap is largest in rich
countries** (Australia — 12.5 years, the United States — 12.46) and smallest in
poor ones (Somalia — 6.5).

As a share of life it varies far less: the spread across 183 countries runs from
**10.9 %** to **16.3 %**, and for 169 countries of 183 it lies between 12 and
16 %. In other words, rich countries **do not compress the period of illness;
they stretch both life and illness proportionally.** This independently confirms
the GBD 2023 conclusion about a widening gap (see source N194 in the registry).

⚠ A caveat on comparability: the WHO puts the gap for the United States at
12.5 years, GBD 2023 at 14. The divergence is methodological, not an error.
Estimates from the two systems must not be mixed in one series.

## sources.csv — fields

| Field | What it means |
|---|---|
| `source_id` | Source number, `N###`. Numbers are not reused |
| `block` | The thematic block the source was assigned to on collection: A — international surveys, B — Russia, C — demography, D — healthy living and health, E — cryonics and digital immortality. **One block per source**; its indicators may sit under any `topic` |
| `type` | Genre: `academic_article`, `poll_national`, `official_stats`, `database`, `meta_analysis` and others |
| `organization_authors` | Who conducted it: organisation or authors |
| `year` | Year of publication, or a range |
| `title` | Title of the work |
| `coverage` | Coverage: country, number of countries, description of the sample |
| `N` | Sample size. For official statistics, a description of coverage stands in place of a number |
| `method` | How the data were collected |
| `fieldwork` | Dates of the field stage |
| `url`, `doi` | Address of the primary source and its DOI, where there is one |
| `access` | What was at hand during extraction: `full`, `partial`, `abstract`, `secondary`, `microdata`, `derived`, `blocked` |
| `license` | Licence of the primary data. **Empty for 168 sources of 185** — not established; republishing such data is in question |
| `peer_review` | `peer_reviewed`, `preprint`, `official`, `grey`, `media`, `conference` |
| `retrieved` | Date of retrieval. **Empty for 178 of 185** |
| `overlap_phase1` | Overlap with the project’s earlier corpus: in quantitative synthesis count such indicators once |
| `tier` | Traceability T1–T3, see above |
| `survey_mode` | Mode of the survey: `online`, `phone`, `f2f`, `mixed`, `cohort`, `register`, `device`, `review` |
| `extraction` | Depth of extraction: `full`, `partial`, `none` |
| `no_data_reason` | Why a source carries no indicators: `reference`, `infrastructure`, `unverified`, `blocked`, `covered_elsewhere`, `pending` |
| `notes` | Free-text remark |

---

## coverage.csv — fields

| Field | Description |
|---|---|
| `country_iso3` | Country code |
| `country_en` | Name |
| `total` | Total indicators for the country |
| `D1`…`E` | Number of indicators in each thematic block |

Only rows with `geo_scope = national` are counted. Indicators from cross-national
studies do not enter the matrix — otherwise coverage would look fuller than it is.
A country with no indicators in the six topics does not enter the matrix at all.

---

## Reproducibility

All published CSV files are assembled from the project’s working files by:

```bash
python scripts/build_dataset.py
```

The script normalises countries to ISO codes, parses value ranges and periods,
attaches source names and links, and recomputes the coverage matrix.
