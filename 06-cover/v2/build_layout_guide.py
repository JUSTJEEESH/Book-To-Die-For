#!/usr/bin/env python3
"""Cover v2 layout guide for WHAT I WANT YOU TO KNOW (image-led cover).

Renders the paperback and hardcover wraps with every piece of type in its final
position, over placeholder art (or real art with --art), plus an annotated
guide version with trim, spine, safe-zone and barcode boxes drawn on.

  python3 06-cover/v2/build_layout_guide.py                 # placeholder art, guides on and off
  python3 06-cover/v2/build_layout_guide.py --art front.png # drop the generated front art in
"""
import os, subprocess, shutil, html, argparse
ap = argparse.ArgumentParser()
ap.add_argument('--art', default=None, help='front cover art (png/jpg), 7:10 or taller; fills the front panel plus bleed')
ap.add_argument('--out-dir', default=None)
ap.add_argument('--spine', type=float, default=0.635)        # 254 pp cream, KDP calculator
ap.add_argument('--no-pdf', action='store_true')
args = ap.parse_args()
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.abspath(args.out_dir) if args.out_dir else os.path.join(HERE, 'build')
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
os.makedirs(OUT, exist_ok=True)
if os.path.isdir(os.path.join(OUT, 'fonts')): shutil.rmtree(os.path.join(OUT, 'fonts'))
shutil.copytree(os.path.join(HERE, 'fonts'), os.path.join(OUT, 'fonts'))
ART = None
if args.art:
    ART = os.path.join(OUT, 'front-art' + os.path.splitext(args.art)[1]); shutil.copy(args.art, ART)

TITLE = 'What I Want<br>You to Know'; TAG = 'My stories. My memories. My words.'
DESC = 'A guided legacy journal for parents and grandparents'
AUTHOR = 'Joshua Caleb Green'; IMPRINT = 'Words to Keep'
BACK = open(os.path.join(ROOT, '06-cover', 'back-cover-copy.txt')).read().strip().split('\n\n')
NAVY = '#1e2838'; CREAM = '#efe7d6'

CSS = """
@font-face{font-family:'Playfair';src:url('fonts/PlayfairDisplay[wght].ttf');font-weight:400 900}
@font-face{font-family:'EB Garamond';src:url('fonts/EBGaramond-500-normal.ttf');font-weight:500}
@font-face{font-family:'EB Garamond';src:url('fonts/EBGaramond-400-italic.ttf');font-style:italic}
@font-face{font-family:'Inter';src:url('fonts/Inter-500-normal.ttf');font-weight:500}
html,body{margin:0;padding:0;-webkit-print-color-adjust:exact;print-color-adjust:exact}
*{box-sizing:border-box}
.wrap{position:relative;overflow:hidden;background:%(navy)s;color:%(cream)s}
.abs{position:absolute}
.title{font-family:'Playfair',serif;font-weight:700;text-transform:uppercase;letter-spacing:0.04em;line-height:1.08;margin:0;text-align:center;text-shadow:0 0 18px rgba(10,16,28,.55),0 2px 6px rgba(10,16,28,.5)}
.tag{font-family:'EB Garamond',serif;font-style:italic;margin:0;text-align:center;text-shadow:0 1px 8px rgba(10,16,28,.6)}
.au{font-family:'EB Garamond',serif;font-weight:500;font-variant:small-caps;letter-spacing:0.14em;margin:0;text-align:center;text-shadow:0 1px 8px rgba(10,16,28,.6)}
.desc{font-family:'Inter',sans-serif;font-weight:500;text-transform:uppercase;letter-spacing:0.22em;margin:0;text-align:center;opacity:.9;text-shadow:0 1px 8px rgba(10,16,28,.6)}
.imp{font-family:'Inter',sans-serif;font-weight:500;text-transform:uppercase;letter-spacing:0.26em;font-size:7.5pt;margin:0;opacity:.75}
.bp{font-family:'EB Garamond',serif;font-weight:500;font-size:12.5pt;line-height:1.5;margin:0 0 11pt 0;opacity:.94}
.bp.lead{font-family:'Playfair',serif;font-weight:700;font-size:23pt;line-height:1.18;margin-bottom:20pt;opacity:1}
.bp.last{font-family:'Playfair',serif;font-weight:700;font-size:15.5pt;margin-top:18pt}
.scrim{background:linear-gradient(to bottom,rgba(12,18,30,.62) 0%%,rgba(12,18,30,.45) 22%%,rgba(12,18,30,0) 42%%)}
.spine-text{position:absolute;left:50%%;top:0.55in;transform-origin:left top;transform:rotate(90deg) translateY(-50%%);white-space:nowrap;display:flex;align-items:center;gap:0.35in}
.spine .title{font-size:15pt;letter-spacing:0.08em;text-shadow:none}
.spine .au{font-size:10pt;text-shadow:none}
.spine-foot{position:absolute;left:50%%;bottom:0.45in;transform:translateX(-50%%);font-family:'Playfair',serif;font-weight:700;font-size:9pt;opacity:.75}
/* guides */
.g{position:absolute;pointer-events:none}
.g.line{background:#ff3b3b}
.g.box{border:1.5px dashed #ffd23b}
.g.safe{border:1.5px dashed #4cff9a}
.g.lab{font:500 8pt Inter,sans-serif;color:#fff;background:rgba(0,0,0,.75);padding:2px 5px;white-space:nowrap}
""" % dict(navy=NAVY, cream=CREAM)

