"""
codesignal_basics.py
Python Contest Fundamentals — Sean Style
Run this file. Read the output. These are your no-brainer tools.
Every section = one concept. Concept first. Example second. Contest hook last.
"""

# ============================================================
# SECTION 1 — BUILT-IN FUNCTIONS (The Workhorses)
# ============================================================
print("=" * 60)
print("SECTION 1 — BUILT-IN FUNCTIONS")
print("=" * 60)

# ── all() / any() ──────────────────────────────────────────
# all() → True if every element is truthy (or iterable is empty)
# any() → True if at least one element is truthy
nums = [2, 4, 6, 8]
print(all(x % 2 == 0 for x in nums))   # True — all even
print(any(x > 5 for x in nums))         # True — at least one > 5
print(all([]))                           # True — vacuously true (empty)
print(any([]))                           # False — nothing to be truthy

# Contest use: validate a whole row/column without a loop
grid_row = [1, 1, 1]
if all(cell == 1 for cell in grid_row):
    pass  # entire row is filled

# ── min() / max() with key ─────────────────────────────────
words = ["banana", "fig", "apple", "kiwi"]
print(min(words, key=len))              # "fig"   — shortest
print(max(words, key=len))              # "banana" — longest

pairs = [(1, 5), (3, 2), (2, 8)]
print(min(pairs, key=lambda x: x[1]))  # (3, 2)  — min by second element
print(max(pairs))                       # (3, 2)  — default: compare tuples lexicographically

# ── sorted() with key ──────────────────────────────────────
# sorted() returns a NEW list. .sort() modifies in place.
arr = [3, 1, 4, 1, 5, 9, 2, 6]
print(sorted(arr))                      # [1, 1, 2, 3, 4, 5, 6, 9]
print(sorted(arr, reverse=True))        # [9, 6, 5, 4, 3, 2, 1, 1]

# Sort by multiple keys: primary = first element desc, secondary = second element asc
data = [(2, 3), (1, 5), (2, 1), (1, 2)]
print(sorted(data, key=lambda x: (-x[0], x[1])))  # [(2,1),(2,3),(1,2),(1,5)]

# ── enumerate() ────────────────────────────────────────────
# gives (index, value) — always use this instead of range(len())
fruits = ["apple", "banana", "cherry"]
for i, fruit in enumerate(fruits):
    print(f"  {i}: {fruit}")
# Start from a custom index
for i, fruit in enumerate(fruits, start=1):
    print(f"  {i}: {fruit}")

# ── zip() ──────────────────────────────────────────────────
# Pairs elements from multiple iterables. Stops at shortest.
a = [1, 2, 3]
b = ["x", "y", "z"]
print(list(zip(a, b)))                  # [(1,'x'),(2,'y'),(3,'z')]

# Unzip (transpose)
pairs2 = [(1, 'x'), (2, 'y'), (3, 'z')]
nums2, letters = zip(*pairs2)
print(nums2, letters)                   # (1,2,3) ('x','y','z')

# zip with index — two lists together
for val_a, val_b in zip(a, b):
    pass  # process in parallel

# ── map() / filter() ───────────────────────────────────────
# map: apply function to each element
# filter: keep elements where function returns True
nums3 = [1, 2, 3, 4, 5]
print(list(map(lambda x: x * 2, nums3)))           # [2,4,6,8,10]
print(list(filter(lambda x: x % 2 == 0, nums3)))   # [2,4]

# Usually list comprehensions are clearer:
print([x * 2 for x in nums3])
print([x for x in nums3 if x % 2 == 0])

# ── sum() with generator ───────────────────────────────────
print(sum(x * x for x in range(5)))    # 0+1+4+9+16 = 30
print(sum(1 for x in arr if x > 3))    # count elements > 3

# ── abs(), divmod(), pow() ─────────────────────────────────
print(abs(-7))                          # 7
print(divmod(17, 5))                    # (3, 2)  → (quotient, remainder)
print(pow(2, 10))                       # 1024
print(pow(2, 10, 1000))                # 24  → (2^10) mod 1000 — fast modular exp

# ── reversed() ─────────────────────────────────────────────
print(list(reversed([1, 2, 3, 4])))    # [4, 3, 2, 1]
# Note: reversed() returns an iterator, not a list
# For a string: s[::-1] is simpler


# ============================================================
# SECTION 2 — STRING METHODS
# ============================================================
print("\n" + "=" * 60)
print("SECTION 2 — STRING METHODS")
print("=" * 60)

