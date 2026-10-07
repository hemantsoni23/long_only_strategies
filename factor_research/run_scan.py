"""
run_scan.py -- build candidate factors, evaluate on each universe, write results/scan_<universe>.csv

usage:
  python3 run_scan.py --rebuild                  # build everything from scratch, evaluate everything
  python3 run_scan.py --add a,b,c                # build only a,b,c, merge into cached state, evaluate only those
  python3 run_scan.py --eval a,b                 # re-evaluate only these (already in cache)
Results are UPSERTED by factor name, so partial runs never drop earlier rows.
"""
import argparse
import os
import pickle
import time

import pandas as pd

from data import load_panels
from factors import build_all, FAMILY
from evaluate import build_universes, forward_returns, evaluate_factor, composite

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, '.cache')
RES = os.path.join(HERE, 'results')
os.makedirs(RES, exist_ok=True)
STATE = os.path.join(CACHE, 'state.pkl')


def load_state():
    with open(STATE, 'rb') as f:
        return pickle.load(f)


def save_state(st):
    with open(STATE, 'wb') as f:
        pickle.dump(st, f, protocol=4)


def build_state(names=None):
    t0 = time.time()
    P = load_panels()
    X, sig, F = build_all(P, names=names)
    print(f'[scan] factors built in {time.time()-t0:.0f}s', flush=True)
    return P, X, sig, F


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rebuild', action='store_true')
    ap.add_argument('--add', default=None)
    ap.add_argument('--eval', default=None)
    ap.add_argument('--universes', default='U1_liquid1000,U2_live_trend,U3_top300')
    a = ap.parse_args()

    if a.rebuild or not os.path.exists(STATE):
        P, X, sig, F = build_state(None)
        st = dict(sig=sig, F=F, FWD=forward_returns(X, sig), U=build_universes(X, sig))
        save_state(st)
        targets = None
    else:
        st = load_state()
        targets = None
        if a.add:
            names = set(a.add.split(','))
            P, X, sig, F = build_state(names)
            assert sig.equals(st['sig'])
            st['F'].update(F)
            save_state(st)
            targets = names
    if a.eval:
        targets = set(a.eval.split(','))

    sig, F, FWD, U = st['sig'], st['F'], st['FWD'], st['U']
    all_ic_path = os.path.join(CACHE, 'ic_series.pkl')
    all_ic = pickle.load(open(all_ic_path, 'rb')) if os.path.exists(all_ic_path) else {}

    for uname in a.universes.split(','):
        mask = U[uname]
        elend = composite(F, ['a3_rs_high', 'q5_126'], mask)
        zen = composite(F, ['a1_52wh', 'q5_189'], mask)
        items = [(n, f) for n, f in F.items() if targets is None or n in targets]
        if targets is None:
            items += [('LIVE_elendel(A3+Q5_126)', elend), ('LIVE_zenith(A1+Q5_189)', zen)]
        rows = []
        t0 = time.time()
        for name, fr in items:
            row, ics = evaluate_factor(name, fr, mask, FWD, base_rank=elend)
            row['family'] = FAMILY.get(name, 'LIVE')
            row['universe'] = uname
            rows.append(row)
            all_ic[(uname, name)] = ics
        new = pd.DataFrame(rows).set_index('factor')
        path = os.path.join(RES, f'scan_{uname}.csv')
        if os.path.exists(path) and targets is not None:
            old = pd.read_csv(path, index_col=0)
            old = old.drop(index=[i for i in new.index if i in old.index])
            new = pd.concat([old, new])
        new.to_csv(path, float_format='%.5f')
        print(f'[scan] {uname}: {len(rows)} factors evaluated in {time.time()-t0:.0f}s', flush=True)
    pickle.dump(all_ic, open(all_ic_path, 'wb'), protocol=4)


if __name__ == '__main__':
    main()
