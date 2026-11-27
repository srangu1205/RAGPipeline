"""Data ingestion: download a PDF, read it with PyMuPDF and collect per-page stats."""

import os
import re
import sys

import pymupdf
import requests

from statsoffile import display_pages_dataframe, display_pages_stats

# Windows consoles default to cp1252, which can't print many PDF characters.
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(PROJECT_DIR, "human-nutrition-text.pdf")
PDF_URL = "https://pressbooks.oer.hawaii.edu/humannutrition2/open/download?type=pdf"


def download_pdf(url: str, path: str) -> None:
    """Download the PDF into the project folder if it isn't there already."""
    if os.path.exists(path):
        print(f"[INFO] File already exists: {path}")
        return
    print(f"[INFO] Downloading PDF from {url} ...")
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    with open(path, "wb") as f:
        f.write(response.content)
    print(f"[INFO] Saved PDF to {path}")


def text_formatter(text: str) -> str:
    """Light cleanup of page text."""
    return text.replace("\n", " ").strip()


def open_and_read_pdf(path: str) -> list[dict]:
    """Read every page and build the pages_and_texts list of dictionaries."""
    pages_and_texts = []
    with pymupdf.open(path) as doc:
        for page_number, page in enumerate(doc):
            text = text_formatter(page.get_text())
            sentences = [s for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
            pages_and_texts.append({
                "page_number": page_number + 1,
                "page_char_count": len(text),
                "page_word_count": len(text.split()),
                "page_sentence_count": len(sentences),
                "page_token_count": len(text) / 4,  # ~4 characters per token
                "text": text,
            })
    return pages_and_texts

def display_pages_andtext(pages_and_texts:list[dict]):
      for page in pages_and_texts:
            print(f"Page number:     {page['page_number']}")
            print(f"Char count:      {page['page_char_count']}")
            print(f"Word count:      {page['page_word_count']}")
            print(f"Sentence count:  {page['page_sentence_count']}")
            print(f"Token count:     {page['page_token_count']:.0f}")
            print(f"Text:            {page['text']}")
            print("-" * 80)
    


def main():
    download_pdf(PDF_URL, PDF_PATH)
    pages_and_texts = open_and_read_pdf(PDF_PATH)

    #print(f"display pages and texts:")
    #display_pages_andtext(pages_and_texts)

    print(f"[INFO] Total pages: {len(pages_and_texts)}")
    print("\n=== pages_and_texts DataFrame ===")
    display_pages_dataframe(pages_and_texts,rows=1208)
    
    print("\n=== pages_and_texts stats ===")
    display_pages_stats(pages_and_texts)
  
   


if __name__ == "__main__":
    main()
