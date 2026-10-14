"""
trade_log_deep_analysis.py
=============================
Deep dive on sector_breadth_trades_v1.csv (the Sector_clean strategy -- now
the MAIN/reverted version, IS 2003-2012, CAGR 25.43%/Sharpe 1.419/604 trades).

Sector_clean is what the strategy trades on, but each trade is re-tagged
here with the finer Sector (raw)/Industry/Industry_clean fields from
instruments_clean.csv purely for ANALYSIS -- to see whether losses/wins
concentrate in specific industries WITHIN a Sector_clean bucket. This is
the evidence needed to answer: "would Industry_clean as a secondary filter
on top of Sector_clean have helped?" -- not a strategy change yet, just
diagnosis.
"""

import os
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
pd.set_option("display.width", 160)
pd.set_option("display.max_rows", 120)

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TRADES_CSV = os.path.join(os.path.dirname(__file__), "sector_breadth_trades_v1.csv")
INSTRUMENTS_CSV = os.path.join(REPO_ROOT, "instruments_clean.csv")


def load_and_enrich():
    trades = pd.read_csv(TRADES_CSV, parse_dates=["Entry_Date", "Exit_Date"])
    trades["Return_Pct"] = (trades["Exit_Price"] / trades["Entry_Price"] - 1.0) * 100.0
    trades["Holding_Days"] = (trades["Exit_Date"] - trades["Entry_Date"]).dt.days
    trades["Win"] = trades["Return_Pct"] > 0

    inst = pd.read_csv(INSTRUMENTS_CSV)[
        ["trading_symbol", "Sector", "Sector_clean", "Industry", "Industry_clean"]
    ].rename(columns={
        "trading_symbol": "Ticker", "Sector": "Sector_raw",
        "Sector_clean": "Sector_clean_tag", "Industry": "Industry_raw",
    })
    trades = trades.merge(inst, on="Ticker", how="left")

    n_unmatched = trades["Sector_clean_tag"].isna().sum()
    mismatch = (trades["Sector"] != trades["Sector_clean_tag"]).sum()
    print(f"Trades: {len(trades)}   Unmatched to instruments_clean.csv: {n_unmatched}   "
          f"Sector(strategy) != Sector_clean(lookup): {mismatch}")
    print(f"Industry_clean coverage among trades: "
          f"{trades['Industry_clean'].notna().mean()*100:.1f}%")
    return trades


def overall_stats(trades, label="ALL TRADES"):
    n = len(trades)
    wins = trades[trades["Win"]]
    losses = trades[~trades["Win"]]
    win_rate = len(wins) / n * 100 if n else np.nan
    avg_win = wins["Return_Pct"].mean() if len(wins) else np.nan
    avg_loss = losses["Return_Pct"].mean() if len(losses) else np.nan
    gross_win = wins["Return_Pct"].sum()
    gross_loss = losses["Return_Pct"].sum()
    profit_factor = abs(gross_win / gross_loss) if gross_loss != 0 else np.nan
    expectancy = trades["Return_Pct"].mean()

    print(f"\n{'='*80}\n{label}  (n={n})\n{'='*80}")
    print(f"  Win rate: {win_rate:.1f}%   Avg win: {avg_win:+.2f}%   Avg loss: {avg_loss:+.2f}%")
    print(f"  Profit factor (sum wins / |sum losses|): {profit_factor:.2f}")
    print(f"  Expectancy (avg return/trade): {expectancy:+.2f}%")
    print(f"  Avg holding days: {trades['Holding_Days'].mean():.1f}  "
          f"(winners: {wins['Holding_Days'].mean():.1f}, losers: {losses['Holding_Days'].mean():.1f})")


def breakdown_by(trades, col, label, min_n=3):
    g = trades.groupby(col, dropna=True)
    tbl = g.agg(
        N=("Return_Pct", "count"),
        WinRate=("Win", "mean"),
        AvgRet=("Return_Pct", "mean"),
        TotalRet=("Return_Pct", "sum"),
        AvgMAE=("MAE_Pct", "mean"),
        AvgHold=("Holding_Days", "mean"),
    ).sort_values("TotalRet")
    tbl["WinRate"] = (tbl["WinRate"] * 100).round(1)
    tbl = tbl.round(2)

    print(f"\n{'='*80}\nBREAKDOWN BY {label}  (bucket total P&L contribution, worst->best)\n{'='*80}")
    print(tbl.to_string())

    thin = tbl[tbl["N"] < min_n]
    if len(thin):
        print(f"\n  ({len(thin)} buckets have < {min_n} trades -- directional only, not statistically reliable)")
    return tbl


