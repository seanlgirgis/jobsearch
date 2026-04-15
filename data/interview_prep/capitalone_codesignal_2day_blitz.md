# Capital One CodeSignal — 2-Day Blitz Plan
**Goal:** Walk into the 70-minute GCA and score in the top tier  
**Your baseline:** Day-88 — 100+ problems done. This is NOT a beginner grind. This is precision sharpening.  
**Method:** Sean Style — concept clarity first, then speed, then simulation  

---

## What The Assessment Needs From You

| Q | Difficulty | What They're Testing | Your Target Time |
|---|-----------|---------------------|-----------------|
| Q1 | Easy | Read carefully, execute cleanly | < 7 min |
| Q2 | Easy-Med | Arrays / strings / HashMap | < 8 min |
| Q3 | Medium | Pattern recognition + clean impl | ~20 min |
| Q4 | Hard | Compose 2 patterns under pressure | ~25 min |
| — | — | Buffer + review | ~10 min |

---

## Your Actual Gaps (Based on What's In Your Folder)

You are strong on: Graphs, DP, Heaps, Intervals, Trees, Binary Search, Sliding Window  

**The holes I see:**
1. **Monotonic Stack** — LC42, LC84, LC85, LC907, LC1475 are ALL empty files. This pattern is a classic Q4 at Capital One.
2. **Speed under pressure** — you understand the concepts; CodeSignal tests whether you can execute in 7 minutes, not 20.
3. **CodeSignal simulation problems** — instruction-following with edge cases disguised as "simple" problems.

**This plan closes those 3 gaps. Nothing else.**

---

## Day 1 — The Stables: Concept Mastery + Monotonic Stack

### Morning Block (2–3 hrs) — The Stables Refresher

The goal here is NOT to learn these. You know them. The goal is to be able to reach for them instantly without thinking — like muscle memory.

#### Stable 1: Stack
**The mental model:** Last In, First Out. A stack is useful when you need to "remember the past" to answer a question about the current element.

```python
stack = []
stack.append(x)     # push
top = stack[-1]     # peek without pop
val = stack.pop()   # pop
```

**CodeSignal trigger:** "next greater element", "valid parentheses", "evaluate expression", "balanced brackets"

**Your anchor problems (already done — just re-read your solution):**
- LC20 Valid Parentheses
- LC155 Min Stack
- LC150 Evaluate Reverse Polish Notation

---

#### Stable 2: Deque (Double-Ended Queue)
**The mental model:** A deque is a sliding window's memory. It remembers the BEST candidates from the past window without re-scanning.

```python
from collections import deque
dq = deque()
dq.append(x)        # add to right
dq.appendleft(x)    # add to left
dq.pop()            # remove from right
dq.popleft()        # remove from left (O(1) — this is why deque beats list)
dq[0]               # peek left
dq[-1]              # peek right
```

**When to use deque over stack:** When your window slides AND you need to prune from BOTH ends.

**Sean's Deque Pattern (Sliding Window Maximum):**
```python
# Maintain a deque of INDICES, values in DECREASING order
# Front of deque = index of max in current window
dq = deque()
result = []
for i, val in enumerate(nums):
    # Remove elements outside window
    while dq and dq[0] < i - k + 1:
        dq.popleft()
    # Remove smaller elements from back (they can never be max)
    while dq and nums[dq[-1]] < val:
        dq.pop()
    dq.append(i)
    if i >= k - 1:
        result.append(nums[dq[0]])
```

**Your anchor:** LC239 Sliding Window Maximum (already done — review it now)

---

#### Stable 3: Monotonic Stack (YOUR MAIN GAP — spend the most time here)

**The mental model:** A stack where you enforce ORDER. You push, but before pushing you pop everything that violates the order. What gets popped = found its answer. What stays = still waiting.

**Two flavors:**
- **Monotonic Decreasing:** Pop when current > top → use for "next greater element"
- **Monotonic Increasing:** Pop when current < top → use for "next smaller element"

**The Template (Monotonic Decreasing):**
```python
stack = []  # stores indices
result = [0] * len(nums)

for i, val in enumerate(nums):
    # While stack has something AND current breaks the monotonic order
    while stack and nums[stack[-1]] < val:
        idx = stack.pop()
        result[idx] = val  # current val is the "next greater" for idx
    stack.append(i)

# Anything left in stack never found an answer
while stack:
    result[stack.pop()] = -1  # or 0, depending on problem
```

