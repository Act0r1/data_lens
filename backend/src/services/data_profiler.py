import logging

import pandas as pd

logger = logging.getLogger(__name__)


def profile_dataframe(df: pd.DataFrame) -> dict:
    profile = {"columns": [], "shape": {"rows": len(df), "cols": len(df.columns)}}

    for col in df.columns:
        col_info = {
            "name": str(col),
            "dtype": str(df[col].dtype),
            "null_count": int(df[col].isnull().sum()),
            "null_pct": round(float(df[col].isnull().mean()) * 100, 1),
            "unique_count": int(df[col].nunique()),
        }

        if pd.api.types.is_numeric_dtype(df[col]):
            desc = df[col].describe()
            col_info.update({
                "type": "numeric",
                "min": float(desc.get("min", 0)),
                "max": float(desc.get("max", 0)),
                "mean": round(float(desc.get("mean", 0)), 2),
                "std": round(float(desc.get("std", 0)), 2),
                "median": float(df[col].median()),
            })
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            col_info.update({
                "type": "datetime",
                "min": str(df[col].min()),
                "max": str(df[col].max()),
            })
        else:
            col_info["type"] = "text"
            top = df[col].value_counts().head(5)
            col_info["top_values"] = {str(k): int(v) for k, v in top.items()}

        profile["columns"].append(col_info)

    logger.info("Profiled %s columns, %s rows", len(df.columns), len(df))
    return profile
