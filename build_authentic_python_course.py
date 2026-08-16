"""
build_authentic_python_course.py — Generates all 15 authentic ByteByteGo-style lesson HTML files
with exact fonts, CSS, code tabs, and custom illustrated SVG diagrams.
"""
import os
import re
import json

with open('scratch/head_shell.html', 'r', encoding='utf-8') as f:
    HEAD_TEMPLATE = f.read()

with open('scratch/foot_shell.html', 'r', encoding='utf-8') as f:
    FOOT_TEMPLATE = f.read()

# Helper to create ByteByteGo Code Tab
def make_code_tab(code_content, lang="python"):
    escaped_code = code_content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return f"""<div class="style_codeTabsWrap__jMkKK">
  <div class="style_codeTabs__DEEq6">
    <div class="ant-tabs ant-tabs-top ant-tabs-card">
      <div class="ant-tabs-nav">
        <div class="ant-tabs-nav-wrap">
          <div class="ant-tabs-nav-list">
            <div class="ant-tabs-tab ant-tabs-tab-active">
              <div class="ant-tabs-tab-btn">{lang.capitalize()}</div>
            </div>
          </div>
        </div>
      </div>
      <div class="ant-tabs-content-holder">
        <div class="ant-tabs-content">
          <div class="ant-tabs-tabpane ant-tabs-tabpane-active">
            <pre><code class="hljs language-{lang}">{escaped_code}</code></pre>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>"""

# Helper to create ByteByteGo Figure wrapper
def make_figure(svg_content):
    return f"""<figure class="py-1"><div style="display:flex;justify-content:center;margin:20px 0">{svg_content}</div></figure>"""

# Helper for Callouts
def make_callout(title, text, kind="tip"):
    border_color = "#35cea0" if kind == "tip" else ("#fa8c16" if kind == "warn" else "#1890ff")
    bg_color = "#f6ffed" if kind == "tip" else ("#fffbe6" if kind == "warn" else "#e6f7ff")
    return f"""<div style="background:{bg_color};border-left:4px solid {border_color};padding:16px 20px;border-radius:6px;margin:24px 0;font-size:15px;line-height:1.6">
  <strong style="color:#282828">{title}</strong>
  <div style="margin-top:6px;color:#333">{text}</div>
</div>"""

