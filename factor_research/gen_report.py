"""gen_report.py -- builds NEW_STRATEGY_IDEAS.md from results/*.csv (tables are generated, never hand-typed)."""
import os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
R = lambda f: pd.read_csv(os.path.join(HERE, 'results', f))

# ───────────── data ─────────────
scan = {u: pd.read_csv(os.path.join(HERE, 'results', f'scan_{u}.csv'), index_col=0)
        for u in ('U1_liquid1000', 'U2_live_trend', 'U3_top300')}
s6 = R('stage6_universe_scan.csv')
ALL = pd.concat([d.reset_index().assign(universe=u) for u, d in scan.items()] + [s6], ignore_index=True)
packs_ic, packs_bk = R('stage11_packs_ic.csv'), R('stage11_packs_books.csv')
ovl = R('stage12_concentration_overlays.csv')
brk = pd.read_csv(os.path.join(HERE, 'results', 'stage5_breakout_events.csv'), index_col=0)
sec_ic = pd.read_csv(os.path.join(HERE, 'results', 'stage7_sector_ic.csv'), index_col=0)
sec_bk = R('stage7_sector_books.csv')
tim = R('stage8_timing.csv')
ast_ic = pd.read_csv(os.path.join(HERE, 'results', 'stage9_asset_ic.csv'), index_col=0)
ast_bk = R('stage9_asset_books.csv')
vix = R('stage9_vix_study.csv')
fir = R('stage9_factor_index_regimes.csv')
corr = pd.read_csv(os.path.join(HERE, 'results', 'stage13_book_correlations.csv'), index_col=0)
etf = R('etf_liquid_list.csv')
sect_stock = R('stage10_sector_same_subset.csv')


def f(x, d=3, pct=False):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return '–'
    return f'{x*100:.1f}%' if pct else f'{x:.{d}f}'


def md(rows, header):
    out = ['| ' + ' | '.join(header) + ' |', '|' + '|'.join(['---'] * len(header)) + '|']
    out += ['| ' + ' | '.join(str(c) for c in r) + ' |' for r in rows]
    return '\n'.join(out)


UN_LABEL = {'U1_liquid1000': 'Liquid-1000', 'U2_live_trend': 'Liquid-1000 ∩ >SMA200', 'U3_top300': 'Top-300',
            'U4_top250': 'Top-250 (csm_absolute universe)', 'U5_highvol_tercile': 'High-vol tercile',
            'U6_lowvol_tercile': 'Low-vol tercile', 'U7_midsmall_301_1000': 'Mid/small (rank 301-1000)'}


def acc_table(factor, unis=('U1_liquid1000', 'U4_top250', 'U7_midsmall_301_1000', 'U3_top300')):
    rows = []
    for u in unis:
        d = ALL[(ALL.universe == u) & (ALL['factor'] == factor)]
        if d.empty:
            continue
        r = d.iloc[0]
        rows.append([UN_LABEL[u], f(r.ic_1), f(r.ic_3), f(r.ic_6), f(r.ic_12), f(r.icir_3, 2), f(r.hit_3, pct=True), f(r.t_3, 1),
                     f(r.ic_disc_3), f(r.ic_hold_3), int(r.peak_h_ic)])
    return md(rows, ['Universe', 'IC 1m', 'IC 3m', 'IC 6m', 'IC 12m', 'ICIR 3m', 'Hit 3m', 't (NW)', 'IC ≤2014', 'IC ≥2015', 'Peak h (m)'])


def pack_table(pack):
    rows = []
    for u in ('U1_liquid1000', 'U4_top250', 'U7_midsmall_301_1000', 'U3_top300'):
        d = packs_ic[(packs_ic.universe == u) & (packs_ic.factor == pack)]
        if d.empty:
            continue
        r = d.iloc[0]
        rows.append([UN_LABEL[u], f(r.ic_1), f(r.ic_3), f(r.ic_6), f(r.ic_12), f(r.icir_3, 2), f(r.hit_3, pct=True), f(r.t_3, 1),
                     f(r.ic_disc_3), f(r.ic_hold_3), int(r.peak_h_ic), f(r.corr_elendel, 2), f(r.inc_ic_3)])
    return md(rows, ['Universe', 'IC 1m', 'IC 3m', 'IC 6m', 'IC 12m', 'ICIR 3m', 'Hit 3m', 't (NW)', 'IC ≤2014', 'IC ≥2015', 'Peak h', 'corr→Elendel', 'incr. IC 3m'])


def book_table(pack, with_ref=True):
    rows = []
    for u in ('U1_liquid1000', 'U4_top250', 'U7_midsmall_301_1000'):
        for nm in ([('LIVE_elendel', 'Elendel signal (reference)')] if with_ref else []) + [(pack, 'this idea')]:
            for gate in ('none', 'sma200_gate50'):
                d = packs_bk[(packs_bk.universe == u) & (packs_bk.pack == nm[0]) & (packs_bk.gate == gate)]
                if d.empty:
                    continue
                r = d.iloc[0]
                rows.append([UN_LABEL[u], nm[1], 'plain' if gate == 'none' else 'SMA200 gate (50% in bear)', f(r.cagr, pct=True), f(r.sharpe, 2),
                             f(r.maxdd, pct=True), f(r.calmar, 2), f(r.sharpe_hold, 2), f(r.turnover, 2), f(r.corr_elen_book, 2)])
    return md(rows, ['Universe', 'Signal', 'Overlay', 'CAGR', 'Sharpe', 'Max DD', 'Calmar', 'Sharpe ≥2015', 'Turnover/mo', 'corr→Elendel book'])


def overlay_table(universe='U1_liquid1000'):
    rows = []
    names = [('LIVE_elendel', 'Elendel signal'), ('P4_resid+persist', 'P4 residual+persistence'), ('P6_tight+persist', 'P6 tight-range trend'),
             ('csm_abs_score', 'csm_absolute score'), ('P2_low_risk', 'P2 low-risk sleeve')]
    for key, lab in names:
        for ov in ('plain', 'sma200_gate50', 'voltarget20', 'gate+voltarget'):
            d = ovl[(ovl.universe == universe) & (ovl.pack == key) & (ovl.n == 15) & (ovl.overlay == ov)]
            if d.empty:
                continue
            r = d.iloc[0]
            rows.append([lab, ov, f(r.cagr, pct=True), f(r.vol, pct=True), f(r.sharpe, 2), f(r.maxdd, pct=True), f(r.calmar, 2), f(r.sharpe_hold, 2), f(r.maxdd_hold, pct=True)])
    return md(rows, ['Signal (top-15)', 'Overlay', 'CAGR', 'Vol', 'Sharpe', 'Max DD', 'Calmar', 'Sharpe ≥2015', 'Max DD ≥2015'])


def conc_table(universe, packkey):
    rows = []
    for ov in ('plain', 'gate+voltarget'):
        r = [ov]
        for n in (8, 10, 15, 25):
            d = ovl[(ovl.universe == universe) & (ovl.pack == packkey) & (ovl.n == n) & (ovl.overlay == ov)].iloc[0]
            r.append(f'{d.cagr*100:.1f}% / {d.maxdd*100:.0f}% / {d.sharpe:.2f}')
        rows.append(r)
    return md(rows, ['Overlay', 'Top-8', 'Top-10', 'Top-15', 'Top-25'])


