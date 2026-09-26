"""Permission flags propagated via a ContextVar.

Responsibility: define Policy (frozen dataclass) and expose get/set helpers; parse locked-glob
strings.
Must not: perform any I/O.
Next: graph._bind() calls set_policy at the start of every node; collab.run_parallel uses
copy_context()
      so Policy propagates correctly into each worker thread.
"""

from __future__ import annotations

from contextvars import ContextVar
from dataclasses import dataclass, field
from fnmatch import fnmatch


class BudgetExceededError(RuntimeError):
    """Raised when token usage or estimated expenditure exceeds configured policy limits."""


@dataclass(frozen=True)
class Policy:
    dry_run: bool = False
    allow_write: bool = True
    allow_terminal: bool = True
    allow_pip: bool = True
    locked: tuple[str, ...] = field(default_factory=tuple)
    max_tokens: int = 1_000_000
    max_cost_usd: float = 10.0

    def is_locked(self, relative: str) -> bool:
        path = relative.replace("\\", "/").lstrip("/")
        name = path.rsplit("/", 1)[-1]
        for raw in self.locked:
            pat = raw.strip().replace("\\", "/")
            if pat and (fnmatch(path, pat) or fnmatch(name, pat)):
                return True
        return False

    def check_budget(self, total_tokens: int, estimated_cost: float) -> None:
        if self.max_tokens > 0 and total_tokens > self.max_tokens:
            raise BudgetExceededError(
                f"Token budget exceeded: {total_tokens} tokens used (limit: {self.max_tokens})"
            )
        if self.max_cost_usd > 0 and estimated_cost > self.max_cost_usd:
            raise BudgetExceededError(
                f"Spend limit exceeded: ${estimated_cost:.4f} "
                f"incurred (limit: ${self.max_cost_usd:.2f})"
            )


# None means "not yet set"; get_policy() returns a default Policy() in that case so callers
# never need to handle None explicitly.
_POLICY: ContextVar[Policy | None] = ContextVar("policy", default=None)


def get_policy() -> Policy:
    return _POLICY.get() or Policy()


def set_policy(policy: Policy) -> None:
    _POLICY.set(policy)


def policy_from_state(state: dict) -> Policy:
    locked = tuple(part.strip() for part in str(state.get("locked", "")).split(",") if part.strip())
    return Policy(
        dry_run=bool(state.get("dry_run")),
        allow_write=bool(state.get("allow_write", True)),
        allow_terminal=bool(state.get("allow_terminal", True)),
        allow_pip=bool(state.get("allow_pip", True)),
        locked=locked,
        max_tokens=int(state.get("max_tokens", 1_000_000) or 1_000_000),
        max_cost_usd=float(state.get("max_cost_usd", 10.0) or 10.0),
    )
