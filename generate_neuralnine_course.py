"""
generate_neuralnine_course.py — Generates ByteByteGo lesson pages aligned with
NeuralNine Beginner -> Intermediate -> Advanced curriculum, plus Statistics and SQL.
"""
import os
import re
import json

with open('scratch/head_shell.html', 'r', encoding='utf-8') as f:
    HEAD_TEMPLATE = f.read()

with open('scratch/foot_shell.html', 'r', encoding='utf-8') as f:
    FOOT_TEMPLATE = f.read()

_TAB_SEQ = 0
COPY_BTN = '''<button type="button" class="ant-btn css-133v4sd ant-btn-default style_copyBtn__4MbAa" aria-label="Copy code"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="5.2" y="1.4" width="8.4" height="9.6" rx="1.2" stroke="#333" stroke-width="1.15"/><rect x="1.4" y="4.8" width="8.4" height="9.6" rx="1.2" fill="#fff" stroke="#333" stroke-width="1.15"/></svg></button>'''

PY_KEYWORDS = set(
    "and as assert async await break class continue def del elif else except False finally "
    "for from global if import in is lambda None nonlocal not or pass raise return True try "
    "while with yield".split()
)
PY_BUILTINS = set(
    "abs all any bool dict enumerate filter float format int len list map max min open "
    "print range set sorted str sum super tuple type zip isinstance".split()
)
SQL_KEYWORDS = set(
    "SELECT FROM WHERE JOIN LEFT RIGHT INNER OUTER ON GROUP BY HAVING ORDER ASC DESC "
    "INSERT INTO VALUES UPDATE SET DELETE CREATE TABLE WITH AS CASE WHEN THEN ELSE END "
    "AND OR NOT NULL DISTINCT COUNT SUM AVG MIN MAX OVER PARTITION ROW_NUMBER RANK "
    "DENSE_RANK LAG LEAD ROWS BETWEEN PRECEDING CURRENT ROW DATE MIN USING".split()
)

def _esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def highlight_code(code, lang):
    lang = (lang or "python").lower()
    if lang in ("text", "plaintext"):
        return _esc(code)
    token_re = re.compile(
        r"(#.*?$|//.*?$|--.*?$|\"\"\"[\s\S]*?\"\"\"|'''[\s\S]*?'''|\"[^\"\\]*(?:\\.[^\"\\]*)*\"|'[^'\\]*(?:\\.[^'\\]*)*'|\b\d+(?:\.\d+)?\b|\b[A-Za-z_][A-Za-z0-9_]*\b)",
        re.M,
    )
    out, last = [], 0
    for m in token_re.finditer(code):
        out.append(_esc(code[last:m.start()]))
        tok = m.group(0)
        low = tok.lower()
        if tok.startswith("#") or tok.startswith("--") or tok.startswith("//"):
            out.append(f'<span class="hljs-comment">{_esc(tok)}</span>')
        elif tok[0] in "\"'":
            out.append(f'<span class="hljs-string">{_esc(tok)}</span>')
        elif tok[0].isdigit():
            out.append(f'<span class="hljs-number">{_esc(tok)}</span>')
        elif lang == "sql" and low in {k.lower() for k in SQL_KEYWORDS}:
            out.append(f'<span class="hljs-keyword">{_esc(tok)}</span>')
        elif lang != "sql" and tok in PY_KEYWORDS:
            out.append(f'<span class="hljs-keyword">{_esc(tok)}</span>')
        elif lang != "sql" and tok in PY_BUILTINS:
            out.append(f'<span class="hljs-built_in">{_esc(tok)}</span>')
        else:
            out.append(_esc(tok))
        last = m.end()
    out.append(_esc(code[last:]))
    return "".join(out)

def _tab_placeholders(active_lang):
    active = (active_lang or "python").lower()
    if active == "sql":
        return ["SQL", "Python", "JavaScript", "Java"]
    return ["Python", "JavaScript", "Java", "Cpp"]

def _stub(lang):
    stubs = {
        "JavaScript": "// Python-first course — open the Python tab for the working example.",
        "Java": "// Python-first course — open the Python tab for the working example.",
        "Cpp": "// Python-first course — open the Python tab for the working example.",
        "Python": "# See the SQL tab for the working query.",
        "SQL": "-- See the Python tab for the working example.",
    }
    return stubs.get(lang, "# See the active tab.")