def unis_table(factors):
    rows = []
    for fa in factors:
        r = [fa]
        for u in ('U4_top250', 'U1_liquid1000', 'U7_midsmall_301_1000', 'U5_highvol_tercile', 'U6_lowvol_tercile'):
            d = ALL[(ALL.universe == u) & (ALL['factor'] == fa)]
            r.append(f(d.iloc[0].ic_3) if not d.empty else '–')
        rows.append(r)
    return md(rows, ['Factor (IC 3m)', 'Top-250', 'Liquid-1000', 'Mid/small', 'High-vol tercile', 'Low-vol tercile'])


def brk_row(name, label):
    r = brk.loc[name]
    return [label, int(r.n), f(r.ex20, pct=True), f(r.ex60, pct=True), f(r.t20, 1), f(r.t60, 1), f(r.hit_vs_uni20, pct=True), f(r.hit_vs_uni60, pct=True), f(r.ex60_disc, pct=True), f(r.ex60_hold, pct=True)]


# ───────────── document ─────────────
L = []
A = L.append
A('# New strategy ideas — factors, accuracy, pros & cons')
A('')
A('_Generated 2026-10-05 from `factor_research/` (all tables are produced by `gen_report.py` from `results/*.csv`; re-run the stage scripts to refresh)._')
A('')
A('**Purpose.** Shortlist single factors / pairs of factors that can anchor *new* strategies, with measured predictive accuracy. '
  'Following your note, overlap with the existing momentum books is **not** treated as disqualifying — it can be reduced through universe, sizing, '
  'stops and overlays — but it is reported for every idea so you know what you are buying.')
A('')
A('## Bottom line')
A('')
A('* **Best factor pairs to build new strategies on** (all positive in both the ≤2014 and ≥2015 halves): '
  '(1) `tight_close_15 + q5_126` — best book Sharpe, mid/small caps; (2) `mom_resid_12_1 + q5_126` — best upgrade of existing books, ~⅓ less turnover; '
  '(3) `lowvol_126 + low_ulcer_252` — lowest drawdown, works in bear markets, low CAGR; (4) `intra_over_252 + low_ulcer_252` — most distinct signal, large caps only.')
A('* **Event/breakout idea**: 52-week-high or Donchian breakouts only pay when gated by top-quartile relative strength + trend template; volume confirmation did not help.')
A('* **"Volatile / high-CAGR" ideas**: selecting *for* volatility has negative IC. What moved drawdowns most was an overlay — SMA200 gate + 20% volatility target cut max drawdown from −58…−74% to −37…−41% in the stripped books at a 0-4 point CAGR cost.')
A('* **Honest limitation**: no factor-based stock idea is uncorrelated with your momentum books (book correlation 0.6-0.9). The only genuinely decorrelated building blocks found are **asset-class rotation with gold (0.26-0.49)** and gold itself (≈ −0.15). Index timing, sector rotation and seasonality did not hold up as stand-alone strategies.')
A('')
A('## 0. How to read the numbers')
A('')
A('* **IC** = monthly cross-sectional Spearman rank correlation of the signal (taken at month-end close) with the forward return from the **next day\'s close** over *h* months (same convention as `calculate_ic` in your runners, plus a 1-day execution lag). '
  '**ICIR** = mean(IC)/std(IC) over months. **Hit** = % of months with IC>0. **t (NW)** = Newey-West t-stat (lag h−1; monthly samples of multi-month returns overlap). '
  '**Peak h** = horizon with the highest IC (the "horizon period" / factor-decay peak).')
A('* Rule of thumb used here: |t|≥3 and the same sign in both halves (**≤2014 discovery**, **≥2015 holdout**). ~120 factors were tested, so |t|<3 is treated as noise.')
A('* **Books** = simplified long-only top-15, equal weight, monthly rebalance, 0.3% one-way cost, **no stops / regime scaling / Crash Guard**. They exist only to compare ideas against each other and against the Elendel signal run through the *same* engine — '
  'their absolute drawdowns (−55% to −70%) are far worse than your live books because the live risk machinery is deliberately absent. "SMA200 gate" = 50% exposure (rest in 6% cash) when the equal-weight market index is below its 200-day average.')
A('* **Universes**: Liquid-1000 = price>₹20, top-1000 by 63d median traded value, circuit ≤5/63d (~700 names avg); Top-250 = csm_absolute\'s universe size; Mid/small = rank 301-1000; vol terciles are within Liquid-1000.')
A('* **Data limits**: only ~2% of stock files are delisted names (**survivorship bias** flatters long-only price signals, low-vol and smooth-trend screens in particular); index data are price indices (no dividends); '
  'ETF/index results are monthly and use ≤19 years of history, so t-stats are lower than for the ~700-stock cross-section.')
A('')

# ---------- executive table ----------
def bk(pack, u, gate='none', col='sharpe'):
    d = packs_bk[(packs_bk.universe == u) & (packs_bk.pack == pack) & (packs_bk.gate == gate)]
    return d.iloc[0][col] if not d.empty else np.nan

