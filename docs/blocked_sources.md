# Источники, до которых не удалось добраться

Список того, что автоматическими средствами открыть не получилось, но что
с высокой вероятностью содержит полезные данные. **Это список задач для ручной
работы**, а не отчёт о неудачах: почти всё здесь достаётся человеком за минуты —
через браузер, институциональный доступ или письмо автору.

Для каждой записи указано: что там должно быть, почему не открылось и что
конкретно нужно сделать.

Обозначения препятствий:
`скан` — PDF без текстового слоя, нужен OCR ·
`403` — сервер отказывает автоматическим запросам, но открывается в браузере ·
`пейвол` — платный доступ ·
`форма` — файл выдаётся после заполнения формы ·
`сертификат` — сайт не проходит проверку TLS стандартными средствами ·
`не индексируется` — работы нет в доступных API.

---

## 1. Первоочередное: закрывает открытые долги проекта

### 1.1 Росстат — доли по каждому из пяти критериев ЗОЖ `скан`

**Что нужно:** доли населения, выполняющие каждый из пяти критериев
(некурение, 400 г овощей и фруктов, физактивность 150 мин/нед, соль до 5 г,
умеренный алкоголь) **за один и тот же год**.

**Что известно:** композит по всем пяти — 9,7 % (2024), 9,1 % (2023),
8,9 % (2020), 12,0 % (2019). Отдельно овощи и фрукты — 12 % (2022).
Остальных трёх долей нет.

**Почему важно:** это ключ к главному сюжету базы. Уже установлено, что разрыв
между самооценкой (около 88 %) и измерением (9,7 %) создаётся не перемножением
пяти умеренных требований, а одним-двумя жёсткими диетическими. Полный набор
долей за один год подтвердил бы это окончательно.

**Препятствие:** файлы открываются, но текста в них нет.
Из PDF в 469 КБ извлекается 44 символа — это скан.

| Адрес | Что внутри |
|---|---|
| https://55.rosstat.gov.ru/storage/mediabank/szn_info-2024.pdf | аналитическая записка по ЗОЖ, 2024 |
| https://48.rosstat.gov.ru/storage/mediabank/СЗН2023(1).pdf | итоги наблюдения 2023 |
| https://rosstat.gov.ru/folder/13721 | раздел «Здравоохранение» |
| https://finexpertiza.ru/press-service/researches/2025/bez-vred-priv/ | вторичный разбор по критериям |

**Что сделать:** прогнать PDF через OCR (FineReader, Adobe, `ocrmypdf`), либо
открыть Finexpertiza в браузере — их пресс-релизы в прошлые годы давали
разбивку по каждому критерию отдельно.

⚠ Отдельно: все сайты Росстата подписаны сертификатами Минцифры, которых нет
в хранилище Windows. В браузере это лечится установкой корневого сертификата
НУЦ Минцифры, автоматическим средствам мешает всегда.

### 1.2 NHK, «Исследование сознания японцев» (日本人の意識調査) `не индексируется`

**Что нужно:** есть ли в этом исследовании вопрос о желаемой продолжительности
жизни, и если да — динамика ответов.

**Почему важно:** исследование идёт **с 1973 года каждые пять лет**.
Гармонизированных международных рядов о желаемой продолжительности жизни
не существует вовсе (проверено по 25 инфраструктурам, см. `gaps.md`, раздел 12).
Если у NHK такой вопрос есть, это **самый длинный ряд в мире по теме**
и потенциально важнейшая находка всего проекта.

**Препятствие:** сайт NHK放送文化研究所 не отдаётся автоматическим запросам,
через веб-поиск конкретные страницы не находятся.

**Что сделать:** зайти на www.nhk.or.jp/bunken/ вручную, найти раздел
日本人の意識調査, проверить анкету на вопрос вида 何歳まで生きたいか.

### 1.3 Aparicio A. (2025), Biogerontology 26(1):13 `пейвол`

**Что нужно:** полный текст. Это ближайший аналог нашей работы — обзор
общественного отношения к продлению жизни, 54 источника в списке литературы.

**Препятствие:** доступ закрыт полностью. Проверено через OpenAlex: OA-версии
нет ни в одном репозитории. Аннотация в OpenAlex пустая (`abstract_inverted_index` = null).
Проверены и не дали результата: ResearchGate, academia.edu, препринт-серверы,
CORE, институциональные репозитории, Semantic Scholar.

**Что сделать:** написать автору. Аффилиация установлена —
**Alberto Aparicio, University of Texas Medical Branch at Galveston**.
DOI 10.1007/s10522-024-10157-z, PMID 39585500.


### 1.4 Архив ВЦИОМ до 2009 года — отношение к науке и старению `не индексируется`

**Что нужно:** замеры вопроса «удастся ли науке победить старение» (или близкого)
за 2000-е годы, чтобы продлить ряд влево.

**Что есть сейчас:** 2009 — 6 % ждут от науки «эликсир вечной молодости»
(другая формулировка) · 2023 — 36 % · 2026 — 46 %. Между 2009 и 2023 провал
в четырнадцать лет.

**Почему важно:** это единственный российский ряд, показывающий рост веры
в технологическое решение старения. Сейчас он опирается на две сопоставимые точки.
Любой замер из 2000-х или 2010-х превратил бы его в полноценный тренд.

**Препятствие:** архив ВЦИОМ ведётся с 1992 года, но публичный поиск по нему
не отдаёт результатов по этой теме. Через веб-поиск находятся только публикации
с 2023 года.

**Что сделать:** запрос напрямую в ВЦИОМ либо поиск по их внутреннему архиву
на wciom.ru по ключевым словам «бессмертие», «продление жизни», «старение»
с фильтром по годам.

---

## 2. Числа, заявленные, но не подтверждённые по первоисточнику

Эти значения встречаются во вторичных пересказах, но сверить их с оригиналом
не удалось. **В датасет они не внесены** либо внесены с явной пометкой.

