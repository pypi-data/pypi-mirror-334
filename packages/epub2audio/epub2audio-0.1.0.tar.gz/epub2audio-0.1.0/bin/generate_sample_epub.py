#!/usr/bin/env -S uv run --script
# /// script
# dependencies = [
#   "ebooklib>=0.18.0",
# ]
# ///
# MISE description="Generate a sample EPUB file"
# MISE alias="generate-sample-epub"
# MISE sources=["generate_sample.py"]
# MISE outputs=["tests/data/sample.epub"]
"""Sample EPUB file for testing."""

import os

from ebooklib import epub

# Create a new EPUB book
book = epub.EpubBook()

# Set metadata
book.set_identifier("id123")
book.set_title("Sample Book")
book.set_language("en")
book.add_author("Test Author")
book.add_metadata("DC", "date", "2025")
book.add_metadata("DC", "publisher", "Test Publisher")
book.add_metadata("DC", "description", "A sample book for testing")

# Create chapters
c1 = epub.EpubHtml(title="Chapter 1", file_name="chap_1.xhtml", lang="en")
c1.content = """
    <h1>Chapter 1: Introduction</h1>
    <p>This is the first chapter of the sample book.</p>
    <p>It contains multiple paragraphs to test text extraction.</p>
"""

c2 = epub.EpubHtml(title="Chapter 2", file_name="chap_2.xhtml", lang="en")
c2.content = """
    <h1>Chapter 2: Content</h1>
    <p>This is the second chapter of the sample book.</p>
    <p>It includes some formatting like <b>bold</b> and <i>italic</i> text.</p>
    <img src="image.jpg" alt="Test image"/>
"""

# Add chapters to book
book.add_item(c1)
book.add_item(c2)

# Create table of contents
book.toc = (
    epub.Link("chap_1.xhtml", "Chapter 1", "chapter1"),
    epub.Link("chap_2.xhtml", "Chapter 2", "chapter2"),
)

# Add navigation files
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# Create spine
book.spine = ["nav", c1, c2]

if not os.path.exists("tests/data"):
    os.makedirs("tests/data")

# Write the EPUB file
epub.write_epub("tests/data/sample.epub", book)
