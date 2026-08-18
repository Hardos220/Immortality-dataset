# -*- coding: utf-8 -*-
"""
Проверка целостности публикуемого датасета.

Запускать перед каждым релизом:
    python scripts/validate.py

Ненулевой код возврата = найдены ошибки.

Закрытые словари берутся из scripts/vocab.py — он кладётся сюда сборкой,
чтобы список допустимых кодов существовал в проекте в одном экземпляре.
"""
import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[0]
DATA = ROOT / "data"
sys.path.insert(0, str(HERE))
import vocab  # noqa: E402

errors, warnings = [], []


def read(name, delimiter=","):
    with (DATA / name).open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh, delimiter=delimiter))


def num(s):
    s = str(s or "").strip().replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


findings = read("findings.csv")
sources = read("sources.csv")
coverage = read("coverage.csv")
src_ids = {s["source_id"] for s in sources}

# 1. уникальность идентификаторов
for name, rows, key in (("findings", findings, "finding_id"), ("sources", sources, "source_id")):
    dup = [k for k, c in Counter(r[key] for r in rows).items() if c > 1]
    if dup:
        errors.append(f"{name}: повторяющиеся {key}: {dup}")

# 2. ссылочная целостность
orphans = sorted({r["finding_id"] for r in findings if r["source_id"] not in src_ids})
if orphans:
    errors.append(f"findings без источника в sources.csv: {orphans}")

# 3. числовые поля действительно числовые
NUM = re.compile(r"^-?\d+(\.\d+)?$")
for r in findings:
    for f in ("value_min", "value_max"):
        v = r[f]
        if v and not NUM.match(v):
            errors.append(f"{r['finding_id']}: {f} не число: {v!r}")
    if r["n_sample"] and not r["n_sample"].isdigit():
        errors.append(f"{r['finding_id']}: n_sample не целое: {r['n_sample']!r}")

# 4. согласованность value_type
for r in findings:
    t, lo, hi = r["value_type"], r["value_min"], r["value_max"]
    if t == "point" and lo != hi:
        errors.append(f"{r['finding_id']}: value_type=point, но {lo} != {hi}")
    if t == "range" and (not lo or not hi):
        errors.append(f"{r['finding_id']}: value_type=range, но границы неполны")
    if t == "range" and lo and hi and float(lo) > float(hi):
        errors.append(f"{r['finding_id']}: value_min > value_max")
    if t == "lower_bound" and hi:
        warnings.append(f"{r['finding_id']}: lower_bound, но задан value_max")

# 5. годы в разумных пределах и по порядку
for r in findings:
    ys, ye = r["year_start"], r["year_end"]
    for y in (ys, ye):
        # верхняя граница отодвинута до 2300: в базе есть датированные
        # долгосрочные прогнозы — ООН считает на 300 лет вперёд (N292),
        # оценка паритета мёртвых и живых профилей приходится на XXII век (N156)
        if y and not (1700 <= int(y) <= 2300):
            errors.append(f"{r['finding_id']}: год вне диапазона: {y}")
    if ys and ye and int(ys) > int(ye):
        errors.append(f"{r['finding_id']}: year_start > year_end")

# 6. коды из закрытых списков
for r in findings:
    if r["geo_scope"] not in vocab.SCOPES:
        errors.append(f"{r['finding_id']}: неизвестный geo_scope: {r['geo_scope']}")
    if r["source_tier"] not in vocab.TIERS:
        errors.append(f"{r['finding_id']}: неизвестный tier: {r['source_tier']}")
    if r["unit"] not in vocab.UNITS:
        errors.append(f"{r['finding_id']}: неизвестная единица: {r['unit']}")
    if r["topic"] not in vocab.TOPIC_CODES:
        errors.append(f"{r['finding_id']}: неизвестная тема: {r['topic']}")

# 7. ISO-код там, где охват национальный
for r in findings:
    if r["geo_scope"] == "national" and not re.fullmatch(r"[A-Z]{3}", r["country_iso3"] or ""):
        errors.append(f"{r['finding_id']}: национальный охват без ISO3: {r['country_iso3']!r}")

