import argparse
import importlib.metadata
import sys

import pypdf

from pdfnumbering.color import hex2rgb
from pdfnumbering.core import PdfNumberer


def create_parser():
    parser = argparse.ArgumentParser(
        description="Stamp pages in a PDF document with page numbers.",
        allow_abbrev=False,
    )

    version_string = "%(prog)s {}".format(importlib.metadata.version("pdfnumbering"))
    parser.add_argument("-v", "--version", action="version", version=version_string)

    styling = parser.add_argument_group("styling options")
    styling.add_argument(
        "--color", default="#ff0000", help="hex color code (default: %(default)s)"
    )
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

    placement = parser.add_argument_group("placement options")
    placement.add_argument(
        "--align",
        default="left",
        choices=("left", "center", "right"),
        help="horizontal alignment of page numbers (default: %(default)s)",
    )
    placement.add_argument(
        "--position",
        metavar=("X", "Y"),
        nargs=2,
        default=(0, 0),
        type=int,
        help="position of page numbers, in points (default: 0 0)",
    )
    placement.add_argument(
        "--margin",
        metavar=("X", "Y"),
        nargs=2,
        type=int,
        help="margin at the page edges, in points (default: adapts to font size)",
    )

    numbering = parser.add_argument_group("numbering options")
    numbering.add_argument(
        "--start",
        default=1,
        type=int,
        help="number to start stamping with (default: %(default)s)",
    )
    numbering.add_argument(
        "--skip",
        metavar="PAGE",
        nargs="*",
        default=(),
        type=int,
        help="pages that should not be stamped",
    )
    numbering.add_argument(
        "--ignore",
        metavar="PAGE",
        nargs="*",
        default=(),
        type=int,
        help="pages that should not be counted",
    )

    parser.add_argument("-o", "--output", help="destination to write output PDF to")
    parser.add_argument("file", metavar="FILE", help="the input PDF file to stamp")

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    # Refuse to write binary data to terminal
    if not args.output and sys.stdout.isatty():
        parser.error("`--output` must be specified or stdout redirected.")

    if args.margin is None:
        args.margin = (28, 28 + args.font_size // 2)

    numberer = PdfNumberer(
        color=hex2rgb(args.color),
        font_size=args.font_size,
        font_family=args.font_family,
        align=args.align[0].upper(),
        position=args.position,
        margin=args.margin,
        start=args.start,
        skip=[page - 1 for page in args.skip],
        ignore=[page - 1 for page in args.ignore],
    )

    document = pypdf.PdfWriter(clone_from=args.file)
    numberer.add_page_numbering(document.pages)
    document.write(args.output or sys.stdout.buffer)


if __name__ == "__main__":
    main()
