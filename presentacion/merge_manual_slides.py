#!/usr/bin/env python3
"""
Splice the hand-made slides back into a freshly generated deck.

Why this exists
---------------
`build_pptx.py` draws 37 slides from code. The shipped deck has 40: three slides
were made **by hand** in PowerPoint (a branded cover, the agent-teams diagram, and
the application-architecture diagram) and cannot be regenerated from the script.

Before this script existed, re-running `build_pptx.py` silently destroyed those
three — the generator saves straight over `Claude_Code_Presentacion.pptx`. That is
a landmine: the deck looked regenerable and wasn't.

The three slides now live in `manual_slides.pptx` (extracted once, committed), and
the full deck is reproducible in two steps:

    python presentacion/build_pptx.py                     # 37 generated slides
    python presentacion/merge_manual_slides.py            # -> 40, manual slides restored

    python presentacion/build_pptx.py --lang en           # same layout, English strings
    python presentacion/merge_manual_slides.py --lang en  # -> 40, from manual_slides_EN.pptx

The English manual slides are a separate file because those three carry translated
headers of their own (same images, different text).

Idempotent: it always rebuilds the merge from `manual_slides.pptx`, so running it
twice is harmless.

Positions are 1-based, in the FINAL deck, and are declared in MANUAL_AT below.
If you add generated slides BEFORE one of these anchors, update the position.
"""
from __future__ import annotations

import copy
import io
import os
import sys

from pptx import Presentation

HERE = os.path.dirname(os.path.abspath(__file__))


def paths(lang: str) -> tuple[str, str]:
    """(generated deck, manual-slides source) for a language."""
    if lang == "es":
        return (os.path.join(HERE, "Claude_Code_Presentacion.pptx"),
                os.path.join(HERE, "manual_slides.pptx"))
    return (os.path.join(HERE, f"Claude_Code_Presentacion_{lang.upper()}.pptx"),
            os.path.join(HERE, f"manual_slides_{lang.upper()}.pptx"))

# (index in manual_slides.pptx, 1-based position in the final deck, label)
MANUAL_AT = [
    (0, 1, "branded cover"),
    (1, 18, "agent-teams diagram"),
    (2, 24, "application architecture"),
]


def copy_slide(src, dest_prs, layout):
    """Deep-copy one slide into dest_prs, preserving shape order (= z-order).

    Shapes are appended in source order; pictures are re-added from their blob so
    the image part and its relationship belong to the destination. Appending both
    kinds in the same pass is what keeps z-order identical — a picture added last
    would otherwise cover the text it sits behind.
    """
    dst = dest_prs.slides.add_slide(layout)
    for shp in list(dst.shapes):  # drop layout placeholders
        shp._element.getparent().remove(shp._element)

    for shp in src.shapes:
        if shp.shape_type == 13 or shp.__class__.__name__ == "Picture":
            dst.shapes.add_picture(
                io.BytesIO(shp.image.blob), shp.left, shp.top, shp.width, shp.height
            )
        else:
            dst.shapes._spTree.append(copy.deepcopy(shp._element))
    return dst


def move_slide(prs, from_idx, to_idx):
    """Move slide from_idx -> to_idx (both 0-based) in the slide id list."""
    ids = prs.slides._sldIdLst
    items = list(ids)
    ids.remove(items[from_idx])
    ids.insert(to_idx, items[from_idx])


def main(lang: str = "es") -> int:
    GENERATED, MANUAL = paths(lang)
    for path, what in ((GENERATED, "generated deck"), (MANUAL, "manual slides")):
        if not os.path.exists(path):
            print(f"ERROR: missing {what}: {path}", file=sys.stderr)
            if path == GENERATED:
                print(f"       run build_pptx.py --lang {lang} first", file=sys.stderr)
            return 1

    prs = Presentation(GENERATED)
    manual = Presentation(MANUAL)
    before = len(prs.slides._sldIdLst)

    if before != 37:
        print(
            f"WARNING: expected 37 generated slides, found {before}. "
            "If you added or removed slides in build_pptx.py, re-check MANUAL_AT "
            "positions below before trusting the output.",
            file=sys.stderr,
        )

    blank = prs.slide_layouts[6]
    for src_idx, target_pos, label in MANUAL_AT:
        src = manual.slides[src_idx]
        copy_slide(src, prs, blank)                      # lands at the end
        move_slide(prs, len(prs.slides._sldIdLst) - 1, target_pos - 1)
        print(f"  restored manual slide -> position {target_pos}  ({label})")

    prs.save(GENERATED)
    after = len(Presentation(GENERATED).slides._sldIdLst)
    print(f"OK  ->  {GENERATED}  ({before} generated + {len(MANUAL_AT)} manual = {after} slides)")
    return 0


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Reinserta las slides hechas a mano.")
    ap.add_argument("--lang", choices=("es", "en"), default="es")
    raise SystemExit(main(ap.parse_args().lang))