s = "  Hello, World!  "

# ── Clean / Transform ──────────────────────────────────────
print(s.strip())                        # "Hello, World!"
print(s.lstrip())                       # "Hello, World!  "
print(s.rstrip())                       # "  Hello, World!"
print(s.lower())                        # "  hello, world!  "
print(s.upper())                        # "  HELLO, WORLD!  "

# ── Split / Join ───────────────────────────────────────────
words2 = "one two three".split()        # ["one", "two", "three"]
words3 = "a,b,c".split(",")            # ["a", "b", "c"]
print(" | ".join(["a", "b", "c"]))     # "a | b | c"
print("".join(["h","e","l","l","o"]))  # "hello"  ← build string from list

# ── Search ─────────────────────────────────────────────────
t = "abcabc"
print(t.find("b"))                      # 1  (first occurrence, -1 if not found)
print(t.count("a"))                     # 2
print(t.startswith("ab"))              # True
print(t.endswith("bc"))                # True
print("bc" in t)                        # True  ← use 'in' for simple membership

# ── Replace ────────────────────────────────────────────────
print("hello world".replace("world", "Python"))  # "hello Python"

# ── Check Type ─────────────────────────────────────────────
print("123".isdigit())                  # True
print("abc".isalpha())                  # True
print("abc123".isalnum())               # True
print("  ".isspace())                   # True

# ── Char ↔ Integer ─────────────────────────────────────────
print(ord('a'))                         # 97
print(ord('A'))                         # 65
print(chr(97))                          # 'a'
print(ord('z') - ord('a'))             # 25  ← character index 0-25

# Contest pattern: map char to index
def char_idx(c): return ord(c) - ord('a')
def idx_char(i): return chr(i + ord('a'))

# ── Slicing ─────────────────────────────────────────────────
s2 = "abcdef"
print(s2[1:4])                          # "bcd"
print(s2[::-1])                         # "fedcba"  ← reverse
print(s2[::2])                          # "ace"  ← every other char

# ── f-strings for debug output ─────────────────────────────
x = 42
print(f"{x:>5}")                        # "   42" right-aligned width 5
print(f"{x:05}")                        # "00042" zero-padded
print(f"{3.14159:.2f}")                 # "3.14"


# ============================================================
# SECTION 3 — COLLECTIONS MODULE
# ============================================================
print("\n" + "=" * 60)
print("SECTION 3 — COLLECTIONS")
print("=" * 60)

from collections import defaultdict, Counter, deque, OrderedDict

# ── defaultdict ─────────────────────────────────────────────
# Never get a KeyError. Missing keys auto-initialize.
freq = defaultdict(int)
for ch in "hello":
    freq[ch] += 1
print(dict(freq))                       # {'h':1,'e':1,'l':2,'o':1}

graph = defaultdict(list)
graph[1].append(2)
graph[1].append(3)
print(dict(graph))                      # {1:[2,3]}

# ── Counter ─────────────────────────────────────────────────
# Frequency map in one line. Has useful methods.
c = Counter("abracadabra")
print(c)                                # Counter({'a':5,'b':2,'r':2,'c':1,'d':1})
print(c.most_common(3))                 # [('a',5),('b',2),('r',2)]
print(c['z'])                           # 0  ← missing key returns 0, not KeyError

# Counter arithmetic
c1 = Counter("aab")
c2 = Counter("abb")
print(c1 + c2)                          # Counter({'a':3,'b':3}) — add counts
print(c1 - c2)                          # Counter({'a':1}) — subtract (keeps positives only)
print(c1 & c2)                          # Counter({'a':1,'b':1}) — intersection (min)
print(c1 | c2)                          # Counter({'a':2,'b':2}) — union (max)

# Anagram check
def is_anagram(s, t): return Counter(s) == Counter(t)

# ── deque ────────────────────────────────────────────────────
# O(1) append/pop from BOTH ends. Lists are O(n) at front.
dq = deque([1, 2, 3])
dq.append(4)                            # [1,2,3,4]
dq.appendleft(0)                        # [0,1,2,3,4]
dq.pop()                                # removes 4
dq.popleft()                            # removes 0
print(list(dq))                         # [1,2,3]
print(dq[0], dq[-1])                    # 1  3  ← peek both ends