def placeholder_art(w, h):
    """A stand-in painted scene: navy night above, a lamplit table with an open journal below."""
    return f"""<svg class="abs" style="left:0;top:0" width="{w}in" height="{h}in" viewBox="0 0 700 {int(h/w*700)}" preserveAspectRatio="xMidYMid slice">
<defs>
 <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#121a2a"/><stop offset=".45" stop-color="#1e2838"/><stop offset="1" stop-color="#3a2f22"/></linearGradient>
 <radialGradient id="lamp" cx=".56" cy=".62" r=".45"><stop offset="0" stop-color="#f2b25a" stop-opacity=".95"/><stop offset=".35" stop-color="#c7792e" stop-opacity=".55"/><stop offset="1" stop-color="#1e2838" stop-opacity="0"/></radialGradient>
 <linearGradient id="table" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a3523"/><stop offset="1" stop-color="#1a1410"/></linearGradient>
 <linearGradient id="page" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#e6d9bd"/><stop offset=".5" stop-color="#f4ecd8"/><stop offset="1" stop-color="#d9c9a8"/></linearGradient>
 <filter id="blur"><feGaussianBlur stdDeviation="14"/></filter>
</defs>
<rect width="700" height="1000" fill="url(#sky)"/>
<rect x="470" y="300" width="150" height="190" rx="4" fill="#0e1522"/>
<rect x="478" y="308" width="134" height="174" rx="2" fill="#243049"/>
<rect x="543" y="308" width="4" height="174" fill="#0e1522"/><rect x="478" y="392" width="134" height="4" fill="#0e1522"/>
<rect width="700" height="1000" fill="url(#lamp)"/>
<path d="M0 640 L700 600 L700 1000 L0 1000 Z" fill="url(#table)"/>
<ellipse cx="400" cy="660" rx="300" ry="120" fill="#f0a84a" opacity=".25" filter="url(#blur)"/>
<path d="M150 700 L350 690 L372 820 L140 835 Z" fill="url(#page)"/>
<path d="M350 690 L560 700 L572 835 L372 820 Z" fill="url(#page)"/>
<path d="M350 690 L372 820" stroke="#b9a785" stroke-width="2"/>
<g stroke="#5b5a6a" stroke-width="1.2" opacity=".55">
 <path d="M178 730 Q 230 722 300 726"/><path d="M182 748 Q 250 740 330 744"/><path d="M186 766 Q 240 760 290 762"/>
 <path d="M398 738 Q 440 730 520 736"/><path d="M402 756 Q 460 750 500 752"/>
</g>
<path d="M300 790 L470 760" stroke="#1b1712" stroke-width="9" stroke-linecap="round"/>
<path d="M300 790 L470 760" stroke="#2d2622" stroke-width="5" stroke-linecap="round"/>
<circle cx="470" cy="760" r="3" fill="#d8b56b"/>
<g opacity=".9"><rect x="600" y="690" width="40" height="55" rx="2" fill="#f0e6cd" transform="rotate(8 620 717)"/><rect x="585" y="705" width="40" height="55" rx="2" fill="#e2d4b3" transform="rotate(-6 605 732)"/></g>
<rect width="700" height="1000" fill="#000" opacity="0"/>
</svg>"""

def front_panel(w, h, guides=False, title_pt=54, pad_x=0.55):
    """Front cover type over art, w x h inches (trim for paperback, board face for hardcover)."""
    art = (f'<img class="abs" src="{os.path.basename(ART)}" style="left:0;top:0;width:{w}in;height:{h}in;object-fit:cover">'
           if ART else placeholder_art(w, h))
    return f"""<div class="abs" style="left:0;top:0;width:{w}in;height:{h}in;overflow:hidden">
  {art}
  <div class="abs scrim" style="left:0;top:0;width:{w}in;height:{h}in"></div>
  <p class="title abs" style="left:{pad_x}in;right:{pad_x}in;top:0.85in;font-size:{title_pt}pt">{TITLE}</p>
  <p class="tag abs" style="left:0;right:0;top:2.72in;font-size:17pt">{TAG}</p>
  <p class="au abs" style="left:0;right:0;bottom:0.82in;font-size:14pt">{AUTHOR}</p>
  <p class="desc abs" style="left:0;right:0;bottom:0.52in;font-size:8pt">{DESC}</p>
</div>"""

