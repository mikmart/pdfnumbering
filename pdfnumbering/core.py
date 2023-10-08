import io
import math
from dataclasses import dataclass
from typing import Container, Iterable, Protocol

import fpdf
import pypdf
from fpdf import Align
from pypdf import PageObject as Page


class Formatter(Protocol):
    def format(self, page_number: int, page_count: int, /) -> str:
        ...


@dataclass(slots=True, kw_only=True)
class PdfNumberer:
    color: tuple[int, int, int] = (255, 0, 0)
    font_size: int = 32
    font_family: str = "Helvetica"
    align: str | Align = Align.L
    position: tuple[int, int] = (0, 0)
    margin: tuple[int, int] = (28, 28)
    start: int = 1
    skip: Container[int] = ()
    ignore: Container[int] = ()
    formatter: Formatter = "{}"

    def add_page_numbering(self, pages: Iterable[Page]) -> None:
        """
        Stamp a set of PDF pages with page numbers.
        """
        page_numbers = list(self._create_page_numbers(pages))
        page_count = max(page for page in page_numbers if page is not None)
        for page_number, page in zip(page_numbers, pages):
            if page_number is not None:
                text = self.formatter.format(page_number, page_count)
                page.merge_page(self._create_stamp(page, text))

    def _create_page_numbers(self, pages: Iterable[Page]) -> Iterable[int | None]:
        page_number = self.start
        for page in pages:
            if page.page_number in self.ignore:
                # Don't count and don't show
                yield None
            elif page.page_number in self.skip:
                # Count but don't show
                yield None
                page_number += 1
            else:
                # Count and show
                yield page_number
                page_number += 1

    def _create_stamp(self, page: Page, text: str) -> Page:
        # Create fpdf page matching pypdf page dimensions
        pdf = fpdf.FPDF(unit="pt")
        pdf.add_page(format=(page.mediabox.width, page.mediabox.height))

        # Position cursor on page
        pdf.set_auto_page_break(False)  # Allow small negative y-positions
        pdf.set_y(math.copysign(self.margin[1], self.position[1]) + self.position[1])
        pdf.set_x(math.copysign(self.margin[0], self.position[0]) + self.position[0])

        # Set font styling
        pdf.set_font(self.font_family, size=self.font_size)
        pdf.set_text_color(*self.color)

        # Write stamp text
        pdf.cell(0, 0, text, align=self.align)

        # Return as a pypdf page
        def to_pypdf(pdf: fpdf.FPDF) -> pypdf.PdfReader:
            return pypdf.PdfReader(io.BytesIO(pdf.output()))

        return to_pypdf(pdf).pages[0]
