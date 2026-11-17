"""
execution_replay.py -- re-account an Elendel-chassis backtest with execution-faithful timing.

The engine (`_run_backtest_core`) books   net_return[i] = sum_s executed_weight[i, s] * close_to_close_return[i, s]   i.e. the weight of DAY i earns DAY i's full close-to-close return.
For a position that is bought at the OPEN of day i that credits the overnight gap (prev close -> open) the buyer never owned; for a position sold at the OPEN of day j the weight is already
zero on day j, so the gap from the previous close to the actual exit fill (average -5% on stop exits) is never charged.  This replay fixes only the boundary days of every closed trade:
    entry day i :  return = close_i / entry_fill - 1              (instead of close_i / close_{i-1} - 1)
    exit  day j :  weight carried from day j-1, return = exit_fill / close_{j-1} - 1   (instead of weight 0)
Everything else (sizing, signals, scaling, costs) is the engine's own.  END_OF_PERIOD trades are untouched.
"""
import numpy as np
import pandas as pd


def faithful_net_returns(csm, res, transaction_cost=0.003, daily_cash_rate=0.0):
    W = res['executed_weights'].copy()
    idx, cols = W.index, list(W.columns)
    col = {c: k for k, c in enumerate(cols)}
    px = csm.prices
    DR = px.pct_change(fill_method=None).fillna(0.0).reindex(index=idx, columns=cols).values.copy()   # engine's own daily returns
    Wv = W.values.copy(); W0 = W.values
    close_ff = px.ffill().reindex(index=idx, columns=cols).values
    n_adj_entry = n_adj_exit = 0
    for m in csm.position_metadata:
        s = col.get(m['Ticker'])
        if s is None:
            continue
        i = idx.get_loc(m['Entry_Date']); j = idx.get_loc(m['Exit_Date'])
        ep = m['Entry_Price']
        if ep and ep > 0 and close_ff[i, s] > 0:
            DR[i, s] = close_ff[i, s] / ep - 1.0; n_adj_entry += 1
        if m['Exit_Reason'] != 'END_OF_PERIOD' and j > 0 and W0[j, s] == 0.0 and W0[j - 1, s] > 0.0:
            xp = m['Exit_Price']
            pc = close_ff[j - 1, s]
            if xp and xp > 0 and pc > 0:
                Wv[j, s] = W0[j - 1, s]; DR[j, s] = xp / pc - 1.0; n_adj_exit += 1
    gross = (Wv * DR).sum(axis=1)
    cash_w = np.clip(1.0 - W0.sum(axis=1), 0, None)
    cost = np.abs(np.diff(W0, axis=0, prepend=0.0)).sum(axis=1) * transaction_cost
    net = pd.Series(gross + cash_w * daily_cash_rate - cost, index=idx)
    return net, dict(entries_adjusted=n_adj_entry, exits_adjusted=n_adj_exit)
