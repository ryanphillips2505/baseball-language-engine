from tools.inspection.workbench import Workbench


def test_workbench_can_build_play_inspection():
    workbench = Workbench()

    inspection = workbench.inspect_play(
        "John Smith strikes out swinging."
    )

    assert inspection.plate_appearance.batter_name == "John Smith"


def test_workbench_can_build_game_inspection():
    workbench = Workbench()

    inspection = workbench.inspect_game(
        [
            "John Smith strikes out swinging.",
            "Wade Webb doubles on a fly ball to center field.",
        ]
    )

    assert len(inspection.play_inspections) == 2
    assert len(inspection.game.plate_appearances) == 2
    