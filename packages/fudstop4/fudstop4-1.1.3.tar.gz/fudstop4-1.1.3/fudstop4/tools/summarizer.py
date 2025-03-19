# Filename: world_class_summarizer.py

import os
import chardet
import pdfplumber
import docx
from transformers import pipeline

def read_pdf(file_path: str) -> str:
    """
    Extracts text from a PDF file using pdfplumber.

    :param file_path: The absolute path to the PDF file.
    :return: A concatenated string of all text in the PDF.
    """
    text_content = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text_content.append(page_text)
    return "\n".join(text_content)


def read_docx(file_path: str) -> str:
    """
    Extracts text from a DOCX file using python-docx.

    :param file_path: The absolute path to the DOCX file.
    :return: A concatenated string of all text in the DOCX file.
    """
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)


def read_text(file_path: str) -> str:
    """
    Reads and decodes text from a file using chardet to detect encoding.

    :param file_path: The absolute path to the text file.
    :return: Decoded text content.
    """
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding'] or 'utf-8'
    # In rare cases, chardet might detect None, or an invalid encoding - we default to utf-8.
    return raw_data.decode(encoding, errors='replace')


def read_document(file_path: str) -> str:
    """
    Reads the file based on its extension or best guess:
      - PDF -> pdfplumber
      - DOCX -> python-docx
      - Else, attempts to read as text with chardet.

    :param file_path: Absolute path to the file.
    :return: Extracted text.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    extension = os.path.splitext(file_path)[1].lower()

    if extension == '.pdf':
        return read_pdf(file_path)
    elif extension == '.docx':
        return read_docx(file_path)
    else:
        # Try reading as text
        return read_text(file_path)


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> list:
    """
    Splits large text into overlapping chunks so we don't exceed model limits.
    Each chunk is ~chunk_size characters; overlap to maintain context continuity.

    :param text: The full text to split.
    :param chunk_size: The approximate size (in characters) of each chunk.
    :param overlap: The number of overlapping characters between adjacent chunks.
    :return: A list of text chunks.
    """
    chunks = []
    start = 0
    length = len(text)

    while start < length:
        end = min(start + chunk_size, length)
        chunk = text[start:end]
        chunks.append(chunk)

        # Move start pointer with overlap
        start = end - overlap
        if start < 0:
            start = 0

        if end >= length:
            break

    return chunks


def summarize_text(text: str) -> str:
    """
    Summarizes the given text with a pre-trained Hugging Face model.

    :param text: The text to summarize.
    :return: A consolidated summary of the text.
    """
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    # Break up large text to avoid model input length issues
    text_chunks = chunk_text(text, chunk_size=1000, overlap=100)
    partial_summaries = []

    for chunk in text_chunks:
        # Summarize each chunk
        summary_output = summarizer(
            chunk,
            max_length=130,     # Adjust for your desired summary length
            min_length=30,      # Adjust for your desired summary length
            do_sample=False
        )
        partial_summaries.append(summary_output[0]['summary_text'])

    # Join chunk summaries into a single text
    return " ".join(partial_summaries)


def main():
    """
    Main function to run the summarizer.
      1. Prompts for file path
      2. Reads file with robust approach
      3. Summarizes file content
      4. Prints the summary
    """
    print("=== World Class Summarizer ===")
    file_path = input("Enter the absolute path to the document: ").strip()

    try:
        text_data = read_document(file_path)
        if not text_data.strip():
            print("Could not extract any text from the file.")
            return

        summary = summarize_text(text_data)
        print("\n=== SUMMARY ===")
        print(summary)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