A('## 1. Ranked summary')
A('')
exec_rows = [
    ['**I1** Tight-range trend', 'tight_close_15 + q5_126', f(packs_ic[(packs_ic.universe=="U7_midsmall_301_1000")&(packs_ic.factor=="P6_tight_range_trend")].iloc[0].icir_3,2)+' (mid/small)',
     f'{f(bk("P6_tight_range_trend","U7_midsmall_301_1000"),2)} / {f(bk("P6_tight_range_trend","U7_midsmall_301_1000","sma200_gate50"),2)}', f(bk('P6_tight_range_trend','U7_midsmall_301_1000','none','corr_elen_book'),2), '**A** – best new risk-adjusted book, highest turnover'],
    ['**I2** Residual momentum + persistence', 'mom_resid_12_1 + q5_126', f(packs_ic[(packs_ic.universe=="U1_liquid1000")&(packs_ic.factor=="P4_residual_plus_persistence")].iloc[0].icir_3,2)+' (liquid)',
     f'{f(bk("P4_residual_plus_persistence","U1_liquid1000"),2)} / {f(bk("P4_residual_plus_persistence","U1_liquid1000","sma200_gate50"),2)}', f(bk('P4_residual_plus_persistence','U1_liquid1000','none','corr_elen_book'),2), '**A** as an upgrade of existing books; high overlap'],
    ['**I3** Low-risk sleeve', 'lowvol_126 + low_ulcer_252', f(packs_ic[(packs_ic.universe=="U1_liquid1000")&(packs_ic.factor=="P2_low_risk_sleeve")].iloc[0].icir_3,2)+' (liquid)',
     f'{f(bk("P2_low_risk_sleeve","U1_liquid1000"),2)} / {f(bk("P2_low_risk_sleeve","U1_liquid1000","sma200_gate50"),2)}', f(bk('P2_low_risk_sleeve','U1_liquid1000','none','corr_elen_book'),2), '**A** for drawdown control / diversification, low CAGR'],
    ['**I4** Quality-intraday trend (large-cap)', 'intra_over_252 + low_ulcer_252', f(packs_ic[(packs_ic.universe=="U4_top250")&(packs_ic.factor=="P1_quality_intraday_trend")].iloc[0].icir_3,2)+' (top-250)',
     f'{f(bk("P1_quality_intraday_trend","U4_top250"),2)} / {f(bk("P1_quality_intraday_trend","U4_top250","sma200_gate50"),2)}', f(bk('P1_quality_intraday_trend','U4_top250','none','corr_elen_book'),2), '**B+** – most distinct signal; large-cap only'],
    ['**I5** csm_absolute-style Sharpe momentum + overlays', 'csm_abs_dual_sharpe (+ gate + vol-target)', f(packs_ic[(packs_ic.universe=="U1_liquid1000")&(packs_ic.factor=="csm_absolute_score")].iloc[0].icir_3,2)+' (liquid)',
     f'{f(bk("csm_absolute_score","U1_liquid1000"),2)} / {f(bk("csm_absolute_score","U1_liquid1000","sma200_gate50"),2)}', f(bk('csm_absolute_score','U1_liquid1000','none','corr_elen_book'),2), '**B** – signal is good, edge of live book is in its overlays'],
    ['**I6** RS-gated breakout v3', '52w-high / Donchian + RS top-25% + trend template', '(event study)', '–', '–', '**B+** – edge is the filter, not the breakout'],
    ['**I7** Anchor-aware long high', 'hi_3y + low_pain_126', f(packs_ic[(packs_ic.universe=="U1_liquid1000")&(packs_ic.factor=="P5_long_anchor_painaware")].iloc[0].icir_3,2)+' (liquid)',
     f'{f(bk("P5_long_anchor_painaware","U1_liquid1000"),2)} / {f(bk("P5_long_anchor_painaware","U1_liquid1000","sma200_gate50"),2)}', f(bk('P5_long_anchor_painaware','U1_liquid1000','none','corr_elen_book'),2), '**C** – high IC, weak book (IC/return disconnect)'],
    ['**X1** Asset-class dual momentum', 'Nifty/Midcap/Smallcap/Gold/cash, 3m momentum or 252d-high', 'N=4 → IC t≤1.8 (1-3m)', 'see §4.1', 'see §6', '**A** for diversification (gold sleeve)'],
    ['**X2** Factor-index regime switch', 'Low-Vol index vs Momentum index by market state', 'hit-rate based', 'see §4.3', '–', '**B** overlay'],
    ['**X3** VIX-spike contrarian re-entry', 'India VIX 2y percentile', 'ts-IC +0.14 (1m)', 'see §3.2', '–', '**B** (39 spike months only)'],
    ['**X4** Sector rotation', '19 sector indices, q5/52w-high/Sharpe', f'ICIR ≈0.2', 'see §4.2', '~0.7', '**C** – weak standalone'],
    ['**X5** Breadth/trend index timing', '% stocks >SMA200, SMA200, VIX, vol', 'bal. acc. 0.50–0.57', 'see §4.4', '–', '**C** as strategy / **B** as overlay'],
    ['**S1** 1-month seasonality tilt', 'same-month 5y mean', 'IC 1m 0.024 (t 4.6)', '–', '–', '**D** – tiny, 80% turnover'],
]
A(md(exec_rows, ['Idea', 'Factors', 'ICIR 3m (best universe)', 'Top-15 book Sharpe plain / gated', 'corr→Elendel book', 'Verdict']))
A('')
A('_Priority key: A = build next; B = worthwhile with design work; C = weak/overlay only; D = skip. Sharpe is net of 0.3% one-way costs vs 6% cash._')
A('')

# ---------- stock ideas ----------
A('## 2. Stock-selection ideas (single factors and factor pairs)')
A('')

A('### I1. Tight-range trend  —  `tight_close_15` + `q5_126`')
A('')
A('**Idea.** Buy names that trend persistently (share of last 126d above SMA50) *and* whose last 15 closes are unusually tight — a quantified "base tightness" in the spirit of VCP/Minervini, but ranked cross-sectionally rather than as a pattern-match.')
A('')
A('* `tight_close_15` = −(std of last 15 closes / their mean). `q5_126` = fraction of last 126 days with close > SMA50 (live Elendel leg).')
A('')
A('**Single factor `tight_close_15` (alone):**')
A('')
A(acc_table('tight_close_15'))
A('')
A('Note the signal is *fast* (month-to-month rank autocorrelation only 0.26) and near-orthogonal to Elendel (corr ≈ 0.00, incremental IC +0.045): its information is short-horizon — IC 1m ≈ IC 3m ≈ 0.04 — so it works as an entry-timing/ranking add-on to a persistent trend signal rather than as a stand-alone hold.')
A('')
A('**Pair (z-score sum):**')
A('')
A(pack_table('P6_tight_range_trend'))
A('')
A('**Top-15 book vs the Elendel signal in the same engine:**')
A('')
A(book_table('P6_tight_range_trend'))
A('')
A('**Pros**')
A('* Best risk-adjusted book of the new packs: ties persistence-alone in Liquid-1000 (Sharpe 0.95) and beats it in mid/small (1.12 vs 1.00; gated 1.26). In Liquid-1000 and mid/small it also holds up in the ≥2015 holdout (Sharpe 0.80–0.93 vs Elendel 0.76–0.86); **in the Top-250 it does not** (holdout Sharpe 0.41–0.42 vs Elendel 0.66–0.68).')
A('* The tightness leg is genuinely distinct information (corr≈0 with Elendel) and has a natural stop location (below the base).')
A('* Strongest IC in the mid/small universe (ICIR 0.92, t 11); 1-month IC is strong, so it also helps entry timing.')
A('**Cons / risks**')
A('* **Turnover 0.6–0.7 of the book per month** (vs 0.4–0.5 for persistence alone): the edge is partly eaten by costs/slippage in small names — the book numbers already include 0.3% one-way.')
A('* Book return correlation with Elendel is still 0.83–0.89 (the persistence leg dominates). Needs universe/stop/sizing differences to be a different strategy.')
A('* In the Top-250 universe it does *not* beat persistence alone (IC 3m 0.075 vs 0.074; Sharpe 0.62 vs 0.64) — mid/small is where it adds value.')
A('* Tight closes in illiquid names can be an artefact of thin trading.')
A('**Implementation notes.** Mid/small universe (rank 301-1000), monthly rank + weekly re-check of tightness; initial stop just under the 15-day low; consider requiring tightness to *persist* (two consecutive month-ends) to cut turnover.')
A('')

A('### I2. Residual momentum + persistence  —  `mom_resid_12_1` + `q5_126`')
A('')
A('**Idea.** Rank on the stock-specific part of 12-1 momentum (daily return minus beta × equal-weight market, summed over t−12…t−1) together with trend persistence. Strips out market-beta-driven winners.')
A('')
A('**Single factor `mom_resid_12_1`:**')
A('')
A(acc_table('mom_resid_12_1'))
A('')
A('**Pair:**')
A('')
A(pack_table('P4_residual_plus_persistence'))
A('')
A('**Top-15 book vs the Elendel signal in the same engine:**')
A('')
A(book_table('P4_residual_plus_persistence'))
A('')
A('**Pros**')
A('* Improves on Elendel in book terms in Liquid-1000 (CAGR 31.5% vs 26.2%, Sharpe 0.84 vs 0.74) and Top-250 (27.9% vs 21.9%, Sharpe 0.80 vs 0.65), with **~34% lower turnover** (0.37 vs 0.56 in Liquid-1000); in mid/small it is roughly level (CAGR 33.4% vs 34.0%, Sharpe 0.89 vs 0.94) but has the second-best ICIR among pairs there (0.84, t 9.5) and lower turnover.')
A('* Hit rate of IC>0 ≈ 80-83% across universes (among the highest of the candidates).')
A('**Cons / risks**')
A('* Correlation with the Elendel book ≈ 0.86–0.90: this is an *upgrade* to existing momentum books more than a new return stream. Residual momentum is already one of your live strategies.')
A('* ≥2015 holdout Sharpe (0.77 liquid-1000) is no better than Elendel\'s (0.77): the in-sample improvement is mostly in ≤2014.')
A('* Needs a stable beta estimate (252d); beta uses an equal-weight market proxy, not Nifty.')
A('')

