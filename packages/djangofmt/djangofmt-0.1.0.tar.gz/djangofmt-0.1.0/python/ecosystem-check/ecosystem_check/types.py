from __future__ import annotations

import dataclasses
import difflib
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass, is_dataclass
from typing import TYPE_CHECKING, Any, Self

if TYPE_CHECKING:
    from ecosystem_check.projects import ClonedRepository, Project


class Serializable:
    """
    Allows serialization of content by casting to a JSON-compatible type.
    """

    def jsonable(self) -> Any:
        # Default implementation for dataclasses
        if is_dataclass(self) and not isinstance(self, type):
            return dataclasses.asdict(self)

        raise NotImplementedError()


class Diff(Serializable):
    def __init__(self, lines: Iterable[str], leading_spaces: int = 0) -> None:
        self.lines = list(lines)

        # Compute added and removed lines once
        self.added = [
            line[2:]
            for line in self.lines
            if line.startswith("+" + " " * leading_spaces)
            # Do not include patch headers
            and not line.startswith("+++")
        ]
        self.removed = [
            line[2:]
            for line in self.lines
            if line.startswith("-" + " " * leading_spaces)
            # Do not include patch headers
            and not line.startswith("---")
        ]

    def __bool__(self) -> bool:
        return bool(self.added or self.removed)

    def __iter__(self) -> Iterator[str]:
        yield from self.lines

    @property
    def lines_added(self) -> int:
        return len(self.added)

    @property
    def lines_removed(self) -> int:
        return len(self.removed)

    @classmethod
    def from_pair(cls, baseline: Sequence[str], comparison: Sequence[str]) -> Self:
        """
        Construct a diff from before and after.
        """
        return cls(difflib.ndiff(baseline, comparison), leading_spaces=1)

    def without_unchanged_lines(self) -> Diff:
        return Diff(line for line in self.lines if line.startswith(("+", "-")))

    def jsonable(self) -> Any:
        return self.lines


@dataclass(frozen=True)
class Result(Serializable):
    """
    The result of an ecosystem check for a collection of projects.
    """

    errored: list[tuple[Project, BaseException]]
    completed: list[tuple[Project, Comparison]]


@dataclass(frozen=True)
class Comparison(Serializable):
    """
    The result of a completed ecosystem comparison for a single project.
    """

    diff: Diff
    repo: ClonedRepository


class ToolError(Exception):
    """An error reported by the checked executable."""
