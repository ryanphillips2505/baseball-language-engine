from assemblers.plate_appearance_grouper import group_gamechanger_plate_appearances


def test_group_gamechanger_plate_appearances_attaches_pitch_lines_to_action():
    lines = [
        "Strike 1 looking.",
        "Ball 1.",
        "Foul.",
        "In play.",
        "John Smith singles on a line drive to center fielder.",
    ]

    grouped = group_gamechanger_plate_appearances(lines)

    assert grouped == [
        "Strike 1 looking.\n"
        "Ball 1.\n"
        "Foul.\n"
        "In play.\n"
        "John Smith singles on a line drive to center fielder."
    ]