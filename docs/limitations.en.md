# Limitations

What these data do not show. This section exists so that you do not draw
conclusions the data will not bear.

> 🇷🇺 Русская версия — [`limitations.md`](limitations.md)

## 1. This is a collection of findings, not a sample of studies

The selection is not systematic: there is no protocol, screening was done by one
person, and the inclusion criteria were refined as the work went on. So **it
cannot be claimed that the database reflects the whole literature on the
subject**, and statements of the form “most studies show…” cannot be made from it.

## 2. A skew towards two countries

Russia and the United States account for more than half of all national
indicators — **532 and 511 of 1835, that is 57 %**. This follows from the
availability of sources, not from the importance of those countries, and as the
database grew the skew widened rather than evened out.

The geography meanwhile expanded to 109 countries, but almost entirely through
cross-national projects: 57 of the 109 countries carry exactly one indicator in
the coverage matrix, and the median across all countries is also one. The
database grew broad as a list, deep only for two countries.

The practical consequence: any statement of the form “people around the world
think such-and-such” must be checked against this skew — does it rest on the
Russian and American figures? The coverage matrix is in `data/coverage.csv` and
on the “Coverage map” tab of the showcase.

## 3. Geographic blanks

Latin America, sub-Saharan Africa, Central Asia and most of the Middle East are
represented either by a single figure from a cross-national study or not at all.
And it is precisely the developing economies that show the highest desire for
longevity — that is, there are fewest data where the signal is strongest.

## 4. Percentages from different rows are often not comparable

This is the principal limitation. Different wordings measure different
constructs: in the United States “do you want to live forever” gives 19–33 %,
“do you want to live to 100” gives 29–77 %. Only indicators sharing the same
`indicator` can properly be compared.

The full list of known non-comparable pairs is in
[`data/codebook.md`](../data/codebook.md).

## 5. The only cross-national measurement publishes the extreme countries only

The Oxford Longevity Project survey of 2024 is the only study that asked the same
question about immortality in 25 countries. Country values are published only for
the five most “for” and the three most “against”.

Because of this, **two testable hypotheses could not be computed**: the overlap
with the other datasets came to 5 and 2 countries instead of the 13 theoretically
possible.

## 6. One tested hypothesis turned out to be false

The supposition that desired lifespan exceeds actual life expectancy by a stable
12–13 years **was not confirmed**: across nine countries the spread ran from
−3.4 to +18.2 years. The agreement for Russia and the United States was a
coincidence.

Instead of a constant, what emerged was a regression of expectations towards a
common notion of a “normal” life: the correlation of actual life expectancy with
the size of the overstatement is r = −0.78 (n = 9).

## 7. The “declaration versus practice” gap is partly definitional

The Rosstat figure of 9.7 % is the simultaneous satisfaction of five conditions.
A conjunction of five requirements, each passed by 60 %, mechanically yields
≈7.8 %. So a substantial part of the “ninefold gap” is created by the arithmetic
of a composite index, not by overstated self-assessment.

The two effects can be separated only through the marginal share of each
criterion, and those are not in the open releases.

The conclusion about the gap is nevertheless robust — it reproduces on indicators
without composite indices: United States 3 : 1, the four McKinsey countries
4.6 : 1, Saudi Arabia 2.5 : 1.

## 8. The last rung of the “ladder” mixes cost with availability

Cryonics is physically available in three countries, costs tens of thousands of
dollars and carries a reputation as a fringe service. The fall at the last step
therefore measures not the price of irreversibility in itself, but that price
multiplied by the absence of a market.

To separate the two, one needs an indicator of an action equally costly but fully
available. There are no such data in the database.

## 9. Tiers are assigned subjectively

`T1`/`T2`/`T3` are one person’s expert judgement, made without a validated
instrument and without computing inter-coder agreement. For a defensible quality
assessment, apply a formal instrument (AXIS, for example) independently.

## 10. Some indicators come from secondary sources

Rows with `source_access = secondary` were obtained from second-hand accounts
rather than from the primary publication. Check them before citing in
peer-reviewed work.

Separately: the annual Rosstat series on healthy lifestyle remain from secondary
sources — the EMISS portal refused the request.

## 11. Russian statistics on the very old are unreliable

The 2021 census cut the size of the 90-and-over group by about 20 %. There is a
scholarly discussion of errors in age recording. Russian figures on the number of
centenarians should be used only with that caveat.

In addition, since March 2025 Rosstat has suspended publication of life
expectancy broken down by region and by sex.

## 12. Forecasts are not of equal standing

The forecast block places side by side official UN demographic projections,
peer-reviewed articles and public statements that went through no review. The
last are marked separately and shown on the chart as an open arrow rather than a
number — because they name no limit at all.

## 13. Confidence intervals are present only where the source published them

`ci_low`, `ci_high` and `sd` are filled in for 26 rows out of 2404 — those where
the source published an interval itself; the `uncertainty` field says what kind.
Carry such bounds along with the value and **do not recompute them**: for complex
samples they account for the design, whereas a formula based on sample size does
not.

For all other rows there is no interval in the data. If you need one, compute it
from `n_sample` — and remember that for quota-based online panels this is a lower
bound: the real error is larger by the design effect.

## 14. Retrospective historical values are approximate

Indicators such as “world life expectancy in 1900 — 32 years” or “Japan around
1925 — roughly 44 years” rest on demographers’ reconstructions, not on censuses
of the time. Their precision is illusory; the values serve for order of magnitude,
not for exact comparison.

## 15. A skew in time: almost everything is from the last 15 years

**1956 indicators of the 2403 with a known year (81.4 %) belong to 2010 or later.**
Earlier points exist almost exclusively in the demographic block, where long
official series are available.

How this affects conclusions: these data support statements about **change over
time** only pointwise. There are long comparable series in the database, but they
concern belief rather than the desire to live longer: the General Social Survey
gives belief in an afterlife for 1973–2024; ISSP and British Social Attitudes give
pairs of points 27 years apart. On the desire for radical life extension itself
there are almost no repeated measurements with one instrument: the single
cross-national measurement (Oxford 2024) is a one-off, and the Russian points were
collected by different organisations with different wordings. Comparisons of the
“before and after COVID” or “generational shift over twenty years” kind are not
supported by this database on this subject.

What to do about it: look not for new countries but for **repeated measurements
with one instrument**. A single question with fixed wording, repeated three times
over ten years, is worth more than ten new countries in one cross-section.

## 16. The “intention” rung is practically empty

After the indicators were coded by ladder rung (see `data/codebook.md`), it turned
out that the “intention” rung holds **9 indicators of 417**. The value layer is
represented by 275 indicators, willingness by 58, action by 75.

How this affects conclusions: the gap between word and deed appears in the
database as a **jump**, not as a descent down steps. The intermediate link — the
person who has resolved to act but has not yet acted — is barely measured. On the
available data one therefore cannot say where exactly people are lost: at the
move from willingness to intention, or from intention to the act.

What to do about it: this is the cheapest possible improvement to the field. It is
enough to add to an existing questionnaire one item of the form “have you done
anything specific in the past year” next to the question about willingness.

## 17. Almost nobody varies the wording of the question

The condition “with health preserved” is coded on **6 indicators**, the opposite
condition on 1. And it is exactly this proviso that reverses the result: the share
wanting a long life depends sharply on whether the question promises health.

How this affects conclusions: the field rests on a distinction it almost never
tests experimentally. Comparing two surveys with different provisos, one cannot
separate the country effect from the wording effect.

What to do about it: a randomised split test of wordings within a single sample.
The `framing` and `question_type` fields were added to the dataset for exactly
that analysis, once such data exist.
