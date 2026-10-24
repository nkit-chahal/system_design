"""
generate_inference_course.py — Builds the AI Inference Engineering course pages in the
GenAI / ML System Design chapter style from lesson fragments in course_src/ai_inference/.

Fragment syntax (see course_src/ai_inference/AUTHORING.md):
  <fig src="003-kv-growth.svg" caption="...">alt text</fig>   numbered figure from images/
  <codetabs><tab label="vLLM" lang="bash">raw code</tab>...</codetabs>
  <tex>inline LaTeX</tex>, <texblock>display LaTeX</texblock>
  <callout kind="tip|warn|info" title="...">html</callout>
"""
import html as htmllib
import json
import os
import re
import sys
import textwrap

from latex2mathml.converter import convert as latex_to_mathml

COURSE_DIR = 'AI Inference Engineering'
SRC_DIR = os.path.join('course_src', 'ai_inference')
IMG_DIR = os.path.join(COURSE_DIR, 'images')

STAGES = {
    'start': 'Start Here',
    's1': 'Stage 1 · How a Model Generates',
    's2': 'Stage 2 · Serving Engines',
    's3': 'Stage 3 · Smaller and Faster Models',
    's4': 'Stage 4 · GPU Math and Cost',
    's5': 'Stage 5 · Production Serving',
    's6': 'Stage 6 · Observability',
    's7': 'Stage 7 · Advanced Serving',
}

CURRICULUM = [
    (1, 'start', 'Introduction and Overview'),
    (2, 's1', 'Prefill vs Decode'),
    (3, 's1', 'KV Cache'),
    (4, 's1', 'Time to First Token'),
    (5, 's1', 'Tokens per Second'),
    (6, 's1', 'Lab - Measure TTFT and Throughput'),
    (7, 's2', 'Continuous Batching'),
    (8, 's2', 'PagedAttention'),
    (9, 's2', 'vLLM'),
    (10, 's2', 'SGLang'),
    (11, 's2', 'TensorRT-LLM'),
    (12, 's2', 'Lab - Benchmark Two Engines at 50 Concurrent Users'),
    (13, 's3', 'Quantization - FP8, INT8 and 4-bit'),
    (14, 's3', 'Distillation'),
    (15, 's3', 'Speculative Decoding'),
    (16, 's3', 'Lab - Halve Model Memory Without Losing Quality'),
    (17, 's4', 'VRAM Budgeting'),
    (18, 's4', 'Tensor Parallelism'),
    (19, 's4', 'GPU Utilization'),
    (20, 's4', 'Cost per Million Tokens'),
    (21, 's4', 'Lab - GPUs for 1,000 Requests per Minute Under a 2s SLA'),
    (22, 's5', 'Autoscaling'),
    (23, 's5', 'Cold Starts'),
    (24, 's5', 'Prefix Caching'),
    (25, 's5', 'Request Routing'),
    (26, 's5', 'Rate Limiting'),
    (27, 's5', 'Lab - Surviving a 10x Traffic Spike'),
    (28, 's6', 'p50, p95 and p99 Latency'),
    (29, 's6', 'Queue Depth'),
    (30, 's6', 'GPU Metrics'),
    (31, 's6', 'Per-Request Token Accounting'),
    (32, 's6', 'Lab - A Dashboard That Explains Latency Spikes'),
    (33, 's7', 'GPU Architecture and Attention Kernels'),
    (34, 's7', 'Disaggregated Prefill and Decode'),
    (35, 's7', 'Mixture-of-Experts Serving'),
    (36, 's7', 'Long-Context Serving'),
    (37, 's7', 'Multi-LoRA and Multi-Tenant Serving'),
    (38, 's7', 'Structured Output and Tool Calling'),
    (39, 's7', 'Batch and Offline Inference'),
    (40, 's7', 'Reliability and Rollouts'),
]

with open('scratch/head_shell.html', 'r', encoding='utf-8') as f:
    HEAD_TEMPLATE = f.read()

with open('scratch/foot_shell.html', 'r', encoding='utf-8') as f:
    FOOT_TEMPLATE = f.read()

