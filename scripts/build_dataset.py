# -*- coding: utf-8 -*-
"""
Сборка публикуемого датасета из рабочих файлов проекта.

Вход  : data/datasets/findings.csv, data/sources/sources_new.csv  (рабочий формат:
        разделитель «;», десятичная запятая, страны по-русски)
Выход : immortality-attitudes-data/data/*.csv  (два формата) + coverage.csv + coverage.json

Что делает нормализация:
  • страна → ISO 3166-1 alpha-3 + английское имя + признак охвата (national/multi/global);
  • значение → value_min / value_max / value_type (point | range | lower_bound),
    потому что в исходнике встречаются «20-24», «>50», «150-190»;
  • год → year_start / year_end (в исходнике бывает «2021-2023», «до 1800»);
  • к каждой находке подтягиваются название источника, ссылка и тир.

Запуск: python scripts_build/build_dataset.py
"""
import csv
import json
import re
import shutil
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_FINDINGS = ROOT / "data" / "datasets" / "findings.csv"
SRC_SOURCES = ROOT / "data" / "sources" / "sources_new.csv"
REPO = ROOT / "immortality-attitudes-data"
OUT = REPO / "data"

# Копия скрипта едет вместе с публикуемым набором как описание процедуры.
# Рабочих файлов в наборе нет и быть не может — он собирается из них,
# а не наоборот. Без этой проверки запуск из набора падал с трассировкой
# и выглядел как сломанный скрипт.
if not SRC_FINDINGS.exists():
    print(
        "Этот скрипт собирает публикуемый набор из рабочих файлов проекта.\n"
        "Не найден %s.\n\n"
        "В опубликованном наборе рабочих файлов нет — скрипт включён в него\n"
        "как описание того, как получены CSV. Проверить сам набор можно\n"
        "командой:  python scripts/validate.py" % SRC_FINDINGS)
    raise SystemExit(0)

OUT.mkdir(parents=True, exist_ok=True)

