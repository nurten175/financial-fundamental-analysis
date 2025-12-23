"""
Fundamental Financial Analysis

This script performs a basic fundamental analysis using
income statement data provided in CSV format.

Metrics calculated:
- Revenue Growth (%)
- Net Margin (%)
- Operating Margin (%)
- EBITDA Margin (%)

A simple rule-based scoring system is applied to summarize
overall financial performance.
"""

from pathlib import Path
import pandas as pd


# =========================================================
# CONFIG
# =========================================================
# The CSV file is not included in the repository.
# You will be prompted to enter the full file path at runtime.
csv_path = Path(input("Enter full path to income statement CSV: ").strip())

if not csv_path.exists():
    raise FileNotFoundError(f"CSV file not found: {csv_path}")


# =========================================================
# LOAD DATA
# =========================================================
df = pd.read_csv(csv_path)

if "Date" not in df.columns:
    raise ValueError("CSV must contain a 'Date' column.")

# Set Date as index and transpose so years become rows
df = df.set_index("Date")
df_t = df.T


# =========================================================
# CALCULATE FUNDAMENTAL METRICS
# =========================================================
required_columns = [
    "Total Revenue",
    "Net Income",
    "Operating Income",
    "EBITDA",
]

missing = [c for c in required_columns if c not in df_t.columns]
if missing:
    raise ValueError(f"Missing required columns: {missing}")

df_t["Revenue_Growth_%"] = df_t["Total Revenue"].pct_change() * 100
df_t["Net_Margin_%"] = (df_t["Net Income"] / df_t["Total Revenue"]) * 100
df_t["Operating_Margin_%"] = (
    df_t["Operating Income"] / df_t["Total Revenue"]
) * 100
df_t["EBITDA_Margin_%"] = (df_t["EBITDA"] / df_t["Total Revenue"]) * 100


# =========================================================
# SCORING FUNCTIONS
# =========================================================
def score_revenue_growth(x):
    if pd.isna(x):
        return 0
    if x > 5:
        return 10
    elif x > 0:
        return 7
    else:
        return 3


def score_margin(x, high=25, mid=15):
    if pd.isna(x):
        return 0
    if x > high:
        return 10
    elif x > mid:
        return 7
    else:
        return 3


# =========================================================
# APPLY SCORES
# =========================================================
df_t["Growth_Score"] = df_t["Revenue_Growth_%"].apply(score_revenue_growth)
df_t["Net_Margin_Score"] = df_t["Net_Margin_%"].apply(score_margin)
df_t["Operating_Margin_Score"] = df_t["Operating_Margin_%"].apply(
    lambda x: score_margin(x, high=30, mid=20)
)

df_t["Fundamental_Score"] = df_t[
    ["Growth_Score", "Net_Margin_Score", "Operating_Margin_Score"]
].mean()


# =========================================================
# OUTPUT
# =========================================================
print("\n=== FUNDAMENTAL METRICS ===")
print(
    df_t[
        [
            "Total Revenue",
            "Revenue_Growth_%",
            "Net_Margin_%",
            "Operating_Margin_%",
            "EBITDA_Margin_%",
            "Fundamental_Score",
        ]
    ].round(2)
)

print("\n=== SCORE BREAKDOWN ===")
print(
    df_t[
        ["Growth_Score", "Net_Margin_Score", "Operating_Margin_Score"]
    ]
)
