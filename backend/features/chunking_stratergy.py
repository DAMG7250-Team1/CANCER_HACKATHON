
# features/chunking_strategy.py
import boto3
import os
import re
from typing import List


def markdown_chunking(markdown_text: str, heading_level: int = 2) -> list:
    """Simple markdown chunker based on heading levels."""

    # Define heading pattern (e.g., ## Heading)
    heading_pattern = r"^" + ("#" * heading_level) + r"\s+"
    pattern = re.compile(heading_pattern)

    chunks = []
    current_chunk = []

    for line in markdown_text.splitlines():
        if pattern.match(line) and current_chunk:
            chunks.append("\n".join(current_chunk))
            current_chunk = [line]
        else:
            current_chunk.append(line)

    if current_chunk:
        chunks.append("\n".join(current_chunk))

    return chunks
