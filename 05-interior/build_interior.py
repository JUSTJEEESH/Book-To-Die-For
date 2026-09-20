#!/usr/bin/env python3
"""Build the print-ready interior PDF from 04-manuscript/MANUSCRIPT.md.

Usage:  python3 05-interior/build_interior.py [--html-only]
Output: 05-interior/build/interior.html and interior.pdf

Trim 7 x 10 in, no bleed. Every page is a fixed 7x10 box; recto/verso margins are set per page
by this script, so the PDF is exactly what KDP receives. Page 1 is a recto.
"""
import re, sys, os, html, subprocess, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MS = os.path.join(ROOT, '04-manuscript', 'MANUSCRIPT.md')
OUT = os.path.join(ROOT, '05-interior', 'build')
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

def add(page):
    page.num = len(pages) + 1
    page.part = part_title
    pages.append(page)
    return page

def is_recto(): return (len(pages) + 1) % 2 == 1
def blank():
    add(Page('', 'blank', folio=False))
def ensure_recto():
    if not is_recto(): blank()
def ensure_verso():
    if is_recto(): blank()

def lines_block(extra_cls=''):
    return f'<div class="lines {extra_cls}"></div>'

def mark(m): return '<span class="mark" aria-hidden="true"></span>' if m else ''

def prompt_page(text, sub, marked, cont=False):
    b = '<div class="prompt-head">'
    if cont:
        b += f'<p class="cont">{esc(text)}<span class="contd"> (continued)</span></p>'
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
    b = ('<div class="prompt-head"><h2 class="prompt">A question from your family.</h2>'
         '<p class="sub">Written by the person who gave you this book.</p></div>'
         '<div class="family-q"><p class="label">Their question</p><div class="qlines two"></div></div>'
         + lines_block())
    return Page(b, 'prompt-page family-page')

def photo_page():
    return Page('<div class="photo-space"></div><p class="photo-cap">For a photograph, a drawing, or anything else.</p>', 'photo-page')

def slot(label, w='100%'):
    return f'<div class="slot" style="width:{w}"><div class="slot-line"></div><p class="slot-label">{esc(label)}</p></div>'

def family_tree_pages(instr):
    v = ('<h2 class="sp-head">Family tree</h2><p class="sp-instr">' + esc(instr) + '</p>'
         '<div class="tree">'
         '<p class="tier">Their parents</p><div class="row">' + slot('name') + slot('name') + slot('name') + slot('name') + '</div>'
         '<p class="tier">My grandparents</p><div class="row">' + slot('name, born') + slot('name, born') + slot('name, born') + slot('name, born') + '</div>'
         '<p class="tier">My parents</p><div class="row wide">' + slot('name, born') + slot('name, born') + '</div>'
         '<p class="tier">Me</p><div class="row one">' + slot('name, born') + '</div>'
         '<p class="tier">My brothers and sisters</p><div class="row">' + ''.join(slot('name, born') for _ in range(4)) + '</div>'
         '<p class="tier">Others who counted as family</p><div class="row">' + ''.join(slot('name, who they were') for _ in range(4)) + '</div>'
         '</div>')
    r = ('<h2 class="sp-head">And where it went</h2><p class="sp-instr">Add anyone the boxes leave out. Draw lines however you like.</p>'
         '<div class="tree">'
         '<p class="tier">Me, and the person I built a life with</p><div class="row wide">' + slot('name, born') + slot('name, born') + '</div>'
         '<p class="tier">Children</p><div class="row">' + ''.join(slot('name, born') for _ in range(4)) + '</div>'
         '<p class="tier">Grandchildren</p><div class="row">' + ''.join(slot('name, born') for _ in range(4)) + '</div><div class="row">' + ''.join(slot('name, born') for _ in range(4)) + '</div>'
         '<p class="tier">And after that</p><div class="row">' + ''.join(slot('') for _ in range(4)) + '</div>'
         '</div>')
    return [Page(v, 'special-page'), Page(r, 'special-page')]

