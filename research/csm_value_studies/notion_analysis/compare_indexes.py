"""Compare saved strategy portfolio values with local index closing levels."""
from pathlib import Path
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent / 'index_comparison'
INDEX = Path('/Users/hemantsoni/Documents/upstox_data_folder/index_data')
START, END = pd.Timestamp('2019-06-03'), pd.Timestamp('2024-12-31')
SOURCES = {
    'Normal value': (ROOT / 'csm_value/output/csm_value_ey_value_long_term_daily_log.csv', 'Portfolio_Value'),
    'Experimental value': (ROOT / 'csm_value/output/csm_value_ey_growth_pullback_experimental_long_term_drift_daily_log.csv', 'Portfolio_Value'),
    'Nifty 50': (INDEX / 'Nifty_50.csv', 'close'),
    'Nifty 500': (INDEX / 'Nifty_500.csv', 'close'),
    'Nifty Smallcap 250': (INDEX / 'NIFTY_SMLCAP_250.csv', 'close'),
}

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    series = {}
    for name, (path, column) in SOURCES.items():
        data = pd.read_csv(path, parse_dates=['datetime']).set_index('datetime').sort_index()
        assert not data.index.has_duplicates, f'{name}: duplicate dates'
        value = data.loc[START:END, column].astype(float)
        assert START in value.index and END in value.index, f'{name}: missing endpoint'
        assert value.notna().all() and (value > 0).all(), f'{name}: invalid values'
        series[name] = value / value.loc[START] * 100_000
    frame = pd.concat(series, axis=1)
    frame.index.name = 'date'
    frame.to_csv(OUT / 'daily_values.csv', float_format='%.6f')
    n_years = (END - START).days / 365.25
    results = []
    for name, s in series.items():
        results.append({'name': name, 'end_value': s.iloc[-1], 'total_pct': (s.iloc[-1] / s.iloc[0] - 1) * 100,
                        'annual_pct': ((s.iloc[-1] / s.iloc[0]) ** (1 / n_years) - 1) * 100,
                        'fall_pct': (s / s.cummax() - 1).min() * 100, 'observations': len(s)})
    pd.DataFrame(results).to_csv(OUT / 'summary.csv', index=False, float_format='%.6f')
    annual = {}
    for year in range(2019, 2025):
        annual[str(year)] = {}
        for name, s in series.items():
            current = s[s.index.year == year]
            previous = s[s.index.year < year]
            start_value = previous.iloc[-1] if len(previous) else s.iloc[0]
            annual[str(year)][name] = (current.iloc[-1] / start_value - 1) * 100
    pd.DataFrame(annual).T.to_csv(OUT / 'yearly_returns.csv', float_format='%.6f')
    missing = {name: [d.strftime('%Y-%m-%d') for d in series['Normal value'].index.difference(s.index)] for name, s in series.items()}
    (OUT / 'audit.json').write_text(json.dumps({'start': str(START.date()), 'end': str(END.date()), 'missing_dates_vs_normal': missing}, indent=2))

    plt.rcParams.update({'svg.fonttype': 'none', 'font.family': 'DejaVu Sans', 'font.size': 10})
    fig, ax = plt.subplots(figsize=(11.2, 5.8), layout='constrained')
    colors = {'Normal value': '#2563eb', 'Experimental value': '#7c3aed', 'Nifty 50': '#9ca3af',
              'Nifty 500': '#ca8a04', 'Nifty Smallcap 250': '#059669'}
    for name, s in series.items():
        # Include every observation: no missing-day interpolation in the underlying data.
        ax.plot(s.index, s / 100_000, label=name, color=colors[name],
                linewidth=2.2 if 'value' in name.lower() else 1.6)
    ax.set_title('How ₹1 lakh grew: strategies and market indexes', loc='left', fontsize=15, weight='bold', pad=18)
    ax.set_ylabel('Value in ₹ lakh')
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.1f}'))
    ax.grid(axis='y', alpha=.2)
    ax.spines[['top', 'right']].set_visible(False)
    ax.legend(ncol=3, loc='upper left', frameon=False, fontsize=9)
    fig.text(.125, -.025, '3 Jun 2019 to 31 Dec 2024. Index lines use closing levels; no dividends or fund costs.', fontsize=9, color='#4b5563')
    fig.savefig(OUT / 'growth_comparison.svg', bbox_inches='tight')
    fig.savefig(OUT / 'growth_comparison.png', dpi=140, bbox_inches='tight')
    print(pd.DataFrame(results).to_string(index=False))
    print('\nAnnual returns (%)')
    print(pd.DataFrame(annual).T.round(2).to_string())
    print('\nMissing dates:', missing)

if __name__ == '__main__':
    main()