# ─────────────────────────── справочник стран ───────────────────────────
# scope: national — одна страна; multi — несколько; global — мир целиком;
#        region — наднациональное объединение; community — не популяционная выборка
COUNTRY = {
    "Австралия":          ("AUS", "Australia", "national"),
    "Аргентина":          ("ARG", "Argentina", "national"),
    "Греция":             ("GRC", "Greece", "national"),
    "Канада":             ("CAN", "Canada", "national"),
    "Коста-Рика":         ("CRI", "Costa Rica", "national"),
    "Тайвань":            ("TWN", "Taiwan", "national"),
    "Гонконг":            ("HKG", "Hong Kong SAR", "national"),
    "Израиль":            ("ISR", "Israel", "national"),
    "Кения":              ("KEN", "Kenya", "national"),
    # страны проекта World Values Survey
    "Албания":            ("ALB", "Albania", "national"),
    "Алжир":              ("DZA", "Algeria", "national"),
    "Андорра":            ("AND", "Andorra", "national"),
    "Армения":            ("ARM", "Armenia", "national"),
    "Азербайджан":        ("AZE", "Azerbaijan", "national"),
    "Беларусь":           ("BLR", "Belarus", "national"),
    "Боливия":            ("BOL", "Bolivia", "national"),
    "Босния и Герцеговина": ("BIH", "Bosnia and Herzegovina", "national"),
    "Венесуэла":          ("VEN", "Venezuela", "national"),
    "Гватемала":          ("GTM", "Guatemala", "national"),
    "Грузия":             ("GEO", "Georgia", "national"),
    "Доминиканская Республика": ("DOM", "Dominican Republic", "national"),
    "Зимбабве":           ("ZWE", "Zimbabwe", "national"),
    "Иордания":           ("JOR", "Jordan", "national"),
    "Ирак":               ("IRQ", "Iraq", "national"),
    "Казахстан":          ("KAZ", "Kazakhstan", "national"),
    "Киргизия":           ("KGZ", "Kyrgyzstan", "national"),
    "Колумбия":           ("COL", "Colombia", "national"),
    "Ливан":              ("LBN", "Lebanon", "national"),
    "Ливия":              ("LBY", "Libya", "national"),
    "Литва":              ("LTU", "Lithuania", "national"),
    "Макао":              ("MAC", "Macao SAR", "national"),
    "Малайзия":           ("MYS", "Malaysia", "national"),
    "Мальдивы":           ("MDV", "Maldives", "national"),
    "Марокко":            ("MAR", "Morocco", "national"),
    "Молдавия":           ("MDA", "Moldova", "national"),
    "Монголия":           ("MNG", "Mongolia", "national"),
    "Мьянма":             ("MMR", "Myanmar", "national"),
    "Никарагуа":          ("NIC", "Nicaragua", "national"),
    "Перу":               ("PER", "Peru", "national"),
    "Пуэрто-Рико":        ("PRI", "Puerto Rico", "national"),
    "Румыния":            ("ROU", "Romania", "national"),
    "Сальвадор":          ("SLV", "El Salvador", "national"),
    "Северная Македония": ("MKD", "North Macedonia", "national"),
    "Сербия":             ("SRB", "Serbia", "national"),
    "Таджикистан":        ("TJK", "Tajikistan", "national"),
    "Таиланд":            ("THA", "Thailand", "national"),
    "Тунис":              ("TUN", "Tunisia", "national"),
    "Уганда":             ("UGA", "Uganda", "national"),
    "Узбекистан":         ("UZB", "Uzbekistan", "national"),
    "Украина":            ("UKR", "Ukraine", "national"),
    "Уругвай":            ("URY", "Uruguay", "national"),
    "Черногория":         ("MNE", "Montenegro", "national"),
    "Эквадор":            ("ECU", "Ecuador", "national"),
    "Эстония":            ("EST", "Estonia", "national"),
    "Эфиопия":            ("ETH", "Ethiopia", "national"),
    # Северная Ирландия - часть Великобритании, отдельной страной не считаем
    "Северная Ирландия":  ("", "Northern Ireland", "region"),
    # страны проекта ISSP
    "Австрия":            ("AUT", "Austria", "national"),
    "Болгария":           ("BGR", "Bulgaria", "national"),
    "Венгрия":            ("HUN", "Hungary", "national"),
    "Ирландия":           ("IRL", "Ireland", "national"),
    "Кипр":               ("CYP", "Cyprus", "national"),
    "Латвия":             ("LVA", "Latvia", "national"),
    "Португалия":         ("PRT", "Portugal", "national"),
    "Словакия":           ("SVK", "Slovakia", "national"),
    "Словения":           ("SVN", "Slovenia", "national"),
    "Хорватия":           ("HRV", "Croatia", "national"),
    "Чили":               ("CHL", "Chile", "national"),
    "Шри-Ланка":          ("LKA", "Sri Lanka", "national"),
    "Малави":             ("MWI", "Malawi", "national"),
    "Нигер":              ("NER", "Niger", "national"),
    "Пакистан":           ("PAK", "Pakistan", "national"),
    "Кирибати":           ("KIR", "Kiribati", "national"),
    "Микронезия":         ("FSM", "Micronesia", "national"),
    "Новая Зеландия":     ("NZL", "New Zealand", "national"),
    "Норвегия":           ("NOR", "Norway", "national"),
    "Сомали":             ("SOM", "Somalia", "national"),
    "Танзания":           ("TZA", "Tanzania", "national"),
    "Филиппины":          ("PHL", "Philippines", "national"),
    "ЦАР":                ("CAF", "Central African Republic", "national"),
    "Англия":             ("GBR", "England", "national"),
    "Англия и Уэльс":     ("GBR", "England and Wales", "national"),
    "Великобритания":     ("GBR", "United Kingdom", "national"),
    "Бразилия":           ("BRA", "Brazil", "national"),
    "Германия":           ("DEU", "Germany", "national"),
    "Дания":              ("DNK", "Denmark", "national"),
    "Египет":             ("EGY", "Egypt", "national"),
    "Индия":              ("IND", "India", "national"),
    "Индонезия":          ("IDN", "Indonesia", "national"),
    "Испания":            ("ESP", "Spain", "national"),
    "Китай":              ("CHN", "China", "national"),
    "Лесото":             ("LSO", "Lesotho", "national"),
    "Мексика":            ("MEX", "Mexico", "national"),
    "Турция":             ("TUR", "Turkiye", "national"),
    "Нигерия":            ("NGA", "Nigeria", "national"),
    "Нидерланды":         ("NLD", "Netherlands", "national"),
    "Россия":             ("RUS", "Russia", "national"),
    "Саудовская Аравия":  ("SAU", "Saudi Arabia", "national"),
    "США":                ("USA", "United States", "national"),
    "USA":                ("USA", "United States", "national"),
    "Финляндия":          ("FIN", "Finland", "national"),
    "Швеция":             ("SWE", "Sweden", "national"),
    "Южная Корея":        ("KOR", "South Korea", "national"),
    "Япония":             ("JPN", "Japan", "national"),
    "Бангладеш":          ("BGD", "Bangladesh", "national"),
    "Вьетнам":            ("VNM", "Viet Nam", "national"),
    "ОАЭ":                ("ARE", "United Arab Emirates", "national"),
    "Иран":               ("IRN", "Iran", "national"),
    "Иран (Гонабад)":     ("IRN", "Iran", "national"),
    "Иран (Нейшабур)":    ("IRN", "Iran", "national"),
    "Италия":             ("ITA", "Italy", "national"),
    "Польша":             ("POL", "Poland", "national"),
    "Сингапур":           ("SGP", "Singapore", "national"),
    "Франция":            ("FRA", "France", "national"),
    "Чехия":              ("CZE", "Czechia", "national"),
    "Швейцария":          ("CHE", "Switzerland", "national"),
    "ЮАР":                ("ZAF", "South Africa", "national"),
    "ЕС":                 ("EUU", "European Union", "region"),
    "UK/CN/DE/US":        ("", "United Kingdom, China, Germany, United States", "multi"),
    # многострановые и неполные охваты — намеренно без ISO, geo_scope != national,
    # чтобы они не попадали в матрицу покрытия как «страна»
    # регионы отчёта Global Longevity Survey: доля по региону, не по стране
    "Латинская Америка":            ("", "Latin America", "region"),
    "Европа":                       ("", "Europe", "region"),
    "Северная Америка":             ("", "North America", "region"),
    "Африка и Ближний Восток":      ("", "Africa and the Middle East", "region"),
    "Азиатско-Тихоокеанский регион": ("", "Asia-Pacific", "region"),
    # регионы отчёта ВОЗ о физической активности
    "Южная Азия":                   ("", "South Asia", "region"),
    "Океания":                      ("", "Oceania", "region"),
    "Центральная Азия и Ближний Восток":
        ("", "Central Asia and North Africa-Middle East", "region"),
    "Африка (36 стран)":            ("", "Africa (36 countries)", "multi"),
    "Африка (38 стран)":            ("", "Africa (38 countries)", "multi"),
    "Европа (50 стран)":            ("", "Europe (50 countries)", "multi"),
    "Латинская Америка (7 стран)":  ("", "Latin America (7 countries)", "multi"),
    "западные страны и Япония":     ("", "Western countries and Japan", "multi"),
    # неслучайные выборки: не популяция страны, а сообщество или панель
    "выборка Prolific":             ("", "Prolific panel (non-probability)", "community"),
    "сообщество LessWrong":         ("", "LessWrong community (non-probability)", "community"),
    # мировые агрегаты и исторические государства
    "Мир":                          ("WLD", "World", "global"),
    "Бельгия":                      ("BEL", "Belgium", "national"),
    "мета-анализ (10 исследований)": ("", "Meta-analysis (10 studies)", "multi"),
    # исторический замер: в сетку покрытия по нынешним странам не входит
    "СССР":                         ("SUN", "Soviet Union (historical)", "region"),
}