# Bounded deque (sliding window of last N items)
window = deque(maxlen=3)
for x in [1, 2, 3, 4, 5]:
    window.append(x)
    print(list(window))                 # auto-drops oldest when full

# Rotate (useful for circular problems)
dq2 = deque([1, 2, 3, 4, 5])
dq2.rotate(2)                           # [4,5,1,2,3]  ← right rotate by 2
dq2.rotate(-1)                          # left rotate by 1


# ============================================================
# SECTION 4 — COMPREHENSIONS
# ============================================================
print("\n" + "=" * 60)
print("SECTION 4 — COMPREHENSIONS")
print("=" * 60)

# ── List Comprehension ──────────────────────────────────────
squares = [x**2 for x in range(6)]                     # [0,1,4,9,16,25]
evens   = [x for x in range(10) if x % 2 == 0]        # [0,2,4,6,8]
matrix  = [[i*j for j in range(3)] for i in range(3)]  # 3x3 times table

# Flatten a 2D list
flat = [cell for row in matrix for cell in row]
print(flat)

# ── Dict Comprehension ──────────────────────────────────────
word_len  = {w: len(w) for w in ["cat", "dog", "elephant"]}
inverted  = {v: k for k, v in word_len.items()}       # flip key/value
filtered  = {k: v for k, v in word_len.items() if v > 3}

# ── Set Comprehension ───────────────────────────────────────
unique_lens = {len(w) for w in ["cat", "dog", "elephant"]}  # {3, 8}

# ── Generator Expression ────────────────────────────────────
# Like list comprehension but lazy — doesn't build the list in memory
# Use when you only need to iterate once, or feed into sum/any/all
total = sum(x**2 for x in range(1000000))   # memory efficient
first_even = next(x for x in range(100) if x % 2 == 0 and x > 10)  # 12


# ============================================================
# SECTION 5 — SORTING DEEP DIVE
# ============================================================
print("\n" + "=" * 60)
print("SECTION 5 — SORTING")
print("=" * 60)

# ── sort() vs sorted() ──────────────────────────────────────
arr2 = [3, 1, 4, 1, 5]
arr2.sort()                             # in-place, returns None
arr3 = sorted([3, 1, 4, 1, 5])         # returns NEW list, original unchanged

# ── Key Functions ───────────────────────────────────────────
# Sort strings by length, then alphabetically
words4 = ["banana", "fig", "apple", "kiwi", "date"]
print(sorted(words4, key=lambda w: (len(w), w)))

# Sort by second element of tuple
pairs3 = [(1, 3), (2, 1), (3, 2)]
print(sorted(pairs3, key=lambda x: x[1]))  # [(2,1),(3,2),(1,3)]

# Sort descending: negate the key
print(sorted(pairs3, key=lambda x: -x[1]))  # [(1,3),(3,2),(2,1)]

# Multiple keys: primary asc, secondary desc
data2 = [(1, 5), (1, 3), (2, 4), (2, 1)]
print(sorted(data2, key=lambda x: (x[0], -x[1])))  # [(1,5),(1,3),(2,4),(2,1)]

# ── operator module (faster than lambda) ────────────────────
import operator
print(sorted(pairs3, key=operator.itemgetter(1)))   # same as lambda x: x[1]
print(sorted(pairs3, key=operator.itemgetter(1, 0))) # sort by [1] then [0]

# ── Stability ───────────────────────────────────────────────
# Python sort is STABLE — equal elements keep original order
# This matters when you sort twice: second sort preserves first sort's order


# ============================================================
# SECTION 6 — ITERTOOLS (Contest Gold)
# ============================================================
print("\n" + "=" * 60)
print("SECTION 6 — ITERTOOLS")
print("=" * 60)

import itertools

# ── accumulate (prefix sum built-in!) ──────────────────────
nums4 = [1, 2, 3, 4, 5]
prefix = list(itertools.accumulate(nums4))
print(prefix)                           # [1, 3, 6, 10, 15]

# With custom operator (running max)
import operator
running_max = list(itertools.accumulate(nums4, max))
print(running_max)                      # [1, 2, 3, 4, 5]

# ── product (Cartesian product — replaces nested loops) ─────
for x, y in itertools.product([0, 1], repeat=2):
    pass  # (0,0),(0,1),(1,0),(1,1) — all 2D pairs

# All pairs from two lists
for a, b in itertools.product([1,2], [10,20]):
    print(f"  ({a},{b})", end=" ")
print()

