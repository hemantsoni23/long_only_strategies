"""Build the Notion-ready report, charts and supporting CSVs from the study."""
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'research/csm_value_studies/notion_analysis'
DATA = json.loads((OUT / 'metrics.json').read_text())['results']
R = {(r['version'], r['case']): r for r in DATA}
CASES = ['fundamental', 'pullback_common', 'pullback_price_only', 'trend_price_only']
NAMES = {'fundamental': 'Fundamental strategy', 'pullback_common': 'Pullback · common eligible',
         'pullback_price_only': 'Pullback · price-only rules', 'trend_price_only': 'Trend · price-only rules'}
COLORS = ['#2863b2', '#7692b2', '#e59138', '#38a272']
START, END = '2019-06-03', '2024-12-31'
plt.rcParams.update({'svg.fonttype': 'none', 'font.family': 'DejaVu Sans', 'font.size': 10})


def pct(x): return '—' if x is None or pd.isna(x) else f'{x * 100:.2f}%'
def signed_pp(x): return '—' if x is None or pd.isna(x) else f'{x:+.2f} pp'
def per(x): return '—' if x is None or pd.isna(x) else f'{x:+.2f}%'
def num(x): return '—' if x is None or pd.isna(x) else f'{x:.2f}'
def table(headers, rows):
    return '| ' + ' | '.join(headers) + ' |\n| ' + ' | '.join(['---'] * len(headers)) + ' |\n' + '\n'.join('| ' + ' | '.join(str(x).replace('|', '\\|') for x in row) + ' |' for row in rows)


def closed(version, case):
    d = pd.read_csv(OUT / f'{version}_{case}_trades.csv', parse_dates=['Entry_Date', 'Exit_Date'])
    return d[(d.Entry_Date >= START) & (d.Exit_Date >= START) & (d.Exit_Date <= END) & (d.Exit_Reason != 'END_OF_PERIOD')].copy()


def boot_spread(d, mode, control, iterations=1500, block=126):
    # Paired circular blocks of fixed daily return paths. This does not
    # recompute the strategy on a resampled market history.
    x = d[f'{mode}:fundamental'].to_numpy(float)
    y = d[f'{mode}:{control}'].to_numpy(float)
    rng = np.random.default_rng(7181)
    n = len(x)
    offsets = np.arange(block)
    out = []
    for _ in range(iterations):
        starts = rng.integers(0, n, size=int(np.ceil(n / block)))
        idx = ((starts[:, None] + offsets) % n).ravel()[:n]
        out.append(np.expm1(np.log1p(x[idx]).sum() * 252 / n) - np.expm1(np.log1p(y[idx]).sum() * 252 / n))
    lo, mid, hi = np.quantile(out, [.025, .5, .975])
    return float(lo), float(mid), float(hi), float(np.mean(np.asarray(out) > 0))


