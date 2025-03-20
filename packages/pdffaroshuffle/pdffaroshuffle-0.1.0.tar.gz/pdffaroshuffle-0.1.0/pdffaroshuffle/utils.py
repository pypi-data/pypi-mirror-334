"""pdfmix executable."""

import logging
import subprocess
import sys
from pathlib import Path


def separate_doc(doc_path: Path, working_path: Path):
    """Split a document in pages."""

    pattern = f"{doc_path.stem}_%03d{doc_path.suffix}"
    args = ["pdfseparate", str(doc_path), f"{str(working_path)}/{pattern}"]
    process = subprocess.run(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if process.returncode != 0:
        logging.error("Document %s cannot be splitted", doc_path)
        sys.exit(3)


def faro_shuffle(working_dir: Path, stem_even: str, stem_odd: str):
    """Mix the pages to put them in the correct order."""
    even_pages = len(list(working_dir.glob(f"{stem_even}*")))
    odd_pages = len(list(working_dir.glob(f"{stem_odd}*")))

    path_order = []
    for even_page in range(1, even_pages + 1):
        odd_page = odd_pages - (even_page - 1)
        even_page_path = working_dir / f"{stem_even}_{even_page:03d}.pdf"
        odd_page_path = working_dir / f"{stem_odd}_{odd_page:03d}.pdf"
        path_order.extend([even_page_path, odd_page_path])

    args = [
        "pdfunite",
    ]
    args.extend(path_order)
    args.append(f"./{stem_even}_{stem_odd}.pdf")

    process = subprocess.run(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if process.returncode != 0:
        logging.error(
            "Document cannot be united:\n\tSTDOUT: %s\n\tSTDERR: %s",
            process.stdout,
            process.stderr,
        )
        sys.exit(4)
