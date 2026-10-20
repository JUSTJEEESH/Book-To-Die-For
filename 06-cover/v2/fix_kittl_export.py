#!/usr/bin/env python3
"""Fix a Kittl PDF export whose page size came out in pixels (1 px = 1 pt, i.e. 72 dpi).

Kittl writes the artboard's pixel size straight into the PDF page size, so a 4466 x 3075 px
artboard becomes a 62 x 43 in page and KDP's previewer shows a giant corner of the cover.
This scales the page by 72/300 so 300 px = 1 in. Vector text, CMYK and the image are untouched.

  python3.13 06-cover/v2/fix_kittl_export.py in.pdf out.pdf
"""
import sys
from pypdf import PdfReader, PdfWriter
src, out = sys.argv[1], sys.argv[2]
r = PdfReader(src); w = PdfWriter(); w.add_page(r.pages[0]); p = w.pages[0]
p.scale_by(72 / 300)
for box in ('cropbox', 'bleedbox', 'trimbox', 'artbox'):
    setattr(p, box, p.mediabox)
w.write(out)
print(f'{out}: {float(p.mediabox.width)/72:.3f} x {float(p.mediabox.height)/72:.3f} in')
