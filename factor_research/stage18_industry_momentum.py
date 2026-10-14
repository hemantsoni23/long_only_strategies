"""
stage18_industry_momentum.py -- point-in-time industry/sector momentum, built bottom-up from
instruments_clean.csv + the stock OHLCV panel (no sector ETF/index price series needed at all).

Why this design (see factor_research/FINDINGS.md / MASTER_RANKING.md and the plan): three prior
sector-momentum attempts failed, and reading stage7_sector.py / stage10_sector_stock.py + the
momentum/ literature pinned down three likely causes, each tested here rather than assumed away:
  1. stage7_sector.py traded only ~19 NSE sector indices (too few independent assets -> weak
     IC/Sharpe/Calmar).  instruments_clean.csv's Sector_clean has the same problem (11 buckets);
     its Industry_clean (205 categories) has never been used for this -- tested here, with a
     per-month minimum-constituent fallback to Sector_clean when an industry is too thin.
  2. stage10 only tested 6/12-month sector momentum.  Moskowitz-Grinblatt (1999) found industry
     momentum strongest at (1,1), no skip month; Grundy-Martin (reported in the Jegadeesh-Titman
     2011 survey) found it insignificant WITH the standard 1-month skip.  Tested here: every
     formation length (1/3/6/12m) built both with and without a 1-month skip.
  3. stage10's stock-vs-sector RESIDUAL factor passed a basic IC screen but stayed 0.6-0.68
     correlated with the live Elendel engine -- not a new return stream.  Moskowitz-Grinblatt's
     own results show industry-ADJUSTING raw momentum kills most of its profit; the construction
     that worked was ADDITIVE (tilt toward hot industries).  Both constructions are built here,
     side by side, rather than only the one that failed before.  Moskowitz-Grinblatt also found
     the effect concentrated in large/liquid names (US); Nijman-Swinkels-Verbeek found the
     opposite in Europe (small growth stocks) -- both ends of the cap spectrum are evaluated
     evenhandedly below (U3_top300 vs U7_midsmall_301_1000), nothing is presupposed.

Construction (point-in-time, no lookahead):
  - Monthly stock return at sig[m] = Cf[sig[m]]/Cf[sig[m-1]] - 1 (exact two-point ratio).
  - Basket membership for the return attributed to month m uses U1 eligibility as of sig[m-1]
    (known before the month starts) -- never the current month's own universe.
  - Industry_clean fallback: at signal date sig[m] (the date the FACTOR VALUE is read, i.e. the
    decision point, separate from the historical return construction above), an industry's own
    basket is trusted only if >=MIN_MEMBERS U1-eligible stocks carry that label *right now*
    (count from U1.loc[sig[m]]); otherwise every member stock temporarily reads its Sector_clean
    parent's basket that month.  This is decided per ticker-month, documented, never dropped.
  - Weighting: equal, and trailing-63d-median-dollar-volume-weighted (X.DV) -- the only cheaply
    available liquidity-weighted proxy (there is no true market-cap series in the panels; Cap in
    instruments_clean.csv is a coarse Small/Mid/Large bucket, not usable as a weight).
  - Formation length L in {1,3,6,12} months, each with skip in {0,1} (skip=1 excludes the most
    recent completed month from the trailing-return window, matching every other factor's
    convention of trading from the close of t+1 with data only through close of t).
  - Construction (a) level: the basket's own trailing return, broadcast to every current member.
    Construction (b) residual: member's own trailing return minus the basket's trailing return.
  - All axes (L, skip, construction, granularity, weighting) are fixed above, before running
    this script -- not expanded after seeing results.  64 factor variants total
    (4 L x 2 skip x 2 construction x 2 granularity x 2 weighting); each is evaluated by
    evaluate_factor() across every forward horizon (1/2/3/6/12m) in one call, which already
    covers the full (L, hold) grid -- a formation length of 6 evaluated at h=1 and h=6 is
    IM(6,1) and IM(6,6) respectively, no separate per-hold construction needed.

instruments_clean.csv look-ahead caveat: it is a static, current-day snapshot (no point-in-time
reclassification history).  This is bounded and documented, not solved: industry reclassification
is rare relative to a company's lifetime, so the dominant error this could introduce (a stock's
basket membership being wrong for years it existed under a different de facto business) should be
a small minority of stock-months.  No attempt is made to guess reclassification dates.

Output: results/stage18_industry_momentum.csv (same schema evaluate_factor emits everywhere else),
results/stage18_coverage.csv (industries clearing the >=10 threshold, by month), and a printed
cross-check of the bottom-up sector baskets against the real NSE sector indices.
"""
import os
import pickle
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from assets import load_indices                                   # noqa: E402
from data import load_panels                                      # noqa: E402
from evaluate import composite, evaluate_factor                    # noqa: E402
from factors import Ctx                                            # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
INSTRUMENTS_CSV = os.path.join(os.path.dirname(HERE), 'instruments_clean.csv')
RESULTS = os.path.join(HERE, 'results')
os.makedirs(RESULTS, exist_ok=True)