A('### I3. Low-risk sleeve  —  `lowvol_126` + `low_ulcer_252`')
A('')
A('**Idea.** Own the calmest uptrending names: lowest 126d volatility and lowest ulcer index (RMS drawdown from trailing 252d peak). A defensive stock sleeve with very low turnover.')
A('')
A('**Single factors:**')
A('')
A('`lowvol_126`'); A('')
A(acc_table('lowvol_126')); A('')
A('`low_ulcer_252`'); A('')
A(acc_table('low_ulcer_252')); A('')
A('**Pair:**'); A('')
A(pack_table('P2_low_risk_sleeve')); A('')
A('**Top-15 book vs the Elendel signal in the same engine:**'); A('')
A(book_table('P2_low_risk_sleeve')); A('')
A('**Pros**')
A('* **Lowest drawdown of any stock idea**: Liquid-1000 plain −37% (vs −67% Elendel); with the SMA200 gate −26%; max DD since 2015 only −16% to −23% in Liquid-1000/Top-250/Top-300 (−33% plain, −16% gated in mid/small).')
A('* Turnover 0.16-0.24 of the book per month (rank autocorrelation 0.95-0.99) → cheap to run.')
A('* Works in every universe and keeps positive IC in bear months (IC 3m ≈ +0.07 to +0.08 in market-below-SMA200 months). Orthogonal to Elendel at factor level (lowvol corr −0.02, incremental IC +0.065).')
A('* Low-vol factor *index* beats the Nifty 500 by ~1.6%/month in drawdowns >10% (§4.3), corroborating the regime behaviour.')
A('**Cons / risks**')
A('* **CAGR only 16-19%** and Sharpe ≈0.6–0.9: rank IC is high but the top-quintile *mean* excess is negative (the edge is win-rate/risk, not return) — IC overstates its value for a return-seeking book.')
A('* Weakest holdout (Sharpe ≥2015 0.39–0.68): low-vol lagged during the 2015-2024 small/mid-cap momentum run.')
A('* Book correlation to Elendel still 0.64–0.75; to Nifty 500 0.76 (it is long equity).')
A('* Survivorship bias flatters low-vol screens the most (delisted names were usually volatile).')
A('')

A('### I4. Quality-intraday trend (large caps)  —  `intra_over_252` + `low_ulcer_252`')
A('')
A('**Idea.** `intra_over_252` = Σ(log close/open) − Σ(log open/prev close) over 252d, daily legs clipped ±15%: stocks whose trend is built **during the session** rather than by overnight gaps. Overnight drift is a *negative* predictor (t −3.2 to −5.1), intraday drift positive. '
  'Paired with low ulcer index for smoothness.')
A('')
A('**Single factor `intra_over_252`:**'); A('')
A(acc_table('intra_over_252')); A('')
A('**Pair:**'); A('')
A(pack_table('P1_quality_intraday_trend')); A('')
A('**Top-15 book vs the Elendel signal in the same engine:**'); A('')
A(book_table('P1_quality_intraday_trend')); A('')
A('**Pros**')
A('* The most *distinct* positive-IC signal found (corr→Elendel 0.31 single / 0.46–0.50 pair) and **strongest in large caps** (IC 3m 0.080 in Top-250, t 5.4 in Top-300) where plain momentum is weakest (IC 3m 0.044 for 12-1 in Top-250).')
A('* Low turnover (0.22) and decent Top-250/Top-300 books: Sharpe 0.74-0.75 plain, 0.86-0.87 gated, max DD gated −42%.')
A('**Cons / risks**')
A('* **Weak in mid/small caps** (Sharpe 0.47-0.61; IC 3m 0.083 but poor book) — keep to the top ~300.')
A('* Depends on the quality of the **open** print (NSE call-auction opening, un-adjusted corporate actions). Daily legs are clipped at ±15%, but the signal should be re-validated on a second data source before going live.')
A('* Mechanism is a behavioural/microstructure story (gap-chasing reverses); less proven than momentum and may be crowded/decay with regime.')
A('')

A('### I5. csm_absolute-style Sharpe momentum with risk overlays  —  `csm_abs_dual_sharpe` (+ SMA200 gate + volatility target)')
A('')
A('**Idea.** Your live `csm_absolute` ranks on a dual-window (9m & 4m, lag 1m) return / monthly-volatility score from the top-250 liquid names, 15 positions. '
  'This section measures (a) how accurate that score is, and (b) what the "volatile but low-drawdown" behaviour is actually built from.')
A('')
A('**Signal accuracy (exact csm_absolute formula, clipped ±5):**'); A('')
A(acc_table('csm_abs_dual_sharpe')); A('')
A('**Where it works** (IC 3m by universe, for context):'); A('')
A(unis_table(['csm_abs_dual_sharpe', 'q5_126', 'LIVE_elendel(A3+Q5_126)', 'mom_12_1', 'low_pain_126', 'hi_3y', 'intra_over_252'])); A('')
A('**Finding 1 — the *signal* is accurate but not special:** ICIR 0.69 (t 8.0, hit 77%) is among the highest of any single stock factor (only `q5_126` is marginally higher at 0.70), yet its stripped top-15 book (CAGR 17%, Sharpe 0.49 in Liquid-1000; 21%/0.63 in Top-250, roughly level with Elendel there) is clearly behind the Elendel signal in Liquid-1000 and mid/small. '
  'I cannot reproduce the live engine here, so I cannot attribute its high-CAGR / low-DD profile; what the tests do show is that the ranking alone does not produce it and that the drawdown profile moves a lot with overlays (Finding 2).')
A('')
A('**Finding 2 — risk overlays do the heavy lifting.** Same top-15 books, Liquid-1000, with an SMA200 market gate (50% in bear), a 20% volatility target (exposure = min(1, 20%/trailing-6m book vol)), and both:'); A('')
A(overlay_table('U1_liquid1000')); A('')
A('Gate + vol-target takes max drawdown for the four momentum-type books from −58%…−74% **down to −37%…−41%** (low-risk sleeve −37% → −24%), always with higher Sharpe and a 0-4 point CAGR give-up (P4: 31.5% → 28.0% CAGR, Sharpe 0.84 → 0.97, DD −69% → −37%).')
A('')
A('**Finding 3 — concentration is not where the return is:** (CAGR / Max DD / Sharpe, Liquid-1000, P4 signal)'); A('')
A(conc_table('U1_liquid1000', 'P4_resid+persist')); A('')
A('Top-8 to top-25 produce similar CAGR (≈28-32%); top-25 has the best Sharpe. Going to 8-10 names adds variance, not return, for these signals.')
A('')
A('**Finding 4 — "volatility-seeking" is the *wrong* direction:** the high-volatility factor has **negative** IC (`hvol_126` IC 3m −0.062, t −4.1, hit 34%); momentum inside the high-vol tercile still works (IC 3m ≈0.055-0.08) but sorting *for* volatility loses. '
  'ATR-expansion (IC 0.005), up-range-expansion days (0.003), jump frequency (−0.013) and a regime-switched beta (long high-beta in bull, low-beta in bear: IC −0.021) carry no usable signal.')