# 8. величины в границах правдоподобия
# Проверка ловит съехавшую колонку и опечатку, а не спорную методику.
# До её появления в базе жила строка «ожидаемая продолжительность жизни
# России за 2024 год = 21,2 года» — доля ожирения, попавшая в соседний ряд.
for r in findings:
    if r["indicator"] in vocab.RANGE_EXEMPT:
        continue
    if any(mark in r["indicator"] for mark in vocab.DELTA_MARKERS):
        continue
    for rule_unit, needle, lo, hi, what in vocab.SANE_RANGES:
        if r["unit"] != rule_unit:
            continue
        if needle and needle not in r["indicator"]:
            continue
        for f in ("value_min", "value_max"):
            v = num(r[f])
            if v is not None and not (lo <= v <= hi):
                errors.append(f"{r['finding_id']}: {what} вне границ {lo}–{hi}: {v}")
        break

# 8б. разрывы внутри одного ряда
# Соседние по времени точки одного показателя не прыгают на десятки единиц.
series = defaultdict(list)
for r in findings:
    if not r["year_start"].isdigit():
        continue
    v = num(r["value_min"])
    if v is None:
        continue
    series[(r["source_id"], r["indicator"], r["country_iso3"], r["subgroup"],
            r["unit"])].append((int(r["year_start"]), v, r["finding_id"]))
for key, points in series.items():
    limit = vocab.SERIES_JUMP.get(key[4])
    if not limit or len(points) < 2:
        continue
    max_jump, max_gap = limit
    points.sort()
    for (y1, v1, f1), (y2, v2, f2) in zip(points, points[1:]):
        if y2 - y1 <= max_gap and abs(v2 - v1) > max_jump:
            errors.append(
                f"{f2}: разрыв в ряду {key[1]} ({key[2] or '—'}): "
                f"{y1} = {v1}, {y2} = {v2}")

# 9. матрица покрытия сходится с findings
recount = Counter()
for r in findings:
    if r["geo_scope"] == "national" and r["country_iso3"]:
        recount[(r["country_iso3"], r["topic"])] += 1
for c in coverage:
    for t in vocab.GRID_TOPICS:
        want, got = recount.get((c["country_iso3"], t), 0), int(c[t])
        if want != got:
            errors.append(f"coverage {c['country_iso3']}/{t}: в файле {got}, по данным {want}")
    total = sum(int(c[t]) for t in vocab.GRID_TOPICS)
    if total != int(c["total"]):
        errors.append(f"coverage {c['country_iso3']}: total {c['total']} != сумме {total}")

# 9б. разделитель внутри значения рвёт строку на лишние колонки
raw = (DATA / "sources.csv").read_text(encoding="utf-8-sig").splitlines()
if raw:
    ncol = len(next(csv.reader([raw[0]])))
    for i, line in enumerate(raw[1:], start=2):
        if line.strip() and len(next(csv.reader([line]))) != ncol:
            errors.append(f"sources.csv строка {i}: колонок не {ncol}")

# 9в. закрытые словари реестра
for s in sources:
    if s.get("extraction", "") not in vocab.EXTRACTION:
        errors.append(f"{s['source_id']}: неизвестная степень разбора: {s.get('extraction')}")
    if s.get("access", "") not in vocab.ACCESS:
        errors.append(f"{s['source_id']}: неизвестный код доступа: {s.get('access')!r}")
    if s.get("type", "") not in vocab.TYPE:
        errors.append(f"{s['source_id']}: неизвестный жанр источника: {s.get('type')!r}")
    if s.get("survey_mode", "") not in vocab.SURVEY_MODE:
        errors.append(f"{s['source_id']}: неизвестный режим опроса: {s.get('survey_mode')!r}")
    if s.get("license", "") not in vocab.LICENSE:
        errors.append(f"{s['source_id']}: неизвестная лицензия: {s.get('license')!r}")
    if s.get("peer_review", "") not in vocab.PEER_REVIEW:
        errors.append(f"{s['source_id']}: неизвестный статус рецензирования: {s.get('peer_review')!r}")
    if s.get("no_data_reason", "") not in vocab.NO_DATA_REASON:
        errors.append(f"{s['source_id']}: неизвестная причина отсутствия данных: "
                      f"{s.get('no_data_reason')!r}")

