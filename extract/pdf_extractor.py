"""PDF text extraction with memory optimization"""
from pathlib import Path
from common.logger import log

class PDFExtractor:
    """Extract text from PDF files with memory optimization"""

    def __init__(self, chunk_size=100):
        self.extracted_count = 0
        self.chunk_size = chunk_size

    def extract_text(self, pdf_path):
        """
        Extract text from PDF with chunked processing

        Args:
            pdf_path: Path to PDF file

        Returns:
            str: Extracted text
        """
        try:
            import PyPDF2

            text_chunks = []
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)

                # Process in chunks to avoid memory issues
                for i in range(0, num_pages, self.chunk_size):
                    chunk_text = ""
                    end_page = min(i + self.chunk_size, num_pages)

                    for page_num in range(i, end_page):
                        page = pdf_reader.pages[page_num]
                        chunk_text += page.extract_text()

                    text_chunks.append(chunk_text)

            text = "".join(text_chunks)
            self.extracted_count += 1
            log.info(f"Extracted text from {pdf_path} ({num_pages} pages)")

            return text

        except Exception as e:
            log.error(f"PDF extraction error: {e}")
            return ""

    def batch_extract(self, pdf_files):
        """Extract text from multiple PDFs"""
        results = {}

        for pdf_file in pdf_files:
            text = self.extract_text(pdf_file)
            results[pdf_file] = text

        log.info(f"Batch extraction complete: {len(results)} files")
        return results
