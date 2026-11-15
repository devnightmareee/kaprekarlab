"""Application helpers built on the core: education, testing, RNG, checksum demo, charts."""
from __future__ import annotations
import random
from typing import Iterator, List, Tuple

from .core import (analyze, from_digits, is_kaprekar, kaprekar_numbers,
                   routine, to_digits)


# ---------- education ----------
_FA = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
_MSG = {
    "en": {"done": "-> {kind} reached after {steps} step(s): {att}", "kinds": {"fixed": "fixed point", "cycle": "cycle", "zero": "zero"},
           "isk": "Is {n} a Kaprekar number?", "stp": "How many Kaprekar-routine steps does {n} need?",
           "yes": "yes", "no": "no", "title": "Kaprekar worksheet", "key": "Answer key", "name": "Name"},
    "fa": {"done": "← {kind} پس از {steps} گام: {att}", "kinds": {"fixed": "نقطهٔ ثابت", "cycle": "چرخه", "zero": "صفر"},
           "isk": "آیا {n} یک عدد کاپرکار است؟", "stp": "عدد {n} در فرایند کاپرکار چند گام تا رسیدن به ثابت نیاز دارد؟",
           "yes": "بله", "no": "خیر", "title": "برگهٔ تمرین اعداد کاپرکار", "key": "پاسخ‌نامه", "name": "نام"},
}


def _fa(text: str, lang: str) -> str:
    return text.translate(_FA) if lang == "fa" else text


def explain(n: int, digits: int = 4, base: int = 10, lang: str = "en") -> List[str]:
    """Human-readable, step-by-step walkthrough of the routine."""
    t = routine(n, digits, base)
    lines = []
    for a, b in zip(t.path, t.path[1:] + (t.path[t.cycle_start],)):
        ds = sorted(to_digits(a, base, digits))
        hi, lo = from_digits(ds[::-1], base), from_digits(ds, base)
        lines.append(f"{hi:0{digits}d} - {lo:0{digits}d} = {b:0{digits}d}")
        if b in t.path[: t.path.index(a) + 1] or b == a:
            break
    m = _MSG[lang]
    lines.append(_fa(m["done"].format(kind=m["kinds"][t.kind], steps=t.steps,
                                      att=" , ".join(map(str, t.attractor))), lang))
    return lines


def quiz(count: int = 5, seed: int | None = None, lang: str = "en") -> List[Tuple[str, str]]:
    """Random (question, answer) pairs for classroom practice."""
    rnd, out, m = random.Random(seed), [], _MSG[lang]
    for _ in range(count):
        if rnd.random() < .5:
            n = rnd.choice(rnd.choice([kaprekar_numbers(10000), list(range(1, 10000))]))
            out.append((_fa(m["isk"].format(n=n), lang), m["yes" if is_kaprekar(n) else "no"]))
        else:
            n = rnd.randrange(1000, 10000)
            t = routine(n)
            out.append((_fa(m["stp"].format(n=f"{n:04d}"), lang), _fa(str(t.steps), lang)))
    return out


# ---------- testing / benchmarking ----------
def known_answers(digits: int = 4, base: int = 10, limit: int | None = None) -> dict:
    """{start: (steps, attractor)} - ready-made known-answer test data for any language."""
    return {n: (t.steps, t.attractor[0]) for n in range(limit or base ** digits)
            for t in [routine(n, digits, base)]}


# ---------- experiments ----------
class KaprekarRNG:
    """Educational 'square-split' generator: x -> (high half + low half of x^2) mod 10^d.
    NOT for security or serious simulation; its short periods are the lesson."""

    def __init__(self, seed: int, digits: int = 4):
        self.d, self.x = digits, seed % 10 ** digits or 1

    def __iter__(self) -> Iterator[int]:
        return self

    def __next__(self) -> int:
        s = f"{self.x * self.x:0{2 * self.d}d}"
        self.x = (int(s[: self.d]) + int(s[self.d:])) % 10 ** self.d or 1
        return self.x

    def period(self) -> int:
        seen, x, i = {}, self.x, 0
        r = KaprekarRNG(x, self.d)
        while x not in seen:
            seen[x] = i
            x, i = next(r), i + 1
        return i - seen[x]


def kaprekar_hash(data: bytes | str, digits: int = 8) -> int:
    """Tiny digit-mixing checksum for teaching (NOT cryptographic)."""
    if isinstance(data, str):
        data = data.encode()
    mod, h = 10 ** digits, 6174
    for b in data:
        h = (h * 31 + b + 1) % mod
        s = sorted(f"{h:0{digits}d}")
        h = (int("".join(s[::-1])) - int("".join(s)) + h) % mod
    return h


# ---------- visualisation ----------
def histogram_svg(digits: int = 4, base: int = 10, width: int = 560, height: int = 260) -> str:
    """SVG bar chart: how many starting numbers need k steps."""
    st = {k: v for k, v in analyze(digits, base).steps.items()}
    top, n = max(st.values()), max(st) + 1
    bw = width / n
    bars = []
    for k in range(n):
        v, h = st.get(k, 0), (height - 60) * st.get(k, 0) / top
        x = k * bw + bw * .15
        bars.append(f'<rect x="{x:.1f}" y="{height - 30 - h:.1f}" width="{bw * .7:.1f}" height="{h:.1f}" fill="#d9b45b"/>'
                    f'<text x="{x + bw * .35:.1f}" y="{height - 34 - h:.1f}" font-size="13" text-anchor="middle" fill="#fff">{v}</text>'
                    f'<text x="{x + bw * .35:.1f}" y="{height - 10}" font-size="14" text-anchor="middle" fill="#fff">{k}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" font-family="DejaVu Sans,sans-serif">'
            + "".join(bars) + "</svg>")


