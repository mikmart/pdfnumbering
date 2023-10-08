# Add page numbers to a PDF document

pdfnumbering builds on [pypdf](https://github.com/py-pdf/pypdf) and
[fpdf2](https://github.com/py-pdf/fpdf2) to make it easy to stamp page numbers
to a PDF document, and provides a convenient CLI tool to do so.

## Installation

```sh
python -m pip install git+https://github.com/mikmart/pdfnumbering.git
```

## Usage

### Package

```py
import sys

from pdfnumbering import PdfNumberer
from pypdf import PdfWriter

INPUT_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]

numberer = PdfNumberer()
document = PdfWriter(clone_from=INPUT_FILE)
numberer.add_page_numbering(document.pages)
document.write(OUTPUT_FILE)
```

### Command line interface

```
$ pdfnumbering --help
usage: pdfnumbering [-h] [-v] [--first-number N] [--ignore-pages [PAGE ...]]
                    [--skip-pages [PAGE ...]] [--stamp-format STRING] [--font-size PT]
                    [--font-family NAME] [--text-color HEX] [--text-align {left,center,right}]
                    [--text-position X Y] [--page-margin X Y] [-o OUTPUT]
                    FILE

Stamp pages in a PDF document with page numbers.

positional arguments:
  FILE                  the input PDF file to stamp

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -o OUTPUT, --output OUTPUT
                        destination to write output to

numbering options:
  --first-number N      number to start counting from (default: 1)
  --ignore-pages [PAGE ...]
                        pages that should not be counted
  --skip-pages [PAGE ...]
                        pages that should not be stamped
  --stamp-format STRING
                        format string for stamp text, formatted with page number and page
                        count (default: "{}")

styling options:
  --font-size PT        font size in points (default: 32)
  --font-family NAME    font family name (default: Helvetica)
  --text-color HEX      hexadecimal color code (default: #ff0000)

placement options:
  --text-align {left,center,right}
                        horizontal alignment of page numbers (default: left)
  --text-position X Y   position of page numbers, in points (default: 0 0)
  --page-margin X Y     margin at the page edges, in points (default: adapts to font size)
```
