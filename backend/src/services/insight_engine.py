import logging

import numpy as np
import pandas as pd
from scipy import stats

logger = logging.getLogger(__name__)


def find_anomalies(df: pd.DataFrame) -> list[dict]:
    insights = []
    numeric_cols = df.select_dtypes(include=["number"]).columns

    for col in numeric_cols:
        series = df[col].dropna()
        if len(series) < 10:
            continue

        z_scores = np.abs(stats.zscore(series))
        anomaly_count = int((z_scores > 3).sum())
        if anomaly_count > 0:
            insights.append({
                "type": "anomaly",
                "title": f"Аномалии в '{col}'",
                "description": f"Найдено {anomaly_count} аномальных значений (Z-score > 3)",
                "severity": "warning",
                "data": {"column": col, "count": anomaly_count},
            })

    return insights


def find_outliers(df: pd.DataFrame) -> list[dict]:
    insights = []
    numeric_cols = df.select_dtypes(include=["number"]).columns

    for col in numeric_cols:
        series = df[col].dropna()
        if len(series) < 10:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outlier_count = int(((series < lower) | (series > upper)).sum())

        if outlier_count > 0:
            insights.append({
                "type": "outlier",
                "title": f"Выбросы в '{col}'",
                "description": f"{outlier_count} значений за пределами IQR",
                "severity": "info",
                "data": {"column": col, "count": outlier_count, "lower": float(lower), "upper": float(upper)},
            })

    return insights


def find_correlations(df: pd.DataFrame) -> list[dict]:
    insights = []
    numeric_cols = df.select_dtypes(include=["number"]).columns

    if len(numeric_cols) < 2:
        return insights

    corr_matrix = df[numeric_cols].corr(method="pearson")
    for i, col1 in enumerate(numeric_cols):
        for col2 in numeric_cols[i + 1:]:
            r = corr_matrix.loc[col1, col2]
            if abs(r) > 0.7:
                insights.append({
                    "type": "correlation",
                    "title": f"Корреляция: {col1} ↔ {col2}",
                    "description": f"Коэффициент Пирсона: {r:.2f}",
                    "severity": "info",
                    "data": {"col1": col1, "col2": col2, "r": round(float(r), 3)},
                })

    return insights


def find_trends(df: pd.DataFrame) -> list[dict]:
    insights = []
    datetime_cols = df.select_dtypes(include=["datetime64"]).columns
    numeric_cols = df.select_dtypes(include=["number"]).columns

    if len(datetime_cols) == 0 or len(numeric_cols) == 0:
        return insights

    date_col = datetime_cols[0]
    for col in numeric_cols:
        subset = df[[date_col, col]].dropna().sort_values(date_col)
        if len(subset) < 5:
            continue

        x = np.arange(len(subset))
        slope, _, r_value, p_value, _ = stats.linregress(x, subset[col])

        if p_value < 0.05 and abs(r_value) > 0.5:
            direction = "рост" if slope > 0 else "снижение"
            insights.append({
                "type": "trend",
                "title": f"Тренд: {direction} в '{col}'",
                "description": f"R² = {r_value**2:.2f}, наклон = {slope:.4f}",
                "severity": "info",
                "data": {"column": col, "slope": float(slope), "r_squared": round(float(r_value**2), 3)},
            })

    return insights


def run_statistical_analysis(df: pd.DataFrame) -> list[dict]:
    all_insights = []
    all_insights.extend(find_anomalies(df))
    all_insights.extend(find_outliers(df))
    all_insights.extend(find_correlations(df))
    all_insights.extend(find_trends(df))
    logger.info("Statistical analysis found %s insights", len(all_insights))
    return all_insights