**Problem → Pattern:**
| Problem | What you maintain | What pop means |
|---------|-----------------|----------------|
| LC739 Daily Temperatures | Decreasing temps | "today is warmer than day at idx" |
| LC496 Next Greater Element | Decreasing values | "this is your next greater" |
| LC84 Largest Rectangle | Increasing heights | "left boundary found" |
| LC42 Trapping Rain Water | Decreasing heights | "water can be trapped here" |
| LC853 Car Fleet | Decreasing times | "this car catches the fleet ahead" |

**Now implement these (they are empty in your folder):**

**Priority 1 — LC739 Daily Temperatures (if not fully solid):**
```python
def dailyTemperatures(temps):
    stack = []  # indices of days waiting for a warmer day
    result = [0] * len(temps)
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            idx = stack.pop()
            result[idx] = i - idx
        stack.append(i)
    return result
```

**Priority 2 — LC42 Trapping Rain Water (fill the empty file):**
```python
def trap(height):
    stack = []
    water = 0
    for i, h in enumerate(height):
        while stack and height[stack[-1]] < h:
            bottom = stack.pop()
            if not stack:
                break
            left = stack[-1]
            width = i - left - 1
            bounded_height = min(height[left], h) - height[bottom]
            water += width * bounded_height
        stack.append(i)
    return water
```

**Priority 3 — LC84 Largest Rectangle in Histogram (fill the empty file):**
```python
def largestRectangleArea(heights):
    stack = []  # monotonic increasing — indices
    max_area = 0
    heights = heights + [0]  # sentinel to flush stack at end
    for i, h in enumerate(heights):
        start = i
        while stack and heights[stack[-1]] > h:
            idx = stack.pop()
            width = i - (stack[-1] + 1 if stack else 0)
            max_area = max(max_area, heights[idx] * width)
            start = idx
        stack.append(start)
        # trick: use start not i — extends rectangle left
    return max_area
```

---

#### Stable 4: HashMap / Buckets / Frequency Map
**The mental model:** Trade space for time. If you're doing O(n²) lookups, a HashMap makes it O(n).

```python
from collections import defaultdict, Counter

# Frequency map
freq = Counter(arr)              # Counter({'a': 3, 'b': 2})
freq = defaultdict(int)          # manual frequency
for x in arr: freq[x] += 1

# Two-sum pattern (seen before?)
seen = {}
for i, n in enumerate(arr):
    comp = target - n
    if comp in seen:
        return [seen[comp], i]
    seen[n] = i

# Group by key
groups = defaultdict(list)
for val in arr:
    groups[key(val)].append(val)

# Bucket sort pattern (when range is bounded)
buckets = [[] for _ in range(max_val + 1)]
for x in arr:
    buckets[x].append(x)
result = [x for b in buckets for x in b]
```

**Your anchor problems:** LC1 Two Sum, LC49 Group Anagrams, LC347 Top K Frequent

---

#### Stable 5: Prefix Sum
**The mental model:** Pre-compute running totals. Any subarray sum becomes O(1).

```python
prefix = [0] * (len(arr) + 1)
for i, v in enumerate(arr):
    prefix[i+1] = prefix[i] + v

# Sum of arr[l..r] (inclusive)
subarray_sum = prefix[r+1] - prefix[l]

# With HashMap — subarray sum equals k
prefix_sum = 0
seen = {0: 1}   # prefix_sum -> count
count = 0
for n in nums:
    prefix_sum += n
    count += seen.get(prefix_sum - k, 0)
    seen[prefix_sum] = seen.get(prefix_sum, 0) + 1
```

**Your anchor:** LC560 Subarray Sum Equals K (you have a review for this)

---

### Afternoon Block (2 hrs) — Speed Drills on Q1/Q2 Style Problems

These are the warmup problems on the actual test. You lose 10+ minutes here when you overthink them.

**Rules for this block:**
- Set a 7-minute timer per problem
- Write the solution, don't think about elegance
- If you're not done in 7 minutes, write a brute force that works

**Problems to drill (from your existing library — just re-solve from scratch, no peeking):**

