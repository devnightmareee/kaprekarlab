"""kaprekarlab - tools for Kaprekar numbers and the Kaprekar routine (6174)."""
from .core import (Analysis, Trajectory, analyze, from_digits, is_kaprekar,
                   kaprekar_numbers, kaprekar_step, routine, to_digits)
from .apps import (KaprekarRNG, ascii_histogram, explain, explorer_html, grade_file,
                   grade_function, histogram_svg, kaprekar_hash, known_answers, quiz,
                   to_csv, trajectory_svg, worksheet, worst_cases)

__version__ = "0.2.0"
KAPREKAR_CONSTANT = 6174