def make_code_tab(code_content, lang="python"):
    global _TAB_SEQ
    _TAB_SEQ += 1
    uid = _TAB_SEQ
    tabs = _tab_placeholders(lang)
    active_label = "SQL" if lang.lower() == "sql" else ("Text" if lang.lower() in ("text", "plaintext") else "Python")
    if active_label == "Text":
        tabs = ["Python", "JavaScript", "Java", "Cpp"]
        active_label = "Python"
    tab_html = []
    pane_html = []
    for i, label in enumerate(tabs):
        is_active = label == active_label
        tab_cls = "ant-tabs-tab ant-tabs-tab-active" if is_active else "ant-tabs-tab"
        pane_cls = "ant-tabs-tabpane ant-tabs-tabpane-active" if is_active else "ant-tabs-tabpane ant-tabs-tabpane-hidden"
        aria_sel = "true" if is_active else "false"
        aria_hid = "false" if is_active else "true"
        tabindex = "0" if is_active else "-1"
        body = code_content if is_active else _stub(label)
        hl_lang = lang if is_active else ("javascript" if label == "JavaScript" else ("java" if label == "Java" else ("sql" if label == "SQL" else "python")))
        if label == "Cpp":
            hl_lang = "cpp"
        highlighted = highlight_code(body, hl_lang if is_active else ("javascript" if label == "JavaScript" else "python"))
        tab_html.append(
            f'<div data-node-key="{i}" class="{tab_cls}">'
            f'<div role="tab" aria-selected="{aria_sel}" class="ant-tabs-tab-btn" tabindex="{tabindex}" '
            f'id="rc-tabs-{uid}-tab-{i}" aria-controls="rc-tabs-{uid}-panel-{i}">{label}</div></div>'
        )
        copy = COPY_BTN
        pane_html.append(
            f'<div role="tabpanel" tabindex="{tabindex}" aria-hidden="{aria_hid}" class="{pane_cls}" '
            f'id="rc-tabs-{uid}-panel-{i}" aria-labelledby="rc-tabs-{uid}-tab-{i}">'
            f'<pre><code class="hljs language-{hl_lang}">{highlighted}</code></pre>{copy}</div>'
        )
    return f'''<div class="style_codeTabsWrap__jMkKK">
<div class="ant-tabs ant-tabs-top ant-tabs-card style_codeTabs__DEEq6 css-133v4sd">
<div role="tablist" class="ant-tabs-nav"><div class="ant-tabs-nav-wrap"><div class="ant-tabs-nav-list">
{''.join(tab_html)}
</div></div></div>
<div class="ant-tabs-content-holder"><div class="ant-tabs-content ant-tabs-content-top">
{''.join(pane_html)}
</div></div>
</div></div>'''

def make_image_figure(img_src, alt_text):
    return (
        f'<figure class="py-1"><div style="display:flex;justify-content:center">'
        f'<img alt="{alt_text}" loading="lazy" src="{img_src}" '
        f'style="max-width:100%;height:auto;"></div></figure>'
    )

def make_svg_figure(filename, alt_text):
    path = os.path.join("Python Course", "images", filename)
    svg = open(path, encoding="utf-8", errors="replace").read()
    svg = re.sub(r"<\?xml[^>]*\?>", "", svg).strip()
    svg = svg.replace("<svg", f'<svg role="img" aria-label="{alt_text}"', 1)
    return f'<figure class="py-1"><div style="display:flex;justify-content:center;overflow:auto">{svg}</div></figure>'

CODE_WIDGET_CSS = """<style id="py-code-tabs">
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
.hljs-keyword{color:#d73a49}.hljs-number{color:#005cc5}.hljs-built_in{color:#e36209}
.hljs-string{color:#e36209}.hljs-comment{color:#6a737d}
.style_codeTabs__DEEq6 .style_copyBtn__4MbAa{position:absolute;top:16px;right:16px;padding:4px;height:auto;border:none;background:transparent;box-shadow:none;cursor:pointer;z-index:2}
.style_learnContent__K5K7M figure.py-1{margin:28px 0;text-align:center}
.style_learnContent__K5K7M figure.py-1 svg{max-width:100%;height:auto}
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
        var pane = btn.closest('.ant-tabs-tabpane');
        var text = pane.querySelector('code').innerText;
        if (navigator.clipboard) navigator.clipboard.writeText(text);
      });
    });
  });
})();
</script>
"""

def make_callout(title, text, kind="tip"):
    border_color = "#35cea0" if kind == "tip" else ("#fa8c16" if kind == "warn" else "#1890ff")
    bg_color = "#f6ffed" if kind == "tip" else ("#fffbe6" if kind == "warn" else "#e6f7ff")
    return f"""<div style="background:{bg_color};border-left:4px solid {border_color};padding:16px 20px;border-radius:6px;margin:24px 0;font-size:15px;line-height:1.6">
  <strong style="color:#282828">{title}</strong>
  <div style="margin-top:6px;color:#333">{text}</div>
</div>"""

def make_ul(items):
    lis = "".join(
        f'<li style="list-style:disc;margin:6px 0;line-height:1.65;font-size:15px;color:#212529;">{i}</li>'
        for i in items
    )
    return f'<ul style="list-style:disc;padding-left:24px;margin:12px 0 18px;">{lis}</ul>'

