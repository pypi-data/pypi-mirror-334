import logging
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from pdffaroshuffle.utils import faro_shuffle, separate_doc


def main():
    if len(sys.argv) != 3:
        logging.error("Missing arguments")
        sys.exit(1)

    even_pages_path = Path(sys.argv[1])
    odd_pages_path = Path(sys.argv[2])

    if not even_pages_path.exists() or even_pages_path.is_dir():
        logging.error("The %s file path is not a regular file", sys.argv[1])
        sys.exit(2)

    if not odd_pages_path.exists() or odd_pages_path.is_dir():
        logging.error("The %s file path is not a regular file", sys.argv[2])
        sys.exit(2)

    with TemporaryDirectory() as tempdir:
        working_path = Path(tempdir)
        separate_doc(even_pages_path, working_path)
        separate_doc(odd_pages_path, working_path)

        faro_shuffle(working_path, even_pages_path.stem, odd_pages_path.stem)
