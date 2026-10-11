#!/usr/bin/env python3
"""Build the single-file index.html: inlines Leaflet, the Nostr/QR bundle, the India outline and licence notices.
Usage: npm install && python3 tools/build.py"""
import re, base64, json, subprocess, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
N = R / 'node_modules'
(R / 'build').mkdir(exist_ok=True)
subprocess.run(['npx', 'esbuild', str(R / 'tools/entry.js'), '--bundle', '--minify', '--format=iife',
                '--platform=browser', '--outfile=' + str(R / 'build/bundle.js')], check=True)
ver = lambda p: json.load(open(N / p / 'package.json'))['version']
MIT_QR = ("MIT License\n\nCopyright (c) 2009 Kazuhiko Arase\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and "
 "associated documentation files (the \"Software\"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, "
 "publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\n"
 "The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\n"
 "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A "
 "PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF "
 "CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n")
LIC = [('leaflet', 'BSD-2-Clause'), ('nostr-tools', 'Unlicense'), ('@noble/curves', 'MIT'), ('@noble/hashes', 'MIT'),
       ('@noble/ciphers', 'MIT'), ('@scure/base', 'MIT'), ('jsqr', 'Apache-2.0'), ('qrcode-generator', 'MIT')]
notes = ["THIRD-PARTY NOTICES\n\nThe original code of Pather Dabi is dedicated to the public domain under CC0 1.0 (see LICENSE).\n"
         "The components below are bundled into index.html and keep their own licences.\n"
         "India outline data: (c) OpenStreetMap contributors, Open Database Licence (ODbL) 1.0, https://www.openstreetmap.org/copyright. This data is NOT CC0.\n"
         "Map tiles are loaded from Esri at run time under Esri's terms. The Atkinson Hyperlegible font is loaded from Google Fonts (SIL OFL) when online.\n"]
for p, l in LIC:
    f = N / p / 'LICENSE'
    notes.append("=" * 70 + f"\n{p} {ver(p)} ({l})\n" + "=" * 70 + "\n" + (f.read_text() if f.exists() else MIT_QR))
notices = "\n".join(notes).replace('</script', '<\\/script')
(R / 'THIRD-PARTY-NOTICES.md').write_text("\n".join(notes))
s = (R / 'src/app.html').read_text()
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
css = (N / 'leaflet/dist/leaflet.css').read_text()
css = re.sub(r'url\(images/([\w\-.]+)\)', lambda m: 'url(data:image/png;base64,' + base64.b64encode((N / 'leaflet/dist/images' / m.group(1)).read_bytes()).decode() + ')', css)
ljs = re.sub(r'//# sourceMappingURL=.*', '', (N / 'leaflet/dist/leaflet.js').read_text())
bun = (R / 'build/bundle.js').read_text()
esc = lambda t: t.replace('</script', '<\\/script')
rep('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.css">', '<style>' + css + '</style>')
rep('<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.js"></script>', '<script>' + esc(ljs) + '\n' + esc(bun) + '</script>')
rep('import{generateSecretKey,getPublicKey,finalizeEvent,verifyEvent,getEventHash,nip44,nip19}from"https://esm.sh/nostr-tools@2.7.2";',
    'const{generateSecretKey,getPublicKey,finalizeEvent,verifyEvent,getEventHash,nip44,nip19}=window.NT,QR=window.QR,jsQR=window.jsQR;')
bj = json.dumps(json.load(open(R / 'data/india-boundary.geojson')), separators=(',', ':'))
rep('const EMBEDDED_BOUNDARY=``;', 'const EMBEDDED_BOUNDARY=`' + bj + '`;')
rep('<!doctype html>', '<!doctype html>\n<!-- Pather Dabi. Original code: CC0 1.0 Universal (public domain). Bundled libraries and the India outline (OpenStreetMap, ODbL) keep their own licences; full notices are in the licences block at the end of this file. -->')
rep('</body>', '<script type="text/plain" id="licenses">\n' + notices + '\n</script></body>')
(R / 'index.html').write_text(s)
m = re.findall(r'<script type="module">(.*?)</script>', s, re.S)
(R / 'build/check.mjs').write_text(m[0])
print(len(s) // 1024, 'KB')
