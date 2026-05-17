#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генерация 7 рисунков для дипломной работы.
Без сторонних библиотек — только встроенный Python (SVG как XML).
"""
import os, math, zlib, struct, base64

OUT = "/projects/sandbox/llplmxvd/diplom/risunki"
os.makedirs(OUT, exist_ok=True)

# Глобальный стиль: чёрно-белый, чтобы хорошо смотрелось в дипломе
FG = "#000000"
BG = "#FFFFFF"
GRID = "#CCCCCC"
ACCENT = "#1F6FB2"   # Сбербанковский синий
ACCENT2 = "#21A038"  # Сбербанковский зелёный
GREY = "#888888"
LIGHT = "#E8E8E8"
FONT = "Times New Roman, Times, serif"

def svg_open(w, h):
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'font-family="{FONT}" font-size="14">\n'
            f'<rect width="{w}" height="{h}" fill="{BG}"/>\n')

def svg_close():
    return '</svg>\n'

def rect(x, y, w, h, fill="none", stroke=FG, sw=1, rx=0):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
            f'rx="{rx}" ry="{rx}"/>\n')

def line(x1, y1, x2, y2, stroke=FG, sw=1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{d}/>\n'

def arrow_def():
    return ('<defs>'
            '<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" '
            'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
            '<path d="M 0 0 L 10 5 L 0 10 z" fill="#000000"/></marker>'
            '<marker id="arrAcc" viewBox="0 0 10 10" refX="9" refY="5" '
            f'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
            f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{ACCENT}"/></marker>'
            '</defs>\n')

def arrow(x1, y1, x2, y2, stroke=FG, sw=1.5):
    marker = "arr" if stroke == FG else "arrAcc"
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" '
            f'stroke-width="{sw}" marker-end="url(#{marker})"/>\n')

def text(x, y, s, *, size=14, anchor="middle", fill=FG, weight="normal", style="normal"):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
            f'font-size="{size}" fill="{fill}" font-weight="{weight}" '
            f'font-style="{style}">{xml_escape(s)}</text>\n')

def text_multiline(x, y, lines, *, size=12, anchor="middle", fill=FG, weight="normal", lh=1.25):
    out = ""
    line_h = int(size * lh)
    for i, ln in enumerate(lines):
        out += text(x, y + i * line_h, ln, size=size, anchor=anchor, fill=fill, weight=weight)
    return out

def xml_escape(s):
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;"))

def box(x, y, w, h, lines, *, size=12, fill=BG, stroke=FG, sw=1, weight="normal", color=FG):
    """Прямоугольник со многострочным текстом по центру."""
    out = rect(x, y, w, h, fill=fill, stroke=stroke, sw=sw, rx=4)
    line_h = int(size * 1.25)
    total_h = len(lines) * line_h
    start_y = y + (h - total_h) / 2 + size
    for i, ln in enumerate(lines):
        out += text(x + w/2, start_y + i * line_h, ln, size=size, fill=color, weight=weight)
    return out

def title(x, y, s, size=15):
    return text(x, y, s, size=size, weight="bold")

def subtitle(x, y, s, size=12):
    return text(x, y, s, size=size, style="italic", fill=GREY)


# ========================================================================
# Рисунок 1.1.1 — Классификация переводов денежных средств
# ========================================================================

def fig_1_1_1():
    W, H = 1100, 800
    svg = svg_open(W, H) + arrow_def()
    svg += title(W/2, 30, "Рисунок 1.1.1 – Классификация переводов денежных средств")

    # Центральный блок
    cx, cy = W/2, H/2 + 20
    cw, ch = 240, 80
    svg += box(cx - cw/2, cy - ch/2, cw, ch,
               ["ПЕРЕВОДЫ", "ДЕНЕЖНЫХ СРЕДСТВ"],
               size=14, weight="bold", fill=LIGHT, sw=2)

    # 8 категорий
    categories = [
        ("По субъектному составу", ["P2P, P2B, B2B,", "B2P, G2P, P2G"]),
        ("По территории", ["внутрибанковские,", "межбанковские,", "трансграничные"]),
        ("По валюте", ["в национальной", "и иностранной"]),
        ("По срокам", ["срочные,", "стандартные,", "регулярные"]),
        ("По инициативе", ["кредитовые,", "дебетовые"]),
        ("По форме расчётов", ["п/п, аккредитив,", "инкассо, чеки,", "ЭДС"]),
        ("По каналу", ["офис, ДБО,", "банкомат, СБП,", "терминал"]),
        ("По цели", ["потребит., налог.,", "инвестиц., соц."]),
    ]

    # 8 позиций по окружности
    radius_x = 460
    radius_y = 290
    for i, (head, items) in enumerate(categories):
        angle = -math.pi/2 + i * (2 * math.pi / 8)
        bx = cx + radius_x * math.cos(angle)
        by = cy + radius_y * math.sin(angle)
        bw, bh = 200, 90
        # стрелка от центра
        # точка контакта на центральном блоке
        if abs(math.cos(angle)) > 0.5:
            sx = cx + (cw/2) * (1 if math.cos(angle) > 0 else -1)
            sy = cy + ((cw/2) * math.sin(angle) / math.cos(angle)) if math.cos(angle) != 0 else cy
            sy = max(cy - ch/2, min(cy + ch/2, sy))
        else:
            sy = cy + (ch/2) * (1 if math.sin(angle) > 0 else -1)
            sx = cx + ((ch/2) * math.cos(angle) / math.sin(angle)) if math.sin(angle) != 0 else cx
            sx = max(cx - cw/2, min(cx + cw/2, sx))
        # точка контакта на блоке-категории
        ex = bx - (bw/2) * math.cos(angle) * 0.9
        ey = by - (bh/2) * math.sin(angle) * 0.9
        svg += line(sx, sy, ex, ey, stroke=GREY, sw=1.2)
        # сам блок
        svg += rect(bx - bw/2, by - bh/2, bw, bh, fill=BG, stroke=ACCENT, sw=1.5, rx=6)
        # заголовок
        svg += text(bx, by - bh/2 + 20, head, size=12, weight="bold", fill=ACCENT)
        # элементы
        for j, it in enumerate(items):
            svg += text(bx, by - bh/2 + 40 + j*15, it, size=11)

    svg += svg_close()
    open(f"{OUT}/risunok_1_1_1.svg", "w", encoding="utf-8").write(svg)
    return svg


# ========================================================================
# Рисунок 1.3.1 — Схема межбанковского перевода через ПС БР
# ========================================================================

def fig_1_3_1():
    W, H = 1100, 600
    svg = svg_open(W, H) + arrow_def()
    svg += title(W/2, 30, "Рисунок 1.3.1 – Схема прохождения межбанковского перевода через ПС БР")

    # Колонки: Плательщик → Банк-отправитель → ПС БР → Банк-получатель → Получатель
    blocks = [
        (60,  220, 160, 100, ["ПЛАТЕЛЬЩИК", "(клиент 1)"], LIGHT),
        (260, 200, 180, 140, ["БАНК-", "ОТПРАВИТЕЛЬ", "(АБС)"], "#D9EAF7"),
        (480, 130, 200, 280, ["ПЛАТЁЖНАЯ", "СИСТЕМА БАНКА", "РОССИИ", "", "Сервисы:", "СС / НС / СБП"], "#FFF3CD"),
        (720, 200, 180, 140, ["БАНК-", "ПОЛУЧАТЕЛЬ", "(АБС)"], "#D9EAF7"),
        (940, 220, 140, 100, ["ПОЛУЧАТЕЛЬ", "(клиент 2)"], LIGHT),
    ]
    for x, y, w, h, lines, fill in blocks:
        svg += box(x, y, w, h, lines, fill=fill, sw=1.5, weight="bold", size=12)

    # Стрелки между ними и подписи
    arrows = [
        (220, 270, 260, 270, "1. Поручение"),
        (440, 270, 480, 270, "2. Платёжное\nсообщение\nISO 20022"),
        (680, 270, 720, 270, "3. Платёжное\nсообщение"),
        (900, 270, 940, 270, "4. Зачисление"),
    ]
    for x1, y1, x2, y2, lbl in arrows:
        svg += arrow(x1, y1, x2, y2, stroke=ACCENT, sw=2)
        for i, ln in enumerate(lbl.split("\n")):
            svg += text((x1+x2)/2, y1 - 18 - (len(lbl.split('\n'))-1-i)*14, ln, size=10, fill=ACCENT)

    # Обратные стрелки (подтверждения)
    rev = [
        (260, 320, 220, 320),
        (480, 320, 440, 320),
        (720, 320, 680, 320),
        (940, 320, 900, 320),
    ]
    for x1, y1, x2, y2 in rev:
        svg += arrow(x1, y1, x2, y2, stroke=GREY, sw=1.2)
    svg += text(W/2, 360, "← Уведомления о статусе и зачислении", size=11, fill=GREY, style="italic")

    # Внизу — этапы обработки в ПС БР
    svg += text(580, 470, "В платёжной системе Банка России:", size=12, weight="bold")
    svg += text(580, 490, "проверка реквизитов → клиринг → расчёт → отправка получателю", size=11, fill=GREY)

    # Снизу — пояснение к АБС
    svg += text(350, 410, "АМЛ-проверка, антифрод,", size=10, fill=GREY, style="italic")
    svg += text(350, 425, "списание со счёта", size=10, fill=GREY, style="italic")
    svg += text(810, 410, "АМЛ-проверка,", size=10, fill=GREY, style="italic")
    svg += text(810, 425, "зачисление на счёт", size=10, fill=GREY, style="italic")

    svg += svg_close()
    open(f"{OUT}/risunok_1_3_1.svg", "w", encoding="utf-8").write(svg)
    return svg


# ========================================================================
# Рисунок 1.3.2 — Архитектура национальной платёжной инфраструктуры РФ
# ========================================================================

def fig_1_3_2():
    W, H = 1100, 700
    svg = svg_open(W, H) + arrow_def()
    svg += title(W/2, 30, "Рисунок 1.3.2 – Архитектура национальной платёжной инфраструктуры РФ")

    # Уровень 1: ЦБ РФ (мегарегулятор)
    svg += box(W/2 - 220, 70, 440, 60, ["БАНК РОССИИ", "(мегарегулятор национальной платёжной системы)"],
               size=14, weight="bold", fill="#FFF3CD", sw=2)

    # Уровень 2: 4 платёжные системы
    systems = [
        (60,  200, ["ПС Банка", "России", "(ПС БР)"], "Сервисы СС, НС, СБП"),
        (300, 200, ["Система", "быстрых платежей", "(СБП)"], "Мгновенные переводы 24/7"),
        (560, 200, ["НСПК", "«Мир»", ""], "Карточные операции"),
        (820, 200, ["СПФС", "Банка России", ""], "Финансовые сообщения"),
    ]
    sys_w, sys_h = 220, 110
    for x, y, ls, sub in systems:
        svg += box(x, y, sys_w, sys_h, ls, fill="#D9EAF7", sw=1.5, weight="bold", size=12)
        svg += text(x + sys_w/2, y + sys_h + 18, sub, size=10, fill=GREY, style="italic")
        # стрелка от ЦБ
        svg += line(W/2, 130, x + sys_w/2, y, stroke=GREY, sw=1)

    # Уровень 3: Коммерческие банки
    bank_y = 410
    bank_w, bank_h = 920, 90
    svg += box((W - bank_w)/2, bank_y, bank_w, bank_h,
               ["КОММЕРЧЕСКИЕ БАНКИ – операторы по переводу денежных средств",
                "(ПАО «Сбербанк», ВТБ, Альфа-Банк, Газпромбанк, Россельхозбанк, Т-Банк и др.)"],
               size=13, weight="bold", fill="#E8F5E8", sw=1.5)

    # стрелки от каждой системы к коммерческим банкам
    for x, y, ls, sub in systems:
        svg += line(x + sys_w/2, y + sys_h + 20, x + sys_w/2, bank_y, stroke=GREY, sw=1)

    # Уровень 4: клиенты
    client_y = 560
    clients = [
        (W/2 - 360, client_y, ["Физические лица", "(110 млн чел.)"], "#F0F0F0"),
        (W/2 - 100, client_y, ["Юридические лица", "(3,2 млн орг.)"], "#F0F0F0"),
        (W/2 + 160, client_y, ["Государство", "(бюджет, фонды)"], "#F0F0F0"),
    ]
    for x, y, ls, fill in clients:
        svg += box(x, y, 200, 70, ls, size=12, weight="bold", fill=fill, sw=1.2)
        svg += line(x + 100, y, x + 100, bank_y + bank_h, stroke=GREY, sw=1)

    svg += text(W/2, H - 20,
                "↑ движение средств | ↓ платёжные распоряжения и идентификация",
                size=11, style="italic", fill=GREY)

    svg += svg_close()
    open(f"{OUT}/risunok_1_3_2.svg", "w", encoding="utf-8").write(svg)
    return svg


# ========================================================================
# Рисунок 2.1.1 — Динамика активов ПАО «Сбербанк» 2022-2024
# ========================================================================

def fig_2_1_1():
    W, H = 900, 600
    svg = svg_open(W, H)
    svg += title(W/2, 30, "Рисунок 2.1.1 – Динамика активов ПАО «Сбербанк» за 2022–2024 гг., млрд руб.")

    # координаты графика
    gx, gy = 110, 80
    gw, gh = 720, 440

    # оси
    svg += line(gx, gy, gx, gy + gh, stroke=FG, sw=1.5)
    svg += line(gx, gy + gh, gx + gw, gy + gh, stroke=FG, sw=1.5)

    # данные
    data = [(2022, 41726), (2023, 51687), (2024, 56822)]
    max_v = 60000
    # сетка по Y
    grid_steps = [0, 10000, 20000, 30000, 40000, 50000, 60000]
    for v in grid_steps:
        ypos = gy + gh - (v / max_v) * gh
        svg += line(gx, ypos, gx + gw, ypos, stroke=GRID, sw=0.7, dash="3,3")
        svg += text(gx - 8, ypos + 4, f"{v:,}".replace(",", " "), size=11, anchor="end")

    # столбцы
    bar_w = 130
    spacing = (gw - bar_w * 3) / 4
    for i, (year, val) in enumerate(data):
        bx = gx + spacing + i * (bar_w + spacing)
        bh = (val / max_v) * gh
        by = gy + gh - bh
        svg += rect(bx, by, bar_w, bh, fill=ACCENT2, stroke="#1A7A2D", sw=1.5)
        # значение
        svg += text(bx + bar_w/2, by - 10, f"{val:,}".replace(",", " "),
                    size=14, weight="bold", fill=ACCENT2)
        # год
        svg += text(bx + bar_w/2, gy + gh + 24, str(year), size=14, weight="bold")

    # подписи осей
    svg += text(gx + gw/2, H - 35, "Год", size=13, style="italic")
    svg += text(20, gy + gh/2, "млрд руб.", size=13, style="italic",
                anchor="middle")
    # повернуть подпись Y
    svg = svg.replace(
        f'<text x="20" y="{gy + gh/2}" text-anchor="middle" font-size="13" fill="#000000" font-weight="normal" font-style="italic">млрд руб.</text>',
        f'<text x="20" y="{gy + gh/2}" text-anchor="middle" font-size="13" fill="#000000" font-style="italic" transform="rotate(-90 20 {gy + gh/2})">млрд руб.</text>'
    )
    # Темп роста
    svg += text(W/2, H - 15, "Темп роста 2024 / 2022 = 136,2 %",
                size=12, fill=GREY, style="italic")

    svg += svg_close()
    open(f"{OUT}/risunok_2_1_1.svg", "w", encoding="utf-8").write(svg)
    return svg


# ========================================================================
# Рисунок 2.2.1 — Динамика количества переводов через СБП в Сбербанке
# ========================================================================

def fig_2_2_1():
    W, H = 900, 600
    svg = svg_open(W, H)
    svg += title(W/2, 30, "Рисунок 2.2.1 – Динамика количества переводов через СБП в ПАО «Сбербанк», млрд опер.")

    gx, gy = 110, 90
    gw, gh = 720, 420

    svg += line(gx, gy, gx, gy + gh, stroke=FG, sw=1.5)
    svg += line(gx, gy + gh, gx + gw, gy + gh, stroke=FG, sw=1.5)

    # квартальные данные из приложения Г (млн → переведём в млрд)
    quarters = [
        ("I'22", 0.853), ("II'22", 0.953), ("III'22", 1.094), ("IV'22", 1.464),
        ("I'23", 1.752), ("II'23", 2.115), ("III'23", 2.367), ("IV'23", 2.807),
        ("I'24", 2.652), ("II'24", 2.876), ("III'24", 3.036), ("IV'24", 3.244),
    ]
    max_v = 3.5
    grid_steps = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]
    for v in grid_steps:
        ypos = gy + gh - (v / max_v) * gh
        svg += line(gx, ypos, gx + gw, ypos, stroke=GRID, sw=0.7, dash="3,3")
        svg += text(gx - 8, ypos + 4, f"{v:.1f}", size=11, anchor="end")

    n = len(quarters)
    bar_w = (gw - 60) / n - 8
    points = []
    for i, (q, v) in enumerate(quarters):
        bx = gx + 30 + i * ((gw - 60) / n)
        bh = (v / max_v) * gh
        by = gy + gh - bh
        svg += rect(bx, by, bar_w, bh, fill="#9FCFEA", stroke=ACCENT, sw=1)
        svg += text(bx + bar_w/2, by - 6, f"{v:.2f}", size=10, fill=ACCENT)
        svg += text(bx + bar_w/2, gy + gh + 18, q, size=10)
        points.append((bx + bar_w/2, by))

    # годовые суммы
    yr_data = [(2022, 4.36), (2023, 9.04), (2024, 11.81)]
    yr_text = "Годовые итоги: 2022 – 4,36 млрд → 2023 – 9,04 млрд → 2024 – 11,81 млрд опер."
    svg += text(W/2, gy - 20, yr_text, size=12, fill=GREY, style="italic")
    svg += text(W/2, H - 35, "Квартал", size=13, style="italic")
    svg += text(20, gy + gh/2, "млрд опер.", size=13, style="italic",
                anchor="middle")
    svg = svg.replace(
        f'<text x="20" y="{gy + gh/2}" text-anchor="middle" font-size="13" fill="#000000" font-weight="normal" font-style="italic">млрд опер.</text>',
        f'<text x="20" y="{gy + gh/2}" text-anchor="middle" font-size="13" fill="#000000" font-style="italic" transform="rotate(-90 20 {gy + gh/2})">млрд опер.</text>'
    )
    svg += text(W/2, H - 15, "Темп роста 2024 / 2022 = 270,9 %",
                size=12, fill=GREY, style="italic")

    svg += svg_close()
    open(f"{OUT}/risunok_2_2_1.svg", "w", encoding="utf-8").write(svg)
    return svg


# ========================================================================
# Рисунок 2.2.2 — Структура комиссионных доходов от РКО
# ========================================================================

def fig_2_2_2():
    W, H = 1000, 650
    svg = svg_open(W, H)
    svg += title(W/2, 30,
        "Рисунок 2.2.2 – Структура комиссионных доходов ПАО «Сбербанк»")
    svg += title(W/2, 50, "от расчётно-кассового обслуживания и переводов в 2024 г.", size=14)

    cx, cy, r = 320, 350, 200

    segments = [
        ("Эквайринг",                        32.7, "#21A038"),
        ("РКО юр. лиц",                      27.8, "#1F6FB2"),
        ("Конверсионные операции",           12.9, "#F4A300"),
        ("Услуги ДБО",                       11.0, "#9B59B6"),
        ("Комиссии физ. лиц (вне СБП)",       8.2, "#E74C3C"),
        ("Трансграничные переводы",           4.2, "#1ABC9C"),
        ("Прочие операции",                   3.2, "#95A5A6"),
    ]

    # рисуем секторы
    start_angle = -math.pi / 2  # начинаем сверху
    for label, pct, color in segments:
        end_angle = start_angle + (pct / 100.0) * 2 * math.pi
        # путь сектора
        x1 = cx + r * math.cos(start_angle)
        y1 = cy + r * math.sin(start_angle)
        x2 = cx + r * math.cos(end_angle)
        y2 = cy + r * math.sin(end_angle)
        large = 1 if (end_angle - start_angle) > math.pi else 0
        path = f'M {cx} {cy} L {x1:.2f} {y1:.2f} A {r} {r} 0 {large} 1 {x2:.2f} {y2:.2f} Z'
        svg += f'<path d="{path}" fill="{color}" stroke="white" stroke-width="2"/>\n'
        # подпись % внутри сектора
        mid = (start_angle + end_angle) / 2
        tr = r * 0.65
        tx = cx + tr * math.cos(mid)
        ty = cy + tr * math.sin(mid)
        if pct >= 5:
            svg += text(tx, ty + 4, f"{pct:.1f}%", size=13, weight="bold", fill="#FFFFFF")
        start_angle = end_angle

    # легенда справа
    lx, ly = 600, 180
    svg += text(lx, ly - 20, "Структура (всего 436,5 млрд руб.):",
                size=14, weight="bold", anchor="start")
    for i, (label, pct, color) in enumerate(segments):
        yy = ly + i * 36
        svg += rect(lx, yy, 22, 22, fill=color, stroke=FG, sw=0.8)
        svg += text(lx + 32, yy + 16, f"{label} – {pct:.1f}%", size=13, anchor="start")
        # абс. значение
        abs_val = pct * 4.365
        svg += text(lx + 32, yy + 30, f"({abs_val:.1f} млрд руб.)", size=10, fill=GREY, anchor="start", style="italic")

    svg += svg_close()
    open(f"{OUT}/risunok_2_2_2.svg", "w", encoding="utf-8").write(svg)
    return svg


# ========================================================================
# Рисунок 2.3.1 — Дерево направлений совершенствования
# ========================================================================

def fig_2_3_1():
    W, H = 1200, 800
    svg = svg_open(W, H) + arrow_def()
    svg += title(W/2, 30,
        "Рисунок 2.3.1 – Дерево направлений совершенствования системы переводов ПАО «Сбербанк»")

    # центр
    cx, cy = W/2, H/2 + 20
    cw, ch = 280, 90
    svg += box(cx - cw/2, cy - ch/2, cw, ch,
               ["СОВЕРШЕНСТВОВАНИЕ", "СИСТЕМЫ ПЕРЕВОДОВ", "ПАО «СБЕРБАНК»"],
               size=14, weight="bold", fill="#FFF3CD", sw=2)

    directions = [
        ("1. Диверсификация",      ["монетизации:",   "премиум-тарифы,",   "кросс-продажи"],     "#21A038"),
        ("2. Модернизация",        ["платёжного шлюза:", "ISO 20022, in-memory,","антифрод-оптим."], "#1F6FB2"),
        ("3. Альтернативные",      ["трансграничные:", "СПФС, CIPS, БРИКС,", "цифровой рубль"],    "#F4A300"),
        ("4. Усиление",            ["безопасности:",   "поведенч. биометрия,","голосовой антифрод"],"#E74C3C"),
        ("5. Адаптация для",       ["слабо охваченных:", "«Лайт»-интерфейс,",  "доверенный клиент"], "#9B59B6"),
        ("6. Облачные технологии", ["и микросервисы:", "Kubernetes, ЦОДы,",  "Chaos Engineering"],  "#1ABC9C"),
        ("7. Цифровой рубль:",     ["смарт-контракты,","целевые выплаты,",   "B2B-сервисы"],         "#34495E"),
        ("8. Финансовая",          ["грамотность:",    "обучение, NPS,",     "снижение рисков"],     "#E67E22"),
    ]

    radius_x = 460
    radius_y = 280
    for i, (head, items, color) in enumerate(directions):
        angle = -math.pi/2 + i * (2*math.pi/8)
        bx = cx + radius_x * math.cos(angle)
        by = cy + radius_y * math.sin(angle)
        bw, bh = 220, 100
        # стрелка от центра
        svg += line(cx + (cw/2) * math.cos(angle), cy + (ch/2) * math.sin(angle),
                    bx - (bw/2) * math.cos(angle) * 0.85, by - (bh/2) * math.sin(angle) * 0.85,
                    stroke=GREY, sw=1.5)
        # блок
        svg += rect(bx - bw/2, by - bh/2, bw, bh, fill=BG, stroke=color, sw=2, rx=8)
        svg += text(bx, by - bh/2 + 22, head, size=13, weight="bold", fill=color)
        for j, it in enumerate(items):
            svg += text(bx, by - bh/2 + 42 + j*16, it, size=11)

    svg += svg_close()
    open(f"{OUT}/risunok_2_3_1.svg", "w", encoding="utf-8").write(svg)
    return svg


# Запускаем все
fig_1_1_1()
fig_1_3_1()
fig_1_3_2()
fig_2_1_1()
fig_2_2_1()
fig_2_2_2()
fig_2_3_1()

# Список созданных файлов
import os
for f in sorted(os.listdir(OUT)):
    full = os.path.join(OUT, f)
    print(f"  {f:<35} {os.path.getsize(full):>8} bytes")

print("\nВсе 7 рисунков успешно созданы!")
