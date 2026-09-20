# -*- coding: utf-8 -*-
"""Inji brand theme, taken from the official Inji deck template (June 2026)."""
import os
from pptx.dml.color import RGBColor
import deck_core, deck_blocks, deck_km

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')

INJI_ORANGE = RGBColor(0xF2, 0x7D, 0x21)
INJI_ORANGE_D = RGBColor(0xF2, 0x68, 0x0C)
INJI_PURPLE = RGBColor(0x6B, 0x21, 0xC8)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
ON_DARK = RGBColor(0xD6, 0xDF, 0xEC)
ON_DARK_DIM = RGBColor(0x92, 0xA4, 0xBE)
SANS = 'Montserrat'


def apply():
    C = deck_core.C
    # brand accents
    C['accent'] = INJI_ORANGE
    C['accent_l'] = RGBColor(0xFD, 0xEE, 0xE0)
    C['violet'] = INJI_PURPLE
    C['violet_l'] = RGBColor(0xEE, 0xE7, 0xFA)
    # the content canvas is the paper the body sits on
    C['bg'] = RGBColor(0xF7, 0xF9, 0xFB)
    C['surf'] = RGBColor(0xEE, 0xF1, 0xF6)
    C['surf2'] = RGBColor(0xDF, 0xE5, 0xEE)

    deck_core.THEME.update(
        bg_image=os.path.join(ASSETS, 'inji_bg.jpg'),
        logo=os.path.join(ASSETS, 'inji_logo.png'),
        rail=os.path.join(ASSETS, 'inji_rail.png'),
        mark=os.path.join(ASSETS, 'inji_mark.png'),
        canvas=True,
        canvas_fill=C['bg'],
        title_color=WHITE,
        sub_color=ON_DARK,
        sub_code_color=RGBColor(0xF6, 0xA8, 0x62),
        sub_strong_color=WHITE,
        kicker_color=INJI_ORANGE,
        footer_color=ON_DARK_DIM,
        title_italic=True,
        rule=False,
    )
    for m in (deck_core, deck_blocks, deck_km):
        m.F_SANS = SANS
