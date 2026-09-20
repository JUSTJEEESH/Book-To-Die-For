#!/usr/bin/env python3
"""Build cover files.

  python3 06-cover/build_cover.py            -> concepts A/B/C front covers (PNG) + full paperback wrap PDF for the chosen direction
Paperback wrap: 7 x 10 trim, 254 pp cream (spine 0.635 in), 0.125 in bleed -> 14.885 x 10.25 in.
"""
import os, subprocess, shutil, html, argparse
ap = argparse.ArgumentParser()
ap.add_argument('--spine', type=float, default=0.635, help='spine width in inches (KDP calculator)')
ap.add_argument('--bleed', type=float, default=0.125, help='bleed per side in inches (0.125 paperback)')
ap.add_argument('--wrap', type=float, default=0.0, help='hardcover wrap-around per side in inches (KDP template), 0 for paperback')
ap.add_argument('--name', default='paperback-wrap', help='output file name')
ap.add_argument('--no-concepts', action='store_true')
ap.add_argument('--hardcover', action='store_true', help='build the KDP case-laminate wrap from the calculator numbers below')
ap.add_argument('--full-w', type=float, default=16.399); ap.add_argument('--full-h', type=float, default=11.417)
ap.add_argument('--panel-w', type=float, default=7.197); ap.add_argument('--panel-h', type=float, default=10.236)
ap.add_argument('--hinge', type=float, default=0.394); ap.add_argument('--margin', type=float, default=0.125)
ap.add_argument('--hc-spine', type=float, default=0.824); ap.add_argument('--hc-wrap', type=float, default=0.591)
ap.add_argument('--title', default='What I Want You to Know'); ap.add_argument('--tag', default='My stories. My memories. My words.')
ap.add_argument('--back', default=None, help='path to back cover copy text file'); ap.add_argument('--ink', default='#1e2838', help='ground color hex')
ap.add_argument('--out-dir', default=None, help='output folder (default 06-cover/build)')
args = ap.parse_args()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.abspath(args.out_dir) if args.out_dir else os.path.join(ROOT, '06-cover', 'build')
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
FONTS = open(os.path.join(ROOT, '05-interior', 'fonts', 'fonts.css')).read()
os.makedirs(OUT, exist_ok=True)
if os.path.isdir(os.path.join(OUT, 'fonts')): shutil.rmtree(os.path.join(OUT, 'fonts'))
shutil.copytree(os.path.join(ROOT, '05-interior', 'fonts'), os.path.join(OUT, 'fonts'))

TITLE = args.title
TAG = args.tag
AUTHOR = 'Joshua Caleb Green'
IMPRINT = 'Words to Keep'
BACK = open(args.back or os.path.join(ROOT, '06-cover', 'back-cover-copy.txt')).read().strip().split('\n\n')

INK = args.ink; CREAM = '#efe7d6'; BONE = '#f3efe6'; CHAR = '#1b1b1b'

BASE_CSS = FONTS + """
html,body{margin:0;padding:0;-webkit-print-color-adjust:exact;print-color-adjust:exact}
*{box-sizing:border-box}
.front{position:relative;width:7in;height:10in;overflow:hidden;display:flex;flex-direction:column;align-items:center;text-align:center}
.t{font-family:'Cormorant Garamond',serif;font-weight:600;text-transform:uppercase;letter-spacing:0.14em;line-height:1.12;margin:0}
.tag{font-family:'EB Garamond',serif;font-style:italic;margin:0}
.au{font-family:'EB Garamond',serif;font-variant:small-caps;letter-spacing:0.14em;margin:0}
.imp{font-family:'Inter',sans-serif;text-transform:uppercase;letter-spacing:0.26em;font-size:7.5pt;margin:0}
.rule{height:0.75pt;width:1.1in}
"""

def concept_a():
    return f"""<div class="front" style="background:{BONE};color:{CHAR};padding:1.6in 0.8in 0.7in">
  <p class="t" style="font-size:44pt">{TITLE}</p>
  <div class="rule" style="background:{CHAR};margin:0.42in 0 0.3in"></div>
  <p class="tag" style="font-size:16pt;color:#333">{TAG}</p>
  <p class="au" style="margin-top:auto;font-size:13pt">{AUTHOR}</p>
  <p class="imp" style="color:#666;margin-top:8pt">{IMPRINT}</p></div>"""

def rules_svg(color, opacity, n=7, w_in=5.4, top_in=6.35, pitch_in=0.36, left_in=0.8):
    lines = ''.join(f'<line x1="0" y1="{top_in + i*pitch_in}in" x2="{w_in}in" y2="{top_in + i*pitch_in}in" stroke="{color}" stroke-opacity="{opacity}" stroke-width="0.75"/>' for i in range(n))
    return f'<svg style="position:absolute;left:{left_in}in;top:0" width="{w_in}in" height="{top_in + n*pitch_in + 0.1}in">{lines}</svg>'

