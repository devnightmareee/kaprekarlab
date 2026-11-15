import unittest
from kaprekarlab import *
from kaprekarlab.apps import KaprekarRNG


class T(unittest.TestCase):
    def test_numbers(self):
        self.assertEqual(kaprekar_numbers(10000),
            [1, 9, 45, 55, 99, 297, 703, 999, 2223, 2728, 4879, 4950, 5050, 5292, 7272, 7777, 9999])
        self.assertFalse(is_kaprekar(10)); self.assertFalse(is_kaprekar(100))

    def test_routine(self):
        t = routine(3524)
        self.assertEqual(t.path, (3524, 3087, 8352, 6174))
        self.assertEqual((t.steps, t.kind, t.attractor), (3, "fixed", (6174,)))
        self.assertEqual(routine(1111).kind, "zero")

    def test_constants(self):
        a4 = analyze(4)
        self.assertEqual(a4.constants, [6174]); self.assertEqual(a4.max_steps, 7)
        self.assertEqual(analyze(3).constants, [495]); self.assertEqual(analyze(3).max_steps, 6)
        self.assertEqual(sum(a4.attractors.values()), 10000)

    def test_two_digit_cycle(self):
        self.assertIn((9, 81, 63, 27, 45), analyze(2).attractors)

    def test_other_base(self):
        self.assertTrue(is_kaprekar(3, 4))  # 3^2 = 21_4 -> 2 + 1 = 3
        self.assertEqual(from_digits(to_digits(1234, 7), 7), 1234)

    def test_apps(self):
        self.assertEqual(explain(3524)[0], "5432 - 2345 = 3087")
        self.assertEqual(len(quiz(4, seed=1)), 4)
        self.assertGreaterEqual(KaprekarRNG(1234).period(), 1)
        self.assertEqual(kaprekar_hash("abc"), kaprekar_hash(b"abc"))
        self.assertTrue(histogram_svg().startswith("<svg"))


class T2(unittest.TestCase):
    def test_fast_filter(self):
        from kaprekarlab.core import is_kaprekar as k
        for base in (10, 7, 16):
            self.assertEqual(kaprekar_numbers(3000, base), [n for n in range(1, 3001) if k(n, base)])

    def test_practical(self):
        self.assertEqual(max(analyze(4).steps), 7)
        w = worst_cases(); self.assertTrue(w and all(routine(n).steps == 7 for n in w))
        self.assertTrue(to_csv().startswith("start,steps,kind,attractor\n0000,0,zero,0"))
        self.assertIn("۱.", worksheet(3, seed=1, lang="fa")); self.assertIn("پاسخ‌نامه", worksheet(3, 1, "fa"))
        self.assertTrue(trajectory_svg(3524).startswith("<svg")); self.assertIn("<html", explorer_html())
        self.assertIn("گام", explain(3524, lang="fa")[-1])

    def test_grade(self):
        ok = grade_function(lambda n: routine(n).steps)
        self.assertEqual((ok["score"], ok["total"]), (100.0, 8991))
        bad = grade_function(lambda n: 3)
        self.assertLess(bad["score"], 50); self.assertTrue(bad["mismatches"])
        self.assertEqual(grade_function(lambda n: 1 / 0)["correct"], 0)


if __name__ == "__main__":
    unittest.main()
