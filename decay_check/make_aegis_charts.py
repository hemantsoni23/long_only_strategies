import os, pickle, warnings
import numpy as np, pandas as pd
warnings.filterwarnings('ignore')
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(HERE, 'results'); AEG = os.path.join(os.path.dirname(HERE), 'csm_aegis')
plt.rcParams.update({'font.family': 'sans-serif', 'font.size': 9, 'axes.edgecolor': '#c3c2b7', 'axes.linewidth': .8, 'axes.spines.top': False, 'axes.spines.right': False, 'axes.grid': True,
                     'grid.color': '#ecebe7', 'grid.linewidth': .6, 'axes.axisbelow': True, 'figure.facecolor': '#fcfcfb', 'axes.facecolor': '#fcfcfb', 'text.color': '#0b0b0b', 'axes.labelcolor': '#52514e', 'xtick.color': '#52514e', 'ytick.color': '#52514e'})
CAT = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4', '#6250d6', '#9a9a95']
def short(l):
    a, b = l.split('→'); return f"{a[:4]}–{b[2:4]}"
# 1 heatmap
ch = pd.read_csv(f'{RES}/battery_chunks.csv'); ch = ch[(ch.h == 3) & (ch.metric == 'ic') & (ch.chunk != 'ALL')]
order = ['A1', 'A2', 'A3', 'A4', 'Q5', 'Q4', 'Q3', 'BASE', 'CTRL', 'R1', 'M3', 'V2', 'V1', 'M1', 'M2', 'Q1', 'Q2', 'T1']
ver = pd.read_csv(f'{RES}/battery_verdicts.csv').set_index('signal').verdict; ver2 = pd.read_csv(f'{RES}/battery_decay_peak_horizon.csv'); ver6 = ver2[ver2.h == 6].set_index('signal').verdict
chunks = ['2008-06→2011-05', '2011-06→2014-05', '2014-06→2017-05', '2017-06→2020-05', '2020-06→2023-05', '2023-06→2026-05']
M = ch.pivot_table(index='signal', columns='chunk', values='mean').reindex(order)[chunks]; T = ch.pivot_table(index='signal', columns='chunk', values='nw_t').reindex(order)[chunks]
fig, ax = plt.subplots(figsize=(11.5, 6.6)); im = ax.imshow(M.values, cmap='RdBu', vmin=-0.15, vmax=0.15, aspect='auto'); ax.grid(False)
for i in range(M.shape[0]):
    for j in range(M.shape[1]): ax.text(j, i, f"{M.values[i, j]:+.3f}\n(t {T.values[i, j]:.1f})", ha='center', va='center', fontsize=7.3, color='#0b0b0b')
    ax.text(len(chunks) - .35, i, f"3m: {ver.get(order[i], '')}", va='center', fontsize=7.5, color='#52514e'); ax.text(len(chunks) + 1.25, i, f"6m: {ver6.get(order[i], '–')}", va='center', fontsize=7.5, color='#52514e')
ax.set_xticks(range(len(chunks))); ax.set_xticklabels([short(c) for c in chunks]); ax.set_yticks(range(len(order))); ax.set_yticklabels(order)
ax.set_title('Signal decay: 3m IC (NW-t) by 3-year chunk, with the decay verdict at 3m and at 6m horizon', loc='left', fontsize=11, fontweight='bold'); ax.set_xlim(-.5, len(chunks) + 2.4)
fig.tight_layout(); fig.savefig(f'{AEG}/charts/fig1_signal_decay.png', dpi=160); plt.close(fig)
# 2 horizon profile
h = pd.read_csv(f'{RES}/battery_horizons.csv'); keys = ['A1', 'A2', 'A3', 'Q5', 'R1', 'BASE', 'M3', 'V2']
fig, ax = plt.subplots(figsize=(8.6, 4.4))
for i, k in enumerate(keys):
    d = h[h.signal == k].sort_values('h'); ax.plot(d.h, d['mean'], marker='o', lw=2, color=CAT[i % 7], ls='-' if i < 7 else '--', label=k)