LESSONS_CONTENT = [
    {
        "num": 1,
        "filename": "001 Python Execution Model, CPython & Architecture.html",
        "title": "Python Execution Model, CPython & Architecture",
        "body": f"""
<p>Python is commonly known as an interpreted scripting language, but in standard implementations (CPython), it operates via a dual-phase <strong>compilation and virtual machine interpretation</strong> architecture. Understanding this internal execution pipeline is fundamental for writing high-performance, memory-efficient Python code and excelling in systems-level technical interviews.</p>

<h2>1. The Four-Stage Execution Pipeline</h2>
<p>When you invoke <code>python app.py</code>, CPython does not interpret raw text line-by-line. Instead, it processes your code through four specialized subsystems:</p>

{make_figure('''<svg width="740" height="200" viewBox="0 0 740 200" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="740" height="200" rx="10" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1.5"/>
  <!-- Source Code -->
  <rect x="25" y="60" width="130" height="80" rx="8" fill="#ffffff" stroke="#1890ff" stroke-width="2"/>
  <text x="90" y="95" fill="#1e293b" font-family="-apple-system, sans-serif" font-size="14" font-weight="700" text-anchor="middle">Source Code</text>
  <text x="90" y="118" fill="#64748b" font-family="-apple-system, sans-serif" font-size="12" text-anchor="middle">script.py (UTF-8)</text>
  
  <path d="M160 100 H195" stroke="#94a3b8" stroke-width="2" stroke-dasharray="4 4"/>
  
  <!-- Tokenizer & AST -->
  <rect x="200" y="60" width="140" height="80" rx="8" fill="#ffffff" stroke="#722ed1" stroke-width="2"/>
  <text x="270" y="95" fill="#1e293b" font-family="-apple-system, sans-serif" font-size="14" font-weight="700" text-anchor="middle">Tokenizer & AST</text>
  <text x="270" y="118" fill="#64748b" font-family="-apple-system, sans-serif" font-size="12" text-anchor="middle">Grammar Validation</text>

  <path d="M345 100 H380" stroke="#94a3b8" stroke-width="2" stroke-dasharray="4 4"/>

  <!-- Bytecode -->
  <rect x="385" y="60" width="145" height="80" rx="8" fill="#ffffff" stroke="#eb2f96" stroke-width="2"/>
  <text x="457" y="95" fill="#1e293b" font-family="-apple-system, sans-serif" font-size="14" font-weight="700" text-anchor="middle">Bytecode (.pyc)</text>
  <text x="457" y="118" fill="#64748b" font-family="-apple-system, sans-serif" font-size="12" text-anchor="middle">PyCodeObject</text>

  <path d="M535 100 H570" stroke="#94a3b8" stroke-width="2" stroke-dasharray="4 4"/>

  <!-- CPython PVM -->
  <rect x="575" y="60" width="140" height="80" rx="8" fill="#ffffff" stroke="#05673d" stroke-width="2"/>
  <text x="645" y="95" fill="#1e293b" font-family="-apple-system, sans-serif" font-size="14" font-weight="700" text-anchor="middle">CPython PVM</text>
  <text x="645" y="118" fill="#05673d" font-family="-apple-system, sans-serif" font-size="12" font-weight="600" text-anchor="middle">ceval.c Eval Loop</text>
</svg>''')}

<ol>
  <li><strong>Lexing & Parsing:</strong> Converts source characters into tokens and constructs an Abstract Syntax Tree (AST). Syntax errors are raised exclusively here.</li>
  <li><strong>Bytecode Generation:</strong> The AST compiler converts nodes into compact bytecode opcodes stored in a <code>PyCodeObject</code>.</li>
  <li><strong>Bytecode Caching (<code>__pycache__</code>):</strong> The bytecode is written to <code>.pyc</code> files containing a magic number header and timestamp/hash. If unchanged, future runs bypass compilation.</li>
  <li><strong>PVM Evaluation Loop:</strong> The virtual machine (a stack-based interpreter implemented in C) reads opcodes sequentially and manipulates the evaluation stack.</li>
</ol>

<h2>2. Disassembling Python Bytecode with <code>dis</code></h2>
<p>CPython operates as a <strong>stack machine</strong> rather than a register machine (like x86 or ARM). Operands are pushed onto an internal evaluation stack, modified, and popped.</p>

{make_code_tab('''import dis

def compute_tax(subtotal, rate=0.08):
    tax = subtotal * rate
    return subtotal + tax

dis.dis(compute_tax)''')}

<p><strong>Bytecode Output Breakdown:</strong></p>
{make_code_tab('''  2           0 LOAD_FAST                0 (subtotal)
              2 LOAD_FAST                1 (rate)
              4 BINARY_MULTIPLY
              6 STORE_FAST               2 (tax)

  3           8 LOAD_FAST                0 (subtotal)
             10 LOAD_FAST                2 (tax)
             12 BINARY_ADD
             14 RETURN_VALUE''', lang="text")}

{make_callout("💡 Key Observation for Senior Engineers", "Local variables inside a function use <code>LOAD_FAST</code> and <code>STORE_FAST</code> (O(1) direct array pointer lookups in the frame object) rather than <code>LOAD_NAME</code> or <code>LOAD_GLOBAL</code> (O(1) dictionary lookups). Local variables in Python functions are resolved with zero hash overhead!")}

<h2>3. Python Implementations: CPython vs PyPy vs Others</h2>
<table class="table-custom">
  <thead>
    <tr>
      <th>Implementation</th>
      <th>Engine</th>
      <th>JIT Enabled?</th>
      <th>Key Strengths & Target Use Cases</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>CPython</strong></td>
      <td>C</td>
      <td>No (Adaptive Interpreter in 3.11+)</td>
      <td>Standard ecosystem reference, 100% C-Extension (NumPy, PyTorch, Pandas) compatibility.</td>
    </tr>
    <tr>
      <td><strong>PyPy</strong></td>
      <td>RPython</td>
      <td>Yes (Tracing JIT)</td>
      <td>4x-8x speedup on pure-Python CPU loops. Higher memory footprint.</td>
    </tr>
    <tr>
      <td><strong>Jython</strong></td>
      <td>Java / JVM</td>
      <td>JVM JIT</td>
      <td>Direct integration with Java enterprise libraries and JVM threading.</td>
    </tr>
  </tbody>
</table>

{make_callout("🎯 Interview Summary Checklist", """<ul>
  <li>Explain the difference between a <code>FunctionObject</code> (mutable, holds closure/globals) and a <code>CodeObject</code> (immutable, holds compiled bytecode).</li>
  <li>Why does CPython use a stack-based VM instead of a register-based VM? (Simpler opcode generation, platform-independent bytecode portability).</li>
</ul>""", kind="tip")}
"""
    },
    {
        "num": 2,
        "filename": "002 Variables, Mutability, Memory & Object Model.html",
        "title": "Variables, Mutability, Memory & Object Model",
        "body": f"""
<p>In Python, <strong>everything is an object</strong>. Variables are not memory boxes that hold values; they are <strong>named references (pointers)</strong> bound to objects in heap memory. Grasping Python's object model and mutability is essential for avoiding catastrophic reference bugs in production.</p>

<h2>1. The Anatomy of a Python Object (<code>PyObject</code>)</h2>
<p>Every object in CPython has a C structure header called <code>PyObject</code> containing two fundamental fields:</p>
<ul>
  <li><code>ob_refcnt</code>: An integer tracking how many references point to this object (used for Garbage Collection).</li>
  <li><code>ob_type</code>: A pointer to the object's type descriptor (which dictates its methods, size, and behavior).</li>
</ul>

{make_figure('''<svg width="740" height="180" viewBox="0 0 740 180" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="740" height="180" rx="10" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1.5"/>
  <!-- Stack Frame -->
  <rect x="30" y="35" width="160" height="110" rx="8" fill="#ffffff" stroke="#1890ff" stroke-width="2"/>
  <text x="110" y="65" fill="#1e293b" font-family="-apple-system, sans-serif" font-size="13" font-weight="700" text-anchor="middle">Stack Frame / Scope</text>
  <text x="50" y="98" fill="#0958d9" font-family="monospace" font-size="13">a = [1, 2]</text>
  <text x="50" y="125" fill="#0958d9" font-family="monospace" font-size="13">b = a</text>

  <!-- Pointers -->
  <path d="M150 95 H290" stroke="#1890ff" stroke-width="2"/>
  <path d="M150 120 L290 98" stroke="#1890ff" stroke-width="2"/>

  <!-- Heap Object -->
  <rect x="300" y="30" width="410" height="120" rx="8" fill="#ffffff" stroke="#05673d" stroke-width="2"/>
  <text x="505" y="58" fill="#05673d" font-family="-apple-system, sans-serif" font-size="13" font-weight="700" text-anchor="middle">PyListObject (Heap Address: 0x7ffd9a00)</text>
  
  <rect x="320" y="75" width="110" height="55" rx="6" fill="#f0fdf4" stroke="#86efac"/>
  <text x="375" y="96" fill="#64748b" font-size="11" text-anchor="middle">ob_refcnt</text>
  <text x="375" y="118" fill="#05673d" font-size="15" font-weight="700" text-anchor="middle">2</text>

  <rect x="445" y="75" width="110" height="55" rx="6" fill="#f0fdf4" stroke="#86efac"/>
  <text x="500" y="96" fill="#64748b" font-size="11" text-anchor="middle">ob_type</text>
  <text x="500" y="118" fill="#05673d" font-size="14" font-weight="700" text-anchor="middle">&list_type</text>

  <rect x="570" y="75" width="120" height="55" rx="6" fill="#f0fdf4" stroke="#86efac"/>
  <text x="630" y="96" fill="#64748b" font-size="11" text-anchor="middle">items pointer</text>
  <text x="630" y="118" fill="#0958d9" font-size="13" font-weight="700" text-anchor="middle">[0x1, 0x2]</text>
</svg>''')}

<h2>2. Mutable vs Immutable Types</h2>
<table class="table-custom">
  <thead>
    <tr>
      <th>Mutability Category</th>
      <th>Python Types</th>
      <th>In-Place Modification Possible?</th>
      <th>Hashable (Usable as Dict Keys)?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Immutable</strong></td>
      <td><code>int</code>, <code>float</code>, <code>str</code>, <code>tuple</code>, <code>frozenset</code>, <code>bytes</code></td>
      <td>❌ No (Creates a new object in memory)</td>
      <td>✅ Yes (If all nested contents are immutable)</td>
    </tr>
    <tr>
      <td><strong>Mutable</strong></td>
      <td><code>list</code>, <code>dict</code>, <code>set</code>, <code>bytearray</code>, custom classes</td>
      <td>✅ Yes (Mutates existing heap buffer)</td>
      <td>❌ No (Un-hashable)</td>
    </tr>
  </tbody>
</table>

<h2>3. Equality (<code>==</code>) vs Identity (<code>is</code>)</h2>
{make_code_tab('''# Equality compares contents; Identity compares memory addresses (id)
list1 = [1, 2, 3]
list2 = [1, 2, 3]

print(list1 == list2) # True (Values match)
print(list1 is list2) # False (Distinct memory addresses: id(list1) != id(list2))

# Small Integer Caching (-5 to 256)
x = 256
y = 256
print(x is y) # True (Shared singleton from CPython pre-allocated pool)

big1 = 1000000
big2 = 1000000
print(big1 is big2) # False (Allocated separately)''')}

{make_callout("⚠️ The Notorious Default Argument Pitfall", """<p>In Python, default arguments are evaluated <strong>once at function definition time</strong>, not each time the function is called:</p>
<pre><code class="hljs language-python"># DANGEROUS:
def add_item(val, target=[]):
    target.append(val)
    return target

# CORRECT:
def add_item_safe(val, target=None):
    if target is None:
        target = []
    target.append(val)
    return target</code></pre>""", kind="warn")}
"""
    },
    {
        "num": 3,
        "filename": "003 Data Structures Deep Dive - Lists, Tuples, Sets, Dictionaries.html",
        "title": "Data Structures Deep Dive - Lists, Tuples, Sets, Dictionaries",
        "body": f"""
<p>Python's built-in data structures are engineered for extreme developer ergonomics and amortized high-speed execution. In this lesson, we examine their internal memory layouts, hashing algorithms, and asymptotic complexity guarantees.</p>

<h2>1. Dynamic Arrays: How <code>list</code> Works Internally</h2>
<p>A Python <code>list</code> is implemented in C as an <strong>array of pointers</strong> (<code>PyObject**</code>), not a linked list. When elements are appended, CPython employs an over-allocation growth strategy to guarantee <strong>O(1) amortized append</strong> operations:</p>

{make_figure('''<svg width="740" height="180" viewBox="0 0 740 180" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="740" height="180" rx="10" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1.5"/>
  <rect x="40" y="45" width="660" height="90" rx="8" fill="#ffffff" stroke="#05673d" stroke-width="2"/>
  <text x="370" y="75" fill="#05673d" font-family="-apple-system, sans-serif" font-size="14" font-weight="700" text-anchor="middle">PyListObject Memory Buffer (Over-allocated Growth: 0 -> 4 -> 8 -> 16 -> 25...)</text>
  
  <rect x="70" y="90" width="100" height="35" rx="4" fill="#dcfce7" stroke="#86efac"/>
  <text x="120" y="112" fill="#166534" font-family="monospace" font-size="12" text-anchor="middle">[0] -> Item 1</text>

  <rect x="180" y="90" width="100" height="35" rx="4" fill="#dcfce7" stroke="#86efac"/>
  <text x="230" y="112" fill="#166534" font-family="monospace" font-size="12" text-anchor="middle">[1] -> Item 2</text>

  <rect x="290" y="90" width="100" height="35" rx="4" fill="#dcfce7" stroke="#86efac"/>
  <text x="340" y="112" fill="#166534" font-family="monospace" font-size="12" text-anchor="middle">[2] -> Item 3</text>

  <rect x="400" y="90" width="120" height="35" rx="4" fill="#f1f5f9" stroke="#cbd5e1" stroke-dasharray="3 3"/>
  <text x="460" y="112" fill="#94a3b8" font-family="monospace" font-size="12" text-anchor="middle">[3] NULL (Free)</text>

  <rect x="530" y="90" width="140" height="35" rx="4" fill="#f1f5f9" stroke="#cbd5e1" stroke-dasharray="3 3"/>
  <text x="600" y="112" fill="#94a3b8" font-family="monospace" font-size="12" text-anchor="middle">[4] NULL (Reserved)</text>
</svg>''')}

<table class="table-custom">
  <thead>
    <tr>
      <th>Operation</th>
      <th>Average Complexity</th>
      <th>Worst Case Complexity</th>
      <th>Internal Mechanism</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>list[i]</code> (Indexing)</td>
      <td><strong>O(1)</strong></td>
      <td><strong>O(1)</strong></td>
      <td>Direct array pointer offset calculation</td>
    </tr>
    <tr>
      <td><code>list.append(x)</code></td>
      <td><strong>O(1)</strong></td>
      <td><strong>O(N)</strong></td>
      <td>Amortized O(1); O(N) when buffer reallocation occurs</td>
    </tr>
    <tr>
      <td><code>list.insert(0, x)</code></td>
      <td><strong>O(N)</strong></td>
      <td><strong>O(N)</strong></td>
      <td>Must shift all subsequent N elements right in memory</td>
    </tr>
  </tbody>
</table>

<h2>2. Compact Hash Table: Python 3.7+ <code>dict</code></h2>
<p>Since Python 3.7, dictionaries maintain insertion order while saving memory using a <strong>two-array sparse + dense design</strong>:</p>

{make_figure('''<svg width="740" height="190" viewBox="0 0 740 190" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="740" height="190" rx="10" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1.5"/>
  <!-- Sparse Indices -->
  <rect x="30" y="35" width="280" height="120" rx="8" fill="#ffffff" stroke="#1890ff" stroke-width="2"/>
  <text x="170" y="60" fill="#1890ff" font-family="-apple-system, sans-serif" font-size="13" font-weight="700" text-anchor="middle">Sparse Indices Array (int8)</text>
  <text x="170" y="82" fill="#64748b" font-family="monospace" font-size="11" text-anchor="middle">hash(key) % 8 = index</text>
  <rect x="45" y="100" width="250" height="35" rx="4" fill="#eff6ff" stroke="#bfdbfe"/>
  <text x="170" y="122" fill="#1d4ed8" font-family="monospace" font-size="12" text-anchor="middle">[-1, 0, -1, 1, -1, -1, 2, -1]</text>

  <!-- Dense Table -->
  <rect x="330" y="35" width="380" height="120" rx="8" fill="#ffffff" stroke="#05673d" stroke-width="2"/>
  <text x="520" y="60" fill="#05673d" font-family="-apple-system, sans-serif" font-size="13" font-weight="700" text-anchor="middle">Dense Entries Table (In Insertion Order)</text>
  <rect x="345" y="80" width="350" height="22" rx="4" fill="#f0fdf4"/>
  <text x="355" y="96" fill="#166534" font-family="monospace" font-size="11">0: [hash, key="user", val="Alice"]</text>
  <rect x="345" y="105" width="350" height="22" rx="4" fill="#f0fdf4"/>
  <text x="355" y="121" fill="#166534" font-family="monospace" font-size="11">1: [hash, key="role", val="Admin"]</text>
  <rect x="345" y="130" width="350" height="22" rx="4" fill="#f0fdf4"/>
  <text x="355" y="146" fill="#166534" font-family="monospace" font-size="11">2: [hash, key="tier", val="Pro"]</text>
</svg>''')}
"""
    },
    {
        "num": 4,
        "filename": "004 Functions, Closures & Scope (LEGB Rule).html",
        "title": "Functions, Closures & Scope (LEGB Rule)",
        "body": f"""
<p>Functions in Python are <strong>first-class objects</strong>. They can be dynamically defined, assigned to variables, passed across namespaces, and bind lexical scope environments via closures.</p>

<h2>1. Scope Resolution: The LEGB Rule</h2>
<p>When Python resolves any variable identifier, it traverses four scopes in strict sequential order:</p>

{make_figure('''<svg width="740" height="190" viewBox="0 0 740 190" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="740" height="190" rx="10" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1.5"/>
  <!-- Concentric Circles/Boxes -->
  <rect x="40" y="30" width="140" height="130" rx="8" fill="#dcfce7" stroke="#10b981" stroke-width="2"/>
  <text x="110" y="70" fill="#065f46" font-size="16" font-weight="700" text-anchor="middle">1. Local</text>
  <text x="110" y="100" fill="#047857" font-size="12" text-anchor="middle">Inside function</text>

  <rect x="210" y="30" width="140" height="130" rx="8" fill="#e0e7ff" stroke="#6366f1" stroke-width="2"/>
  <text x="280" y="70" fill="#3730a3" font-size="16" font-weight="700" text-anchor="middle">2. Enclosing</text>
  <text x="280" y="100" fill="#4338ca" font-size="12" text-anchor="middle">Nested closures</text>

  <rect x="380" y="30" width="140" height="130" rx="8" fill="#fce7f3" stroke="#ec4899" stroke-width="2"/>
  <text x="450" y="70" fill="#831843" font-size="16" font-weight="700" text-anchor="middle">3. Global</text>
  <text x="450" y="100" fill="#9d174d" font-size="12" text-anchor="middle">Module level</text>

  <rect x="550" y="30" width="150" height="130" rx="8" fill="#ffedd5" stroke="#f97316" stroke-width="2"/>
  <text x="625" y="70" fill="#7c2d12" font-size="16" font-weight="700" text-anchor="middle">4. Built-in</text>
  <text x="625" y="100" fill="#9a3412" font-size="12" text-anchor="middle">len, range, dict</text>
</svg>''')}

<h2>2. Closures & Cell Objects</h2>
<p>When an inner function references an enclosing variable, Python wraps that variable in a <code>cell</code> object in heap memory so it persists even after the outer function frame returns:</p>

{make_code_tab('''def make_rate_limiter(max_requests):
    count = 0
    def allow_request():
        nonlocal count
        if count < max_requests:
            count += 1
            return True
        return False
    return allow_request

limiter = make_rate_limiter(2)
print(limiter()) # True
print(limiter()) # True
print(limiter()) # False (Limit reached!)
print(limiter.__closure__[0].cell_contents) # 2''')}
"""
    },
    {
        "num": 5,
        "filename": "005 Object-Oriented Programming & Dunder Methods.html",
        "title": "Object-Oriented Programming & Dunder Methods",
        "body": f"""
<p>Python's object-oriented architecture relies on <strong>Special Methods (Dunder Methods)</strong>. By implementing these hooks, custom classes integrate seamlessly with Python's built-in operators, iteration systems, and type checking.</p>

<h2>1. Core Dunder Protocols</h2>
<table class="table-custom">
  <thead>
    <tr>
      <th>Protocol</th>
      <th>Dunder Method</th>
      <th>Invoked By</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Representation</strong></td>
      <td><code>__str__</code>, <code>__repr__</code></td>
      <td><code>print(obj)</code>, <code>repr(obj)</code></td>
    </tr>
    <tr>
      <td><strong>Comparison</strong></td>
      <td><code>__eq__</code>, <code>__lt__</code>, <code>__hash__</code></td>
      <td><code>a == b</code>, <code>a &lt; b</code>, <code>hash(a)</code></td>
    </tr>
    <tr>
      <td><strong>Container</strong></td>
      <td><code>__len__</code>, <code>__getitem__</code>, <code>__contains__</code></td>
      <td><code>len(c)</code>, <code>c[key]</code>, <code>x in c</code></td>
    </tr>
    <tr>
      <td><strong>Callable</strong></td>
      <td><code>__call__</code></td>
      <td><code>instance(*args)</code></td>
    </tr>
  </tbody>
</table>

<h2>2. Complete Pythonic Vector Example</h2>
{make_code_tab('''class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        
    def __repr__(self) -> str:
        return f"Vector({self.x!r}, {self.y!r})"
        
    def __add__(self, other: "Vector") -> "Vector":
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x == other.x and self.y == other.y

v1 = Vector(3, 4)
v2 = Vector(1, 2)
print(v1 + v2) # Vector(4, 6)
print(v1 == Vector(3, 4)) # True''')}
"""
    },
    {
        "num": 6,
        "filename": "006 Inheritance, MRO & The C3 Linearization Algorithm.html",
        "title": "Inheritance, MRO & The C3 Linearization Algorithm",
        "body": f"""
<p>Python resolves multiple inheritance using the <strong>Method Resolution Order (MRO)</strong>, computed via the deterministic <strong>C3 Linearization Algorithm</strong>. This eliminates the ambiguities of the classic Diamond Problem and enables cooperative multiple inheritance via <code>super()</code>.</p>

<h2>1. The Diamond Hierarchy & C3 Merge</h2>
{make_figure('''<svg width="740" height="210" viewBox="0 0 740 210" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="740" height="210" rx="10" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1.5"/>
  <!-- Class A -->
  <rect x="310" y="20" width="120" height="40" rx="6" fill="#eff6ff" stroke="#1890ff" stroke-width="2"/>
  <text x="370" y="45" fill="#1e293b" font-size="14" font-weight="700" text-anchor="middle">Class A</text>

  <!-- Class B & C -->
  <rect x="180" y="85" width="120" height="40" rx="6" fill="#f3e8ff" stroke="#722ed1" stroke-width="2"/>
  <text x="240" y="110" fill="#1e293b" font-size="14" font-weight="700" text-anchor="middle">Class B(A)</text>

  <rect x="440" y="85" width="120" height="40" rx="6" fill="#f3e8ff" stroke="#722ed1" stroke-width="2"/>
  <text x="500" y="110" fill="#1e293b" font-size="14" font-weight="700" text-anchor="middle">Class C(A)</text>

  <!-- Class D -->
  <rect x="310" y="150" width="120" height="40" rx="6" fill="#fce7f3" stroke="#eb2f96" stroke-width="2"/>
  <text x="370" y="175" fill="#1e293b" font-size="14" font-weight="700" text-anchor="middle">Class D(B, C)</text>

  <path d="M370 150 L240 125" stroke="#94a3b8" stroke-width="2"/>
  <path d="M370 150 L500 125" stroke="#94a3b8" stroke-width="2"/>
  <path d="M240 85 L370 60" stroke="#94a3b8" stroke-width="2"/>
  <path d="M500 85 L370 60" stroke="#94a3b8" stroke-width="2"/>
</svg>''')}

<h2>2. Inspecting MRO at Runtime</h2>
{make_code_tab('''class A:
    def ping(self): print("A")

class B(A):
    def ping(self):
        print("B")
        super().ping()

class C(A):
    def ping(self):
        print("C")
        super().ping()

class D(B, C):
    def ping(self):
        print("D")
        super().ping()

d = D()
d.ping()
# Output order: D -> B -> C -> A
print([cls.__name__ for cls in D.__mro__])
# ['D', 'B', 'C', 'A', 'object']''')}
"""
    },
    {
        "num": 7,
        "filename": "007 Advanced Decorators & Function Wrappers.html",
        "title": "Advanced Decorators & Function Wrappers",
        "body": f"""
<p>Decorators enable clean metaprogramming by wrapping functions or classes to augment their behavior with cross-cutting concerns (authentication, telemetry, caching, rate-limiting) without polluting core logic.</p>

<h2>1. Creating Production-Grade Decorators with <code>functools.wraps</code></h2>
{make_code_tab('''import time
import functools
import logging

def retry(max_attempts=3, delay_sec=1.0):
    def decorator(func):
        @functools.wraps(func) # Preserves docstrings, signatures & __name__
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    logging.warning(f"Attempt {attempts} failed: {e}. Retrying...")
                    time.sleep(delay_sec)
            return func(*args, **kwargs) # Final attempt
        return wrapper
    return decorator

@retry(max_attempts=3, delay_sec=0.5)
def call_flaky_api():
    # Network request simulation
    return {"status": "ok"}''')}
"""
    },
    {
        "num": 8,
        "filename": "008 Iterators, Iterables & Generators.html",
        "title": "Iterators, Iterables & Generators",
        "body": f"""
<p>Generators allow streaming evaluation of massive datasets with <strong>O(1) memory complexity</strong> by pausing and resuming function state via the <code>yield</code> keyword.</p>

<h2>1. Generator Execution Mechanics</h2>
{make_figure('''<svg width="740" height="170" viewBox="0 0 740 170" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="740" height="170" rx="10" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1.5"/>
  <rect x="40" y="40" width="180" height="90" rx="8" fill="#ffffff" stroke="#1890ff" stroke-width="2"/>
  <text x="130" y="75" fill="#1e293b" font-size="14" font-weight="700" text-anchor="middle">Caller Invokes next()</text>
  <text x="130" y="100" fill="#64748b" font-size="12" text-anchor="middle">Requests next item</text>

  <path d="M225 85 H330" stroke="#05673d" stroke-width="2" stroke-dasharray="4 4"/>

  <rect x="340" y="40" width="360" height="90" rx="8" fill="#ffffff" stroke="#05673d" stroke-width="2"/>
  <text x="520" y="70" fill="#05673d" font-size="14" font-weight="700" text-anchor="middle">Generator Frame State</text>
  <text x="520" y="95" fill="#1e293b" font-size="12" text-anchor="middle">Executes until `yield val` -> Pauses -> Emits item</text>
  <text x="520" y="115" fill="#64748b" font-size="11" text-anchor="middle">Local registers & instruction pointer frozen in RAM</text>
</svg>''')}

<h2>2. Streaming Huge Files with O(1) RAM</h2>
{make_code_tab('''def stream_large_dataset(filepath, chunk_size=64*1024):
    """Processes arbitrarily large files without exhausting RAM."""
    with open(filepath, 'r', encoding='utf-8') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

# Streams a 50GB file with constant memory usage!
for block in stream_large_dataset("access.log"):
    analyze_block(block)''')}
"""
    },
    {
        "num": 9,
        "filename": "009 Context Managers & The with Statement.html",
        "title": "Context Managers & The with Statement",
        "body": f"""
<p>Context managers ensure deterministic resource acquisition and release (RAII pattern in Python), preventing memory leaks, socket starvation, and unclosed database transactions.</p>

<h2>1. The Context Manager Protocol</h2>
{make_code_tab('''class DatabaseTransaction:
    def __init__(self, db_client):
        self.client = db_client

    def __enter__(self):
        self.client.begin_transaction()
        return self.client

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.client.rollback()
            print(f"Transaction aborted due to error: {exc_val}")
            return False # Propagate exception
        self.client.commit()
        return True''')}
"""
    },
    {
        "num": 10,
        "filename": "010 Concurrency I - Threads, Processes & the Global Interpreter Lock (GIL).html",
        "title": "Concurrency I - Threads, Processes & the Global Interpreter Lock (GIL)",
        "body": f"""
<p>Concurrency in Python requires choosing the right tool for the job. The <strong>Global Interpreter Lock (GIL)</strong> is a mutex preventing multiple native OS threads from executing CPython bytecode simultaneously on multiple CPU cores.</p>

<h2>1. CPU-Bound vs I/O-Bound Decision Matrix</h2>
<table class="table-custom">
  <thead>
    <tr>
      <th>Task Type</th>
      <th>Bottleneck</th>
      <th>Recommended Concurrency Model</th>
      <th>Reasoning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>I/O Bound</strong> (HTTP calls, DB queries)</td>
      <td>Network / Disk Latency</td>
      <td><code>asyncio</code> or <code>ThreadPoolExecutor</code></td>
      <td>The GIL is automatically released during OS socket/file wait times.</td>
    </tr>
    <tr>
      <td><strong>CPU Bound</strong> (Image processing, ML)</td>
      <td>CPU Instructions</td>
      <td><code>ProcessPoolExecutor</code> or Native C-Extensions</td>
      <td>Spawns independent OS processes with separate CPython heaps and PVMs.</td>
    </tr>
  </tbody>
</table>
"""
    },
    {
        "num": 11,
        "filename": "011 Concurrency II - Asynchronous Programming with Asyncio.html",
        "title": "Concurrency II - Asynchronous Programming with Asyncio",
        "body": f"""
<p><code>asyncio</code> enables single-threaded cooperative multitasking using an <strong>event loop</strong> to manage thousands of concurrent I/O connections with minimal memory overhead.</p>

<h2>1. High-Performance Concurrent Requests</h2>
{make_code_tab('''import asyncio
import httpx

async def fetch_endpoint(client, url):
    resp = await client.get(url)
    return url, resp.status_code

async def main():
    urls = ["https://httpbin.org/delay/1" for _ in range(50)]
    async with httpx.AsyncClient() as client:
        tasks = [fetch_endpoint(client, u) for u in urls]
        # Runs 50 network requests concurrently in ~1.2 seconds!
        results = await asyncio.gather(*tasks)
        print(f"Successfully processed {len(results)} responses.")

if __name__ == "__main__":
    asyncio.run(main())''')}
"""
    },
    {
        "num": 12,
        "filename": "012 Metaclasses & Class Creation Mechanics.html",
        "title": "Metaclasses & Class Creation Mechanics",
        "body": f"""
<p>If classes are blueprints for objects, <strong>metaclasses are blueprints for classes</strong>. Metaclasses allow frameworks (like Django ORM or Pydantic) to inspect, validate, and alter class structures at import time.</p>

<h2>1. Validating API Contracts with Metaclasses</h2>
{make_code_tab('''class EnforceDocstringsMeta(type):
    def __new__(cls, name, bases, dct):
        for attr_name, attr_val in dct.items():
            if callable(attr_val) and not attr_name.startswith("__"):
                if not attr_val.__doc__:
                    raise TypeError(f"Method '{attr_name}' in class '{name}' must have a docstring!")
        return super().__new__(cls, name, bases, dct)

class BaseService(metaclass=EnforceDocstringsMeta):
    pass

class PaymentService(BaseService):
    def charge(self, amount):
        """Processes credit card charge."""
        return True''')}
"""
    },
    {
        "num": 13,
        "filename": "013 Memory Management, Garbage Collection & CPython Internals.html",
        "title": "Memory Management, Garbage Collection & CPython Internals",
        "body": f"""
<p>CPython memory management combines <strong>PyMalloc (small object allocator)</strong>, <strong>Reference Counting</strong>, and a <strong>Generational Cyclic Garbage Collector</strong>.</p>

<h2>1. Three-Generation Cyclic Garbage Collector</h2>
<ul>
  <li><strong>Generation 0:</strong> Newly allocated objects. Collected frequently.</li>
  <li><strong>Generation 1:</strong> Objects surviving Gen 0 collections.</li>
  <li><strong>Generation 2:</strong> Long-lived objects (e.g. module imports, singletons). Collected rarely.</li>
</ul>

{make_callout("💡 Memory Optimization: __slots__", """<p>Defining <code>__slots__ = ('x', 'y')</code> in a class prevents creation of the instance <code>__dict__</code>, reducing memory consumption per instance by over <strong>60%</strong>!</p>""", kind="tip")}
"""
    },
    {
        "num": 14,
        "filename": "014 Performance Optimization, Profiling & C-Extensions.html",
        "title": "Performance Optimization, Profiling & C-Extensions",
        "body": f"""
<p>Optimizing Python code requires scientific profiling with <code>cProfile</code>, eliminating algorithmic bottlenecks, and delegating compute kernels to native C/Rust extensions.</p>

<h2>1. Profiling with <code>cProfile</code></h2>
{make_code_tab('''import cProfile
import pstats

def heavy_computation():
    return sum(i * i for i in range(1_000_000))

profiler = cProfile.Profile()
profiler.enable()
heavy_computation()
profiler.disable()

stats = pstats.Stats(profiler).sort_stats('cumtime')
stats.print_stats(10)''')}
"""
    },
    {
        "num": 15,
        "filename": "015 Python Testing, Type Annotations & Production Best Practices.html",
        "title": "Python Testing, Type Annotations & Production Best Practices",
        "body": f"""
<p>Writing production-grade Python requires modern static type hinting (PEP 484), robust automated test suites with <code>pytest</code>, and clean modular architecture.</p>

<h2>1. Structural Subtyping with <code>typing.Protocol</code></h2>
{make_code_tab('''from typing import Protocol, TypeVar

class Serializable(Protocol):
    def to_json(self) -> str:
        ...

T = TypeVar('T', bound=Serializable)

def export_record(item: T) -> str:
    return item.to_json()''')}
"""
    }
]