| Источник | Незакрытое число | Препятствие |
|---|---|---|
| Dong, Milholland & Vijg 2016, Nature | предел 115 лет, «плато в 88 % наборов данных», вероятность превысить 125 лет менее 1:10 000 | `403` Nature |
| Einmahl et al. 2019, JASA | точечные оценки предела 115,7 года (женщины) и 114,1 (мужчины) | `пейвол` |
| Barbi et al. 2018, Science | точная величина плато смертности после 105 лет (около 0,47–0,48 в год) | `403` Science |
| Sheeran 2002 | «около 47 % намеренных реально действуют» — канонічная цифра разрыва | `не индексируется` в Europe PMC |
| Conner & Norman 2022 | доли объяснённой дисперсии поведения (заявлено 18–23 %) | в абстракте отсутствуют, нужен полный текст |
| Cutler et al. 2018 | привязка процентов неприверженности к группам болезней | в абстракте есть проценты, но без привязки |
| Bowen & Skirbekk 2016, Ageing & Society | все числовые результаты | журнал не индексируется в Europe PMC |

**Что сделать:** для первых трёх достаточно открыть PDF через институциональный
доступ и выписать значения. Sheeran 2002 — искать в European Review of Social
Psychology, том 12.

⚠ Важно: числа по Dong et al. широко разошлись по прессе. Прежде чем цитировать
«предел 115 лет», стоит убедиться, что это утверждение самих авторов, а не
пересказ. Нейтральный статистический обзор (Belzile et al. 2022) прямо пишет,
что в этом споре часть выводов получена **некорректным статистическим анализом**.

---

## 3. Отчёты опросных организаций

| Источник | Что внутри | Препятствие | Адрес |
|---|---|---|---|
| Global Longevity Survey 2024, полный отчёт | полная страновая таблица по бессмертию для Египта, Саудовской Аравии, ОАЭ, Турции, Индонезии, Коста-Рики | `форма` | globallongevitystudy.com/#block-download |
| Ipsos, Attitudes to Ageing 2025 | страновая таблица по 32 странам, N = 23 745 | PDF не разобран | ipsos.com/sites/default/files/ct/news/documents/2025-07/ipsos-attitudes-to-ageing-2025-survey-report.pdf |
| Geneva Association / Dynata 2025 | опрос по 12 странам, включая Бразилию, Мексику, Индию | PDF не разобран | genevaassociation.org/sites/default/files/2025-02/insurance_and_longevity_report_1902_final.pdf |
| CBOS K_049_26 (Польша) | N и метод опроса о границах старости, ряд с 1998 года | PDF не разобран | cbos.pl/SPISKOM.POL/2026/K_049_26.PDF |
| AIA Healthy Living Index | 15 рынков АТР, N = 10 316, четыре волны с 2011 | PDF не разобран | aia.com/content/dam/group/en/docs/healthy-living-pdf/aia-healthy-living-index-infographic-regional-2016.pdf |
| Datafolha, «Idosos no Brasil 2024» | национальный бразильский замер отношения к старению | первоисточник не найден | — |
| OECD, Health at a Glance 2025 | ОПЖ и здоровая ОПЖ в возрасте 65 лет по странам | `403` | oecd.org/content/dam/oecd/en/publications/reports/2025/11/health-at-a-glance-2025_a894f72e/8f9e3f98-en.pdf |

⚠ По Ipsos 2025 отдельно: во вторичных пересказах обнаружены три расхождения.
CNN Brasil приводит «57 % бразильцев ждут старости, 38 % — нет», что зеркально
повторяет глобальные 57/38 и похоже на ошибку пересказа. По Таиланду один
источник даёт порог старости 68 лет, другой 65. Сверять только по PDF.

---

## 4. Крионика и цифровое бессмертие

| Источник | Что внутри | Препятствие |
|---|---|---|
| Alcor, статистика членства | точные числа и исторический ряд | `403`, открывается в браузере: alcor.org/resources/blog/alcor-members-and-patients-where-and-how-many/ |
| Cryonics Wiki, таблица провайдеров | сводка по всем организациям мира | `403`: cryonics.miraheze.org/wiki/List_of_long-term_care_providers |
| IJHCI 2026, «Adoption of AI-Based Deathbots» | N и страна выборки | `403` Taylor & Francis, DOI 10.1080/10447318.2025.2543995 |
| Thornton et al. 2024, JEET | N, страна и годы волн; единственный источник с ДИНАМИКОЙ по загрузке сознания | PDF 23 стр. не разобран: jeet.ieet.org/index.php/home/article/download/140/131 |
| Mortality 2025, «Digital afterlife leaders» | профессионализация отрасли | `пейвол` |
| StoryFile, дело о банкротстве | подтверждение Chapter 11 и суммы долга около 4,5 млн долларов | сведения только из деловой прессы, нужен реестр PACER |

⚠ По Thornton 2024: издатель — IEET, трансгуманистический институт, то есть
**идеологически ангажирован**. Перед внесением обязательно прочитать
методологический раздел и зафиксировать характер выборки.

⚠ По обоим опросам о крионике (Швейцария 2026, США 2021): среди авторов значится
**E. F. Kendziorra**, по всем признакам — CEO Tomorrow Bio и президент European
Biostasis Foundation. Тождество требует **ручной верификации**, конфликт интересов
подлежит декларированию.

---

## 5. Регионы, где поиск не дал ничего

Это не «не смог открыть», а «похоже, не существует». Отмечено для полноты.

- **Центральная Азия.** Central Asia Barometer ведёт 12 волн по пяти странам
  (ca-barometer.org), но модулей о старении, долголетии и ЗОЖ в открытых
  материалах нет. Найдены только локальные академические работы по Казахстану.
- **Африка южнее Сахары, кроме ЮАР.** Afrobarometer закрывает приоритеты
  здоровья по 38 странам, но **прямых вопросов о желаемой продолжительности
  жизни нет вовсе**.
- **Балканы, Украина, Румыния, Болгария, Сербия.** Ничего релевантного.
- **Национально репрезентативные опросы о крионике** в США, Великобритании,
  Японии, Китае и России. За пределами Германии 2014 и Швейцарии 2026
  в мире нет ни одного.

---

## 6. Технические ограничения инструментов

Зафиксировано для тех, кто будет продолжать сбор автоматическими средствами.

- **Общий веб-поиск нестабилен.** DuckDuckGo блокирует при интенсивном
  обращении и восстанавливается через несколько часов. Публичные инстансы
  SearX отдают 429 и 403. Mojeek почти не даёт внешних ссылок.
  В проекте применён общий межпроцессный ограничитель: не чаще одного
  запроса в 4 секунды на всю машину.
- **Работают стабильно и без ключей:** OpenAlex, Europe PMC, Crossref, PubMed,
  DOAJ, Wikipedia API на любом языке, Wikidata SPARQL, ВОЗ GHO, Eurostat,
  Всемирный банк.