def back_block(x, y, w, h):
    ps = ''.join(f'<p class="bp{" lead" if i==0 else ""}{" last" if i==len(BACK)-1 else ""}">{html.escape(t)}</p>' for i, t in enumerate(BACK))
    return f'<div class="abs" style="left:{x}in;top:{y}in;width:{w}in;height:{h}in">{ps}</div>'

def spine_block(x, y, w, h):
    return f"""<div class="abs spine" style="left:{x}in;top:{y}in;width:{w}in;height:{h}in">
  <div class="spine-text"><p class="title">{TITLE.replace('<br>', ' ')}</p><p class="au">{AUTHOR}</p></div>
  <div class="spine-foot">W</div></div>"""

def guide(x, y, w, h, kind, label=None, lab_dy=0.02):
    s = f'<div class="g {kind}" style="left:{x}in;top:{y}in;width:{w}in;height:{h}in"></div>'
    if label: s += f'<div class="g lab" style="left:{x+0.05}in;top:{y+lab_dy}in">{label}</div>'
    return s

def render(name, body, W, H):
    doc = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}@page{{size:{W}in {H}in;margin:0}}body{{background:#777}}</style></head><body>{body}</body></html>'
    p = os.path.join(OUT, name + '.html'); open(p, 'w').write(doc)
    png = os.path.join(OUT, name + '.png')
    subprocess.run([CHROME, '--headless', '--no-sandbox', '--disable-gpu', '--hide-scrollbars', f'--window-size={int(W*96)},{int(H*96)+87}',
                    '--force-device-scale-factor=1.5', f'--screenshot={png}', 'file://' + p], capture_output=True)
    if not args.no_pdf:
        pdf = os.path.join(OUT, name + '.pdf')
        subprocess.run([CHROME, '--headless', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer', f'--print-to-pdf={pdf}', 'file://' + p], capture_output=True)
    print(name, f'{W:.3f} x {H:.3f} in')

# ---------------- paperback: 7 x 10 trim, 0.125 bleed ----------------
TW, TH, BL, SP = 7.0, 10.0, 0.125, args.spine
W, H = TW*2 + SP + 2*BL, TH + 2*BL
def paperback(guides):
    g = ''
    if guides:
        g += guide(BL, BL, TW, TH, 'line', None).replace('class="g line"', 'class="g box"')
        g += guide(BL+TW+SP, BL, TW, TH, 'box', 'FRONT trim 7 x 10 in', 0.05)
        g += guide(BL, BL, TW, TH, 'box', 'BACK trim 7 x 10 in', 0.05)
        g += guide(BL+TW, 0, SP, H, 'box', None)
        g += guide(BL+TW+SP+0.5, BL+0.5, TW-1.0, TH-1.0, 'safe', 'safe zone (0.5 in inside trim)', 0.03)
        g += guide(BL+0.5, BL+0.5, TW-1.0, TH-1.0, 'safe', 'safe zone (0.5 in inside trim)', 0.03)
        g += guide(BL+TW-0.35-2.0, BL+TH-0.35-1.2, 2.0, 1.2, 'box', 'leave clear: KDP barcode 2 x 1.2 in', 0.45)
        g += f'<div class="g lab" style="left:{BL+TW+SP+0.1}in;top:{H-0.35}in">bleed 0.125 in all round; file {W:.3f} x {H:.3f} in = {round(W*300)} x {round(H*300)} px at 300 dpi</div>'
        g += f'<div class="g lab" style="left:{BL+TW+0.02}in;top:{H/2-1.3}in;transform:rotate(90deg);transform-origin:left top">spine {SP} in (254 pp cream)</div>'
    return f"""<div class="wrap" style="width:{W}in;height:{H}in">
  <div class="abs" style="left:{BL+TW+SP-0.3}in;top:0;width:{TW+BL+0.3}in;height:{H}in;overflow:hidden">
    <div class="abs" style="left:0.3in;top:0;width:{TW+BL}in;height:{H}in">{front_panel(TW+2*BL, TH+2*BL).replace('top:0.85in', f'top:{0.85+BL}in').replace('top:2.72in', f'top:{2.72+BL}in').replace('bottom:0.82in', f'bottom:{0.82+BL}in').replace('bottom:0.52in', f'bottom:{0.52+BL}in').replace(f'left:0;top:0;width:{TW+2*BL}in', f'left:-{BL}in;top:-{BL}in;width:{TW+2*BL}in', 1)}</div>
    <div class="abs" style="left:0;top:0;width:0.6in;height:{H}in;background:linear-gradient(to right,{NAVY} 0%,{NAVY} 50%,rgba(30,40,56,0) 100%)"></div>
  </div>
  {back_block(BL+0.85, BL+0.95, 5.1, TH-1.9)}
  <p class="imp abs" style="left:{BL+0.85}in;top:{BL+TH-0.62}in">{IMPRINT}</p>
  {spine_block(BL+TW, BL, SP, TH)}
  {g}
</div>"""
render('paperback-wrap-v2', paperback(False), W, H)
render('paperback-wrap-v2-GUIDE', paperback(True), W, H)

# ---------------- hardcover: KDP case laminate numbers (254 pp, 7 x 10) ----------------
FW, FH, PW, PH, HG, MG, HSP, WR = 16.399, 11.417, 7.197, 10.236, 0.394, 0.125, 0.824, 0.591
assert abs(2*WR + 2*PW + HSP - FW) < 0.01
face_w = PW - HG
back_x0, spine_x0, front_x0 = WR, WR + PW, WR + PW + HSP
front_face_x0 = front_x0 + HG
def hardcover(guides):
    g = ''
    if guides:
        g += guide(front_x0, WR, PW, PH, 'box', 'FRONT panel 7.197 x 10.236 (hinge 0.394 on the spine side)', 0.05)
        g += guide(back_x0, WR, PW, PH, 'box', 'BACK panel 7.197 x 10.236', 0.05)
        g += guide(spine_x0, 0, HSP, FH, 'box', None)
        g += guide(front_face_x0+0.5, WR+0.5, face_w-1.0, PH-1.0, 'safe', 'safe zone (0.5 in inside the board face)', 0.03)
        g += guide(back_x0+0.5, WR+0.5, face_w-1.0, PH-1.0, 'safe', 'safe zone', 0.03)
        g += guide(back_x0+face_w-0.25-2.0, FH-WR-0.375-1.2, 2.0, 1.2, 'box', 'leave clear: barcode 2 x 1.2 in', 0.45)
        g += f'<div class="g lab" style="left:{front_face_x0+0.1}in;top:{FH-0.4}in">wrap 0.591 in all round; file 16.399 x 11.417 in = 4920 x 3425 px at 300 dpi</div>'
        g += f'<div class="g lab" style="left:{spine_x0+0.05}in;top:{FH/2-1.6}in;transform:rotate(90deg);transform-origin:left top">spine 0.824 in (safe 0.699 x 9.986)</div>'
    art_w, art_h = FW - front_x0, FH   # art fills from the spine edge to the outer wrap edge, full height
    fp = front_panel(art_w, art_h, title_pt=52)
    # re-centre the type on the visible board face (hinge excluded, wrap excluded)
    fp = fp.replace('top:0.85in', f'top:{WR+0.85}in').replace('top:2.72in', f'top:{WR+2.72}in').replace('bottom:0.82in', f'bottom:{WR+0.82}in').replace('bottom:0.52in', f'bottom:{WR+0.52}in')
    fp = fp.replace('left:0.55in;right:0.55in', f'left:{HG+0.5}in;right:{WR+0.5}in').replace('left:0;right:0', f'left:{HG}in;right:{WR}in')
    return f"""<div class="wrap" style="width:{FW}in;height:{FH}in">
  <div class="abs" style="left:{front_x0-0.3}in;top:0;width:{art_w+0.3}in;height:{FH}in;overflow:hidden">
    <div class="abs" style="left:0.3in;top:0;width:{art_w}in;height:{FH}in">{fp}</div>
    <div class="abs" style="left:0;top:0;width:{0.3+HG}in;height:{FH}in;background:linear-gradient(to right,{NAVY} 0%,{NAVY} 45%,rgba(30,40,56,0) 100%)"></div>
  </div>
  {back_block(back_x0+MG+0.5, WR+0.95, 5.1, PH-1.9)}
  <p class="imp abs" style="left:{back_x0+MG+0.5}in;top:{WR+PH-0.62}in">{IMPRINT}</p>
  {spine_block(spine_x0, WR, HSP, PH).replace('font-size:15pt', 'font-size:16pt')}
  {g}
</div>"""
render('hardcover-wrap-v2', hardcover(False), FW, FH)
render('hardcover-wrap-v2-GUIDE', hardcover(True), FW, FH)

# thumbnail test: the front at Amazon search size
subprocess.run(['convert', os.path.join(OUT, 'paperback-wrap-v2.png'), '-crop', f'{int((TW+BL)*96*1.5)}x{int(H*96*1.5)}+{int((BL+TW+SP)*96*1.5)}+0', '-resize', '160x', os.path.join(OUT, 'front-thumb-160.png')])
