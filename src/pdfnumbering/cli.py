"""
Command line interface to the package.
"""
import argparse
import sys

import pypdf

from . import __version__
from .color import hex2rgb
from .core import Align, PdfNumberer


def create_parser():
    """
    Create parser for CLI arguments.
    """
    parser = argparse.ArgumentParser(
        description="Stamp pages in a PDF document with page numbers.",
        allow_abbrev=False,
    )

    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )

    numbering = parser.add_argument_group("numbering options")
    numbering.add_argument(
        "--first-number",
        metavar="N",
        default=1,
        type=int,
        help="number to start counting from (default: %(default)s)",
    )
    numbering.add_argument(
        "--ignore-pages",
        metavar="PAGE",
        nargs="*",
        default=(),
        type=int,
        help="pages that should not be counted",
    )
    numbering.add_argument(
        "--skip-pages",
        metavar="PAGE",
        nargs="*",
        default=(),
        type=int,
        help="pages that should not be stamped",
    )
    numbering.add_argument(
        "--stamp-format",
        metavar="STRING",
        default="{}",
        help='format string for stamp text, formatted with page number and page count (default: "{}")',
    )

    styling = parser.add_argument_group("styling options")
    styling.add_argument(
        "--font-size",
        metavar="PT",
        default=32,
        type=int,
        help="font size in points (default: %(default)s)",
    )
    styling.add_argument(
        "--font-family",
        metavar="NAME",
        default="Helvetica",
        help="font family name (default: %(default)s)",
    )
    styling.add_argument(
        "--text-color",
        metavar="HEX",
        default="#ff0000",
        help="hexadecimal color code (default: %(default)s)",
    )

    placement = parser.add_argument_group("placement options")
    placement.add_argument(
        "--text-align",
        default="left",
        choices=("left", "center", "right"),
        help="horizontal alignment of page numbers (default: %(default)s)",
    )
    placement.add_argument(
        "--text-position",
        metavar=("X", "Y"),
        nargs=2,
        default=(0, 0),
        type=int,
        help="position of page numbers, in points (default: 0 0)",
    )
    placement.add_argument(
        "--page-margin",
        metavar=("X", "Y"),
        nargs=2,
        type=int,
        help="margin at the page edges, in points (default: adapts to font size)",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=argparse.FileType("wb"),
        help="destination to write output to",
    )
    parser.add_argument(
        "file",
        metavar="FILE",
        type=argparse.FileType("rb"),
        help="the input PDF file to stamp",
    )

    return parser


def process_args(args) -> tuple[argparse.Namespace, str | None]:
    """
    Post-process parsed CLI arguments.
    """
    # Refuse to write binary data to terminal
    if not args.output and sys.stdout.isatty():
        return args, "--output must be specified or stdout redirected."

    # Parse hex color code to RGB tuple
    try:
        args.text_color = hex2rgb(args.text_color)
    except ValueError as error:
        return args, f"argument --text-color: {error}"

    # Convert align string choice to enum value
    args.text_align = Align.coerce(args.text_align[0].upper())

    # Adapt vertical margins to font size by default
    if args.page_margin is None:
        args.page_margin = (28, 28 + args.font_size // 2)

    # Convert pages from 1-based to 0-based indexing
    args.ignore_pages = [page - 1 for page in args.ignore_pages]
    args.skip_pages = [page - 1 for page in args.skip_pages]

    return args, None


def main():
    """
    Command line entrypoint.
    """
    parser = create_parser()
    args = parser.parse_args()
    args, error = process_args(args)
    if error is not None:
        parser.error(error)

    numberer = PdfNumberer(
        first_number=args.first_number,
        ignore_pages=args.ignore_pages,
        skip_pages=args.skip_pages,
        stamp_format=args.stamp_format,
        font_size=args.font_size,
        font_family=args.font_family,
        text_color=args.text_color,
        text_align=args.text_align,
        text_position=args.text_position,
        page_margin=args.page_margin,
    )

    document = pypdf.PdfWriter(clone_from=args.file)
    numberer.add_page_numbering(document.pages)
    document.write(args.output or sys.stdout.buffer)


if __name__ == "__main__":
    main()
