"""
check_svg.py — Finds layout defects in hand-written course figures by rendering each SVG in
headless Chrome and measuring every <text> element: text running outside the canvas, and text
overlapping other text. Prints one line per problem and exits non-zero if any are found.

Usage (from the repo root):
  python course_src/check_svg.py "AI Training Engineering/images/003-*.svg"
"""
import glob
import html
import json
import pathlib
import re
import subprocess
import sys
import tempfile

CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
TOLERANCE = 1.5  # px of overlap ignored, so touching glyph boxes do not count

MEASURE_JS = r"""
const out = [];
document.querySelectorAll('div.fig').forEach(div => {
  const svg = div.querySelector('svg');
  const name = div.dataset.name;
  if (!svg) { out.push({name, problem: 'no <svg> element'}); return; }
  const vb = svg.viewBox && svg.viewBox.baseVal && svg.viewBox.baseVal.width
    ? svg.viewBox.baseVal : {x: 0, y: 0, width: svg.width.baseVal.value, height: svg.height.baseVal.value};
  const texts = [...svg.querySelectorAll('text')].filter(t => t.textContent.trim());
  const boxes = texts.map(t => {
    const b = t.getBBox();
    const m = t.getCTM(); // map to the svg's user space when inside transformed groups
    const pts = [[b.x, b.y], [b.x + b.width, b.y + b.height]].map(([x, y]) => {
      const p = svg.createSVGPoint(); p.x = x; p.y = y;
      const q = p.matrixTransform(m); return [q.x, q.y];
    });
    return {t: t.textContent.trim().slice(0, 60), x0: Math.min(pts[0][0], pts[1][0]), y0: Math.min(pts[0][1], pts[1][1]),
            x1: Math.max(pts[0][0], pts[1][0]), y1: Math.max(pts[0][1], pts[1][1])};
  });
  boxes.forEach(b => {
    if (b.x0 < vb.x - 1 || b.y0 < vb.y - 1 || b.x1 > vb.x + vb.width + 1 || b.y1 > vb.y + vb.height + 1)
      out.push({name, problem: 'outside canvas', text: b.t,
                box: [b.x0, b.y0, b.x1, b.y1].map(Math.round), canvas: [vb.width, vb.height]});
  });
  for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
    const a = boxes[i], c = boxes[j];
    const w = Math.min(a.x1, c.x1) - Math.max(a.x0, c.x0), h = Math.min(a.y1, c.y1) - Math.max(a.y0, c.y0);
    // Stacked lines of one label touch by a few px of glyph-box padding; only count real overlap.
    const minH = Math.min(a.y1 - a.y0, c.y1 - c.y0);
    if (w > TOL && h > Math.max(TOL, 0.3 * minH)) out.push({name, problem: 'text overlaps text', text: a.t, other: c.t});
  }
});
document.getElementById('result').textContent = JSON.stringify(out);
"""


def check(paths):
    figs = []
    for p in paths:
        svg = pathlib.Path(p).read_text(encoding='utf-8')
        svg = re.sub(r'<\?xml[^>]*\?>', '', svg)
        figs.append(f'<div class="fig" data-name="{html.escape(pathlib.Path(p).name)}">{svg}</div>')
    page = ('<html><body>' + ''.join(figs) + '<pre id="result"></pre><script>const TOL = '
            + str(TOLERANCE) + ';' + MEASURE_JS + '</script></body></html>')
    with tempfile.TemporaryDirectory() as tmp:
        page_path = pathlib.Path(tmp) / 'check.html'
        page_path.write_text(page, encoding='utf-8')
        dom = subprocess.run(
            [CHROME, '--headless=new', '--disable-gpu', '--no-first-run', f'--user-data-dir={tmp}\\profile',
             '--virtual-time-budget=3000', '--dump-dom', page_path.as_uri()],
            capture_output=True, text=True, encoding='utf-8', timeout=120).stdout
    m = re.search(r'<pre id="result">(.*?)</pre>', dom, re.S)
    if not m or not m.group(1).strip():
        sys.exit('could not read measurement results from Chrome')
    return json.loads(html.unescape(m.group(1)))


def main():
    paths = sorted({p for pattern in sys.argv[1:] for p in glob.glob(pattern)})
    if not paths:
        sys.exit(__doc__)
    problems = check(paths)
    for p in problems:
        detail = f" vs '{p['other']}'" if 'other' in p else ''
        where = f" box={p['box']} canvas={p['canvas']}" if 'box' in p else ''
        print(f"{p['name']}: {p['problem']}: '{p.get('text', '')}'{detail}{where}")
    print(f'{len(paths)} figures checked, {len(problems)} problems')
    sys.exit(1 if problems else 0)


if __name__ == '__main__':
    main()