# 9е. неопределённость величины
for r in findings:
    unc = r.get("uncertainty", "")
    if unc not in vocab.UNCERTAINTY:
        errors.append(f"{r['finding_id']}: неизвестный тип неопределённости: {unc!r}")
    lo, hi, sd = num(r.get("ci_low")), num(r.get("ci_high")), num(r.get("sd"))
    for name, v in (("ci_low", r.get("ci_low")), ("ci_high", r.get("ci_high")),
                    ("sd", r.get("sd"))):
        if v and num(v) is None:
            errors.append(f"{r['finding_id']}: {name} не число: {v!r}")
    if lo is not None and hi is not None and lo > hi:
        errors.append(f"{r['finding_id']}: ci_low {lo} больше ci_high {hi}")
    # значение обязано лежать внутри собственного доверительного интервала
    val = num(r.get("value_min"))
    if unc in ("ci95", "ui95") and val is not None:
        if lo is not None and val < lo:
            errors.append(f"{r['finding_id']}: значение {val} ниже нижней границы {lo}")
        if hi is not None and val > hi:
            errors.append(f"{r['finding_id']}: значение {val} выше верхней границы {hi}")
    if (lo is not None or hi is not None) and not unc:
        errors.append(f"{r['finding_id']}: границы заданы, а тип неопределённости пуст")
    if sd is not None and unc != "sd":
        errors.append(f"{r['finding_id']}: задано sd, но тип неопределённости {unc!r}")

# 9е-2. состояние проверки величины
for r in findings:
    v = r.get("verification", "")
    if v not in vocab.VERIFICATION:
        errors.append(f"{r['finding_id']}: неизвестное состояние проверки: {v!r}")
    if v in vocab.VERIFICATION_DATED and not r.get("verified_on"):
        errors.append(f"{r['finding_id']}: заявлена проверка «{v}», но дата не указана")

# 9ж-2. ключ показателя должен различать строки
# Две строки с одним источником, индикатором, страной, годом, подгруппой
# и единицей неразличимы: их нельзя ни сопоставить, ни обновить поодиночке.
seen_keys = {}
for r in findings:
    k = (r["source_id"], r["indicator"], r["country_raw"], r["year_start"],
         r["subgroup"], r["unit"])
    if k in seen_keys:
        errors.append(f"{r['finding_id']} и {seen_keys[k]}: одинаковый ключ "
                      f"{r['source_id']}/{r['indicator']}/{r['country_raw']}/"
                      f"{r['year_start']}/{r['subgroup']}")
    seen_keys[k] = r["finding_id"]

# 9е2. одно измерение под двумя именами показателя.
#
# Ключ повтора включает имя показателя, поэтому одна и та же величина,
# заведённая дважды под разными именами, для него — две разные строки.
# Так 15.08.2026 нашлись F174 и F2493: прогноз объёма мировой экономики
# здорового образа жизни на 2029 год, 9,8 триллиона долларов, один
# источник N062, но имена wellness_economy_proj и wellness_economy_size.
# Совпадение источника, года, страны, подгруппы, значения и единицы при
# разных именах — почти всегда дубль, и его надо разбирать руками.
by_value = defaultdict(list)
for r in findings:
    v = (r.get("value") or "").strip()
    if not v:
        continue
    by_value[(r["source_id"], r["country_raw"], r.get("year_start", ""),
              r.get("subgroup", ""), v, r.get("unit", ""))].append(r)
for k, rows in by_value.items():
    names = {r["indicator"] for r in rows}
    if len(rows) > 1 and len(names) > 1:
        errors.append(
            "%s: одна величина под разными именами показателя (%s), "
            "источник %s, %s год, значение %s"
            % (" и ".join(r["finding_id"] for r in rows),
               ", ".join(sorted(names)), k[0], k[2], k[4]))

