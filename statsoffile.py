"""Helpers to display pages_and_texts as a DataFrame and show its statistics."""

import pandas as pd


def display_pages_dataframe(pages_and_texts: list[dict], rows: int = 1208) -> pd.DataFrame:
    """Show pages_and_texts as a DataFrame (first `rows` rows) and return it."""
    df = pd.DataFrame(pages_and_texts)
    with pd.option_context("display.max_rows", None, "display.max_columns", None,
                           "display.width", 200, "display.max_colwidth", 60):
        print("Total records:", len(pages_and_texts))
        print(df.head(rows))
    return df


def display_pages_stats(pages_and_texts: list[dict]) -> pd.DataFrame:
    """Show summary statistics (count, mean, std, min, max...) of the numeric fields."""
    stats = pd.DataFrame(pages_and_texts).describe().round(2)
    with pd.option_context("display.max_columns", None, "display.width", 200):
        print(stats)
    return stats