#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Создание HTML-файла с превью всех 7 рисунков.
HTML открывается в любом браузере и позволяет посмотреть рисунки до вставки.
"""
import os

OUT = "/projects/sandbox/llplmxvd/diplom/risunki"

figures = [
    ("risunok_1_1_1.svg", "Рисунок 1.1.1 – Классификация переводов денежных средств"),
    ("risunok_1_3_1.svg", "Рисунок 1.3.1 – Схема прохождения межбанковского перевода через ПС БР"),
    ("risunok_1_3_2.svg", "Рисунок 1.3.2 – Архитектура национальной платёжной инфраструктуры РФ"),
    ("risunok_2_1_1.svg", "Рисунок 2.1.1 – Динамика активов ПАО «Сбербанк» за 2022–2024 гг."),
    ("risunok_2_2_1.svg", "Рисунок 2.2.1 – Динамика количества переводов через СБП в ПАО «Сбербанк»"),
    ("risunok_2_2_2.svg", "Рисунок 2.2.2 – Структура комиссионных доходов от РКО"),
    ("risunok_2_3_1.svg", "Рисунок 2.3.1 – Дерево направлений совершенствования системы переводов"),
]

# читаем все SVG целиком и встраиваем
parts = []
parts.append("""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Рисунки к дипломной работе — превью</title>
<style>
  body { font-family: 'Times New Roman', serif; max-width: 1400px; margin: 30px auto; padding: 20px; background: #F5F5F5; }
  h1 { text-align: center; color: #1F6FB2; }
  .figure { background: white; padding: 20px; margin: 30px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-radius: 8px; }
  .caption { font-style: italic; text-align: center; margin-top: 15px; color: #555; font-size: 14px; }
  svg { max-width: 100%; height: auto; display: block; margin: 0 auto; }
  .meta { color: #888; font-size: 13px; text-align: center; margin-bottom: 30px; }
</style>
</head>
<body>
<h1>Рисунки к дипломной работе</h1>
<p class="meta">Тема: «Организация переводов денежных средств в коммерческих банках (на материалах ПАО Сбербанк)»<br>
Превью семи рисунков перед вставкой в Word-документ</p>
""")

for filename, title in figures:
    full = os.path.join(OUT, filename)
    if not os.path.exists(full):
        continue
    with open(full, encoding="utf-8") as f:
        svg_content = f.read()
    # уберём XML-декларацию
    svg_content = svg_content.replace('<?xml version="1.0" encoding="UTF-8"?>\n', '')
    parts.append(f'<div class="figure">{svg_content}<div class="caption">{title}</div></div>\n')

parts.append("""
<p class="meta">
Все рисунки сохранены как SVG (масштабируемая векторная графика).<br>
Для вставки в Word см. инструкцию в файле <code>README.md</code>.
</p>
</body>
</html>
""")

html = "\n".join(parts)
output_path = os.path.join(OUT, "preview.html")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Создан HTML-файл превью: {output_path}")
print(f"Размер: {os.path.getsize(output_path)} bytes")
print()
print("Откройте preview.html в любом браузере, чтобы увидеть все 7 рисунков сразу.")
