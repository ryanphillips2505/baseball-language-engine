from __future__ import annotations

from typing import Any

from .models import ValidationIssue


UNKNOWN_EVENT_NAMES = {"unknown", "UNKNOWN", None}


def _event_name(pa: Any) -> str | None:
    event = getattr(pa, "baseball_event", None)
    primary = getattr(event, "primary_event", None)

    if primary is None:
        return None

    return getattr(primary, "value", str(primary))


def run_validation_checks(data: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    game = data.get("game")
    plate_appearances = getattr(game, "plate_appearances", []) or []
    cleaned = data.get("cleaned_plate_appearances", []) or []

    for index, pa in enumerate(plate_appearances, start=1):
        batter = getattr(pa, "batter_name", None)
        raw = cleaned[index - 1] if index - 1 < len(cleaned) else None

        if not batter:
            issues.append(
                ValidationIssue(
                    level="error",
                    check="batter_extraction",
                    message="Missing batter name.",
                    index=index,
                    raw=raw,
                )
            )

        event_name = _event_name(pa)
        if event_name in UNKNOWN_EVENT_NAMES:
            issues.append(
                ValidationIssue(
                    level="error",
                    check="event_detection",
                    message="Missing or unknown primary event.",
                    index=index,
                    batter=batter,
                    raw=raw,
                )
            )

        is_bip = bool(getattr(pa, "is_bip", False))

        if is_bip and not getattr(pa, "ball_type", None):
            issues.append(
                ValidationIssue(
                    level="warning",
                    check="ball_type",
                    message="Ball in play is missing ball type.",
                    index=index,
                    batter=batter,
                    raw=raw,
                )
            )

        if is_bip and not getattr(pa, "location", None):
            issues.append(
                ValidationIssue(
                    level="warning",
                    check="location",
                    message="Ball in play is missing location.",
                    index=index,
                    batter=batter,
                    raw=raw,
                )
            )

        for runner_event in getattr(pa, "runner_events", []) or []:
            if not getattr(runner_event, "event_type", None):
                issues.append(
                    ValidationIssue(
                        level="error",
                        check="runner_events",
                        message="Runner event is missing event type.",
                        index=index,
                        batter=batter,
                        raw=raw,
                    )
                )

            if not getattr(runner_event, "base", None):
                issues.append(
                    ValidationIssue(
                        level="warning",
                        check="runner_events",
                        message="Runner event is missing base.",
                        index=index,
                        batter=batter,
                        raw=raw,
                    )
                )

            if not getattr(runner_event, "runner_name", None):
                issues.append(
                    ValidationIssue(
                        level="warning",
                        check="runner_events",
                        message="Runner event is missing runner name.",
                        index=index,
                        batter=batter,
                        raw=raw,
                    )
                )

    return issues