def draw_charts(returns):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.6), sharex=True)
    for ax, mode in zip(axes, ('normal', 'experimental')):
        m = [R[(mode, c)]['windows']['full'] for c in CASES]
        y = np.arange(len(CASES))
        ax.barh(y - .18, [x['cagr'] * 100 for x in m], height=.34, color='#2863b2', label='CAGR')
        ax.barh(y + .18, [abs(x['max_drawdown']) * 100 for x in m], height=.34, color='#d1794a', label='|Maximum drawdown|')
        for i, x in enumerate(m):
            ax.text(x['cagr'] * 100 + .4, i - .18, f"{x['cagr'] * 100:.1f}%", va='center', fontsize=9)
            ax.text(abs(x['max_drawdown']) * 100 + .4, i + .18, f"{abs(x['max_drawdown']) * 100:.1f}%", va='center', fontsize=9)
        ax.set_yticks(y, [NAMES[c] for c in CASES]); ax.invert_yaxis()
        ax.set_title(mode.title() + ' engine', fontweight='bold')
        ax.set_xlabel('Annualized CAGR or drawdown magnitude (%)')
        ax.grid(axis='x', alpha=.2); ax.set_axisbelow(True)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(.5, .94), ncol=2, fontsize=9)
    fig.suptitle('Performance by ranking and eligibility rules', fontweight='bold', fontsize=15)
    fig.text(.5, .01, '2019-06-03 to 2024-12-31 · Compare within each panel; engines have different accounting', ha='center', fontsize=9)
    fig.tight_layout(rect=(0, .04, 1, .88)); fig.savefig(OUT / 'performance.svg', bbox_inches='tight'); fig.savefig(OUT / 'performance.png', dpi=130, bbox_inches='tight'); plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5), sharex=True)
    for ax, mode in zip(axes, ('normal', 'experimental')):
        m = [R[(mode, c)]['windows']['full'] for c in CASES]
        y = np.arange(len(CASES))
        ax.barh(y - .18, [x['win_rate'] * 100 for x in m], height=.34, color='#35a779', label='Winning trades')
        ax.barh(y + .18, [x['loss_rate'] * 100 for x in m], height=.34, color='#d16b5d', label='Losing trades')
        for i, x in enumerate(m):
            ax.text(x['win_rate']*100+.4, i-.18, f"{x['win_rate']*100:.1f}%", va='center', fontsize=9)
            ax.text(x['loss_rate']*100+.4, i+.18, f"{x['loss_rate']*100:.1f}%", va='center', fontsize=9)
        ax.set_yticks(y, [NAMES[c] for c in CASES]); ax.invert_yaxis(); ax.set_xlim(0, 72)
        ax.set_xlabel('Share of closed trades (%)'); ax.set_title(mode.title() + ' engine', fontweight='bold')
        ax.grid(axis='x', alpha=.2); ax.set_axisbelow(True)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(.5, .94), ncol=2, fontsize=9)
    fig.suptitle('Winner and loser rates by strategy', fontweight='bold', fontsize=15)
    fig.text(.5, .01, 'Unweighted entry-to-exit price returns; open end-of-period positions excluded', ha='center', fontsize=9)
    fig.tight_layout(rect=(0, .04, 1, .88)); fig.savefig(OUT / 'trade_outcomes.svg', bbox_inches='tight'); fig.savefig(OUT / 'trade_outcomes.png', dpi=130, bbox_inches='tight'); plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2), sharey=True)
    for ax, mode in zip(axes, ('normal', 'experimental')):
        for case, color in zip(CASES, COLORS):
            series = (1 + returns[f'{mode}:{case}']).cumprod()
            plot_idx = np.unique(np.r_[np.arange(0, len(series), 5), len(series) - 1])
            ax.plot(returns.index[plot_idx], series.iloc[plot_idx], lw=1.6, label=NAMES[case], color=color)
        ax.set_xlim(returns.index.min(), returns.index.max())
        ax.set_title(mode.title() + ' engine', fontweight='bold'); ax.grid(alpha=.2)
        ax.set_xlabel('Year'); ax.legend(fontsize=8, loc='upper left')
    axes[0].set_ylabel('Growth of ₹1 of modeled portfolio value')
    fig.suptitle('Illustrative portfolio paths', fontsize=15, fontweight='bold')
    fig.text(.5, .01, 'Return booking differs by panel; paths include modeled cash return and trading costs', ha='center', fontsize=9)
    fig.tight_layout(rect=(0, .04, 1, .93)); fig.savefig(OUT / 'portfolio_paths.svg', bbox_inches='tight'); fig.savefig(OUT / 'portfolio_paths.png', dpi=130, bbox_inches='tight'); plt.close(fig)


