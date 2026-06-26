from pathlib import Path

from tools.inspection.workbench import Workbench


def test_workbench_can_load_game_file(tmp_path: Path):
    game = tmp_path / "game.txt"

    game.write_text(
        "Strike 1 swinging.\n"
        "John Smith strikes out swinging.\n"
        "\n"
        "Ball 1.\n"
        "Trey Jones walks.\n"
    )

    workbench = Workbench()

    inspection = workbench.inspect_game_file(game)

    assert len(inspection.play_inspections) == 2