CURRICULUM = [
    {
        "num": 1,
        "tier": "Beginner Series",
        "filename": "001 Installation, Syntax & Variables.html",
        "title": "Installation, Syntax & Variables",
        "body": f"""
<p>Welcome to the Python Masterclass! In this introductory lesson, we cover setting up Python, running your first program, and mastering Python's dynamic variable and memory binding model.</p>

<h2>1. Running Your First Python Program</h2>
<p>Python code is executed either interactively in the REPL or saved in <code>.py</code> script files executed via the interpreter:</p>
{make_code_tab('''# Hello World in Python
name = "Developer"
print(f"Hello, {name}! Welcome to Python.")

# Multi-variable assignment
x, y, z = 10, 20, 30
print(f"Sum = {x + y + z}")''')}

<h2>2. Primitive Data Types in Python</h2>
<table class="table-custom" style="width:100%;border-collapse:collapse;margin:20px 0;">
  <thead>
    <tr style="background:#f8fafc;border-bottom:2px solid #e2e8f0;text-align:left;">
      <th style="padding:10px;">Data Type</th>
      <th style="padding:10px;">Type Name</th>
      <th style="padding:10px;">Example Literal</th>
      <th style="padding:10px;">Mutability</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="padding:10px;"><strong>Integer</strong></td><td><code>int</code></td><td><code>42</code>, <code>-100</code></td><td>Immutable</td></tr>
    <tr><td style="padding:10px;"><strong>Float</strong></td><td><code>float</code></td><td><code>3.14159</code></td><td>Immutable</td></tr>
    <tr><td style="padding:10px;"><strong>String</strong></td><td><code>str</code></td><td><code>"NeuralNine"</code></td><td>Immutable</td></tr>
    <tr><td style="padding:10px;"><strong>Boolean</strong></td><td><code>bool</code></td><td><code>True</code>, <code>False</code></td><td>Immutable</td></tr>
  </tbody>
</table>

{make_callout("💡 Key Concept: Dynamic Typing", "Variables in Python do not have types; <strong>objects have types</strong>. A variable is simply a pointer/reference bound to an object in heap memory.")}
"""
    },
    {
        "num": 2,
        "tier": "Beginner Series",
        "filename": "002 Operators, Conditionals & User Input.html",
        "title": "Operators, Conditionals & User Input",
        "body": f"""
<p>Control flow structures allow your programs to make decisions dynamically based on boolean conditions, logical operators, and interactive user inputs.</p>

<h2>1. If, Elif, Else Branching</h2>
{make_code_tab('''# Reading user input and making decisions
age_input = input("Enter your age: ")
age = int(age_input)

if age >= 18:
    print("Eligible for driving license and voting.")
elif age >= 16:
    print("Eligible for learner permit.")
else:
    years_left = 18 - age
    print(f"You will be eligible in {years_left} years.")''')}

<h2>2. Comparison and Logical Operators</h2>
<p>Python supports chained comparisons which make conditional code exceptionally readable:</p>
{make_code_tab('''score = 85
# Chained comparison (equivalent to: score >= 80 and score < 90)
if 80 <= score < 90:
    grade = "B"
    print(f"Congratulations! Grade: {grade}")''')}
"""
    },
    {
        "num": 3,
        "tier": "Beginner Series",
        "filename": "003 Loops & Iteration (While, For Loops).html",
        "title": "Loops & Iteration (While, For Loops)",
        "body": f"""
<p>Iteration is the backbone of data processing. Python provides <code>for</code> loops for traversing iterables and <code>while</code> loops for condition-controlled repetition.</p>

<h2>1. Range and For Loops</h2>
{make_code_tab('''# Iterating over ranges
for i in range(1, 6):
    print(f"Iteration #{i}")

# Using enumerate for index-value pairs
fruits = ["Apple", "Banana", "Cherry"]
for idx, fruit in enumerate(fruits, start=1):
    print(f"{idx}. {fruit}")''')}

<h2>2. While Loops with Break and Continue</h2>
{make_code_tab('''counter = 0
while True:
    counter += 1
    if counter % 2 == 0:
        continue # Skip even numbers
    if counter > 7:
        break # Exit loop
    print(f"Odd count: {counter}")''')}
"""
    },
    {
        "num": 4,
        "tier": "Beginner Series",
        "filename": "004 Sequences, Collections & Dictionaries.html",
        "title": "Sequences, Collections & Dictionaries",
        "body": f"""
<p>Python's core collections (Lists, Tuples, Sets, and Dictionaries) offer high-speed operations for data grouping, lookup, and transformation.</p>

<h2>1. List Slicing & Comprehensions</h2>
{make_code_tab('''# List Comprehension with filtering
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
squares_of_evens = [n ** 2 for n in numbers if n % 2 == 0]
print("Squares of evens:", squares_of_evens) # [4, 16, 36, 64, 100]

# List Slicing: [start:stop:step]
reversed_nums = numbers[::-1]
print("Reversed:", reversed_nums)''')}

<h2>2. Dictionaries & Sets for O(1) Lookups</h2>
{make_code_tab('''# Fast dictionary key-value lookups
user_roles = {
    "alice": "Admin",
    "bob": "Engineer",
    "charlie": "Designer"
}

# Safe lookup with .get()
role = user_roles.get("david", "Guest")
print(f"David role: {role}")

# Set operations (Union, Intersection, Difference)
dev_skills = {"Python", "SQL", "Docker"}
required_skills = {"Python", "Kubernetes"}
print("Shared skills:", dev_skills & required_skills)''')}
"""
    },
    {
        "num": 5,
        "tier": "Beginner Series",
        "filename": "005 Functions & Exception Handling.html",
        "title": "Functions & Exception Handling",
        "body": f"""
<p>Functions promote code reuse and modularity, while structured exception handling (<code>try/except/finally</code>) ensures your applications fail gracefully without crashing.</p>

<h2>1. Function Signatures with *args and **kwargs</h2>
{make_code_tab('''def create_profile(username, *hobbies, **metadata):
    profile = {
        "username": username,
        "hobbies": list(hobbies),
        "metadata": metadata
    }
    return profile

user = create_profile("alice", "coding", "gaming", role="Admin", verified=True)
print(user)''')}

<h2>2. Robust Error Handling with Try/Except/Finally</h2>
{make_code_tab('''def parse_int_safe(val):
    try:
        result = int(val)
    except (ValueError, TypeError) as err:
        print(f"Parsing error: {err}. Defaulting to 0.")
        return 0
    else:
        print("Parsing successful!")
        return result
    finally:
        print("Cleanup routine executed.")

print(parse_int_safe("42"))
print(parse_int_safe("invalid_num"))''')}
"""
    },
    {
        "num": 6,
        "tier": "Intermediate Series",
        "filename": "006 File Operations & Logging.html",
        "title": "File Operations & Logging",
        "body": f"""
<p>Working with files and configuring enterprise logging are fundamental engineering skills. In this lesson, we explore file I/O context managers, JSON serialization, and Python's built-in <code>logging</code> module.</p>

<h2>1. Safe File Handling with Context Managers</h2>
{make_code_tab('''import json

data = {"server": "prod-01", "port": 8080, "status": "active"}

# Writing JSON to file
with open("config.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

# Reading JSON from file
with open("config.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
    print(f"Loaded config: {loaded['server']}:{loaded['port']}")''')}

<h2>2. Production Logging Setup</h2>
{make_code_tab('''import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("AppLogger")

logger.info("Application starting up...")
logger.warning("Cache size nearing threshold.")
logger.error("Database connection failed!")''')}
"""
    },
    {
        "num": 7,
        "tier": "Intermediate Series",
        "filename": "007 Classes, Objects & Encapsulation.html",
        "title": "Classes, Objects & Encapsulation",
        "body": f"""
<p>Object-Oriented Programming (OOP) allows modeling complex software systems into cohesive objects combining state and behavior. Encapsulation protects internal object state from unauthorized modification.</p>

<h2>1. OOP Core Concepts & Encapsulation Architecture</h2>
{make_image_figure("images/oop_classes_guide.jpg", "Python Classes, Objects, and Encapsulation Architecture")}

<h2>2. Complete Encapsulation Example with Properties</h2>
{make_code_tab('''class BankAccount:
    def __init__(self, owner: str, initial_balance: float = 0.0):
        self.owner = owner
        self.__balance = initial_balance # Private attribute (name mangled)

    @property
    def balance(self) -> float:
        """Getter for balance."""
        return self.__balance

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive!")
        self.__balance += amount
        print(f"Deposited ${amount:.2f}. New Balance: ${self.__balance:.2f}")

    def withdraw(self, amount: float):
        if amount > self.__balance:
            raise ValueError("Insufficient funds!")
        self.__balance -= amount
        print(f"Withdrew ${amount:.2f}. Remaining Balance: ${self.__balance:.2f}")

account = BankAccount("Alice", 100.0)
account.deposit(50.0)
account.withdraw(30.0)
print(f"Final balance: ${account.balance:.2f}")''')}
"""
    },
    {
        "num": 8,
        "tier": "Intermediate Series",
        "filename": "008 Inheritance & Method Overriding.html",
        "title": "Inheritance & Method Overriding",
        "body": f"""
<p>Inheritance allows a child class to inherit attributes and methods from a parent class, enabling polymorphism and DRY (Don't Repeat Yourself) design.</p>

<h2>1. Single & Multiple Inheritance with <code>super()</code></h2>
{make_code_tab('''class Employee:
    def __init__(self, name: str, emp_id: str, salary: float):
        self.name = name
        self.emp_id = emp_id
        self.salary = salary

    def get_role_details(self) -> str:
        return f"{self.name} (ID: {self.emp_id}) - Base Salary: ${self.salary}"

class SoftwareEngineer(Employee):
    def __init__(self, name: str, emp_id: str, salary: float, tech_stack: list):
        super().__init__(name, emp_id, salary) # Call parent constructor
        self.tech_stack = tech_stack

    def get_role_details(self) -> str: # Method Overriding
        base_info = super().get_role_details()
        return f"{base_info} | Tech Stack: {', '.join(self.tech_stack)}"

dev = SoftwareEngineer("Alice", "E-101", 120000, ["Python", "FastAPI", "PostgreSQL"])
print(dev.get_role_details())''')}
"""
    },
    {
        "num": 9,
        "tier": "Intermediate Series",
        "filename": "009 Multithreading, Synchronization & Queues.html",
        "title": "Multithreading, Synchronization & Queues",
        "body": f"""
<p>Concurrency in Python allows executing multiple tasks in parallel or concurrently. In this lesson, we master threads, synchronization locks, daemon threads, and thread-safe queues.</p>

<h2>1. Multithreading Architecture & Thread Synchronization</h2>
{make_image_figure("images/multithreading_guide.jpg", "Python Multithreading, Locks, and Worker Queues Guide")}

<h2>2. Producer-Consumer Pattern with Thread-Safe Queues</h2>
{make_code_tab('''import threading
import queue
import time

task_queue = queue.Queue()

def worker(worker_id):
    while True:
        task = task_queue.get()
        if task is None: # Sentinel shutdown value
            break
        print(f"Worker-{worker_id} processing task: {task}")
        time.sleep(0.5)
        task_queue.task_done()

# Spawn 3 worker threads
threads = []
for i in range(3):
    t = threading.Thread(target=worker, args=(i+1,))
    t.start()
    threads.append(t)

# Enqueue 6 tasks
for task_id in range(1, 7):
    task_queue.put(f"Download_File_{task_id}.pdf")

task_queue.join() # Wait for all tasks to be completed

# Stop workers
for _ in range(3):
    task_queue.put(None)
for t in threads:
    t.join()

print("All worker tasks completed successfully!")''')}
"""
    },
    {
        "num": 10,
        "tier": "Intermediate Series",
        "filename": "010 Sockets, Network & Database Programming.html",
        "title": "Sockets, Network & Database Programming",
        "body": f"""
<p>Low-level network communication via TCP/UDP sockets and relational database persistence using SQLite/PostgreSQL are core components of backend web and microservice systems.</p>

<h2>1. TCP Sockets & Connection Pool Architecture</h2>
{make_image_figure("images/socket_networking_guide.jpg", "Python TCP Sockets and Database Connection Pools Architecture")}

<h2>2. SQLite Database Programming in Python</h2>
{make_code_tab('''import sqlite3

# Connecting to an in-memory SQLite database
with sqlite3.connect(":memory:") as conn:
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL
        )
    """)
    
    # Inserting records with parameterized queries
    users = [("alice", "alice@example.com"), ("bob", "bob@example.com")]
    cursor.executemany("INSERT INTO users (username, email) VALUES (?, ?)", users)
    conn.commit()

    # Querying records
    cursor.execute("SELECT id, username, email FROM users")
    for row in cursor.fetchall():
        print(f"User ID {row[0]}: {row[1]} ({row[2]})")''')}
"""
    },
    {
        "num": 11,
        "tier": "Intermediate Series",
        "filename": "011 Recursion & XML Processing.html",
        "title": "Recursion & XML Processing",
        "body": f"""
<p>Recursion provides elegant solutions for hierarchical data structures like trees and graphs, while XML parsing enables processing legacy enterprise protocols and document schemas.</p>

<h2>1. Recursive Tree Traversal</h2>
{make_code_tab('''class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def calculate_max_depth(root: TreeNode) -> int:
    if root is None:
        return 0
    left_depth = calculate_max_depth(root.left)
    right_depth = calculate_max_depth(root.right)
    return 1 + max(left_depth, right_depth)

# Constructing tree: 1 -> (2, 3 -> (4))
root = TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4)))
print(f"Max tree depth: {calculate_max_depth(root)}") # 3''')}
"""
    },
    {
        "num": 12,
        "tier": "Advanced Series",
        "filename": "012 Magic Methods & Dunder Protocols.html",
        "title": "Magic Methods & Dunder Protocols",
        "body": f"""
