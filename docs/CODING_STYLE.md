# jobsearch/CodingStyle.md   (proposed location – or add to Specs/00000.CodingConventions.md)

## Python Coding Style – Current Standards (2026)

We follow **modern, strict, professional Python** practices. Goal: readable, type-safe, maintainable code that scales to a real tool.

### Core Principles
1. PEP 8 + modern extensions (black + isort + ruff)
2. Strict static typing (PEP 484, 563, 649, 695)
3. Explicit > implicit
4. Small functions, single responsibility
5. Defensive programming + clear error messages

### Formatting & Linting
- **Formatter**: black (line length 100 or 88 – decide later, default 100 for now)
- **Import sorter**: isort (profile black)
- **Linter**: ruff (replaces flake8, pylint, etc.)
  - Enable strict mode + typing rules
  - Enforce: no unused imports/vars, type annotations, docstrings
- **Pre-commit hooks** recommended (black, isort, ruff, mypy)

### Typing
- Use **strict typing everywhere** possible
- Annotations on **all function parameters and return types**
- Prefer **TypeAlias** (PEP 695) and modern generics
- Use **typing.Self** when appropriate (Python 3.11+)
- **No** implicit Any – use `Any` only when truly dynamic and unavoidable
- Prefer **TypedDict**, **dataclasses**, **NamedTuple**, **pydantic.BaseModel** over plain dicts/lists when structure is known
- Use **Literal**, **Annotated**, **TypeGuard** where they add clarity

Examples:

```python
from __future__ import annotations  # if needed for older Python

from dataclasses import dataclass
from typing import Literal, Self, TypeAlias

RoleName: TypeAlias = Literal["Senior Data Engineer", "Performance Engineer"]

@dataclass(frozen=True)
class ExperienceEntry:
    company: str
    role: RoleName
    start: str          # ISO-like or "Present"
    end: str | None
    highlights: list[str]

class MasterProfileLoader:
    def get_recent_experience(self, n: int = 3) -> list[ExperienceEntry]:
        ...
    
    def get_top_skills(self, n: int = 15, /, *, min_years: float = 2.0) -> list[dict[str, Any]]:
        ...