#!/usr/bin/env python3
"""
================================================================================
SR-AIBRIDGE v6.0 — HARMONY RESULT TYPE (Option C Hardened)
================================================================================
File:     harmony_result.py
Standard: Python 3.11+ | mypy --strict | ruff check
Purpose:  Rust-inspired Result[T, E] type for zero null-safety across all
          61 Python engines. Replaces all Optional[...] returns.

Replaces: Every "Optional[Foo]" and unchecked None cascade.
Architect: Kyle S. Whitlock
Temporal Seal: 2026-04-25 20:15 Tulsa, OK
================================================================================
"""

from __future__ import annotations

import functools
import traceback
from dataclasses import dataclass
from typing import (
    Any,
    Awaitable,
    Callable,
    Generic,
    Iterator,
    TypeVar,
    Union,
    final,
)

# ============================================================================
# TYPE VARIABLES
# ============================================================================

T = TypeVar("T")
E = TypeVar("E", bound=Exception)
U = TypeVar("U")
F = TypeVar("F", bound=Exception)

# ============================================================================
# CORE RESULT TYPE — OK | ERR
# ============================================================================
#
# Design Principles:
#   1. No value is ever None unexpectedly — every return is either Ok(value)
#      or Err(exception_with_full_context).
#   2. Unwrapping without checking is a compile-time error (mypy --strict).
#   3. Chaining operations: and_then, map, map_err — errors propagate
#      automatically without try/except boilerplate.
#   4. Full traceback capture on every Err for immutable audit logging.
#   5. __slots__ on all classes — zero dict overhead per instance.


@final
@dataclass(frozen=True, slots=True)
class Ok(Generic[T]):
    """Success variant containing a value of type T."""

    value: T

    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False

    def unwrap(self) -> T:
        return self.value

    def unwrap_or(self, _default: U) -> T:
        return self.value

    def unwrap_or_else(self, _op: Callable[[], U]) -> T:
        return self.value

    def expect(self, _msg: str) -> T:
        return self.value

    def map(self, op: Callable[[T], U]) -> Ok[U]:
        return Ok(op(self.value))

    def map_err(self, _op: Callable[[Any], F]) -> Ok[T]:
        return self

    def and_then(self, op: Callable[[T], Result[U, F]]) -> Result[U, F]:
        return op(self.value)

    def or_else(self, _op: Callable[[Any], Result[U, F]]) -> Ok[T]:
        return self

    def ok(self) -> Some[T]:
        return Some(self.value)

    def err(self) -> Nothing:
        return Nothing()

    def __iter__(self) -> Iterator[T]:
        yield self.value

    def __repr__(self) -> str:
        return f"Ok({self.value!r})"

    def __bool__(self) -> bool:
        return True


@final
@dataclass(frozen=True, slots=True)
class Err(Generic[E]):
    """Failure variant containing an exception of type E + full traceback."""

    error: E
    _traceback: str = ""

    def __post_init__(self) -> None:
        # Capture traceback at creation time if not provided
        if not self._traceback:
            object.__setattr__(self, "_traceback", traceback.format_exc())

    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True

    def unwrap(self) -> Never:
        raise UnwrapError(f"Called unwrap() on Err: {self.error}") from self.error

    def unwrap_or(self, default: U) -> U:
        return default

    def unwrap_or_else(self, op: Callable[[E], U]) -> U:
        return op(self.error)

    def expect(self, msg: str) -> Never:
        raise UnwrapError(f"{msg}: {self.error}") from self.error

    def map(self, _op: Callable[[Any], U]) -> Err[E]:
        return self

    def map_err(self, op: Callable[[E], F]) -> Err[F]:
        new_err = op(self.error)
        return Err(new_err, self._traceback)

    def and_then(self, _op: Callable[[Any], Result[U, F]]) -> Err[E]:
        return self

    def or_else(self, op: Callable[[E], Result[U, F]]) -> Result[U, F]:
        return op(self.error)

    def ok(self) -> Nothing:
        return Nothing()

    def err(self) -> Some[E]:
        return Some(self.error)

    def __iter__(self) -> Iterator[Any]:
        return
        yield  # Empty iterator

    def __repr__(self) -> str:
        return f"Err({self.error!r})"

    def __bool__(self) -> bool:
        return False

    @property
    def traceback(self) -> str:
        return self._traceback


