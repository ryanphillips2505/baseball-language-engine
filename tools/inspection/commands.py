from __future__ import annotations

from .workbench import Workbench


def inspect_play(raw_play: str) -> None:
    """
    Inspect a single raw play.
    """
    workbench = Workbench()

    inspection = workbench.inspect_play(raw_play)
    workbench.print_play(inspection)


def inspect_game(path: str) -> None:
    """
    Inspect a raw game file through the full BLE pipeline.
    """
    workbench = Workbench()
    workbench.print_ble_file_inspection(path)


def inspect_report(path: str) -> None:
    """
    Build and print the report inspection for a raw game file.
    """
    workbench = Workbench()

    inspection = workbench.inspect_game_file(path)
    workbench.print_game(inspection)