# Article rules copied from the GenAI chapters' stylesheet (the shared shell only has a subset),
# plus the code-tab widget used by the Python Course and a few lesson-specific pieces.
LESSON_CSS = """<style id="inference-lesson-css">
.style_learnContent__K5K7M h2,.style_learnContent__K5K7M h3{margin-bottom:10px;font-weight:600;color:#282828;text-wrap:balance}
.style_learnContent__K5K7M h2{margin-top:28px}
.style_learnContent__K5K7M h3{font-size:26px;line-height:37px;margin-top:22px}
.style_learnContent__K5K7M h4{margin:18px 0 10px;font-size:20px;font-weight:600;color:#282828;line-height:28px;text-wrap:balance}
.style_learnContent__K5K7M ul{margin-left:28px;margin-bottom:16px;list-style:disc;color:#212529}
.style_learnContent__K5K7M ul li{list-style:disc}
.style_learnContent__K5K7M li{color:#212529;line-height:26px;font-size:15px;margin:2px 0}
.style_learnContent__K5K7M li p{margin-top:0;margin-bottom:4px}
.style_learnContent__K5K7M ol{margin-left:28px;margin-bottom:16px}
.style_learnContent__K5K7M ol,.style_learnContent__K5K7M ol li{list-style:decimal}
.style_learnContent__K5K7M figcaption{margin:12px 0;color:#212529;font-size:15px}
.style_learnContent__K5K7M figure{margin:24px 0}
.style_learnContent__K5K7M figure img{max-width:100%;height:auto}
.style_learnContent__K5K7M .table-wrap{overflow:auto;margin:18px 0;position:relative}
.style_learnContent__K5K7M table{margin:0 auto;border:1px solid #e9e9e9;border-collapse:collapse;color:#212529;font-size:15px}
.style_learnContent__K5K7M table tr{border-bottom:1px solid #e9e9e9}
.style_learnContent__K5K7M table tr:last-child{border-bottom:none}
.style_learnContent__K5K7M tbody tr:nth-child(2n){background-color:#f5f5f5}
.style_learnContent__K5K7M table td,.style_learnContent__K5K7M thead th{padding:10px;border-right:1px solid #e9e9e9;line-height:24px;vertical-align:top}
.style_learnContent__K5K7M thead th{text-align:left;font-weight:600;background:#fafafa}
.style_learnContent__K5K7M table td:last-child,.style_learnContent__K5K7M thead th:last-child{border-right:none}
.style_learnContent__K5K7M :not(pre)>code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:13.5px;background:#f3f4f6;border-radius:4px;padding:1px 5px}
.style_learnContent__K5K7M math[display=block]{display:block;margin:18px 0;font-size:18px;overflow-x:auto}
.style_learnContent__K5K7M .lesson-head{margin-bottom:18px}
.style_learnContent__K5K7M .lesson-stage{display:block;font-size:13px;font-weight:600;letter-spacing:.6px;text-transform:uppercase;color:#05673d;margin-bottom:4px}
.style_learnContent__K5K7M .lesson-nav{display:flex;justify-content:space-between;gap:12px;border-top:1px solid #dedede;padding-top:24px;margin-top:40px}
.style_learnContent__K5K7M .lesson-nav a{text-decoration:none;padding:8px 16px;border:1px solid #d9d9d9;line-height:22px;height:auto;max-width:48%}
.style_learnContent__K5K7M .lesson-nav a.ant-btn-primary:hover{color:#fff}
.style_learnContent__K5K7M .callout{border-left:4px solid;padding:14px 18px;border-radius:6px;margin:22px 0;font-size:15px;line-height:1.6}
.style_learnContent__K5K7M .callout p:last-child{margin-bottom:0}
.style_learnContent__K5K7M .callout-tip{background:#f6ffed;border-color:#35cea0}
.style_learnContent__K5K7M .callout-warn{background:#fffbe6;border-color:#fa8c16}
.style_learnContent__K5K7M .callout-info{background:#e6f7ff;border-color:#1890ff}
.style_codeTabsWrap__jMkKK{margin:20px 0}
.style_codeTabs__DEEq6.ant-tabs{display:flex!important;flex-direction:column;padding:0;margin:16px 0;border-radius:10px;border:1px solid #d3d3d3;background:#fff;overflow:hidden}
.style_codeTabs__DEEq6>.ant-tabs-nav{display:flex!important;align-items:flex-end;padding:2px 15px 0;background:#e7fff9;margin:0!important;border-radius:10px 10px 0 0}
.style_codeTabs__DEEq6 .ant-tabs-nav-wrap{display:flex;flex:1 1 auto}
.style_codeTabs__DEEq6 .ant-tabs-nav-list{display:flex!important;flex-direction:row!important;align-items:flex-end}
.style_codeTabs__DEEq6 .ant-tabs-tab{display:inline-flex!important;align-items:center;height:35px;padding:0 16px;border:1px solid transparent;border-bottom:none;background:transparent;cursor:pointer;flex:none}
.style_codeTabs__DEEq6 .ant-tabs-tab-active{border-radius:6px 6px 0 0;border:1px solid #d3d3d3;border-bottom:none;background:#fff}
.style_codeTabs__DEEq6 .ant-tabs-tab-active .ant-tabs-tab-btn{color:#006147}
.style_codeTabs__DEEq6 .ant-tabs-tab-btn{color:#666;font-weight:600;line-height:35px}
.style_codeTabs__DEEq6 .ant-tabs-content-holder{background:#fff}
.style_codeTabs__DEEq6 .ant-tabs-tabpane{position:relative}
.style_codeTabs__DEEq6 .ant-tabs-tabpane-hidden{display:none!important}
.style_codeTabs__DEEq6 pre{padding:16px 48px 18px 18px!important;margin:0!important;border:none!important;background:transparent!important;overflow-x:auto}
.style_codeTabs__DEEq6 pre code{background:transparent;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:13.5px;line-height:1.55;color:#24292f;white-space:pre}
.style_codeTabs__DEEq6 pre code span{font-family:inherit!important;font-style:normal}
.hljs-keyword{color:#d73a49}.hljs-number{color:#005cc5}.hljs-built_in{color:#6f42c1}
.hljs-string{color:#032f62}.hljs-comment{color:#6a737d}.hljs-attr{color:#005cc5}
.style_codeTabs__DEEq6 .style_copyBtn__4MbAa{position:absolute;top:16px;right:16px;padding:4px;height:auto;border:none;background:transparent;box-shadow:none;cursor:pointer;z-index:2}
</style>"""

