# Price Momentum and Trading Volume

**Charles M. C. Lee, Bhaskaran Swaminathan (Cornell) · 2000 · *Journal of Finance* 55(5), 2017–2069 · Source file `Finance/AbnormalReturnsMomentum_LeeSwaminathan_2000.pdf` (identical copy: `AbnormalReturnsMomentum2_LeeSwaminathan_2000.pdf`) · NYSE/AMEX stocks, Jan 1965–Dec 1995, price ≥ \$1, ≥2 yrs of history; Nasdaq-NMS 1983–96 holdout in a footnote**

## Claim / contribution
Past turnover links intermediate-horizon "momentum" and long-horizon "value":
1. **J–T momentum reverses in years 4–5.** For J=12, losses over years 2–5 (10.95%) almost offset the year-1 gain (11.56%). Part of momentum is therefore overreaction, not only underreaction.
2. **Low-turnover stocks outperform high-turnover stocks**, and the effect lasts 3–5 years. Low (high) volume stocks have value (glamour) characteristics and receive systematically positive (negative) earnings surprises over the next 8 quarters. This is mispricing, not a liquidity premium.
3. **Volume predicts both the size and the persistence of momentum.**
   - The momentum spread in year 1 is larger among *high*-volume stocks, driven by high-volume losers continuing to lose.
   - **High-volume winners and low-volume losers** ("late stage") reverse fast.
   - **Low-volume winners and high-volume losers** ("early stage") keep trending for about 3 years.
   - This is summarized as the "momentum life cycle" (MLC).

## Methodology
- Volume = average daily **turnover** (shares traded / shares outstanding, %) over the formation window $J$. It is essentially dollar volume scaled by market cap.
- Each month, stocks are sorted **independently** into 10 return deciles (R1–R10) on past $J$-month return and 3 volume terciles (V1 low … V3 high) on $J$-month turnover, giving 30 portfolios. Robustness partitions are 5×5 and 3×10.
- $J,K\in\{3,6,9,12\}$ months. Equal-weighted, J–T overlapping portfolios (1/K of the book revised monthly), **one-week skip** (a one-month skip gives similar results).
- Long horizon: annual event-time returns for years 1–5 with Hansen–Hodrick t-stats (11 lags). Returns are raw, industry-adjusted (25 two-digit-SIC groups), size-adjusted, or size-B/M-adjusted.
- Other tests:
  - FF3 time-series regressions;
  - Fama–MacBeth regressions of the year-$K$ return on the prior-year return, by subsample;
  - IBES and Compustat characteristics;
  - 4-day $[-2,+1]$ CARs around the next 8 earnings announcements;
  - change in volume $\Delta V=V(6,t)-V(t-4)$.
- Descriptive: extreme deciles trade more (J=6: R1 0.17%, R10 0.23% vs R5 0.12% daily turnover), and winners trade more than losers.

## Main results
**Simple momentum (Table I, % per month):**
- J=6/K=9: R10 1.65, R1 0.57, spread **1.08**.
- J=12/K=3: 1.54 (t=5.63).
- Year-1 spread 10.62–12.70% p.a.
- Years 2–3: small and insignificant. Years 4–5: significantly negative, e.g. J=12: −4.54% ($t$=−2.44) and −3.75% ($t$=−2.47).
- The reversal grows with $J$.

**Volume × momentum, first year (Table II, J=6, K=6, % per month):**
| | V1 (low) | V2 | V3 (high) | V3−V1 (t) |
|---|---|---|---|---|
| R1 losers | 1.12 | 0.67 | 0.09 | −1.04 (−5.19) |
| R10 winners | 1.67 | 1.78 | 1.55 | −0.12 (−0.67) |
| R10−R1 | **0.54** (2.07) | 1.11 | **1.46** (5.93) | **0.91** (4.61) |
- Low volume beats high volume in almost every cell. For J=9/K=6 the gap is 1.02%/mo among losers and 0.26% among winners.
- The larger momentum spread among high-volume names comes almost entirely from **losers**: R1V1 earns more than 1%/mo, while R1V3 earns −0.21% to +0.41%/mo.
- Buying high-volume winners does *not* help. The winner gap is small in year 1 and grows to 2–6% p.a. from year 2 onward.
- A volume-based liquidity story would predict the opposite of the larger spread in the more liquid, high-volume group.

**Robustness (Table III):**
- The pattern holds in all subperiods (1965–75, 1976–85, 1986–95) and is strongest in the latest one.
- 5×5 and 3×10 partitions give the same pattern or stronger.
- Largest 50% of NYSE/AMEX (5×5, J=K=6): spread **0.95% (V5) vs 0.24% (V1)**.
- Value-weighted: spreads 0.35 / 1.04 / 1.15%, with V3−V1 = 0.80% (significant at 1%).
- The Nasdaq-NMS holdout is stronger still.

**FF3 (Table V, J=K=6, α % per month):**
- R10−R1 α: **0.86 (V1), 1.42 (V2), 1.82 (V3)**; V3−V1 = 0.96 ($t$=5.00).
- The "early" combination R10V1 − R1V3 earns 1–2%/mo α.
- HML loadings fall with volume: R10V1 0.44 vs R10V3 −0.06. The difference of −0.51 is about the value–glamour spread in FF (1993). SMB loadings do not differ by volume.

