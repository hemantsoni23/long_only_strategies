import os, pickle, sys
import numpy as np, pandas as pd
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
plt.rcParams.update({'font.family': 'sans-serif', 'font.size': 9, 'axes.edgecolor': '#c3c2b7', 'axes.linewidth': .8,
                     'axes.spines.top': False, 'axes.spines.right': False, 'axes.grid': True, 'grid.color': '#ecebe7',
                     'grid.linewidth': .6, 'axes.axisbelow': True, 'figure.facecolor': '#fcfcfb', 'axes.facecolor': '#fcfcfb',
                     'text.color': '#0b0b0b', 'axes.labelcolor': '#52514e', 'xtick.color': '#52514e', 'ytick.color': '#52514e'})
CAT = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4', '#6250d6']
NAMES = {'residual': 'Residual momentum', 'absolute': 'CSM Absolute', 'batch': 'CSM Batch', 'elendel': 'CSM Elendel',
         'zenith': 'CSM Zenith', 'quad': 'CSM Quad'}
OUT = 'charts'
c = pd.read_csv('results/cs_chunks.csv'); S = pickle.load(open('.cache/cs_series.pkl', 'rb'))

def short(lab):
    a, b = lab.split('→'); return f"{a[:4]}-{b[2:4]}" if a[:4] != b[:4] else a

def shade(t):
    return '#9fc3ef' if t < 1 else ('#4f93e3' if t < 2 else '#1f5fae')

# 1: 3m IC by chunk
def bars(metric, h, fname, title, ylab, order=list(NAMES), ncols=3):
    fig, axs = plt.subplots(2, ncols, figsize=(12, 6.2), sharey=False)
    for ax, nm in zip(axs.flat, order):
        d = c[(c.strategy == nm) & (c.metric == metric) & (c.h == h) & (c.chunk != 'ALL')]
        a = c[(c.strategy == nm) & (c.metric == metric) & (c.h == h) & (c.chunk == 'ALL')].iloc[0]
        x = np.arange(len(d))
        ax.bar(x, d['mean'], color=[shade(t) for t in d.nw_t], width=.68)
        ax.axhline(a['mean'], color='#52514e', ls='--', lw=1)
        ax.axhline(0, color='#c3c2b7', lw=.8)
        for xi, (m, t) in enumerate(zip(d['mean'], d.nw_t)):
            ax.text(xi, m + (0.002 if m >= 0 else -0.002), f"t={t:.1f}", ha='center', va='bottom' if m >= 0 else 'top', fontsize=7.5, color='#52514e')
        ax.set_xticks(x); ax.set_xticklabels([short(l) for l in d.chunk], rotation=0, fontsize=7.5)
        ax.margins(y=0.16)
        ax.set_title(f"{NAMES[nm]}  (all-history {a['mean']:+.3f})", fontsize=9.5, loc='left')
        ax.grid(axis='x', visible=False)
    fig.suptitle(title, x=0.01, ha='left', fontsize=12, fontweight='bold')
    fig.text(0.01, 0.005, "36-month chunks anchored on the latest month (last chunk ends 2026-05).  Dashed = all-history mean.  Bar shade = Newey-West t: dark >=2, mid 1-2, light <1.", fontsize=8, color='#52514e')
    fig.tight_layout(rect=(0, .03, 1, .95)); fig.savefig(f'{OUT}/{fname}', dpi=160); plt.close(fig)

bars('ic', 3, 'fig1_ic3m_chunks.png', 'Signal decay: 3-month rank IC by 3-year chunk', 'IC')
bars('exc', 3, 'fig4_topN_excess_chunks.png', 'Does the top-N ranking beat its eligible universe? Top-N basket excess per 3 months, by chunk', 'excess')

