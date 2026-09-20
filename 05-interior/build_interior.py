#!/usr/bin/env python3
"""Build the print-ready interior PDF from 04-manuscript/MANUSCRIPT.md.

Usage:  python3 05-interior/build_interior.py [--html-only]
Output: 05-interior/build/interior.html and interior.pdf

Trim 7 x 10 in, no bleed. Every page is a fixed 7x10 box; recto/verso margins are set per page
by this script, so the PDF is exactly what KDP receives. Page 1 is a recto.
"""
import re, sys, os, html, subprocess, shutil

import argparse
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ap = argparse.ArgumentParser()
_ap.add_argument('--manuscript', default=os.path.join(ROOT, '04-manuscript', 'MANUSCRIPT.md'))
_ap.add_argument('--out', default=os.path.join(ROOT, '05-interior', 'build'))
_ap.add_argument('--html-only', action='store_true')
_ap.add_argument('--trim-w', type=float, default=7.0); _ap.add_argument('--trim-h', type=float, default=10.0)
_ap.add_argument('--extra-css', default=None)
_ap.add_argument('--lang', default='en')
_ap.add_argument('--photo-fill', action='store_true', help='use a photo page instead of a blank when a page is needed for recto/verso alignment inside the parts')
_args = _ap.parse_args()
_L = {
 'en': dict(family_h='A question from your family.', family_sub='Written by the person who gave you this book.', their_q='Their question',
            photo='For a photograph, a drawing, or anything else.', contd='(continued)', to='To', signed='Signed', date='Date',
            contents='Contents', index='Where to find things', tree='Family tree', tree2='And where it went', tree_sub2='Add anyone the boxes leave out. Draw lines however you like.',
            t_their='Their parents', t_gp='My grandparents', t_p='My parents', t_me='Me', t_sib='My brothers and sisters', t_oth='Others who counted as family',
            name='name', name_born='name, born', name_who='name, who they were', people='The important people', p_name='Name', p_who='Who they were to me', p_line="One line I'd want you to know",
            sayings='Family sayings', s_said='We always said', s_meant='What it meant', songs='The songs', so_title='Title, and who sang it', so_why='Why',
            recipe='The recipe', r_called="What it's called", r_who='Who taught it to me', r_in='What goes in it', r_how='How to make it', r_part="The part that isn't written down anywhere",
            decades='My life, a line at a time', dec=['Before I was ten','My teens','My twenties','My thirties','My forties','My fifties','My sixties','My seventies','After that','Now'],
            given_to='This book was given to', by='by', on='on', because='Because', self_intro='If you bought this book for yourself:', belongs='This book belongs to',
            parts={'PART ONE':'Part One','PART TWO':'Part Two','PART THREE':'Part Three','PART FOUR':'Part Four','PART FIVE':'Part Five','PART SIX':'Part Six','PART SEVEN':'Part Seven','PART EIGHT':'Part Eight','PART NINE':'Part Nine','PART TEN':'Part Ten','PART ELEVEN':'Part Eleven','PART TWELVE':'Part Twelve','PART THIRTEEN':'Part Thirteen'}),
 'es': dict(family_h='Una pregunta de tu familia.', family_sub='Escrita por la persona que te regaló este libro.', their_q='Su pregunta',
            photo='Para una fotografía, un dibujo o cualquier otra cosa.', contd='(continúa)', to='Para', signed='Firma', date='Fecha',
            contents='Contenido', index='Dónde encontrar cada cosa', tree='Árbol familiar', tree2='Y hacia dónde siguió', tree_sub2='Agrega a quien falte. Dibuja las líneas como quieras.',
            t_their='Sus padres', t_gp='Mis abuelos', t_p='Mis padres', t_me='Yo', t_sib='Mis hermanos y hermanas', t_oth='Otros que fueron familia',
            name='nombre', name_born='nombre, año', name_who='nombre, quién fue', people='Las personas importantes', p_name='Nombre', p_who='Quién fue para mí', p_line='Una línea que quiero que sepas de esta persona',
            sayings='Dichos de la familia', s_said='Lo que siempre decíamos', s_meant='Lo que quería decir', songs='Las canciones', so_title='Título, y quién la cantaba', so_why='Por qué',
            recipe='La receta', r_called='Cómo se llama', r_who='Quién me la enseñó', r_in='Lo que lleva', r_how='Cómo se hace', r_part='La parte que no está escrita en ningún lado',
            decades='Mi vida, una línea a la vez', dec=['Antes de los diez','Mi adolescencia','Mis veintes','Mis treintas','Mis cuarentas','Mis cincuentas','Mis sesentas','Mis setentas','Después','Ahora'],
            given_to='Este libro fue regalado a', by='por', on='el', because='Porque', self_intro='Si compraste este libro para ti:', belongs='Este libro pertenece a',
            parts={'PRIMERA PARTE':'Primera parte','SEGUNDA PARTE':'Segunda parte','TERCERA PARTE':'Tercera parte','CUARTA PARTE':'Cuarta parte','QUINTA PARTE':'Quinta parte','SEXTA PARTE':'Sexta parte','SÉPTIMA PARTE':'Séptima parte','OCTAVA PARTE':'Octava parte','NOVENA PARTE':'Novena parte','DÉCIMA PARTE':'Décima parte','UNDÉCIMA PARTE':'Undécima parte','DUODÉCIMA PARTE':'Duodécima parte','DECIMOTERCERA PARTE':'Decimotercera parte'}),
}[_args.lang]
MS = os.path.abspath(_args.manuscript)
OUT = os.path.abspath(_args.out)
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'

# ---------- parse ----------
def parse(path):
    items = []
    cur = None
    for raw in open(path, encoding='utf-8').read().split('\n'):
        line = raw.rstrip()
        if line.startswith('@@ '):
            if cur: items.append(cur)
            head = line[3:].strip()
            kind, _, rest = head.partition(' ')
            cur = {'kind': kind, 'arg': rest.strip(), 'lines': []}
        elif cur is not None:
            cur['lines'].append(line)
    if cur: items.append(cur)
    for it in items:
        ls = [l for l in it['lines']]
        while ls and not ls[0].strip(): ls.pop(0)
        while ls and not ls[-1].strip(): ls.pop()
        it['lines'] = ls
    return items