ax.set_xticks([1, 3, 6, 12]); ax.set_xticklabels(['1m', '3m', '6m', '12m']); ax.set_ylabel('mean IC'); ax.legend(frameon=False, ncol=4, fontsize=8)
ax.set_title('Horizon profile: anchors peak at 6–12 months; R1 at 6m; M3 and V2 are short-horizon', loc='left', fontsize=10.5, fontweight='bold'); fig.tight_layout(); fig.savefig(f'{AEG}/charts/fig2_horizon.png', dpi=160); plt.close(fig)
# 3 equity vs nifty vs placebo
r = pd.read_csv(f'{AEG}/output/daily_returns_v1_0.csv', index_col=0, parse_dates=True).ret; r = r[r.index >= '2005-01-01']
nif = pd.read_parquet(os.path.join(AEG, 'data', 'nifty500_price_index.parquet'))['Nifty_500'].dropna().pct_change().reindex(r.index).fillna(0)
pl = pickle.load(open(os.path.join(HERE, '.cache', 'aegis_placebo_ret.pkl'), 'rb')) if os.path.exists(os.path.join(HERE, '.cache', 'aegis_placebo_ret.pkl')) else None
fig, ax = plt.subplots(figsize=(11, 4.6)); eq = (1 + r).cumprod(); ax.plot(eq.index, eq, color=CAT[0], lw=2, label='CSM Aegis (faithful)'); ax.plot(eq.index, (1 + nif).cumprod(), color='#0b0b0b', lw=1.4, label='Nifty 500 (price)')
if pl is not None:
    lo, hi, mid = pl.quantile(.05, axis=1), pl.quantile(.95, axis=1), pl.mean(axis=1); ax.fill_between(pl.index, lo, hi, color=CAT[1], alpha=.18, label='placebo 5–95% (random picks, same wrapper)'); ax.plot(pl.index, mid, color=CAT[1], lw=1.2)
ax.set_yscale('log'); ax.set_ylabel('growth of 1 (log)'); ax.legend(frameon=False, fontsize=8, loc='upper left'); ax.set_title('Equity curve vs Nifty 500 and the placebo band (unlimited-capacity ceiling; see capacity table)', loc='left', fontsize=10.5, fontweight='bold')
fig.tight_layout(); fig.savefig(f'{AEG}/charts/fig3_equity.png', dpi=160); plt.close(fig)
# 4 chunks
c = pd.read_csv(f'{RES}/aegis_chunks.csv'); cc = [x for x in c.chunk.unique() if x != 'ALL']; names = ['AEGIS(R1)', 'wrapper[ELEN]', 'wrapper[ZEN]', 'wrapper[BASE]', 'live Elendel', 'live Zenith', 'live Quad']
fig, ax = plt.subplots(figsize=(12, 4.6)); wd = 0.115; x = np.arange(len(cc))
for i, k in enumerate(names):
    d = c[c.strategy == k].set_index('chunk'); ax.bar(x + (i - 3) * wd, [d.cagr.get(z, np.nan) * 100 for z in cc], wd * .92, color=CAT[i], label=k)
nb = c[c.strategy == 'AEGIS(R1)'].set_index('chunk').bench_cagr; ax.plot(x, [nb[z] * 100 for z in cc], color='#0b0b0b', marker='o', ms=4, lw=1.3, label='Nifty 500 (price)'); ax.axhline(0, color='#c3c2b7', lw=.8)
ax.set_xticks(x); ax.set_xticklabels([short(z) for z in cc]); ax.set_ylabel('CAGR, %'); ax.legend(frameon=False, ncol=4, fontsize=8); ax.set_title('Faithful CAGR by 3-year chunk: new strategy, same wrapper on existing selectors, live books', loc='left', fontsize=10.5, fontweight='bold')
fig.tight_layout(); fig.savefig(f'{AEG}/charts/fig4_chunks.png', dpi=160); plt.close(fig)
# 5 ablation
s3 = pd.read_csv(f'{RES}/aegis_stage3.csv'); base = s3[s3.test == 'BASELINE'].iloc[0]; ab = s3[s3.test.str.startswith('ablation')].copy(); ab['dCAGR'] = (base.cagr - ab.cagr) * 100; ab['dSharpe'] = base.sharpe - ab.sharpe
pl_row = pd.read_csv(f'{RES}/aegis_bakeoff.csv').set_index('name').loc['placebo mean (100 random draws)']
fig, axs = plt.subplots(1, 2, figsize=(12, 4.4)); lab = [t.replace('ablation ', '') for t in ab.test]
axs[0].barh(lab, ab.dCAGR, color=[CAT[2] if v > 0 else CAT[1] for v in ab.dCAGR]); axs[0].axvline(0, color='#52514e', lw=.8); axs[0].set_title('CAGR points the component adds (baseline minus ablated)', loc='left', fontsize=10, fontweight='bold'); axs[0].invert_yaxis()
axs[1].barh(lab, ab.dSharpe, color=[CAT[2] if v > 0 else CAT[1] for v in ab.dSharpe]); axs[1].axvline(0, color='#52514e', lw=.8); axs[1].set_title('Sharpe the component adds', loc='left', fontsize=10, fontweight='bold'); axs[1].invert_yaxis()
fig.text(.01, .01, f"Selector vs placebo: R1 {base.cagr*100:.1f}% / Sharpe {base.sharpe:.2f} against random picks {pl_row.cagr*100:.1f}% / {pl_row.sharpe:.2f} with the identical wrapper.", fontsize=8.5, color='#52514e')
fig.tight_layout(rect=(0, .04, 1, 1)); fig.savefig(f'{AEG}/charts/fig5_ablation.png', dpi=160); plt.close(fig); print('ok')
