import io
import math
from dataclasses import dataclass
from typing import Container, Iterable

import fpdf
import pypdf
from fpdf import Align
from pypdf import PageObject as Page


@dataclass(slots=True, kw_only=True)
class PdfNumberer:
    start: int = 1
    ignore: Container[int] = ()
    skip: Container[int] = ()
    format: str = "{}"
    color: tuple[int, int, int] = (255, 0, 0)
    font_size: int = 32
    font_family: str = "Helvetica"
    align: str | Align = Align.L
    position: tuple[int, int] = (0, 0)
    margin: tuple[int, int] = (28, 28)

    def add_page_numbering(self, pages: Iterable[Page]) -> None:
        """
        Stamp a collection of PDF pages with page numbers.
        """
        page_numbers, page_count = self._create_numbering(pages)
        for page_number, page in zip(page_numbers, pages):
            if page_number is not None:
                text = self.format.format(page_number, page_count)
                page.merge_page(self._create_stamp(page, text))

    def _create_numbering(self, pages: Iterable[Page]) -> tuple[list[int | None], int]:
        """
        Create page numbers and total page count.
        """
        page_numbers = []
        current_number = self.start
        for page in pages:
            if page.page_number in self.ignore:
                # Don't count and don't number
                page_numbers.append(None)
            elif page.page_number in self.skip:
                # Count but don't number
                page_numbers.append(None)
                current_number += 1
            else:
                # Count and number
                page_numbers.append(current_number)
                current_number += 1
        return page_numbers, current_number

    def _create_stamp(self, page: Page, text: str) -> Page:
        """
        Create a page for stamping text.
        """
        # Create an empty fpdf page matching the pypdf page dimensions
        pdf = fpdf.FPDF(unit="pt")
        pdf.add_page(format=(page.mediabox.width, page.mediabox.height))

        # Position text cursor on page
        pdf.set_auto_page_break(False)  # Allow small negative y-positions
        pdf.set_y(math.copysign(self.margin[1], self.position[1]) + self.position[1])
        pdf.set_x(math.copysign(self.margin[0], self.position[0]) + self.position[0])

        # Set font styling
        pdf.set_font(self.font_family)
        pdf.set_font_size(self.font_size)
        pdf.set_text_color(*self.color)

        # Write stamp text
        pdf.cell(0, 0, text, align=self.align)

        # Convert to a pypdf page and return
        def to_pypdf(pdf: fpdf.FPDF) -> pypdf.PdfReader:
            return pypdf.PdfReader(io.BytesIO(pdf.output()))

        return to_pypdf(pdf).pages[0]