A('')
A('**Pros** — exact live-signal accuracy is now measured; overlays are portable to every book; shows what to keep (gate + vol-target) when building volatile, high-CAGR books.')
A('**Cons** — the stripped books cannot reproduce the live engine; a proper test needs the full event-driven loop (stops, crash guard, take-profit). Gate/vol-target parameters (SMA200, 50%, 20%, 6m) were fixed in advance, not tuned, but are only one choice.')
A('')

A('### I6. RS-gated breakout v3  —  52-week-high / Donchian breakout + RS rank + trend template')
A('')
A('**Idea.** Event-driven entry on daily breakouts, but only for names that already have top-quartile 6-month relative strength and pass the Stage-2 trend template (C>SMA50>SMA150>SMA200, SMA200 rising, within 25% of 52w high, >30% above 52w low). Entry T+1 close; excess = forward return minus the same-day liquid-universe mean.')
A('')
brk_rows = [brk_row('hi252', '52w closing-high breakout (all)'), brk_row('hi252 | RS top25%', '… + RS top-25%'), brk_row('hi252 | TT+vol1.5+RS25', '… + trend template + vol≥1.5x + RS top-25%'),
            brk_row('hi252 | compressed(VCP)', '… + compressed base (VCP-like)'), brk_row('don55', 'Donchian-55 breakout (all)'), brk_row('don55 | RS top25%', '… + RS top-25%'),
            brk_row('don55 | TT+vol1.5+RS25', '… + trend template + vol≥1.5x + RS top-25%')]
A(md(brk_rows, ['Event', 'N', 'Excess 20d', 'Excess 60d', 't 20d', 't 60d', '% beating universe 20d', '% beating universe 60d', 'Excess 60d ≤2014', 'Excess 60d ≥2015']))
A('')
A('**Pros**')
A('* The filter turns a flat signal into a significant one: Donchian-55 alone is +0.6% at 60d (t 1.6); with RS top-25% it is +2.6% (t 4.4); 52w-high with RS top-25%: +2.9% (t 5.6). Positive in both halves.')
A('* Clean, rule-based entries with natural stop levels; fits the existing HR/VCP event-driven chassis.')
A('**Cons / risks**')
A('* **Hit rate vs universe is under 50% (43-49%)** and median 20d excess is negative: the average comes from a fat right tail, so a breakout book needs payoff asymmetry (tight stops, let winners run) and tolerance for many small losses.')
A('* The edge is momentum/RS in disguise, so correlation to momentum books will be high unless exits/sizing differ.')
A('* **Volume confirmation did not help** (52w-high on <1.5× volume: 20d +0.9% vs +0.45% on ≥1.5×; Donchian-55 on ≥1.5× volume is negative at 20d) — contrary to the usual rule; consider dropping the volume gate in HR/VCP.')
A('* Holdout (≥2015) edge is roughly one-half to two-thirds of the ≤2014 edge.')
A('')

A('### I7. Anchor-aware long high  —  `hi_3y` + `low_pain_126`')
A('')
A('**Idea.** Proximity to the 756-day high (long-horizon anchoring) combined with low average drawdown pain. Highest IC among the pairs, but a **cautionary example**:')
A('')
A(pack_table('P5_long_anchor_painaware')); A('')
A('**Top-15 book vs the Elendel signal in the same engine:**'); A('')
A(book_table('P5_long_anchor_painaware')); A('')
A('**Pros** — high IC (ICIR 0.39-0.65, hit 70-81%, IC 12m 0.12-0.13), moderate drawdowns (gated −40% to −47%). '
  '**Cons** — **the IC does not translate into returns**: CAGR 13-24% and Sharpe 0.43-0.89. The signal ranks the whole cross-section well by selecting low-risk names, whose absolute returns are modest. Treat as a risk/quality filter on other ideas, not a standalone book.')
A('')

A('### S1. One-month seasonality tilt (rejected as a strategy)')
A('')
A('`season_same_month_5y` (mean return of the upcoming calendar month over the previous 5 years): IC 1m = 0.024, ICIR 0.30, hit 61%, t 4.6 — real but **dies after one month** (IC 3m 0.005, t 0.9), has ~0 correlation with everything else, and composites containing it ran at 75-85% monthly turnover. '
  'Adding it to Elendel/Zenith (weight 0.5) lowered book Sharpe. Quarterly (earnings-cycle) and 3y/8y variants are weaker (IC 1m 0.022-0.025, IC 3m ≤0.014). Skip, or use only as a tie-breaker.')
A('')

# ---------- volatility/vix ----------
A('## 3. Volatility- and regime-based ideas (risk management as strategy)')
A('')
A('### 3.1 Trend gate + volatility target (see I5, Finding 2)')
A('')
A('Both overlays use only month-end information. Combined, they reduced max drawdown by 20-34 points in the four momentum-type books (13 points in the low-risk sleeve) and are the most robust "improvement per unit of complexity" found in this study. '
  'Caveat: they were evaluated on stripped books — the live books already contain some of this (regime leverage, Crash Guard), so the *marginal* benefit has to be re-measured in the live engine.')
A('')
A('### 3.2 India VIX spike as a contrarian re-entry / risk-on signal')
A('')
A('When India VIX is in the **top 20% of its trailing 2-year range**, the next 1-3 months have been unusually good for Indian equities (2010-2026, 39 month-ends in the top quintile):')
A('')
vr = []
for a, lab in (('Nifty_50', 'Nifty 50'), ('Nifty_500', 'Nifty 500'), ('MIDCAP100', 'Midcap 100'), ('SMLCAP100', 'Smallcap 100')):
    for h in (1, 3):
        d = vix[(vix.asset == a) & (vix.signal == 'vix_pctile_2y') & (vix.h == h)].iloc[0]
        vr.append([lab, f'{h}m', f(d.ts_ic), f(d.mean_fwd_hiVIX, pct=True), f(d.mean_fwd_rest, pct=True), f(d.p_up_hiVIX, pct=True), f(d.p_up_rest, pct=True)])
A(md(vr, ['Index', 'Horizon', 'Time-series IC (rank)', 'Mean fwd return, VIX top-20%', 'Mean fwd return, rest', 'P(up), VIX top-20%', 'P(up), rest']))
A('')
A('**Pros** — simple, uses a data series you already hold, opposite in sign to a naive "low VIX = safe" rule (the *low-VIX* gate has negative IC −0.12 and loses money as a timer); P(up) is 18-22 points higher at 1m in every index (8-14 points at 3m). '
  'Natural fit for **post-Crash-Guard re-entry** and for leaning into drawdowns.')
A('**Cons** — only 39 high-VIX months (clustered around 2011, 2013, 2015-16, 2020, 2022); monthly-IC t-stat is ≈2; VIX is available from 2009 only; the 3m IC is small (0.07-0.12) so the value is in the *tail* months, not in a continuous signal.')
A('')

