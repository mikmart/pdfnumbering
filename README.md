# Adding page numbers to a PDF document

## Installation

```sh
python -m pip install git+https://github.com/mikmart/pdfnumbering.git
```

## Usage

### Package

```py
import sys

from pypdf import PdfWriter
from pdfnumbering import PdfNumberer

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
usage: pdfnumbering [-h] [-v] [--start START] [--ignore [PAGE ...]] [--skip [PAGE ...]]
                    [--format FORMAT] [--color COLOR] [--font-size PT]
                    [--font-family NAME] [--align {left,center,right}] [--position X Y]
                    [--margin X Y] [-o OUTPUT]
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
  --start START         first number to stamp with (default: 1)
  --ignore [PAGE ...]   pages that should not be counted
  --skip [PAGE ...]     pages that should not be stamped
  --format FORMAT       format string for stamp text, formatted with page number and page
                        count (default: "{}")

styling options:
  --color COLOR         hex color code (default: #ff0000)
  --font-size PT        font size in points (default: 32)
  --font-family NAME    font family name (default: Helvetica)

placement options:
  --align {left,center,right}
                        horizontal alignment of page numbers (default: left)
  --position X Y        position of page numbers, in points (default: 0 0)
  --margin X Y          margin at the page edges, in points (default: adapts to font size)
```
