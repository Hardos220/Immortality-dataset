# -*- coding: utf-8 -*-
"""
Архивация версии витрины.

Каждая опубликованная версия index.html сохраняется в site/archive/ под именем
с номером версии и датой, плюс строка в манифесте. Версия и дата читаются
из самого файла, руками ничего вводить не нужно.

Запуск: python scripts_build/archive_version.py
Идемпотентен: если версия уже заархивирована и файл не менялся, ничего не делает.
"""
import hashlib
import io
import re
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "site" / "index.html"
ARCH = ROOT / "site" / "archive"
MANIFEST = ARCH / "MANIFEST.md"


def read_version(text):
    m = re.search(r"Версия\s+(\d+\.\d+(?:\.\d+)?)\s+·\s+(\d{2}\.\d{2}\.\d{4})", text)
    if m:
        d, mo, y = m.group(2).split(".")
        return m.group(1), "%s-%s-%s" % (y, mo, d)
    m = re.search(r"версия\s+(\d+\.\d+(?:\.\d+)?)", text)
    return (m.group(1) if m else "0.0"), date.today().isoformat()


def stats(text):
    """Счётчики на странице подставляются скриптом, поэтому в разметке их нет.
    Берём из тех же мест, откуда их берёт сама страница: длина массива SRC
    и константа N_FIN."""
    m = re.search(r"const SRC = \[(.*?)\n\];", text, re.S)
    nsrc = len([l for l in m.group(1).split("\n") if l.strip().startswith("[")]) if m else "?"
    f = re.search(r"const N_FIN = (\d+);", text)
    return str(nsrc), (f.group(1) if f else "?")


def main():
    # Копия скрипта едет вместе с публикуемым набором как описание процедуры.
    # Архив версий ведётся в рабочем репозитории, в набор он не входит.
    if not SRC.exists():
        print(
            "Этот скрипт архивирует опубликованную версию витрины и ждёт\n"
            "site/index.html. Не найден %s.\n\n"
            "Архив версий ведётся в рабочем репозитории проекта; в набор\n"
            "скрипт включён как описание процедуры." % SRC)
        raise SystemExit(0)
    ARCH.mkdir(parents=True, exist_ok=True)

    text = io.open(SRC, encoding="utf-8").read()
    ver, dt = read_version(text)
    nsrc, nfnd = stats(text)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()

    target = ARCH / ("index_v%s_%s.html" % (ver, dt))

    if target.exists():
        old = hashlib.sha256(io.open(target, encoding="utf-8").read().encode("utf-8")).hexdigest()
        if old == digest:
            print("версия %s за %s уже в архиве, файл не менялся" % (ver, dt))
            return
        # та же версия, но содержимое иное — добавляем короткий хеш
        target = ARCH / ("index_v%s_%s_%s.html" % (ver, dt, digest[:7]))

    shutil.copy2(SRC, target)

    row = ("| %s | %s | %s | %s | %s | `%s` |\n"
           % (ver, dt, nsrc, nfnd, target.name, digest[:12]))
    if not MANIFEST.exists():
        io.open(MANIFEST, "w", encoding="utf-8", newline="\n").write(
            "# Архив версий витрины\n\n"
            "Каждая опубликованная версия сохраняется целиком. Файлы самодостаточны:\n"
            "открываются локально без сети и без внешних зависимостей.\n\n"
            "Хеш — SHA-256 файла на момент архивации, первые 12 символов.\n\n"
            "| Версия | Дата | Источников | Показателей | Файл | SHA-256 |\n"
            "|---|---|---|---|---|---|\n")
    with io.open(MANIFEST, "a", encoding="utf-8", newline="\n") as f:
        f.write(row)

    kb = target.stat().st_size / 1024
    print("заархивировано: %s (%.0f КБ)" % (target.name, kb))
    print("  версия %s, дата %s, источников %s, показателей %s" % (ver, dt, nsrc, nfnd))


if __name__ == "__main__":
    main()