CODE_WIDGET_JS = """
<script>
(function(){
  document.querySelectorAll('.style_codeTabsWrap__jMkKK').forEach(function(wrap){
    var tabs = wrap.querySelectorAll('.ant-tabs-tab');
    var panes = wrap.querySelectorAll('.ant-tabs-tabpane');
    tabs.forEach(function(tab, i){
      tab.addEventListener('click', function(){
        tabs.forEach(function(t){ t.classList.remove('ant-tabs-tab-active'); t.querySelector('[role=tab]').setAttribute('aria-selected','false'); });
        panes.forEach(function(p){ p.classList.remove('ant-tabs-tabpane-active'); p.classList.add('ant-tabs-tabpane-hidden'); p.setAttribute('aria-hidden','true'); });
        tab.classList.add('ant-tabs-tab-active');
        tab.querySelector('[role=tab]').setAttribute('aria-selected','true');
        panes[i].classList.add('ant-tabs-tabpane-active');
        panes[i].classList.remove('ant-tabs-tabpane-hidden');
        panes[i].setAttribute('aria-hidden','false');
      });
    });
    wrap.querySelectorAll('.style_copyBtn__4MbAa').forEach(function(btn){
      btn.addEventListener('click', function(){
        var text = btn.closest('.ant-tabs-tabpane').querySelector('code').innerText;
        if (navigator.clipboard) navigator.clipboard.writeText(text);
      });
    });
  });
})();
</script>
"""