def esc(s): return html.escape(s, quote=False)

def paras(lines):
    out, buf = [], []
    for l in lines:
        if l.strip(): buf.append(l.strip())
        else:
            if buf: out.append(' '.join(buf)); buf = []
    if buf: out.append(' '.join(buf))
    return out

# ---------- page model ----------
class Page:
    def __init__(self, body, cls='', folio=True, part=None, spread_text=None):
        self.body = body; self.cls = cls; self.folio = folio; self.part = part
        self.num = None

pages = []
part_label = None      # e.g. "Part One"
part_title = None
skipline = None
contents = []          # (label, title, pagenum)
ten_targets = []       # prompt texts for "ten pages" lookup
prompt_index = {}      # prompt text -> page number
index_entries = []     # (part_title, text, page)
story_pages_list = []  # first page of each story spread

flows = []   # (start_page, n_pages, pdf_path)

def md_to_html(text):
    out = []; para = []; inlist = False
    def flush():
        nonlocal para
        if para: out.append('<p>' + esc(' '.join(para)) + '</p>'); para = []
    for line in text.split('\n'):
        l = line.rstrip()
        if l.startswith('## '):
            flush()
            if inlist: out.append('</ul>'); inlist = False
            out.append(f'<h2>{esc(l[3:])}</h2>')
        elif l.startswith('### '):
            flush(); out.append(f'<h3>{esc(l[4:])}</h3>')
        elif l.startswith('- '):
            flush()
            if not inlist: out.append('<ul>'); inlist = True
            out.append(f'<li>{esc(l[2:])}</li>')
        elif not l.strip():
            flush()
            if inlist: out.append('</ul>'); inlist = False
        else:
            if inlist: out.append('</ul>'); inlist = False
            para.append(l.strip())
    flush()
    if inlist: out.append('</ul>')
    html_ = '\n'.join(out)
    # bold **x**
    html_ = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_)
    return html_