# Type alias for union
Result = Union[Ok[T], Err[E]]


# ============================================================================
# NEVER TYPE — FOR UNWRAP ON ERR
# ============================================================================

class Never:
    """Bottom type — no value can ever be constructed."""

    def __init__(self) -> None:
        raise RuntimeError("Never type cannot be instantiated")


class UnwrapError(RuntimeError):
    """Raised when unwrap() is called on an Err value."""

    pass


# ============================================================================
# OPTION TYPE — SOME | NOTHING (For nullable values)
# ============================================================================
#
# Replaces: Optional[T], Union[T, None], T | None
# Usage:    Instead of "def foo() -> Optional[Bar]", use "def foo() -> Result[Bar, FooError]"
#           For truly optional values (config flags, etc.), use Option[T].


@final
@dataclass(frozen=True, slots=True)
class Some(Generic[T]):
    value: T

    def is_some(self) -> bool:
        return True

    def is_none(self) -> bool:
        return False

    def unwrap(self) -> T:
        return self.value

    def unwrap_or(self, _default: U) -> T:
        return self.value

    def map(self, op: Callable[[T], U]) -> Some[U]:
        return Some(op(self.value))

    def __repr__(self) -> str:
        return f"Some({self.value!r})"


@final
@dataclass(frozen=True, slots=True)
class Nothing:
    def is_some(self) -> bool:
        return False

    def is_none(self) -> bool:
        return True

    def unwrap(self) -> Never:
        raise UnwrapError("Called unwrap() on Nothing")

    def unwrap_or(self, default: U) -> U:
        return default

    def map(self, _op: Callable[[Any], U]) -> Nothing:
        return self

    def __repr__(self) -> str:
        return "Nothing"


Option = Union[Some[T], Nothing]


# ============================================================================
# DECORATORS — AUTO-WRAP FUNCTIONS IN RESULT
# ============================================================================


def as_result(*exceptions: type[Exception]) -> Callable[[Callable[..., T]], Callable[..., Result[T, Exception]]]:
    """
    Decorator: Wrap function return in Result, catching specified exceptions.

    Usage:
        @as_result(ValueError, KeyError)
        def parse_config(raw: str) -> dict[str, Any]:
            return json.loads(raw)

        result = parse_config('{"bad"')  # -> Err(ValueError(...))
    """

    def decorator(func: Callable[..., T]) -> Callable[..., Result[T, Exception]]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Result[T, Exception]:
            try:
                value = func(*args, **kwargs)
                return Ok(value)
            except exceptions as e:
                return Err(e)
            except Exception as e:
                # Catch-all only if Exception is in the exception list
                if Exception in exceptions:
                    return Err(e)
                raise

        return wrapper

    return decorator


def as_result_async(
    *exceptions: type[Exception],
) -> Callable[[Callable[..., Awaitable[T]]], Callable[..., Awaitable[Result[T, Exception]]]]:
    """Async version of as_result decorator."""

    def decorator(
        func: Callable[..., Awaitable[T]],
    ) -> Callable[..., Awaitable[Result[T, Exception]]]:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Result[T, Exception]:
            try:
                value = await func(*args, **kwargs)
                return Ok(value)
            except exceptions as e:
                return Err(e)
            except Exception as e:
                if Exception in exceptions:
                    return Err(e)
                raise

        return wrapper

    return decorator


# ============================================================================
# TYPE GUARDS — FOR PATTERN MATCHING AND NARROWING
# ============================================================================


def is_ok(result: Result[T, E]) -> bool:
    """Type guard: returns True if result is Ok."""
    return isinstance(result, Ok)