<p>Magic methods (dunder methods) allow your custom classes to seamlessly hook into Python's native operators, string conversions, iteration, and context managers.</p>

<h2>1. Building a Custom Container with Dunder Hooks</h2>
{make_code_tab('''class Inventory:
    def __init__(self):
        self._items = {}

    def __setitem__(self, key: str, quantity: int):
        self._items[key] = quantity

    def __getitem__(self, key: str) -> int:
        return self._items.get(key, 0)

    def __len__(self) -> int:
        return len(self._items)

    def __contains__(self, key: str) -> bool:
        return key in self._items

    def __repr__(self) -> str:
        return f"Inventory({self._items!r})"

inv = Inventory()
inv["Laptop"] = 5
inv["Mouse"] = 20
print(len(inv)) # 2
print("Laptop" in inv) # True
print(inv["Mouse"]) # 20
print(inv) # Inventory({'Laptop': 5, 'Mouse': 20})''')}
"""
    },
    {
        "num": 13,
        "tier": "Advanced Series",
        "filename": "013 Decorators & Generators.html",
        "title": "Decorators & Generators",
        "body": f"""
<p>Decorators and Generators represent two of the most powerful metaprogramming and memory-streaming paradigms in modern Python.</p>

<h2>1. Decorators Flow & Generator Yield State Machine</h2>
{make_image_figure("images/decorators_generators_guide.jpg", "Python Decorators and Generators Internals Architecture")}