def render_flow(path, label, title, start):
    W, H = _args.trim_w, _args.trim_h
    body = md_to_html(open(path, encoding='utf-8').read())
    fonts_css = open(os.path.join(ROOT, '05-interior', 'fonts', 'fonts.css'), encoding='utf-8').read().replace("url('fonts/", "url('" + os.path.join(ROOT, '05-interior', 'fonts') + "/")
    css = f"""{fonts_css}
@page {{ size: {W}in {H}in; margin: 0.75in 0.75in 0.875in 0.875in; counter-increment: page;
  @bottom-left {{ content: counter(page) "   " "{title}"; font-family: 'EB Garamond', serif; font-size: 10pt; color: #333; font-variant-numeric: oldstyle-nums; vertical-align: top; padding-top: 0; margin-bottom: 0.42in; }} }}
@page :right {{ margin: 0.75in 0.75in 0.875in 0.875in;
  @bottom-left {{ content: none; }}
  @bottom-right {{ content: "{title}" "   " counter(page); font-family: 'EB Garamond', serif; font-size: 10pt; color: #333; font-variant-numeric: oldstyle-nums; margin-bottom: 0.42in; }} }}
@page :left {{ margin: 0.75in 0.875in 0.875in 0.75in; }}
html {{ counter-reset: page {start - 1}; }}
body {{ margin: 0; font-family: 'EB Garamond', serif; font-size: 12.5pt; line-height: 1.5; color: #111; -webkit-print-color-adjust: exact; }}
.opener {{ padding-top: 1.35in; max-width: 5.2in; margin-bottom: 0.5in; }}
.part-label {{ font-family: 'Inter', sans-serif; font-weight: 500; font-size: 9pt; letter-spacing: 0.24em; text-transform: uppercase; color: #444; margin: 0 0 14pt 0; }}
h1 {{ font-family: 'Cormorant Garamond', serif; font-weight: 600; font-size: 40pt; line-height: 1.05; margin: 0 0 18pt 0; }}
h2 {{ font-family: 'Cormorant Garamond', serif; font-weight: 600; font-size: 22pt; line-height: 1.15; margin: 22pt 0 8pt 0; break-after: avoid; }}
h3 {{ font-family: 'EB Garamond', serif; font-weight: 600; font-size: 13pt; margin: 14pt 0 4pt 0; break-after: avoid; }}
p {{ margin: 0 0 9pt 0; max-width: 5.6in; orphans: 2; widows: 2; }}
ul {{ margin: 0 0 9pt 0; padding-left: 1.2em; max-width: 5.6in; }}
li {{ margin: 0 0 4pt 0; }}
strong {{ font-weight: 600; }}
"""
    doc_ = ('<!doctype html><html><head><meta charset="utf-8"><style>' + css + '</style></head><body>'
            f'<div class="opener"><p class="part-label">{esc(label)}</p><h1>{esc(title)}</h1></div>' + body + '</body></html>')
    hp = os.path.join(OUT, f'_flow_{start}.html'); os.makedirs(OUT, exist_ok=True)
    open(hp, 'w', encoding='utf-8').write(doc_)
    pdfp = os.path.join(OUT, f'_flow_{start}.pdf')
    subprocess.run([CHROME, '--headless', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer', f'--print-to-pdf={pdfp}', 'file://' + hp], capture_output=True)
    info = subprocess.run(['pdfinfo', pdfp], capture_output=True, text=True).stdout
    n = int(re.search(r'Pages:\s+(\d+)', info).group(1))
    return n, pdfp

def add(page):
    page.num = len(pages) + 1
    page.part = part_title
    pages.append(page)
    return page

def is_recto(): return (len(pages) + 1) % 2 == 1
def blank():
    add(Page('', 'blank', folio=False))
def _filler():
    # inside the parts, an alignment page can carry the photo caption instead of being empty
    if _args.photo_fill and part_title:
        add(photo_page())
    else:
        blank()
def ensure_recto():
    if not is_recto(): _filler()
def ensure_verso():
    if is_recto(): _filler()

def lines_block(extra_cls=''):
    return f'<div class="lines {extra_cls}"></div>'

def mark(m): return '<span class="mark" aria-hidden="true"></span>' if m else ''

def prompt_page(text, sub, marked, cont=False):
    b = '<div class="prompt-head">'
    if cont:
        b += f'<p class="cont">{esc(text)}<span class="contd"> {esc(_L["contd"])}</span></p>'
    else:
        b += f'<h2 class="prompt">{mark(marked)}{esc(text)}</h2>'
        if sub: b += f'<p class="sub">{esc(sub)}</p>'
    b += '</div>' + lines_block()
    if skipline and not cont:
        b += f'<p class="skipline">{esc(skipline)}</p>'
    return Page(b, 'prompt-page')

def opener_page(label, title, intro):
    b = f'<div class="opener"><p class="part-label">{esc(label)}</p><h1 class="part-title">{esc(title)}</h1>'
    b += '<div class="intro">' + ''.join(f'<p>{esc(p)}</p>' for p in intro) + '</div></div>'
    return Page(b, 'opener-page', folio=False)

def quick_page(heading, items, finish=False):
    b = f'<h2 class="quick-head">{esc(heading)}</h2><div class="quick">'
    for it in items:
        t = esc(it)
        b += f'<div class="qitem"><p class="stem">{t}</p><div class="qlines"></div></div>'
    b += '</div>'
    return Page(b, 'quick-page')

def family_page():
    b = (f'<div class="prompt-head"><h2 class="prompt">{esc(_L["family_h"])}</h2>'
         f'<p class="sub">{esc(_L["family_sub"])}</p></div>'
         f'<div class="family-q"><p class="label">{esc(_L["their_q"])}</p><div class="qlines two"></div></div>'
         + lines_block())
    return Page(b, 'prompt-page family-page')

def photo_page():
    return Page(f'<div class="photo-space"></div><p class="photo-cap">{esc(_L["photo"])}</p>', 'photo-page')

def slot(label, w='100%'):
    return f'<div class="slot" style="width:{w}"><div class="slot-line"></div><p class="slot-label">{esc(label)}</p></div>'

def family_tree_pages(instr):
    L = _L; nb = L['name_born']
    v = (f'<h2 class="sp-head">{esc(L["tree"])}</h2><p class="sp-instr">' + esc(instr) + '</p>'
         '<div class="tree">'
         f'<p class="tier">{esc(L["t_their"])}</p><div class="row">' + ''.join(slot(L['name']) for _ in range(4)) + '</div>'
         f'<p class="tier">{esc(L["t_gp"])}</p><div class="row">' + ''.join(slot(nb) for _ in range(4)) + '</div>'
         f'<p class="tier">{esc(L["t_p"])}</p><div class="row wide">' + slot(nb) + slot(nb) + '</div>'
         f'<p class="tier">{esc(L["t_me"])}</p><div class="row one">' + slot(nb) + '</div>'
         f'<p class="tier">{esc(L["t_sib"])}</p><div class="row">' + ''.join(slot(nb) for _ in range(4)) + '</div>'
         f'<p class="tier">{esc(L["t_oth"])}</p><div class="row">' + ''.join(slot(L['name_who']) for _ in range(4)) + '</div>'
         '</div>')
    t2 = {'en': ('Me, and the person I built a life with', 'Children', 'Grandchildren', 'And after that'), 'es': ('Yo, y la persona con quien hice mi vida', 'Hijos', 'Nietos', 'Y después')}[_args.lang]
    r = (f'<h2 class="sp-head">{esc(L["tree2"])}</h2><p class="sp-instr">{esc(L["tree_sub2"])}</p>'
         '<div class="tree">'
         f'<p class="tier">{esc(t2[0])}</p><div class="row wide">' + slot(nb) + slot(nb) + '</div>'
         f'<p class="tier">{esc(t2[1])}</p><div class="row">' + ''.join(slot(nb) for _ in range(4)) + '</div>'
         f'<p class="tier">{esc(t2[2])}</p><div class="row">' + ''.join(slot(nb) for _ in range(4)) + '</div><div class="row">' + ''.join(slot(nb) for _ in range(4)) + '</div>'
         f'<p class="tier">{esc(t2[3])}</p><div class="row">' + ''.join(slot('') for _ in range(4)) + '</div>'
         '</div>')
    return [Page(v, 'special-page'), Page(r, 'special-page')]

def important_people_pages(instr):
    def rows(n):
        s = ''
        for _ in range(n):
            s += (f'<div class="person"><div class="pl"><span class="pl-label">{esc(_L["p_name"])}</span><div class="slot-line"></div></div>'
                  f'<div class="pl"><span class="pl-label">{esc(_L["p_who"])}</span><div class="slot-line"></div></div>'
                  f'<div class="pl"><span class="pl-label">{esc(_L["p_line"])}</span><div class="slot-line"></div></div></div>')
        return s
    v = f'<h2 class="sp-head">{esc(_L["people"])}</h2><p class="sp-instr">' + esc(instr) + '</p><div class="people">' + rows(4) + '</div>'
    r = '<div class="people top">' + rows(5) + '</div>'
    return [Page(v, 'special-page'), Page(r, 'special-page')]

def sayings_page(instr):
    b = f'<h2 class="sp-head">{esc(_L["sayings"])}</h2><p class="sp-instr">' + esc(instr) + '</p><div class="sayings">'
    for _ in range(7):
        b += (f'<div class="saying"><div class="pl"><span class="pl-label">{esc(_L["s_said"])}</span><div class="slot-line"></div></div>'
              f'<div class="pl"><span class="pl-label">{esc(_L["s_meant"])}</span><div class="slot-line"></div></div></div>')
    b += '</div>'
    return Page(b, 'special-page')

def songs_page(instr):
    b = f'<h2 class="sp-head">{esc(_L["songs"])}</h2><p class="sp-instr">' + esc(instr) + '</p><div class="sayings">'
    for _ in range(7):
        b += (f'<div class="saying"><div class="pl"><span class="pl-label">{esc(_L["so_title"])}</span><div class="slot-line"></div></div>'
              f'<div class="pl"><span class="pl-label">{esc(_L["so_why"])}</span><div class="slot-line"></div></div></div>')
    b += '</div>'
    return Page(b, 'special-page')

def recipe_pages(instr):
    v = (f'<h2 class="sp-head">{esc(_L["recipe"])}</h2><p class="sp-instr">' + esc(instr) + '</p>'
         f'<div class="pl"><span class="pl-label">{esc(_L["r_called"])}</span><div class="slot-line"></div></div>'
         f'<div class="pl"><span class="pl-label">{esc(_L["r_who"])}</span><div class="slot-line"></div></div>'
         f'<p class="tier mt">{esc(_L["r_in"])}</p>' + lines_block('short'))
    r = (f'<p class="tier top">{esc(_L["r_how"])}</p>' + lines_block('') +
         f'<p class="tier mt">{esc(_L["r_part"])}</p><div class="qlines three"></div>')
    return [Page(v, 'special-page recipe'), Page(r, 'special-page recipe')]

def decades_page(instr):
    rows = _L['dec']
    b = f'<h2 class="sp-head">{esc(_L["decades"])}</h2><p class="sp-instr">' + esc(instr) + '</p><div class="decades">'
    for r in rows:
        b += f'<div class="pl"><span class="pl-label">{esc(r)}</span><div class="slot-line"></div></div>'
    b += '</div>'
    return Page(b, 'special-page decades-page')

def drawbox(caption='Drawn by', h='flex: 1 1 auto; min-height: 60mm'):
    return f'<div class="drawbox" style="{h}"><span class="draw-cap">{esc(caption)}</span></div>'

def cast_page():
    b = ('<div class="cast-fields">'
         '<div class="pl"><span class="pl-label">Name</span><div class="slot-line"></div></div>'
         '<div class="pl"><span class="pl-label">What they are</span><div class="slot-line"></div></div>'
         '<div class="pl"><span class="pl-label">What they always say</span><div class="slot-line"></div></div>'
         '<div class="pl"><span class="pl-label">The trouble they always get into</span><div class="slot-line"></div></div>'
         '<div class="pl"><span class="pl-label">Who they are secretly based on</span><div class="slot-line"></div></div>'
         '</div>' + drawbox('Drawn by', 'flex: 1 1 auto; min-height: 70mm; margin-top: 5mm'))
    return Page(b, 'special-page cast-page')

def places_page(instr):
    b = '<h2 class="sp-head">Where the stories happened</h2><p class="sp-instr">' + esc(instr) + '</p>' + drawbox('', 'height: 95mm') + '<div class="lines short" style="margin-top:6mm"></div>'
    return Page(b, 'special-page')

def startend_page(lines_):
    b = '<h2 class="sp-head">How we started, how we ended</h2><div style="margin-top:6mm">'
    for lab in [l.strip() for l in lines_ if l.strip()]:
        b += f'<p class="stem" style="font-size:14pt;margin:5mm 0 1mm 0">{esc(lab)}</p><div class="qlines three"></div>'
    b += '</div>'
    return Page(b, 'special-page')

def story_pages():
    left = ('<div class="story-head">'
            '<div class="pl"><span class="pl-label">Title</span><div class="slot-line big"></div></div>'
            '<div class="two-col" style="margin-top:2mm"><div class="pl"><span class="pl-label">First told</span><div class="slot-line"></div></div>'
            '<div class="pl"><span class="pl-label">Told to</span><div class="slot-line"></div></div></div>'
            '<div class="tally"><span class="pl-label">Times asked for</span><div class="boxes">' + ''.join('<span class="box"></span>' for _ in range(12)) + '</div></div>'
            '</div>' + lines_block())
    right = lines_block('full') + drawbox('Drawn by', 'height: 62mm; margin-top: 5mm')
    return [Page(left, 'prompt-page story-page'), Page(right, 'prompt-page story-page cont')]

def longstory_pages(heading, sub, n):
    out = []
    first = (f'<div class="prompt-head"><h2 class="prompt">{esc(heading)}</h2>' + (f'<p class="sub">{esc(sub)}</p>' if sub else '') + '</div>' + lines_block())
    out.append(Page(first, 'prompt-page'))
    for i in range(n - 1):
        body = lines_block('full') if i < n - 2 else (lines_block('full') + drawbox('Drawn by', 'height: 55mm; margin-top: 5mm'))
        out.append(Page(body, 'prompt-page cont'))
    return out

def lifepage(text, sub):
    b = '<div class="prompt-head">' + f'<h2 class="prompt">{esc(text)}</h2>' + (f'<p class="sub">{esc(sub)}</p>' if sub else '') + '</div>'
    b += '<div class="life-body"><div class="lines" style="margin-top:4mm"></div>' + drawbox('A photograph, if there is one', 'height: 58mm; margin-top: 5mm') + '</div>'
    return Page(b, 'prompt-page life-page')

def fields_page(heading, sub, items):
    b = f'<h2 class="sp-head">{esc(heading)}</h2>' + (f'<p class="sp-instr">{esc(sub)}</p>' if sub else '') + '<div class="fields">'
    for i, (label, n) in enumerate(items):
        grow = ' grow' if i == len(items) - 1 else ''
        b += f'<div class="field{grow}"><span class="pl-label">{esc(label)}</span><div class="qlines" style="height:{10*n}mm;min-height:{10*n}mm"></div></div>'
    b += '</div>'
    return Page(b, 'special-page fields-page')

def names_page(heading, sub):
    b = f'<h2 class="sp-head">{esc(heading)}</h2>' + (f'<p class="sp-instr">{esc(sub)}</p>' if sub else '') + '<div class="fields">'
    for _ in range(3):
        b += ('<div class="namegroup">'
              '<div class="two-col"><div class="pl"><span class="pl-label">Name</span><div class="slot-line"></div></div>'
              '<div class="pl"><span class="pl-label">Who they are to me</span><div class="slot-line"></div></div></div>'
              '<div class="pl"><span class="pl-label">Living, or not, and where</span><div class="slot-line"></div></div>'
              '<div class="field"><span class="pl-label">What we have agreed to say</span><div class="qlines" style="height:20mm"></div></div>'
              '</div>')
    b += '</div>'
    return Page(b, 'special-page fields-page')

def words_page(heading, sub):
    b = f'<h2 class="sp-head">{esc(heading)}</h2>' + (f'<p class="sp-instr">{esc(sub)}</p>' if sub else '') + '<div class="sayings">'
    for _ in range(8):
        b += ('<div class="saying"><div class="two-col"><div class="pl"><span class="pl-label">The word</span><div class="slot-line"></div></div>'
              '<div class="pl" style="flex:2 1 0"><span class="pl-label">What it means</span><div class="slot-line"></div></div></div></div>')
    b += '</div>'
    return Page(b, 'special-page')

def photogrid_page(heading):
    b = f'<h2 class="sp-head">{esc(heading)}</h2><div class="grid2">'
    for _ in range(4):
        b += ('<div class="gridcell">' + drawbox('', 'height: 62mm') +
              '<div class="pl"><span class="pl-label">Name</span><div class="slot-line"></div></div>'
              '<div class="pl"><span class="pl-label">Who, or where</span><div class="slot-line"></div></div></div>')
    b += '</div>'
    return Page(b, 'special-page grid-page')

def changelog_page(heading):
    b = f'<h2 class="sp-head">{esc(heading)}</h2><p class="sp-instr">Date. What changed. What we did about it.</p><div class="changelog">'
    for _ in range(7):
        b += ('<div class="logrow"><div class="pl" style="flex:0 0 1.3in"><span class="pl-label">Date</span><div class="slot-line"></div></div>'
              '<div class="pl" style="flex:1 1 auto"><span class="pl-label">What changed, and what we did</span><div class="slot-line"></div><div class="slot-line"></div></div></div>')
    b += '</div>'
    return Page(b, 'special-page')

def wordentry_page():
    def entry():
        return ('<div class="wentry">'
                '<div class="two-col"><div class="pl" style="flex:1 1 0"><span class="pl-label">The word</span><div class="slot-line big"></div></div>'
                '<div class="pl" style="flex:1 1 0"><span class="pl-label">How to say it</span><div class="slot-line big"></div></div></div>'
                '<div class="pl"><span class="pl-label">What it means</span><div class="slot-line"></div></div>'
                '<div class="pl"><span class="pl-label">When we said it, and who said it best</span><div class="slot-line"></div><div class="slot-line"></div></div>'
                '<div class="pl"><span class="pl-label">How it sounds to me (for the one learning it)</span><div class="slot-line"></div></div>'
                '</div>')
    return Page('<div class="wentries">' + entry() + entry() + '</div>', 'special-page word-page')

def song_page(heading, sub):
    b = (f'<div class="prompt-head"><h2 class="prompt">{esc(heading)}</h2>' + (f'<p class="sub">{esc(sub)}</p>' if sub else '') + '</div>'
         '<div class="two-col" style="margin-top:3mm"><div class="pl"><span class="pl-label">Title, or the first line</span><div class="slot-line"></div></div>'
         '<div class="pl"><span class="pl-label">Who sang it, and when</span><div class="slot-line"></div></div></div>'
         '<p class="pl-label" style="margin:4mm 0 0 0">The words, as we sang them</p>' + lines_block())
    return Page(b, 'prompt-page')

def letter_pages(heading, n):
    out = []
    first = (f'<div class="prompt-head letter-head"><h2 class="prompt">{esc(heading)}</h2>'
             f'<div class="pl to"><span class="pl-label">{esc(_L["to"])}</span><div class="slot-line"></div></div></div>' + lines_block())
    out.append(Page(first, 'prompt-page letter-page'))
    for _ in range(n - 1):
        out.append(Page(lines_block('full'), 'prompt-page letter-page cont'))
    return out

def text_page(kind, lines):
    ps = paras(lines)
    if kind == 'half-title':
        return Page(f'<div class="half-title"><p>{esc(ps[0])}</p></div>', 'front', folio=False)
    if kind == 'title':
        nl = [l.strip() for l in lines if l.strip()]
        t, st, au, imp = nl[0], nl[1], nl[2], nl[3]
        return Page(f'<div class="title-page"><p class="tp-title">{esc(t)}</p><p class="tp-sub">{esc(st)}</p>'
                    f'<p class="tp-author">{esc(au)}</p><p class="tp-imprint">{esc(imp)}</p></div>', 'front', folio=False)
    if kind == 'copyright':
        return Page('<div class="copyright">' + ''.join(f'<p>{esc(p)}</p>' for p in ps) + '</div>', 'front', folio=False)
    if kind == 'given':
        b = (f'<div class="given"><p class="given-lead">{esc(_L["given_to"])}</p><div class="slot-line big"></div>'
             f'<div class="two-col"><div class="pl"><span class="pl-label">{esc(_L["by"])}</span><div class="slot-line"></div></div>'
             f'<div class="pl"><span class="pl-label">{esc(_L["on"])}</span><div class="slot-line"></div></div></div>'
             f'<p class="given-lead mt">{esc(_L["because"])}</p><div class="qlines three"></div>'
             f'<div class="given-self"><p class="given-lead small">{esc(_L["self_intro"])}</p>'
             f'<p class="given-lead">{esc(_L["belongs"])}</p><div class="slot-line big"></div></div></div>')
        return Page(b, 'front given-page', folio=False)
    if kind == 'letter-opening':
        b = f'<h2 class="fm-head">{esc(ps[0])}</h2><div class="fm-text">' + ''.join(f'<p>{esc(p)}</p>' for p in ps[1:]) + '</div>'
        return Page(b, 'front fm')
    if kind == 'giver-note':
        b = f'<h2 class="fm-head small">{esc(ps[0])}</h2><div class="fm-text"><p class="fm-lead">{esc(ps[1])}</p><ol class="giver">' + ''.join(f'<li>{esc(x)}</li>' for x in ps[2:]) + '</ol></div>'
        return Page(b, 'front fm giver-page')
    if kind in ('howto',):
        b = f'<h2 class="fm-head small">{esc(ps[0])}</h2><div class="fm-text">' + ''.join(f'<p>{esc(p)}</p>' for p in ps[1:]) + '</div>'
        return Page(b, 'front fm')
    if kind == 'ten':
        items = [l[2:].strip() for l in lines if l.startswith('- ')]
        body_ps = [p for p in paras([l for l in lines if not l.startswith('- ')])]
        b = f'<h2 class="fm-head small">{esc(body_ps[0])}</h2><div class="fm-text">' + ''.join(f'<p>{esc(p)}</p>' for p in body_ps[1:])
        b += '<ol class="ten">' + ''.join(f'<li><span class="ten-t">{esc(t)}</span><span class="ten-p">{{{{TEN:{esc(t)}}}}}</span></li>' for t in items) + '</ol></div>'
        return Page(b, 'front fm ten-page')
    if kind == 'permission':
        b = f'<div class="permission"><h2 class="fm-head">{esc(ps[0])}</h2>' + ''.join(f'<p>{esc(p)}</p>' for p in ps[1:]) + '</div>'
        return Page(b, 'front fm permission-page')
    if kind == 'contents':
        return Page('{{CONTENTS}}', 'front fm contents-page')
    if kind == 'in-my-own-hand':
        b = f'<h2 class="fm-head small">{esc(ps[0])}</h2><div class="hand">'
        for p in ps[1:-1]:
            b += f'<p class="stem">{esc(p)}</p><div class="qlines two"></div>'
        b += (f'<div class="two-col sig"><div class="pl"><span class="pl-label">{esc(_L["signed"])}</span><div class="slot-line"></div></div>'
              f'<div class="pl"><span class="pl-label">{esc(_L["date"])}</span><div class="slot-line"></div></div></div></div>')
        return Page(b, 'special-page hand-page')
    if kind == 'for-the-reader':
        b = f'<div class="reader"><p class="reader-head">{esc(ps[0])}</p>' + ''.join(f'<p>{esc(p)}</p>' for p in ps[1:]) + '</div>'
        return Page(b, 'reader-page', folio=False)
    if kind == 'index':
        return Page('{{INDEX}}', 'front fm index-page')
    if kind == 'storylist':
        return Page('{{STORYLIST}}', 'front fm index-page')
    if kind == 'storyteller':
        nl = [l.strip() for l in lines if l.strip()]
        b = '<div class="given" style="padding-top:0.6in">'
        for lab in nl:
            b += f'<p class="given-lead">{esc(lab)}</p><div class="slot-line big"></div><div style="height:7mm"></div>'
        b += '</div>'
        return Page(b, 'front given-page', folio=False)
    if kind == 'rules':
        b = f'<h2 class="fm-head small">{esc(ps[0])}</h2><div class="fm-text"><p class="fm-lead">{esc(ps[1])}</p>' + ''.join(f'<p class="rule-line">{esc(x)}</p>' for x in ps[2:]) + '</div>'
        return Page(b, 'front fm')
    if kind == 'anything-else':
        return Page(f'<div class="prompt-head"><h2 class="prompt">{esc(ps[0])}</h2></div>' + lines_block(), 'prompt-page')
    if kind == 'blank':
        return Page('', 'blank', folio=False)
    raise ValueError(kind)

# ---------- layout ----------
items = parse(MS)
ROMAN = _L['parts']

for it in items:
    k, a, ls = it['kind'], it['arg'], it['lines']
    if k == 'page':
        if a == 'blank':
            blank(); continue
        if a in ('in-my-own-hand','for-the-reader','anything-else','storylist'): part_title = None
        pg = text_page(a, ls)
        if a in ('half-title','title','giver-note','letter-opening','permission','contents','in-my-own-hand','rules'):
            ensure_recto()
        add(pg)
        if a in ('letter-opening', 'howto', 'ten', 'in-my-own-hand'):
            head = paras(ls)[0] if paras(ls) else a
            contents.append(('', head.rstrip('.'), pg.num))
    elif k == 'opener':
        label, _, title = a.partition('|')
        label, title = label.strip(), title.strip()
        skipline = None
        ensure_recto()
        part_label, part_title = ROMAN.get(label, label.title()), title
        pg = add(opener_page(part_label, title, paras(ls)))
        contents.append((part_label, title, pg.num))
    elif k == 'skipline':
        skipline = ' '.join(paras(ls))
    elif k in ('prompt', 'spread'):
        marked = a.strip() == '*'
        text = ls[0].strip(); sub = None
        for l in ls[1:]:
            if l.startswith('>'): sub = l[1:].strip()
        if k == 'spread':
            ensure_verso()
            pg = add(prompt_page(text, sub, marked)); prompt_index[text] = pg.num
            add(prompt_page(text, sub, marked, cont=True))
        else:
            pg = add(prompt_page(text, sub, marked)); prompt_index[text] = pg.num
        index_entries.append((part_title, text, pg.num))
    elif k in ('quick', 'finish'):
        pg = add(quick_page(a, [l[2:].strip() for l in ls if l.startswith('- ')], finish=(k=='finish')))
        index_entries.append((part_title, a, pg.num))
    elif k == 'family':
        pg = add(family_page()); index_entries.append((part_title, _L['family_h'].rstrip('.'), pg.num))
    elif k == 'photo':
        add(photo_page())
    elif k == 'special':
        instr = ' '.join(paras(ls))
        names = {'family-tree':_L['tree'],'important-people':_L['people'],'family-sayings':_L['sayings'],'decades':_L['decades'],'songs':_L['songs'],'recipe':_L['recipe'],'places':'Where the stories happened','startend':'How we started, how we ended'}
        start = len(pages) + 1
        if a == 'family-tree':
            ensure_verso(); start = len(pages) + 1; [add(p) for p in family_tree_pages(instr)]
        elif a == 'important-people':
            ensure_verso(); start = len(pages) + 1; [add(p) for p in important_people_pages(instr)]
        elif a == 'family-sayings': add(sayings_page(instr))
        elif a == 'decades': add(decades_page(instr))
        elif a == 'places': add(places_page(instr))
        elif a == 'startend': add(startend_page(ls))
        elif a == 'songs': add(songs_page(instr))
        elif a == 'recipe':
            ensure_verso(); start = len(pages) + 1; [add(p) for p in recipe_pages(instr)]
        else: raise ValueError(a)
        index_entries.append((part_title, names[a], start))
    elif k == 'lifepage':
        text = ls[0].strip(); sub = None
        for l in ls[1:]:
            if l.startswith('>'): sub = l[1:].strip()
        pg = add(lifepage(text, sub)); prompt_index[text] = pg.num; index_entries.append((part_title, text, pg.num))
    elif k == 'fields':
        sub = None; items = []
        for l in ls:
            if l.startswith('>'): sub = l[1:].strip()
            elif l.startswith('- '):
                lab, _, n = l[2:].partition('|'); items.append((lab.strip(), int(n.strip() or 2)))
        pg = add(fields_page(a, sub, items)); index_entries.append((part_title, a, pg.num))
    elif k == 'names':
        sub = None
        for l in ls:
            if l.startswith('>'): sub = l[1:].strip()
        pg = add(names_page(a, sub)); index_entries.append((part_title, a, pg.num))
    elif k == 'words':
        sub = None
        for l in ls:
            if l.startswith('>'): sub = l[1:].strip()
        pg = add(words_page(a, sub)); index_entries.append((part_title, a, pg.num))
    elif k == 'photogrid':
        pg = add(photogrid_page(a)); index_entries.append((part_title, a, pg.num))
    elif k == 'changelog':
        pg = add(changelog_page(a)); index_entries.append((part_title, a, pg.num))
    elif k == 'flow':
        fpath, _, rest = a.partition('|'); label, _, title = rest.partition('|')
        fpath, label, title = fpath.strip(), label.strip(), title.strip()
        ensure_recto()
        start = len(pages) + 1
        part_label, part_title = ROMAN.get(label, label.title()), title
        n, fpdf = render_flow(os.path.join(os.path.dirname(MS), fpath), part_label, title, start)
        for _ in range(n): add(Page('', 'flow-placeholder', folio=False))
        flows.append((start, n, fpdf))
        contents.append((part_label, title, start))
        index_entries.append((title, title, start))
    elif k == 'wordentry':
        add(wordentry_page())
    elif k == 'song':
        sub = None
        for l in ls:
            if l.startswith('>'): sub = l[1:].strip()
        pg = add(song_page(a, sub)); prompt_index[a] = pg.num; index_entries.append((part_title, a, pg.num))
    elif k == 'cast':
        add(cast_page())
    elif k == 'story':
        ensure_verso()
        pg = add(story_pages()[0]); story_pages_list.append(pg.num)
        add(story_pages()[1])
    elif k == 'longstory':
        heading, _, n = a.partition('|')
        heading, n = heading.strip(), int(n.strip() or 2)
        sub = ' '.join(paras(ls))
        ensure_verso()
        first = None
        for p_ in longstory_pages(heading, sub, n):
            q = add(p_); first = first or q
        prompt_index[heading] = first.num
        index_entries.append((part_title, heading, first.num))
    elif k == 'letter':
        heading, _, n = a.partition('|')
        heading, n = heading.strip(), int(n.strip() or 2)
        ensure_verso()
        first = None
        for p in letter_pages(heading, n):
            q = add(p); first = first or q
        prompt_index[heading] = first.num
        index_entries.append((part_title, heading, first.num))
    else:
        raise ValueError(k)

# ---------- substitutions ----------
def contents_html():
    b = f'<h2 class="fm-head small">{esc(_L["contents"])}</h2><div class="toc">'
    for label, title, num in contents:
        if label:
            b += f'<p class="toc-part"><span class="toc-label">{esc(label)}</span><span class="toc-title">{esc(title)}</span><span class="toc-num">{num}</span></p>'
        else:
            b += f'<p class="toc-fm"><span class="toc-title">{esc(title)}</span><span class="toc-num">{num}</span></p>'
    return b + '</div>'

def ten_lookup(t):
    # match by prefix against prompt_index keys
    for k, v in prompt_index.items():
        if k.lower().startswith(t.lower().rstrip('.').split('.')[0][:28].lower()):
            return str(v)
    for k, v in prompt_index.items():
        if t.lower()[:20] in k.lower():
            return str(v)
    return '?'

def index_pages():
    # group by part in order; each entry one line
    lines = []
    cur = None
    for part, text, num in index_entries:
        if part != cur:
            lines.append(('head', part, None)); cur = part
        lines.append(('item', text, num))
    PER_PAGE = 88   # two columns of 44 lines
    chunks = [lines[i:i+PER_PAGE] for i in range(0, len(lines), PER_PAGE)]
    out = []
    for ci, chunk in enumerate(chunks):
        half = (len(chunk) + 1) // 2
        cols = [chunk[:half], chunk[half:]]
        b = f'<h2 class="fm-head small">{esc(_L["index"])}</h2>' if ci == 0 else ''
        b += '<div class="index-cols">'
        for col in cols:
            b += '<div class="index-col">'
            for kind, text, num in col:
                if kind == 'head': b += f'<p class="idx-head">{esc(text)}</p>'
                else: b += f'<p class="idx-item"><span class="idx-t">{esc(text)}</span><span class="idx-n">{num}</span></p>'
            b += '</div>'
        b += '</div>'
        out.append(b)
    return out

# expand the index placeholder into real pages, renumbering what follows
for i, p in enumerate(pages):
    if p.body == '{{INDEX}}':
        bodies = index_pages()
        new_pages = [Page(b, 'front fm index-page') for b in bodies]
        tail = pages[i+1:]
        del pages[i:]
        for np_ in new_pages:
            np_.num = len(pages) + 1; np_.part = None; pages.append(np_)
        for tp in tail:
            tp.num = len(pages) + 1; pages.append(tp)
        break
if len(pages) % 2 == 1: blank()

def storylist_html():
    b = '<h2 class="fm-head small">The list</h2><p class="fm-lead" style="margin-bottom:6pt">Write each story\'s title next to its page, so anyone can find it again.</p><div class="index-cols">'
    half = (len(story_pages_list) + 1) // 2
    for col in (story_pages_list[:half], story_pages_list[half:]):
        b += '<div class="index-col">'
        for num in col:
            b += f'<div class="sl-row"><span class="sl-num">{num}</span><div class="slot-line" style="flex:1 1 auto;height:6.2mm"></div></div>'
        b += '</div>'
    return b + '</div>'

for p in pages:
    if '{{STORYLIST}}' in p.body: p.body = p.body.replace('{{STORYLIST}}', storylist_html())
    if '{{CONTENTS}}' in p.body: p.body = p.body.replace('{{CONTENTS}}', contents_html())
    p.body = re.sub(r'\{\{TEN:(.*?)\}\}', lambda m: ten_lookup(html.unescape(m.group(1))), p.body)

# ---------- render ----------
CSS = open(os.path.join(ROOT, '05-interior', 'interior.css'), encoding='utf-8').read()
if (_args.trim_w, _args.trim_h) != (7.0, 10.0):
    CSS += f"\n@page {{ size: {_args.trim_w}in {_args.trim_h}in; }} .page {{ width: {_args.trim_w}in; height: {_args.trim_h}in; }}\n"
if _args.extra_css:
    CSS += '\n' + open(_args.extra_css, encoding='utf-8').read()
if _args.lang == 'es':
    CSS += '\n.toc-label { width: 1.55in; } .toc-fm .toc-title { margin-left: 1.55in; }\n'
CSS += '''
.fields { display: flex; flex-direction: column; flex: 1 1 auto; }
.fields .field { margin-bottom: 3.5mm; }
.fields .field.grow { flex: 1 1 auto; display: flex; flex-direction: column; }
.fields .field.grow .qlines { flex: 1 1 auto; height: auto !important; }
.fields .field .pl-label { display: block; margin-bottom: 1mm; }
.namegroup { margin-bottom: 5mm; padding-bottom: 3mm; border-bottom: 0.5pt solid #ddd; }
.grid2 { display: flex; flex-wrap: wrap; gap: 6mm 8mm; margin-top: 4mm; }
.gridcell { flex: 0 0 calc(50% - 4mm); }
.gridcell .pl { margin-top: 2mm; }
.changelog .logrow { display: flex; gap: 6mm; margin-bottom: 4mm; }
.life-body { display: flex; flex-direction: column; flex: 1 1 auto; }
.wentries { display: flex; flex-direction: column; justify-content: space-between; flex: 1 1 auto; }
.wentry { padding: 2mm 0 6mm 0; border-bottom: 0.5pt solid #ddd; }
.wentry:last-child { border-bottom: none; }
.wentry .pl { margin-bottom: 2mm; }
.wentry .pl .slot-line { height: 8mm; }
.life-body .lines { flex: 1 1 auto; }
'''
FONTS = open(os.path.join(ROOT, '05-interior', 'fonts', 'fonts.css'), encoding='utf-8').read()

def render_page(p):
    side = 'recto' if p.num % 2 == 1 else 'verso'
    folio = ''
    if p.folio:
        part = esc(p.part) if p.part else ''
        folio = f'<div class="folio"><span class="folio-part">{part}</span><span class="folio-num">{p.num}</span></div>'
    return f'<section class="page {side} {p.cls}" data-page="{p.num}"><div class="content">{p.body}</div>{folio}</section>'

doc = ('<!doctype html><html><head><meta charset="utf-8"><title>What I Want You to Know — interior</title>'
       f'<style>{FONTS}\n{CSS}</style></head><body>' + ''.join(render_page(p) for p in pages) + '</body></html>')
os.makedirs(OUT, exist_ok=True)
html_path = os.path.join(OUT, 'interior.html')
open(html_path, 'w', encoding='utf-8').write(doc)
# fonts are referenced relative to the html; copy the folder next to it
if os.path.isdir(os.path.join(OUT, 'fonts')): shutil.rmtree(os.path.join(OUT, 'fonts'))
shutil.copytree(os.path.join(ROOT, '05-interior', 'fonts'), os.path.join(OUT, 'fonts'))

# ---------- overflow check (fails the build if anything spills past the page margins) ----------
check_html = doc.replace('</body>', '''<script>
const out=[];document.querySelectorAll('section.page').forEach(s=>{const c=s.querySelector('.content');
const pr=s.getBoundingClientRect();const limit=pr.bottom-parseFloat(getComputedStyle(s).paddingBottom);
let worst=0;s.querySelectorAll('.content *').forEach(e=>{const r=e.getBoundingClientRect();if(r.height>0&&r.bottom>limit+0.5)worst=Math.max(worst,r.bottom-limit);});
if(c&&c.scrollHeight>c.clientHeight+1)worst=Math.max(worst,c.scrollHeight-c.clientHeight);
if(worst>0)out.push(s.dataset.page+':'+worst.toFixed(1));});
const pre=document.createElement('pre');pre.id='overflow-report';pre.textContent=out.join(' ')||'OK';document.body.appendChild(pre);
</script></body>''')
check_path = os.path.join(OUT, '_check.html')
open(check_path, 'w', encoding='utf-8').write(check_html)
r = subprocess.run([CHROME, '--headless', '--no-sandbox', '--disable-gpu', '--window-size=672,960', '--dump-dom', 'file://' + check_path], capture_output=True, text=True)
os.remove(check_path)
m = re.search(r'<pre id="overflow-report">(.*?)</pre>', r.stdout, flags=re.S)
report = m.group(1).strip() if m else 'no report'
if report != 'OK':
    print('OVERFLOW (page:px past margin):', report)
    sys.exit(1)
print('overflow check: OK')

print(f'pages: {len(pages)}')
for label, title, num in contents:
    print(f'  {num:>4}  {label} {title}')

if not _args.html_only:
    pdf_path = os.path.join(OUT, 'interior.pdf')
    r = subprocess.run([CHROME, '--headless', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer',
                        '--run-all-compositor-stages-before-draw', '--virtual-time-budget=10000',
                        f'--print-to-pdf={pdf_path}', 'file://' + html_path], capture_output=True, text=True)
    if flows:
        tmp = os.path.join(OUT, '_split'); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
        subprocess.run(['pdfseparate', pdf_path, os.path.join(tmp, 'm-%04d.pdf')], check=True)
        order = []
        skip_until = 0
        for i in range(1, len(pages) + 1):
            hit = [f for f in flows if f[0] == i]
            if hit:
                start, n, fpdf = hit[0]
                subprocess.run(['pdfseparate', fpdf, os.path.join(tmp, f'f{start}-%04d.pdf')], check=True)
                order += [os.path.join(tmp, f'f{start}-{j:04d}.pdf') for j in range(1, n + 1)]
                skip_until = start + n - 1
            elif i <= skip_until:
                continue
            else:
                order.append(os.path.join(tmp, f'm-{i:04d}.pdf'))
        final = os.path.join(OUT, 'interior.pdf')
        subprocess.run(['pdfunite'] + order + [final + '.tmp'], check=True)
        os.replace(final + '.tmp', final)
        shutil.rmtree(tmp, ignore_errors=True)
        for _, _, fpdf in flows:
            for ext in ('.pdf', '.html'):
                try: os.remove(fpdf.replace('.pdf', ext))
                except OSError: pass
    data = open(pdf_path, 'rb').read()
    n = len(re.findall(rb'/Type\s*/Page[^s]', data))
    print(f'pdf pages (approx): {n}  size: {len(data)/1e6:.1f} MB')
