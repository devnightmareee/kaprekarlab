# kaprekarlab

A small, dependency-free Python toolkit for **Kaprekar numbers** and the **Kaprekar routine** (the famous constant **6174**), created by Parsa Daryabar (dev_nightmare) and students of Kamal School as a school project.

> Named in honour of **D. R. Kaprekar** (1905–1986), the Indian schoolteacher who discovered these patterns.

---

## 🇬🇧 English

### What are they?

- **Kaprekar number**: `n` such that splitting `n²` into two parts (right part > 0) and adding them gives `n`. Example: `45² = 2025 → 20 + 25 = 45`.
- **Kaprekar routine**: sort the digits descending and ascending, subtract, repeat. Every 4-digit number (not all digits equal) reaches **6174** in at most **7** steps; 3-digit numbers reach **495**.

### Install & try

```bash
pip install kaprekarlab          # from PyPI (Python 3.8+, no dependencies)
kaprekarlab routine 3524         # step-by-step walkthrough to 6174
kaprekarlab list 10000           # all Kaprekar numbers up to 10000
kaprekarlab analyze --digits 3   # constants, cycles, step histogram
kaprekarlab quiz -n 5            # practice questions
```

### From source

```bash
git clone https://github.com/devnightmareee/kaprekarlab && cd kaprekarlab
pip install -e .
python -m unittest discover -s tests
```

### API

```python
from kaprekarlab import is_kaprekar, routine, analyze, explain

is_kaprekar(297)                 # True
routine(3524).path               # (3524, 3087, 8352, 6174)
analyze(4).constants             # [6174]
analyze(2).attractors            # { (9,81,63,27,45): ... }
```

### CLI reference

| Command | Description |
|---------|-------------|
| `kaprekarlab check N` | Is N a Kaprekar number? |
| `kaprekarlab list LIMIT` | All Kaprekar numbers up to LIMIT |
| `kaprekarlab routine N [--digits N]` | Step-by-step to fixed point |
| `kaprekarlab analyze [--digits N] [--base B]` | Attractors, max steps, histogram |
| `kaprekarlab svg [--path N]` | SVG histogram or trajectory |
| `kaprekarlab quiz [-n N] [--lang fa\|en]` | Practice questions |
| `kaprekarlab worksheet [-n N] [--lang fa\|en]` | Printable worksheet + key |
| `kaprekarlab grade FILE` | Grade a student `.py` (runs their code!) |
| `kaprekarlab csv [--digits N] [--base B]` | CSV of every number's trajectory |
| `kaprekarlab worst [--digits N] [--limit N]` | Edge-case inputs needing max steps |
| `kaprekarlab html OUT` | Offline interactive explorer page |
| `kaprekarlab rng SEED [-n N]` | Educational RNG based on the routine |
| `kaprekarlab hash TEXT` | Toy checksum |
| `kaprekarlab vectors [--digits N]` | Known-answer JSON for cross-checking |

> `grade` imports and runs the student's file — only grade code you trust.

### Workflow ideas

- **Grade programs automatically**: Student writes `steps(n)` in `student.py` → `kaprekarlab grade student.py` checks it on all 8,991 four-digit inputs and lists mismatches.
- **Hand out practice sheets**: `kaprekarlab worksheet -n 10 --lang fa > sheet.md`
- **Analyse in Excel / Sheets / pandas**: `kaprekarlab csv --digits 4 > data.csv`
- **Cross-check another language**: `kaprekarlab vectors > vectors.json`
- **Draw figures for reports**: `kaprekarlab svg` (histogram) or `kaprekarlab svg --path 3524`
- **Explore other bases / digit counts**: `is_kaprekar(n, base)`, `analyze(digits, base)`

### Contributing

Ideas welcome: new bases, faster algorithms, other languages (JS, C, Rust), classroom worksheets, better visualisations. Open an issue or a pull request and add tests.

### License

MIT © Parsa Daryabar (dev_nightmare) and kaprekarlab contributors

---

## 🇮🇷 فارسی

### اعداد کاپرکار و فرایند کاپرکار (ثابت ۶۱۷۴) چیست؟

