from Backend.app.Services.ingestion.text_cleaner import TextCleaner


def test_normal_text() -> None:
    cleaner = TextCleaner()

    result = cleaner.clean(
        "This is a normal document."
    )

    assert result == "This is a normal document."

    print("PASS: Normal text test")


def test_multiple_spaces() -> None:
    cleaner = TextCleaner()

    result = cleaner.clean(
        "This    is     a document."
    )

    assert result == "This is a document."

    print("PASS: Multiple spaces test")


def test_tabs() -> None:
    cleaner = TextCleaner()

    result = cleaner.clean(
        "Enterprise\tAI\tChatbot"
    )

    assert result == "Enterprise AI Chatbot"

    print("PASS: Tab normalization test")


def test_blank_lines() -> None:
    cleaner = TextCleaner()

    result = cleaner.clean(
        "Paragraph one.\n\n\n\nParagraph two."
    )

    assert result == (
        "Paragraph one.\n\n"
        "Paragraph two."
    )

    print("PASS: Blank line normalization test")


def test_hyphenated_word() -> None:
    cleaner = TextCleaner()

    result = cleaner.clean(
        "Enter-\nprise AI Chatbot"
    )

    assert result == "Enterprise AI Chatbot"

    print("PASS: Hyphenated word test")


def test_unicode_normalization() -> None:
    cleaner = TextCleaner()

    result = cleaner.clean(
        "Enterprise ＡＩ Chatbot"
    )

    assert result == "Enterprise AI Chatbot"

    print("PASS: Unicode normalization test")


def test_empty_text() -> None:
    cleaner = TextCleaner()

    try:
        cleaner.clean("")

    except ValueError:
        print("PASS: Empty text test")

    else:
        print(
            "FAIL: Empty text should raise ValueError"
        )


def test_invalid_input() -> None:
    cleaner = TextCleaner()

    try:
        cleaner.clean(123)  # type: ignore[arg-type]

    except TypeError:
        print("PASS: Invalid input test")

    else:
        print(
            "FAIL: Invalid input should raise TypeError"
        )


if __name__ == "__main__":

    print(
        "\n========== TEXT CLEANER TESTS =========="
    )

    test_normal_text()
    test_multiple_spaces()
    test_tabs()
    test_blank_lines()
    test_hyphenated_word()
    test_unicode_normalization()
    test_empty_text()
    test_invalid_input()