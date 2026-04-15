# nuggets.md
# Python Nuggets — Personal Field Manual
# Sean Girgis | Dallas, TX | Senior Data Engineer / AI Architect
# Maintained by Claude Code via nugget_prompt.md

> **Simplicity and clarity is Gold.**  
> These are the things tutorials skipped. One tight insight per entry.  
> Append-only. Never delete. Date-stamped.

---

## HOW TO ADD A NUGGET

Open Claude Code and say:
> *"Read prompts\nugget_prompt.md. Append this nugget to nuggets.md. Update the TOC."*

Then describe your nugget. Claude Code handles the rest.

---

## TABLE OF CONTENTS

### Formatting
<a id="toc-formatting--format-spec--inside-"></a>
- [Formatting — Format Spec `:` inside `{}`](#formatting--format-spec--inside-)

### Collections
*(none yet)*

### Itertools & Functools
*(none yet)*

### Comprehensions
*(none yet)*

### Decorators & Closures
*(none yet)*

### OOP
*(none yet)*

### Exceptions
*(none yet)*

### File & IO
*(none yet)*

### DSA Patterns
<a id="toc-dsa-patterns--to_signed_32--systematic-32-bit-sanitizer"></a>
- [DSA Patterns — to\_signed\_32 — Systematic 32-bit Sanitizer](#dsa-patterns--to_signed_32--systematic-32-bit-sanitizer)
<a id="toc-dsa-patterns--to_signed_32--the-full-story-mask-max-and-the-three-zones"></a>
- [DSA Patterns — to\_signed\_32 — The Full Story, MASK MAX and the Three Zones](#dsa-patterns--to_signed_32--the-full-story-mask-max-and-the-three-zones)
<a id="toc-dsa-patterns--bit-extract-and-insert--read-and-write-a-single-bit-at-position-i"></a>
- [DSA Patterns — Bit Extract and Insert — Read and Write a Single Bit at Position i](#dsa-patterns--bit-extract-and-insert--read-and-write-a-single-bit-at-position-i)
<a id="toc-dsa-patterns--python-list-internals--the-dynamic-array-under-the-hood"></a>
- [DSA Patterns — Python List Internals — The Dynamic Array Under the Hood](#dsa-patterns--python-list-internals--the-dynamic-array-under-the-hood)

> 📓 **Topics with full master guides — nuggets to be added later:**
> - Lists & Arrays → `lists_arrays_master_guide.ipynb` (5 patterns)
> - Multidimensional Tensors → `multidimensional_tensors_master_guide.ipynb` (5 patterns)
> - Reverse Bits conveyor belt pattern → pending
> - AND vs XOR for masking → pending
> - 32-bit loop always 32 iterations — why not early exit → pending

### Debugging & Tracing
*(none yet)*

### Miscellaneous
<a id="toc-miscellaneous--0x80000000--most-negative-32-bit-integer"></a>
- [Miscellaneous — 0x80000000 — Most Negative 32-bit Integer](#miscellaneous--0x80000000--most-negative-32-bit-integer)

---
---

<!-- ============================================================ -->
<!--                        NUGGETS START                         -->
<!-- ============================================================ -->

---

## Formatting — Format Spec `:` inside `{}`
**Date added:** 2026-03-20  
**Tags:** `f-string` `formatting` `print` `alignment`

### The Story
Inside an f-string `{}`, the colon `:` is the divider between *what to show* and *how to show it*.
Everything after the colon is display-only — it never changes the value, just the visual.
This is Python's mini format spec language, available anywhere you use `format()` or f-strings.

### Syntax / Pattern
```python
# ── PATTERN ──────────────────────────────────────────
{value : [fill][align][width][.precision][type]}
#         ^     ^      ^      ^            ^
#         pad   < > ^  min    decimal      d f s %
#         char  align chars  places        type
```

### Quick Examples
```python
# ── EXAMPLES — run this cell, read the output ────────
n = 42

print(f"{n:>3}")        # '  42'   right-align, width 3
print(f"{n:<5}|")       # '42   |' left-align, width 5
print(f"{n:^5}|")       # ' 42  |' centered, width 5
print(f"{n:0>5}")       # '00042'  zero-pad, right-align, width 5
print(f"{3.14159:.2f}") # '3.14'   2 decimal places
print(f"{0.75:.0%}")    # '75%'    as percent, no decimals

# Simplicity and clarity is Gold
```

### LC / Real-World Hook
Critical in debug print traces inside loops — `{i:>3} {val:>6}` lines up output so
you can visually scan stack/queue state during monotonic stack problems.

[↑ Back to TOC](#toc-formatting--format-spec--inside-)

---

## Miscellaneous — 0x80000000 — Most Negative 32-bit Integer
**Date added:** 2026-03-20
**Tags:** `hex` `integers` `binary` `32-bit` `signed` `unsigned` `DSA`

### The Story
`0x80000000` is a hex literal. Python reads it as a plain positive integer `2147483648`.
In C and Java's 32-bit signed world, that same bit pattern flips sign and means `-2147483648` — the most negative int possible.
Python has no fixed bit width, so it always shows the unsigned face — no overflow, no wrap, no surprises.

### Syntax / Pattern
```python
# ── PATTERN ──────────────────────────────────────────
# hex literal — Python sees a positive integer, always
0x80000000          # evaluates to 2147483648 (not negative in Python)

# the Python way to express the 32-bit signed floor
-(2**31)            # -2147483648

# they are the same magnitude — one is positive, one is negative
0x80000000 == 2**31 # True
```

### Quick Examples
```python
# ── EXAMPLES — run this cell, read the output ────────

print(f"0x80000000      = {0x80000000}")            # 2147483648
print(f"Most negative   = {-(2**31)}")              # -2147483648
print(f"Same magnitude? = {0x80000000 == 2**31}")   # True
print(f"Hex back        = {hex(0x80000000)}")       # 0x80000000

# Python's big-integer math — no C overflow, ever
print(f"0x80000000 + 1  = {0x80000000 + 1}")       # 2147483649 (not wrap-around)

# Simplicity and clarity is Gold
```

### LC / Real-World Hook
LC 190 Reverse Bits and LC 231 Power of Two originate in C where `INT_MIN = -2147483648 = 0x80000000` — when you see this magic number in a problem, it is always the 32-bit signed floor.

[↑ Back to TOC](#toc-miscellaneous--0x80000000--most-negative-32-bit-integer)

---

## DSA Patterns — to\_signed\_32 — Systematic 32-bit Sanitizer
**Date added:** 2026-03-20
**Tags:** `bit-manipulation` `MASK` `MAX` `signed` `unsigned` `32-bit` `LC`

### The Story
Python integers grow without limit — bit operations can return huge positive numbers that C would show as negative.
`MASK` is the box: 32 ones that chop any result down to 32 bits.
`MAX` is the halfway line: above it means you are in negative territory and need exactly one correction.
Run every bit result through `to_signed_32` and you never have to inspect values by hand again.

### Syntax / Pattern

```python
# ── PATTERN ──────────────────────────────────────────
MASK = 0xFFFFFFFF   # the box — 32 ones — chops to 32 bits
MAX  = 0x7FFFFFFF   # the halfway line — largest positive 32-bit int

def to_signed_32(n):
    n = n & MASK              # step 1 — fit in box
    if n > MAX:               # step 2 — in negative half?
        n -= 0x100000000      # step 3 — convert to real negative
    return n
```

### Quick Examples

```python
# ── EXAMPLES — run this cell, read the output ────────
MASK = 0xFFFFFFFF
MAX  = 0x7FFFFFFF

def to_signed_32(n):
    n = n & MASK
    if n > MAX:
        n -= 0x100000000
    return n

print(to_signed_32(1))             #  1            untouched — already clean
print(to_signed_32(2147483647))    #  2147483647   MAX itself — untouched
print(to_signed_32(2147483648))    # -2147483648   just crossed the line
print(to_signed_32(0xFFFFFFFF))    # -1            MASK itself = -1 signed
print(to_signed_32(~1 & MASK))     # -2            what C gives for ~1

# Simplicity and clarity is Gold
```

### LC / Real-World Hook
LC 190 Reverse Bits, LC 191 Hamming Weight, LC 338 Counting Bits — paste `to_signed_32` at the top of every bit manipulation solution where Python output must match C 32-bit signed behavior.

[↑ Back to TOC](#toc-dsa-patterns--to_signed_32--systematic-32-bit-sanitizer)

---

## DSA Patterns — to\_signed\_32 — The Full Story, MASK MAX and the Three Zones
**Date added:** 2026-03-20
**Tags:** `bit-manipulation` `MASK` `MAX` `signed` `unsigned` `32-bit` `to_signed_32` `LC`

### The Story
Python has no 32-bit box — bit operations return whatever size they want.
`MASK` is the cookie cutter: AND any result with it and you get exactly 32 bits, nothing more.
`MAX` is the halfway line inside that box. The box has three zones — zero, positive, and negative-in-disguise.
Above `MAX` means you are in negative territory wearing a big positive number as a costume.
One subtraction of `0x100000000` (one full box width) slides it onto the real signed number line.
The function is invisible when the number is already clean. It self-sanitizes. No visual inspection needed. Ever.

### Syntax / Pattern

```python
# ── PATTERN ──────────────────────────────────────────
MASK = 0xFFFFFFFF        # the box — 32 ones — cookie cutter
MAX  = 0x7FFFFFFF        # halfway line — largest positive 32-bit int

# three zones inside the 32-bit box:
# zone 1 — zero            → n == 0         → do nothing
# zone 2 — [1 … MAX]       → positive       → do nothing
# zone 3 — [MAX+1 … MASK]  → negative in disguise → subtract 0x100000000

def to_signed_32(n):
    n &= MASK             # step 1 — AND chops all bits above bit 31 to zero
    if n > MAX:           # step 2 — are we in zone 3?
        n -= 0x100000000  # step 3 — slide left onto the signed number line
    return n
```

### Quick Examples

```python
# ── EXAMPLES — run this cell, read the output ────────
MASK = 0xFFFFFFFF
MAX  = 0x7FFFFFFF

def to_signed_32(n):
    n &= MASK
    if n > MAX:
        n -= 0x100000000
    return n

num1 = 1            # zone 2 — positive
num2 = 0x7FFFFFFF   # zone 2 — MAX itself
num3 = 0x80000000   # zone 3 — most negative (just crossed the line)
num4 = 0            # zone 1 — zero
num5 = 0xFFFFFFFF   # zone 3 — MASK itself = -1 signed

print(to_signed_32(num1))  #  1            untouched
print(to_signed_32(num2))  #  2147483647   MAX — untouched
print(to_signed_32(num3))  # -2147483648   most negative — just crossed the line
print(to_signed_32(num4))  #  0            zero — untouched
print(to_signed_32(num5))  # -1            MASK itself = -1 signed

# Simplicity and clarity is Gold
```

### LC / Real-World Hook
Paste `MASK`, `MAX`, and `to_signed_32` at the top of every bit manipulation solution — LC 190 Reverse Bits, LC 191 Hamming Weight, LC 201 Bitwise AND of Numbers Range. In Citi telemetry, the same pattern applies when raw 32-bit sensor registers arrive unsigned but must be interpreted as signed deltas.

[↑ Back to TOC](#toc-dsa-patterns--to_signed_32--the-full-story-mask-max-and-the-three-zones)

---

## DSA Patterns — Bit Extract and Insert — Read and Write a Single Bit at Position i
**Date added:** 2026-03-21
**Tags:** `bit-manipulation` `extract` `insert` `shift` `OR` `AND` `position` `LC`

### The Story
Two primitives underlie every bit operation you will ever write.
**Extract** means read what is sitting at position `i` — is it a 0 or a 1?
**Insert** means place a specific value (0 or 1) at position `i` without disturbing anything else.
Extract uses shift-then-AND. Insert uses shift-then-OR to force a 1, and shift-then-AND-NOT to force a 0.
Every other bit operation is just these two chained together.

### Syntax / Pattern

```python
# ── PATTERN ──────────────────────────────────────────

# ── EXTRACT — read the bit at position i ─────────────
bit = (n >> i) & 1
# shift right by i so the target bit lands at position 0
# AND with 1 masks every other bit away
# result is exactly 0 or 1 — nothing else

# ── INSERT 1 — force a 1 at position i ───────────────
n = n | (1 << i)
# 1 << i builds a mask with only position i ON
# OR turns that bit ON — every other bit untouched

# ── INSERT 0 — force a 0 at position i ───────────────
n = n & ~(1 << i)
# 1 << i builds the mask
# ~ flips it — position i is now the only 0
# AND forces that bit OFF — every other bit untouched
```

### Quick Examples

```python
# ── EXAMPLES — run this cell, read the output ────────
n = 0b10110101              # starting number

# extract bit at position 2 — expect 1
bit = (n >> 2) & 1
print(f"bit at pos 2        = {bit}")               # 1

# extract bit at position 3 — expect 0
bit = (n >> 3) & 1
print(f"bit at pos 3        = {bit}")               # 0

# insert 1 at position 3 — turn that 0 into a 1
n_set = n | (1 << 3)
print(f"after set   pos 3   = {bin(n_set)}")        # 0b10111101

# insert 0 at position 2 — turn that 1 into a 0
n_clr = n & ~(1 << 2)
print(f"after clear pos 2   = {bin(n_clr)}")        # 0b10110001

# verify the clear worked — extract from modified number
print(f"bit at pos 2 after clear = {(n_clr >> 2) & 1}")  # 0

# Simplicity and clarity is Gold
```

### LC / Real-World Hook
LC 190 Reverse Bits extracts at position `i` and inserts at mirror position `31 - i`. LC 191 Hamming Weight counts every extracted 1. In Citi telemetry, sensor status registers pack multiple flags into one 32-bit integer — extract reads a flag, insert sets or clears it without touching the others.

[↑ Back to TOC](#toc-dsa-patterns--bit-extract-and-insert--read-and-write-a-single-bit-at-position-i)

---

## DSA Patterns — Python List Internals — The Dynamic Array Under the Hood
**Date added:** 2026-03-21
**Tags:** `list` `array` `dynamic-array` `slice` `copy` `2D` `initialization` `gotcha`

### The Story
A Python list is a dynamic array living in contiguous memory.
It doubles in capacity when full — that is why `append` is O(1) amortized but `insert(0, x)` is O(n): every element shifts right to make room.
Slicing makes a new list. Assignment makes an alias — same object, same memory.
The 2D initialization trap has burned everyone at least once: `[[0]*3]*3` looks like three rows but is actually one row referenced three times.

### Syntax / Pattern

```python
# ── PATTERN ──────────────────────────────────────────

# ── CORE OPERATIONS ──────────────────────────────────
a = [1, 2, 3]
a.append(4)          # O(1) amortized — fast
a.insert(0, 99)      # O(n) — shifts every element right — slow
a.pop()              # O(1) — remove last
a.pop(0)             # O(n) — shifts every element left — slow

# ── COPY TRAP ────────────────────────────────────────
b = a                # NOT a copy — b and a point to the same object
c = a[:]             # real shallow copy — new list, same element values
d = a.copy()         # identical to a[:]
e = a[1:3]           # slice — new list containing indices 1 and 2 only

# ── 2D INITIALIZATION TRAP ───────────────────────────
bad  = [[0] * 3] * 3                    # 3 aliases to the SAME row — trap
good = [[0] * 3 for _ in range(3)]      # 3 independent rows — correct
```

### Quick Examples

```python
# ── EXAMPLES — run this cell, read the output ────────

# ── COPY TRAP PROOF ──────────────────────────────────
a = [1, 2, 3]
b = a          # alias
c = a[:]       # real copy
b[0] = 99
print(f"a after b[0]=99 : {a}")    # [99, 2, 3]  — a changed too
print(f"c after b[0]=99 : {c}")    # [1, 2, 3]   — c untouched

# ── 2D TRAP PROOF ────────────────────────────────────
bad  = [[0] * 3] * 3
good = [[0] * 3 for _ in range(3)]
bad[0][0]  = 99
good[0][0] = 99
print(f"bad  after [0][0]=99 : {bad}")   # [[99,0,0],[99,0,0],[99,0,0]] — all rows changed
print(f"good after [0][0]=99 : {good}")  # [[99,0,0],[0,0,0],[0,0,0]]   — only row 0 changed

# ── NEGATIVE INDEXING ────────────────────────────────
nums = [10, 20, 30, 40, 50]
print(f"last        : {nums[-1]}")     # 50
print(f"second last : {nums[-2]}")     # 40
print(f"reverse     : {nums[::-1]}")   # [50, 40, 30, 20, 10]

# Simplicity and clarity is Gold
```

### LC / Real-World Hook
LC 48 Rotate Matrix, LC 54 Spiral Matrix, LC 74 Search 2D Matrix all require correct 2D initialization — the aliased-row trap produces bugs that look like logic errors but are memory errors. In Citi telemetry, 2D grids model time-series across endpoints; same initialization rules apply.

[↑ Back to TOC](#toc-dsa-patterns--python-list-internals--the-dynamic-array-under-the-hood)

---