TOPIC_RU = {
    "D1": "Желание бессмертия, вера в загробную жизнь, страх смерти",
    "D2": "Желаемая и ожидаемая продолжительность жизни",
    "D3": "Отношение к технологиям продления жизни",
    "D4": "Демография и статистика населения",
    "D5": "ЗОЖ, здоровье, wellness",
    "E":  "Крионика, цифровое бессмертие, рынки",
    # M — не установка, а описание выборки (доля мужчин, доля с высшим
    # образованием и т. п.). В сетку страна × тема такие строки не входят.
    "M":  "Состав выборки",
}


def en_note(note):
    """Уточнение охвата в скобках по-английски: «25 стран» → «25 countries»."""
    n = note.strip()
    m = re.fullmatch(r"(\d+\+?)\s+(?:стран|страны|странa|страна)", n)
    if m:
        return "%s countries" % m.group(1)
    m = re.fullmatch(r"(\d+)\s+рынков", n)
    if m:
        return "%s markets" % m.group(1)
    return {
        "крион. сообщество": "cryonics community",
        "философы": "philosophers",
        "рекорд": "record",
    }.get(n, n)


def norm_country(raw):
    raw = (raw or "").strip()
    if raw in COUNTRY:
        iso, en, scope = COUNTRY[raw]
        return iso, en, scope, raw
    if raw.startswith("мир"):
        m = re.search(r"\((.+)\)", raw)
        note = m.group(1) if m else ""
        scope = "community" if "крион" in note else "global"
        # Уточнение в скобках прежде переносилось как есть, и в колонку
        # country_en публикуемого набора попадала кириллица: «World
        # (25 стран)». Колонка объявлена английской, читать её так нельзя.
        return "WLD", "World" + (f" ({en_note(note)})" if note else ""), scope, raw
    return "", raw, "other", raw


