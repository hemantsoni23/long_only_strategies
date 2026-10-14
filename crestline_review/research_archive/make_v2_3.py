"""Builds crestline_v2_3.py (the FIXED BASELINE) from crestline_lab.py. Only correctness/realism fixes; strategy logic is unchanged."""
import os
here = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(here, "crestline_lab.py")).read()
def sub(old, new, count=1):
    global s
    assert s.count(old) == count, (s.count(old), old[:70]); s = s.replace(old, new)

sub('STRATEGY_NAME        = "CRESTLINE_V2_2"', 'STRATEGY_NAME        = "CRESTLINE_V2_3"')
sub('START_DATE           = "2015-01-01"', 'START_DATE           = "2006-01-01"   # v2.2 used 2015, which hides 2008-09; use anchors via CRESTLINE_OFFSET / anchor_report.py')
sub('CASH_RATE_ANNUAL     = 0.00', 'CASH_RATE_ANNUAL     = 0.065          # idle cash swept to a liquid fund (live must actually do this)')
sub('CA_ADJUST            = False            # True: back-adjust history for flagged jumps (split-neutral positions) instead of masking',
    'CA_ADJUST            = True             # back-adjust history at flagged jumps (split-neutral positions); False = v2.2 masking (books splits as real losses)')
# dead switch: entry weights are capped at 1/TOP_N so inverse-vol sizing can never bind
sub('SIZE_BY_VOL          = False            # True: entry weight proportional to 1/ATR% (cap/ADV rules unchanged)\n', '')
sub('''                    raw_w = np.ones(len(cids))
                    if SIZE_BY_VOL:
                        a_ = atr_pct_sig[k][cids]
                        raw_w = np.where(np.isfinite(a_) & (a_ > 0), 1.0 / np.where(a_ > 0, a_, 1.0), np.nan)
                        raw_w = np.where(np.isnan(raw_w), np.nanmedian(raw_w), raw_w)
                    w_int = allocate(raw_w, caps)''', '''                    w_int = allocate(np.ones(len(cids)), caps)''')
header = '''"""
crestline_v2_3.py -- CRESTLINE v2.3 : the FIXED BASELINE of v2.2 (strategy logic unchanged)
============================================================================================
Derived from Crestine/crestline_v2_2.py (colleague's file, untouched) via crestline_review/make_lab.py + make_v2_3.py.
Signal, universe, ranking, sizing, stops, schedule and overlay are exactly v2.2. What changed (see crestline_review/REVIEW.md s.3):

  FIX 1  CA_ADJUST (default True)  Vendor OHLCV holds ~680 unadjusted down-jumps (splits/bonuses) and ~230 up-jumps. v2.2 only masked
         those cells, so a position HELD through one booked the split as a real -50..-90% loss (INNOVTEC -89%, AIRAN -81% ...), and the
         hard stop fired on it. v2.3 back-adjusts price history and divides volume at every flagged jump; positions are split-neutral.
  FIX 2  CASH_RATE_ANNUAL = 6.5%   v2.2 booked 0% on ~48% idle capital. Live has to sweep idle cash to a liquid fund / LIQUIDBEES.
  FIX 3  START_DATE = 2006         2015 hid 2008-09 (-28%). v2.2's first-year buffer is unchanged.
  FIX 4  anchor_report.py          v2.2's headline is a single 60-bar schedule anchor (the best of six). Always quote the distribution
         over CRESTLINE_OFFSET in {0,10,..,50} and the staggered 6-anchor blend.
  CLEAN  removed SIZE_BY_VOL (could never bind: weights are capped at 1/TOP_N).

Reproduce v2.2 exactly:  CL_OVR='{"CA_ADJUST": false, "CASH_RATE_ANNUAL": 0.0, "START_DATE": "2015-01-01"}' python3 crestline_v2_3.py
Lab switches kept for later experiments (all default OFF = v2.2 logic): SCORE_W_HP/TP, RESID_W, M3_EXCL_Q, BEAR_NO_ENTRY.
Env: CL_OVR (JSON config overrides), CL_OUT (output dir), CRESTLINE_OFFSET (schedule anchor).

KNOWN LIMITATIONS NOT FIXED (unchanged v2.2 behaviour): INITIAL_CAPITAL=1 lakh so the 5%-ADV cap never binds (set it to the real book size); a capped slot is left
idle instead of walking down the rank list; fills ignore locked circuits and impact (flat 0.3%/side); overlay scales new entries only; pre-2020 volume is thin.
"""
'''
# replace the original module docstring (everything up to the first 'import os')
i = s.index("import os\nimport glob")
s = header + "\n" + s[i:]
s = s.replace('"crestline_v2_2_output"', '"crestline_v2_3_output"')
open(os.path.join(here, "crestline_v2_3.py"), "w").write(s)
print("ok", len(s))
