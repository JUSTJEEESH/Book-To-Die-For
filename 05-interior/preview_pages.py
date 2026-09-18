#!/usr/bin/env python3
"""Render individual pages of build/interior.html to PNG for visual checks.
Usage: python3 05-interior/preview_pages.py OUTDIR 3 5 7 ...
"""
import re, sys, os, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
html_path = os.path.join(ROOT, '05-interior', 'build', 'interior.html')
doc = open(html_path, encoding='utf-8').read()
head = doc.split('<body>')[0] + '<body>'
sections = re.findall(r'<section class="page[^"]*" data-page="(\d+)">.*?</section>', doc, flags=re.S)
secs = {int(m.group(1)): m.group(0) for m in re.finditer(r'<section class="page[^"]*" data-page="(\d+)">.*?</section>', doc, flags=re.S)}
outdir = sys.argv[1]; os.makedirs(outdir, exist_ok=True)
for n in map(int, sys.argv[2:]):
    one = head + secs[n].replace('page-break-after: always','') + '</body></html>'
    p = os.path.join(ROOT, '05-interior', 'build', f'_p{n}.html')
    open(p, 'w', encoding='utf-8').write(one)
    png = os.path.join(outdir, f'p{n:03d}.png')
    subprocess.run([CHROME, '--headless', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
                    '--window-size=672,1047', '--force-device-scale-factor=1.5',
                    f'--screenshot={png}', 'file://' + p], capture_output=True)
    os.remove(p)
    print(png)