def factor_bins(version, field):
    d = closed(version, 'fundamental').dropna(subset=[field, 'PnL_Pct']).copy()
    d['bucket'] = pd.qcut(d[field], 4, duplicates='drop')
    rows = []
    for band, g in d.groupby('bucket', observed=True):
        rows.append([f'{band.left:.3f} to {band.right:.3f}', len(g), pct((g.PnL_Pct > 0).mean()), per(g.PnL_Pct.mean()), f'{g.Holding_Days.mean():.0f}'])
    return rows


def pair_entries(version, case):
    a = closed(version, 'fundamental')
    b = closed(version, case)
    keys = ['Ticker', 'Entry_Date']
    if a.duplicated(keys).any() or b.duplicated(keys).any():
        raise ValueError('Ambiguous same-ticker, same-date entries in pair analysis')
    p = a[keys + ['PnL_Pct', 'Exit_Date']].merge(b[keys + ['PnL_Pct', 'Exit_Date']], on=keys, suffixes=('_fund', '_control'), validate='one_to_one')
    return {'matched': len(p), 'both_win': int(((p.PnL_Pct_fund > 0) & (p.PnL_Pct_control > 0)).sum()),
            'fund_only_win': int(((p.PnL_Pct_fund > 0) & (p.PnL_Pct_control <= 0)).sum()),
            'control_only_win': int(((p.PnL_Pct_fund <= 0) & (p.PnL_Pct_control > 0)).sum()),
            'neither_win': int(((p.PnL_Pct_fund <= 0) & (p.PnL_Pct_control <= 0)).sum()),
            'mean_delta': float((p.PnL_Pct_fund - p.PnL_Pct_control).mean()) if len(p) else None}