COPY_BTN = '''<button type="button" class="ant-btn css-133v4sd ant-btn-default style_copyBtn__4MbAa" aria-label="Copy code"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="5.2" y="1.4" width="8.4" height="9.6" rx="1.2" stroke="#333" stroke-width="1.15"/><rect x="1.4" y="4.8" width="8.4" height="9.6" rx="1.2" fill="#fff" stroke="#333" stroke-width="1.15"/></svg></button>'''

KEYWORDS = {
    'python': set(
        "and as assert async await break class continue def del elif else except False finally "
        "for from global if import in is lambda None nonlocal not or pass raise return True try "
        "while with yield".split()
    ),
    'bash': set("if then else elif fi for in do done while case esac function export local return".split()),
    'yaml': {'true', 'false', 'null'},
    'promql': set("sum rate avg max min by without histogram_quantile irate increase count topk on ignoring offset".split()),
}
BUILTINS = {
    'python': set(
        "abs all any bool dict enumerate filter float format int len list map max min open "
        "print range set sorted str sum super tuple type zip isinstance round".split()
    ),
}


def highlight(code, lang):
    lang = (lang or 'text').lower()
    if lang in ('text', 'plaintext'):
        return htmllib.escape(code, quote=False)
    comment = r'//.*?$' if lang in ('javascript', 'cpp') else r'#.*?$'
    # YAML keys ("key:") get their own token so they can be colored as attributes.
    yaml_key = r'(?<![\w.-])[A-Za-z_][\w.-]*(?=:(?:\s|$))|' if lang == 'yaml' else ''
    token_re = re.compile(
        rf'({comment}|"""[\s\S]*?"""|"[^"\\\n]*(?:\\.[^"\\\n]*)*"|\'[^\'\\\n]*(?:\\.[^\'\\\n]*)*\''
        rf'|\b\d+(?:\.\d+)?(?:e-?\d+)?\b|{yaml_key}\b[A-Za-z_][A-Za-z0-9_]*\b)',
        re.M,
    )
    keywords = KEYWORDS.get(lang, set())
    builtins = BUILTINS.get(lang, set())
    out, last = [], 0
    for m in token_re.finditer(code):
        out.append(htmllib.escape(code[last:m.start()], quote=False))
        tok = m.group(0)
        esc = htmllib.escape(tok, quote=False)
        if tok.startswith('#') or tok.startswith('//'):
            out.append(f'<span class="hljs-comment">{esc}</span>')
        elif tok[0] in '"\'':
            out.append(f'<span class="hljs-string">{esc}</span>')
        elif tok[0].isdigit():
            out.append(f'<span class="hljs-number">{esc}</span>')
        elif lang == 'yaml' and code[m.end():m.end() + 1] == ':':
            out.append(f'<span class="hljs-attr">{esc}</span>')
        elif tok in keywords:
            out.append(f'<span class="hljs-keyword">{esc}</span>')
        elif tok in builtins:
            out.append(f'<span class="hljs-built_in">{esc}</span>')
        else:
            out.append(esc)
        last = m.end()
    out.append(htmllib.escape(code[last:], quote=False))
    return ''.join(out)


