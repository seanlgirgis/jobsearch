# Capital One — CodeSignal GCA Prep
**Role:** Lead Data Engineer  
**Format:** General Coding Assessment (GCA) — 70 minutes, 4 questions  
**Language:** Python 3  
**Source:** Sam Ali (Principal Recruiter, Card Tech)

---

## Assessment Structure

| Question | Difficulty | Target Time | Focus |
|----------|-----------|-------------|-------|
| Q1 | Easy | < 7 min | String manipulation / basic logic |
| Q2 | Easy-Medium | < 8 min | Arrays, conditionals, instruction-following |
| Q3 | Medium | ~20 min | HashMaps, 2D arrays, sliding window |
| Q4 | Hard | ~25 min | Graph, DP, or complex matrix traversal |
| Buffer | — | ~10 min | Review, edge cases, partial credit |

---

## Strategy

### Time Management
- Q1 + Q2 done in under 15 minutes — non-negotiable
- If Q3 blocks you for 10+ minutes → skip to Q4, come back
- Always attempt every question — partial test passes count
- Submit early and often against visible test cases

### Scoring Mindset
- GCA is automated: test case passes = score
- No style grading — use short variable names, no docstrings
- Brute force that passes all tests beats elegant code that doesn't

### Edge Cases to Always Check
- Empty input (`[]`, `""`, `0`)
- Single element
- Negative numbers
- Duplicates
- Off-by-one on indices

---

## Key Topics & Patterns

### 1. String Manipulation
```python
s.split(), s.strip(), s.lower(), s.replace()
''.join(list)
s[::-1]  # reverse
ord(c) - ord('a')  # char to index
collections.Counter(s)  # frequency map
```

### 2. Arrays & Two Pointers
```python
# Two pointer
l, r = 0, len(arr) - 1
while l < r:
    ...

# Sliding window
window = collections.deque()
for i, val in enumerate(arr):
    window.append(val)
    if len(window) > k:
        window.popleft()
```

### 3. HashMaps (Most Important Optimization Tool)
```python
from collections import defaultdict, Counter

freq = defaultdict(int)
for x in arr:
    freq[x] += 1

# Two-sum pattern
seen = {}
for i, n in enumerate(arr):
    complement = target - n
    if complement in seen:
        return [seen[complement], i]
    seen[n] = i
```

### 4. 2D Arrays / Matrix Traversal
```python
rows, cols = len(grid), len(grid[0])

# Iterate all cells
for r in range(rows):
    for c in range(cols):
        val = grid[r][c]

# 4-directional neighbors (with bounds check)
directions = [(0,1),(0,-1),(1,0),(-1,0)]
for dr, dc in directions:
    nr, nc = r + dr, c + dc
    if 0 <= nr < rows and 0 <= nc < cols:
        # process grid[nr][nc]

# BFS from a cell
from collections import deque
queue = deque([(start_r, start_c)])
visited = set()
visited.add((start_r, start_c))
while queue:
    r, c = queue.popleft()
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
            visited.add((nr, nc))
            queue.append((nr, nc))
```

### 5. Sorting Tricks
```python
arr.sort()                          # in-place
sorted(arr, key=lambda x: -x)      # descending
sorted(arr, key=lambda x: (x[1], x[0]))  # multi-key
```

### 6. Stack / Queue
```python
stack = []
stack.append(x)
stack.pop()

from collections import deque
q = deque()
q.append(x)
q.popleft()
```

### 7. Binary Search
```python
import bisect
bisect.bisect_left(arr, target)   # leftmost index
bisect.bisect_right(arr, target)  # rightmost index

# Manual
lo, hi = 0, len(arr) - 1
while lo <= hi:
    mid = (lo + hi) // 2
    if arr[mid] == target: return mid
    elif arr[mid] < target: lo = mid + 1
    else: hi = mid - 1
```

### 8. Dynamic Programming (Basic)
```python
# 1D DP
dp = [0] * (n + 1)
dp[0] = base_case
for i in range(1, n + 1):
    dp[i] = dp[i-1] + ...

# 2D DP
dp = [[0] * cols for _ in range(rows)]
```

---

## Most Likely Q3/Q4 Patterns at Capital One GCA

Based on Capital One's known GCA flavor:

1. **Island counting / flood fill** — BFS/DFS on matrix
2. **Subarray problems** — sliding window or prefix sums
3. **String encoding/decoding** — stack-based
4. **Interval merging** — sort + greedy
5. **Top-K elements** — heap (`heapq`)

```python
import heapq
# Min-heap
heap = []
heapq.heappush(heap, val)
heapq.heappop(heap)

# Top K largest
heapq.nlargest(k, arr)
```

---

## Quick Python Gotchas

```python
# Integer division
5 // 2  # = 2

# Max/min int
float('inf'), float('-inf')

# Enumerate
for i, val in enumerate(arr):

# Zip
for a, b in zip(arr1, arr2):

# List comprehension
[x**2 for x in range(10) if x % 2 == 0]

# Dict comprehension
{k: v for k, v in pairs}
```

---

## Day-Of Checklist

- [ ] Chrome or Firefox (latest stable)
- [ ] Quiet room, phone off
- [ ] CodeSignal sample test done beforehand
- [ ] Python 3 selected as language
- [ ] Scratch paper for diagrams
- [ ] Read problem statement twice before coding
- [ ] Submit against visible test cases early

---

## Practice Drill Plan (Before Test)

### Priority Order
1. Two Sum / HashMap problems (30 min)
2. Matrix BFS / island counting (45 min)
3. Sliding window / subarray sum (30 min)
4. Interval merging (20 min)
5. Full timed mock — 4 problems in 70 min

### LeetCode Problems to Hit
| # | Problem | Pattern |
|---|---------|---------|
| 1 | Two Sum | HashMap |
| 200 | Number of Islands | BFS/DFS matrix |
| 53 | Maximum Subarray | Sliding window / Kadane |
| 56 | Merge Intervals | Sort + greedy |
| 347 | Top K Frequent | Heap |
| 242 | Valid Anagram | Counter |
| 283 | Move Zeroes | Two pointer |
| 73 | Set Matrix Zeroes | Matrix |

---

## Contact
Sam Ali — 551-237-6369  
CodeSignal support: support@codesignal.com