<h2>2. Combining Decorators with Generators</h2>
{make_code_tab('''import functools
import time

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        print(f"[Timer] {func.__name__} took {duration:.6f}s")
        return result
    return wrapper

@timer
def generate_fibonacci_stream(limit: int):
    a, b = 0, 1
    count = 0
    while count < limit:
        yield a
        a, b = b, a + b
        count += 1

fibs = list(generate_fibonacci_stream(10))
print("First 10 Fibonacci numbers:", fibs)''')}
"""
    },
    {
        "num": 14,
        "tier": "Advanced Series",
        "filename": "014 Argument Parsing & Type Hinting.html",
        "title": "Argument Parsing & Type Hinting",
        "body": f"""
<p>CLI tools and robust enterprise applications rely on static typing for early error catching (PEP 484) and <code>argparse</code> for professional command-line interfaces.</p>

<h2>1. Professional Command-Line Argument Parsing</h2>
{make_code_tab('''import argparse

def create_parser():
    parser = argparse.ArgumentParser(description="Python Server CLI Manager")
    parser.add_argument("--host", default="127.0.0.1", help="Host IP address")
    parser.add_argument("--port", type=int, default=8080, help="Port number")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    return parser

parser = create_parser()
args = parser.parse_args(["--port", "9000", "--debug"])
print(f"Starting server on {args.host}:{args.port} (Debug: {args.debug})")''')}

<h2>2. Modern Type Annotations with Generics and Unions</h2>
{make_code_tab('''from typing import Optional, Union, List, Dict

def find_user_by_id(user_id: int, db: Dict[int, str]) -> Optional[str]:
    return db.get(user_id)

data: Dict[int, str] = {1: "Alice", 2: "Bob"}
user = find_user_by_id(1, data)
print(f"Found user: {user}")''')}
"""
    },
    {
        "num": 15,
        "tier": "Advanced Series",
        "filename": "015 Python Design Patterns - Factory, Singleton, Proxy & Composite.html",
        "title": "Python Design Patterns - Factory, Singleton, Proxy & Composite",
        "body": f"""