class LessonBuilder:
    """Expands one lesson fragment's custom tags into the article HTML."""

    def __init__(self, num):
        self.num = num
        self.fig_count = 0
        self.tab_seq = 0
        self.code_blocks = []

    def _attrs(self, raw):
        return {k: htmllib.unescape(v) for k, v in re.findall(r'([\w-]+)="([^"]*)"', raw)}

    def _codetabs(self, m):
        tabs = re.findall(r'<tab\b([^>]*)>(.*?)</tab>', m.group(1), re.S)
        if not tabs:
            raise ValueError(f'lesson {self.num}: <codetabs> without <tab> children')
        self.tab_seq += 1
        uid = f'{self.num}-{self.tab_seq}'
        tab_html, pane_html = [], []
        for i, (raw_attrs, code) in enumerate(tabs):
            attrs = self._attrs(raw_attrs)
            code = textwrap.dedent(code.strip('\n')).rstrip()
            active = i == 0
            tab_html.append(
                f'<div data-node-key="{i}" class="ant-tabs-tab{" ant-tabs-tab-active" if active else ""}">'
                f'<div role="tab" aria-selected="{str(active).lower()}" class="ant-tabs-tab-btn" tabindex="{0 if active else -1}" '
                f'id="rc-tabs-{uid}-tab-{i}" aria-controls="rc-tabs-{uid}-panel-{i}">{htmllib.escape(attrs.get("label", "Code"))}</div></div>'
            )
            pane_cls = 'ant-tabs-tabpane ant-tabs-tabpane-active' if active else 'ant-tabs-tabpane ant-tabs-tabpane-hidden'
            lang = attrs.get('lang', 'text')
            pane_html.append(
                f'<div role="tabpanel" tabindex="{0 if active else -1}" aria-hidden="{str(not active).lower()}" class="{pane_cls}" '
                f'id="rc-tabs-{uid}-panel-{i}" aria-labelledby="rc-tabs-{uid}-tab-{i}">'
                f'<pre><code class="hljs language-{lang}">{highlight(code, lang)}</code></pre>{COPY_BTN}</div>'
            )
        block = f'''<div class="style_codeTabsWrap__jMkKK">
<div class="ant-tabs ant-tabs-top ant-tabs-card style_codeTabs__DEEq6 css-133v4sd">
<div role="tablist" class="ant-tabs-nav"><div class="ant-tabs-nav-wrap"><div class="ant-tabs-nav-list">{''.join(tab_html)}</div></div></div>
<div class="ant-tabs-content-holder"><div class="ant-tabs-content ant-tabs-content-top">{''.join(pane_html)}</div></div>
</div></div>'''
        # Park finished code blocks so later passes (math, figures) never touch code text.
        self.code_blocks.append(block)
        return f'\x00CODE{len(self.code_blocks) - 1}\x00'

    def _fig(self, m):
        attrs = self._attrs(m.group(1))
        alt = ' '.join(m.group(2).split())
        src = attrs['src']
        if not os.path.exists(os.path.join(IMG_DIR, src)):
            if attrs.get('optional'):
                print(f'  [skip] lesson {self.num}: optional image images/{src} not generated yet')
                return ''
            raise FileNotFoundError(f'lesson {self.num}: missing images/{src}')
        self.fig_count += 1
        width = f' width="{attrs["width"]}"' if 'width' in attrs else ''
        return (
            f'<figure class="py-1"><div style="display:flex;justify-content:center">'
            f'<img alt="{htmllib.escape(alt)}" loading="lazy" decoding="async" src="images/{src}"{width}></div>'
            f'<div style="display:flex;justify-content:center"><figcaption class="py-1">'
            f'Figure {self.fig_count}: {attrs["caption"]}</figcaption></div></figure>'
        )

    def _callout(self, m):
        attrs = self._attrs(m.group(1))
        kind = attrs.get('kind', 'tip')
        title = f'<strong>{attrs["title"]}</strong>' if 'title' in attrs else ''
        body = m.group(2).strip()
        if not body.startswith('<'):
            body = f'<p>{body}</p>'
        return f'<div class="callout callout-{kind}">{title}{body}</div>'

    def _heading_id(self, m):
        level, attrs, inner = m.group(1), m.group(2), m.group(3)
        if 'id=' in attrs:
            return m.group(0)
        slug = re.sub(r'[^a-z0-9]+', '-', re.sub(r'<[^>]+>', '', inner).lower()).strip('-')
        return f'<h{level}{attrs} id="{slug}">{inner}</h{level}>'

    def build(self, src):
        body = re.sub(r'<codetabs>(.*?)</codetabs>', self._codetabs, src, flags=re.S)
        body = re.sub(r'<texblock>(.*?)</texblock>', lambda m: latex_to_mathml(m.group(1).strip(), display='block'), body, flags=re.S)
        body = re.sub(r'<tex>(.*?)</tex>', lambda m: latex_to_mathml(m.group(1).strip()), body, flags=re.S)
        body = re.sub(r'<fig\b([^>]*)>(.*?)</fig>', self._fig, body, flags=re.S)
        body = re.sub(r'<callout\b([^>]*)>(.*?)</callout>', self._callout, body, flags=re.S)
        body = re.sub(r'(<table\b.*?</table>)', r'<div class="table-wrap">\1</div>', body, flags=re.S)
        body = re.sub(r'<h([234])([^>]*)>(.*?)</h\1>', self._heading_id, body, flags=re.S)
        leftover = re.search(r'</?(fig|codetabs|tab|tex|texblock|callout)\b', body)
        if leftover:
            raise ValueError(f'lesson {self.num}: unexpanded <{leftover.group(1)}> tag near: {body[leftover.start():leftover.start() + 80]!r}')
        return re.sub(r'\x00CODE(\d+)\x00', lambda m: self.code_blocks[int(m.group(1))], body)


