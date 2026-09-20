# -*- coding: utf-8 -*-
"""Composite slide blocks: bullets, cards, the recurring architecture spine,
sequence diagrams, demo checkpoints, exercises, decision trees."""
from deck_core import *   # noqa

# ---------------------------------------------------------------- bullets
def bullets(slide, x, y, w, items, size=12.5, gap=0.085, bullet_col=None,
            lead=None, width_h=None):
    """items: str | (text, level) | (text, level, colorkey)"""
    bullet_col = bullet_col or C['accent']
    cy = y
    for it in items:
        lvl, colk = 0, None
        if isinstance(it, tuple):
            txt = it[0]
            lvl = it[1] if len(it) > 1 else 0
            colk = it[2] if len(it) > 2 else None
        else:
            txt = it
        ind = 0.0 if lvl == 0 else 0.30
        fs = size if lvl == 0 else size - 1.3
        col = C['ink'] if lvl == 0 else C['muted']
        bold = False
        if colk == 'strong':
            col = C['ink']; bold = True
        elif colk == 'warn':
            col = C['amber']
        elif colk == 'bad':
            col = C['red']
        elif colk == 'good':
            col = C['green']
        # estimate height
        mono_pen = 0.88 if '`' in txt else 1.0
        chars_per_line = int((w - ind - 0.26) * (72.0 / (fs * 0.505)) * 0.96 * mono_pen)
        nlines = max(1, -(-len(txt) // max(18, chars_per_line)))
        hgt = nlines * (fs / 72.0) * 1.26 + 0.02
        dot_y = cy + (fs / 72.0) * 0.52
        if lvl == 0:
            d = rect(slide, x + ind + 0.025, dot_y, 0.085, 0.085,
                     fill=bullet_col, shape=MSO_SHAPE.OVAL)
        else:
            d = rect(slide, x + ind + 0.04, dot_y + 0.028, 0.09, 0.028,
                     fill=C['faint'])
        _, tf = tb(slide, x + ind + 0.23, cy, w - ind - 0.23, hgt + 0.1)
        # inline bold via **..**
        parts = re.split(r'(\*\*[^*]+\*\*|`[^`]+`)', txt)
        chunks = []
        for pt in parts:
            if not pt:
                continue
            if pt.startswith('**'):
                chunks.append((pt[2:-2], col, True))
            elif pt.startswith('`'):
                chunks.append((pt[1:-1], C['primary'], False, False, F_MONO))
            else:
                chunks.append((pt, col, bold))
        rich(tf, chunks, size=fs, first=True, line_spacing=1.24)
        cy += hgt + gap
    return cy

def card(slide, x, y, w, h, title, items, accent=None, tint=None, size=10.5,
         tsize=12, icon=None):
    accent = accent or C['primary']
    tint = tint if tint is not None else C['surf']
    rect(slide, x, y, w, h, fill=tint, line=None, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
         adj=0.045)
    rect(slide, x, y, 0.055, h, fill=accent)
    _, tf = tb(slide, x + 0.26, y + 0.16, w - 0.42, 0.3)
    para(tf, title, size=tsize, color=accent, bold=True, first=True)
    cy = y + 0.16 + (tsize / 72.0) * 1.5
    if items:
        bullets(slide, x + 0.24, cy, w - 0.44, items, size=size, gap=0.065,
                bullet_col=accent)
    return y + h

def statcard(slide, x, y, w, h, big, label, accent=None, tint=None):
    accent = accent or C['primary']
    rect(slide, x, y, w, h, fill=tint if tint is not None else C['surf'],
         shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.08)
    _, tf = tb(slide, x + 0.12, y + 0.14, w - 0.24, h * 0.5)
    para(tf, big, size=19, color=accent, bold=True, align=PP_ALIGN.CENTER, first=True)
    _, tf2 = tb(slide, x + 0.10, y + h - 0.44, w - 0.2, 0.4)
    para(tf2, label, size=9, color=C['muted'], align=PP_ALIGN.CENTER, first=True)

def callout(slide, x, y, w, text, kind='note', h=None, size=10.5, title=None):
    pal = dict(note=(C['primary'], C['primary_l']), warn=(C['amber'], C['amber_l']),
               bad=(C['red'], C['red_l']), good=(C['green'], C['green_l']),
               tip=(C['accent'], C['accent_l']), spec=(C['violet'], C['violet_l']))
    fg, bgc = pal[kind]
    if h is None:
        cpl = int((w - 0.62) * (72.0 / (size * 0.505)) * 0.97)
        nl = max(1, -(-len(text) // max(20, cpl)))
        h = 0.20 + nl * (size / 72.0) * 1.3 + (0.22 if title else 0)
    rect(slide, x, y, w, h, fill=bgc, shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.09)
    rect(slide, x, y, 0.05, h, fill=fg)
    _, tf = tb(slide, x + 0.22, y + 0.10, w - 0.4, h - 0.16)
    parts = re.split(r'(\*\*[^*]+\*\*|`[^`]+`)', text)
    ch = []
    for pt in parts:
        if not pt:
            continue
        if pt.startswith('**'):
            ch.append((pt[2:-2], fg, True))
        elif pt.startswith('`'):
            ch.append((pt[1:-1], C['primary'], False, False, F_MONO))
        else:
            ch.append((pt, C['ink2'], False))
    if title:
        para(tf, title, size=size - 0.5, color=fg, bold=True, first=True)
        rich(tf, ch, size=size, line_spacing=1.22)
    else:
        rich(tf, ch, size=size, first=True, line_spacing=1.22)
    return y + h

# ---------------------------------------------------------------- the spine
SPINE = [
    ("Issuer",        "Inji Certify / national system"),
    ("Mimoto",        "wallet backend (BFF)"),
    ("Inji Wallet",   "holder app  |  Inji Web"),
    ("Credential\nStore", "encrypted, on device / DB"),
    ("Verifier",      "Inji Verify / relying party"),
]
SPINE_KEYS = ["issuer", "mimoto", "wallet", "store", "verifier"]

def spine(slide, y=2.25, highlight=(), big=True, show_web=True, labels=True):
    """The one recurring architecture diagram. highlight = list of SPINE_KEYS."""
    n = len(SPINE)
    gap = 0.66 if big else 0.42
    bw = (CW - gap * (n - 1)) / n
    bh = 1.05 if big else 0.72
    xs = []
    for i, (name, sub) in enumerate(SPINE):
        x = ML + i * (bw + gap)
        xs.append(x)
        on = SPINE_KEYS[i] in highlight
        fill = C['primary'] if on else C['surf']
        fg = C['white'] if on else C['ink2']
        bd = None if on else C['line']
        s = rect(slide, x, y, bw, bh, fill=fill, line=bd, lw=1.1,
                 shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.10)
        if on:
            rect(slide, x - 0.055, y - 0.055, bw + 0.11, bh + 0.11, fill=None,
                 line=C['accent'], lw=2.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.10)
        tf = s.text_frame; tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.06)
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = name.replace("\n", " ")
        r.font.size = Pt(13 if big else 11); r.font.bold = True
        r.font.name = F_SANS; r.font.color.rgb = fg
        if big:
            q = tf.add_paragraph(); q.alignment = PP_ALIGN.CENTER
            q.space_before = Pt(2)
            r2 = q.add_run(); r2.text = sub
            r2.font.size = Pt(8.5); r2.font.name = F_SANS
            r2.font.color.rgb = C['accent_l'] if on else C['muted']
    # arrows + protocol labels
    prot = ["OpenID4VCI", "stores", "OpenID4VP", "presents"]
    prot = ["OpenID4VCI", "downloads", "writes", "OpenID4VP"]
    for i in range(n - 1):
        x1 = xs[i] + bw; x2 = xs[i + 1]
        cy = y + bh / 2
        c = line(slide, x1 + 0.06, cy, x2 - 0.06, cy, C['ink2'], 1.5)
        arrowhead(c, tail=True)
        if labels and big:
            mid = (x1 + x2) / 2.0
            isprot = i in (0, 3)
            pw = 1.30 if isprot else 1.00
            chip(slide, mid - pw / 2, y - 0.40, pw, 0.27, prot[i],
                 C['accent_l'] if isprot else C['white'],
                 C['accent'] if isprot else C['muted'], size=8.2, bold=isprot,
                 border=C['accent'] if isprot else C['line'])
            line(slide, mid, y - 0.13, mid, cy - 0.02, C['line'], 0.9, dash=2)
    if show_web and big:
        # Inji Web attached under the holder tier
        wx = xs[2]
        wy = y + bh + 0.52
        on = 'web' in highlight
        s = rect(slide, wx, wy, bw, 0.6, fill=C['accent'] if on else C['white'],
                 line=C['accent'], lw=1.3, shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.16,
                 dash=None if on else 2)
        tf = s.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = "Inji Web  (browser holder)"
        r.font.size = Pt(10); r.font.bold = True; r.font.name = F_SANS
        r.font.color.rgb = C['white'] if on else C['accent']
        line(slide, wx + bw / 2, y + bh, wx + bw / 2, wy, C['accent'], 1.1, dash=2)
        # web -> mimoto
        c = line(slide, wx, wy + 0.3, xs[1] + bw / 2, wy + 0.3, C['accent'], 1.1, dash=2)
        line(slide, xs[1] + bw / 2, wy + 0.3, xs[1] + bw / 2, y + bh, C['accent'], 1.1, dash=2)
        _, tf = tb(slide, xs[1] + bw / 2 + 0.10, wy + 0.34, wx - xs[1] - bw / 2 - 0.2, 0.24)
        para(tf, "Inji Web uses Mimoto as its BFF", size=8, color=C['accent'],
             italic=True, align=PP_ALIGN.CENTER, first=True)
    return y + bh

def spine_strip(slide, y=6.42, highlight=()):
    """Thin 'you are here' version of the spine."""
    n = len(SPINE)
    gap = 0.30
    bw = (CW - gap * (n - 1)) / n
    bh = 0.34
    for i, (name, _) in enumerate(SPINE):
        x = ML + i * (bw + gap)
        on = SPINE_KEYS[i] in highlight
        chip(slide, x, y, bw, bh, name.replace("\n", " "),
             C['primary'] if on else C['surf'],
             C['white'] if on else C['faint'], size=9, bold=on,
             border=None if on else C['surf2'])
        if i < n - 1:
            c = line(slide, x + bw + 0.04, y + bh / 2, x + bw + gap - 0.04, y + bh / 2,
                     C['line'], 1.0)
            arrowhead(c, tail=True, size='sm')

# ---------------------------------------------------------------- section divider
def section(title, minutes, blurb, covers, highlight=(), num=None):
    s = new_slide(dark=True)
    STATE['section'] = title
    STATE['toc'].append((title, minutes, STATE['n']))
    rect(s, 0, 0, W, H, fill=C['dark'])
    rect(s, 0, 0, 0.18, H, fill=C['accent'])
    _, tf = tb(s, 1.0, 1.95, 7.2, 0.4)
    para(tf, ("SECTION %s" % num) if num else "SECTION", size=11,
         color=C['accent'], bold=True, first=True)
    _, tf = tb(s, 1.0, 2.38, 7.4, 1.3)
    para(tf, title, size=34, color=C['white'], bold=True, first=True, line_spacing=1.03)
    _, tf = tb(s, 1.0, 3.92, 7.0, 0.9)
    para(tf, blurb, size=12.5, color=RGBColor(0x9E, 0xB8, 0xCE), first=True,
         line_spacing=1.3)
    # timing badge
    b = rect(s, 9.4, 2.30, 2.9, 1.0, fill=C['dark2'], line=C['accent'], lw=1.2,
             shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.10)
    _, tf = tb(s, 9.5, 2.48, 2.7, 0.45)
    para(tf, minutes, size=22, color=C['white'], bold=True, align=PP_ALIGN.CENTER,
         first=True)
    _, tf = tb(s, 9.5, 2.95, 2.7, 0.3)
    para(tf, "teaching time", size=9, color=C['accent'], align=PP_ALIGN.CENTER,
         first=True)
    _, tf = tb(s, 9.4, 3.55, 3.0, 0.3)
    para(tf, "IN THIS SECTION", size=8.5, color=C['accent'], bold=True, first=True)
    cy = 3.86
    for ctext in covers:
        rect(s, 9.42, cy + 0.075, 0.07, 0.07, fill=C['accent'], shape=MSO_SHAPE.OVAL)
        _, tf = tb(s, 9.62, cy, 2.8, 0.30)
        para(tf, ctext, size=9.5, color=RGBColor(0xC6, 0xD6, 0xE4), first=True,
             line_spacing=1.15)
        cy += 0.295
    if highlight:
        n = len(SPINE); gap = 0.30
        bw = (CW - gap * (n - 1)) / n
        for i, (name, _) in enumerate(SPINE):
            x = ML + i * (bw + gap)
            on = SPINE_KEYS[i] in highlight
            chip(s, x, 6.30, bw, 0.36, name.replace("\n", " "),
                 C['accent'] if on else C['dark2'],
                 C['dark'] if on else RGBColor(0x5C, 0x78, 0x92), size=9, bold=on)
            if i < n - 1:
                c = line(s, x + bw + 0.04, 6.48, x + bw + gap - 0.04, 6.48,
                         RGBColor(0x2C, 0x48, 0x60), 1.0)
                arrowhead(c, tail=True, size='sm')
    footer(s, dark=True)
    return s

# ---------------------------------------------------------------- content slide
def slide(title, kicker=None, sub=None, hl=None):
    s = new_slide()
    y = head(s, title, kicker, sub)
    if hl:
        spine_strip(s, 6.42, hl)
    return s, y

# ---------------------------------------------------------------- sequence
LIFELINE = RGBColor(0x7C, 0x90, 0xA6)


def _label_width(txt, fs, numbered):
    """Approximate rendered width, in inches, of a marked-up label."""
    w = (4 if numbered else 0) * fs * 0.52 / 72.0
    for pt in re.split(r'(`[^`]+`|\*\*[^*]+\*\*)', txt):
        if not pt:
            continue
        if pt.startswith('`'):
            w += (len(pt) - 2) * fs * 0.615 / 72.0
        elif pt.startswith('**'):
            w += (len(pt) - 4) * fs * 0.565 / 72.0
        else:
            w += len(pt) * fs * 0.525 / 72.0
    return w


def _fit_label(txt, fs, numbered, avail):
    """Shrink the font until the label fits `avail` inches. Returns (font, width)."""
    w = _label_width(txt, fs, numbered)
    if w + 0.18 <= avail:
        return fs, w
    fs2 = max(6.4, fs * (avail - 0.18) / max(w, 0.01))
    return fs2, _label_width(txt, fs2, numbered)


def sequence(slide_, actors, steps, top=1.40, height=5.30, numbered=True,
             lane_colors=None, fsize=8.7):
    """Sequence diagram. steps: (from, to, label[, kind]) kind in req|resp|self|note."""
    n = len(actors)
    lw = CW / n
    cx = [ML + lw * (i + 0.5) for i in range(n)]
    bw = min(2.12, lw - 0.16)
    L, R = ML - 0.20, ML + CW + 0.20          # hard bounds for any label
    for i, a in enumerate(actors):
        col = (lane_colors or {}).get(i, C['primary'])
        sh = rect(slide_, cx[i] - bw / 2, top, bw, 0.42, fill=col,
                  shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.20)
        tf = sh.text_frame; tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.03)
        tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = a
        r.font.size = Pt(9.3); r.font.bold = True; r.font.name = F_SANS
        r.font.color.rgb = C['white']
        # lifeline: prominent, and anchored with a cap at each end
        line(slide_, cx[i], top + 0.42, cx[i], top + height, LIFELINE, 1.6, dash=2)
        rect(slide_, cx[i] - 0.05, top + 0.42, 0.10, 0.055, fill=LIFELINE)
        rect(slide_, cx[i] - 0.05, top + height - 0.055, 0.10, 0.055, fill=LIFELINE)
    y0 = top + 0.60
    usable = height - 0.68
    step = usable / max(1, len(steps))
    lab_h = min(0.30, max(0.16, step * 0.62))
    for k, st in enumerate(steps):
        a, b, txt = st[0], st[1], st[2]
        kind = st[3] if len(st) > 3 else 'req'
        yy = y0 + k * step
        ya = yy + step * 0.80
        if kind == 'note':
            nw = CW - 1.2
            fs2, _ = _fit_label(txt, fsize, False, nw - 0.30)
            rect(slide_, ML + 0.6, yy + 0.02, nw, min(step * 0.86, 0.30),
                 fill=C['amber_l'], shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.25)
            _, tf = tb(slide_, ML + 0.7, yy + 0.02, nw - 0.20,
                       min(step * 0.86, 0.30), wrap=False, anchor=MSO_ANCHOR.MIDDLE)
            para(tf, txt, size=fs2, color=C['amber'], bold=True, italic=True,
                 align=PP_ALIGN.CENTER, first=True)
            continue
        dashed = (kind == 'resp')
        fg = C['muted'] if dashed else C['primary']
        if kind == 'self':
            x = cx[a]
            rect(slide_, x, ya - 0.10, 0.26, 0.16, fill=None, line=C['ink2'], lw=1.0)
            c = line(slide_, x + 0.26, ya + 0.06, x + 0.02, ya + 0.06, C['ink2'], 1.0)
            arrowhead(c, tail=True, size='sm')
            room_r, room_l = R - (x + 0.34), (x - 0.06) - L
            avail = max(room_r, room_l)
            fs2, ew = _fit_label(txt, fsize, numbered, avail)
            boxw = min(ew + 0.18, avail)
            if room_r >= boxw:
                lx, la = x + 0.34, PP_ALIGN.LEFT
            else:
                lx, la = max(L, x - 0.06 - boxw), PP_ALIGN.RIGHT
        else:
            x1, x2 = cx[a], cx[b]
            sgn = 1 if x2 > x1 else -1
            c = line(slide_, x1 + sgn * 0.03, ya, x2 - sgn * 0.03, ya, fg, 1.4,
                     dash=2 if dashed else None)
            arrowhead(c, tail=True, size='sm')
            fs2, ew = _fit_label(txt, fsize, numbered, R - L)
            boxw = min(ew + 0.18, R - L)     # tight: never wider than the text needs
            mid = (x1 + x2) / 2.0
            lx = max(L, min(mid - boxw / 2, R - boxw))
            la = PP_ALIGN.CENTER
        # opaque mask, only as wide as the text, so lifelines stay visible either side
        rect(slide_, lx, yy + 0.005, boxw, lab_h, fill=C['white'])
        _, tf = tb(slide_, lx + 0.05, yy + 0.02, boxw - 0.10, lab_h,
                   wrap=False, anchor=MSO_ANCHOR.MIDDLE)
        ch = []
        if numbered:
            ch.append(("%d  " % (k + 1), C['accent'], True))
        for pt in re.split(r'(`[^`]+`|\*\*[^*]+\*\*)', txt):
            if not pt:
                continue
            if pt.startswith('`'):
                ch.append((pt[1:-1], C['primary'] if not dashed else C['muted'],
                           False, False, F_MONO))
            elif pt.startswith('**'):
                ch.append((pt[2:-2], C['ink'], True))
            else:
                ch.append((pt, C['ink2'] if not dashed else C['muted'], False))
        rich(tf, ch, size=fs2, align=la, first=True, line_spacing=1.0)


# ---------------------------------------------------------------- demo / exercise
def demo_slide(num, title, minutes, setup, show, behind, fail=None):
    s = new_slide()
    rect(s, 0, 0, W, 0.90, fill=C['accent'])
    _, tf = tb(s, ML, 0.20, 8.5, 0.34)
    para(tf, "DEMO CHECKPOINT %d   •   %s" % (num, minutes), size=10,
         color=C['accent_l'], bold=True, first=True)
    _, tf = tb(s, ML, 0.45, 9.6, 0.42)
    para(tf, title, size=20, color=C['white'], bold=True, first=True)
    y = 1.24
    ch = 4.18
    card(s, ML, y, 3.88, ch, "Before you start", setup, accent=C['primary'],
         tint=C['surf'], size=10.2)
    card(s, ML + 4.07, y, 3.88, ch, "What the room sees", show, accent=C['accent'],
         tint=C['accent_l'], size=10.2)
    card(s, ML + 8.14, y, 4.08, ch, "What is really happening", behind,
         accent=C['violet'], tint=C['violet_l'], size=10.2)
    if fail:
        callout(s, ML, y + ch + 0.24, CW, fail, kind='warn',
                title="If it breaks in front of the room", size=10.3)
    footer(s)
    return s

def exercise_slide(title, items, kicker="HANDS-ON"):
    s, y = slide(title, kicker=kicker)
    return s, y