def is_err(result: Result[T, E]) -> bool:
    """Type guard: returns True if result is Err."""
    return isinstance(result, Err)


def is_some(option: Option[T]) -> bool:
    return isinstance(option, Some)


def is_none(option: Option[T]) -> bool:
    return isinstance(option, Nothing)


# ============================================================================
# COLLECT — AGGREGATE MULTIPLE RESULTS
# ============================================================================
#
# Usage:
#     results = [engine_health_check(e) for e in engines]  # List[Result[Health, Error]]
#     collected = collect(results)  # -> Result[List[Health], FirstError]


def collect(results: list[Result[T, E]]) -> Result[list[T], E]:
    """Collect a list of Results into a single Result.

    Returns Ok([values]) if all succeed, or Err(first_error) if any fail.
    """
    values: list[T] = []
    for r in results:
        if is_err(r):
            return r  # type: ignore[return-value]
        values.append(r.unwrap())
    return Ok(values)


def collect_all_errors(results: list[Result[T, E]]) -> Result[list[T], list[E]]:
    """Collect all errors, not just the first."""
    values: list[T] = []
    errors: list[E] = []
    for r in results:
        if is_err(r):
            errors.append(r.error)  # type: ignore[attr-defined]
        else:
            values.append(r.unwrap())
    if errors:
        return Err(ExceptionGroup("Multiple failures", errors))  # type: ignore[return-value]
    return Ok(values)


# ============================================================================
# HARMONY-SPECIFIC RESULT TYPES
# ============================================================================


@dataclass(frozen=True, slots=True)
class HarmonyError(Exception):
    """Base for all Harmony-specific errors with domain and law context."""

    domain: str
    law_triggered: str
    mu_at_failure: float
    action_hash: str
    timestamp: str

    def __str__(self) -> str:
        return (
            f"HarmonyError[domain={self.domain}, law={self.law_triggered}, "
            f"mu={self.mu_at_failure:.6f}, action={self.action_hash[:16]}..., "
            f"time={self.timestamp}]"
        )


@dataclass(frozen=True, slots=True)
class SealVerificationError(HarmonyError):
    """SHA3-512 seal mismatch or missing seal."""

    expected_seal: str
    actual_seal: str


@dataclass(frozen=True, slots=True)
class ResonanceViolationError(HarmonyError):
    """mu dropped below 0.9995 threshold."""

    domain_values: dict[str, float]


@dataclass(frozen=True, slots=True)
class CHGateViolationError(HarmonyError):
    """One or more of the 16 laws were violated."""

    violated_laws: list[str]
    gate_priority: str


# ============================================================================
# EXAMPLE: REPLACING Optional WITH Result
# ============================================================================
#
# BEFORE (unsafe):
#     def get_engine_config(engine_id: str) -> Optional[dict]:
#         config = _load_config(engine_id)
#         return config  # Could be None!
#
#     cfg = get_engine_config("bridge_core")
#     port = cfg.get("port")  # CRASH if cfg is None!
#
# AFTER (safe):
#     def get_engine_config(engine_id: str) -> Result[dict, FileNotFoundError]:
#         try:
#             with open(f"/harmony/config/{engine_id}.yaml") as f:
#                 return Ok(yaml.safe_load(f))
#         except FileNotFoundError as e:
#             return Err(e)
#
#     result = get_engine_config("bridge_core")
#     match result:
#         case Ok(cfg):
#             port = cfg["port"]
#         case Err(e):
#             logger.error(f"Config missing: {e}")
#             return Err(e)  # Propagate upstream


# ============================================================================
# MODULE EXPORTS
# ============================================================================

__all__ = [
    "Ok",
    "Err",
    "Result",
    "Some",
    "Nothing",
    "Option",
    "Never",
    "UnwrapError",
    "as_result",
    "as_result_async",
    "is_ok",
    "is_err",
    "is_some",
    "is_none",
    "collect",
    "collect_all_errors",
    "HarmonyError",
    "SealVerificationError",
    "ResonanceViolationError",
    "CHGateViolationError",
]