def lesson_filename(num, title):
    return f'{num:03d} {title}.html'


def nav_button(lesson, label, primary):
    style = 'display:inline-flex;align-items:center;gap:6px;border-radius:6px;font-weight:600;'
    if primary:
        style += 'background:#05673d;border-color:#05673d;color:#fff;'
    cls = 'ant-btn ant-btn-primary' if primary else 'ant-btn ant-btn-default'
    href = '../index.html' if lesson is None else lesson_filename(lesson[0], lesson[2])
    return f'<a href="{htmllib.escape(href)}" class="{cls}" style="{style}">{label}</a>'


def build_page(index):
    num, stage, title = CURRICULUM[index]
    with open(os.path.join(SRC_DIR, f'{num:03d}.html'), encoding='utf-8') as f:
        body = LessonBuilder(num).build(f.read())

    head = re.sub(r'<aside\b.*?</aside>', '', HEAD_TEMPLATE, count=1, flags=re.S)
    head = re.sub(r'<title>.*?</title>', f'<title>{htmllib.escape(title)} | AI Inference Engineering</title>', head, count=1, flags=re.S)
    head = head.replace('</head>', LESSON_CSS + '</head>', 1) if '</head>' in head else LESSON_CSS + head

    prev_l = CURRICULUM[index - 1] if index > 0 else None
    next_l = CURRICULUM[index + 1] if index + 1 < len(CURRICULUM) else None
    prev_btn = nav_button(prev_l, f'← {prev_l[2]}' if prev_l else '← Back to Hub', False)
    next_btn = nav_button(next_l, f'Next: {next_l[2]} →' if next_l else 'Course complete! Back to Hub →', True)

    # No <header> wrapper here: nav_inject.js hides every <header> except its own topbar.
    article = f"""<article class="style_learnContent__K5K7M">
<div class="lesson-head"><strong class="style_chapter__grtAe">{num:02d}</strong><span class="lesson-stage">{STAGES[stage]}</span><h1>{htmllib.escape(title)}</h1></div>
{body}
<div class="lesson-nav">{prev_btn}{next_btn}</div>
"""
    page = head + article + FOOT_TEMPLATE + CODE_WIDGET_JS + """
<!-- nav-inject-patched -->
<script src="../nav_map.js"></script>
<script src="../nav_inject.js"></script>
"""
    with open(os.path.join(COURSE_DIR, lesson_filename(num, title)), 'w', encoding='utf-8') as f:
        f.write(page)


def build_all(only=None):
    os.makedirs(IMG_DIR, exist_ok=True)
    built = 0
    for i, (num, _, title) in enumerate(CURRICULUM):
        if only and num not in only:
            continue
        if not os.path.exists(os.path.join(SRC_DIR, f'{num:03d}.html')):
            print(f'  [todo] {num:03d} {title}: no source fragment yet')
            continue
        build_page(i)
        built += 1
    # Stage grouping for build_index.py / build_unified_nav_data.py sidebars.
    with open(os.path.join(COURSE_DIR, 'course.json'), 'w', encoding='utf-8') as f:
        json.dump({'subgroups': {lesson_filename(n, t): STAGES[s] for n, s, t in CURRICULUM}}, f, indent=2, ensure_ascii=False)
    print(f'Built {built} AI Inference Engineering lessons.')


if __name__ == '__main__':
    build_all({int(a) for a in sys.argv[1:]} or None)