def main():
    assert len(DATA) == 8, 'All eight cases must finish before building the document.'
    returns = pd.read_csv(OUT / 'daily_returns.csv', index_col='date', parse_dates=True)
    draw_charts(returns)
    sme = {p.stem for p in (ROOT / 'fundamentals/sme').glob('*.json')}
    parts = []
    def add(s): parts.append(s.strip())

    add(table(['Strategy logic', 'Normal value', 'Experimental value–growth–pullback'], [
      ['Data and universe', 'Upstox OHLCV ∩ fundamentals JSON ∩ NSE valuation-price symbols; main and SME files; results usable next day; cutoff 31 Dec 2024.', 'Same source and timing rules. Neither uses a top-1,000 price × volume rank filter.'],
      ['Other eligibility', 'Previous month-end NSE price > ₹20; ≤5 high=low days in prior 63 sessions; lagged prior-month return ≥ −15%; at least 60 eligible stocks.', 'Same; high=low is only a circuit proxy. CA-unit mask can exclude uncertain share counts.'],
      ['Fundamental factor', 'TTM net profit from four consecutive quarters ÷ (as-traded price × filed shares); TTM profit > 0, latest-quarter YoY profit growth > 0 and E/P ≤50%.', 'Same eligibility. Earnings-yield and latest-quarter symmetric YoY growth are percentile-ranked as separate scoring components.'],
      ['OHLCV contribution', 'Price and circuit/falling-knife filters, 21-day volatility sizing, benchmark/regime, risk and close-based stops. No OHLCV score in ranking.', 'Same plus pullback score from relative strength versus its 252-session peak and proportion of recent closes above SMA50.'],
      ['Ranking', 'Highest E/P first; monthly cross-sectional z-scoring preserves its order.', '55% E/P rank + 20% profit-growth rank + 25% inverse A3/Q5 price-strength rank. Missing secondary leg receives neutral percentile.'],
      ['Stock selection', 'Top 20 entries; previous monthly selections may remain through rank 40, subject to 10-rank swap gap.', 'Same 20/40/10 selection rules; actual holdings and target selections can temporarily differ.'],
      ['Rebalancing', 'Month-end close signal; next session open execution. Defers first two consecutive monthly target drops; exit on the third.', 'Same timing; defers first three drops, exits on the fourth. Rebalances continuing holdings on a new month signal or risk-scale change; missing-open resizes retry.'],
      ['Position sizing', 'Inverse 21-session volatility; 0.75% risk budget ÷ 15% entry stop = 5% maximum target weight. 20 × 5% permits up to 100% before overlays.', 'Same cap and 20 positions. Risk adjustments, missing quotes, insufficient eligible stocks and cash-funded trading fees can reduce exposure.'],
      ['Portfolio and cash', 'Unused weight earns a modeled 6.5% p.a. liquid-fund rate; 0.30% one-way turnover cost. No capacity cap by default.', 'Same cash-rate and cost assumptions; actual modeled opening trades and drifting weights drive transaction costs. No default capacity cap.'],
      ['Market and volatility risk', 'Benchmark = equal-weight daily returns of loaded OHLCV symbols with a fundamentals filename, not Nifty. Bear multiplier 0.8; volatility target 20%.', 'Same benchmark; bear multiplier 0.5; volatility target 22%. Both use correlation guard, monthly panic exposure and daily crash guard.'],
      ['Stop loss', '15% below entry and 20% below peak close; tighter effective stop ratchets up. Checked at close after five calendar days, executed at the next valid open.', 'Same. No ATR chandelier stop or fixed take-profit by default. Gap can produce a worse fill than the trigger.'],
      ['Re-entry cooldown', 'Losing stop: 20 × loss % / 10, capped at 10–60 calendar days. Crash guard imposes a separate 10-session portfolio cooldown.', 'Same. Profitable stop has no loss-scaled cooldown by default.'],
      ['Exit logic', 'Close-confirmed stop, persistent monthly target drop, crash guard, or final-period mark. Fundamental eligibility failure can be delayed by the rebalance buffer.', 'Same exit types, with the longer three-drop buffer. End-of-period marks are not sales.'],
      ['Return accounting', 'Target-weight based; daily target reweighting / turnover limitation remains in the normal runner. Full exits have zero exit-day stock weight.', 'Execution book marks open/close holdings and charges modeled trades. Reported returns attribute overnight/intraday holdings, but omit full-exit stock contribution on exit day.']]))

    add('''## Reading the answer\n\n**The result depends on the technical comparison.** In both engines, the fundamental strategy beat pullback-only ranking on the same fundamentally eligible stocks. Against the broader price-trend control, however, both fundamental versions had lower CAGR and deeper drawdown in this history. They had higher closed-trade win rates, illustrating that a higher win rate does not necessarily produce a higher portfolio return. See the numerical comparisons and winner sizes below.\n\nThese tests measure historical associations under specified controls; they do not establish that fundamentals universally cause better results or predict future performance. The two production versions have different risk settings and accounting, so compare cases **within the same engine**, not across the normal and experimental columns. The sample and parameters were previously researched; 2022–2024 is a previously examined comparison, not an untouched holdout.\n\n[[PERFORMANCE_CHART]]''')
    add('''## How the analysis separates fundamentals from OHLCV\n\n1. **Fundamental strategy**: the version's current ranking and quarterly eligibility checks.\n2. **Pullback · common eligible**: replace its fundamental ranking with the experimental version's OHLCV pullback rank but keep the same monthly, point-in-time fundamental eligibility. This tests the ranking change *conditional on the fundamental screen*; it is not a no-fundamentals portfolio.\n3. **Pullback · price-only rules**: use the same pullback score but remove quarterly-profit, earnings-yield, filing-age and share-count eligibility; keep the OHLCV price/circuit/falling-knife rules.\n4. **Trend · price-only rules**: rank the same A3/Q5 price-strength inputs in the opposite direction, preferring stronger rather than weaker price action; retain the same price-only eligibility.\n\nEach comparison retains that version's max positions, stops, timing, portfolio/risk rules, cash and cost assumptions. The technical tests begin at the same first eligible signal month as the fundamental strategy, July 2019. Both price-only controls still use the fixed list of OHLCV symbols that have a fundamentals file and at least one available quarterly-result record in the historical corpus, plus the available NSE valuation-price symbol list. This is not a point-in-time, unrestricted market universe; the list can have survivorship and future-membership bias. The tests therefore do not measure fundamentals in every possible technical strategy. A3/Q5 use forward-filled closes and neutral ranks for missing secondary inputs, matching the existing experimental construction.\n\n```mermaid\nflowchart LR\n    A[OHLCV + matching stock files] --> B[Price and circuit checks]\n    B --> C[Fundamental eligibility]\n    C --> D[E/P or value + growth + pullback rank]\n    C --> E[Control: pullback rank on same eligible set]\n    B --> F[Controls: pullback or trend rank without quarterly screens]\n    D --> G[Same version-specific selection and execution]\n    E --> G\n    F --> G\n```''')

    rows=[]
    for version in ('normal','experimental'):
        for case in CASES:
            m=R[(version,case)]['windows']['full']
            rows.append([version.title(),NAMES[case],pct(m['cagr']),pct(m['max_drawdown']),num(m['sharpe']),pct(m['exposure']),pct(m['annual_turnover'])])
    add('## Portfolio results: each control uses the same engine as its baseline\n\n'+table(['Engine','Selection','CAGR','Max DD','Sharpe','Avg stock exposure','Annual turnover'],rows))
    add('CAGR and drawdown use the 3 June 2019–31 December 2024 daily return stream. The comparison compounds the first reporting-day return; the normal runner’s printed CAGR can differ by about 0.01 percentage points because it rebases at the first close. Turnover is total absolute buy plus sell weight changes. Normal turnover is the older target-weight estimate; experimental turnover is actual modeled open-trade turnover. Both assume 0.30% one-way cost and a 6.5% annual return on modeled idle cash.')
    add('[[PATHS_CHART]]')

    rows=[]
    for version in ('normal','experimental'):
        for case in CASES:
            m=R[(version,case)]['windows']['full']
            rows.append([version.title(),NAMES[case],m['closed'],f"{m['winners']} / {pct(m['win_rate'])}",f"{m['losers']} / {pct(m['loss_rate'])}",m['flat'],per(m['mean_win_pct']),per(m['mean_loss_pct'])])
    add('## Winners and losers: closed-trade price returns\n\n'+table(['Engine','Selection','Closed','Winners / rate','Losers / rate','Flat','Mean winner','Mean loser'],rows))
    add('A winner is a completed position with entry-to-exit price return > 0; a loser is < 0; flat equals 0. Rates use closed positions including flats in the denominator. Positions still open on 31 December 2024 are excluded. The return is an **unweighted price change**, not portfolio contribution or net return after all costs. Trade counts differ because the strategies enter different stocks and exit on different dates; a larger winner count alone does not establish improvement.')
    add('[[OUTCOMES_CHART]]')

    rows=[]
    for version in ('normal','experimental'):
        f=R[(version,'fundamental')]['windows']['full']
        for case in CASES[1:]:
            c=R[(version,case)]['windows']['full']
            rows.append([version.title(),NAMES[case],signed_pp((f['win_rate']-c['win_rate'])*100),signed_pp((f['loss_rate']-c['loss_rate'])*100),signed_pp(f['mean_win_pct']-c['mean_win_pct']),signed_pp(f['mean_loss_pct']-c['mean_loss_pct']),signed_pp((f['cagr']-c['cagr'])*100),signed_pp((f['max_drawdown']-c['max_drawdown'])*100)])
    add('## Incremental differences: fundamental minus each control\n\n'+table(['Engine','Control','Winner-rate Δ','Loser-rate Δ','Mean winner Δ','Mean loser Δ','CAGR Δ','Max-DD Δ'],rows))
    add('Differences are in percentage points. Positive max-DD Δ means the fundamental version had a smaller drawdown because drawdown is shown as a negative number. A positive mean-loser Δ means its average losing price return was less negative. These are descriptive strategy-level differences, not causal estimates: signals change which stocks are held, their weights, entry dates, exit dates, exposure and transaction costs.')

    rows=[]
    for v in ('normal','experimental'):
        for c in ('pullback_common','pullback_price_only','trend_price_only'):
            m=pair_entries(v,c)
            rows.append([v.title(),NAMES[c],m['matched'],m['both_win'],m['fund_only_win'],m['control_only_win'],m['neither_win'],signed_pp(m['mean_delta'])])
    add('### Matched stock-and-entry-date outcomes\n\n'+table(['Engine','Control','Matched entries','Both win','Only fundamental wins','Only control wins','Neither wins','Mean trade-return Δ'],rows))
    add('A match uses the same ticker and entry date and excludes end-of-period marks. Exit dates can differ, so the return difference includes exit timing. A zero count means there were no directly matched entries for that pair. The matched subset omits all non-overlapping selections and is not representative of the entire opportunity set.')

    rows=[]
    for version in ('normal','experimental'):
        for case in CASES:
            rec=R[(version,case)]
            for window in ('development','previously_examined_2022_2024','year_2024'):
                m=rec['windows'][window]
                rows.append([version.title(),NAMES[case],{'development':'2019–21','previously_examined_2022_2024':'2022–24 (examined)','year_2024':'2024'}[window],pct(m['cagr']),pct(m['max_drawdown']),pct(m['win_rate']),m['closed']])
    add('## Period breakdown\n\n'+table(['Engine','Selection','Period','CAGR','Max DD','Win rate','Closed'],rows))
    add('Windows are slices of full-path portfolios, not fresh portfolios initialized on each boundary. Closed-trade windows require both entry and exit inside the window; an entry before the start or a position still open at the end is excluded from that window’s trade statistics. Both 2019–2021 and 2022–2024 influenced prior research.')

    rows=[]
    for v in ('normal','experimental'):
        for c in ('pullback_common','trend_price_only'):
            low,mid,high,freq=boot_spread(returns,v,c)
            rows.append([v.title(),NAMES[c],signed_pp(low*100),signed_pp(mid*100),signed_pp(high*100),pct(freq)])
    add('### Paired return-stream sensitivity\n\n'+table(['Engine','Control','2.5th percentile CAGR Δ','Median Δ','97.5th percentile Δ','Samples with Δ > 0'],rows))
    add('This resamples the already-realized paired daily return streams with 1,500 circular blocks of 126 sessions and a fixed seed. It does not rerun stock selection on a resampled market, correct for strategy search, or produce the probability of future outperformance. These are descriptive sensitivity ranges, not independent confidence intervals.')

    add('## Trade-log deep dive: current fundamental versions')
    for version in ('normal','experimental'):
        r=R[(version,'fundamental')];m=r['windows']['full'];g=r['trade_groups'];d=closed(version,'fundamental')
        good=d[d.PnL_Pct>0];bad=d[d.PnL_Pct<0]
        top10=float(good.nlargest(min(10,len(good)),'PnL_Pct').PnL_Pct.sum()/good.PnL_Pct.sum()) if len(good) and good.PnL_Pct.sum()!=0 else np.nan
        add(f"### {version.title()} value strategy\n\nCompleted positions: **{m['closed']}**. Median trade return: **{per(m['median_pnl_pct'])}**; mean/median holding: **{m['mean_holding_days']:.1f} / {m['median_holding_days']:.1f} calendar days**. Median earnings yield at entry was **{pct(good.EP_At_Entry.median())}** for winners and **{pct(bad.EP_At_Entry.median())}** for losers. The ten highest-return winners represent **{pct(top10)}** of the sum of positive *unweighted trade percentage returns*; this is not their share of portfolio profit.")
        if version=='experimental':
            net=d.PnL_Abs.dropna(); nwin=int((net>0).sum()); nloss=int((net<0).sum())
            add(f"The experimental execution-book trade log shows **{nwin}/{len(net)} ({pct(nwin/len(net))})** positive rupee-P&L positions and **{nloss}/{len(net)} ({pct(nloss/len(net))})** negative positions after modeled trading fees. This is an execution-book measure; it does not equal the reported portfolio’s zero-exit-day return convention. Normal-version rupee P&L is an estimate under its older accounting and is not compared to this figure.")
        add(f"Among winners, median maximum adverse excursion was **{per(good.MAE_Pct.median())}** and median maximum favorable excursion was **{per(good.MFE_Pct.median())}**. For losers the corresponding medians were **{per(bad.MAE_Pct.median())}** and **{per(bad.MFE_Pct.median())}**. These entry-to-intraday-low/high path measures are descriptive and can differ from the close-based stop trigger.")
        sr=[[x['group'],x['n'],pct(x['win_rate']),per(x['mean_pnl_pct']),f"{x['mean_days']:.1f}"] for x in g['Exit_Reason']]
        add('**Exit reasons**\n\n'+table(['Reason','Closed','Win rate','Mean price return','Mean calendar days'],sr))
        det=[[x['group'],x['n'],pct(x['win_rate']),per(x['mean_pnl_pct']),f"{x['mean_days']:.1f}"] for x in g['Exit_Detail']]
        add('**Exit details**\n\n'+table(['Detail','Closed','Win rate','Mean price return','Mean calendar days'],det))
        hr=[[x['group'],x['n'],pct(x['win_rate']),per(x['mean_pnl_pct'])] for x in g['holding_bands']]
        add('**Holding-period bands**\n\n'+table(['Days held','Closed','Win rate','Mean price return'],hr))
        rg=[[x['group'],x['n'],pct(x['win_rate']),per(x['mean_pnl_pct']),f"{x['mean_days']:.0f}"] for x in g['Regime_At_Entry']]
        add('**Entry regime**\n\n'+table(['Regime','Closed','Win rate','Mean price return','Mean days'],rg))
        is_sme=d.Ticker.isin(sme); n=int(is_sme.sum())
        add(f"**SME-file check:** {n} of {len(d)} completed positions ({pct(n/len(d))}) match a ticker filename in `fundamentals/sme/`. This is a filename-based indicator, not a historical exchange-board classification; half-year-only filings generally fail the four-quarter requirement.")
        for title,kind in [('Largest positive price-return trades','best'),('Largest negative price-return trades','worst')]:
            vals=g[kind][:5]
            tb=[[x['Ticker'],x['Entry_Date'][:10],x['Exit_Date'][:10],per(x['PnL_Pct']),x['Holding_Days'],x['Exit_Reason']] for x in vals]
            add(f'**{title}**\n\n'+table(['Ticker','Entry','Exit','Price return','Calendar days','Exit'],tb))

    add('Holding bands and exit reasons are known only after the trade ends. Stops naturally remove many losing positions early while successful trades can remain open longer. A higher win rate in a longer holding band does not establish that forcing a stock to be held longer would improve its outcome. Likewise, the high win rate among rebalance exits is not an independent signal available at entry.')

    add('## Earnings yield and profit growth inside the selected trades')
    for v in ('normal','experimental'):
        add(f'### {v.title()}: earnings-yield quartiles at entry\n\n'+table(['Retrospective E/P range','Closed','Win rate','Mean price return','Mean days'],factor_bins(v,'EP_At_Entry')))
    add('Quartiles are calculated retrospectively across all closed positions, not within each month and not available as fixed thresholds at the historical entry date. These are descriptive associations among already-selected trades, not evidence that changing an E/P threshold would improve the strategy. E/P is in decimal units: 0.10 means 10%. E/P and its market-cap denominator can be affected by stale shares, corporate actions, issuer revisions and exceptional profits.')
    add('### Experimental: quarterly-profit-growth quartiles at entry\n\n'+table(['Retrospective symmetric growth range','Closed','Win rate','Mean price return','Mean days'],factor_bins('experimental','PROFIT_GROWTH_At_Entry')))
    add('Profit growth is `(current-quarter profit − year-ago profit) / ((abs(current) + abs(previous)) / 2)`, not conventional percentage growth. A positive value can include a move from a larger loss to a smaller loss; TTM net profit must still be positive.')

    add('''## Interpretation and limitations\n\n- **Fundamental contribution is conditional.** The common-eligible control isolates replacing the composite ranking while keeping fundamental screening; price-only controls remove the screen and ranking together. Neither design proves a universal fundamental alpha or a causal effect on an individual stock.\n- **The comparison benchmark matters.** Pullback and trend use the same price inputs in opposite directions. A fundamental strategy can beat one and lose to the other; this distinction is part of the result.\n- **The sample is not independent.** Strategy, limits, stops and ranking were selected after repeated work on 2019–2024. Multiple-signal selection and repeated trials can overstate the strength of historical results; see [Novy-Marx, Backtesting Strategies Based on Multiple Signals](https://www.nber.org/papers/w21329).\n- **Accounting differs.** The normal runner still holds target weights and misses turnover caused by weight drift. The experimental runner models opening trades, but its requested zero exit-day stock contribution means reported equity is not the execution book’s P&L. A winner’s entry/exit return is not the same as its contribution to reported CAGR.\n- **Data and execution remain material.** The current security list can exclude delisted stocks and includes future file membership. Historical filings may have overwritten revisions; corporate actions, stale prices, unusual gains and split/share units can distort E/P and returns. Most half-year SME reports fail the quarterly requirement. There is no default trading-capacity limit, and fixed 0.30% costs do not model market impact or actual fills.\n- **No post-2024 data is used.** A fresh, independently sourced period and execution/volume validation would be needed to establish whether an observed difference survives outside the research sample.''')

    add('''## Reproduce and inspect\n\nThe calculations use the local `csm_value/csm_value_strategy.py`, `csm_value/run_csm_value_backtest.py`, `csm_value/csm_value_experimental_strategy.py`, and `csm_value/run_csm_value_experimental_backtest.py`; the raw fundamentals are in `fundamentals/`, daily OHLCV in `/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data`, and NSE as-traded month-end prices in `csm_value/data/nse_monthly_prices.csv`. The analysis was produced by `research/csm_value_studies/notion_fundamental_analysis.py` and the companion builder.\n\n[[DATA_ATTACHMENTS]]''')

    # Compact underlying closed-trade records for independent inspection.
    cols=['Ticker','Entry_Date','Exit_Date','Entry_Price','Exit_Price','PnL_Pct','PnL_Abs','Holding_Days','Exit_Reason','Exit_Detail','Regime_At_Entry','EP_At_Entry','PROFIT_GROWTH_At_Entry','PULLBACK_At_Entry']
    for version in ('normal','experimental'):
        chunks=[]
        for case in CASES:
            frame=closed(version,case).reindex(columns=cols)
            frame.insert(0,'Case',case)
            chunks.append(frame)
        pd.concat(chunks,ignore_index=True).to_csv(OUT/f'{version}_closed_trades.csv',index=False)
    pd.DataFrame([{'version':r['version'],'case':r['case'], **r['windows']['full']} for r in DATA]).drop(columns=['exit_counts']).to_csv(OUT/'comparison_summary.csv',index=False)
    (OUT/'NOTION_REPORT.md').write_text('\n\n'.join(parts)+'\n')
    print('REPORT', OUT/'NOTION_REPORT.md')
    for f in ('performance.svg','trade_outcomes.svg','portfolio_paths.svg','normal_closed_trades.csv','experimental_closed_trades.csv','comparison_summary.csv'):
        print(f, (OUT/f).stat().st_size)


if __name__=='__main__': main()
