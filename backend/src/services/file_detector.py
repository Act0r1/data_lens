import csv
import logging

import chardet

logger = logging.getLogger(__name__)

COMMON_ENCODINGS = ["utf-8", "cp1251", "windows-1252", "latin-1"]


def detect_encoding(raw_bytes: bytes) -> str:
    result = chardet.detect(raw_bytes[:10000])
    encoding = result.get("encoding", "utf-8")
    confidence = result.get("confidence", 0)
    logger.info("Detected encoding: %s (confidence: %s)", encoding, confidence)

    if confidence < 0.5:
        for enc in COMMON_ENCODINGS:
            try:
                raw_bytes[:5000].decode(enc)
                return enc
            except (UnicodeDecodeError, LookupError):
                continue
    return encoding or "utf-8"


def detect_delimiter(text: str) -> str:
    try:
        dialect = csv.Sniffer().sniff(text[:5000])
        return dialect.delimiter
    except csv.Error:
        if "\t" in text[:1000]:
            return "\t"
        if ";" in text[:1000]:
            return ";"
        return ","
