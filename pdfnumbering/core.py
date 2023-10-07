import io
from dataclasses import dataclass

import fpdf
import pypdf

from .color import hex2rgb


@dataclass(slots=True, kw_only=True)
class PdfNumberer:
    font_family: str = "Helvetica"
    font_size: int = 32
    color: str = "#ff0000"
    position: tuple[int, int] = (10, 5)

    @property
    def _final_position(self) -> tuple[int, int]:
        return self.position[0], self.position[1] + self.font_size

    def stamp_page_numbers(self, document: pypdf.PdfReader | pypdf.PdfWriter) -> None:
        """
        Add page number stamps to each page of a PDF document.
        """
        for page in document.pages:
            page.merge_page(self._create_stamp(page))

    def _create_stamp(self, page: pypdf.PageObject) -> pypdf.PageObject:
        def to_fpdf_format(page: pypdf.PageObject) -> tuple[float, float]:
            return page.mediabox.width, page.mediabox.height

        pdf = fpdf.FPDF(unit="pt")
        pdf.add_page(format=to_fpdf_format(page))
        pdf.set_font(self.font_family, size=self.font_size)
        pdf.set_text_color(*hex2rgb(self.color))
        pdf.text(*self._final_position, str(page.page_number + 1))

        def to_pypdf(pdf: fpdf.FPDF) -> pypdf.PdfReader:
            return pypdf.PdfReader(io.BytesIO(pdf.output()))

        return to_pypdf(pdf).pages[0]