def nested_industry_within_sector(trades, min_n=3):
    print(f"\n{'='*90}\nWORST Industry_clean GROUPS WITHIN EACH Sector_clean BUCKET\n{'='*90}")
    for sector, sub in trades.groupby("Sector"):
        ind = sub.groupby("Industry_clean", dropna=True).agg(
            N=("Return_Pct", "count"), TotalRet=("Return_Pct", "sum"),
            AvgRet=("Return_Pct", "mean"), WinRate=("Win", "mean"),
        ).sort_values("TotalRet")
        ind["WinRate"] = (ind["WinRate"] * 100).round(1)
        ind = ind.round(2)
        n_untagged = sub["Industry_clean"].isna().sum()
        print(f"\n  -- {sector} -- (sector total: {sub['Return_Pct'].sum():+.1f}%, "
              f"{len(sub)} trades, {n_untagged} untagged)")
        worst = ind[ind["N"] >= min_n].head(3)
        best = ind[ind["N"] >= min_n].tail(3)
        if len(worst):
            print(f"    Worst industries (>= {min_n} trades):")
            print("    " + worst.to_string().replace("\n", "\n    "))
        if len(best) and not best.index.equals(worst.index):
            print(f"    Best industries (>= {min_n} trades):")
            print("    " + best.to_string().replace("\n", "\n    "))


def worst_trades(trades, n=20):
    print(f"\n{'='*90}\nWORST {n} INDIVIDUAL TRADES\n{'='*90}")
    cols = ["Ticker", "Sector", "Industry_clean", "Entry_Date", "Exit_Date",
            "Return_Pct", "Exit_Reason", "MAE_Pct", "Holding_Days"]
    worst = trades.sort_values("Return_Pct").head(n)[cols]
    print(worst.to_string(index=False))

    print(f"\n  Sector distribution of the {n} worst trades:")
    print(worst["Sector"].value_counts().to_string())
    print(f"\n  Industry_clean distribution of the {n} worst trades:")
    print(worst["Industry_clean"].value_counts().to_string())


def what_if_filter_worst_industries(trades, n_exclude_list=(3, 5, 8)):
    """Naive simulation: if we had refused to enter trades in the N
    worst-performing (by total P&L, >=3-trade) Industry_clean groups,
    identified WITH FULL HINDSIGHT on this exact sample, how much would
    aggregate trade P&L have improved? This is NOT a valid ex-ante filter
    (it's fit on the same trades being scored -- pure hindsight/in-sample
    bias) -- it only answers "is there enough concentration of losses in a
    few industries to make an Industry_clean filter worth designing
    properly," not "here is a filter to deploy."
    """
    print(f"\n{'='*90}\nHINDSIGHT CHECK: would excluding the worst Industry_clean groups have helped?\n"
          f"(fit on this same sample -- NOT a valid filter, just a concentration check)\n{'='*90}")
    ind_stats = trades.groupby("Industry_clean", dropna=True).agg(
        N=("Return_Pct", "count"), TotalRet=("Return_Pct", "sum")
    )
    ind_stats = ind_stats[ind_stats["N"] >= 3].sort_values("TotalRet")

    base_total = trades["Return_Pct"].sum()
    base_n = len(trades)
    print(f"  Baseline: {base_n} trades, total return sum {base_total:+.1f}%, "
          f"avg/trade {base_total/base_n:+.2f}%")

    for n_exclude in n_exclude_list:
        worst_industries = set(ind_stats.head(n_exclude).index)
        kept = trades[~trades["Industry_clean"].isin(worst_industries)]
        excluded = trades[trades["Industry_clean"].isin(worst_industries)]
        print(f"\n  Exclude worst {n_exclude} industries {sorted(worst_industries)}:")
        print(f"    Removed {len(excluded)} trades, total return of removed: {excluded['Return_Pct'].sum():+.1f}%")
        print(f"    Remaining {len(kept)} trades, total return sum {kept['Return_Pct'].sum():+.1f}%, "
              f"avg/trade {kept['Return_Pct'].sum()/len(kept):+.2f}%  "
              f"(vs baseline avg/trade {base_total/base_n:+.2f}%)")


def main():
    trades = load_and_enrich()
    overall_stats(trades, "ALL TRADES (Sector_clean strategy)")

    losses = trades[~trades["Win"]]
    wins = trades[trades["Win"]]
    overall_stats(losses, "LOSING TRADES ONLY")
    overall_stats(wins, "WINNING TRADES ONLY")

    breakdown_by(trades, "Exit_Reason", "EXIT REASON")
    breakdown_by(trades, "Sector", "SECTOR_CLEAN (strategy's own tag)")
    breakdown_by(trades, "Sector_raw", "SECTOR (raw, 80-category field)", min_n=3)
    breakdown_by(trades, "Industry_clean", "INDUSTRY_CLEAN (202-category field)", min_n=3)
    breakdown_by(trades, "Industry_raw", "INDUSTRY (raw, 138-category field, ~45% coverage)", min_n=3)

    nested_industry_within_sector(trades)
    worst_trades(trades, n=20)
    what_if_filter_worst_industries(trades)

    out = os.path.join(os.path.dirname(__file__), "sector_breadth_trades_v1_enriched.csv")
    trades.to_csv(out, index=False)
    print(f"\nSaved enriched trade log (with Sector_raw/Industry/Industry_clean tags) to {out}")


if __name__ == "__main__":
    main()