MIN_MEMBERS = 10          # Industry_clean fallback-to-Sector_clean threshold (pre-set, not tuned)
LOOKBACKS = (1, 3, 6, 12)  # formation length in months
DV_WINDOW = 63             # trailing dollar-volume window for the liquidity-weighted basket


# ───────────────────────── load state + universes ─────────────────────────
st = pickle.load(open(os.path.join(HERE, '.cache', 'state.pkl'), 'rb'))
sig, F, U, FWD = st['sig'], st['F'], st['U'], st['FWD']
UN = pickle.load(open(os.path.join(HERE, '.cache', 'extra_universes.pkl'), 'rb'))
UNIVERSES = {
    'U1_liquid1000': U['U1_liquid1000'],
    'U3_top300': U['U3_top300'],
    'U4_top250': UN['U4_top250'],
    'U7_midsmall_301_1000': UN['U7_midsmall_301_1000'],
}
U1 = U['U1_liquid1000']

P = load_panels()
X = Ctx(P)
cols = X.C.columns
elen_base = {u: composite(F, ['a3_rs_high', 'q5_126'], m) for u, m in UNIVERSES.items()}

# ───────────────────────── instruments_clean.csv -> ticker labels ─────────────────────────
inst = (pd.read_csv(INSTRUMENTS_CSV)[['trading_symbol', 'Sector_clean', 'Industry_clean']]
        .dropna(subset=['trading_symbol'])
        .drop_duplicates('trading_symbol', keep='first')
        .set_index('trading_symbol'))
inst = inst.reindex(cols)                                   # align to price-panel ticker order
sector_of = inst['Sector_clean']
industry_of = inst['Industry_clean']
has_label = sector_of.notna() & industry_of.notna()
print(f"[stage18] instruments_clean.csv coverage: {int(has_label.sum())}/{len(cols)} price tickers "
      f"have a Sector_clean+Industry_clean label ({int(sector_of.notna().sum())} have Sector_clean alone)")

# ───────────────────────── monthly stock returns, sampled at sig ─────────────────────────
Cm = X.Cf.reindex(sig)
mret = Cm.pct_change()                                      # sig x tickers, month-over-month
elig_prev = U1.shift(1).reindex(sig).fillna(False)           # eligibility known BEFORE the month trades
dv_m = X.DV.rolling(DV_WINDOW, min_periods=21).median().reindex(sig).shift(1)   # known before the month

# ───────────────────────── per-month industry coverage (for the >=10 fallback + report) ─────────────────────────
ind_names = sorted(industry_of.dropna().unique())
sec_names = sorted(sector_of.dropna().unique())
ind_onehot = pd.DataFrame({n: (industry_of == n).values for n in ind_names}, index=cols)
# industry_count[t, industry] = # of U1-eligible-AT-t stocks currently carrying that label
ind_count = pd.DataFrame(U1.reindex(sig).fillna(False).values.astype('float64') @ ind_onehot.values,
                          index=sig, columns=ind_names)
ok_industry = ind_count >= MIN_MEMBERS

