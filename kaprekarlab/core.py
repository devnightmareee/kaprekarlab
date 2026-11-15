"""Core Kaprekar mathematics: Kaprekar numbers and the Kaprekar routine, in any base."""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from typing import List, Tuple


def to_digits(n: int, base: int = 10, width: int = 0) -> List[int]:
    """Digits of n (most significant first), left-padded with zeros to `width`."""
    if n < 0:
        raise ValueError("n must be >= 0")
    ds: List[int] = []
    while n:
        n, r = divmod(n, base)
        ds.append(r)
    ds += [0] * (width - len(ds))
    return ds[::-1] or [0]


def from_digits(ds, base: int = 10) -> int:
    n = 0
    for d in ds:
        n = n * base + d
    return n


def is_kaprekar(n: int, base: int = 10) -> bool:
    """True if n**2 can be split into two parts (right part > 0) whose sum is n."""
    if n < 1:
        return False
    if n == 1:
        return True
    sq = to_digits(n * n, base)
    for i in range(1, len(sq)):
        right = from_digits(sq[i:], base)
        if right and from_digits(sq[:i], base) + right == n:
            return True
    return False


def kaprekar_numbers(limit: int, base: int = 10) -> List[int]:
    """All Kaprekar numbers in [1, limit]."""
    m = base - 1  # n^2 - n = a*(base^k - 1) is always divisible by base-1: cheap pre-filter
    return [n for n in range(1, limit + 1) if n * (n - 1) % m == 0 and is_kaprekar(n, base)]


def kaprekar_step(n: int, digits: int = 4, base: int = 10) -> int:
    """One step of the Kaprekar routine: (digits sorted descending) - (ascending)."""
    ds = to_digits(n, base, digits)
    if len(ds) > digits:
        raise ValueError(f"{n} has more than {digits} digits")
    ds.sort()
    return from_digits(ds[::-1], base) - from_digits(ds, base)


@dataclass(frozen=True)
class Trajectory:
    start: int
    path: Tuple[int, ...]       # every distinct value visited, in order
    cycle_start: int            # index in `path` where the cycle begins
    cycle: Tuple[int, ...]
    digits: int
    base: int

    @property
    def steps(self) -> int:
        """Steps needed to first reach the attractor (fixed point or cycle)."""
        return self.cycle_start

    @property
    def kind(self) -> str:
        if self.cycle == (0,):
            return "zero"
        return "fixed" if len(self.cycle) == 1 else "cycle"

    @property
    def attractor(self) -> Tuple[int, ...]:
        """The cycle, rotated so it starts at its smallest element."""
        i = self.cycle.index(min(self.cycle))
        return self.cycle[i:] + self.cycle[:i]


def routine(n: int, digits: int = 4, base: int = 10) -> Trajectory:
    """Run the Kaprekar routine from n until a value repeats."""
    seen, path, x = {}, [], n
    while x not in seen:
        seen[x] = len(path)
        path.append(x)
        x = kaprekar_step(x, digits, base)
    cs = seen[x]
    return Trajectory(n, tuple(path), cs, tuple(path[cs:]), digits, base)


@dataclass(frozen=True)
class Analysis:
    digits: int
    base: int
    attractors: Counter   # attractor -> how many starting numbers reach it
    steps: Counter        # steps -> how many starting numbers need that many

    @property
    def constants(self) -> List[int]:
        """Non-zero fixed points, i.e. Kaprekar constants (6174 for 4 digits)."""
        return sorted(a[0] for a in self.attractors if len(a) == 1 and a[0] != 0)

    @property
    def max_steps(self) -> int:
        return max(self.steps)


@lru_cache(maxsize=None)
def analyze(digits: int = 4, base: int = 10) -> Analysis:
    """Run the routine from every number with `digits` digits (leading zeros allowed)."""
    attractors, steps = Counter(), Counter()
    for n in range(base ** digits):
        t = routine(n, digits, base)
        attractors[t.attractor] += 1
        steps[t.steps] += 1
    return Analysis(digits, base, attractors, steps)
