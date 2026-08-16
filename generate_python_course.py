"""
generate_python_course.py — Generates all 15 complete, rich ByteByteGo-style lesson HTML files for Python Masterclass.
"""
import os
import json

HTML_SHELL_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0">
<title>ByteByteGo | Python Masterclass: {title}</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/github.min.css">
<style>
/* Base ByteByteGo Reset & Fonts */
*, *:before, *:after { box-sizing: border-box; }
body {
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  color: #212529;
  background-color: #f2f2f2;
  -webkit-font-smoothing: antialiased;
  line-height: 1.6;
}
a { color: #1677ff; text-decoration: none; }
a:hover { color: #69b1ff; }

/* ByteByteGo Top Header */
.style_header__IrB9Y {
  position: fixed;
  top: 0; left: 0; right: 0;
  height: 64px;
  background: #ffffff;
  border-bottom: 1px solid #dedede;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 32px;
  z-index: 100;
}
.brand-title {
  font-weight: 700;
  font-size: 18px;
  color: #05673d;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Layout */
.style_learn__wJdK1 {
  display: flex;
  margin-top: 64px;
  min-height: calc(100vh - 64px);
}

/* Sider Menu */
.style_sider__Hlcz3 {
  width: 320px;
  background: #484848;
  color: #fff;
  flex-shrink: 0;
  overflow-y: auto;
  height: calc(100vh - 64px);
  position: sticky;
  top: 64px;
  padding: 20px 0;
}
.style_sider__Hlcz3 h2 {
  font-size: 16px;
  color: #aaa;
  padding: 0 20px 12px;
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 600;
}
.menu-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.menu-item {
  display: block;
}
.menu-link {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  color: #ddd;
  font-size: 14px;
  border-left: 4px solid transparent;
  transition: all 0.2s ease;
  line-height: 1.4;
}
.menu-link:hover {
  background: #3e3e3e;
  color: #fff;
}
.menu-link.active {
  background: #05673d;
  color: #fff;
  font-weight: 600;
  border-left-color: #35ddac;
}
.menu-link .num-tag {
  font-family: monospace;
  font-size: 12px;
  background: rgba(255,255,255,0.15);
  padding: 2px 6px;
  border-radius: 4px;
  margin-right: 10px;
  flex-shrink: 0;
}

/* Content Area */
.style_content__Qif_T {
  flex-grow: 1;
  background-color: #fff;
  min-width: 0;
}
.style_articleWrap__Xn2yv {
  max-width: 900px;
  margin: 0 auto;
  padding: 40px 48px 80px;
}
.style_learnContent__K5K7M .style_chapter__grtAe {
  font-size: 64px;
  font-weight: 700;
  color: #35cea0;
  line-height: 1;
  margin-bottom: 8px;
  font-family: -apple-system, BlinkMacSystemFont, sans-serif;
}
.style_learnContent__K5K7M h1 {
  font-size: 34px;
  font-weight: 700;
  color: #282828;
  margin-top: 0;
  margin-bottom: 24px;
  line-height: 1.25;
}
.style_learnContent__K5K7M h2 {
  font-size: 24px;
  font-weight: 600;
  color: #282828;
  margin-top: 36px;
  margin-bottom: 14px;
  border-bottom: 1px solid #eee;
  padding-bottom: 8px;
}
.style_learnContent__K5K7M h3 {
  font-size: 19px;
  font-weight: 600;
  color: #333;
  margin-top: 24px;
  margin-bottom: 10px;
}
.style_learnContent__K5K7M p {
  font-size: 16px;
  line-height: 1.7;
  color: #334155;
  margin-bottom: 16px;
}
.style_learnContent__K5K7M ul, .style_learnContent__K5K7M ol {
  font-size: 16px;
  color: #334155;
  line-height: 1.7;
  padding-left: 24px;
  margin-bottom: 18px;
}
.style_learnContent__K5K7M li {
  margin-bottom: 8px;
}
.style_learnContent__K5K7M pre {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 16px;
  overflow-x: auto;
  margin: 20px 0;
  font-family: "SF Mono", Monaco, Menlo, Consolas, monospace;
  font-size: 14px;
}
.style_learnContent__K5K7M code {
  font-family: "SF Mono", Monaco, Menlo, Consolas, monospace;
  font-size: 0.9em;
  background: rgba(0,0,0,0.05);
  padding: 2px 5px;
  border-radius: 4px;
  color: #0f172a;
}
.style_learnContent__K5K7M pre code {
  background: transparent;
  padding: 0;
  color: inherit;
}
.style_learnContent__K5K7M figure {
  margin: 28px 0;
  text-align: center;
}
.callout {
  padding: 16px 20px;
  border-radius: 8px;
  margin: 24px 0;
  font-size: 15px;
  line-height: 1.6;
}
.callout-info {
  background: #f0fdf4;
  border-left: 4px solid #10b981;
  color: #065f46;
}
.callout-tip {
  background: #eff6ff;
  border-left: 4px solid #3b82f6;
  color: #1e40af;
}
.callout-warning {
  background: #fffbeb;
  border-left: 4px solid #f59e0b;
  color: #92400e;
}
.table-custom {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
  font-size: 15px;
}
.table-custom th, .table-custom td {
  border: 1px solid #e2e8f0;
  padding: 10px 14px;
  text-align: left;
}
.table-custom th {
  background: #f8fafc;
  font-weight: 600;
  color: #1e293b;
}

/* Prev / Next Bottom Navigation */
.lesson-nav-bottom {
  display: flex;
  justify-content: space-between;
  border-top: 1px solid #e2e8f0;
  padding-top: 24px;
  margin-top: 48px;
}
.btn-nav {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  color: #475569;
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  transition: all 0.2s;
}
.btn-nav:hover {
  background: #e2e8f0;
  color: #0f172a;
}
.btn-nav-primary {
  background: #05673d;
  color: #fff;
  border-color: #05673d;
}
.btn-nav-primary:hover {
  background: #044e2e;
  color: #fff;
}
</style>
</head>
<body>
<div id="__next">
  <div class="ant-layout">
    <header class="style_header__IrB9Y">
      <a href="../index.html" class="brand-title">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" stroke="#05673d" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        ByteByteGo | Python Masterclass
      </a>
      <div>
        <a href="../index.html" style="font-weight: 600; color: #333;">← All Courses</a>
      </div>
    </header>

    <div class="style_learn__wJdK1">
      <!-- Sidebar Navigation -->
      <aside class="style_sider__Hlcz3">
        <h2>Python Curriculum</h2>
        <ul class="menu-list">
"""

def generate_lessons():
    os.makedirs('Python Course', exist_ok=True)
    
    # Load all 15 lessons detailed content
    all_lessons = [
        {
            "num": 1,
            "filename": "001 Python Execution Model, CPython & Architecture.html",
            "title": "Python Execution Model, CPython & Architecture",
            "read_time": 15,
            "content": """
<p>Python is commonly known as an interpreted scripting language, but in standard implementations (CPython), it operates via a dual-phase <strong>compilation and virtual machine interpretation</strong> architecture. Understanding this internal execution pipeline is fundamental for writing high-performance, memory-efficient Python code and excelling in systems-level technical interviews.</p>

<h2>1. The Four-Stage Execution Pipeline</h2>
<p>When you invoke <code>python app.py</code>, CPython does not interpret raw text line-by-line. Instead, it processes your code through four specialized subsystems:</p>

<figure>
  <svg width="100%" height="230" viewBox="0 0 800 230" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect width="800" height="230" rx="12" fill="#1e293b"/>
    <!-- Source Code -->
    <rect x="25" y="75" width="135" height="80" rx="8" fill="#3b82f6" fill-opacity="0.2" stroke="#3b82f6" stroke-width="2"/>
    <text x="92" y="110" fill="#f8fafc" font-size="14" font-weight="700" text-anchor="middle">Source Code</text>
    <text x="92" y="132" fill="#94a3b8" font-size="12" text-anchor="middle">script.py (UTF-8)</text>
    
    <path d="M165 115 H205" stroke="#64748b" stroke-width="2" stroke-dasharray="4 4"/>
    
    <!-- Lexer/Parser AST -->
    <rect x="215" y="75" width="145" height="80" rx="8" fill="#8b5cf6" fill-opacity="0.2" stroke="#8b5cf6" stroke-width="2"/>
    <text x="287" y="110" fill="#f8fafc" font-size="14" font-weight="700" text-anchor="middle">Tokenizer & AST</text>
    <text x="287" y="132" fill="#94a3b8" font-size="12" text-anchor="middle">Grammar Validation</text>

    <path d="M365 115 H405" stroke="#64748b" stroke-width="2" stroke-dasharray="4 4"/>

    <!-- Bytecode -->
    <rect x="415" y="75" width="145" height="80" rx="8" fill="#ec4899" fill-opacity="0.2" stroke="#ec4899" stroke-width="2"/>
    <text x="487" y="110" fill="#f8fafc" font-size="14" font-weight="700" text-anchor="middle">Bytecode (.pyc)</text>
    <text x="487" y="132" fill="#94a3b8" font-size="12" text-anchor="middle">PyCodeObject in RAM</text>

    <path d="M565 115 H605" stroke="#64748b" stroke-width="2" stroke-dasharray="4 4"/>

    <!-- PVM -->
    <rect x="615" y="75" width="160" height="80" rx="8" fill="#10b981" fill-opacity="0.2" stroke="#10b981" stroke-width="2"/>
    <text x="695" y="110" fill="#f8fafc" font-size="14" font-weight="700" text-anchor="middle">CPython PVM</text>
    <text x="695" y="132" fill="#10b981" font-size="12" text-anchor="middle">ceval.c Loop</text>
  </svg>
</figure>

<ol>
  <li><strong>Lexing & Parsing:</strong> Converts source characters into tokens and constructs an Abstract Syntax Tree (AST). Syntax errors are raised exclusively here.</li>
  <li><strong>Bytecode Generation:</strong> The AST compiler converts nodes into compact bytecode opcodes stored in a <code>PyCodeObject</code>.</li>
  <li><strong>Bytecode Caching (<code>__pycache__</code>):</strong> The bytecode is written to <code>.pyc</code> files containing a magic number header and timestamp/hash. If unchanged, future runs bypass compilation.</li>
  <li><strong>PVM Evaluation Loop:</strong> The virtual machine (a stack-based interpreter implemented in C) reads opcodes sequentially and manipulates the evaluation stack.</li>
</ol>

<h2>2. Disassembling Python Bytecode with <code>dis</code></h2>
<p>CPython operates as a <strong>stack machine</strong> rather than a register machine (like x86 or ARM). Operands are pushed onto an internal evaluation stack, modified, and popped.</p>

<pre><code class="language-python">import dis

def compute_tax(subtotal, rate=0.08):
    tax = subtotal * rate
    return subtotal + tax

dis.dis(compute_tax)
</code></pre>

<p><strong>Detailed Opcode Breakdown:</strong></p>
<pre><code class="language-text">  2           0 LOAD_FAST                0 (subtotal)
              2 LOAD_FAST                1 (rate)
              4 BINARY_MULTIPLY
              6 STORE_FAST               2 (tax)

  3           8 LOAD_FAST                0 (subtotal)
             10 LOAD_FAST                2 (tax)
             12 BINARY_ADD
             14 RETURN_VALUE
</code></pre>

<div class="callout callout-tip">
  <strong>Key Observation:</strong> Notice how variables inside a function use <code>LOAD_FAST</code> and <code>STORE_FAST</code> (O(1) array index lookups in the frame object) rather than <code>LOAD_NAME</code> or <code>LOAD_GLOBAL</code> (O(1) hash map lookups). Local variables in Python functions are resolved using direct pointer offsets!
</div>

<h2>3. Comparing Python Implementations</h2>
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
      <td>No (Adaptive Interpreter 3.11+)</td>
      <td>Standard ecosystem, 100% C-Extension (NumPy, PyTorch, Pandas) compatibility.</td>
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

<div class="callout callout-info">
  <strong>🎯 Technical Interview Checklist:</strong>
  <ul>
    <li>Explain the difference between a <code>FunctionObject</code> (mutable, holds scope/globals) and a <code>CodeObject</code> (immutable, holds compiled bytecode).</li>
    <li>Why does CPython use a stack-based VM instead of a register-based VM? (Simpler opcode generation, platform-independent portability).</li>
  </ul>
</div>
"""
        },
        {
            "num": 2,
            "filename": "002 Variables, Mutability, Memory & Object Model.html",
            "title": "Variables, Mutability, Memory & Object Model",
            "read_time": 16,
            "content": """
<p>In Python, <strong>everything is an object</strong>. Variables are not memory boxes that hold values; they are <strong>named references (pointers)</strong> bound to objects in heap memory. Grasping Python's object model and mutability is essential for avoiding catastrophic reference bugs in production.</p>

<h2>1. The Anatomy of a Python Object (<code>PyObject</code>)</h2>
<p>Every object in CPython has a C structure header called <code>PyObject</code> containing two fundamental fields:</p>
<ul>
  <li><code>ob_refcnt</code>: An integer tracking how many references point to this object (used for Garbage Collection).</li>
  <li><code>ob_type</code>: A pointer to the object's type descriptor (which dictates its methods, size, and behavior).</li>
</ul>

<figure>
  <svg width="100%" height="200" viewBox="0 0 800 200" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect width="800" height="200" rx="12" fill="#1e293b"/>
    <!-- Variable Names on Stack -->
    <rect x="40" y="50" width="160" height="110" rx="8" fill="#3b82f6" fill-opacity="0.15" stroke="#3b82f6" stroke-width="1.5"/>
    <text x="120" y="75" fill="#f8fafc" font-size="14" font-weight="700" text-anchor="middle">Stack Frame / Namespace</text>
    <text x="60" y="110" fill="#93c5fd" font-size="14" font-family="monospace">a = [1, 2]</text>
    <text x="60" y="140" fill="#93c5fd" font-size="14" font-family="monospace">b = a</text>

    <!-- Arrow 1 -->
    <path d="M170 105 H320" stroke="#38bdf8" stroke-width="2" marker-end="url(#arrow)"/>
    <!-- Arrow 2 -->
    <path d="M170 135 L320 108" stroke="#38bdf8" stroke-width="2"/>

    <!-- Heap Object -->
    <rect x="330" y="45" width="420" height="120" rx="8" fill="#10b981" fill-opacity="0.15" stroke="#10b981" stroke-width="2"/>
    <text x="540" y="75" fill="#10b981" font-size="14" font-weight="700" text-anchor="middle">PyListObject (Heap Address: 0x7ffd...)</text>
    <rect x="350" y="90" width="110" height="55" rx="6" fill="#0f172a" stroke="#475569"/>
    <text x="405" y="112" fill="#94a3b8" font-size="11" text-anchor="middle">ob_refcnt</text>
    <text x="405" y="132" fill="#f8fafc" font-size="14" font-weight="700" text-anchor="middle">2</text>

    <rect x="470" y="90" width="110" height="55" rx="6" fill="#0f172a" stroke="#475569"/>
    <text x="525" y="112" fill="#94a3b8" font-size="11" text-anchor="middle">ob_type</text>
    <text x="525" y="132" fill="#f8fafc" font-size="14" font-weight="700" text-anchor="middle">&list_type</text>

    <rect x="590" y="90" width="140" height="55" rx="6" fill="#0f172a" stroke="#475569"/>
    <text x="660" y="112" fill="#94a3b8" font-size="11" text-anchor="middle">items pointer</text>
    <text x="660" y="132" fill="#38bdf8" font-size="14" font-weight="700" text-anchor="middle">[0x1, 0x2]</text>
  </svg>
</figure>

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
      <td>❌ No (Creates a new object)</td>
      <td>✅ Yes (If all contents are immutable)</td>
    </tr>
    <tr>
      <td><strong>Mutable</strong></td>
      <td><code>list</code>, <code>dict</code>, <code>set</code>, <code>bytearray</code>, custom classes</td>
      <td>✅ Yes (Mutates same memory buffer)</td>
      <td>❌ No (Un-hashable)</td>
    </tr>
  </tbody>
</table>

<h2>3. Equality (<code>==</code>) vs Identity (<code>is</code>)</h2>
<pre><code class="language-python"># Identity vs Value Check
list1 = [1, 2, 3]
list2 = [1, 2, 3]

print(list1 == list2) # True (Contents are equivalent)
print(list1 is list2) # False (Different memory addresses: id(list1) != id(list2))

# Small Integer Caching & String Interning
x = 256
y = 256
print(x is y) # True (CPython pre-allocates small ints from -5 to 256)

big1 = 1000000
big2 = 1000000
print(big1 is big2) # False (Outside pre-allocated cache range)
</code></pre>

<div class="callout callout-warning">
  <strong>⚠️ The Notorious Default Argument Pitfall:</strong>
  <pre><code class="language-python"># BAD: Default argument evaluated ONCE at function definition time!
def append_item(val, target_list=[]):
    target_list.append(val)
    return target_list

print(append_item(1)) # [1]
print(append_item(2)) # [1, 2] -- UNEXPECTED MUTATION!

# PRO FIX: Use None as default sentinel
def append_item_clean(val, target_list=None):
    if target_list is None:
        target_list = []
    target_list.append(val)
    return target_list
</code></pre>
</div>
"""
        },
        {
            "num": 3,
            "filename": "003 Data Structures Deep Dive - Lists, Tuples, Sets, Dictionaries.html",
            "title": "Data Structures Deep Dive - Lists, Tuples, Sets, Dictionaries",
            "read_time": 20,
            "content": """
<p>Python's core data structures are engineered for extreme developer productivity and amortized high-speed throughput. In this lesson, we examine their internal memory architectures, hashing mechanisms, resizing algorithms, and asymptotic complexity.</p>

<h2>1. Dynamic Arrays: How <code>list</code> Works Internally</h2>
<p>A Python <code>list</code> is an <strong>array of pointers</strong> (<code>PyObject**</code>), not a linked list. When elements are appended, CPython uses an over-allocation strategy to guarantee <strong>O(1) amortized append</strong> operations:</p>
<pre><code class="language-text">new_allocated = (size_t)newsize + (newsize >> 3) + (newsize < 9 ? 3 : 6);
</code></pre>

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
      <td>Direct memory pointer offset calculation</td>
    </tr>
    <tr>
      <td><code>list.append(x)</code></td>
      <td><strong>O(1)</strong></td>
      <td><strong>O(N)</strong></td>
      <td>Amortized O(1); O(N) when realloc occurs</td>
    </tr>
    <tr>
      <td><code>list.insert(0, x)</code></td>
      <td><strong>O(N)</strong></td>
      <td><strong>O(N)</strong></td>
      <td>Must shift all subsequent N elements right</td>
    </tr>
    <tr>
      <td><code>list.pop()</code></td>
      <td><strong>O(1)</strong></td>
      <td><strong>O(1)</strong></td>
      <td>Pointers shrunk from tail in-place</td>
    </tr>
  </tbody>
</table>

<h2>2. The Compact Hash Table: Python 3.7+ <code>dict</code></h2>
<p>Since Python 3.7, dictionaries maintain insertion order while consuming up to 30% less memory using a <strong>two-array split hash table design</strong>:</p>

<figure>
  <svg width="100%" height="220" viewBox="0 0 800 220" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect width="800" height="220" rx="12" fill="#1e293b"/>
    <!-- Sparse Hash Indices -->
    <rect x="30" y="50" width="300" height="130" rx="8" fill="#3b82f6" fill-opacity="0.15" stroke="#3b82f6" stroke-width="1.5"/>
    <text x="180" y="75" fill="#3b82f6" font-size="14" font-weight="700" text-anchor="middle">Sparse Indices Array (int8 / int16)</text>
    <text x="50" y="110" fill="#94a3b8" font-size="12" font-family="monospace">hash(key) % 8 = index</text>
    <rect x="50" y="125" width="260" height="35" rx="4" fill="#0f172a" stroke="#475569"/>
    <text x="180" y="148" fill="#38bdf8" font-size="13" font-family="monospace">[-1, 0, -1, 1, -1, -1, 2, -1]</text>

    <!-- Dense Entries Array -->
    <rect x="370" y="50" width="400" height="130" rx="8" fill="#10b981" fill-opacity="0.15" stroke="#10b981" stroke-width="1.5"/>
    <text x="570" y="75" fill="#10b981" font-size="14" font-weight="700" text-anchor="middle">Dense Entries Array (In Insertion Order)</text>
    <rect x="390" y="95" width="360" height="25" rx="4" fill="#0f172a"/>
    <text x="400" y="112" fill="#a7f3d0" font-size="11" font-family="monospace">0: [hash="user", key="user", val="Alice"]</text>
    <rect x="390" y="125" width="360" height="25" rx="4" fill="#0f172a"/>
    <text x="400" y="142" fill="#a7f3d0" font-size="11" font-family="monospace">1: [hash="role", key="role", val="Admin"]</text>
    <rect x="390" y="155" width="360" height="25" rx="4" fill="#0f172a"/>
    <text x="400" y="172" fill="#a7f3d0" font-size="11" font-family="monospace">2: [hash="auth", key="auth", val=True]</text>
  </svg>
</figure>

<p><strong>Collision Resolution:</strong> CPython uses <strong>open addressing with pseudo-random perturbation probing</strong> rather than linear probing to minimize primary clustering.</p>
"""
        },
        {
            "num": 4,
            "filename": "004 Functions, Closures & Scope (LEGB Rule).html",
            "title": "Functions, Closures & Scope (LEGB Rule)",
            "read_time": 14,
            "content": """
<p>Functions in Python are <strong>first-class citizens</strong>. They can be assigned to variables, passed as arguments, returned from other functions, and store lexical scope closures.</p>

<h2>1. Scope Resolution: The LEGB Rule</h2>
<p>When Python resolves a variable name, it traverses four scopes in strict sequential order:</p>
<ol>
  <li><strong>Local (L):</strong> Names assigned within a function body.</li>
  <li><strong>Enclosing (E):</strong> Names in the local scope of enclosing/nested functions (closures).</li>
  <li><strong>Global (G):</strong> Names assigned at the top-level of the module file.</li>
  <li><strong>Built-in (B):</strong> Pre-defined names in Python's <code>builtins</code> module (e.g. <code>len</code>, <code>range</code>, <code>ValueError</code>).</li>
</ol>

<h2>2. Closures & Free Variables</h2>
<p>A closure occurs when an inner function captures and remembers variables from its enclosing scope even after the outer function has finished executing:</p>

<pre><code class="language-python">def create_multiplier(factor):
    # 'factor' is a free variable captured in the cell object
    def multiply(x):
        return x * factor
    return multiply

double = create_multiplier(2)
print(double(10)) # 20
print(double.__closure__[0].cell_contents) # 2
</code></pre>

<h2>3. <code>global</code> vs <code>nonlocal</code></h2>
<pre><code class="language-python">def outer():
    count = 0
    def inner():
        nonlocal count # Rebinds to the enclosing function's variable!
        count += 1
        return count
    return inner

counter = outer()
print(counter()) # 1
print(counter()) # 2
</code></pre>
"""
        },
        {
            "num": 5,
            "filename": "005 Object-Oriented Programming & Dunder Methods.html",
            "title": "Object-Oriented Programming & Dunder Methods",
            "read_time": 18,
            "content": """
<p>Python's object-oriented capabilities are deeply integrated into the language via <strong>Special Methods (Dunder Methods)</strong>. By implementing dunder methods, your custom classes seamlessly hook into standard operators, iteration protocols, and built-in functions.</p>

<h2>1. Essential Dunder Protocol Categories</h2>
<table class="table-custom">
  <thead>
    <tr>
      <th>Protocol</th>
      <th>Dunder Methods</th>
      <th>Python Operator / Built-in Trigger</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>String Representation</strong></td>
      <td><code>__str__(self)</code>, <code>__repr__(self)</code></td>
      <td><code>str(obj)</code>, <code>print(obj)</code>, <code>repr(obj)</code></td>
    </tr>
    <tr>
      <td><strong>Comparison</strong></td>
      <td><code>__eq__</code>, <code>__lt__</code>, <code>__le__</code>, <code>__gt__</code>, <code>__ge__</code></td>
      <td><code>==</code>, <code>&lt;</code>, <code>&lt;=</code>, <code>&gt;</code>, <code>&gt;=</code></td>
    </tr>
    <tr>
      <td><strong>Container Emulation</strong></td>
      <td><code>__len__</code>, <code>__getitem__</code>, <code>__setitem__</code></td>
      <td><code>len(obj)</code>, <code>obj[key]</code>, <code>obj[key] = val</code></td>
    </tr>
    <tr>
      <td><strong>Callable Objects</strong></td>
      <td><code>__call__(self, *args, **kwargs)</code></td>
      <td><code>obj()</code> (Invoking object as a function)</td>
    </tr>
  </tbody>
</table>

<h2>2. <code>__repr__</code> vs <code>__str__</code></h2>
<p>A classic interview question is distinguishing the purpose of these two representation methods:</p>
<ul>
  <li><code>__str__</code>: Human-readable output intended for end-users.</li>
  <li><code>__repr__</code>: Unambiguous technical representation, ideally executable Python code (e.g. <code>eval(repr(obj)) == obj</code>).</li>
</ul>

<pre><code class="language-python">class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        
    def __repr__(self) -> str:
        return f"Vector({self.x!r}, {self.y!r})"
        
    def __add__(self, other: "Vector") -> "Vector":
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)

v1 = Vector(2, 3)
v2 = Vector(5, 7)
print(v1 + v2) # Vector(7, 10)
</code></pre>
"""
        },
        {
            "num": 6,
            "filename": "006 Inheritance, MRO & The C3 Linearization Algorithm.html",
            "title": "Inheritance, MRO & The C3 Linearization Algorithm",
            "read_time": 22,
            "content": """
<p>Python supports multiple inheritance through the <strong>Method Resolution Order (MRO)</strong>, calculated deterministically using the <strong>C3 Linearization Algorithm</strong>. This prevents ambiguities in the classic "Diamond Problem" and enables cooperative multiple inheritance via <code>super()</code>.</p>

<h2>1. The Diamond Problem & C3 Algorithm</h2>
<figure>
  <svg width="100%" height="220" viewBox="0 0 800 220" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect width="800" height="220" rx="12" fill="#1e293b"/>
    <!-- Node A -->
    <rect x="340" y="20" width="120" height="45" rx="6" fill="#3b82f6" stroke="#60a5fa" stroke-width="2"/>
    <text x="400" y="47" fill="#fff" font-size="14" font-weight="700" text-anchor="middle">Class A</text>

    <!-- Node B & C -->
    <rect x="200" y="95" width="120" height="45" rx="6" fill="#8b5cf6" stroke="#a78bfa" stroke-width="2"/>
    <text x="260" y="122" fill="#fff" font-size="14" font-weight="700" text-anchor="middle">Class B(A)</text>

    <rect x="480" y="95" width="120" height="45" rx="6" fill="#8b5cf6" stroke="#a78bfa" stroke-width="2"/>
    <text x="540" y="122" fill="#fff" font-size="14" font-weight="700" text-anchor="middle">Class C(A)</text>

    <!-- Node D -->
    <rect x="340" y="165" width="120" height="45" rx="6" fill="#ec4899" stroke="#f472b6" stroke-width="2"/>
    <text x="400" y="192" fill="#fff" font-size="14" font-weight="700" text-anchor="middle">Class D(B, C)</text>

    <!-- Connectors -->
    <path d="M400 165 L260 140" stroke="#94a3b8" stroke-width="2"/>
    <path d="M400 165 L540 140" stroke="#94a3b8" stroke-width="2"/>
    <path d="M260 95 L400 65" stroke="#94a3b8" stroke-width="2"/>
    <path d="M540 95 L400 65" stroke="#94a3b8" stroke-width="2"/>
  </svg>
</figure>

<h2>2. Inspecting the MRO</h2>
<pre><code class="language-python">class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass

print(D.__mro__)
# Output: (D, B, C, A, object)
</code></pre>

<div class="callout callout-info">
  <strong>💡 C3 Linearization Rules:</strong>
  <ul>
    <li><strong>Subclasses come before base classes:</strong> D before B, B before A.</li>
    <li><strong>Declaration order matters:</strong> Because <code>D(B, C)</code> lists B before C, B's hierarchy is explored first.</li>
    <li><strong>Monotonicity:</strong> If class X precedes class Y in any base class MRO, it must precede Y in all derived MROs.</li>
  </ul>
</div>
"""
        },
        {
            "num": 7,
            "filename": "007 Advanced Decorators & Function Wrappers.html",
            "title": "Advanced Decorators & Function Wrappers",
            "read_time": 18,
            "content": """
<p>Decorators represent a powerful metaprogramming pattern in Python, enabling you to inject cross-cutting concerns (authentication, caching, metrics, rate limiting) cleanly without modifying core function signatures.</p>

<h2>1. Creating Production-Grade Decorators with <code>functools.wraps</code></h2>
<pre><code class="language-python">import time
import functools
import logging

logging.basicConfig(level=logging.INFO)

def profile_execution(threshold_sec=0.1):
    def decorator(func):
        @functools.wraps(func) # Preserves __name__, __doc__, and annotations
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            duration = time.perf_counter() - start
            if duration > threshold_sec:
                logging.warning(f"SLOW CALL: {func.__name__} took {duration:.4f}s")
            return result
        return wrapper
    return decorator

@profile_execution(threshold_sec=0.05)
def process_data(records):
    time.sleep(0.06)
    return len(records)
</code></pre>
"""
        },
        {
            "num": 8,
            "filename": "008 Iterators, Iterables & Generators.html",
            "title": "Iterators, Iterables & Generators",
            "read_time": 16,
            "content": """
<p>Generators allow streaming evaluation of massive datasets with <strong>O(1) memory complexity</strong> by pausing and resuming function state using the <code>yield</code> keyword.</p>

<h2>1. The Iteration Protocol</h2>
<ul>
  <li><strong>Iterable:</strong> An object implementing <code>__iter__()</code> returning an iterator.</li>
  <li><strong>Iterator:</strong> An object implementing <code>__next__()</code> returning elements sequentially or raising <code>StopIteration</code>.</li>
</ul>

<pre><code class="language-python">def chunked_file_reader(filepath, chunk_size=1024*1024):
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

# Streams a 50GB file with only 1MB in memory!
for chunk in chunked_file_reader("huge_log.csv"):
    process(chunk)
</code></pre>
"""
        },
        {
            "num": 9,
            "filename": "009 Context Managers & The with Statement.html",
            "title": "Context Managers & The with Statement",
            "read_time": 15,
            "content": """
<p>Context managers ensure deterministic resource acquisition and release (RAII pattern in Python), preventing memory leaks, socket starvation, and unclosed database transactions.</p>

<h2>1. Implementing <code>__enter__</code> and <code>__exit__</code></h2>
<pre><code class="language-python">class ManagedTransaction:
    def __init__(self, db_conn):
        self.conn = db_conn

    def __enter__(self):
        self.conn.begin()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.conn.rollback() # Rollback on exception
            logging.error(f"Transaction aborted: {exc_val}")
            return False # Re-raise exception
        self.conn.commit()
        return True
</code></pre>
"""
        },
        {
            "num": 10,
            "filename": "010 Concurrency I - Threads, Processes & the Global Interpreter Lock (GIL).html",
            "title": "Concurrency I - Threads, Processes & the Global Interpreter Lock (GIL)",
            "read_time": 25,
            "content": """
<p>Concurrency in Python requires choosing the right tool for the job. The <strong>Global Interpreter Lock (GIL)</strong> is a mutual-exclusion lock preventing multiple native OS threads from executing CPython bytecode simultaneously on multiple CPU cores.</p>

<h2>1. CPU-Bound vs I/O-Bound Strategy</h2>
<table class="table-custom">
  <thead>
    <tr>
      <th>Task Type</th>
      <th>Bottleneck</th>
      <th>Recommended Concurrency Model</th>
      <th>Reason</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>I/O Bound</strong> (Network, DB, File I/O)</td>
      <td>Waiting for sockets / disk</td>
      <td><code>asyncio</code> or <code>threading.Thread</code></td>
      <td>GIL is released during socket/system calls.</td>
    </tr>
    <tr>
      <td><strong>CPU Bound</strong> (Data processing, ML)</td>
      <td>CPU registers / calculation</td>
      <td><code>multiprocessing.Process</code> or C-Extensions</td>
      <td>Bypasses the GIL by spawning separate OS processes with discrete PVMs.</td>
    </tr>
  </tbody>
</table>
"""
        },
        {
            "num": 11,
            "filename": "011 Concurrency II - Asynchronous Programming with Asyncio.html",
            "title": "Concurrency II - Asynchronous Programming with Asyncio",
            "read_time": 22,
            "content": """
<p><code>asyncio</code> enables single-threaded cooperative multitasking using an <strong>event loop</strong> to handle thousands of concurrent I/O connections with minimal memory overhead.</p>

<h2>1. The Event Loop Architecture</h2>
<pre><code class="language-python">import asyncio
import httpx

async def fetch_status(client, url):
    resp = await client.get(url)
    return url, resp.status_code

async def main():
    urls = ["https://httpbin.org/delay/1" for _ in range(50)]
    async with httpx.AsyncClient() as client:
        tasks = [fetch_status(client, u) for u in urls]
        # Runs 50 network requests concurrently in ~1 second!
        results = await asyncio.gather(*tasks)
        print(f"Completed {len(results)} requests.")

asyncio.run(main())
</code></pre>
"""
        },
        {
            "num": 12,
            "filename": "012 Metaclasses & Class Creation Mechanics.html",
            "title": "Metaclasses & Class Creation Mechanics",
            "read_time": 20,
            "content": """
<p>If classes are blueprints for objects, <strong>metaclasses are blueprints for classes</strong>. Metaclasses allow frameworks (like Django ORM or Pydantic) to inspect, validate, and alter class structures at import time.</p>

<h2>1. <code>type</code> as a Metaclass</h2>
<pre><code class="language-python"># Dynamic class construction using type:
# type(name, bases, dict)
Person = type('Person', (object,), {
    'species': 'Homo sapiens',
    'greet': lambda self: f"Hello from {self.species}"
})

p = Person()
print(p.greet()) # Hello from Homo sapiens
</code></pre>
"""
        },
        {
            "num": 13,
            "filename": "013 Memory Management, Garbage Collection & CPython Internals.html",
            "title": "Memory Management, Garbage Collection & CPython Internals",
            "read_time": 22,
            "content": """
<p>CPython memory management combines <strong>PyMalloc (small object allocator)</strong>, <strong>Reference Counting</strong>, and a <strong>Generational Cyclic Garbage Collector</strong>.</p>

<h2>1. Three-Generation Cyclic GC</h2>
<ul>
  <li><strong>Generation 0:</strong> Newly allocated objects. Collected frequently.</li>
  <li><strong>Generation 1:</strong> Objects surviving Gen 0 collections.</li>
  <li><strong>Generation 2:</strong> Long-lived objects (e.g. module imports). Collected rarely.</li>
</ul>

<div class="callout callout-tip">
  <strong>Optimization Tip: <code>__slots__</code></strong><br>
  Defining <code>__slots__ = ('x', 'y')</code> in a class replaces the default instance <code>__dict__</code> with a compact C-struct array, reducing memory usage per instance by over 60%!
</div>
"""
        },
        {
            "num": 14,
            "filename": "014 Performance Optimization, Profiling & C-Extensions.html",
            "title": "Performance Optimization, Profiling & C-Extensions",
            "read_time": 18,
            "content": """
<p>Optimizing Python code requires scientific profiling using <code>cProfile</code>, algorithmic tuning, and delegating compute kernels to native C/Rust extensions.</p>

<h2>1. Profiling with <code>cProfile</code></h2>
<pre><code class="language-python">import cProfile
import pstats

def high_cpu_job():
    return sum(i * i for i in range(1_000_000))

profiler = cProfile.Profile()
profiler.enable()
high_cpu_job()
profiler.disable()

stats = pstats.Stats(profiler).sort_stats('cumtime')
stats.print_stats(10)
</code></pre>
"""
        },
        {
            "num": 15,
            "filename": "015 Python Testing, Type Annotations & Production Best Practices.html",
            "title": "Python Testing, Type Annotations & Production Best Practices",
            "read_time": 20,
            "content": """
<p>Writing production-grade Python requires modern static type hinting (PEP 484), robust automated test suites with <code>pytest</code>, and clean modular architecture.</p>

<h2>1. Modern Type Hinting (Python 3.10+)</h2>
<pre><code class="language-python">from typing import TypeVar, Protocol

class Renderable(Protocol):
    def render(self) -> str: ...

T = TypeVar('T', bound=Renderable)

def render_all(items: list[T]) -> list[str]:
    return [item.render() for item in items]
</code></pre>
"""
        }
    ]

    for item in all_lessons:
        num_str = f"{item['num']:02d}"
        
        # Build sider links
        sider_html = ""
        for other in all_lessons:
            active_cls = " active" if other['num'] == item['num'] else ""
            sider_html += f"""
          <li class="menu-item">
            <a href="{other['filename']}" class="menu-link{active_cls}">
              <span class="num-tag">{other['num']:02d}</span>
              <span>{other['title']}</span>
            </a>
          </li>"""

        # Navigation buttons
        prev_btn = ""
        if item['num'] > 1:
            prev_lesson = all_lessons[item['num'] - 2]
            prev_btn = f'<a href="{prev_lesson["filename"]}" class="btn-nav">← Previous: {prev_lesson["title"]}</a>'
        else:
            prev_btn = '<a href="../index.html" class="btn-nav">← Back to Hub</a>'

        next_btn = ""
        if item['num'] < len(all_lessons):
            next_lesson = all_lessons[item['num']]
            next_btn = f'<a href="{next_lesson["filename"]}" class="btn-nav btn-nav-primary">Next: {next_lesson["title"]} →</a>'
        else:
            next_btn = '<a href="../index.html" class="btn-nav btn-nav-primary">🎓 Course Completed! Back to Hub →</a>'

        full_html = HTML_SHELL_HEAD.replace('{title}', item['title'])
        full_html += sider_html
        full_html += f"""
        </ul>
      </aside>

      <!-- Main Article -->
      <main class="style_content__Qif_T">
        <div class="style_articleWrap__Xn2yv">
          <article class="style_learnContent__K5K7M">
            <header>
              <div class="style_chapter__grtAe">{num_str}</div>
              <h1>{item['title']}</h1>
            </header>

            {item['content']}

            <div class="lesson-nav-bottom">
              {prev_btn}
              {next_btn}
            </div>
          </article>
        </div>
      </main>
    </div>
  </div>
</div>

<!-- nav-inject-patched -->
<script src="../nav_map.js"></script>
<script src="../nav_inject.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/highlight.min.js"></script>
<script>hljs.highlightAll();</script>
</body>
</html>
"""
        target_path = os.path.join('Python Course', item['filename'])
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(full_html)
            
    print(f"Generated {len(all_lessons)} rich Python lessons in Python Course/ directory.")

if __name__ == '__main__':
    generate_lessons()
