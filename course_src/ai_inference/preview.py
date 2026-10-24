"""
preview.py — Renders course figures or built lesson pages to PNG with headless Chrome,
so authors can look at what they drew before shipping it.

Usage (from the repo root):
  python course_src/ai_inference/preview.py figs <out_dir> <image> [<image> ...]
      One PNG sheet with the figures stacked at natural size.
  python course_src/ai_inference/preview.py page <out_dir> <lesson_number>
      Full-page screenshot of the built lesson, cut into 2000px-tall segments.
"""
import glob
import os
import pathlib
import re
import subprocess
import sys
import tempfile

from PIL import Image

CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
COURSE_DIR = 'AI Inference Engineering'


def screenshot(url, out_png, width, height):
    # A fresh profile per call lets several authors render at the same time.
    with tempfile.TemporaryDirectory() as profile:
        subprocess.run(
            [CHROME, '--headless=new', '--disable-gpu', '--no-first-run', f'--user-data-dir={profile}',
             '--hide-scrollbars', '--allow-file-access-from-files', '--virtual-time-budget=4000',
             f'--window-size={width},{height}', f'--screenshot={out_png}', url],
            capture_output=True, timeout=120,
        )


def image_height(path):
    if path.endswith('.svg'):
        m = re.search(r'<svg[^>]*\sheight="(\d+)"', open(path, encoding='utf-8').read())
        return int(m.group(1)) if m else 400
    w, h = Image.open(path).size
    return int(h * min(1, 1000 / w))


def render_figs(out_dir, images):
    parts = []
    for img in images:
        uri = pathlib.Path(img).resolve().as_uri()
        parts.append(f'<div style="margin:0 0 18px"><div style="font:11px monospace;color:#888">{os.path.basename(img)}</div>'
                     f'<img src="{uri}" style="outline:1px solid #eee;max-width:1000px"></div>')
    sheet = pathlib.Path(out_dir) / 'figures.html'
    sheet.write_text('<html><body style="margin:12px;background:#fff">' + ''.join(parts) + '</body></html>', encoding='utf-8')
    out_png = str(pathlib.Path(out_dir) / 'figures.png')
    screenshot(sheet.resolve().as_uri(), out_png, 1040, min(8000, 120 + sum(image_height(i) + 40 for i in images)))
    print(out_png)


def render_page(out_dir, num):
    matches = glob.glob(os.path.join(COURSE_DIR, f'{int(num):03d} *.html'))
    if not matches:
        sys.exit(f'lesson {num} is not built yet; run generate_inference_course.py {num}')
    full = str(pathlib.Path(out_dir) / f'page_{int(num):03d}.png')
    screenshot(pathlib.Path(matches[0]).resolve().as_uri(), full, 1440, 16000)
    # Keep the article column only (this also drops fixed widgets pinned to the
    # viewport edges), then trim the blank space below the page.
    column = Image.open(full).convert('RGB').crop((180, 0, 1260, 16000))
    gray = column.convert('L').point(lambda v: 0 if v > 245 else 255)
    bottom = (gray.getbbox() or (0, 0, column.width, column.height))[3]
    for i, top in enumerate(range(0, bottom, 2000)):
        box = (0, top, column.width, min(bottom, top + 2000))
        if gray.crop(box).getbbox() is None:
            continue  # the shell's min-height layout leaves an empty gap above the footer
        part = str(pathlib.Path(out_dir) / f'page_{int(num):03d}_{i}.png')
        column.crop(box).save(part)
        print(part)


if __name__ == '__main__':
    mode, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    if mode == 'figs':
        render_figs(out, sys.argv[3:])
    elif mode == 'page':
        render_page(out, sys.argv[3])
    else:
        sys.exit(__doc__)