def ascii_histogram(digits: int = 4, base: int = 10, cols: int = 40) -> str:
    st = analyze(digits, base).steps
    top = max(st.values())
    return "\n".join(f"{k:>2} | {'#' * max(1, cols * st[k] // top)} {st[k]}" for k in sorted(st))


def worksheet(count: int = 10, seed: int | None = None, lang: str = "en") -> str:
    """Printable Markdown worksheet with an answer key (Persian or English)."""
    qs, m = quiz(count, seed, lang), _MSG[lang]
    body = [f"# {m['title']}", "", f"{m['name']}: ____________________", ""]
    body += [f"{_fa(str(i), lang)}. {q}  ____" for i, (q, _) in enumerate(qs, 1)]
    body += ["", f"## {m['key']}", ""] + [f"{_fa(str(i), lang)}. {a}" for i, (_, a) in enumerate(qs, 1)]
    return "\n".join(body) + "\n"


# ---------- data export & worst cases ----------
def to_csv(digits: int = 4, base: int = 10) -> str:
    """CSV (start,steps,kind,attractor) for every number - open it in Excel / Sheets / pandas."""
    rows = ["start,steps,kind,attractor"]
    for n in range(base ** digits):
        t = routine(n, digits, base)
        rows.append(f"{n:0{digits}d},{t.steps},{t.kind},{'-'.join(map(str, t.attractor))}")
    return "\n".join(rows) + "\n"


def worst_cases(digits: int = 4, base: int = 10) -> List[int]:
    """Starting numbers that need the maximum number of steps - ideal edge-case test inputs."""
    top = analyze(digits, base).max_steps
    return [n for n in range(base ** digits) if routine(n, digits, base).steps == top]


def trajectory_svg(n: int, digits: int = 4, base: int = 10) -> str:
    """SVG strip showing the path n -> ... -> attractor."""
    path = routine(n, digits, base).path
    w, gap = 96, 36
    width = len(path) * (w + gap) - gap + 20
    parts = []
    for i, v in enumerate(path):
        x = 10 + i * (w + gap)
        parts.append(f'<rect x="{x}" y="10" width="{w}" height="46" rx="10" fill="#1d3557" stroke="#d9b45b" stroke-width="2"/>'
                     f'<text x="{x + w / 2}" y="40" font-size="22" font-weight="bold" text-anchor="middle" fill="#fff">{v:0{digits}d}</text>')
        if i + 1 < len(path):
            parts.append(f'<text x="{x + w + gap / 2}" y="40" font-size="24" text-anchor="middle" fill="#d9b45b">&#8594;</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} 66" font-family="DejaVu Sans,sans-serif">'
            + "".join(parts) + "</svg>")


# ---------- grading student programs ----------
def grade_function(func, digits: int = 4, base: int = 10) -> dict:
    """Check func(n) -> steps-to-attractor against the library on every non-repdigit n with `digits` digits."""
    bad, total = [], 0
    for n in range(base ** (digits - 1), base ** digits):
        t = routine(n, digits, base)
        if t.kind == "zero":
            continue
        total += 1
        try:
            got = func(n)
        except Exception as e:  # a crashing student program is just a wrong answer
            got = f"error: {e}"
        if got != t.steps:
            bad.append((n, t.steps, got))
    return {"total": total, "correct": total - len(bad),
            "score": round(100 * (total - len(bad)) / total, 1), "mismatches": bad[:10]}


def grade_file(path: str, digits: int = 4) -> dict:
    """Load a student's .py file that defines steps(n) and grade it. WARNING: this runs their code."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("student_submission", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return grade_function(mod.steps, digits)


# ---------- offline interactive page ----------
EXPLORER_HTML = r"""<!doctype html><html lang="fa" dir="rtl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Kaprekar Explorer</title><style>body{font-family:Tahoma,sans-serif;max-width:640px;margin:30px auto;padding:0 16px;background:#0f1b2d;color:#eef2f7}
h1{color:#d9b45b}input,button{font-size:18px;padding:6px 10px;margin:4px;border-radius:8px;border:1px solid #d9b45b}input{background:#07101d;color:#ffe9a8}
button{background:#d9b45b;font-weight:bold;cursor:pointer}pre{background:#07101d;padding:14px;border-radius:10px;direction:ltr;font-size:17px;line-height:1.6}</style>
<h1>کاوشگر کاپرکار · Kaprekar Explorer</h1>
<label>عدد / number <input id="n" value="3524"></label><label>رقم‌ها / digits <input id="d" value="4" size="2"></label><button onclick="run()">محاسبه</button>
<pre id="o"></pre><script>
function isK(n){if(n==1n)return true;const s=(n*n).toString();for(let i=1;i<s.length;i++){const r=BigInt(s.slice(i)),l=BigInt(s.slice(0,i));if(r>0n&&l+r===n)return true}return false}
function run(){const d=+document.getElementById('d').value||4;let x=BigInt(document.getElementById('n').value||0),seen={},k=0,out=['Kaprekar number? '+isK(x)];
while(!(x in seen)){seen[x]=k++;const s=x.toString().padStart(d,'0').split('').sort(),lo=BigInt(s.join('')),hi=BigInt(s.slice().reverse().join('')),nx=hi-lo;
out.push(hi.toString().padStart(d,'0')+' - '+lo.toString().padStart(d,'0')+' = '+nx.toString().padStart(d,'0'));x=nx}
out.push('-> repeats at '+x.toString().padStart(d,'0')+' after '+seen[x]+' step(s)');document.getElementById('o').textContent=out.join('\n')}
run()</script></html>
"""


def explorer_html() -> str:
    """Self-contained HTML page (no Python needed) where students try any number."""
    return EXPLORER_HTML
