"""Builds the Fabio Media logo SVGs into brand/.

The mark is a camera viewfinder (four corners) around an F whose middle bar is
a play button. The wordmark is FABIO MEDIA. in Inter ExtraBold, converted to
outlines so the files look the same everywhere, with or without the font.

Run from the repository root:
    python3 tools/build-logo.py
Needs fontTools (pip install fonttools) and Inter ExtraBold installed.
"""
import pathlib

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "brand"
FONT = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"

WHITE, BLACK, ORANGE, DARK = "#f4f4f6", "#0a0a0c", "#ff5d3b", "#0a0a0c"

# The F is drawn on a 100x100 grid and scaled into the viewfinder.
F_SCALE = 0.70
F_SHIFT_X = 50 - 48 * F_SCALE   # centres the F's bounding box (x 18..78)
F_SHIFT_Y = 50 - 50 * F_SCALE   # centres the F's bounding box (y 12..88)

TEXT = "FABIO MEDIA"
TEXT_SIZE = 46          # in mark units; the mark is 100 tall
LETTER_SPACING = 2.2
GAP = 24                # between mark and wordmark


def mark(fg):
    """The viewfinder mark on a 100x100 grid, without a background."""
    corners = (f'<g fill="none" stroke="{fg}" stroke-width="5" stroke-linecap="square">'
               '<path d="M8.5 26V8.5H26"/><path d="M74 8.5h17.5V26"/>'
               '<path d="M91.5 74v17.5H74"/><path d="M26 91.5H8.5V74"/></g>')
    f = (f'<g transform="translate({F_SHIFT_X:.2f} {F_SHIFT_Y:.2f}) scale({F_SCALE})">'
         f'<rect x="18" y="12" width="14" height="76" fill="{fg}"/>'
         f'<rect x="18" y="12" width="60" height="14" fill="{fg}"/>'
         f'<path d="M38 38l28 15-28 15z" fill="{ORANGE}"/></g>')
    return corners + f


def wordmark_paths(fg, x0, baseline):
    """FABIO MEDIA. as outlined paths starting at x0; returns (svg, width)."""
    font = TTFont(FONT)
    glyphs = font.getGlyphSet()
    cmap = font.getBestCmap()
    upm = font["head"].unitsPerEm
    scale = TEXT_SIZE / upm
    x = x0
    parts = []
    for i, ch in enumerate(TEXT + "."):
        name = cmap[ord(ch)]
        pen = SVGPathPen(glyphs)
        glyphs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, x, baseline)))
        colour = ORANGE if ch == "." else fg
        d = pen.getCommands()
        if d:
            parts.append(f'<path d="{d}" fill="{colour}"/>')
        x += glyphs[name].width * scale + (LETTER_SPACING if i < len(TEXT) else 0)
    return "".join(parts), x - x0


def cap_height():
    font = TTFont(FONT)
    return font["OS/2"].sCapHeight * TEXT_SIZE / font["head"].unitsPerEm


def svg(width, height, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.1f} {height}" '
            f'role="img" aria-label="{title}"><title>{title}</title>{body}</svg>\n')


def main():
    OUT.mkdir(exist_ok=True)
    baseline = 50 + cap_height() / 2
    for name, fg in (("white", WHITE), ("black", BLACK)):
        (OUT / f"mark-{name}.svg").write_text(svg(100, 100, mark(fg), "Fabio Media"))
        words, width = wordmark_paths(fg, 100 + GAP, baseline)
        (OUT / f"logo-{name}.svg").write_text(svg(100 + GAP + width, 100, mark(fg) + words, "Fabio Media"))
    # Square icon on a dark tile, for favicons and profile pictures.
    tile = f'<rect width="100" height="100" rx="22" fill="{DARK}"/><g transform="translate(14 14) scale(.72)">{mark(WHITE)}</g>'
    (OUT / "icon-tile.svg").write_text(svg(100, 100, tile, "Fabio Media"))
    # Tiny sizes (browser tab): only the play-F, larger, because the corners would crowd it.
    small = (f'<rect width="100" height="100" rx="22" fill="{DARK}"/><g transform="translate(14 13) scale(.75)">'
             f'<rect x="18" y="12" width="16" height="76" fill="{WHITE}"/><rect x="18" y="12" width="60" height="16" fill="{WHITE}"/>'
             f'<path d="M40 40l30 16-30 16z" fill="{ORANGE}"/></g>')
    (OUT / "icon-small.svg").write_text(svg(100, 100, small, "Fabio Media"))
    print("wrote", ", ".join(sorted(p.name for p in OUT.glob("*.svg"))))


if __name__ == "__main__":
    main()
