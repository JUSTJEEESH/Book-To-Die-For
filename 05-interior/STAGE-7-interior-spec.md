# STAGE 7 — KDP Interior Specification

**Status:** Built. `build/interior.pdf` is the print-ready interior (254 pages, 7 x 10 in, fonts embedded).
**Rebuild:** `python3 05-interior/build_interior.py` (reads `04-manuscript/MANUSCRIPT.md`, writes `build/interior.html` and `build/interior.pdf`).
**Preview pages:** `python3 05-interior/preview_pages.py OUTDIR 16 24 ...` renders single pages to PNG.

## KDP settings to select at upload

| Setting | Value |
|---|---|
| Trim size | 7 x 10 in (17.78 x 25.4 cm) |
| Interior | Black & white |
| Paper | Cream |
| Bleed | No bleed |
| Page count | 254 (even; last page is a verso) |
| Cover finish | Matte |
| Spine width (cream, 254 pp at 0.0025 in/page) | 0.635 in |
| Full cover file size (with 0.125 in bleed) | 14.885 x 10.25 in |

Hardcover (same interior file): KDP 7 x 10 case laminate. Spine width for hardcover is computed by
KDP's cover calculator; use it at upload time.

## Page geometry

| Element | Value |
|---|---|
| Page box | 7 x 10 in, no bleed |
| Top margin | 0.75 in |
| Bottom margin | 0.875 in (running foot sits at 0.42 in from the trim edge) |
| Inside (gutter) margin | 0.875 in (KDP minimum for 151–300 pages is 0.625 in) |
| Outside margin | 0.75 in |
| Text measure | 5.375 in |
| Writing rules | 9 mm pitch, 0.75 pt, 39% gray (#9c9c9c) |
| Rules per full prompt page | 23 |

## Typography

| Role | Face | Size / leading |
|---|---|---|
| Prompts | EB Garamond Medium | 21 / 25.6 pt |
| Sub-lines | EB Garamond Italic | 12.5 / 17.5 pt, 67% black |
| Part titles | Cormorant Garamond SemiBold | 40 / 42 pt |
| Part introductions, front matter | EB Garamond Regular | 13 / 19.5 pt and 12.5 / 18.75 pt |
| Special-page headings | Cormorant Garamond SemiBold | 27 pt |
| Quick-ones stems | EB Garamond Regular | 13.5 pt |
| Labels (family tree, slots) | Inter | 7–8 pt, letterspaced caps, gray |
| Running foot | EB Garamond, small caps for the part name, oldstyle figures | 10 / 9.5 pt |
| Marked-prompt sign | A 0.42 em ring, 1.1 pt stroke, before the prompt | |

Smallest text in the book: 7 pt slot labels on the family tree (decorative, not read continuously).
Smallest text meant to be read: 9.5 pt skip line and running foot.

All three typefaces are SIL Open Font License; embedding and commercial print use are permitted.

## Page hierarchy, as built

1. Half title (recto) · blank · title page (recto) · copyright · giver's page (recto) · blank
2. This book is yours (recto) · How to use this book · You can skip anything (recto) · If you only fill out ten pages · Contents (recto) · blank
3. Each part: opener on a recto; prompts one per page; spreads start on a verso; special two-page items start on a verso; quick ones; a question from your family; a photo page where the budget allows
4. Letters: each starts on a verso; the last letter runs four pages
5. In my own hand (recto) · For the one reading this · Anything else · blank

The build script inserts blank pages only where recto/verso alignment requires them (nine in total).

## Preflight checks passed

- `pdfinfo`: 254 pages, 504 x 720 pt (exactly 7 x 10 in)
- `pdffonts`: every font embedded and subset; no system-font fallbacks
- No content inside the 0.25 in safe zone from any trim edge except the running foot at 0.42 in (KDP requires 0.25 in minimum outside, 0.375 in + 0.25 in inside for this page count; both satisfied)
- Visual check of title, giver, opening letter, ten pages, contents, opener, prompt, marked prompt, family tree, spread, quick ones, family question, Part Six skip line, letter, in my own hand, reader page, blank pages

## Known limitations

- KDP prints on standard stock; gel pens may ghost. The copyright page and the how-to page both recommend a fine ballpoint or fine-tip pen.
- The gray rules are 39% black. On KDP's cream paper they print as a soft gray. If a proof shows them too faint, raise to 45% in `interior.css` (`.lines`, `.qlines`, `.slot-line`) and rebuild.
- Order a printed proof before publishing. It is the only reliable check of gutter comfort and rule darkness.
