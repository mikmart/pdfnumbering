import argparse

import pypdf

from pdfnumbering.core import PdfNumberer


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--output", required=True)
    parser.add_argument("--font-size", default=32, type=int)
    return parser.parse_args()


def main():
    args = parse_args()
    numberer = PdfNumberer(font_size=args.font_size)
    document = pypdf.PdfWriter(clone_from=args.file)
    numberer.stamp_page_numbers(document)
    document.write(args.output)


if __name__ == "__main__":
    main()