| # | Problem | Pattern | Target |
|---|---------|---------|--------|
| LC217 | Contains Duplicate | Set/HashMap | 3 min |
| LC242 | Valid Anagram | Counter | 3 min |
| LC1 | Two Sum | HashMap | 4 min |
| LC283 | Move Zeroes | Two pointer | 4 min |
| LC20 | Valid Parentheses | Stack | 5 min |
| LC121 | Best Time Buy/Sell Stock | Single pass | 5 min |
| LC125 | Valid Palindrome | Two pointer | 5 min |

**After each:** time yourself, check correctness, move on. Don't over-review.

---

### Evening Block (1 hr) — Medium Pattern Drills

Focus on the patterns that appear in Q3 most:

| # | Problem | Pattern |
|---|---------|---------|
| LC3 | Longest Substring Without Repeat | Sliding window + set |
| LC424 | Longest Repeating Char Replacement | Sliding window + freq map |
| LC56 | Merge Intervals | Sort + greedy |
| LC739 | Daily Temperatures | Monotonic stack |

**Time yourself:** aim for 15 minutes per problem. If you're over 20, stop, read your review, and try again tomorrow.

---

## Day 2 — Speed + Simulation + Mock

### Morning Block (2 hrs) — Matrix & BFS Refresh

Capital One Q4 is often a grid problem. You've done LC200, LC994 — but can you do it in 15 minutes cold?

**The BFS Grid Template (memorize this cold):**
```python
from collections import deque

def bfs_grid(grid):
    rows, cols = len(grid), len(grid[0])
    visited = set()
    dirs = [(0,1),(0,-1),(1,0),(-1,0)]

    def bfs(r, c):
        queue = deque([(r, c)])
        visited.add((r, c))
        while queue:
            cr, cc = queue.popleft()
            for dr, dc in dirs:
                nr, nc = cr + dr, cc + dc
                if (0 <= nr < rows and 0 <= nc < cols
                        and (nr, nc) not in visited
                        and grid[nr][nc] == TARGET):
                    visited.add((nr, nc))
                    queue.append((nr, nc))

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == TARGET and (r, c) not in visited:
                bfs(r, c)
                count += 1
    return count
```

**Drill (15 min each, from scratch, no peeking):**
- LC200 Number of Islands
- LC994 Rotting Oranges (multi-source BFS — slightly different)
- LC130 Surrounded Regions (you have a review — redo it)

---

### Afternoon Block (1.5 hrs) — CodeSignal-Style Simulation Problems

These are the problems that LOOK easy but burn time when you miss an edge case. The CodeSignal Drone problem you already solved is this type.

**Pattern for instruction-following problems:**
1. Read TWICE before coding
2. Trace through Example 1 by hand before writing a line
3. Write the brute force first — get it passing
4. Optimize only if time allows

**Re-solve your CodeSignal problems (from scratch, under 20 min each):**
- `cs_drone_delivery_foot_distance.py` — Drone Delivery
- `custom_codesignal_harmonious_building_patterns.py` — Harmonious Buildings

**Then add this one (Common CodeSignal simulation pattern — intervals + simulation):**

```
Problem: Given a list of tasks with start/end times, find the minimum
number of workers needed to handle all tasks simultaneously.

Input: tasks = [[1,3],[2,4],[3,6]]
Output: 2

Pattern: Sort by start, use min-heap of end times.
```

```python
import heapq
def min_workers(tasks):
    tasks.sort()
    heap = []  # end times of active workers
    max_workers = 0
    for start, end in tasks:
        # Free up workers whose tasks have ended
        while heap and heap[0] <= start:
            heapq.heappop(heap)
        heapq.heappush(heap, end)
        max_workers = max(max_workers, len(heap))
    return max_workers
```

---

### Evening Block — Full Timed Mock (70 minutes, no interruptions)

**Setup:**
- Close everything except your editor
- Set a 70-minute timer
- No peeking at solutions, no Google

**Mock Problem Set:**

**Q1 (Easy — target 7 min):**
Given a string, return True if it is a palindrome ignoring non-alphanumeric characters.
```
Input: "A man, a plan, a canal: Panama"
Output: True
```

**Q2 (Easy-Med — target 8 min):**
Given an array of integers, return indices of the two numbers that add up to a target. Each input has exactly one solution.
```
Input: nums = [2, 7, 11, 15], target = 9
Output: [0, 1]
```

