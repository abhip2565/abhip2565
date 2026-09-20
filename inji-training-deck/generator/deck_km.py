# -*- coding: utf-8 -*-
"""Extra diagram primitives for the Key Manager deep dive."""
from deck_blocks import *   # noqa


def node(slide, x, y, w, h, title, sub=None, fill=None, fg=None, border=None,
         tsize=11.5, ssize=8.5, adj=0.10, mono=False):
    fill = C['surf'] if fill is None else fill
    fg = C['ink'] if fg is None else fg
    s = rect(slide, x, y, w, h, fill=fill, line=border, lw=1.2,
             shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=adj)
    tf = s.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.06)
    tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER; p.line_spacing = 1.08
    r = p.add_run(); r.text = title
    r.font.size = Pt(tsize); r.font.bold = True
    r.font.name = F_MONO if mono else F_SANS; r.font.color.rgb = fg
    if sub:
        q = tf.add_paragraph(); q.alignment = PP_ALIGN.CENTER
        q.space_before = Pt(2); q.line_spacing = 1.1
        r2 = q.add_run(); r2.text = sub
        r2.font.size = Pt(ssize); r2.font.name = F_SANS
        r2.font.color.rgb = fg
    return s


def arrow(slide, x1, y1, x2, y2, color=None, lw=1.4, dash=None, label=None,
          lsize=8.2, lcolor=None, lside='above', lw_box=1.9):
    c = line(slide, x1, y1, x2, y2, color or C['ink2'], lw, dash=dash)
    arrowhead(c, tail=True)
    if label:
        mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0
        if lside == 'above':
            bx, by = mx - lw_box / 2, my - 0.30
        elif lside == 'below':
            bx, by = mx - lw_box / 2, my + 0.06
        elif lside == 'on':
            bx, by = mx - lw_box / 2, my - 0.13
        else:
            bx, by = mx + 0.10, my - 0.13
        rect(slide, bx, by, lw_box, 0.24, fill=C['white'])
        _, tf = tb(slide, bx, by, lw_box, 0.24, wrap=False, anchor=MSO_ANCHOR.MIDDLE)
        para(tf, label, size=lsize, color=lcolor or C['muted'], bold=True,
             align=PP_ALIGN.CENTER, first=True)
    return c


def zone(slide, x, y, w, h, label, color, tint=None, dash=True, lpos='tl'):
    rect(slide, x, y, w, h, fill=tint, line=color, lw=1.4,
         dash=2 if dash else None, shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.03)
    bw = min(w - 0.2, 0.26 + len(label) * 0.088)
    bx = x + 0.14 if lpos == 'tl' else x + w - bw - 0.14
    chip(slide, bx, y - 0.14, bw, 0.28, label, color, C['white'], size=8.6)


def lifecycle(slide, y, states, h=0.78, gap=0.30):
    n = len(states)
    bw = (CW - gap * (n - 1)) / n
    for i, (name, sub, col) in enumerate(states):
        x = ML + i * (bw + gap)
        node(slide, x, y, bw, h, name, sub, fill=col, fg=C['white'],
             tsize=10.5, ssize=8.0, adj=0.16)
        if i < n - 1:
            arrow(slide, x + bw + 0.04, y + h / 2, x + bw + gap - 0.04, y + h / 2,
                  C['ink2'], 1.4)
    return y + h


def timeline(slide, x, y, w, bars, years, hrow=0.52, vgap=0.52, xlabel="Y%d"):
    """bars = [(label, start_frac, end_frac, color, note, row)] — bars may share a row."""
    axis_y = y + 0.24
    line(slide, x, axis_y, x + w, axis_y, C['line'], 1.1)
    for i in range(years + 1):
        tx = x + w * i / years
        line(slide, tx, axis_y - 0.07, tx, axis_y + 0.07, C['faint'], 1.0)
        _, tf = tb(slide, tx - 0.40, y - 0.04, 0.80, 0.22, wrap=False)
        para(tf, xlabel % i, size=7.8, color=C['faint'], align=PP_ALIGN.CENTER, first=True)
    maxrow = max(bb[5] for bb in bars)
    for label, a_, b_, col, note, row in bars:
        cy = axis_y + 0.22 + row * vgap
        bx, bw2 = x + w * a_, max(w * (b_ - a_), 0.14)
        rect(slide, bx, cy, bw2, hrow - 0.16, fill=col,
             shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.24)
        if label:
            inside = bw2 > (len(label) * 0.062 + 0.22)
            if inside:
                _, tf = tb(slide, bx + 0.06, cy, bw2 - 0.12, hrow - 0.16,
                           wrap=False, anchor=MSO_ANCHOR.MIDDLE)
                para(tf, label, size=8.4, color=C['white'], bold=True,
                     align=PP_ALIGN.CENTER, first=True)
            else:
                _, tf = tb(slide, bx + bw2 / 2 - 1.30, cy - 0.26, 2.60, 0.22,
                           wrap=False, anchor=MSO_ANCHOR.MIDDLE)
                para(tf, label, size=8.2, color=col, bold=True,
                     align=PP_ALIGN.CENTER, first=True)
        if note:
            _, t2 = tb(slide, bx, cy + hrow - 0.15, max(bw2, 2.2), 0.24, wrap=False)
            para(t2, note, size=8.0, color=col, bold=True, first=True)
    return axis_y + 0.22 + (maxrow + 1) * vgap + 0.10


def kv_rows(slide, x, y, w, rows, ksize=9.0, vsize=9.0, pitch=0.30, kw=1.5):
    cy = y
    for k, v in rows:
        _, tf = tb(slide, x, cy, kw, 0.26, wrap=False)
        para(tf, k, size=ksize, color=C['muted'], bold=True, font=F_MONO, first=True)
        _, t2 = tb(slide, x + kw, cy, w - kw, 0.26)
        para(t2, v, size=vsize, color=C['ink2'], first=True)
        cy += pitch
    return cy