# ---------- index / ETF ----------
A('## 4. Index & ETF ideas')
A('')
A('Data: 208 index series (broad, sector, factor, G-Sec, VIX, 2× leveraged/inverse) back to 2000-2005; ~140 ETFs with >1,000 days (NIFTYBEES 2002, LIQUIDBEES/GOLDBEES 2007, silver 2022+, Nasdaq/Hang Seng/sector ETFs 2010-2022+). Monthly signal, T+1 fill, 0.1% one-way cost, cash = LIQUIDBEES (6% before 2007).')
A('')
A('### 4.1 X1 Asset-class dual momentum (Nifty 50 / Midcap 100 / Smallcap 100 / Gold / cash)')
A('')
A('Rank the four assets monthly on a momentum/trend score, hold the top 1 or 2; optional absolute filter (12m return must beat cash, otherwise LIQUIDBEES). Window 2008-04 → 2026-07 (limited by GOLDBEES).')
A('')
rows = []
sub = ast_bk[(ast_bk.k.isin([1, 2]))]
pick = [('hi_252', 1, 'none'), ('mom_3_0', 1, 'none'), ('mom_6_1', 1, 'abs>cash'), ('mom_12_1', 2, 'none'), ('q5_126', 2, 'none'), ('q5_126', 1, 'none')]
for fac, k, gate in pick:
    d = ast_bk[(ast_bk.factor == fac) & (ast_bk.k == k) & (ast_bk.gate == gate)].iloc[0]
    rows.append([fac, k, gate, f(d.cagr, pct=True), f(d.vol, pct=True), f(d.sharpe, 2), f(d.maxdd, pct=True), f(d.calmar, 2), f(d.sharpe_disc, 2), f(d.sharpe_hold, 2), f(d.turn, 2), f(d.hit_vs_cash, pct=True)])
A(md(rows, ['Score', 'Top-k', 'Abs. filter', 'CAGR', 'Vol', 'Sharpe', 'Max DD', 'Calmar', 'Sharpe ≤2014', 'Sharpe ≥2015', 'Turnover', '% months > cash']))
A('')
A('Reference (same window, buy & hold): Nifty 50 CAGR 9.2% / DD −49%; Midcap 100 13.5% / −56%; Smallcap 100 9.6% / −66%; **Gold 13.3% / −17% (Sharpe 0.53)**; equal-weight of the four 12.6% / −43%.')
A('')
ic_rows = [[n, f(r.ic_1), f(r.hit_1, pct=True), f(r.t_1, 1), f(r.ic_3), f(r.hit_3, pct=True), f(r.t_3, 1), f(r.ic_6), f(r.hit_6, pct=True), f(r.t_6, 1)]
           for n, r in ast_ic.sort_values('ic_3', ascending=False).head(6).iterrows()]
A('**Cross-asset IC (N=4 assets per month, ~160 months):**'); A('')
A(md(ic_rows, ['Factor', 'IC 1m', 'Hit 1m', 't 1m', 'IC 3m', 'Hit 3m', 't 3m', 'IC 6m', 'Hit 6m', 't 6m']))
A('')
A('**Pros** — **genuinely different return stream**: monthly return correlation with the stock books is only 0.26-0.49 for the 252d-high / 3m-momentum rotations and **−0.12 to −0.19 for gold** (§6); best configurations reach 16-19% CAGR with max DD ≈ −20% to −25% (Calmar 0.7-0.8); ETF-implementable (NIFTYBEES/JUNIORBEES/GOLDBEES/LIQUIDBEES + mid/small ETFs from 2019/2023).')
A('**Cons** — **those two were the best of 24 configurations tried (6 scores × top-1/2 × with/without absolute filter); the median configuration returned 13.1% CAGR, Sharpe 0.46, max DD −29%** (equal-weight 4 assets: 12.6%, 0.42, −43%), so most of the value is diversification, not selection skill. **Cross-asset IC is weak statistically** (|t| ≤ 1.8 at 1-3m; up to 2.4 at 6m, with N=4 assets and overlapping returns); hit rates are only 50-58%; results are flattered by gold\'s 2019-2026 run and by a short window (18 years) with few regime changes; Smallcap/Midcap index ETFs with real liquidity only exist since 2019-2024 (index returns are not what you would have captured earlier); price indices omit dividends.')
A('')
A('### 4.2 X4 Sector-index rotation (19 sectors/themes, 2004-2026)')
A('')
rows = [[n, f(r.ic_1), f(r.icir_1, 2), f(r.hit_1, pct=True), f(r.ic_3), f(r.icir_3, 2), f(r.hit_3, pct=True), f(r.t_3, 1), f(r.ic_6), f(r.t_6, 1), f(r.ic_disc_3), f(r.ic_hold_3)]
        for n, r in sec_ic.sort_values('icir_3', ascending=False).head(6).iterrows()]
A(md(rows, ['Factor', 'IC 1m', 'ICIR 1m', 'Hit 1m', 'IC 3m', 'ICIR 3m', 'Hit 3m', 't 3m', 'IC 6m', 't 6m', 'IC ≤2014', 'IC ≥2015']))
A('')
bk3 = sec_bk[(sec_bk.k == 3) & (sec_bk.trend_filter == False)].sort_values('sharpe', ascending=False).head(4)
rows = [[r.factor, f(r.cagr, pct=True), f(r.vol, pct=True), f(r.sharpe, 2), f(r.maxdd, pct=True), f(r.sharpe_hold, 2), f(r.turn, 2)] for _, r in bk3.iterrows()]
A('Top-3 sector books (EW sectors: CAGR 12.9%, DD −58%; Nifty 500: 12.7%, −62%):'); A('')
A(md(rows, ['Score', 'CAGR', 'Vol', 'Sharpe', 'Max DD', 'Sharpe ≥2015', 'Turnover']))
A('')
A('**Pros** — consistent sign: trend-persistence/52w-high/Sharpe scores have positive IC at every horizon, strongest at 6m (IC ≈ 0.11-0.13, hit 63-65%); low-ulcer top-3 gives CAGR 14.9% at DD −52%. '
  '**Cons** — **ICIR ≈ 0.2, holdout IC halves (≥2015 ≈ 0.05)**; books barely beat the Nifty 500 and still draw down ~50%; sectors overlap (Bank / Pvt Bank / Fin Services); sector ETFs exist only from 2020-2022 for most themes. '
  'Better as a conditioning input (the stock-level sector factors in §5 add little) than as its own strategy. **Verdict: C.**')
A('')
A('### 4.3 X2 Factor-index regime switch (Low-Vol vs Momentum/Alpha indices)')
A('')
piv = fir.pivot(index='index', columns='regime', values='mean_excess_m')
hit = fir.pivot(index='index', columns='regime', values='hit_beats_n500')
rows = []
for idx in ['LowVol30(N100)', 'Momentum30(N200)', 'Alpha50', 'Midcap150Mom50', 'Quality30(N200)', 'Value20(N50)']:
    rows.append([idx] + [f'{piv.loc[idx, c]*100:+.2f}% ({hit.loc[idx, c]*100:.0f}%)' for c in ('all', 'bull', 'bear', 'VIX>median', 'mkt DD>10%')])
A('Mean monthly excess return vs Nifty 500 (and % of months beating it), by regime known at month-end:'); A('')
A(md(rows, ['Factor index', 'All', 'Bull (>SMA200)', 'Bear', 'VIX>median', 'Mkt DD>10%']))
A('')
A('**Pros** — the Low-Vol index is the only factor index that **gains** when the market is in drawdown (+1.6%/month, 59% hit when the Nifty 500 is >10% off its 1y high; +0.7%/month in bear regimes) while Momentum/Alpha indices lose in those states (−0.2% to −0.5%/month) → a simple state-dependent switch between the momentum books and a low-vol sleeve (I3). '
  '**Cons** — differences are small per month (≤1.6%), hit rates only 51-59%, factor indices start 2003-2009 (NIFTY100 Quality 2009, Value 20 2009) and several factor ETFs/indices are very recent (HighBeta/LowVol 50 from 2024); not significant as standalone strategies.')