# 9ж. признак прогноза согласован с годом — проверка ОДНОСТОРОННЯЯ.
#
# Год позже текущего обязан нести признак прогноза: наблюдения из будущего
# не бывает. Обратное неверно, и прежняя двусторонняя проверка на этом
# ошибалась. Прогноз — это будущее относительно ИСТОЧНИКА, а не относительно
# сегодня: средний вариант World Population Prospects 2024 даёт для Японии
# 85,15 года на 2026 год, и этот год уже наступил, но величина осталась
# модельной оценкой. Требовать снять признак значило бы выдать прогноз
# за замер. Поэтому величина за прошедший год может быть и тем, и другим,
# а различает их только разбор источника.
for r in findings:
    ys = r.get("year_start", "")
    if not ys.isdigit():
        continue
    if int(ys) > 2026 and r.get("is_projection", "") != "1":
        errors.append(f"{r['finding_id']}: год {ys} ещё не наступил, "
                      f"но is_projection не выставлен")

# 9г. «n/a» в поле ссылки — не адрес: витрина делала из него битую ссылку
for s in sources:
    if (s.get("url") or "").strip() == "n/a":
        errors.append(f"{s['source_id']}: url = 'n/a'; для отсутствующей ссылки поле пустое")

# 9д. заявленная степень разбора и наличие строк не должны спорить
have = Counter(r["source_id"] for r in findings)
for s in sources:
    ex, n = s.get("extraction", ""), have.get(s["source_id"], 0)
    if ex in ("full", "partial") and n == 0:
        errors.append(f"{s['source_id']}: степень разбора «{ex}», но показателей нет")
    if ex == "none" and n:
        errors.append(f"{s['source_id']}: степень разбора «none», но показателей {n}")

# 10. ссылки на источники
no_url = [s["source_id"] for s in sources if not (s.get("url") or "").strip()]
if no_url:
    warnings.append(f"источники без URL ({len(no_url)}): {', '.join(no_url)}")
secondary = [s["source_id"] for s in sources if s["access"] == "secondary"]
if secondary:
    warnings.append(f"источники из пересказов, требуют проверки ({len(secondary)}): "
                    f"{', '.join(secondary)}")
no_data = sorted(s["source_id"] for s in sources if not have.get(s["source_id"]))
if no_data:
    warnings.append(f"источники в реестре без единого показателя ({len(no_data)}): "
                    f"{', '.join(no_data)}")
# отсутствие данных должно быть объяснено, а не выглядеть недоделкой
unexplained = sorted(s["source_id"] for s in sources
                     if not have.get(s["source_id"]) and not s.get("no_data_reason"))
if unexplained:
    errors.append(f"источники без показателей и без указанной причины "
                  f"({len(unexplained)}): {', '.join(unexplained)}")
# лицензия источника нужна, чтобы знать, что можно перепубликовать
no_lic = [s["source_id"] for s in sources if not s.get("license")]
if no_lic:
    warnings.append(f"лицензия источника не определена ({len(no_lic)}) — "
                    f"пока не заполнена, перепубликация таких данных под вопросом")

# 11. имя показателя как словарь, а не как подпись строки
# Страна и год должны жить в своих полях: пока они впечатаны в indicator,
# правило сопоставимости «сравнивать строки с одним indicator» ничего
# не разрешает сравнивать.
inds = {r["indicator"] for r in findings}
with_year = {i for i in inds if re.search(r"_(1[789]|2[0-3])\d{2}\b", i)}
if with_year:
    warnings.append(f"имена показателей с годом внутри ({len(with_year)}): "
                    f"{', '.join(sorted(with_year)[:8])} …")
by_ind = defaultdict(set)
for r in findings:
    by_ind[r["indicator"]].add(r["country_iso3"] or r["country_raw"])
multi = sum(1 for v in by_ind.values() if len(v) > 1)
warnings.append(f"сопоставимость: показателей, встречающихся более чем "
                f"у одной страны — {multi} из {len(inds)}")

# 12. счётчики в документах совпадают с данными
# Раздел закрывает главную причину расхождений: README и CITATION.cff
# обновлялись руками и отставали от базы на несколько версий.
n_src, n_fin, n_cov = len(sources), len(findings), len(coverage)


def check_doc(path, label, patterns):
    if not path.exists():
        warnings.append(f"{label}: файл не найден")
        return
    text = path.read_text(encoding="utf-8")
    for pattern, expected, what in patterns:
        found = re.findall(pattern, text)
        if not found:
            warnings.append(f"{label}: не найдено место «{what}»")
            continue
        for got in found:
            if int(str(got).replace(" ", "")) != expected:
                errors.append(f"{label}: {what} = {got}, в данных {expected}")