# ── permutations / combinations ─────────────────────────────
print(list(itertools.permutations([1,2,3], 2)))  # ordered pairs
print(list(itertools.combinations([1,2,3], 2)))  # unordered pairs (no repeat)
print(list(itertools.combinations_with_replacement([1,2,3], 2)))  # with repeat

# ── chain (flatten or concatenate iterables) ────────────────
flat2 = list(itertools.chain([1,2], [3,4], [5]))  # [1,2,3,4,5]
flat3 = list(itertools.chain.from_iterable([[1,2],[3,4],[5]]))  # same

# ── groupby (group consecutive equal elements) ──────────────
data3 = [("a", 1), ("a", 2), ("b", 3), ("b", 4), ("c", 5)]
for key, group in itertools.groupby(data3, key=lambda x: x[0]):
    print(f"  {key}: {list(group)}")
# Note: groupby only groups CONSECUTIVE equal keys — sort first if needed


# ============================================================
# SECTION 7 — FUNCTOOLS
# ============================================================
print("\n" + "=" * 60)
print("SECTION 7 — FUNCTOOLS")
print("=" * 60)

import functools

# ── lru_cache / cache — THE MOST IMPORTANT ONE FOR CONTESTS ─
# Memoizes recursive calls. Converts O(2^n) DP to O(n).
# @cache is Python 3.9+ shorthand for @lru_cache(maxsize=None)

@functools.lru_cache(maxsize=None)
def fib(n):
    if n <= 1: return n
    return fib(n-1) + fib(n-2)

print(fib(50))                          # instant — without cache this is 2^50 calls

# Works with multiple parameters too
@functools.lru_cache(maxsize=None)
def dp(i, remaining):
    if remaining == 0: return True
    if i >= 5 or remaining < 0: return False
    return dp(i+1, remaining-1) or dp(i+1, remaining)

# IMPORTANT: lru_cache requires HASHABLE arguments
# Lists are not hashable — convert to tuple before passing
def solve(nums5, target):
    @functools.lru_cache(maxsize=None)
    def helper(i, remaining):
        if remaining == 0: return True
        if i == len(nums5) or remaining < 0: return False
        return helper(i+1, remaining-nums5[i]) or helper(i+1, remaining)
    return helper(0, target)

# ── reduce ──────────────────────────────────────────────────
print(functools.reduce(lambda a, b: a * b, [1,2,3,4,5]))  # 120 (factorial)
print(functools.reduce(max, [3,1,4,1,5,9]))                # 9


# ============================================================
# SECTION 8 — RECURSION CONTROL
# ============================================================
print("\n" + "=" * 60)
print("SECTION 8 — RECURSION CONTROL")
print("=" * 60)

import sys

# Python default recursion limit = 1000
print(sys.getrecursionlimit())          # 1000

# For deep recursion (graphs with 10^4+ nodes), increase it:
sys.setrecursionlimit(10**6)
# Put this at the TOP of your solution file on CodeSignal

# ── When Python recursion WILL blow up ──────────────────────
# - DFS on a graph with 10^5 nodes
# - Recursive DP without memoization on large n
# - Any recursive function with depth > 1000

# ── Convert DFS recursion to iterative (stack-based) ────────
# Recursive DFS (may hit limit):
def dfs_recursive(graph, start, visited=None):
    if visited is None: visited = set()
    visited.add(start)
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited)
    return visited

# Iterative DFS (same result, no recursion limit):
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                stack.append(neighbor)
    return visited

# ── Key Rule ────────────────────────────────────────────────
# For CodeSignal: put sys.setrecursionlimit(10**6) at top if you use recursion
# For safety: prefer iterative BFS/DFS when N > 5000


# ============================================================
# SECTION 9 — HEAPQ
# ============================================================
print("\n" + "=" * 60)
print("SECTION 9 — HEAPQ")
print("=" * 60)

import heapq

# Python heapq is a MIN-HEAP
heap = []
heapq.heappush(heap, 5)
heapq.heappush(heap, 2)
heapq.heappush(heap, 8)
heapq.heappush(heap, 1)
print(heap[0])                          # 1 — peek min without popping
print(heapq.heappop(heap))              # 1 — remove and return min
print(heap)                             # [2, 5, 8]

# heapify — convert list to heap in-place O(n)
arr4 = [5, 2, 8, 1, 9]
heapq.heapify(arr4)
print(arr4[0])                          # 1 — min is at index 0

