"""TikTok Creator Analytics — verified Overview analysis.

Reads the TikTok Studio export for Nov 16-22, 2026 (retrieved Nov 24, 2026)
and computes weekly totals, the Nov 16-18 baseline, and the Nov 19-20 spike.
All numbers printed here trace to data/overview_2026-11-16_to_2026-11-22.csv.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

BASE = Path(__file__).resolve().parent
DATA = BASE / "data" / "overview_2026-11-16_to_2026-11-22.csv"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)

# TikTok Studio export uses a BOM and quoted fields.
df = pd.read_csv(DATA, encoding="utf-8-sig")
for col in ["Video Views", "Profile Views", "Likes", "Comments", "Shares"]:
    df[col] = pd.to_numeric(df[col])

total_views = int(df["Video Views"].sum())
total_profile_views = int(df["Profile Views"].sum())
total_likes = int(df["Likes"].sum())
total_comments = int(df["Comments"].sum())
total_shares = int(df["Shares"].sum())
avg_daily_views = total_views / len(df)

baseline = df[df["Date"].isin(["November 16", "November 17", "November 18"])]
baseline_avg = baseline["Video Views"].mean()

nov19 = int(df.loc[df["Date"] == "November 19", "Video Views"].iloc[0])
nov20 = int(df.loc[df["Date"] == "November 20", "Video Views"].iloc[0])
spike_total = nov19 + nov20
spike_pct_of_week = spike_total / total_views * 100
nov19_multiple = nov19 / baseline_avg
nov20_multiple = nov20 / baseline_avg

print("TikTok Studio Overview — Nov 16-22, 2026 (retrieved Nov 24, 2026)")
print(f"Days in export: {len(df)}")
print(f"Total video views: {total_views:,}")
print(f"Total profile views: {total_profile_views:,}")
print(f"Total likes: {total_likes:,}")
print(f"Total comments: {total_comments:,}")
print(f"Total shares: {total_shares:,}")
print(f"Average daily video views: {avg_daily_views:,.1f}")
print(f"Baseline avg daily views, Nov 16-18: {baseline_avg:,.1f}")
print(f"Nov 19 views: {nov19:,} ({nov19_multiple:.2f}x baseline)")
print(f"Nov 20 views: {nov20:,} ({nov20_multiple:.2f}x baseline, peak day)")
print(f"Nov 19+20 combined: {spike_total:,} ({spike_pct_of_week:.2f}% of the week's views)")

# Chart: daily views, spike days highlighted.
colors = ["#d9534f" if d in ("November 19", "November 20") else "#89949e" for d in df["Date"]]
labels = [d.replace("November ", "Nov ") for d in df["Date"]]
fig, ax = plt.subplots(figsize=(8, 3.65), layout="constrained")
bars = ax.bar(labels, df["Video Views"], color=colors)
ax.bar_label(bars, labels=[f"{v:,}" for v in df["Video Views"]], padding=4, fontsize=8)
ax.set_ylim(0, df["Video Views"].max() * 1.18)
ax.set_title("Daily Video Views — Nov 16-22, 2026", loc="left")
ax.set_ylabel("Video views")
ax.spines[["top", "right"]].set_visible(False)
fig.savefig(OUT / "daily_views.png", dpi=160)
print(f"Chart written to: {OUT / 'daily_views.png'}")
