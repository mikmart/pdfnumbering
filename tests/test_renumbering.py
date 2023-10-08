from pdfnumbering import PdfNumberer


def test_renumbering_page_count():
    # Page count is unchanged by default.
    numberer = PdfNumberer()
    _, count = numberer._renumber([0, 1, 2])
    assert count == 3

    # Ignoring reduces page count.
    numberer = PdfNumberer(ignore_pages=[2])
    _, count = numberer._renumber([0, 1, 2])
    assert count == 2

    # Skipping doesn't affect page count.
    numberer = PdfNumberer(skip_pages=[2])
    _, count = numberer._renumber([0, 1, 2])
    assert count == 3


def test_renumbering_first_number():
    # Defaults to 1-based numbering.
    numberer = PdfNumberer()
    numbers, _ = numberer._renumber([0, 1, 2])
    assert numbers == [1, 2, 3]

    # Can change first number.
    numberer = PdfNumberer(first_number=42)
    numbers, _ = numberer._renumber([0, 1, 2])
    assert numbers == [42, 43, 44]


def test_renumbering_ignoring():
    numberer = PdfNumberer(ignore_pages=[0])
    numbers, _ = numberer._renumber([0, 1, 2])
    assert numbers == [None, 1, 2]

    numberer = PdfNumberer(ignore_pages=[1])
    numbers, _ = numberer._renumber([0, 1, 2])
    assert numbers == [1, None, 2]


def test_renumbering_skipping():
    numberer = PdfNumberer(skip_pages=[0])
    numbers, _ = numberer._renumber([0, 1, 2])
    assert numbers == [None, 2, 3]

    numberer = PdfNumberer(skip_pages=[1])
    numbers, _ = numberer._renumber([0, 1, 2])
    assert numbers == [1, None, 3]