# Согласование числительных меняет окончание («показателя» против
# «показателей»), поэтому шаблоны заканчиваются на \w*, а не на точное слово.
check_doc(ROOT / "README.md", "README.md", [
    (r"(\d[\d ]*) источник\w* , ?".replace(" , ?", ", ") + r"\d[\d ]* числов\w* показател\w*",
     n_src, "число источников"),
    (r"\d[\d ]* источник\w*, (\d[\d ]*) числов\w* показател\w*",
     n_fin, "число показателей"),
    (r"замеры по (\d+) стран\w*", n_cov, "число стран"),
    (r"sources\.csv\s+(\d+) источник", n_src, "строка sources.csv"),
    (r"findings\.csv\s+(\d+) показател", n_fin, "строка findings.csv"),
])
check_doc(ROOT / "CITATION.cff", "CITATION.cff", [
    (r"из (\d[\d ]*) источник\w*", n_src, "число источников"),
    (r"и (\d[\d ]*) числов\w* показател\w*", n_fin, "число показателей"),
    (r"замеры по (\d+) стран\w*", n_cov, "число стран"),
])
check_doc(DATA / "codebook.md", "codebook.md", [
    (r"\| `sources\.csv` \| (\d+) источник", n_src, "строка sources.csv"),
])

# версия должна быть одна во всех трёх местах
vers = {}
for path, pattern in ((ROOT / "CITATION.cff", r'^version: "([\d.]+)"'),
                      (ROOT / "README.md", r"\(версия ([\d.]+)\) \[Набор данных\]"),
                      (ROOT / "index.html", r"Версия\s+([\d.]+)\s*·")):
    if path.exists():
        m = re.search(pattern, path.read_text(encoding="utf-8"), re.M)
        if m:
            vers[path.name] = m.group(1)
if len(set(vers.values())) > 1:
    errors.append(f"версия расходится между файлами: {vers}")

# витрина в наборе должна быть той же, что счётчики набора
idx = ROOT / "index.html"
if idx.exists():
    t = idx.read_text(encoding="utf-8")
    m = re.search(r"const N_FIN = (\d+);", t)
    if m and int(m.group(1)) != n_fin:
        errors.append(f"index.html: N_FIN = {m.group(1)}, показателей в данных {n_fin}")
    m = re.search(r"const SRC = \[(.*?)\n\];", t, re.S)
    if m:
        n = len([x for x in m.group(1).split("\n") if x.strip().startswith("[")])
        # N999 — собственные расчёты составителя. В реестре набора запись
        # нужна, в списке источников на витрине ей не место: сослаться
        # на составителя как на источник данных нельзя. Расхождение ровно
        # на эту одну запись — норма, любое другое — ошибка сборки.
        hidden = sum(1 for s in sources if s["source_id"] == "N999")
        if n != n_src - hidden:
            errors.append(f"index.html: в реестре SRC {n} строк, "
                          f"источников {n_src} минус скрытых {hidden}")

# ── отчёт ──
print(f"findings : {len(findings)}")
print(f"sources  : {len(sources)}")
print(f"coverage : {len(coverage)} стран")
print(f"тиры     : {dict(Counter(r['source_tier'] for r in findings))}")
print(f"типы значений: {dict(Counter(r['value_type'] for r in findings))}")
print(f"доступ   : {dict(Counter(s['access'] for s in sources))}")
print(f"версия   : {vers}")
ver_counts = Counter(r.get("verification", "") for r in findings)
print("проверка величин:")
for code in ("primary", "corroborated", "from_primary", "secondary", "pending", "failed"):
    if ver_counts.get(code):
        print(f"   {code:14} {ver_counts[code]:5}  — {vocab.VERIFICATION[code]}")
unchecked = ver_counts.get("secondary", 0) + ver_counts.get("pending", 0)
print(f"   {'ИТОГО ждут сверки':14} {unchecked:5}")

if warnings:
    print(f"\nПредупреждения ({len(warnings)}):")
    for w in warnings:
        print("  ! " + w)

if errors:
    print(f"\nОШИБКИ ({len(errors)}):")
    for e in errors:
        print("  x " + e)
    sys.exit(1)

print("\n[ok] Все проверки пройдены.")
