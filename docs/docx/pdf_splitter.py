import os
import logging
from pathlib import Path
from pdf2docx import Converter
import PyPDF2
from typing import Dict, Tuple, Optional

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PDFSplitter:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.output_dir = os.path.dirname(pdf_path)
        self.page_ranges = {}
        self._analyze_pdf()

    def _analyze_pdf(self) -> None:
        """Analyze PDF structure and determine page ranges."""
        logger.info(f"Analyzing PDF: {self.pdf_path}")
        
        # Use PyPDF2 to get document structure and page count
        with open(self.pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            self.total_pages = len(reader.pages)
            logger.info(f"Total pages: {self.total_pages}")
            
            # Check for table of contents
            toc = reader.outline
            if toc:
                logger.info("Found table of contents structure")
                self._extract_page_ranges_from_toc(toc)
            else:
                logger.warning("No table of contents found, using default page ranges")
                self._set_default_page_ranges()
    def _extract_page_ranges_from_toc(self, toc) -> None:
        """Extract page ranges from table of contents."""
        # Implementation would parse TOC structure
        # For now, using default ranges as TOC parsing requires manual review
        self._set_default_page_ranges()

    def _set_default_page_ranges(self) -> None:
        """Set default page ranges for each section."""
        # These ranges should be adjusted based on actual PDF structure
        self.page_ranges = {
            'Table_of_Contents': (1, 3),
            'Introduction': (4, 8),
            'Chapters_1-3': (9, 35),
            'Chapters_4-6': (36, 62),
            'Chapters_7-9': (63, 89),
            'Chapters_10-12': (90, 116),
            'Chapters_13-15': (117, 143),
            'Chapters_16-19': (144, self.total_pages)
        }

    def convert_section(self, section_name: str, start_page: int, end_page: int) -> bool:
        """Convert a specific section of the PDF to DOCX."""
        output_path = os.path.join(self.output_dir, f"{section_name}.docx")
        logger.info(f"Converting section: {section_name} (pages {start_page}-{end_page})")
        
        cv = None
        try:
            cv = Converter(self.pdf_path)
            cv.convert(output_path, start=start_page-1, end=end_page)  # pdf2docx uses 0-based indexing
            logger.info(f"Successfully created: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error converting section {section_name}: {str(e)}")
            return False
        finally:
            if cv is not None:
                cv.close()

    def split_pdf(self) -> None:
        """Split PDF into specified sections."""
        logger.info("Starting PDF splitting process")
        
        for section_name, (start_page, end_page) in self.page_ranges.items():
            self.convert_section(section_name, start_page, end_page)

def main():
    pdf_path = "/Users/ojeromyo/Desktop/wellspring_directory/docs/The-Wellspring-Book.pdf"
    
    if not os.path.exists(pdf_path):
        logger.error(f"PDF file not found: {pdf_path}")
        return

    try:
        splitter = PDFSplitter(pdf_path)
        splitter.split_pdf()
        logger.info("PDF splitting completed successfully")
    except Exception as e:
        logger.error(f"Error during PDF splitting: {str(e)}")

if __name__ == "__main__":
    main()

