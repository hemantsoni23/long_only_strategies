import os, sys
import numpy as np, pandas as pd
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
plt.rcParams.update({'font.family': 'sans-serif', 'font.size': 9, 'axes.edgecolor': '#c3c2b7', 'axes.linewidth': .8, 'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.grid': True, 'grid.color': '#ecebe7', 'grid.linewidth': .6, 'axes.axisbelow': True, 'figure.facecolor': '#fcfcfb', 'axes.facecolor': '#fcfcfb',
                     'text.color': '#0b0b0b', 'axes.labelcolor': '#52514e', 'xtick.color': '#52514e', 'ytick.color': '#52514e'})
CAT = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4', '#6250d6']
def short(l):
    a, b = l.split('→'); return f"{a[:4]}–{b[2:4]}"
# fig6: P&L by chunk
b1 = pd.read_csv('results/b1_pnl_chunks.csv'); names = {'hr_faithful': 'HR breakout', 'vcp_faithful': 'VCP', 'elendel': 'CSM Elendel', 'zenith': 'CSM Zenith', 'quad': 'CSM Quad'}
chunks = [c for c in b1.chunk.unique() if c != 'ALL']
fig, axs = plt.subplots(1, 2, figsize=(13, 4.8), gridspec_kw={'width_ratios': [2.3, 1]})
ax = axs[0]; wd = 0.14; x = np.arange(len(chunks))
nif = b1[b1.strategy == 'hr_faithful'].set_index('chunk').bench_cagr
for i, (k, lab) in enumerate(names.items()):
    d = b1[b1.strategy == k].set_index('chunk'); ax.bar(x + (i - 2) * wd, [d.cagr.get(c, np.nan) * 100 for c in chunks], wd * .92, color=CAT[i], label=lab)
ax.plot(x, [nif[c] * 100 for c in chunks], color='#0b0b0b', marker='o', ms=4, lw=1.4, label='Nifty 500 (price)')
ax.axhline(0, color='#c3c2b7', lw=.8); ax.set_xticks(x); ax.set_xticklabels([short(c) for c in chunks]); ax.set_ylabel('CAGR, %')
ax.set_title('Faithful-booked CAGR by 3-year chunk (identical windows)', loc='left', fontsize=10.5, fontweight='bold'); ax.legend(frameon=False, ncol=3, fontsize=8)
ax = axs[1]; allc = b1[b1.chunk == 'ALL'].set_index('strategy')
labs = ['hr_engine', 'hr_faithful', 'vcp_engine', 'vcp_faithful']; cols = ['#b7c9e6', CAT[0], '#f2bba3', CAT[1]]
ax.bar(range(4), [allc.loc[l, 'cagr'] * 100 for l in labs], color=cols, width=.65)
for i, l in enumerate(labs): ax.text(i, allc.loc[l, 'cagr'] * 100 + .8, f"{allc.loc[l, 'cagr'] * 100:.0f}%", ha='center', fontsize=8.5)
ax.set_xticks(range(4)); ax.set_xticklabels(['HR\nengine', 'HR\nfaithful', 'VCP\nengine', 'VCP\nfaithful']); ax.set_title('Engine vs faithful booking, 2008–26', loc='left', fontsize=10.5, fontweight='bold'); ax.margins(y=.12)
fig.tight_layout(); fig.savefig('charts/fig6_pnl_faithful.png', dpi=160); plt.close(fig)
# fig7: ablations
a = pd.read_csv('results/b3_ablations.csv'); fig, axs = plt.subplots(1, 2, figsize=(12, 4.3))
for ax, w, t in zip(axs, ('hr', 'vcp'), ('HR breakout', 'VCP')):
    d = a[a.strategy == w]; order = ['base', 'nopattern', 'noregime', 'notrend']; lab = ['live (all three)', 'no pattern', 'no regime filter', 'no trend gate']
    al = [d[(d.variant == v) & (d.chunk == 'ALL')].cagr.iloc[0] * 100 for v in order]; la = [d[(d.variant == v) & d.chunk.str.endswith('2026-05')].cagr.iloc[0] * 100 for v in order]
    x = np.arange(4); ax.bar(x - .18, al, .34, color=CAT[0], label='2008–26'); ax.bar(x + .18, la, .34, color=CAT[1], label='latest 3 years')
    for xi, (u, v) in enumerate(zip(al, la)): ax.text(xi - .18, u + .4, f'{u:.0f}', ha='center', fontsize=8); ax.text(xi + .18, v + .4, f'{v:.0f}', ha='center', fontsize=8)
    ax.set_xticks(x); ax.set_xticklabels(lab, fontsize=8.5); ax.set_title(f'{t}: faithful CAGR %, one component removed', loc='left', fontsize=10, fontweight='bold'); ax.legend(frameon=False, fontsize=8); ax.margins(y=.15)