# 2: horizon profile, latest vs prior vs all
fig, axs = plt.subplots(2, 3, figsize=(12, 6), sharey=True)
for ax, nm in zip(axs.flat, NAMES):
    d = c[(c.strategy == nm) & (c.metric == 'ic')]
    chunks = [x for x in d.chunk.unique() if x != 'ALL']
    for lab, ch, col, ls in (('latest 3y', chunks[-1], CAT[1], '-'), ('previous 3y', chunks[-2], CAT[3], '-'), ('2017-20 chunk' if False else 'all history', 'ALL', '#52514e', '--')):
        y = d[d.chunk == ch].sort_values('h')
        ax.plot(y.h, y['mean'], marker='o', ms=5, color=col, ls=ls, lw=2, label=lab)
    ax.axhline(0, color='#c3c2b7', lw=.8); ax.set_xticks(C.HORIZONS); ax.set_xticklabels([f'{h}m' for h in C.HORIZONS])
    ax.set_title(NAMES[nm], loc='left', fontsize=9.5)
axs[0, 0].legend(frameon=False, fontsize=8)
fig.suptitle('Horizon profile: IC vs forward horizon (latest 3y vs previous 3y vs all history)', x=.01, ha='left', fontsize=12, fontweight='bold')
fig.tight_layout(rect=(0, 0, 1, .95)); fig.savefig(f'{OUT}/fig2_horizon_profile.png', dpi=160); plt.close(fig)

# 3: rolling 36m mean IC (3m)
fig, ax = plt.subplots(figsize=(12, 5))
for col, nm in zip(CAT, NAMES):
    x = S[nm][3]['ic'].dropna(); x = x.loc[x.index[0] + 12:]
    rw = C.rolling_window_means(x); rw.index = rw.index.to_timestamp()
    ax.plot(rw.index, rw.values, color=col, lw=1.8, label=NAMES[nm])
ax.axhline(0, color='#52514e', lw=.9)
ax.set_ylabel('rolling 36-month mean of 3m IC'); ax.legend(frameon=False, ncol=3, fontsize=8.5, loc='upper left', bbox_to_anchor=(0.55, 1.0))
ax.set_title('Rolling 3-year IC: cyclical - today\'s level is close to the 2017-18 and 2009-10 troughs, not below them (except Quad)', loc='left', fontsize=12, fontweight='bold')
fig.tight_layout(); fig.savefig(f'{OUT}/fig3_rolling_ic.png', dpi=160); plt.close(fig)

# 5: events
e = pd.read_csv('results/ev_chunks.csv'); e = e[e.h == 20]
fig, axs = plt.subplots(2, 2, figsize=(12, 6.2))
for r, w in enumerate(('hr', 'vcp')):
    for k, (base, lab) in enumerate((('market', 'vs equal-weight market'), ('trend-peers', 'vs trend-gate peers (pattern-only edge)'))):
        ax = axs[r, k]; d = e[(e.strategy == w) & (e.base == base) & (e.chunk != 'ALL')]; a = e[(e.strategy == w) & (e.base == base) & (e.chunk == 'ALL')].iloc[0]
        x = np.arange(len(d)); ax.bar(x, d.mean_event * 100, color=[shade(t) for t in d.nw_t], width=.68)
        ax.axhline(a.mean_event * 100, color='#52514e', ls='--', lw=1); ax.axhline(0, color='#c3c2b7', lw=.8)
        for xi, (m, t, n) in enumerate(zip(d.mean_event * 100, d.nw_t, d.n_events)):
            ax.text(xi, m + (0.05 if m >= 0 else -0.05), f"t={t:.1f}\nn={n}", ha='center', va='bottom' if m >= 0 else 'top', fontsize=7, color='#52514e')
        ax.set_xticks(x); ax.set_xticklabels([short(l) for l in d.chunk], fontsize=7.5)
        ax.margins(y=0.25)
        ax.set_title(f"{'HR breakout' if w == 'hr' else 'VCP'} - {lab}  (all {a.mean_event * 100:+.2f}%)", loc='left', fontsize=9.5)
        ax.set_ylabel('mean 20-day excess, %'); ax.grid(axis='x', visible=False)
fig.suptitle('Breakout strategies: 20-trading-day excess return after the entry signal, by chunk', x=.01, ha='left', fontsize=12, fontweight='bold')
fig.tight_layout(rect=(0, 0, 1, .95)); fig.savefig(f'{OUT}/fig5_events.png', dpi=160); plt.close(fig)
print('ok')
