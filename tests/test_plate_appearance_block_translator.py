from translators.plate_appearance_block_translator import translate_pa_block


def test_translate_pa_block():
    block = (
        "Strike 1 looking.\n"
        "Ball 1.\n"
        "Foul.\n"
        "John Smith singles to center field."
    )

    result = translate_pa_block(block)

    assert result.action_text == "John Smith singles to center field."
    assert result.pitch_lines == [
        "Strike 1 looking.",
        "Ball 1.",
        "Foul.",
    ]
    assert result.raw_lines == [
        "Strike 1 looking.",
        "Ball 1.",
        "Foul.",
        "John Smith singles to center field.",
    ]