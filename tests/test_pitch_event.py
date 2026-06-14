from models.pitch_event import PitchEvent


def test_pitch_event_model():
    pitch = PitchEvent(
        pitch_number=1,
        count_before="0-0",
        result="Strike Looking",
        swing=False,
        ball_in_play=False,
    )

    assert pitch.pitch_number == 1
    assert pitch.count_before == "0-0"
    assert pitch.result == "Strike Looking"
    assert pitch.swing is False
    assert pitch.ball_in_play is False
    assert pitch.terminal_pitch is False
    