def norm_value(raw):
    """'37,4' → (37.4, 37.4, point);  '20-24' → (20, 24, range);  '>50' → (50, '', lower_bound)"""
    s = (raw or "").strip().replace(",", ".")
    if not s:
        return "", "", "unknown"
    m = re.fullmatch(r"(-?\d+(?:\.\d+)?)\s*[-–]\s*(-?\d+(?:\.\d+)?)", s)
    if m:
        return m.group(1), m.group(2), "range"
    m = re.fullmatch(r">\s*(-?\d+(?:\.\d+)?)", s)
    if m:
        return m.group(1), "", "lower_bound"
    m = re.fullmatch(r"<\s*(-?\d+(?:\.\d+)?)", s)
    if m:
        return "", m.group(1), "upper_bound"
    m = re.fullmatch(r"-?\d+(?:\.\d+)?", s)
    if m:
        return s, s, "point"
    return "", "", "non_numeric"


def norm_year(raw):
    s = (raw or "").strip()
    if not s:
        return "", ""
    if s.startswith("до "):
        return "", s[3:].strip()
    m = re.fullmatch(r"(\d{4})\s*[-–]\s*(\d{4})", s)
    if m:
        return m.group(1), m.group(2)
    m = re.fullmatch(r"(\d{4})", s)
    if m:
        return s, s
    return "", ""


def norm_n(raw):
    """'8750' → 8750; '60000 дх' → ''(в примечание); 'n/a' → ''"""
    s = (raw or "").strip()
    if not s or s in ("n/a", "—", "-"):
        return "", ""
    m = re.fullmatch(r"(\d[\d\s]*)", s)
    if m:
        return m.group(1).replace(" ", ""), ""
    return "", s


def read(path):
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh, delimiter=";"))


findings = read(SRC_FINDINGS)
sources = {r["source_id"]: r for r in read(SRC_SOURCES)}

COLS = [
    "finding_id", "source_id", "topic", "topic_label", "indicator",
    "country_raw", "country_en", "country_iso3", "geo_scope",
    "year_start", "year_end", "n_sample", "n_note", "subgroup",
    "value_min", "value_max", "value_type", "unit",
    "ci_low", "ci_high", "sd", "uncertainty",
    "is_projection", "is_derived", "verification", "verified_on",
    "question_short", "note",
    "question_type", "technology_type", "response_type", "framing", "ladder_step",
    "source_name", "source_year", "source_url", "source_doi", "source_tier",
    "source_access", "source_license", "source_peer_review",
]

