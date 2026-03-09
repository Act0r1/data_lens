import logging

logger = logging.getLogger(__name__)

WB_PATTERNS = {
    "артикул поставщика", "артикул wb", "баркод", "бренд",
    "предмет", "размер", "кол-во", "цена со скидкой",
    "возврат", "логистика", "к перечислению", "sku",
    "nmid", "supplierarticle",
}

OZON_PATTERNS = {
    "ozon id", "артикул", "sku", "fbo", "fbs",
    "цена продажи", "комиссия", "последняя миля",
    "обработка", "логистика",
}

C1_PATTERNS = {
    "номенклатура", "контрагент", "дебет", "кредит",
    "количество", "сумма", "организация", "склад",
    "приход", "расход", "счёт",
}

ADS_PATTERNS = {
    "cpc", "cpm", "ctr", "показы", "клики",
    "расход", "конверсия", "impressions", "clicks",
    "campaign", "кампания", "acos", "roas",
}


def detect_domain(columns: list[str]) -> str:
    cols_lower = {c.lower().strip() for c in columns}

    scores = {
        "wb": len(cols_lower & WB_PATTERNS),
        "ozon": len(cols_lower & OZON_PATTERNS),
        "1c": len(cols_lower & C1_PATTERNS),
        "ads": len(cols_lower & ADS_PATTERNS),
    }

    best = max(scores, key=scores.get)
    if scores[best] >= 2:
        logger.info("Detected domain: %s (score: %s)", best, scores[best])
        return best

    logger.info("Domain: generic")
    return "generic"
