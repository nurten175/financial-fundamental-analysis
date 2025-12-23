#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 17:57:17 2025

@author: nurtenerust
"""

import pandas as pd

df = pd.read_csv("/Users/nurtenerust/Desktop/aapl_income_statement.csv")
print(df.head())

# Date sütununu index yap
df = df.set_index("Date")

# Tabloyu çevir (yıllar satır olsun)
df_t = df.T

print(df_t)
# Temel oranlar
df_t["Revenue_Growth_%"] = df_t["Total Revenue"].pct_change() * 100
df_t["Net_Margin_%"] = (df_t["Net Income"] / df_t["Total Revenue"]) * 100
df_t["Operating_Margin_%"] = (df_t["Operating Income"] / df_t["Total Revenue"]) * 100
df_t["EBITDA_Margin_%"] = (df_t["EBITDA"] / df_t["Total Revenue"]) * 100

print(df_t[[
    "Total Revenue",
    "Revenue_Growth_%",
    "Net_Margin_%",
    "Operating_Margin_%",
    "EBITDA_Margin_%"
]])

def score_revenue_growth(x):
    if x > 5:
        return 10
    elif x > 0:
        return 7
    else:
        return 3

def score_margin(x, high=25, mid=15):
    if x > high:
        return 10
    elif x > mid:
        return 7
    else:
        return 3

# Skorlar
df_t["Growth_Score"] = df_t["Revenue_Growth_%"].apply(score_revenue_growth)
df_t["Net_Margin_Score"] = df_t["Net_Margin_%"].apply(score_margin)
df_t["Operating_Margin_Score"] = df_t["Operating_Margin_%"].apply(
    lambda x: score_margin(x, high=30, mid=20)
)

# Final Fundamental Score (ortalama)
df_t["Fundamental_Score"] = df_t[
    ["Growth_Score", "Net_Margin_Score", "Operating_Margin_Score"]
].mean()

print(df_t[[
    "Revenue_Growth_%",
    "Net_Margin_%",
    "Operating_Margin_%",
    "Fundamental_Score"
]])
# Skorları ayrı ayrı görelim
print(df_t[[
    "Growth_Score",
    "Net_Margin_Score",
    "Operating_Margin_Score"
]])

# Fundamental Score'u tekrar hesapla (emin olmak için)
df_t["Fundamental_Score"] = df_t[
    ["Growth_Score", "Net_Margin_Score", "Operating_Margin_Score"]
].mean()

print(df_t[[
    "Revenue_Growth_%",
    "Net_Margin_%",
    "Operating_Margin_%",
    "Fundamental_Score"
]])