# ── Max-Heap Trick ──────────────────────────────────────────
# heapq has no max-heap — negate values
max_heap = []
for x in [5, 2, 8, 1]:
    heapq.heappush(max_heap, -x)
print(-heapq.heappop(max_heap))         # 8 — actual max

# ── Heap with priority + value ──────────────────────────────
# Push tuples: (priority, value) — Python compares tuples element by element
task_heap = []
heapq.heappush(task_heap, (3, "low priority task"))
heapq.heappush(task_heap, (1, "urgent task"))
heapq.heappush(task_heap, (2, "medium task"))
priority, task = heapq.heappop(task_heap)
print(f"  Next: [{priority}] {task}")  # [1] urgent task

# ── nlargest / nsmallest ────────────────────────────────────
nums6 = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
print(heapq.nlargest(3, nums6))         # [9, 6, 5]
print(heapq.nsmallest(3, nums6))        # [1, 1, 2]

# With key — find 3 longest words
words5 = ["banana", "fig", "apple", "kiwi"]
print(heapq.nlargest(2, words5, key=len))  # ["banana", "apple"]


# ============================================================
# SECTION 10 — BISECT (Binary Search on Sorted List)
# ============================================================
print("\n" + "=" * 60)
print("SECTION 10 — BISECT")
print("=" * 60)

import bisect

sorted_arr = [1, 3, 5, 7, 9]

# bisect_left: index of leftmost position to insert val (keeping sorted)
print(bisect.bisect_left(sorted_arr, 5))   # 2 — exact match → leftmost
print(bisect.bisect_left(sorted_arr, 4))   # 2 — between 3 and 5

# bisect_right: index of rightmost position to insert val
print(bisect.bisect_right(sorted_arr, 5))  # 3 — after existing 5
print(bisect.bisect_right(sorted_arr, 4))  # 2 — same as left (no match)

# ── Check if element exists ─────────────────────────────────
def contains(arr, val):
    i = bisect.bisect_left(arr, val)
    return i < len(arr) and arr[i] == val

# ── Count elements less than val ────────────────────────────
def count_less_than(arr, val):
    return bisect.bisect_left(arr, val)

# ── Count elements in range [lo, hi] ────────────────────────
def count_range(arr, lo, hi):
    return bisect.bisect_right(arr, hi) - bisect.bisect_left(arr, lo)

print(count_range(sorted_arr, 3, 7))    # 3 — elements: 3,5,7

# ── insort — insert maintaining sort ────────────────────────
lst = [1, 3, 5]
bisect.insort(lst, 4)
print(lst)                              # [1, 3, 4, 5]


# ============================================================
# SECTION 11 — MATH MODULE
# ============================================================
print("\n" + "=" * 60)
print("SECTION 11 — MATH")
print("=" * 60)

import math

# ── Infinity ────────────────────────────────────────────────
print(float('inf'))                     # inf   ← use as initial max
print(float('-inf'))                    # -inf  ← use as initial min
print(math.inf)                         # same thing
print(math.inf > 10**18)               # True

# ── Floor / Ceil / Round ────────────────────────────────────
print(math.floor(3.7))                 # 3
print(math.ceil(3.2))                  # 4
print(round(3.5))                      # 4  ← banker's rounding (rounds to even)
print(round(2.5))                      # 2  ← NOT 3 — banker's rounding!

# Safe integer ceiling division without float:
def ceil_div(a, b): return (a + b - 1) // b
print(ceil_div(7, 3))                  # 3  ← same as math.ceil(7/3)

# ── sqrt / log ──────────────────────────────────────────────
print(math.sqrt(16))                   # 4.0
print(int(math.sqrt(16)))              # 4  ← integer sqrt
print(math.isqrt(16))                  # 4  ← integer sqrt (Python 3.8+, exact)
print(math.log(8, 2))                  # 3.0  ← log base 2 of 8
print(math.log10(1000))               # 3.0

# ── GCD / LCM ───────────────────────────────────────────────
print(math.gcd(12, 8))                # 4
print(math.lcm(4, 6))                 # 12  ← Python 3.9+
# Manual LCM: a * b // gcd(a, b)

# ── Factorial / Power ───────────────────────────────────────
print(math.factorial(5))              # 120
print(math.comb(5, 2))               # 10  ← C(5,2) — combinations
print(math.perm(5, 2))               # 20  ← P(5,2) — permutations