coverage = pd.DataFrame({
    'usable_industries': ok_industry.sum(axis=1),
    'median_members_usable': ind_count.where(ok_industry).median(axis=1),
    'min_members_usable': ind_count.where(ok_industry).min(axis=1),
}, index=sig)
coverage.to_csv(os.path.join(RESULTS, 'stage18_coverage.csv'))
print('[stage18] industry coverage (usable_industries = labels with >=%d live U1 members), by year:' % MIN_MEMBERS)
print(coverage['usable_industries'].groupby(coverage.index.year).mean().round(1).to_string())

# effective group per ticker per signal date: its Industry_clean if currently usable, else "SEC:"+Sector_clean
ind_vals = industry_of.values
sec_keys = ('SEC:' + sector_of.fillna('UNKNOWN')).values
ok_lookup = ok_industry.reindex(columns=ind_names)
eff_group = pd.DataFrame(index=sig, columns=cols, dtype=object)
for t in sig:
    ok_row = ok_lookup.loc[t]
    usable = pd.Series(ind_vals, index=cols).map(ok_row).fillna(False).values
    row = np.where(usable & has_label.values, ind_vals, np.where(has_label.values, sec_keys, None))
    eff_group.loc[t] = row

is_industry_level = eff_group.notna() & ~eff_group.astype(str).apply(lambda r: r.str.startswith('SEC:'))
print(f"[stage18] avg share of labelled tickers resolved at Industry_clean (vs Sector_clean fallback): "
      f"{float(is_industry_level.sum(axis=1).sum()) / float(eff_group.notna().sum(axis=1).sum()):.2%}")


# ───────────────────────── basket returns (equal- and DV-weighted), per group ─────────────────────────
def build_baskets(label_series, weight_frame=None):
    """label_series: ticker -> group name (static). Returns DataFrame sig x groups of basket monthly returns
    and a matching DataFrame of member counts, using elig_prev as membership and (optionally) weight_frame
    (sig x tickers, already lagged) for weighting."""
    names = sorted(label_series.dropna().unique())
    onehot = pd.DataFrame({n: (label_series == n).values for n in names}, index=cols)
    elig = elig_prev.reindex(columns=cols).fillna(False)
    r = mret.reindex(columns=cols)
    valid = elig & r.notna()
    if weight_frame is None:
        w = valid.astype('float64')
    else:
        w = valid.astype('float64') * weight_frame.reindex(columns=cols).fillna(0.0).clip(lower=0.0)
    rw = (r.fillna(0.0) * w)
    num = rw.values @ onehot.values
    den = w.values @ onehot.values
    cnt = valid.astype('float64').values @ onehot.values
    with np.errstate(invalid='ignore', divide='ignore'):
        ret = np.where(den > 0, num / den, np.nan)
    return (pd.DataFrame(ret, index=sig, columns=names),
            pd.DataFrame(cnt, index=sig, columns=names))


sector_ret_eq, _ = build_baskets(sector_of)
industry_ret_eq, _ = build_baskets(industry_of)
sector_ret_dv, _ = build_baskets(sector_of, dv_m)
industry_ret_dv, _ = build_baskets(industry_of, dv_m)


def combined_basket(weighting):
    sec_r, ind_r = (sector_ret_eq, industry_ret_eq) if weighting == 'eq' else (sector_ret_dv, industry_ret_dv)
    out = pd.concat([sec_r.add_prefix('SEC:'), ind_r], axis=1)
    return out


# ───────────────────────── trailing-return / broadcast helpers ─────────────────────────
def trailing_logret(ret_frame, L, skip):
    """log1p-cumsum trailing L-month return ending at t (skip=0) or t-1 (skip=1)."""
    logr = np.log1p(ret_frame.clip(-0.9, 5.0)).fillna(0.0)
    cum = logr.cumsum()
    end = cum.shift(1) if skip else cum
    start = end.shift(L)
    return np.expm1(end - start)


def broadcast(trailing_group_ret, eff_group_frame):
    """trailing_group_ret: sig x groups. eff_group_frame: sig x tickers (group name per cell). -> sig x tickers."""
    out = pd.DataFrame(index=sig, columns=cols, dtype='float64')
    for t in sig:
        g = eff_group_frame.loc[t]
        valid = g.notna()
        vals = trailing_group_ret.loc[t].reindex(g[valid]).values
        row = np.full(len(cols), np.nan)
        row[valid.values] = vals
        out.loc[t] = row
    return out


