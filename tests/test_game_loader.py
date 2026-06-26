from pathlib import Path

from tools.inspection.game_loader import load_game_file


def test_load_game_file(tmp_path: Path):
    game = tmp_path / "game.txt"

    game.write_text(
        "Play One\n"
        "Result One\n"
        "\n"
        "Play Two\n"
        "Result Two\n"
    )

    plays = load_game_file(game)

    assert len(plays) == 2

    assert plays[0] == "Play One\nResult One"

    assert plays[1] == "Play Two\nResult Two"