# ============================================================
# SECTION 12 — PYTHON GOTCHAS IN CONTESTS
# ============================================================
print("\n" + "=" * 60)
print("SECTION 12 — GOTCHAS")
print("=" * 60)

# ── Integer division ────────────────────────────────────────
print(7 // 2)                          # 3    ← floor division
print(7 / 2)                           # 3.5  ← float division
print(-7 // 2)                         # -4   ← floors toward negative infinity!
print(-7 % 3)                          # 2    ← Python mod is always non-negative

# ── Swap without temp ───────────────────────────────────────
x, y = 1, 2
x, y = y, x                            # x=2, y=1  — clean, Pythonic

# ── Chained comparisons ─────────────────────────────────────
n = 5
print(1 < n < 10)                      # True  — reads naturally
print(0 <= n <= 100)                   # True

# ── Walrus operator := (Python 3.8+) ────────────────────────
# Assign AND test in one expression — useful in while loops
import re
data4 = "hello world"
if m := re.search(r'\b\w{5}\b', data4):
    print(m.group())                   # "hello"

# In while loop (read lines until empty)
# while chunk := file.read(1024): process(chunk)

# ── is vs == ────────────────────────────────────────────────
a2, b2 = [1, 2, 3], [1, 2, 3]
print(a2 == b2)                        # True  — same values
print(a2 is b2)                        # False — different objects
# NEVER use 'is' to compare values. Only use for None checks:
val = None
if val is None: pass                   # correct
if val == None: pass                   # works but wrong style

# ── Mutable default argument trap ───────────────────────────
def bad_append(x, lst=[]):             # lst is shared across all calls!
    lst.append(x)
    return lst

def good_append(x, lst=None):          # correct pattern
    if lst is None: lst = []
    lst.append(x)
    return lst

# ── None in comparisons ─────────────────────────────────────
# None is falsy: if not None → True
# 0 is falsy: if not 0 → True
# Empty list [] is falsy: if not [] → True
# These are DIFFERENT. Be explicit when it matters:
result = None
if result is None: pass                # checks specifically for None
if not result: pass                    # True for None, 0, [], "", {}, set()

# ── Unpacking ───────────────────────────────────────────────
first, *rest = [1, 2, 3, 4, 5]
print(first, rest)                     # 1  [2, 3, 4, 5]

*start, last = [1, 2, 3, 4, 5]
print(start, last)                     # [1, 2, 3, 4]  5

a3, b3, *_ = [1, 2, 3, 4, 5]         # ignore the rest with _

# ── Range tricks ────────────────────────────────────────────
print(list(range(5, 0, -1)))           # [5,4,3,2,1]  ← count down
print(list(range(10, 0, -2)))          # [10,8,6,4,2] ← step -2

# ── Tuple as dict key (hashable) ────────────────────────────
visited = {}
visited[(0, 0)] = True                 # grid cell as key
visited[(1, 2)] = True

# ── Set operations ──────────────────────────────────────────
s1 = {1, 2, 3, 4}
s2 = {3, 4, 5, 6}
print(s1 | s2)                         # {1,2,3,4,5,6}  union
print(s1 & s2)                         # {3,4}          intersection
print(s1 - s2)                         # {1,2}          difference
print(s1 ^ s2)                         # {1,2,5,6}      symmetric difference
print(s1.issubset(s1 | s2))           # True

# ── Frozenset (hashable set — use as dict key or in set of sets) ─
fs = frozenset([1, 2, 3])
d = {fs: "found"}                      # works because frozenset is hashable


# ============================================================
# SECTION 13 — ITERATOR PROTOCOL
# ============================================================
print("\n" + "=" * 60)
print("SECTION 13 — ITERATORS")
print("=" * 60)

# ── iter() / next() ─────────────────────────────────────────
lst2 = [10, 20, 30]
it = iter(lst2)
print(next(it))                        # 10
print(next(it))                        # 20
print(next(it, "done"))               # 30
print(next(it, "done"))               # "done" ← default when exhausted

# ── Generator function ──────────────────────────────────────
def count_up(n):
    for i in range(n):
        yield i                        # pauses here, resumes on next()

gen = count_up(3)
print(list(gen))                       # [0, 1, 2]

# ── Generator as lazy pipeline ──────────────────────────────
def read_chunks(data5, size):
    for i in range(0, len(data5), size):
        yield data5[i:i+size]

for chunk in read_chunks("abcdefgh", 3):
    print(chunk, end=" ")              # abc def gh
print()

# ── enumerate is an iterator ─────────────────────────────────
e = enumerate(["a", "b", "c"])
print(next(e))                         # (0, 'a')
print(next(e))                         # (1, 'b')


# ============================================================
# SECTION 14 — ALIASES VS COPIES (The Trap That Kills Problems)
# ============================================================
print("\n" + "=" * 60)
print("SECTION 14 — ALIASES VS COPIES")
print("=" * 60)

import copy

original = [[1, 2], [3, 4]]

# ── Alias — same object ─────────────────────────────────────
alias = original
alias[0][0] = 99
print(original)                        # [[99,2],[3,4]] — changed!

original = [[1, 2], [3, 4]]            # reset

# ── Shallow copy — new outer list, same inner objects ───────
shallow = original[:]                  # or original.copy()
shallow[0][0] = 99
print(original)                        # [[99,2],[3,4]] — inner changed!

original = [[1, 2], [3, 4]]            # reset

# ── Deep copy — fully independent ───────────────────────────
deep = copy.deepcopy(original)
deep[0][0] = 99
print(original)                        # [[1,2],[3,4]] — untouched

# ── For contest: safe 2D grid copy ──────────────────────────
grid = [[1, 0, 1], [0, 1, 0]]
grid_copy = [row[:] for row in grid]  # shallow-copy each row = deep copy for 2D int grid
grid_copy[0][0] = 9
print(grid[0][0])                      # 1 — original untouched


# ============================================================
# SECTION 15 — QUICK REFERENCE CARD
# ============================================================
print("\n" + "=" * 60)
print("SECTION 15 — QUICK REFERENCE (Print this)")
print("=" * 60)

REFERENCE = """
BUILT-INS
  all(iterable)        → True if all truthy
  any(iterable)        → True if any truthy
  enumerate(it, start=0) → (idx, val) pairs
  zip(a, b)            → pairs, stops at shortest
  sorted(it, key=, reverse=) → new sorted list
  min/max(it, key=)    → with custom comparator
  sum(x*x for x in it) → generator sum
  abs(x)               → absolute value
  divmod(a,b)          → (quotient, remainder)
  pow(base,exp,mod)    → fast modular exponent

STRINGS
  s.split() / ''.join(lst)
  s.strip() / s.lower() / s.upper()
  s.find(sub) / s.count(sub) / sub in s
  s.startswith(p) / s.endswith(p)
  s.isdigit() / s.isalpha() / s.isalnum()
  ord(c) - ord('a')    → char → 0-25 index
  chr(i + ord('a'))    → index → char
  s[::-1]              → reverse string

COLLECTIONS
  defaultdict(int/list/set)
  Counter(iterable)    → freq map, .most_common(k)
  deque()              → append/appendleft/pop/popleft O(1)

SORTING
  sorted(data, key=lambda x: (x[0], -x[1]))
  arr.sort(key=..., reverse=True)

ITERTOOLS
  accumulate(arr)        → prefix sums
  product(a, b)          → cartesian product
  permutations(arr, r)   → ordered subsets
  combinations(arr, r)   → unordered subsets
  chain.from_iterable(lsts) → flatten

FUNCTOOLS
  @lru_cache(maxsize=None)  → memoize recursive DP
  reduce(func, iterable)    → fold

RECURSION
  import sys; sys.setrecursionlimit(10**6)
  Prefer iterative DFS for N > 5000

HEAPQ (min-heap)
  heapq.heappush(h, val)
  heapq.heappop(h)
  heapq.heapify(arr)
  heapq.nlargest(k, arr)
  Max-heap: push -val, pop and negate

BISECT
  bisect_left(arr, val)   → insert left of equals
  bisect_right(arr, val)  → insert right of equals
  insort(arr, val)        → insert maintaining sort

MATH
  float('inf') / float('-inf')
  math.isqrt(n)           → integer sqrt
  math.gcd(a, b)
  math.comb(n, k)         → n choose k
  ceil_div(a,b) = (a+b-1)//b  → no float needed

GOTCHAS
  -7 // 2 = -4   (floors toward -inf)
  -7 %  3 =  2   (always non-negative in Python)
  round(2.5) = 2  (banker's rounding!)
  [row[:] for row in grid]  → safe 2D copy
  if val is None:  vs  if not val:  → different!
"""
print(REFERENCE)
