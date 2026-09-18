#!/usr/bin/env python3
"""Build cover files.

  python3 06-cover/build_cover.py            -> concepts A/B/C front covers (PNG) + full paperback wrap PDF for the chosen direction
Paperback wrap: 7 x 10 trim, 250 pp cream (spine 0.625 in), 0.125 in bleed -> 14.875 x 10.25 in.
"""
import os, subprocess, shutil, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, '06-cover', 'build')
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
FONTS = open(os.path.join(ROOT, '05-interior', 'fonts', 'fonts.css')).read()
os.makedirs(OUT, exist_ok=True)
if os.path.isdir(os.path.join(OUT, 'fonts')): shutil.rmtree(os.path.join(OUT, 'fonts'))
shutil.copytree(os.path.join(ROOT, '05-interior', 'fonts'), os.path.join(OUT, 'fonts'))

TITLE = 'What I Want You to Know'
TAG = 'My stories. My memories. My words.'
AUTHOR = 'Joshua Caleb Green'
IMPRINT = 'Words to Keep'
BACK = open(os.path.join(ROOT, '06-cover', 'back-cover-copy.txt')).read().strip().split('\n\n')

INK = '#1e2838'; CREAM = '#efe7d6'; BONE = '#f3efe6'; CHAR = '#1b1b1b'

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

def rules_svg(color, opacity, n=7, w_in=5.4, top_in=6.35, pitch_in=0.36):
    lines = ''.join(f'<line x1="0" y1="{top_in + i*pitch_in}in" x2="{w_in}in" y2="{top_in + i*pitch_in}in" stroke="{color}" stroke-opacity="{opacity}" stroke-width="0.75"/>' for i in range(n))
    return f'<svg style="position:absolute;left:0.8in;top:0" width="{w_in}in" height="10in">{lines}</svg>'

def concept_b():
    return f"""<div class="front" style="background:{INK};color:{CREAM};padding:1.75in 0.8in 0.7in">
  {rules_svg(CREAM, 0.28)}
  <p class="t" style="font-size:44pt;position:relative">{TITLE}</p>
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
render_png('concept-A-bone', concept_a())
render_png('concept-B-ink', concept_b())
render_png('concept-C-rules', concept_c())

# ---- full paperback wrap for concept B ----
SPINE = 0.625; BLEED = 0.125; W = 7 + SPINE + 7 + 2*BLEED; H = 10 + 2*BLEED
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
p = os.path.join(OUT, 'paperback-wrap.html'); open(p, 'w').write(wrap)
pdf = os.path.join(OUT, 'paperback-wrap.pdf')
subprocess.run([CHROME, '--headless', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer', f'--print-to-pdf={pdf}', 'file://' + p], capture_output=True)
print(pdf)
