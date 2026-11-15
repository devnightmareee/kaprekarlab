import argparse, json
from . import __version__
from .apps import (KaprekarRNG, ascii_histogram, explain, explorer_html, grade_file, histogram_svg,
                   kaprekar_hash, known_answers, quiz, to_csv, trajectory_svg, worksheet, worst_cases)
from .core import analyze, is_kaprekar, kaprekar_numbers, routine


def main(argv=None):
    p = argparse.ArgumentParser("kaprekarlab", description="Kaprekar numbers & routine toolkit")
    p.add_argument("--version", action="version", version=__version__)
    sp = p.add_subparsers(dest="cmd", required=True)
    a = sp.add_parser("check", help="is N a Kaprekar number?"); a.add_argument("n", type=int); a.add_argument("--base", type=int, default=10)
    a = sp.add_parser("list", help="Kaprekar numbers up to LIMIT"); a.add_argument("limit", type=int); a.add_argument("--base", type=int, default=10)
    a = sp.add_parser("routine", help="run the Kaprekar routine on N")
    a.add_argument("n", type=int); a.add_argument("--digits", type=int, default=4); a.add_argument("--lang", choices=["en", "fa"], default="en"); a.add_argument("--json", action="store_true")
    a = sp.add_parser("analyze", help="attractors & step histogram"); a.add_argument("--digits", type=int, default=4); a.add_argument("--base", type=int, default=10); a.add_argument("--json", action="store_true")
    a = sp.add_parser("svg", help="histogram (or path of N) as SVG"); a.add_argument("--digits", type=int, default=4); a.add_argument("--path", type=int, help="draw the path of this number instead")
    a = sp.add_parser("quiz", help="practice questions"); a.add_argument("-n", type=int, default=5); a.add_argument("--seed", type=int); a.add_argument("--lang", choices=["en", "fa"], default="en")
    a = sp.add_parser("worksheet", help="printable Markdown worksheet + answer key"); a.add_argument("-n", type=int, default=10); a.add_argument("--seed", type=int); a.add_argument("--lang", choices=["en", "fa"], default="fa")
    a = sp.add_parser("grade", help="grade a student .py file that defines steps(n) (runs their code!)"); a.add_argument("file"); a.add_argument("--digits", type=int, default=4)
    a = sp.add_parser("csv", help="every number's steps/attractor as CSV"); a.add_argument("--digits", type=int, default=4); a.add_argument("--base", type=int, default=10)
    a = sp.add_parser("worst", help="inputs needing the most steps (edge-case tests)"); a.add_argument("--digits", type=int, default=4); a.add_argument("--limit", type=int, default=20)
    a = sp.add_parser("html", help="write an offline interactive explorer page"); a.add_argument("out")
    a = sp.add_parser("rng", help="educational RNG"); a.add_argument("seed", type=int); a.add_argument("-n", type=int, default=10)
    a = sp.add_parser("hash", help="toy checksum"); a.add_argument("text")
    a = sp.add_parser("vectors", help="known-answer JSON"); a.add_argument("--digits", type=int, default=4)
    r = p.parse_args(argv)
    if r.cmd == "check": print(is_kaprekar(r.n, r.base))
    elif r.cmd == "list": print(*kaprekar_numbers(r.limit, r.base))
    elif r.cmd == "routine":
        if r.json:
            t = routine(r.n, r.digits)
            print(json.dumps({"start": t.start, "path": t.path, "steps": t.steps, "kind": t.kind, "attractor": t.attractor}))
        else:
            print("\n".join(explain(r.n, r.digits, lang=r.lang)))
    elif r.cmd == "analyze":
        an = analyze(r.digits, r.base)
        if r.json:
            print(json.dumps({"constants": an.constants, "max_steps": an.max_steps, "steps": dict(an.steps),
                              "attractors": {"-".join(map(str, k)): v for k, v in an.attractors.items()}}))
        else:
            print("constants:", an.constants, "| max steps:", an.max_steps)
            for at, c in an.attractors.most_common(): print(" attractor", at, "<-", c, "numbers")
            print(ascii_histogram(r.digits, r.base))
    elif r.cmd == "svg": print(trajectory_svg(r.path, r.digits) if r.path is not None else histogram_svg(r.digits))
    elif r.cmd == "quiz":
        for q, ans in quiz(r.n, r.seed, r.lang): print(q, " [", ans, "]")
    elif r.cmd == "worksheet": print(worksheet(r.n, r.seed, r.lang))
    elif r.cmd == "grade":
        g = grade_file(r.file, r.digits)
        print(f"score {g['score']}%  ({g['correct']}/{g['total']})")
        for n, want, got in g["mismatches"]: print(f"  n={n}: expected {want}, got {got}")
    elif r.cmd == "csv": print(to_csv(r.digits, r.base), end="")
    elif r.cmd == "worst":
        w = worst_cases(r.digits); print(*w[:r.limit], f"... ({len(w)} total)" if len(w) > r.limit else "")
    elif r.cmd == "html":
        open(r.out, "w", encoding="utf-8").write(explorer_html()); print("wrote", r.out)
    elif r.cmd == "rng": g = KaprekarRNG(r.seed); print(*[next(g) for _ in range(r.n)], "| period:", KaprekarRNG(r.seed).period())
    elif r.cmd == "hash": print(kaprekar_hash(r.text))
    elif r.cmd == "vectors": print(json.dumps(known_answers(r.digits)))