<p>Design patterns offer standardized, time-tested architectural solutions to common software design problems. In this lesson, we explore Pythonic implementations of Factory, Singleton, Proxy, and Composite patterns.</p>

<h2>1. Common Python Design Patterns Overview</h2>
{make_image_figure("images/design_patterns_guide.jpg", "Python Design Patterns: Factory, Singleton, Proxy, Composite")}

<h2>2. Singleton & Factory Method Implementation</h2>
{make_code_tab('''# 1. Thread-safe Singleton Pattern
class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connected = True
        return cls._instance

# 2. Factory Pattern
class NotificationFactory:
    @staticmethod
    def create_notifier(channel: str):
        if channel == "email":
            return lambda msg: f"[Email Sent]: {msg}"
        elif channel == "sms":
            return lambda msg: f"[SMS Sent]: {msg}"
        raise ValueError(f"Unknown channel: {channel}")

db1 = DatabaseConnection()
db2 = DatabaseConnection()
print("Same DB Instance?", db1 is db2) # True

notifier = NotificationFactory.create_notifier("email")
print(notifier("Your order has shipped!"))''')}
"""
    },
    {
        "num": 16,
        "tier": "Advanced Series",
        "filename": "016 Statistics, Probability & Hypothesis Testing.html",
        "title": "Statistics, Probability & Hypothesis Testing",
        "body": f"""
<p>This lesson covers the statistics layer used in data-science interviews: probability, sampling, confidence intervals, p-values, hypothesis tests, and A/B experimentation. The goal is to explain results in plain language, not recite formulas.</p>

<h2>1. Probability, Bayes, Expectation</h2>
<p>A pointer is just an index into data. In statistics the same idea shows up as a sample index: we move through observations and ask what we can predict about the next one.</p>
{make_svg_figure("stats_sample_pointer.svg", "Index i pointing at a sample value inside an observation array")}
<p>Start with the core objects: events, conditional probability, Bayes’ theorem, expected value, and variance.</p>
{make_code_tab('''# Bayes: P(disease | positive) with a rare condition
# P(D) = 0.01, P(+|D) = 0.99, P(+|no D) = 0.05
p_d = 0.01
p_pos_given_d = 0.99
p_pos_given_no_d = 0.05
p_pos = p_pos_given_d * p_d + p_pos_given_no_d * (1 - p_d)
p_d_given_pos = (p_pos_given_d * p_d) / p_pos
print(round(p_d_given_pos, 3))  # ~0.167, not 0.99

values = [2, 4, 4, 4, 5, 5, 7, 9]
mean = sum(values) / len(values)
variance = sum((x - mean) ** 2 for x in values) / len(values)
print(mean, variance)''')}
{make_callout("💡 Interview wording", "A <strong>p-value of 0.03</strong> means: if the null were true, data at least this extreme would appear about 3% of the time. It is <em>not</em> the probability that the null is true, and it is not the probability that you replicated the result.")}

<h2>2. Distributions, CLT, Confidence Intervals</h2>
<table class="table-custom" style="width:100%;border-collapse:collapse;margin:20px 0;">
  <thead>
    <tr style="background:#f8fafc;border-bottom:2px solid #e2e8f0;text-align:left;">
      <th style="padding:10px;">Distribution</th>
      <th style="padding:10px;">When you use it</th>
      <th style="padding:10px;">Key parameters</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="padding:10px;"><strong>Bernoulli / Binomial</strong></td><td>Clicks, conversions, pass/fail</td><td>n trials, p success</td></tr>
    <tr><td style="padding:10px;"><strong>Poisson</strong></td><td>Counts per interval (tickets, errors)</td><td>λ rate</td></tr>
    <tr><td style="padding:10px;"><strong>Normal</strong></td><td>Means, residuals, many large-n stats</td><td>μ, σ</td></tr>
  </tbody>
</table>
<p>The Central Limit Theorem says the sampling distribution of the mean becomes approximately normal as n grows, even when the raw data are not normal. That is why a 95% confidence interval for a mean is often:</p>
{make_code_tab('''import math

# 95% CI for a conversion rate (normal approximation)
n, successes = 8000, 1000
p_hat = successes / n
se = math.sqrt(p_hat * (1 - p_hat) / n)
z = 1.96
lo, hi = p_hat - z * se, p_hat + z * se
print(f"p̂ = {p_hat:.4f}, 95% CI = ({lo:.4f}, {hi:.4f})")''')}
{make_callout("⚠️ Sampling vs population", "A confidence interval is a statement about the procedure: in repeated samples, about 95% of such intervals contain the true parameter. One interval either contains it or it does not.")}

<h2>3. Hypothesis Testing Toolkit</h2>
{make_svg_figure("stats_hypothesis_tree.svg", "Hypothesis testing splits into significance tests, confidence intervals, and A/B experiments")}
{make_ul([
    "<strong>Null / alternative</strong> — H0 is the default (no difference). H1 is what you hope to detect.",
    "<strong>Type I (α)</strong> — false positive: reject a true null. Usually 5%.",
    "<strong>Type II (β)</strong> — false negative: miss a real effect. Power = 1 − β.",
    "<strong>z-test</strong> — large n, known or well-estimated variance (e.g. conversion rates).",
    "<strong>t-test</strong> — means with estimated variance, smaller n.",
    "<strong>Chi-square</strong> — independence / goodness of fit on counts.",
    "<strong>ANOVA</strong> — compare means across more than two groups.",
])}
{make_code_tab('''import math

def two_proportion_z(p1, n1, p2, n2):
    """H0: p1 == p2. Returns z and two-sided p (normal approx)."""
    p_pool = (p1 * n1 + p2 * n2) / (n1 + n2)
    se = math.sqrt(p_pool * (1 - p_pool) * (1 / n1 + 1 / n2))
    z = (p1 - p2) / se
    # crude two-sided p via error function
    p_two = math.erfc(abs(z) / math.sqrt(2))
    return z, p_two

# Photoshop onboarding: treatment 13.2% vs control 12.5%
z, p = two_proportion_z(0.132, 20000, 0.125, 20000)
print(round(z, 3), round(p, 4))''')}