A('')
A('### 4.4 X5 Equity-index timing (trend, breadth, VIX, volatility)')
A('')
rows = []
for a, lab in (('Nifty_500', 'Nifty 500'), ('NIFTY_MIDCAP_100', 'Midcap 100'), ('NIFTY_SMLCAP_100', 'Smallcap 100')):
    for s in ('sma200', 'breadth200_gt50', 'vote_sma200_breadth'):
        d = tim[(tim.asset == a) & (tim.signal == s)].iloc[0]
        rows.append([lab, s, f(d.pct_on, pct=True), f(d.balanced_acc, 2), f(d.cagr, pct=True), f(d.bh_cagr, pct=True), f(d.maxdd, pct=True), f(d.bh_maxdd, pct=True), f(d.sharpe, 2), f(d.bh_sharpe, 2), f(d.sharpe_hold, 2)])
A(md(rows, ['Asset', 'Signal (ON = invested, else cash)', '% months ON', 'Balanced accuracy', 'CAGR', 'Buy&hold CAGR', 'Max DD', 'B&H Max DD', 'Sharpe', 'B&H Sharpe', 'Sharpe ≥2015']))
A('')
A('Breadth = % of liquid stocks above their own SMA200 (computed from the stock panel). Balanced accuracy = mean of P(ON → asset beats cash) and P(OFF → asset loses to cash).')
A('')
A('**Pros** — halves the index drawdown (−56%→−23% for Nifty 50 with breadth; Midcap −67%→−26%); breadth200 (alone or combined with SMA200) gave the largest drawdown cut for the smallest CAGR loss among the nine signals tried. '
  '**Cons** — accuracy is **barely above a coin flip (0.50-0.57)**, time-series ICs are ≈0, and timed CAGR is **below buy-and-hold** (e.g. Nifty 500 9.5% vs 13.3%; Midcap 12.7% vs 19.2%) because cash earns 6% and misses sharp recoveries. '
  'Valid only as a **drawdown overlay** for the stock books (§3.1), not as a strategy. A 2× leveraged Nifty TR index with the same gates did not help either (best: CAGR 9.2% vs 13.2% buy-and-hold, DD −35% vs −58%).')
A('')

# ---------- stock-level sector ----------
A('## 5. Sector information as a *stock-level* factor (tested, low value)')
A('')
A('No sector map exists in the data, so each stock was assigned (point-in-time) to the sector index with the highest trailing-252d correlation of market-residual returns (only ~24% of stock-months clear a 0.10 correlation bar). On the **same assigned subset**:')
A('')
rows = []
for _, r in sect_stock[sect_stock.universe.isin(['U1_liquid1000 & assigned', 'U7_midsmall_301_1000 & assigned'])].iterrows():
    rows.append([UN_LABEL[r.universe.replace(' & assigned', '')] + ' (assigned stocks)', r.factor, f(r.ic_3), f(r.icir_3, 2), f(r.hit_3, pct=True), f(r.t_3, 1), f(r.corr_elendel, 2), f(r.inc_ic_3)])
A(md(rows, ['Universe', 'Factor', 'IC 3m', 'ICIR 3m', 'Hit 3m', 't', 'corr→Elendel', 'incr. IC 3m']))
A('')
A('Sector momentum *level* has no signal (IC 3m ≤0.02, |t|<1.5 when evaluated across all assigned stocks); sector *trend quality* (q5, 52w-high) is weak but orthogonal (corr 0.12-0.32, IC 3m 0.017-0.044, t≈1.4-3.3, incremental IC +0.01 to +0.05); '
  'stock-minus-sector momentum is a slightly smoother momentum (higher ICIR, lower correlation) but **not more predictive** and has ~zero incremental IC. **Verdict: skip as a standalone factor.**')
A('')

# ---------- universe guide ----------
A('## 6. Where each factor works (universe guide) and cross-strategy correlation')
A('')
A(unis_table(['q5_126', 'a1_52wh', 'hi_3y', 'mom_12_1', 'mom_resid_12_1', 'csm_abs_dual_sharpe', 'low_pain_126', 'low_ulcer_252', 'lowvol_126', 'low_beta_252', 'intra_over_252', 'tight_close_15', 'neg_overnight_126_clip', 'hvol_126']))
A('')
A('Reading: persistence/anchor factors work everywhere and are strongest in mid/small and low-vol names; **momentum weakens in large caps** (Top-250 IC of 12-1 is half that of mid/small) while **risk-aware and intraday factors strengthen there** (low_pain 0.092, hi_3y 0.082, intra_over_252 0.080 in Top-250). Low-beta only works in large caps (0.065 vs 0.033 mid/small). Raw volatility-seeking is negative everywhere.')
A('')
A('**Monthly-return correlation across the candidate strategies** (2008-04 → 2026-07, net of costs; stock books = top-15 in Liquid-1000 unless noted):')
A('')
keep = ['Elendel_book', 'P4_resid+persist', 'P6_tight+persist', 'P2_low_risk', 'P1_intraday+ulcer', 'AssetRotation_hi_252_top1', 'AssetRotation_mom_3_0_top1', 'SectorRotation_low_ulcer_top3', 'Gold_buyhold', 'Nifty500_buyhold']
keep = [k for k in keep if k in corr.columns]
sub = corr.loc[keep, keep]
rows = [[k[:30]] + [f'{sub.loc[k, c]:.2f}' for c in keep] for k in keep]
SHORT = {'Elendel_book': 'Elendel', 'P4_resid+persist': 'I2 resid', 'P6_tight+persist': 'I1 tight', 'P2_low_risk': 'I3 low-risk', 'P1_intraday+ulcer': 'I4 intraday', 'AssetRotation_hi_252_top1': 'X1 hi252', 'AssetRotation_mom_3_0_top1': 'X1 mom3m', 'SectorRotation_low_ulcer_top3': 'X4 sector', 'Gold_buyhold': 'Gold', 'Nifty500_buyhold': 'Nifty500'}
rows = [[SHORT.get(k, k)] + [f'{sub.loc[k, c]:.2f}' for c in keep] for k in keep]
A(md(rows, [''] + [SHORT.get(k, k) for k in keep]))
A('')
A('The factor-based stock ideas are 0.6-0.9 correlated with the Elendel book (as you expected). The only low-correlation building blocks are **asset-class rotation (0.26-0.49) and gold (≈ −0.15)**; the low-risk sleeve is the lowest of the stock ideas (0.63).')
A('')

# ---------- ETF list ----------
A('### ETF proxies available for the index ideas (recent median daily traded value)')
A('')
want = ['NIFTYBEES', 'JUNIORBEES', 'BANKBEES', 'MID150BEES', 'HDFCSML250', 'GOLDBEES', 'SILVERBEES', 'LIQUIDBEES', 'LIQUIDCASE', 'MON100', 'HNGSNGBEES', 'ITBEES', 'PHARMABEES', 'PSUBNKBEES', 'LTGILTBEES', 'SMALLCAP', 'MIDCAPETF']
e = etf.set_index('symbol')
rows = []
for s in want:
    if s in e.index:
        r = e.loc[s]
        rows.append([s, str(r['name'])[:40], str(r.start), f'₹{r.recent_med_value_inr/1e7:.1f} cr'])