# ───────────────────────── build the 64 factor variants ─────────────────────────
NEW = {}
own_trailing = {(L, s): trailing_logret(mret, L, s) for L in LOOKBACKS for s in (0, 1)}

for weighting in ('eq', 'dv'):
    basket = combined_basket(weighting)
    for L in LOOKBACKS:
        for skip in (0, 1):
            trail_basket = trailing_logret(basket, L, skip)
            own = own_trailing[(L, skip)]
            for gran_name, eff in (('ind', eff_group), ('sec', 'SEC:' + sector_of.fillna('UNKNOWN'))):
                if gran_name == 'sec':
                    eff_frame = pd.DataFrame(np.tile(eff.values, (len(sig), 1)), index=sig, columns=cols)
                    eff_frame = eff_frame.where(np.tile(has_label.values, (len(sig), 1)), None)
                else:
                    eff_frame = eff
                level = broadcast(trail_basket, eff_frame)
                resid = own - level
                tag = f"{gran_name}_{weighting}_L{L}_skip{skip}"
                NEW[f'indmom_level_{tag}'] = level.astype('float32')
                NEW[f'indmom_resid_{tag}'] = resid.astype('float32')

print(f"[stage18] built {len(NEW)} factor variants")
pickle.dump(NEW, open(os.path.join(HERE, '.cache', 'stage18_industry_factors.pkl'), 'wb'))

# ───────────────────────── evaluate ─────────────────────────
rows = []
for name, fr in NEW.items():
    for uname, mask in UNIVERSES.items():
        r, _ = evaluate_factor(name, fr, mask, FWD, base_rank=elen_base[uname], horizons=(1, 2, 3, 6, 12))
        r['universe'] = uname
        rows.append(r)
    print(f"  evaluated {name}", flush=True)

df = pd.DataFrame(rows)
df.to_csv(os.path.join(RESULTS, 'stage18_industry_momentum.csv'), index=False, float_format='%.5f')
cols_show = ['factor', 'universe', 'avg_n', 'ic_3', 'icir_3', 't_3', 'ic_disc_3', 'ic_hold_3',
             'ic_6', 'icir_6', 't_6', 'corr_elendel', 'inc_ic_3', 'inc_ic_6']
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 40); pd.set_option('display.max_rows', 300)
print(df[cols_show].sort_values('inc_ic_3', ascending=False).head(40).round(4).to_string(index=False))

# ───────────────────────── sanity cross-check vs real NSE sector indices ─────────────────────────
IDX_MAP = {
    'Financial Services': ['Nifty_Bank', 'Nifty_Fin_Service'],
    'Technology': ['Nifty_IT'],
    'Healthcare': ['NIFTY_HEALTHCARE', 'Nifty_Pharma'],
    'Consumer Defensive': ['Nifty_FMCG'],
    'Consumer Cyclical': ['Nifty_Auto', 'Nifty_Consumption'],
    'Basic Materials': ['Nifty_Metal'],
    'Energy': ['Nifty_Energy'],
    'Real Estate': ['Nifty_Realty'],
    'Communication Services': ['Nifty_Media'],
    'Industrials': ['Nifty_Infra'],
}
try:
    idx_close = load_indices()['close']
    idx_mret = idx_close.reindex(sig).pct_change()
    print('\n[stage18] cross-check: bottom-up Sector_clean basket vs matching real NSE index (monthly-return corr)')
    for sec, idx_names in IDX_MAP.items():
        for ix in idx_names:
            if ix in idx_mret.columns:
                j = sector_ret_eq[sec].dropna().index.intersection(idx_mret[ix].dropna().index)
                if len(j) > 24:
                    c = sector_ret_eq[sec].loc[j].corr(idx_mret[ix].loc[j])
                    print(f"  {sec:<24} vs {ix:<18} corr={c:+.2f}  n={len(j)}")
except Exception as e:
    print('[stage18] index cross-check skipped:', e)