**Long horizon (Tables VI–VII, J=6, annual %):**
| Strategy | Yr 1 | Yr 2 | Yr 3 | Yr 4 | Yr 5 |
|---|---|---|---|---|---|
| Simple R10−R1 | 12.49 (5.04) | −1.10 | −0.32 | −2.77 | −2.96 (−2.46) |
| Late R10V3−R1V1 | 6.84 (2.53) | −5.35 (−2.17) | −3.91 | −6.33 (−3.54) | −4.78 (−2.64) |
| Early R10V1−R1V3 | **16.70** (5.85) | 6.19 (3.16) | 5.85 (2.56) | 1.53 | −0.11 |
- Early minus simple is +4.21 / 7.29 / 6.17 / 4.29 / 2.85% over years 1–5 (significant in years 1–4). This survives industry adjustment (industry adjustment cuts year-1 simple momentum from 12.5% to 10.1%, about −20%, but leaves the volume effect intact) and size adjustment.
- The effect is weaker but present after size + B/M adjustment (early − simple: 3.54% in yr 1, 2.68% in yr 2) and in the top-50% subsample.
- Fama–MacBeth slopes of the year-$K$ return on the prior-year return:
  - all stocks: 0.067 ($t$=4.37) in year 1, about −0.03 (significant) in years 4–5;
  - early-stage stocks: 0.130 in year 1, still +0.063 ($t$=2.37) in year 3;
  - late-stage stocks: 0.023 in year 1, −0.037 ($t$=−3.11) in year 3.
  - Size-based stage definitions are weak and inconsistent, so volume is not a size proxy.

**Why it is not liquidity (Section IV):**
- Turnover's Spearman correlation with size is 0.20, with price 0.11, with relative spread −0.12.
- High-volume stocks earned *higher* returns in each of the 5 pre-formation years.
- Characteristics (Table IX, 5×5):
  - high- vs low-volume losers: analyst coverage 9.6 vs 3.6, IBES long-term growth 12.85% vs 9.33%, B/M 0.815 vs 1.125, ROE 11.3% vs 7.3%;
  - subsequent 3-year ΔROE is *worse* for high-volume stocks, although analysts forecast higher growth;
  - prior 5-year returns: low-volume winners 133.5% vs high-volume winners 247.6%; low-volume losers 29.0% vs high-volume losers 108.9%.
  - High-volume winners and low-volume losers are *long-term* winners/losers. Low-volume winners and high-volume losers are *recent* ones.
- Earnings-announcement CARs (Table X, 1974–95): R1V1 − R1V3 is about **+1.1% per announcement** for each of the next 8 quarters; R10V1 − R10V3 is 0.50–1.22%. Volume alone: V1 − V3 is about 0.6% per announcement in the future and ≈0 before formation. Because these are short-window returns, risk cannot explain them.
- $\Delta V$ (turnover change vs 4 years earlier; rank correlation with the level 0.48): the highest-ΔV quintile underperforms the lowest by 2–5% p.a. over 5 years, for winners and losers alike. Most of the predictive power comes from **ΔV, not lagged volume** (Table XII). This points to sentiment or attention rather than liquidity.

**Behavioral models:**
- Hong–Stein, with volume as a diffusion proxy, fits winners (low-volume winners trend more) but not losers.
- Daniel–Hirshleifer–Subrahmanyam and De Long et al., with volume as feedback trading, fit losers but not winners.
- Barberis–Shleifer–Vishny fits the analyst-extrapolation evidence.
- No single model fits everything. The MLC is offered as a heuristic: stocks cycle glamour → late-stage winner (high volume) → reversal → early-stage loser, and so on.

## Critical assessment
- **Strong points:** independent double sorts with many partitions; long-horizon event-time evidence; short-window earnings-announcement tests, which cleanly separate mispricing from risk; the ΔV test against liquidity.
- **Caveats:**
  - Equal-weighted portfolios in a 1965–95 NYSE/AMEX sample. The value-weighted and top-50% results are weaker.
  - Turnover conventions changed later (Nasdaq double counting, post-2000 HFT volume inflation), and later work finds the volume–momentum interaction attenuated.
  - Year 4–5 t-stats rely on overlapping annual returns with HH correction.
  - The MLC is descriptive, not a model.
  - The late-stage strategy is essentially a long-horizon contrarian bet embedded in momentum.
- **Corrections to the earlier summary:**
  - The momentum spread is larger among high-volume stocks because **high-volume losers keep losing**, not because high-volume winners continue. High-volume winners slightly *underperform* low-volume winners.
  - It is **low-volume losers**, not high-volume losers, that rebound quickly.
  - The main skip is one week (one month in robustness).

## Practical relevance for a quant PM
- Condition momentum on turnover:
  - on the short side, prefer high-volume losers;
  - on the long side, prefer low-volume winners (the "early" strategy: roughly +4 to +7% p.a. over simple momentum, with continuation for about 3 years, allowing slower turnover);
  - avoid shorting low-volume losers, which rebound strongly.
- Use **abnormal turnover** (level vs its own multi-year history) as a glamour/sentiment signal, with ≈0.6% per earnings announcement in drift. It complements B/M, analyst coverage and LTG as a value/glamour proxy that is only weakly correlated with size and spreads.
- Momentum sleeves carry embedded long-horizon reversal risk concentrated in high-volume winners. Time exits and holding periods accordingly.
