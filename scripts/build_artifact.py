# -*- coding: utf-8 -*-
"""
Сборка версии для публикации через Artifact.

index.html — полноценный самодостаточный документ: с DOCTYPE, <head>,
meta viewport и Open Graph. Это то, что вы кладёте на свой хостинг.

Платформа Artifact оборачивает содержимое в собственный скелет
<!doctype html><head>…</head><body>, поэтому для неё нужен файл БЕЗ
собственных html/head/body — иначе получится вложенный документ.
Скрипт вырезает обвязку и оставляет <title>, <meta description>,
JSON-LD, <style> и всё тело.

Запуск: python site/build_artifact.py
Результат: site/_artifact.html
"""
import re
from pathlib import Path

SRC = Path(__file__).parent / "index.html"
OUT = Path(__file__).parent / "_artifact.html"

# Копия скрипта едет вместе с публикуемым набором как описание процедуры;
# рядом с ней витрины нет, она лежит на уровень выше. Без этой проверки
# запуск из набора падал с трассировкой.
if not SRC.exists():
    print(
        "Этот скрипт готовит витрину к публикации через Artifact и ждёт\n"
        "index.html рядом с собой. Не найден %s.\n\n"
        "В опубликованном наборе витрина лежит в корне, а скрипт включён\n"
        "как описание процедуры. Запускать его нужно из рабочего\n"
        "репозитория проекта: python site/build_artifact.py" % SRC)
    raise SystemExit(0)

html = SRC.read_text(encoding="utf-8")

# Эмблема должна быть data-URI: из отдельного файла она «портит» холст,
# и выгрузка графика падает на toBlob. Проверяем, что её не отвязали обратно.
assert 'src="emblem.png"' not in html, "эмблема снова ссылается на файл — выгрузка сломается"

# то, что нужно сохранить из <head>
keep = []
m = re.search(r"<title>.*?</title>", html, re.S)
if m:
    keep.append(m.group(0))
m = re.search(r'<meta name="description"[^>]*>', html)
if m:
    keep.append(m.group(0))
m = re.search(r'<script type="application/ld\+json">.*?</script>', html, re.S)
if m:
    keep.append(m.group(0))

# тело: от <style> до </body>
style_start = html.index("<style>")
body_end = html.rindex("</body>")
body = html[style_start:body_end]

# внутри тела <head> уже закрыт — убираем маркеры обвязки
body = body.replace("</head>\n<body>", "").replace("</head>", "").replace("<body>", "")

OUT.write_text("\n".join(keep) + "\n\n" + body.strip() + "\n", encoding="utf-8")

size_kb = OUT.stat().st_size / 1024
print(f"[ok] {OUT.name}: {size_kb:.1f} КБ")

# Проверяем именно теги обвязки. Просто искать "<head" нельзя:
# подстрока встречается в <header class="masthead">.
text = OUT.read_text(encoding="utf-8").lower()
for pattern in (r"<!doctype", r"</?html[\s>]", r"</?head[\s>]", r"</?body[\s>]"):
    found = re.search(pattern, text)
    assert not found, f"обвязка не вырезана: {found.group(0)!r}"
print("[ok] обвязка вырезана, файл пригоден для Artifact")