def important_people_pages(instr):
    def rows(n):
        s = ''
        for _ in range(n):
            s += ('<div class="person"><div class="pl"><span class="pl-label">Name</span><div class="slot-line"></div></div>'
                  '<div class="pl"><span class="pl-label">Who they were to me</span><div class="slot-line"></div></div>'
                  '<div class="pl"><span class="pl-label">One line I\'d want you to know</span><div class="slot-line"></div></div></div>')
        return s
    v = '<h2 class="sp-head">The important people</h2><p class="sp-instr">' + esc(instr) + '</p><div class="people">' + rows(4) + '</div>'
    r = '<div class="people top">' + rows(5) + '</div>'
    return [Page(v, 'special-page'), Page(r, 'special-page')]

def sayings_page(instr):
    b = '<h2 class="sp-head">Family sayings</h2><p class="sp-instr">' + esc(instr) + '</p><div class="sayings">'
    for _ in range(7):
        b += ('<div class="saying"><div class="pl"><span class="pl-label">We always said</span><div class="slot-line"></div></div>'
              '<div class="pl"><span class="pl-label">What it meant</span><div class="slot-line"></div></div></div>')
    b += '</div>'
    return Page(b, 'special-page')

def songs_page(instr):
    b = '<h2 class="sp-head">The songs</h2><p class="sp-instr">' + esc(instr) + '</p><div class="sayings">'
    for _ in range(7):
        b += ('<div class="saying"><div class="pl"><span class="pl-label">Title, and who sang it</span><div class="slot-line"></div></div>'
              '<div class="pl"><span class="pl-label">Why</span><div class="slot-line"></div></div></div>')
    b += '</div>'
    return Page(b, 'special-page')

def recipe_pages(instr):
    v = ('<h2 class="sp-head">The recipe</h2><p class="sp-instr">' + esc(instr) + '</p>'
         '<div class="pl"><span class="pl-label">What it\'s called</span><div class="slot-line"></div></div>'
         '<div class="pl"><span class="pl-label">Who taught it to me</span><div class="slot-line"></div></div>'
         '<p class="tier mt">What goes in it</p>' + lines_block('short'))
    r = ('<p class="tier top">How to make it</p>' + lines_block('') +
         '<p class="tier mt">The part that isn\'t written down anywhere</p><div class="qlines three"></div>')
    return [Page(v, 'special-page recipe'), Page(r, 'special-page recipe')]

def decades_page(instr):
    rows = ['Before I was ten', 'My teens', 'My twenties', 'My thirties', 'My forties', 'My fifties', 'My sixties', 'My seventies', 'After that', 'Now']
    b = '<h2 class="sp-head">My life, a line at a time</h2><p class="sp-instr">' + esc(instr) + '</p><div class="decades">'
    for r in rows:
        b += f'<div class="pl"><span class="pl-label">{esc(r)}</span><div class="slot-line"></div></div>'
    b += '</div>'
    return Page(b, 'special-page decades-page')

def letter_pages(heading, n):
    out = []
    first = (f'<div class="prompt-head letter-head"><h2 class="prompt">{esc(heading)}</h2>'
             '<div class="pl to"><span class="pl-label">To</span><div class="slot-line"></div></div></div>' + lines_block())
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
        b = ('<div class="given"><p class="given-lead">This book was given to</p><div class="slot-line big"></div>'
             '<div class="two-col"><div class="pl"><span class="pl-label">by</span><div class="slot-line"></div></div>'
             '<div class="pl"><span class="pl-label">on</span><div class="slot-line"></div></div></div>'
             '<p class="given-lead mt">Because</p><div class="qlines three"></div>'
             '<div class="given-self"><p class="given-lead small">If you bought this book for yourself:</p>'
             '<p class="given-lead">This book belongs to</p><div class="slot-line big"></div></div></div>')
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
        b += ('<div class="two-col sig"><div class="pl"><span class="pl-label">Signed</span><div class="slot-line"></div></div>'
              '<div class="pl"><span class="pl-label">Date</span><div class="slot-line"></div></div></div></div>')
        return Page(b, 'special-page hand-page')
    if kind == 'for-the-reader':
        b = f'<div class="reader"><p class="reader-head">{esc(ps[0])}</p>' + ''.join(f'<p>{esc(p)}</p>' for p in ps[1:]) + '</div>'
        return Page(b, 'reader-page', folio=False)
    if kind == 'index':
        return Page('{{INDEX}}', 'front fm index-page')
    if kind == 'anything-else':
        return Page(f'<div class="prompt-head"><h2 class="prompt">{esc(ps[0])}</h2></div>' + lines_block(), 'prompt-page')
    if kind == 'blank':
        return Page('', 'blank', folio=False)
    raise ValueError(kind)

