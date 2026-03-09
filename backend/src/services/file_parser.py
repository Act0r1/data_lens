import io
import logging

import pandas as pd

from src.services.file_detector import detect_encoding, detect_delimiter

logger = logging.getLogger(__name__)


def parse_csv(raw_bytes: bytes) -> pd.DataFrame:
    encoding = detect_encoding(raw_bytes)
    text = raw_bytes.decode(encoding, errors="replace")
    delimiter = detect_delimiter(text)
    logger.info("Parsing CSV: encoding=%s, delimiter=%r", encoding, delimiter)
    return pd.read_csv(io.StringIO(text), sep=delimiter, on_bad_lines="skip")


def parse_excel(raw_bytes: bytes, sheet: int = 0) -> pd.DataFrame:
    logger.info("Parsing Excel sheet %s", sheet)
    return pd.read_excel(io.BytesIO(raw_bytes), sheet_name=sheet, engine="openpyxl")


def parse_file(raw_bytes: bytes, filename: str) -> pd.DataFrame:
    ext = filename.rsplit(".", 1)[-1].lower() if filename else "csv"
    if ext in ("xlsx", "xls"):
        return parse_excel(raw_bytes)
    return parse_csv(raw_bytes)