def concept_b(w=7.0, h=10.0, pad_x=0.8, pad_top=1.75, pad_bottom=0.7, title_pt=44):
    rw = w - 2*pad_x
    return f"""<div class="front" style="width:{w}in;height:{h}in;background:{INK};color:{CREAM};padding:{pad_top}in {pad_x}in {pad_bottom}in">
  {rules_svg(CREAM, 0.28, w_in=rw, top_in=h-3.65, left_in=pad_x)}
  <p class="t" style="font-size:{title_pt}pt;position:relative">{TITLE}</p>
  <div class="rule" style="background:{CREAM};opacity:0.8;margin:0.42in 0 0.3in"></div>
  <p class="tag" style="font-size:16pt;opacity:0.92">{TAG}</p>
  <p class="au" style="margin-top:auto;font-size:13pt;position:relative">{AUTHOR}</p>
  <p class="imp" style="opacity:0.7;margin-top:8pt;position:relative">{IMPRINT}</p></div>"""

def concept_c():
    return f"""<div class="front" style="background:{BONE};color:{CHAR};padding:1.55in 0.8in 0.7in">
  {rules_svg('#555', 0.45, n=8, top_in=5.9)}
  <p class="t" style="font-size:44pt;position:relative">{TITLE}</p>
  <p class="tag" style="font-size:16pt;color:#333;margin-top:0.35in;position:relative">{TAG}</p>
  <p class="au" style="margin-top:auto;font-size:13pt;position:relative">{AUTHOR}</p>
  <p class="imp" style="color:#666;margin-top:8pt;position:relative">{IMPRINT}</p></div>"""

