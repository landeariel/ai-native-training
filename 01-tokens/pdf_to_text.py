"""
Convert a PDF into a plain-text file and report its page and word count.

Usage:
    01-tokens/.venv/bin/python -I 01-tokens/pdf_to_text.py input.pdf output.txt
"""

import sys
from pathlib import Path

from pypdf import PdfReader


def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: pdf_to_text.py input.pdf output.txt")
    pdf_path, txt_path = Path(sys.argv[1]), Path(sys.argv[2])

    reader = PdfReader(pdf_path)
    pages = [page.extract_text() or "" for page in reader.pages]
    text = "\n\n".join(pages)
    txt_path.write_text(text, encoding="utf-8")

    print(f"Pages:      {len(reader.pages)}")
    print(f"Words:      {len(text.split())}")
    print(f"Characters: {len(text)}")
    print(f"Saved to    {txt_path}")


if __name__ == "__main__":
    main()