<h2>4. A/B Testing: Should We Launch?</h2>
{make_svg_figure("stats_ab_test.svg", "Control versus treatment conversion with a decision pointer")}
<p>Treatment conversion <strong>13.2%</strong>, control <strong>12.5%</strong> is not an automatic ship. Walk this order:</p>
{make_ul([
    "Was assignment randomized? Any selection bias or peeking?",
    "Was the sample size planned for a minimum detectable effect and target power?",
    "Is the result statistically significant <em>and</em> practically meaningful?",
    "What happened to guardrail metrics (latency, refunds, crash rate)?",
    "Multiple tests / novelty effects — did you inflate false positives?",
])}
{make_callout("Launch checklist", "Sample size → hypothesis → confidence → significance → effect size → guardrails → business impact. A tiny lift that is significant on 10M users may still not be worth the engineering or UX cost.", "info")}
"""
    },
    {
        "num": 17,
        "tier": "Advanced Series",
        "filename": "017 SQL for Analytics & Product Metrics.html",
        "title": "SQL for Analytics & Product Metrics",
        "body": f"""
<p>SQL for product and data-science interviews is about joins, filters, window functions, and metric definitions — retention, funnels, and cohorts — not memorizing 300 LeetCode variants. Aim for 50–70 serious problems until these patterns are automatic.</p>

<h2>1. Core Query Building Blocks</h2>
{make_svg_figure("sql_join_pointer.svg", "Joining events to users with an index into the events table")}
{make_ul([
    "<code>JOIN</code> / <code>LEFT JOIN</code> — attach events to users without dropping unmatched rows unless you mean to.",
    "<code>GROUP BY</code> + <code>HAVING</code> — aggregate, then filter groups.",
    "<code>CASE WHEN</code> — bucket metrics and build funnel flags.",
    "<strong>CTEs</strong> and subqueries — name each metric step instead of nesting blindly.",
])}
{make_code_tab('''WITH daily AS (
  SELECT user_id, DATE(event_ts) AS dt, COUNT(*) AS events
  FROM events
  GROUP BY 1, 2
)
SELECT user_id, SUM(events) AS total_events
FROM daily
GROUP BY user_id
HAVING SUM(events) >= 10;''', lang="sql")}

<h2>2. Window Functions</h2>
{make_svg_figure("sql_window_pointer.svg", "ROW_NUMBER window with pointer i on the current user event")}
<table class="table-custom" style="width:100%;border-collapse:collapse;margin:20px 0;">
  <thead>
    <tr style="background:#f8fafc;border-bottom:2px solid #e2e8f0;text-align:left;">
      <th style="padding:10px;">Function</th>
      <th style="padding:10px;">Typical use</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="padding:10px;"><code>ROW_NUMBER()</code></td><td>First event per user, latest session</td></tr>
    <tr><td style="padding:10px;"><code>RANK()</code> / <code>DENSE_RANK()</code></td><td>Leaderboards; ties handled differently</td></tr>
    <tr><td style="padding:10px;"><code>LAG()</code> / <code>LEAD()</code></td><td>Previous/next date, session gaps</td></tr>
    <tr><td style="padding:10px;">Rolling <code>AVG() OVER (... ROWS)</code></td><td>7-day moving averages</td></tr>
  </tbody>
</table>
{make_code_tab('''SELECT
  user_id,
  event_ts,
  ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_ts) AS event_n,
  LAG(event_ts) OVER (PARTITION BY user_id ORDER BY event_ts) AS prev_ts,
  AVG(amount) OVER (
    PARTITION BY user_id
    ORDER BY event_ts
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) AS rolling_7_amt
FROM events;''', lang="sql")}

<h2>3. Retention (D1 / D7 / D30)</h2>
<p>Define a cohort (signup day) and check whether the user returned on day N.</p>
{make_code_tab('''WITH first_seen AS (
  SELECT user_id, DATE(MIN(event_ts)) AS cohort_dt
  FROM events
  GROUP BY user_id
),
activity AS (
  SELECT DISTINCT user_id, DATE(event_ts) AS dt
  FROM events
)
SELECT
  f.cohort_dt,
  COUNT(*) AS users,
  AVG(CASE WHEN d1.user_id IS NOT NULL THEN 1.0 ELSE 0 END) AS d1,
  AVG(CASE WHEN d7.user_id IS NOT NULL THEN 1.0 ELSE 0 END) AS d7,
  AVG(CASE WHEN d30.user_id IS NOT NULL THEN 1.0 ELSE 0 END) AS d30
FROM first_seen f
LEFT JOIN activity d1
  ON d1.user_id = f.user_id AND d1.dt = DATE(f.cohort_dt, '+1 day')
LEFT JOIN activity d7
  ON d7.user_id = f.user_id AND d7.dt = DATE(f.cohort_dt, '+7 day')
LEFT JOIN activity d30
  ON d30.user_id = f.user_id AND d30.dt = DATE(f.cohort_dt, '+30 day')
GROUP BY f.cohort_dt;''', lang="sql")}
{make_callout("💡 Metric definition", "Interviewers care whether D1 means <em>any event on calendar day +1</em> vs <em>returned within 24 hours</em>. State the definition before writing SQL.")}