A(md(rows, ['ETF', 'Name', 'History from', 'Median value / day']))
A('')
A('Full list: `results/etf_liquid_list.csv`. Note mid/small-cap ETFs with meaningful liquidity only exist from 2019-2024, so back-tests on those sleeves rely on index data that you could not have fully captured earlier.')
A('')

# ---------- rejected ----------
A('## 7. Rejected / low-value signals (so they are not re-tested)')
A('')
rej = ['rev_1m', 'rev_1w', 'overnight_126', 'overnight_minus_intraday_126', 'gapup_freq_63', 'event_ret_63', 'illiq_amihud_63', 'small_dvol_63', 'vol_surge_21_252', 'up_capture_252', 'high_beta_252', 'hvol_126',
       'beta_regime', 'atr_expansion_14_63', 'range_expansion_up', 'mom_accel', 'nr7_count_21', 'vr_5_252', 'autocorr1_126', 'jump_up_freq_126']
rows = []
for n in rej:
    d = ALL[(ALL.universe == 'U1_liquid1000') & (ALL['factor'] == n)]
    if d.empty:
        continue
    r = d.iloc[0]
    note = {'overnight_minus_intraday_126': 'sign-flipped = I4 (intraday-led trend)', 'rev_1m': 'continuation, not reversal', 'rev_1w': 'continuation, not reversal',
            'illiq_amihud_63': 'no illiquidity premium', 'small_dvol_63': 'no small-size premium', 'hvol_126': 'volatility-seeking loses'}.get(n, '')
    rows.append([n, f(r.ic_1), f(r.ic_3), f(r.icir_3, 2), f(r.hit_3, pct=True), f(r.t_3, 1), f(r.ic_disc_3), f(r.ic_hold_3), note])
A(md(rows, ['Factor', 'IC 1m', 'IC 3m', 'ICIR 3m', 'Hit 3m', 't', 'IC ≤2014', 'IC ≥2015', 'Note']))
A('')

# ---------- next steps ----------
A('## 8. Suggested build order')
A('')
A('1. **I1 + I2 as new books in the mid/small universe** (rank 301-1000) using the existing chassis; keep the top-15 / hysteresis / inverse-vol machinery but add the **SMA200 gate + volatility-target overlay** (§3.1) and re-measure in the full engine. These have the best evidence and the best book Sharpe, but expect 0.8-0.9 correlation with the current momentum books — differentiate via universe, stops and sizing.')
A('2. **I3 low-risk sleeve** as the drawdown-control / diversification book (low turnover, works in bear regimes); combine with the **factor-index regime evidence** (§4.3) to scale it up when the market is >10% off its high.')
A('3. **X1 asset-class rotation** (Nifty/Midcap/Smallcap/Gold/LIQUIDBEES) as the genuinely decorrelated sleeve — treat the gold leg skeptically (2019-26 bull) and cap its weight.')
A('4. **I6 breakout v3** — add RS-top-quartile + trend-template gate to HR/VCP, drop the volume requirement, and evaluate with the stop/exit logic (event study shows no raw edge without the gate).')
A('5. **I4** only for a large-cap (top-300) variant, after validating open-price quality on a second data source.')
A('6. **Add the India-VIX spike rule** as a re-entry/leverage signal to the Crash Guard logic of existing books and test it in the live engine (39 events — treat as supporting evidence only).')
A('')
A('## 9. Caveats that matter')
A('')
A('* **Survivorship bias** (only ~2% of symbols are delisted) inflates absolute CAGRs, most for low-vol and smooth-trend selection; relative comparisons are more trustworthy than levels.')
A('* **Stripped books**: equal weight, monthly, no stops/Crash Guard/take-profit/regime leverage. Use them to *rank ideas*, not to forecast live CAGR/drawdown.')
A('* **Holdout decay**: nearly every price-based signal has ~30-40% lower IC in 2015-2026 than in 2004-2014 (still t>5 for the main factors). Idea ranks were not tuned on the holdout, but the pack definitions were chosen after seeing single-factor results on the full sample.')
A('* **Multiple testing**: ~120 factors, ~10 packs, many universes. Packs/overlay parameters (weights 0.5/1.0, SMA200, 50%, 20% vol target) were fixed in advance, but an idea that wins in one universe only (e.g. I1 in mid/small, I4 in large-cap) deserves out-of-sample paper trading before capital.')
A('* **Index/ETF history is short and regime-poor** (≤19y with gold), cross-asset N is tiny, and index ≠ tradable ETF before 2010-2024.')
A('* Equal-weight market index is used as the beta/regime proxy (as in the live runners); benchmark index files in `benchmark_data/` cover 2026 only, but `index_data/` has the full history if you want to switch to Nifty-based regime flags.')
A('')
A('## 10. Appendix — definitions and files')
A('')
A('| Factor | Definition (signal at close of t; higher = better) |')
A('|---|---|')
defs = [('q5_126 / q5_189', 'share of last 126/189 days with close > SMA50 (live Elendel / Zenith leg)'),
        ('a1_52wh, a3_rs_high', 'close / 252d high; RS-line (stock/equal-weight market) / its 252d max (live)'),
        ('tight_close_15', '−std(close, 15d)/mean(close, 15d)'),
        ('mom_resid_12_1', 'Σ over t−252…t−21 of [daily return − beta₍t−1₎ × equal-weight market return], beta from 252d rolling covariance'),
        ('lowvol_126', '−std of daily returns over 126d'),
        ('low_ulcer_252', '−sqrt(mean( (close / trailing-252d max − 1)² )) over 252d'),
        ('low_pain_126', 'mean over 126d of (close / trailing-126d max − 1)  (negative; closer to 0 is better)'),
        ('intra_over_252', 'Σ log(close/open) − Σ log(open/prev close) over 252d, each daily leg clipped to ±15%'),
        ('hi_3y', 'close / 756d high'),
        ('csm_abs_dual_sharpe', '½[(P₍t−1₎/P₍t−10₎ −1)/σ₉ₘ + (P₍t−1₎/P₍t−5₎ −1)/σ₄ₘ], σ = monthly-return std × √12, clipped ±5 (csm_absolute.py)'),
        ('hvol_126, beta_regime, …', 'see `factors.py` (all ~120 definitions with docstrings)')]
for a, b in defs:
    A(f'| `{a}` | {b} |')
A('')
A('Files: `data.py`, `assets.py` (loaders) · `factors.py` (factor library) · `evaluate.py` (IC/ICIR/hit/t engine) · `portfolio_lab.py`, `index_lab.py` (books) · `run_scan.py` + `stage2…13_*.py` (studies) · `results/*.csv` (all numbers) · `FINDINGS.md` (first-pass study) · `gen_report.py` (this document).')

import re
text = '\n'.join(L) + '\n'
text = re.sub(r'\n(\*\*(?:Pros|Cons|Cons / risks|Implementation notes\.?)\*\*)', r'\n\n\1', text)
text = re.sub(r'(\*\*(?:Pros|Cons / risks)\*\*)\n\*', r'\1\n\n*', text)
text = re.sub(r'\n{3,}', '\n\n', text)
open(os.path.join(HERE, 'NEW_STRATEGY_IDEAS.md'), 'w').write(text)
print('written', len('\n'.join(L)), 'chars')