- **عدد کاپرکار**: عدد `n` هست که اگر مربعش رو به دو قسمت تقسیم کنیم (قسمت راست بزرگتر از صفر باشه) و جمعشون کنیم، خود `n` بدست بیاد. مثال: `45² = 2025 → 20 + 25 = 45`.
- **فرایند کاپرکار**: ارقام عدد رو نزولی و صعودی مرتب کن، کم کن، تکرار کن. هر عدد چهار رقمی (که همه ارقامش یکی نباشه) حداکثر در **۷** گام به **۶۱۷۴** می‌رسه؛ اعداد سه رقمی به **۴۹۵** می‌رسن.

### نصب و استفاده

```bash
pip install kaprekarlab          # از PyPI (پایتون ۳.۸+، بدون وابستگی)
kaprekarlab routine 3524         # گام به گام تا ۶۱۷۴
kaprekarlab list 10000           # تمام اعداد کاپرکار تا ۱۰۰۰۰
kaprekarlab analyze --digits 3   # ثابت‌ها، چرخه‌ها، نمودار گام‌ها
kaprekarlab quiz -n 5 --lang fa  # سوالات تمرینی به فارسی
```

### از سورس

```bash
git clone https://github.com/devnightmareee/kaprekarlab && cd kaprekarlab
pip install -e .
python -m unittest discover -s tests
```

### API

```python
from kaprekarlab import is_kaprekar, routine, analyze, explain

is_kaprekar(297)                 # True
routine(3524).path               # (3524, 3087, 8352, 6174)
analyze(4).constants             # [6174]
explain(3524, lang="fa")        # ['۵۴۳۲ - ۲۳۴۵ = ۳۰۸۷', '...']
```

### خط فرمان

| دستور | توضیح |
|-------|-------|
| `kaprekarlab check N` | آیا N عدد کاپرکار است؟ |
| `kaprekarlab list LIMIT` | تمام اعداد کاپرکار تا LIMIT |
| `kaprekarlab routine N [--digits N]` | گام‌به‌گام تا نقطه ثابت |
| `kaprekarlab analyze [--digits N] [--base B]` | جذاب‌ترین‌ها، بیشترین گام، نمودار |
| `kaprekarlab svg [--path N]` | نمودار SVG مسیر یا توزیع |
| `kaprekarlab quiz [-n N] [--lang fa\|en]` | سوالات تمرینی |
| `kaprekarlab worksheet [-n N] [--lang fa\|en]` | برگه تمرین + پاسخ‌نامه |
| `kaprekarlab grade FILE` | تصحیح فایل `.py` دانش‌آموز (کدشان اجرا می‌شود!) |
| `kaprekarlab csv [--digits N] [--base B]` | خروجی CSV تمام مسیرها |
| `kaprekarlab worst [--digits N] [--limit N]` | ورودی‌های لبه (نیازمند بیشترین گام) |
| `kaprekarlab html OUT` | صفحه تعاملی آفلاین |
| `kaprekarlab rng SEED [-n N]` | تولیدکننده تصادفی آموزشی |
| `kaprekarlab hash TEXT` | هش نمونه |
| `kaprekarlab vectors [--digits N]` | JSON پاسخ‌های شناخته‌شده برای بررسی متقاطع |

> `grade` فایل دانش‌آموز را ایمپورت و اجرا می‌کند — فقط کدی را تصحیح کنید که به آن اعتماد دارید.

### کاربردها

- **تصحیح خودکار برنامه‌های دانش‌آموزان**: دانش‌آموز تابع `steps(n)` را در `student.py` می‌نویسد → `kaprekarlab grade student.py` روی ۸۹۹۱ ورودی چهاررقمی بررسی می‌کند.
- **برگه تمرین**: `kaprekarlab worksheet -n 10 --lang fa > sheet.md`
- **تحلیل در اکسل / گوگل شیت / pandas**: `kaprekarlab csv --digits 4 > data.csv`
- **بررسی متقاطع زبان‌های دیگر**: `kaprekarlab vectors > vectors.json`
- **رسم شکل برای گزارش**: `kaprekarlab svg` (هیستوگرام) یا `kaprekarlab svg --path 3524`
- **کاوش پایه‌ها / تعداد ارقام مختلف**: `is_kaprekar(n, base)` و `analyze(digits, base)`

### مشارکت

ایده‌ها خوش‌آمد است: پایه‌های جدید، الگوریتم‌های سریع‌تر، زبان‌های دیگر (JS، C، Rust)، برگه‌های کلاسی، مصورسازی‌های بهتر. issue یا PR باز کنید و تست اضافه کنید.

### مجوز

MIT © پارسا دریابُر (dev_nightmare) و مشارکت‌کنندگان kaprekarlab
