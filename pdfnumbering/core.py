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
    first_number: int = 1
    ignore_pages: Container[int] = ()
    skip_pages: Container[int] = ()
    stamp_format: str = "{}"
    font_size: int = 32
    font_family: str = "Helvetica"
    text_color: tuple[int, int, int] = (255, 0, 0)
    text_align: str | Align = Align.L
    text_position: tuple[int, int] = (0, 0)
    page_margin: tuple[int, int] = (28, 28)

    def add_page_numbering(self, pages: Iterable[Page]) -> None:
        """
        Stamp a collection of PDF pages with page numbers.
        """
        page_numbers = (page.page_number for page in pages)
        page_numbers, page_count = self._renumber(page_numbers)
        for page_number, page in zip(page_numbers, pages):
            if page_number is not None:
                text = self.stamp_format.format(page_number, page_count)
                page.merge_page(self._create_stamp(page, text))

    def _renumber(self, page_numbers: Iterable[int]) -> tuple[list[int | None], int]:
        """
        Create page numbers and total page count.
        """
        new_numbers = []
        next_number = self.first_number
        for page_number in page_numbers:
            if page_number in self.ignore_pages:
                # Don't count and don't number
                new_numbers.append(None)
            elif page_number in self.skip_pages:
                # Count but don't number
                new_numbers.append(None)
                next_number += 1
            else:
                # Count and number
                new_numbers.append(next_number)
                next_number += 1
        return new_numbers, next_number - 1

    def _create_stamp(self, page: Page, text: str) -> Page:
        """
        Create a page for stamping text.
        """
        # Create an empty fpdf page matching the pypdf page dimensions
        pdf = fpdf.FPDF(unit="pt")
        pdf.add_page(format=(page.mediabox.width, page.mediabox.height))

        # Set font styling
        pdf.set_font(self.font_family)
        pdf.set_font_size(self.font_size)
        pdf.set_text_color(*self.text_color)

        # Position text cursor on page
        def add_margin(position, margin):
            return position + math.copysign(margin, position)

        pdf.set_auto_page_break(False)  # Allow small negative y-positions
        pdf.set_y(add_margin(self.text_position[1], self.page_margin[1]))
        pdf.set_x(add_margin(self.text_position[0], self.page_margin[0]))

        # Write stamp text
        pdf.cell(0, 0, text, align=self.text_align)

        # Convert to a pypdf page and return
        def to_pypdf(pdf: fpdf.FPDF) -> pypdf.PdfReader:
            return pypdf.PdfReader(io.BytesIO(pdf.output()))

        return to_pypdf(pdf).pages[0]