**Q3 (Medium — target 20 min):**
Given a string s, find the length of the longest substring without repeating characters.
```
Input: "abcabcbb"
Output: 3
```

**Q4 (Hard — target 25 min):**
Given an m×n grid of integers where 1=land and 0=water, return the number of distinct islands. Two islands are the same if they have the same shape (same relative cell positions).
```
Input: [[1,1,0],[0,1,1],[0,0,1]]
Output: 2 (or depends on shapes — trace it)
Hint: BFS/DFS + record the path shape as a tuple
```

**After the mock:**
- Score yourself: how many test cases would pass?
- Identify what slowed you down
- Fix exactly those things — nothing else

---

## The Night Before the Test — 30-Minute Review Only

Do NOT grind problems the night before. Do this instead:

1. **Read your 5 templates out loud** (stack, deque/mono, HashMap, prefix sum, BFS grid) — 15 min
2. **Re-read the CodeSignal strategy** from `capitalone_codesignal_prep.md` — 5 min
3. **Trace through your Drone solution** one more time — 5 min
4. **Stop. Sleep.** Fatigue costs more test points than one more problem.

---

## The GCA Day Checklist

- [ ] Chrome or Firefox open, CodeSignal sample test done
- [ ] Scratch paper next to keyboard
- [ ] Phone off, door closed, 70-minute block blocked
- [ ] Python 3 selected as language
- [ ] Q1+Q2 done before minute 15 — non-negotiable
- [ ] If Q3 blocks at minute 10 → skip to Q4, come back
- [ ] Submit early against visible test cases — don't save submits

---

## Sean's Cheat Sheet (Print or Keep Open)

```python
# ---- STACK ----
stack = []
stack.append(x); stack.pop(); stack[-1]

# ---- DEQUE ----
from collections import deque
dq = deque()
dq.append(x); dq.appendleft(x); dq.pop(); dq.popleft(); dq[0]; dq[-1]

# ---- MONOTONIC DECREASING (next greater) ----
stack = []
for i, v in enumerate(arr):
    while stack and arr[stack[-1]] < v:
        idx = stack.pop()
        result[idx] = v       # v is the answer for idx
    stack.append(i)

# ---- MONOTONIC INCREASING (next smaller / histogram) ----
stack = []
for i, v in enumerate(arr + [0]):   # sentinel
    while stack and arr[stack[-1]] > v:
        idx = stack.pop()
        # compute width using stack[-1] or 0
    stack.append(i)

# ---- HASHMAP ----
from collections import defaultdict, Counter
freq = Counter(arr)
seen = {}; seen.get(key, default)

# ---- PREFIX SUM ----
pre = [0]; 
for v in arr: pre.append(pre[-1] + v)
# sum(l..r) = pre[r+1] - pre[l]

# ---- SLIDING WINDOW ----
l = 0
for r, v in enumerate(arr):
    # expand window with v
    while window_invalid:
        # shrink: remove arr[l]; l += 1
    # update answer with (r - l + 1)

# ---- BFS GRID ----
from collections import deque
dirs = [(0,1),(0,-1),(1,0),(-1,0)]
visited = set()
queue = deque([(r0, c0)]); visited.add((r0, c0))
while queue:
    r, c = queue.popleft()
    for dr, dc in dirs:
        nr, nc = r+dr, c+dc
        if 0<=nr<rows and 0<=nc<cols and (nr,nc) not in visited and CONDITION:
            visited.add((nr,nc)); queue.append((nr,nc))

# ---- HEAP ----
import heapq
heap = []
heapq.heappush(heap, val)
heapq.heappop(heap)        # min element
heapq.nlargest(k, arr)     # top k largest
# For max-heap: push -val, pop gives -min = max
```

---

## Summary

| Day | Morning | Afternoon | Evening |
|-----|---------|-----------|---------|
| Day 1 | Stables review + Monotonic Stack (fill the gaps) | Speed drill: 7 Easy problems × 7 min | Medium drill: LC3, LC424, LC56, LC739 |
| Day 2 | Matrix BFS cold re-solve | CodeSignal simulation re-solve + intervals | Full 70-min timed mock |
| Eve of test | Read 5 templates aloud | Re-read strategy doc | STOP. Sleep. |