rows = []
missing_src = set()
for f in findings:
    sid = f["source_id"]
    s = sources.get(sid)
    if not s:
        missing_src.add(sid)
    iso_c = norm_country(f["country"])
    vmin, vmax, vtype = norm_value(f["value"])
    ys, ye = norm_year(f["year"])
    n_num, n_note = norm_n(f.get("N", ""))
    rows.append({
        "finding_id": f["finding_id"],
        "source_id": sid,
        "topic": f["topic"],
        "topic_label": TOPIC_RU.get(f["topic"], ""),
        "indicator": f["indicator"],
        "country_raw": iso_c[3],
        "country_en": iso_c[1],
        "country_iso3": iso_c[0],
        "geo_scope": iso_c[2],
        "year_start": ys,
        "year_end": ye,
        "n_sample": n_num,
        "n_note": n_note,
        "subgroup": f.get("subgroup", ""),
        "value_min": vmin,
        "value_max": vmax,
        "value_type": vtype,
        "unit": f["unit"],
        "question_short": f.get("question_short", ""),
        "note": f.get("note", ""),
        # классификация показателя: см. data/codebook.md, раздел «Типология вопросов»
        "question_type": f.get("question_type", ""),
        "technology_type": f.get("technology_type", ""),
        "response_type": f.get("response_type", ""),
        "framing": f.get("framing", ""),
        "ladder_step": f.get("ladder_step", ""),
        # неопределённость величины, как её опубликовал источник
        "ci_low": f.get("ci_low", ""),
        "ci_high": f.get("ci_high", ""),
        "sd": f.get("sd", ""),
        "uncertainty": f.get("uncertainty", ""),
        # прогноз или сценарий, а не замер; величина посчитана нами
        "is_projection": f.get("is_projection", ""),
        "is_derived": f.get("is_derived", ""),
        # откуда мы знаем, что число такое: см. codebook, «Состояние проверки»
        "verification": f.get("verification", ""),
        "verified_on": f.get("verified_on", ""),
        "source_name": (s["organization_authors"] + " — " + s["title"]) if s else "",
        "source_year": s["year"] if s else "",
        "source_url": (s["url"] if s and s["url"] not in ("n/a", "") else "") if s else "",
        "source_doi": s.get("doi", "") if s else "",
        "source_tier": s["tier"] if s else "",
        "source_access": s["access"] if s else "",
        "source_license": s.get("license", "") if s else "",
        "source_peer_review": s.get("peer_review", "") if s else "",
    })


# Колонки с дробными числами. Разделитель в них задаётся форматом файла,
# а не тем, как значение было набрано в рабочей таблице.
NUMERIC_COLS = ("value_min", "value_max", "ci_low", "ci_high", "sd")


def write_csv(path, cols, data, delimiter=",", decimal="."):
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter=delimiter,
                           quoting=csv.QUOTE_MINIMAL, lineterminator="\r\n")
        w.writeheader()
        for r in data:
            out = dict(r)
            # Числовые колонки приводятся к формату файла целиком.
            # Прежде границы интервала и стандартное отклонение просто
            # копировались из рабочего файла с десятичной запятой — и в
            # «международном» findings.csv оказывались строки вида «68,6».
            # pandas читал ci_low, ci_high и sd как object, а не float,
            # и любое среднее по ним падало.
            for k in NUMERIC_COLS:
                v = out.get(k)
                if not v:
                    continue
                v = str(v).replace(",", ".")
                out[k] = v.replace(".", ",") if decimal == "," else v
            w.writerow(out)


# ── findings: два формата ──
write_csv(OUT / "findings.csv", COLS, rows)                              # международный
write_csv(OUT / "findings_ru.csv", COLS, rows, delimiter=";", decimal=",")  # для рус. Excel

# ── sources: два формата ──
SCOLS = ["source_id", "block", "type", "organization_authors", "year", "title",
         "coverage", "N", "method", "fieldwork", "url", "doi", "access",
         "license", "peer_review", "retrieved", "overlap_phase1", "tier",
         "survey_mode", "extraction", "no_data_reason", "notes"]
srows = [{k: r.get(k, "") for k in SCOLS} for r in sources.values()]
write_csv(OUT / "sources.csv", SCOLS, srows)
write_csv(OUT / "sources_ru.csv", SCOLS, srows, delimiter=";")

# ── карта покрытия: страна × тема ──
TOPICS = ["D1", "D2", "D3", "D4", "D5", "E"]
grid = defaultdict(lambda: defaultdict(int))
iso_name = {}
for r in rows:
    if r["geo_scope"] != "national":
        continue
    iso = r["country_iso3"]
    if not iso:
        continue
    iso_name[iso] = r["country_en"]
    grid[iso][r["topic"]] += 1

