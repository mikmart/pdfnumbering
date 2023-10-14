from pdfnumbering.cli import create_parser, process_args


def processed(argv):
    parser = create_parser()
    args = parser.parse_args(argv)
    return process_args(args)


def test_cli_adaptive_margins():
    # Page margins adapt to font size
    args0, _ = processed(["-", "--font-size=32"])
    args1, _ = processed(["-", "--font-size=64"])
    assert args0.page_margin < args1.page_margin