def build_course():
    os.makedirs('Python Course', exist_ok=True)
    
    for lesson in LESSONS_CONTENT:
        num_str = f"{lesson['num']:02d}"
        
        # Build sider menu items in authentic ByteByteGo menu item style
        sider_items = ""
        for item in LESSONS_CONTENT:
            is_active = (item['num'] == lesson['num'])
            selected_cls = " ant-menu-item-selected" if is_active else ""
            sider_items += f"""
<li class="ant-menu-item{selected_cls}" role="menuitem" style="padding-left:16px;">
  <a href="{item['filename']}" style="display:flex;align-items:center;color:inherit;text-decoration:none;width:100%;height:100%;">
    <span style="font-family:monospace;font-size:11px;background:rgba(255,255,255,0.15);padding:2px 5px;border-radius:3px;margin-right:8px;color:#fff;">{item['num']:02d}</span>
    <span style="font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{item['title']}</span>
  </a>
</li>"""

        # Build custom aside
        custom_aside = f"""<aside class="ant-layout-sider style_sider__Hlcz3 css-133v4sd" style="flex:0 0 300px;max-width:300px;min-width:300px;width:300px;">
  <div class="ant-layout-sider-children">
    <h2 style="padding:10px 16px 6px;font-size:14px;color:#aaa;font-weight:600;margin:0;">Python Masterclass</h2>
    <ul class="ant-menu ant-menu-root ant-menu-inline ant-menu-dark css-133v4sd" role="menu">
      {sider_items}
    </ul>
  </div>
</aside>"""

        # Replace aside in head_shell
        head = re.sub(r'<aside[^>]*>.*?</aside>', custom_aside, HEAD_TEMPLATE, flags=re.DOTALL)
        
        # Bottom Prev/Next navigation buttons
        prev_btn = ""
        if lesson['num'] > 1:
            prev_l = LESSONS_CONTENT[lesson['num'] - 2]
            prev_btn = f'<a href="{prev_l["filename"]}" class="ant-btn ant-btn-default" style="display:inline-flex;align-items:center;gap:6px;border-radius:6px;font-weight:600;">← {prev_l["title"]}</a>'
        else:
            prev_btn = '<a href="../index.html" class="ant-btn ant-btn-default" style="display:inline-flex;align-items:center;gap:6px;border-radius:6px;font-weight:600;">← Back to Hub</a>'

        next_btn = ""
        if lesson['num'] < len(LESSONS_CONTENT):
            next_l = LESSONS_CONTENT[lesson['num']]
            next_btn = f'<a href="{next_l["filename"]}" class="ant-btn ant-btn-primary" style="display:inline-flex;align-items:center;gap:6px;border-radius:6px;font-weight:600;background:#05673d;border-color:#05673d;color:#fff;">Next: {next_l["title"]} →</a>'
        else:
            next_btn = '<a href="../index.html" class="ant-btn ant-btn-primary" style="display:inline-flex;align-items:center;gap:6px;border-radius:6px;font-weight:600;background:#05673d;border-color:#05673d;color:#fff;">🎓 Course Completed! Back to Hub →</a>'

        article_html = f"""<article class="style_learnContent__K5K7M">
  <header>
    <strong class="style_chapter__grtAe">{num_str}</strong>
    <h1>{lesson['title']}</h1>
  </header>
  {lesson['body']}
  <div style="display:flex;justify-content:space-between;border-top:1px solid #dedede;padding-top:24px;margin-top:40px;">
    {prev_btn}
    {next_btn}
  </div>
</article>"""

        full_html = head + article_html + FOOT_TEMPLATE
        
        # Add nav inject scripts
        if "nav_inject.js" not in full_html:
            full_html += """
<!-- nav-inject-patched -->
<script src="../nav_map.js"></script>
<script src="../nav_inject.js"></script>
"""
        target_path = os.path.join('Python Course', lesson['filename'])
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(full_html)

    print(f"Successfully generated all {len(LESSONS_CONTENT)} authentic ByteByteGo lessons!")

if __name__ == '__main__':
    build_course()