- **Сканы PDF** требуют OCR — без него любой обход блокировок бесполезен.

---

## 7. Собрано страновыми агентами (217 стран)

Прогон по всем странам мира дал **363 записей о недоступных источниках
из 147 стран**. Ниже — по одной-две на страну, полный список
в рабочем файле проекта.

⚠ Важно понимать статус этого раздела. Страновые отчёты — **слой генерации
лидов, а не слой проверенных данных**. Автоматическая сверка показала, что
из 60 проверенных ссылок только 24 содержат на самой странице те числа,
что указаны рядом с ними в отчёте. Часть расхождений объясняется тем, что
число лежит в PDF за ссылкой, а не на ней самой, но проверять надо каждое.

**Поэтому числа отсюда в датасет не внесены.** Это адреса, по которым
стоит сходить руками.

| Страна | Источник |
|---|---|
| ABW | https://cbs.aw/wp/ / HTTP 307 Temporary Redirect |
| ABW | https://cbs.aw/wp/index.php/category/statistical-overview-of-aruba/ / HTTP 307 Temporary Redirect |
| AFG | Не предпринимались попытки открыть конкретные URL в этой сессии — все запросы шли через структурированные API (WHO, World Bank, OpenAlex, PubMed). Прямые веб-страницы и PDF не запрашивались из-за лими |
| AGO | https://en.wikipedia.org/wiki/Demographics_of_Angola / Не запрошен из-за лимита шагов |
| AND | 1. **PDF презентации ENSA 2024** (`https://www.govern.ad/documents/1898932/0/20250929+Presentaci%C3%B3+ENSA+2024.pdf/...`) — не скачан из-за лимита шагов; может содержать дополнительные таблицы (по во |
| AND | 5. **Сайт CRES/IEA** (`https://www.iea.ad/cres`) — не открыт из-за лимита шагов; мог бы содержать архив опросов по темам, выходящим за рамки ENSA. |
| ARG | http://www.msal.gob.ar/images/stories/bes/graficos/0000001444cnt-4ta-encuesta-nacional-factores-riesgo_2019_principales-resultados.pdf / Таймаут соединения (WinError 10060). PDF с результатами 4-й ENF |
| ARG | https://durham-repository.worktribe.com/output/1334080 / HTTP 403 Forbidden. Репозиторий Durham University — возможно, полный текст Hornsey et al. 2018. |
| ASM | https://www.cia.gov/the-world-factbook/countries/american-samoa/ / Ресурс закрыт (sunset) 4 февраля 2026 г. |
| ATG | https://antigua.news/2024/02/14/steps-survey-extended-due-to-lack-of-participation/ / упомянут в выдаче, но не открыт — может содержать детали низкого участия |
| ATG | https://data.who.int/countries/028 / не открыт напрямую (интерактивная страница WHO, требует JS-рендеринга) |
| AUS | https://api.openalex.org/works?search=Australia+survey+attitudes+aging+longevity / search_openalex → HTTP 429 Too Many Requests |
| AUS | https://scholar.google.com/scholar?q=Australia+survey+attitudes+longevity+life+extension / search_web → HTTP 403 Forbidden |
| AUT | https://www.statistik.at/.../gesundheitsverhalten/ernaehrung / Не запрашивал — лимит шагов |
| AUT | https://www.statistik.at/.../gesundheitsverhalten/koerperliche-aktivitaet / Не запрашивал — лимит шагов |
| AZE | https://www.stat.gov.az/menu/index.php?lang=az&id=13 / HTTP 404 — конкретная страница раздела здравоохранения не найдена по этому URL; структура сайта требует уточнения |
| BEL | Eurobarometer public opinion archives** (https://europa.eu/eurobarometer) — не запрашивались. |
| BEL | Sciensano** (https://www.sciensano.be) — не запрашивался. |
| BGD | https://cdn.who.int/media/docs/default-source/searo/ageing-and-health/bangladesh_country-profile.pdf / Ошибка разбора PDF инструментом (`name 'io' is not defined`). |
| BGD | https://public-pages-files-2025.frontiersin.org/journals/public-health/articles/10.3389/fpubh.2025.1517482/pdf / Та же ошибка разбора PDF; HTML-версия той же статьи открыта успешно. |
| BGR | `https://nsi.bg` — сайт НСИ Болгарии: не открыт через `fetch_page` (веб-поиск и fetch были недоступны в сессии). |
| BGR | `https://www.alpharesearch.bg` — сайт «Алфа Рисърч»: не открыт. |
| BHS | `https://www.bahamas.gov.bs/` (BNSI) / Не запрашивался из-за лимита шагов |
| BHS | `https://www.who.int/teams/noncommunicable-diseases/surveillance/data/bahamas` (STEPS) / Не запрашивался из-за лимита шагов |
| BLR | OpenAlex** (https://api.openalex.org) — дважды вернул HTTP 429 Too Many Requests. Поиск по "Belarus life expectancy healthy lifestyle survey" и "Belarus attitudes aging longevity life extension" не вы |
| BLR | Белстат** (https://www.belstat.gov.by) — не запрашивался напрямую из-за лимита шагов; в открытых поисковых выдачах данных по установкам к старению/долголетию не индексируется. |
| BLZ | https://sib.org.bz/mics7/ / Страница пустая, только меню, нет контента |
| BLZ | https://sib.org.bz/mics7/snapshot/ / Не проверялось отдельно, но родительская страница пуста |
| BMU | http://healthcouncil.bm/launch-of-the-population-norms-in-bermuda-survey/ / Не извлечён текст |
| BMU | https://database.earth/population/bermuda/life-expectancy / Не извлечён текст |
| BOL | https://www.ine.gob.bo/index.php/estadisticas-sociales/salud / Страница пуста — только меню, данных нет |
| BOL | https://www.ine.gob.bo/index.php/publicaciones/anuario-estadistico-2024 / Не открывался из-за лимита шагов |
| BRA | https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/29471-pns-2019-cai-o-consumo-de-tabaco-mas-aumenta-o-de-bebida-alcoolica / HTTP 403 Forbidden |
| BRA | https://agenciadenoticias.ibge.gov.br/media/com_mediaibge/arquivos/6a25a69bd2bb7bdcdabd528a5bfb5f7d.pdf / не запрашивался (вероятно, тот же PDF) |
| BRB | Сайт Barbados Statistical Service (https://www.stats.gov.bb/) / Не запрашивался из-за лимита шагов; потенциально содержит данные переписей и обследований здоровья. |
| BRN | https://www.moh.gov.bn/SitePages/NHANSS.aspx** — страница Министерства здравоохранения Брунея о NHANSS: HTTP 404 (страница не найдена или перемещена). |
| BTN | https://www.who.int/publications/m/item/national-survey-for-noncommunicable-disease-risk-factors-and-mental-health-using-who-steps-approach-in-bhutan-2014 / HTTP 404 — страница удалена или перемещена |
| BWA | https://www.statsbots.org.bw/publications/statistical-publications / HTTP 404 — раздел публикаций Statistics Botswana |
| BWA | https://www.statsbots.org.wip/publications / DNS error (опечатка в домене) |
| CAF | `https://www.stat-centrafrique.com/` (ICASEES) / Не запрашивался отдельно; в общем веб-поиске соединение не устанавливалось (WinError 10060). |
| CAN | https://angusreid.org/aging-longevity/ — HTTP 404 |
| CAN | https://angusreid.org/older-canadians-feel-younger-than-their-age/ — HTTP 404 |
| CHI | https://www.gov.gg/healthprofile / HTTP 404 — страница не найдена |
| CHL | https://www.ine.gob.cl/ / Не запрашивался (лимит шагов). |
| CHL | https://www.latinobarometro.org/latContents.jsp / Открыт, но конкретные анкеты волн (Cuestionarios) с вопросами о долголетии/старении/смерти не запрошены из-за лимита шагов. |
| CHN | https://bmcgeriatr.biomedcentral.com/ (первичный DOI обзора DAP-R) / Не запрашивался; использован пересказ eBiotrade |
| CHN | https://wenku.baidu.com/view/afc522ebae51f01dc281e53a580216fc700a5384.html / Не запрашивался (статья «Отношение к старению у пожилых китайцев: базовое состояние, когортные различия и факторы влияния») |
| CIV | Afrobarometer** (https://www.afrobarometer.org/) — сайт не вернул результатов по Кот-д'Ивуару в контексте здоровья/старения. Возможно, данные есть, но поиск не сработал. |
| CIV | DHS Program** (https://dhsprogram.com/) — стандартные обследования DHS по Кот-д'Ивуару существуют, но не содержат вопросов по теме исследования. |
| CMR | Nambiema A. et al., 2025 (JACC)** — полный текст не открыт, в абстракте нет страновых чисел по Камеруну. URL: https://www.jacc.org/ (полный текст за платным доступом JACC). |
| CMR | Wasnyo Y. et al., 2024 (Cureus)** — абстракт получен, полный текст не открыт. URL: https://www.cureus.com/articles/291412 (открытый доступ, но не загружался). |
| COD | https://dhsprogram.com — полные вопросники DHS-VIII / Требуется регистрация; стандартные вопросники DHS не содержат модулей по старению/смерти |
| COD | https://gatsdata.org — GATS по COD / Не проводилось |
| COG | https://dhsprogram.com/Countries/Country-Main.cfm?ctr=53 / Динамическая загрузка, fetch отдаёт только меню навигации (1396 символов), контент отчётов EDS не извлечён. |
| COG | https://dhsprogram.com/Countries/Country-Main.cfm?ctr=53&c=Congo&r=1 / То же — только меню. |
| COL | https://link.springer.com/article/10.1007/s10804-018-9299-8 / Client Challenge (требуется JS/куки) |
| COL | https://link.springer.com/content/pdf/10.1007/s10804-018-9299-8.pdf / Client Challenge |
| COM | OpenAlex** (`https://api.openalex.org/`) — HTTP 429 Too Many Requests на все запросы по теме. Не позволил проверить наличие академических работ. |
| CPV | https://doi.org/10.1787/888933570371 и другие DOI OECD / Не запрашивались — таблицы OECD по Кабо-Верде, не по теме установок |
| CPV | https://ine.cv / Не запрашивался из-за недоступности поиска |
| CYM | https://www.caymaniantimes.ky/documents/2025-07-14-16-56-47-1-ACFROG1.PDF / Не открывался (PDF, не опробован из-за лимита шагов). |
| CYM | https://www.eso.ky/storage/page_docums/uploadFilePdf/822/The%20Cayman%20Islands%27%20Quality%20of%20Life%20Report%20Spring%202024%20Final.pdf / Не открывался (аналогичная проблема с PDF, не опробован  |
| CYP | https://ec.europa.eu/eurostat/databrowser/view/hlth_ehis_pe9e/default/table?lang=en / Пустой ответ (0 символов), требуется JS |
| CYP | https://www.cystat.gov.cy/en/SubthemeStatistics?id=46 / HTTP 302, бесконечный редирект |
| CZE | https://doi.org/10.3390/geriatrics11010002 — HTTP 403 (доступ через PMC12821523 получен альтернативным путём). |
| CZE | https://europepmc.org/article/MED/41562786 — вернул только заголовок без полного текста. |
| DMA | https://academic.oup.com/innovateage/article/7/Supplement_1/156/7487924 / Не открыта (лимит шагов) |
| DMA | https://caribbean.un.org/sites/default/files/2023-03/The%20ageing%20Caribbean-%2020%20years%20of%20the%20Madrid%20Plan%20of%20Action.pdf / Не открыта (лимит шагов) |
| DNK | Danmarks Statistik — здравоохранение / https://www.dst.dk/da/Statistik/emner/sundhed / Не запрашивался из-за лимита шагов |
| DNK | Danskernes Sundhed (нац. профиль здоровья) / https://www.danskernessundhed.dk/ / Не запрашивался из-за лимита шагов |
| DOM | https://www.one.gob.do/ (Oficina Nacional de Estadística) / Не запрошен из-за лимита шагов; search_web возвращал 403 |
| ECU | Сайт INEC (https://www.ecuadorencifras.gob.ec) — не запрашивался. |
| ECU | Сайт ВОЗ по Эквадору (https://www.who.int/countries/ecu/) — не запрашивался. |
| ERI | https://europepmc.org/article/MED/38330202 / Страница редиректит на авторизацию, абстракт не отдан напрямую (получен через PMC-зеркало) |
| ERI | https://www.openalex.org/ (поиск по теме) / HTTP 429 Too Many Requests |
| EST | https://www.tai.ee/et/uuringud / HTTP 404 (страница не существует) |
| EST | https://www.tai.ee/et/valjaanded/trukised-ja-uuringud / HTTP 404 (страница не существует) |
| FJI | `https://extranet.who.int/ncdsmicrodata/index.php/catalog/736` / Открылась страница STEPS Нигера 2007, а не Фиджи — ID каталога неверный |
| FJI | `https://www.statsfiji.gov.fj/` / Бинарный/сжатый ответ, текст не извлечён (вероятно, нестандартное кодирование) |
| FRO | Heilsustýrið** (Управление здравоохранения Фарер) — https://www.heilsustyrid.fo/ — не изучено. |
| FRO | Statbank Hagstova** — https://statbank.hagstova.fo/ — не изучено содержимое таблиц по здоровью. |
| FSM | https://extranet.who.int/ncdsmicrodata/index.php/catalog/STEPS/search?query=Micronesia / Поиск по каталогу не работает через query-параметр, возвращает общий список |
| FSM | https://www.who.int/publications/m/item/2012-2014-steps-country-report-federated-states-of-micronesia-(chuuk) / HTTP 404 — страница удалена или перемещена |
| GBR | https://natcen.ac.uk/publications/british-social-attitudes-survey / HTTP 404 Not Found |
| GEO | https://www.geostat.ge/en/modules/categories/683/health / Открыта, но оказалась страницей занятости, а не здоровья |
| GEO | https://www.who.int/ncds/surveillance/steps/georgia / HTTP 404 Not Found |
| GHA | Afrobarometer Round 10 codebook (2024)** — упомянут на сайте, но не загружен; может содержать модули по здоровью/ЗОЖ. URL: https://www.afrobarometer.org/countries/ghana |
| GIB | https://www.gha.gi/wp-content/uploads/2023/02/Health-and-Lifestyle-Report-2021.pdf / PDF не распарсился инструментом (ошибка `name 'io' is not defined`) — содержит основные цифры опроса, но текст не и |
| GIB | https://www.yourgibraltartv.com/society/23872-our-nation-s-health-health-and-lifestyle-survey-2021 / HTTP 404 — страница удалена или перемещена |
| GIN | STEPS Guinea report (PDF на сайте ВОЗ)** — конкретный URL не найден через поиск; возможно, отчёт существует, но не индексирован в Википедии. |
| GMB | https://dhsprogram.com/pubs/pdf/FR369/FR369.pdf / Ошибка разбора PDF на стороне инструмента (name 'io' is not defined) |
| GNQ | http://www.inege.gq / Сайт на nginx без контента (заглушка) |
| GNQ | https://www.inege.gq / Перенаправление на парковочную страницу магазина |
| GRC | Сайт ΕΛΣΤΑΤ** (https://www.statistics.gr/) — не запрашивался напрямую; рекомендуется проверить вручную на наличие модулей EHIS и национальных обследований здоровья. |
| GRD | https://www3.paho.org/data/index.php/en/indicators-dashboard.html?...&country=Grenada / HTTP 502 Bad Gateway |
| GRL | https://bank.stat.gl/pxweb/da/Greenland/Greenland__SU__SU10/ / Не открывал — лимит шагов. |
| GRL | https://ghdx.healthdata.org/geography/greenland / Не открывал — лимит шагов. |
| GTM | OpenAlex** (https://api.openalex.org) — HTTP 429 Too Many Requests при двух последовательных попытках. Причина: превышение лимита запросов к API. |
| GUY | https://api.worldbank.org/... — HTTP 502 (временная недоступность API Всемирного банка) |
| GUY | https://www.paho.org/en/countries/guyana — HTTP 404 (страница отсутствует или перемещена) |
| HKG | https://www.censtatd.gov.hk/ (раздел отчётов) / Не запрашивался из-за лимита шагов |
| HKG | https://www.dh.gov.hk/ (Population Health Survey) / Не запрашивался из-за лимита шагов |
| HTI | https://dhsprogram.com/Countries/Country-Main.cfm?c=Haiti / Страница вернула статус «Processing…», конкретные годы DHS и ссылки на отчёты не извлечены (1396 символов, без данных) |
| IMN | https://data.humdata.org/dataset/who-data-for-imn / Не загружался (вероятно, тот же класс ограничений) |
| IMN | https://data.unicef.org/country/imn/ / HTTP 403 Forbidden |
| IND | https://academic.oup.com/ije/article/51/4/e167/6503318 / Не открыт (лимит шагов) |
| IND | https://healthnutritionindia.in/reports/documents/35/NFHS-5_INDIA_REPORT.pdf / Не открыт (лимит шагов) |
| IRL | Central Statistics Office Ireland — https://www.cso.ie/ — не запрашивался из-за лимита шагов. |
| IRL | Healthy Ireland Survey reports — https://www.gov.ie/en/department-of-health/publications/healthy-ireland-survey/ — не запрашивался из-за лимита шагов. |
| ITA | https://www.censis.it/ / Поиск через search_web возвращал 403 Forbidden |
| ITA | https://www.demos.it/ / Поиск через search_web возвращал 403 Forbidden |
| JOR | https://bmcpublichealth.biomedcentral.com/articles/10.1186/s12889-023-17183-5 / Client Challenge (защита от ботов, требуется браузер) |
| KAZ | https://stat.gov.kz/kk/industries/social-statries/health / Не запрашивалось, но скорее всего аналогично |
| KAZ | https://stat.gov.kz/ru/industries/social-statries/health / Страница отдаёт только меню, без конкретных данных |
| KHM | https://data.worldbank.org/indicator/SP.DYN.LE00.IN?locations=KH / Не открывался напрямую; данные взяты через worldbank(). |
| KHM | https://dhsprogram.com/publications/publication-FR386-DHS-Final-Reports.cfm (CDHS 2021–2022 Final Report, PDF ~500 стр.) / Не запрашивался в этой сессии; PDF большой, требует отдельного fetch_page. |
| KIR | https://www.nso.gov.ki/ / Таймаут / не успели |
| KNA | 1. **World Bank Data API** (`https://api.worldbank.org/v2/country/KNA/indicator/SP.DYN.LE00.IN`) — HTTP 502 Bad Gateway (серверная ошибка на стороне провайдера данных). |
| KNA | 2. **OpenAlex API** (`https://api.openalex.org/works?search=...`) — HTTP 429 Too Many Requests (превышение rate limit). |
| KOR | https://api.openalex.org/works?search=… / HTTP 429 Too Many Requests (две попытки) |
| KOR | https://kosis.kr (통계청) / Не запрашивался из-за лимита шагов |
| KWT | Сайт Central Statistical Bureau Кувейта (https://www.csb.gov.kw) / Не запрашивался из-за лимита шагов |
| LAO | https://europepmc.org/article/MED/37424682 / Только заглушка, раздел Data недоступен |
| LAO | https://www.thelancet.com/journals/lanwpc/article/PIIS2666-6065(22)00209-3/fulltext / HTTP 403 Forbidden |
| LBN | MICS 2023 (полный отчёт)** — на сайте CAS упомянут, но прямая ссылка на PDF не извлечена из-за SEO-спама на странице. |
| LBR | https://www.lisgis.net/ / Сайт взломан, отображается тайский спам-контент вместо статистики |
| LBY | https://bsca.ly / DNS не резолвится (getaddrinfo failed) |
| LBY | https://mics.unicef.org/surveys / HTTP 403 Forbidden |
| LCA | https://api.openalex.org/works?search=Saint+Lucia+aging+attitudes+longevity+survey / HTTP 429 Too Many Requests |
| LCA | https://www.stats.gov.lc/health/ / HTTP 404 Not Found |
| LIE | PDF медиа-брифинга** https://www.regierung.li/files/attachments/20241129-medienorientierung-gesundheitsbefragung.pdf — не загружен. |
| LUX | https://statistiques.public.lu/fr/recherche.html?search=sant%C3%A9 / HTTP 404 |
| LUX | https://statistiques.public.lu/fr/themes.html / HTTP 404 |
| MAC | https://api.openalex.org/works?search=Macao+longevity+attitudes+aging+survey / HTTP 429 Too Many Requests |
| MAC | https://api.worldbank.org/v2/... (MAC, SH.XPD.CHEX.GD.ZS, 2020) / HTTP 502 Bad Gateway |
| MAF | https://www.iedom.fr/IMG/pdf/saint-martin_2023_chiffres_cles.pdf / Не запрашивался (лимит шагов) |
| MAF | https://www.insee.fr/fr/statistiques/2011101?geo=COM-97127 / Не запрашивался в этой сессии (лимит шагов) |
| MAR | https://www.hcp.ma/Publications_r205.html / HTTP 404 — страница не существует или перемещена |
| MAR | https://www.hcp.ma/Revenu-conditions-de-vie/Nutrition-et-sante_r217.html / HTTP 404 — страница не существует или перемещена |
| MCO | https://api.worldbank.org/v2/... (MCO, SP.DYN.LE00.IN) / HTTP 502 Bad Gateway на всех попытках (2019, 2022). Сервер World Bank не отвечает на запросы по Монако. |
| MCO | https://imsee.mc/content/download/265444/file/Monaco%20en%20Chiffres%202025%20Edito.pdf / PDF не запрашивался из-за лимита шагов; вероятно содержит данные об ОПЖ и здоровье. |
| MDA | https://statistica.md/ro/area-statistica-sns / HTTP 404 — раздел здравоохранения по этому пути не существует; нужна навигация через «Statistici A–Z» или «Banca de date» на главной странице BNS. |
| MDG | https://microdata.worldbank.org (DHS Madagascar) / Не запрашивалось; известно только из вторичного упоминания в Wikipedia |
| MDG | https://www.instat.mg / Не открывался в рамках сессии |
| MDV | https://extranet.who.int/ncdsmicrodata/index.php/catalog/736 / Каталог микроданных STEPS — открыл запись по Нигеру вместо Мальдив (ID 736 — это Niger 2007). Для Мальдив нужен другой catalog ID, не про |
| MDV | https://www.who.int/publications/m/item/2011-steps-country-report-maldives / Страница-описание отчёта; PDF (4,4 MB) не извлечён через fetch_page — отдаётся только через кнопку Download. |
| MEX | https://en.www.inegi.org.mx/contenidos/saladeprensa/boletines/2023/ENASEM/ENASEM_21.pdf / Ошибка парсера PDF |
| MEX | https://www.inegi.org.mx/contenidos/programas/enasem/2024/doc/enasem_2024_presentacion.pdf / Ошибка парсера PDF (`name 'io' is not defined`) |
| MHL | https://data.who.int/countries/584 / Не открыт из-за лимита шагов; WHO API (`who_indicator`) вернул пустые массивы по `life_expectancy` и `hale` для MHL |
| MHL | https://data.worldbank.org/country/marshall-islands / World Bank API возвращал HTTP 502 на все запросы (life expectancy, доля 65+, и т.д.) |
| MKD | https://api.openalex.org/... / HTTP 429 Too Many Requests — инструмент временно недоступен. |
| MKD | https://equityhealthj.biomedcentral.com/articles/10.1186/s12939-023-02082-3 / BMC вернул «Client Challenge» — требуется другой браузер / отключён блокировщик. |
| MMR | Сайт Department of Population Мьянмы** (https://www.dop.gov.mm) — не проверялся из-за лимита шагов; известно, что после 2021 года доступ к государственным статистическим ресурсам Мьянмы ограничен. |
| MNE | https://www.monstat.org/cg/page.php?id=1488** — предполагаемый раздел статистики здоровья Monstat: возвращает только заголовок «MONSTAT / UPRAVA ZA STATISTKU» без содержания (пустая страница, 29 симво |
| MNP | https://data.worldbank.org/country/northern-mariana-islands / World Bank API возвращает HTTP 502 |
| MNP | https://ver1.cnmicommerce.com/divisions/central-statistics/ / Не открыт — не хватило шагов |
| MRT | https://www.ons.mr/ / Отказ соединения (WinError 10061) — сайт недоступен из текущей сети |
| MUS | Statistics Mauritius (https://statsmauritius.govmu.org)** — не запрашивался из-за лимита шагов. |
| NCL | https://api.openalex.org/works?search=... / HTTP 429 Too Many Requests |
| NCL | https://api.worldbank.org/v2/country/NCL/indicator/SH.XPD.CHEX.GD.ZS / Таймаут |
| NER | https://europepmc.org/article/MED/38330202 / Техническая ошибка сервера EuropePMC ("The Data section on the Article page is currently unavailable") |
| NER | https://www.stat-niger.org / Сайт не открыт напрямую в рамках поиска (упоминается в Wikipedia как официальный ресурс) |
| NGA | https://academic.oup.com/gerontologist/article/62/9/1243/6661277 / HTTP 403 Forbidden |
| NGA | https://onlinelibrary.wiley.com/doi/10.1002/puh2.70125 / HTTP 403 Forbidden |
| NIC | https://es.wikipedia.org/wiki/Salud_en_Nicaragua / Статья существует, но текст пустой (chars: 0) |
| NLD | https://www.cbs.nl/nl-nl/maatwerk/2024/45/leefstijlmonitor-2023 / HTTP 404 (страница не найдена) |
| NOR | OpenAlex (https://api.openalex.org) / HTTP 429 (слишком много запросов) — не удалось получить академические данные |
| NOR | https://www.fhi.no/he/folkehelserapporten/levevaner/royking-og-snusbruk-i-norge/ / HTTP 404 (страница не найдена) |
| NRU | https://microdata.pacificdata.org/index.php/catalog/25/pdf-documentation / Не запрашивался из-за лимита шагов |
| NRU | https://nauru-data.sprep.org/resource/republic-nauru-demographic-and-health-survey-2007 / Не запрашивался из-за лимита шагов |
| NZL | https://www.health.govt.nz/nz-health-statistics/national-collections-and-surveys/surveys/new-zealand-health-survey / HTTP 403 Forbidden |
| OMN | GSA 2024/2025 Abstract Book PDF** (PMC11688754, PMC12755232) — найдены в EuropePMC, но представляют собой большие PDF-сборники тезисов конференций; в рамках лимита шагов проверить наличие оманских тез |
| PAK | https://azaadurdu.pk/109179/ / Не открывался (Gallup Pakistan) |
| PAK | https://e.jang.com.pk/detail/101629 / Не открывался |
| PHL | Сайт Philippine Statistics Authority (https://psa.gov.ph)** — не запрашивался из-за лимита шагов; вероятно, содержит данные национальных обследований (например, National Nutrition Survey, National Dem |
| PHL | Сайт Pulse Asia (https://www.pulseasia.ph)** — не запрашивался. |
| PLW | https://academic.oup.com/gerontologist/article/64/2/gnad078/7205917 / Не успел скачать полный текст (лимит шагов исчерпан) |
| PLW | https://palaugov.pw/health-statistics/ / Не загружался из-за лимита шагов; известно только по упоминанию в Википедии |
| PNG | https://europepmc.org/article/MED/35223727 / Только заголовок, полный текст недоступен через EuropePMC (Data section unavailable) |
| PRI | Полные тексты статей PMID 40163751, 35948823, 38846258, 32037335** — платный доступ или PDF без машиночитаемого слоя; абстракты через EuropePMC API в данной сессии не извлечены (запросы возвращали раб |
| PRK | `https://europepmc.org/article/MED/30997161` / Страница EuropePMC вернула только служебный заголовок (419 символов), полный текст не отдан напрямую. |
| PRY | https://www.ine.gov.py/ / Сетевая ошибка (search_web недоступен) |
| PRY | https://www.mspbs.gov.py/ / Сетевая ошибка |
| PSE | https://bmcgeriatr.biomedcentral.com/articles/10.1186/s12877-025-05946-1 / Client Challenge (anti-bot) BMC |
| PSE | https://bmcpublichealth.biomedcentral.com/articles/10.1186/s12889-025-23880-0 / Client Challenge (anti-bot) BMC |
| PYF | https://www.ispf.pf/publications/ / HTTP 404 Not Found — раздел публикаций отсутствует или перенесён |
| QAT | https://doi.org/10.21203/rs.3.rs-4374618/v1 (Mohamed et al., 2024, препринт) / Не открыт полный текст; доступ по абстракту через EuropePMC |
| RUS | https://wciom.ru/search?query=долголетие / HTTP 500 Internal Server Error |
| RWA | https://bmcpublichealth.biomedcentral.com/articles/10.1186/s12889-024-19038-z / BMC заблокировал запрос (Client Challenge / ad blocker) |
| RWA | https://europepmc.org/article/MED/38840236 / EuropePMC вернул только заглушку (Data section unavailable) |
| SAU | https://doi.org/10.3390/healthcare13111229 — прямой доступ через doi.org вернул HTTP 403 (MDPI блокирует ботов). Текст получен через зеркало PMC (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12155436/ |
| SAU | https://europepmc.org/article/MED/40508843 — страница EuropePMC вернула только шапку без полного текста (вероятно, требуется авторизация через ORCID для части PMC-материалов). |
| SDN | http://hdl.handle.net/10500/4659 / Диссертация о народном исламе в Судане — потенциально релевантна, но полный текст не открыт в сессии |
| SDN | https://brill.com/downloadpdf/title/31679.pdf / Книга об аде в исламе — не страновое исследование |
| SEN | https://api.openalex.org/works?search=Senegal+attitudes+aging+longevity / HTTP 429 (Too Many Requests) — превышение лимита запросов к OpenAlex |
| SEN | https://www.ansd.sn/ / Открыт, но не содержит модулей по отношению к старению/долголетию; только экономические и демографические индикаторы |
| SGP | https://www.moh.gov.sg/resources-statistics/singapore-health-facts/health-surveys / HTTP 404 (страница удалена/перемещена) |
| SGP | https://www.moh.gov.sg/resources-statistics/singapore-health-facts/national-population-health-survey / HTTP 404 (страница удалена/перемещена) |
| SLE | https://api.openalex.org/works?search=... / HTTP 429 Too Many Requests |
| SLE | https://dhsprogram.com/pubs/pdf/FR365/FR365.pdf / Ошибка парсера PDF (`name 'io' is not defined`) |
| SMR | https://giornalesm.com/san-marino-indagine-sui-consumi-e-sullo-stile-di-vita-delle-famiglie-sammarinesi-nuovi-nuclei-familiari-con-ampiezza-ridotta-o-monocomponente/ / Открыта, но содержит только заго |
| SMR | https://www.statistica.sm/indagine-sui-consumi-e-sullo-stile-di-vita-delle-famiglie-sammarinesi / HTTP 404 — страница отсутствует (вероятно, перенесена в раздел «pub1») |
| STP | https://www.ine.st/mics/ — HTTP 404 (страница не существует). |
| STP | https://www.who.int/ncds/surveillance/steps/Sao-Tome-and-Principe — HTTP 404 (страница не существует). |
| SVK | NCZI** (https://www.nczisk.sk) — не запрашивался. |
| SVK | ÚVZ SR** (https://www.uvzsr.sk) — не запрашивался. |
| SVN | https://www.stat.si/ (SURS) / Не запрашивался из-за лимита шагов |
| SXM | http://stats.sintmaartengov.org/ (главная) / Не загружалась отдельно; на странице таблиц Census 2011 видно, что весь контент — ссылки на Excel-файлы |
| SXM | http://stats.sintmaartengov.org/tables.php?division=social&topic=cen → файл Health 2011 / Скачиваемый Excel-файл, текстовый слой отсутствует, инструмент fetch_page не извлекает содержимое .xls/.xlsx |
| SYC | WHO STEPS Seychelles country report (PDF) / Не найден путь из-за блокировки поиска |
| SYR | https://doi.org/10.1007/s44192-024-00120-2 / Сайт издателя Springer Nature вернул «Client Challenge» (предположительно защита от ботов/CAPTCHA). Полный текст получен через PMC (см. выше). |
| TCA | PDF факт-шит GSHS TCI 2022** (https://cdn.who.int/media/docs/default-source/ncds/ncd-surveillance/data-reporting/turks-and-caicos/gshs/2022-gshs-turks-and-caicos-factsheet.pdf) — PDF не распарсился ин |
| TCA | World Bank API** (https://api.worldbank.org/v2/country/TCA/indicator/SP.DYN.LE00.IN) — HTTP 502 Bad Gateway на момент запроса. |
| THA | Сайт NSO Таиланда (http://www.nso.go.th) / Не запрашивался из-за лимита шагов |
| TJK | https://www.stat.tj/ru/social / HTTP 500 Internal Server Error |
| TJK | https://www.stat.tj/social / HTTP 500 Internal Server Error |
| TKM | Wikipedia: «Mental health in Turkmenistan»** (https://en.wikipedia.org/wiki/Mental_health_in_Turkmenistan) — не загружалась в рамках отведённых шагов; потенциально могла содержать данные о суицидах и  |
| TLS | https://dhsprogram.com/pubs/pdf/FR329/FR329.pdf (DHS 2016 Timor-Leste) — не запрашивался в этой сессии из-за лимита шагов. |
| TLS | https://www.statistics.gov.tl/ — DNS не резолвится (getaddrinfo failed). |
| TON | https://psro.dataforall.org/sites/default/files/2024-10/Tonga_Demographic_and_Health_Survey_DHS_Report_2012.pdf / PDF не распарсился (ошибка парсера: `name 'io' is not defined`). Полный текст 339-стра |
| TTO | https://api.openalex.org/... / HTTP 429 Too Many Requests (на протяжении всей сессии) |
| TTO | https://cso.gov.tt/ / HTTP 403 Forbidden |
| TUR | https://bmcgeriatr.biomedcentral.com/track/pdf/10.1186/s12877-018-0902-4 / полный текст не открыт |
| TUR | https://data.tuik.gov.tr/ (TÜİK) / не запрашивался из-за лимита шагов |
| TUV | https://ia801705.us.archive.org/34/items/2007-tuvalu-dhs-report/2007_Tuvalu_DHS-Report.pdf / Полный PDF TDHS 2007 (430 стр.) / Ошибка парсера PDF на стороне инструмента (`name 'io' is not defined`) |
| TUV | https://microdata.pacificdata.org/index.php/catalog/460/related-materials / Микроданные TDHS 2007 / Требуется регистрация; не запрашивались |
| UKR | https://translational-medicine.biomedcentral.com/track/pdf/10.1186/s12967-017-1259-8 / Client Challenge / блокировка (PDF не загрузился) |
| USA | Gallup Life Evaluation Index (https://www.gallup.com/394505/indicator-life-evaluation-index.aspx) — не загружался целенаправленно. |
| VCT | https://cdn.who.int/media/docs/default-source/ncds/ncd-surveillance/data-reporting/saint-vincent-and-the-grenadines/steps/stvincent_steps_factsheet_2013-14.pdf / STEPS Fact Sheet 2013–14 / Та же ошибк |
| VCT | https://cdn.who.int/media/docs/default-source/ncds/ncd-surveillance/data-reporting/saint-vincent-and-the-grenadines/steps/stvincent_steps_report_2013-14.pdf / STEPS Country Report 2013–14, ~80 стр. /  |
| VEN | http://www.ine.gob.ve/ / Сайт INE Venezuela в ходе сессии не открыт через fetch_page (не проверялось из-за лимита шагов); известно, что сайт работает нестабильно с 2017 г. |
| VEN | https://api.openalex.org/ (поиск по Venezuela) / HTTP 429 Too Many Requests — временная блокировка |
| VIR | https://assets.ctfassets.net/9crgcb5vlu43/2fzCUjTlCtl6Z9N5svZIlx/3763227ae8c849591732ed6912d1ff97/longevity-economy-outlook-2026-virgin-islands.doi.10.26419-2fint.00401.054.pdf / Не запрашивался; PDF  |
| VIR | https://doh.vi.gov/wp-content/uploads/2026/04/2025_Annual_Report_FINAL.pdf / Ошибка парсинга PDF инструментом |
| VNM | GSO Vietnam (https://www.gso.gov.vn)** — сайт доступен, но специализированных публикаций по теме отношения к старению/смерти/ЗОЖ в открытом доступе не обнаружено. |
| WSM | https://en.wikipedia.org/wiki/Samoa_Bureau_of_Statistics / HTTP 404 — страница отсутствует |
| WSM | https://www.who.int/ncds/surveillance/steps/samoa/en/ / HTTP 404 — страница отсутствует |
| XKX | https://ask.rks-gov.net/** — загрузился как SPA, текстового контента нет (117 символов). |
| YEM | https://www.cso-yemen.org / Сайт национального статведомства — не открыт из текущей среды (вероятно, ограничения хостинга или блокировка). |
| ZMB | `https://www.zamstats.gov.zm` / Не загружался — приоритет отдан Wikipedia для подтверждения названия ведомства. |
| ZWE | https://api.openalex.org/works (поиск по attitudes aging Zimbabwe) / HTTP 429 Too Many Requests |
| ZWE | https://www.google.com / DuckDuckGo (search_web) / HTTP 403 Forbidden |