def render_png(name, body, w_in=7, h_in=10):
    p = os.path.join(OUT, f'_{name}.html')
    open(p, 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}body{{background:#888}}</style></head><body>{body}</body></html>')
    png = os.path.join(OUT, f'{name}.png')
    subprocess.run([CHROME, '--headless', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
                    f'--window-size={int(w_in*96)},{int(h_in*96)+87}', '--force-device-scale-factor=2',
                    f'--screenshot={png}', 'file://' + p], capture_output=True)
    os.remove(p); print(png)

# ---- concepts ----
if not args.no_concepts:
    render_png('concept-A-bone', concept_a())
    render_png('concept-B-ink', concept_b())
    render_png('concept-C-rules', concept_c())

# ---- full wrap for concept B (paperback by default; hardcover with --wrap and KDP's spine) ----
SPINE = args.spine; BLEED = args.bleed + args.wrap; W = 7 + SPINE + 7 + 2*BLEED; H = 10 + 2*BLEED
print(f'wrap: {W:.3f} x {H:.3f} in, spine {SPINE} in, edge allowance {BLEED} in per side')
back_ps = ''.join(f'<p class="bp{" lead" if i==0 else ""}{" last" if i==len(BACK)-1 else ""}">{html.escape(t)}</p>' for i, t in enumerate(BACK))
wrap = f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}
@page{{size:{W}in {H}in;margin:0}}
.wrap{{position:relative;width:{W}in;height:{H}in;background:{INK};color:{CREAM};overflow:hidden}}
.back{{position:absolute;left:{BLEED}in;top:{BLEED}in;width:7in;height:10in;padding:0.95in 0.85in 0.7in}}
.spine{{position:absolute;left:{BLEED+7}in;top:{BLEED}in;width:{SPINE}in;height:10in}}
.frontpos{{position:absolute;left:{BLEED+7+SPINE}in;top:{BLEED}in}}
.bp{{font-family:'EB Garamond',serif;font-size:12.6pt;line-height:1.5;margin:0 0 11pt 0;opacity:0.95;max-width:5.1in}}
.bp.lead{{font-family:'Cormorant Garamond',serif;font-weight:600;font-size:25pt;line-height:1.15;margin-bottom:22pt;opacity:1;max-width:4.6in}}
.bp.last{{font-family:'Cormorant Garamond',serif;font-weight:600;font-size:17pt;margin-top:20pt}}
.barcode{{position:absolute;right:{BLEED+0.35}in;bottom:{BLEED+0.35}in;width:2in;height:1.2in;background:#fff}}
.spine-text{{position:absolute;left:50%;top:0.55in;transform-origin:left top;transform:rotate(90deg) translateY(-50%);white-space:nowrap;display:flex;align-items:center;gap:0.35in}}
.spine .t{{font-size:17pt;letter-spacing:0.16em}}
.spine .au{{font-size:10.5pt}}
.spine-imp{{position:absolute;left:0;right:0;bottom:0.45in;text-align:center}}
.spine-imp .imp{{font-size:6.5pt;opacity:0.75}}
.backimp{{position:absolute;left:0.85in;bottom:0.55in}}
</style></head><body>
<div class="wrap">
  <div class="back">{back_ps}<div class="backimp"><p class="imp" style="opacity:0.7">{IMPRINT}</p></div></div>
  <div class="barcode"></div>
  <div class="spine"><div class="spine-text"><p class="t">{TITLE}</p><p class="au">{AUTHOR}</p></div><div class="spine-imp"><p class="imp">WTK</p></div></div>
  <div class="frontpos">{concept_b()}</div>
</div></body></html>"""
p = os.path.join(OUT, args.name + '.html'); open(p, 'w').write(wrap)
pdf = os.path.join(OUT, args.name + '.pdf')
subprocess.run([CHROME, '--headless', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer', f'--print-to-pdf={pdf}', 'file://' + p], capture_output=True)
print(pdf)


# ================= HARDCOVER (KDP case laminate) =================
if args.hardcover:
    FW, FH, PW, PH = args.full_w, args.full_h, args.panel_w, args.panel_h
    WR, HG, MG, SP = args.hc_wrap, args.hinge, args.margin, args.hc_spine
    # sanity: 2*wrap + 2*panel + spine == full width
    calc = 2*WR + 2*PW + SP
    assert abs(calc - FW) < 0.01, f'geometry mismatch: {calc:.3f} vs {FW}'
    back_x0, spine_x0, front_x0 = WR, WR + PW, WR + PW + SP
    face_w = PW - HG                     # visible board face, hinge excluded
    back_face_x0 = back_x0              # back face runs from wrap line to hinge
    front_face_x0 = front_x0 + HG       # front face starts after the hinge
    y0 = WR
    back_ps = ''.join(f'<p class="bp{" lead" if i==0 else ""}{" last" if i==len(BACK)-1 else ""}">{html.escape(t)}</p>' for i, t in enumerate(BACK))
    # barcode reserve: 2 x 1.2 in, 0.25 in from the hinge, 0.375 in above the bottom wrap line
    bc_right = back_x0 + PW - HG - 0.25
    bc_bottom = FH - WR - 0.375
    front = concept_b(w=face_w, h=PH, pad_x=0.62, pad_top=1.85, pad_bottom=0.75, title_pt=42)
    wrap = f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}
@page{{size:{FW}in {FH}in;margin:0}}
.wrap{{position:relative;width:{FW}in;height:{FH}in;background:{INK};color:{CREAM};overflow:hidden}}
.back{{position:absolute;left:{back_face_x0 + MG + 0.25}in;top:{y0 + MG + 0.7}in;width:{face_w - 2*MG - 0.5}in;height:{PH - 2*MG - 0.7}in}}
.spine{{position:absolute;left:{spine_x0}in;top:{y0}in;width:{SP}in;height:{PH}in}}
.frontpos{{position:absolute;left:{front_face_x0}in;top:{y0}in}}
.bp{{font-family:'EB Garamond',serif;font-size:12.6pt;line-height:1.5;margin:0 0 11pt 0;opacity:0.95;max-width:5.1in}}
.bp.lead{{font-family:'Cormorant Garamond',serif;font-weight:600;font-size:25pt;line-height:1.15;margin-bottom:22pt;opacity:1;max-width:4.6in}}
.bp.last{{font-family:'Cormorant Garamond',serif;font-weight:600;font-size:17pt;margin-top:20pt}}
.barcode{{position:absolute;left:{bc_right - 2.0}in;top:{bc_bottom - 1.2}in;width:2in;height:1.2in;background:#fff}}
.spine-text{{position:absolute;left:50%;top:0.55in;transform-origin:left top;transform:rotate(90deg) translateY(-50%);white-space:nowrap;display:flex;align-items:center;gap:0.35in}}
.spine .t{{font-size:17pt;letter-spacing:0.16em}}
.spine .au{{font-size:10.5pt}}
.spine-imp{{position:absolute;left:0;right:0;bottom:0.45in;text-align:center}}
.spine-imp .imp{{font-size:6.5pt;opacity:0.75}}
.backimp{{position:absolute;left:0;bottom:0.15in}}
</style></head><body>
<div class="wrap">
  <div class="back">{back_ps}<div class="backimp"><p class="imp" style="opacity:0.7">{IMPRINT}</p></div></div>
  <div class="barcode"></div>
  <div class="spine"><div class="spine-text"><p class="t">{TITLE}</p><p class="au">{AUTHOR}</p></div><div class="spine-imp"><p class="imp">WTK</p></div></div>
  <div class="frontpos">{front}</div>
</div></body></html>"""
    p = os.path.join(OUT, 'hardcover-wrap.html'); open(p, 'w').write(wrap)
    pdf = os.path.join(OUT, 'hardcover-wrap.pdf')
    subprocess.run([CHROME, '--headless', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer', f'--print-to-pdf={pdf}', 'file://' + p], capture_output=True)
    print(f'hardcover wrap: {FW} x {FH} in; back face x {back_face_x0:.3f}-{back_face_x0+face_w:.3f}; spine x {spine_x0:.3f}-{spine_x0+SP:.3f}; front face x {front_face_x0:.3f}-{front_face_x0+face_w:.3f}')
    print(pdf)
