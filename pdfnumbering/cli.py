import argparse
import importlib.metadata
import sys

import pypdf

from pdfnumbering.core import PdfNumberer


def create_parser():
    parser = argparse.ArgumentParser(
        description="Stamp pages in a PDF with page numbers.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    version_string = "%(prog)s {}".format(importlib.metadata.version("pdfnumbering"))
    parser.add_argument("-v", "--version", action="version", version=version_string)

    styling = parser.add_argument_group("styling options")
    styling.add_argument("--color", default="#ff0000")
    styling.add_argument("--font-size", default=32, type=int)
    styling.add_argument("--font-family", default="Helvetica")

    placement = parser.add_argument_group("placement options")
    placement.add_argument(
        "--align",
        default="left",
        choices=("left", "center", "right"),
    )
    placement.add_argument(
        "--position",
        metavar=("X", "Y"),
        nargs=2,
        default=(0, 0),
        type=int,
    )
    placement.add_argument(
        "--margin",
        metavar=("X", "Y"),
        nargs=2,
        type=int,
    )

    numbering = parser.add_argument_group("numbering options")
    numbering.add_argument(
        "--start", default=1, type=int, help="number to start stamping with"
    )
    numbering.add_argument(
        "--skip",
        metavar="PAGE",
        nargs="*",
        type=int,
        help="pages that should not be stamped",
    )
    numbering.add_argument(
        "--ignore",
        metavar="PAGE",
        nargs="*",
        type=int,
        help="pages that should not be counted",
    )

    parser.add_argument("file", help="the input PDF file to stamp")
    parser.add_argument("-o", "--output", help="destination for output PDF")

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    if not args.output and sys.stdout.isatty():
        parser.error("`--output` must be specified or stdout redirected.")

    if args.margin is None:
        args.margin = (28, 28 + int(args.font_size / 2))

    numberer = PdfNumberer(
        color=args.color,
        font_family=args.font_family,
        font_size=args.font_size,
        align=args.align[0].upper(),
        position=tuple(args.position),  # type: ignore
        margin=tuple(args.margin),  # type: ignore
        start=args.start,
        skip=[page - 1 for page in args.skip or ()],
        ignore=[page - 1 for page in args.ignore or ()],
    )

    document = pypdf.PdfWriter(clone_from=args.file)
    numberer.add_page_numbering(document.pages)
    document.write(args.output or sys.stdout.buffer)


if __name__ == "__main__":
    main()