cov_rows = []
# total считается строго по шести показанным темам, иначе он разъезжается
# с суммой ячеек: в базе есть строки со служебными темами (состав выборки).
for iso in sorted(grid, key=lambda i: (-sum(grid[i].get(t, 0) for t in TOPICS), i)):
    rec = {"country_iso3": iso, "country_en": iso_name[iso],
           "total": sum(grid[iso].get(t, 0) for t in TOPICS)}
    for t in TOPICS:
        rec[t] = grid[iso].get(t, 0)
    # Страна без единого замера по шести темам в матрицу не попадает.
    # Так в неё однажды вошла Бельгия: у неё есть ровно одна строка, и та
    # со служебной темой M (длительность исследования). Строка в наборе
    # нужна, но страной с данными Бельгия от этого не становится —
    # а счётчик стран из-за неё вырос со 109 до 110.
    if rec["total"] == 0:
        continue
    cov_rows.append(rec)
write_csv(OUT / "coverage.csv", ["country_iso3", "country_en", "total"] + TOPICS, cov_rows)

# то же в JSON — для встраивания в витрину
# Один ISO может стоять у нескольких написаний («Иран», «Иран (Нейшабур)»).
# Берём каноническое: без уточнения в скобках и покороче.
RU_NAME = {}
for k, v in COUNTRY.items():
    if v[2] != "national":
        continue
    cur = RU_NAME.get(v[0])
    if cur is None or (("(" in cur) and ("(" not in k)) or \
            (("(" in cur) == ("(" in k) and len(k) < len(cur)):
        RU_NAME[v[0]] = k
RU_NAME.update({"GBR": "Великобритания", "USA": "США"})
cov_json = [{
    "iso": r["country_iso3"],
    "ru": RU_NAME.get(r["country_iso3"], r["country_en"]),
    "en": r["country_en"],
    "total": r["total"],
    "cells": [r[t] for t in TOPICS],
} for r in cov_rows]
(OUT / "coverage.json").write_text(
    json.dumps({"topics": TOPICS, "labels": [TOPIC_RU[t] for t in TOPICS], "rows": cov_json},
               ensure_ascii=False, indent=1), encoding="utf-8")

# ── скрипты набора ──
# У каждого скрипта один авторский экземпляр — в рабочем дереве. В набор он
# кладётся копией при сборке. Прежде копии правились по отдельности и
# разъехались: публикуемый build_dataset.py отстал от рабочего на несколько
# итераций и не запускался вовсе.
for src_path, dst_name in (
    (ROOT / "scripts_build" / "vocab.py", "vocab.py"),
    (ROOT / "scripts_build" / "build_dataset.py", "build_dataset.py"),
    (ROOT / "scripts_build" / "archive_version.py", "archive_version.py"),
    (ROOT / "site" / "build_artifact.py", "build_artifact.py"),
):
    shutil.copy2(src_path, REPO / "scripts" / dst_name)
print("[ok] scripts/: 4 файла синхронизированы с рабочим деревом")

# ── отчёт ──
print(f"[ok] findings: {len(rows)} строк → findings.csv + findings_ru.csv")
print(f"[ok] sources : {len(srows)} строк → sources.csv + sources_ru.csv")
print(f"[ok] coverage: {len(cov_rows)} стран с национальными замерами")
by_type = defaultdict(int)
for r in rows:
    by_type[r["value_type"]] += 1
print("     типы значений:", dict(by_type))
no_iso = sorted({r["country_raw"] for r in rows if not r["country_iso3"] and r["geo_scope"] == "other"})
if no_iso:
    print("[!]  страны без кода:", no_iso)
if missing_src:
    print("[!]  находки без источника:", sorted(missing_src))
print("\nПокрытие по странам (национальные замеры):")
for r in cov_rows:
    cells = " ".join(f"{t}:{r[t]}" if r[t] else f"{t}:·" for t in TOPICS)
    print(f"  {r['country_iso3']}  {r['country_en']:<22} всего {r['total']:>3}   {cells}")