fig.tight_layout(); fig.savefig('charts/fig7_ablation.png', dpi=160); plt.close(fig)
# fig8: terciles
c1 = pd.read_csv('results/c1_ic_terciles.csv'); c1.columns = ['chunk'] + list(c1.columns[1:])
books = ['absolute', 'batch', 'elendel', 'zenith', 'quad', 'residual']; bn = {'absolute': 'Absolute', 'batch': 'Batch', 'elendel': 'Elendel', 'zenith': 'Zenith', 'quad': 'Quad', 'residual': 'Residual'}
fig, axs = plt.subplots(1, 2, figsize=(12.5, 4.3))
for ax, by, ttl in zip(axs, ('vol', 'liq'), ('3m IC by stock-volatility tercile', '3m IC by liquidity tercile')):
    x = c1[c1.by == by]; pre = x[~x.chunk.str.endswith('2026-05') & ~x.chunk.str.endswith('2023-05')].groupby('book')[['low', 'mid', 'high']].mean()
    last = x[x.chunk.str.endswith('2026-05')].set_index('book')[['low', 'mid', 'high']]
    for i, b in enumerate(books):
        ax.plot([0, 1, 2], pre.loc[b], color=CAT[i], ls=':', lw=1.4, marker='o', ms=3); ax.plot([0, 1, 2], last.loc[b], color=CAT[i], lw=2, marker='o', ms=5, label=bn[b])
    ax.axhline(0, color='#c3c2b7', lw=.8); ax.set_xticks([0, 1, 2]); ax.set_xticklabels(['low', 'mid', 'high'] if by == 'vol' else ['least liquid', 'mid', 'most liquid']); ax.set_title(ttl + '  (dotted = before 2020, solid = latest 3y)', loc='left', fontsize=9.5, fontweight='bold')
axs[0].legend(frameon=False, ncol=3, fontsize=8)
fig.tight_layout(); fig.savefig('charts/fig8_terciles.png', dpi=160); plt.close(fig)
# fig9: variants / improvements
d = pd.read_csv('results/d_improvements.csv'); sel = ['incumbent', 'I2 residual R3b', 'I3 incumbent + R3b', 'I4 incumbent + 52w-high', 'I1 raw 12-1m return']
fig, axs = plt.subplots(1, 2, figsize=(13, 4.6), sharey=False)
for ax, col, ttl in zip(axs, ('exc_all', 'exc_last2'), ('Top-N basket excess per 3m, full history', 'Top-N basket excess per 3m, latest 6 years')):
    bk = ['absolute', 'batch', 'elendel', 'zenith', 'quad']; x = np.arange(len(bk)); w = 0.16
    for i, v in enumerate(sel):
        vals = [d[(d.book == b) & (d.variant == v)][col].iloc[0] * 100 for b in bk]; ax.bar(x + (i - 2) * w, vals, w * .92, color=['#9a9a95', CAT[0], CAT[2], CAT[3], '#e0b0b0'][i], label=v)
    ax.axhline(0, color='#c3c2b7', lw=.8); ax.set_xticks(x); ax.set_xticklabels([bn[b] + ' pool' for b in bk]); ax.set_title(ttl + ', %', loc='left', fontsize=10, fontweight='bold')
axs[0].legend(frameon=False, fontsize=7.5, ncol=1)
fig.tight_layout(); fig.savefig('charts/fig9_improvements.png', dpi=160); plt.close(fig)
print('ok')