<h2>4. Funnels, Cohorts, Top Percentiles</h2>
{make_svg_figure("sql_funnel_tree.svg", "Product SQL patterns: retention, funnels, and cohort conversion")}
<p>Classic prompts: users who used feature A before buying B; conversion by cohort; top 10% most engaged users.</p>
{make_code_tab('''-- Feature A before purchase B
WITH a AS (
  SELECT user_id, MIN(event_ts) AS a_ts
  FROM events WHERE event_name = 'feature_a' GROUP BY 1
),
b AS (
  SELECT user_id, MIN(event_ts) AS b_ts
  FROM events WHERE event_name = 'purchase_b' GROUP BY 1
)
SELECT COUNT(*) AS converted
FROM a JOIN b USING (user_id)
WHERE a.a_ts < b.b_ts;

-- Top 10% engaged users (by event count)
WITH counts AS (
  SELECT user_id, COUNT(*) AS n
  FROM events
  GROUP BY user_id
),
ranked AS (
  SELECT user_id, n,
         PERCENT_RANK() OVER (ORDER BY n) AS pct
  FROM counts
)
SELECT user_id, n
FROM ranked
WHERE pct >= 0.90;''', lang="sql")}
{make_callout("Practice set", "Drill JOIN, GROUP BY, HAVING, CASE, CTEs, ROW_NUMBER/RANK/DENSE_RANK, LAG/LEAD, rolling averages, date math, retention, funnels, and cohorts until you can write them without a cheat sheet.", "info")}
"""
    }
]

def build_all():
    os.makedirs('Python Course', exist_ok=True)
    os.makedirs('Python Course/images', exist_ok=True)
    
    for lesson in CURRICULUM:
        num_str = f"{lesson['num']:02d}"
        
        # Build sidebar menu with tiers
        sider_items = ""
        current_tier = ""
        for item in CURRICULUM:
            if item['tier'] != current_tier:
                current_tier = item['tier']
                sider_items += f"""<li style="padding:14px 16px 4px;font-size:12px;color:#35cea0;font-weight:700;text-transform:uppercase;letter-spacing:1px;">{current_tier}</li>"""

            is_active = (item['num'] == lesson['num'])
            selected_cls = " ant-menu-item-selected" if is_active else ""
            sider_items += f"""
<li class="ant-menu-item{selected_cls}" role="menuitem" style="padding-left:16px;">
  <a href="{item['filename']}" style="display:flex;align-items:center;color:inherit;text-decoration:none;width:100%;height:100%;">
    <span style="font-family:monospace;font-size:11px;background:rgba(255,255,255,0.15);padding:2px 5px;border-radius:3px;margin-right:8px;color:#fff;">{item['num']:02d}</span>
    <span style="font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{item['title']}</span>
  </a>
</li>"""

        custom_aside = f"""<aside class="ant-layout-sider style_sider__Hlcz3 css-133v4sd" style="flex:0 0 310px;max-width:310px;min-width:310px;width:310px;">
  <div class="ant-layout-sider-children">
    <h2 style="padding:10px 16px 6px;font-size:14px;color:#aaa;font-weight:600;margin:0;">Python Masterclass</h2>
    <ul class="ant-menu ant-menu-root ant-menu-inline ant-menu-dark css-133v4sd" role="menu">
      {sider_items}
    </ul>
  </div>
</aside>"""

        head = re.sub(r'<aside[^>]*>.*?</aside>', custom_aside, HEAD_TEMPLATE, flags=re.DOTALL)
        if "style_codeTabs__DEEq6 .ant-tabs-nav" not in head:
            if "</title>" in head:
                head = head.replace("</title>", "</title>" + CODE_WIDGET_CSS, 1)
            else:
                head = CODE_WIDGET_CSS + head
        
        # Navigation buttons
        prev_btn = ""
        if lesson['num'] > 1:
            prev_l = CURRICULUM[lesson['num'] - 2]
            prev_btn = f'<a href="{prev_l["filename"]}" class="ant-btn ant-btn-default" style="display:inline-flex;align-items:center;gap:6px;border-radius:6px;font-weight:600;">← {prev_l["title"]}</a>'
        else:
            prev_btn = '<a href="../index.html" class="ant-btn ant-btn-default" style="display:inline-flex;align-items:center;gap:6px;border-radius:6px;font-weight:600;">← Back to Hub</a>'

        next_btn = ""
        if lesson['num'] < len(CURRICULUM):
            next_l = CURRICULUM[lesson['num']]
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
        if 'id="py-code-tabs"' not in full_html[-4000:]:
            full_html += CODE_WIDGET_CSS
        if "style_copyBtn__4MbAa" in full_html and "navigator.clipboard" not in full_html:
            full_html += CODE_WIDGET_JS
        if "nav_inject.js" not in full_html:
            full_html += """
<!-- nav-inject-patched -->
<script src="../nav_map.js"></script>
<script src="../nav_inject.js"></script>
"""
        target_path = os.path.join('Python Course', lesson['filename'])
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(full_html)

    print(f"Generated all {len(CURRICULUM)} lessons with embedded images and ByteByteGo styles!")

if __name__ == '__main__':
    build_all()