# ---------- layout ----------
items = parse(MS)
ROMAN = {'PART ONE':'Part One','PART TWO':'Part Two','PART THREE':'Part Three','PART FOUR':'Part Four','PART FIVE':'Part Five',
         'PART SIX':'Part Six','PART SEVEN':'Part Seven','PART EIGHT':'Part Eight','PART NINE':'Part Nine','PART TEN':'Part Ten',
         'PART ELEVEN':'Part Eleven','PART TWELVE':'Part Twelve','PART THIRTEEN':'Part Thirteen'}

for it in items:
    k, a, ls = it['kind'], it['arg'], it['lines']
    if k == 'page':
        if a == 'blank':
            blank(); continue
        if a in ('in-my-own-hand','for-the-reader','anything-else'): part_title = None
        pg = text_page(a, ls)
        if a in ('half-title','title','giver-note','letter-opening','permission','contents','in-my-own-hand'):
            ensure_recto()
        add(pg)
        if a == 'letter-opening': contents.append(('', 'This book is yours', pg.num))
        if a == 'howto': contents.append(('', 'How to use this book', pg.num))
        if a == 'ten': contents.append(('', 'If you only fill out ten pages', pg.num))
        if a == 'in-my-own-hand': contents.append(('', 'In my own hand', pg.num))
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
        pg = add(family_page()); index_entries.append((part_title, 'A question from your family', pg.num))
    elif k == 'photo':
        add(photo_page())
    elif k == 'special':
        instr = ' '.join(paras(ls))
        names = {'family-tree':'Family tree','important-people':'The important people','family-sayings':'Family sayings','decades':'My life, a line at a time','songs':'The songs','recipe':'The recipe'}
        start = len(pages) + 1
        if a == 'family-tree':
            ensure_verso(); start = len(pages) + 1; [add(p) for p in family_tree_pages(instr)]
        elif a == 'important-people':
            ensure_verso(); start = len(pages) + 1; [add(p) for p in important_people_pages(instr)]
        elif a == 'family-sayings': add(sayings_page(instr))
        elif a == 'decades': add(decades_page(instr))
        elif a == 'songs': add(songs_page(instr))
        elif a == 'recipe':
            ensure_verso(); start = len(pages) + 1; [add(p) for p in recipe_pages(instr)]
        else: raise ValueError(a)
        index_entries.append((part_title, names[a], start))
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
    b = '<h2 class="fm-head small">Contents</h2><div class="toc">'
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
        b = '<h2 class="fm-head small">Where to find things</h2>' if ci == 0 else ''
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

for p in pages:
    if '{{CONTENTS}}' in p.body: p.body = p.body.replace('{{CONTENTS}}', contents_html())
    p.body = re.sub(r'\{\{TEN:(.*?)\}\}', lambda m: ten_lookup(html.unescape(m.group(1))), p.body)

# ---------- render ----------
CSS = open(os.path.join(ROOT, '05-interior', 'interior.css'), encoding='utf-8').read()
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

if '--html-only' not in sys.argv:
    pdf_path = os.path.join(OUT, 'interior.pdf')
    r = subprocess.run([CHROME, '--headless', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer',
                        '--run-all-compositor-stages-before-draw', '--virtual-time-budget=10000',
                        f'--print-to-pdf={pdf_path}', 'file://' + html_path], capture_output=True, text=True)
    data = open(pdf_path, 'rb').read()
    n = len(re.findall(rb'/Type\s*/Page[^s]', data))
    print(f'pdf pages (approx): {n}  size: {len(data)/1e6:.1f} MB')
