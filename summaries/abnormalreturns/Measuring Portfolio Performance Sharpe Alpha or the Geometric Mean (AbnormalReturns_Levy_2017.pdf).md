# Measuring Portfolio Performance: Sharpe, Alpha, or the Geometric Mean? — Detailed Quantitative Research Notes

**Moshe Levy** (Hebrew University) · 2017 · *Journal of Investment Management* 15(3), pp. 1–17 · Source file: `Finance/AbnormalReturns_Levy_2017.pdf` (Drive id `1BgivK6TduMOLmtAeHTe469nHgoTCY5LM`)

## Question
Sharpe (1966, 1994): with normal returns and unlimited borrowing/lending at one risk-free rate, the Sharpe ratio ranks funds identically to expected utility for every risk-averse investor (later extended to all investors who prefer more to less, including Prospect Theory investors: Levy–Levy 2004; Levy–De Giorgi–Hens 2012). Real investors face (i) a borrowing rate well above the lending rate and (ii) a hard leverage cap (Reg T: borrow at most 100% of own capital, i.e. $x\le 2$). Once either holds, there is no longer a single measure that is optimal for all investors (Markowitz 2005). The paper asks which single number — Sharpe, Fama–French 5-factor alpha, or the geometric mean (GM) — best reproduces the ranking implied by direct expected-utility maximization under realistic financing. Motivation for needing *some* scalar: fund selection by investors who do not know their utility, manager evaluation/compensation, and setting the manager's objective.

Supporting facts cited: US bank interest margins ~4.2% (Saunders–Schumacher 2000, for 1995); prime 3.5% vs near-zero deposit rates (Jan 2016); aggregate margin debt below 10% of customer assets at all brokers examined and below 2.5% at Merrill, Paine Webber, Schwab; those who borrow typically use ~50% of Reg T capacity (Fortune 2000).

## Setup
Fund $j$ has empirical distribution $(R_i, p_i)_{i=1}^{120}$, $p_i=1/120$, of total monthly returns. Investor puts fraction $x$ in the fund:
$$EU(x)=\sum_{i=1}^{N}p_i\,U\!\big[W_0\big(xR_i+(1-x)R_f\big)\big],\qquad R_f=\begin{cases}R_f^L & x<1\\ R_f^B & x>1\end{cases},\quad x<2,$$
and the fund's "true" score is $EU(x^*)$. Base case: $R_f^L=0.82\%$, $R_f^B=4.32\%$ annual (sample averages, spread set to 3.5% "to be conservative").

Candidate measures:
- Sharpe $=(\sum_i p_iR_i - R_f^L)/\sigma(R)$ — lending rate in the numerator, as in practice.
- FF5 alpha from monthly regressions (Fama–French 2016 factors, Ken French library).
- $\mathrm{GM}=\prod_i R_i^{p_i}$, with $\mathrm{GM}\approx\mu-\sigma^2/2$ (Young–Trent 1969; Markowitz 2012).

Why GM is a natural candidate: $\log\mathrm{GM}=E[\log R]$ is the EU of a log (Bernoulli) investor at $x=1$, so the max-GM fund is always in the SSD-efficient set (Levy 2015); it is increasing in mean, decreasing in variance, and (at higher order) increasing in skewness; for i.i.d. returns and $H\to\infty$ the max-GM fund almost surely ends with more wealth (Kelly 1956; Latane 1959; Markowitz 1976), though it is EU-optimal only for $\alpha=1$ (Samuelson 1971; Merton–Samuelson 1974). Levy explicitly does not re-open the long-run debate; the claim is about GM as an *approximate* ranking at ordinary horizons.

Preferences: CRRA $W^{1-\alpha}/(1-\alpha)$, $\alpha\in\{0.5,\dots,2.5\}$ (empirically relevant range 1–2 per Arrow, Tobin–Dolde, Friend–Blume, Kydland–Prescott); generalized CRRA $(W+A)^{1-\alpha}/(1-\alpha)$ with $\alpha=1.5$, $A\in\{0.5,1,2\}$; negative exponential $-e^{-bW}$, $W_0=1$, $b\in\{0.01,0.1,1\}$.

Evaluation criteria:
1. Spearman correlation across funds between the measure and $EU(x^*)$.
2. "Wrong choice": in 1,000 random 10-fund menus, the share where the measure's top fund is not the EU-maximizer.
3. Average annual certainty-equivalent loss of those wrong choices: with $W_0=1$, $U(CE)=EU(x^*)$ for the chosen (A) and optimal (B) fund; loss $=CE_B^{12}-CE_A^{12}$ (endnote 9).

Distributions are treated as known (ex-post = ex-ante); estimation error is acknowledged but set aside as common to all measures.

## Data
- CRSP Survivor-Bias-Free Mutual Fund Database: all US domestic equity funds with complete monthly returns July 2005–June 2015, 10,145 funds; the analysis uses the 10,019 with $x^*>0$ (mean above the lending rate; all others have identical EU = all-cash). Results "almost identical" when incomplete-record funds are included.
- Robustness: all US hedge funds in the Thomson-Reuters database with complete records over the same window.

Median monthly moments (Table 1):

| | Mutual funds | Hedge funds |
|---|---:|---:|
| Mean | 0.59% | 0.49% |
| Std. dev. | 4.32% | 4.38% |
| Skewness | −0.75 | −0.57 |
| Kurtosis | 5.33 | 5.34 |
| JB rejects normality at 1% / 5% / 10% | 90.6 / 97.1 / 98.2% | 91.9 / 97.2 / 98.5% |

## Results

**Textbook financing (unlimited borrowing at $R_f^L$), CRRA 1.5.** Despite pervasive non-normality, Spearman(Sharpe, EU) = 0.998; wrong choice 7.7%; annual CE loss 0.04% — consistent with Levy–Markowitz (1979), Kroll–Levy–Markowitz (1984), Simaan (1993). Non-normality is not the problem.

**Realistic financing ($x<2$, 350 bp spread), CRRA 1.5, mutual funds.**

| Measure | Spearman with EU | Wrong choice (10-fund menu) | Ann. CE loss |
|---|---:|---:|---:|
| Sharpe | 0.372 | 82.5% | 4.22% |
| FF5 alpha | 0.188 | 69.8% | 2.61% |
| GM | 0.974 | 18.0% | 0.15% |

With 100-fund menus Sharpe picks wrong 98% of the time, CE loss 9.24%. GM's CE loss is ~28x smaller than Sharpe's and ~17x smaller than alpha's. Hedge funds (Fig. 6): Spearman 0.36 (Sharpe), 0.42 (alpha), 0.96 (GM).

**Mechanism (Fig. 7).** Top-10 Sharpe funds are low-$\sigma$; top-10 GM funds are high-$\mu$. Levering the Sharpe funds up to the GM funds' volatility would dominate them, but requires leverage of hundreds of percent. Sharpe's ranking is effectively driven by the denominator, GM's by the mean.

**Decomposition (Fig. 8, CRRA 1.5).**
- Panel A, rate spread only (no cap): Spearman(Sharpe, EU) falls monotonically with $R_f^B-R_f^L$ and levels off near 0.4; Spearman(GM, EU) *rises* with the spread. Crossover at a spread of **1.6%**. Alpha is below Sharpe throughout.
- Panel B, cap only (equal rates): Sharpe deteriorates as the cap tightens; GM deteriorates as the cap loosens (levered high-Sharpe funds become attainable). Crossover at a borrowing limit of about **120%** of capital — Reg T (100%) is already on the GM side. With both frictions, GM's advantage is larger still.

**Preference sweep (Table 2, realistic financing).** Entries: Spearman / wrong choice % / ann. CE loss %.

| Preference | Sharpe | FF5 alpha | GM |
|---|---|---|---|
| CRRA $\alpha=0.5$ | 0.173 / 88.5 / 8.65 | 0.034 / 74.2 / 5.64 | 0.995 / 0.7 / 0.00 |
| CRRA $\alpha=1.0$ | 0.279 / 82.9 / 5.79 | 0.116 / 73.3 / 3.87 | 0.992 / 20.2 / 0.11 |
| CRRA $\alpha=1.5$ | 0.372 / 82.5 / 4.22 | 0.188 / 69.8 / 2.61 | 0.974 / 18.0 / 0.15 |
| CRRA $\alpha=2.0$ | 0.479 / 80.3 / 3.07 | 0.273 / 68.1 / 2.00 | 0.934 / 23.4 / 0.18 |
| CRRA $\alpha=2.5$ | 0.586 / 78.6 / 2.36 | 0.365 / 67.4 / 1.54 | 0.873 / 34.2 / 0.26 |
| Gen. CRRA $A=0.5$ | 0.429 / 79.7 / 3.58 | 0.286 / 65.4 / 2.31 | 0.969 / 19.6 / 0.15 |
| Gen. CRRA $A=1$ | 0.344 / 79.6 / 4.52 | 0.225 / 67.2 / 2.99 | 0.989 / 20.3 / 0.13 |
| Gen. CRRA $A=2$ | 0.277 / 82.3 / 6.35 | 0.176 / 67.0 / 4.20 | 0.995 / 11.9 / 0.07 |
| NegExp $b=0.01$ | 0.058 / 89.6 / 11.29 | 0.056 / 71.8 / 7.01 | 0.957 / 19.2 / 0.23 |
| NegExp $b=0.1$ | 0.086 / 88.5 / 10.73 | 0.068 / 69.7 / 7.11 | 0.969 / 15.2 / 0.13 |
| NegExp $b=1$ | 0.302 / 82.9 / 5.71 | 0.195 / 66.7 / 3.55 | 0.993 / 16.3 / 0.13 |

GM wins on all three criteria in every row. Fig. 9: Sharpe improves with $\alpha$ because optimal leverage on the max-Sharpe fund falls (the less the investor wants to lever, the less the financing friction matters), but GM stays ahead over the relevant range.

**Horizon (Sec. 4, Fig. 11).** Even with frictionless financing, Sharpe rankings are not invariant to the return interval (Levy 1972; Levhari–Levy 1977): 10-year Sharpe ratios from 1,000 bootstrapped 120-month paths per fund scatter widely against monthly Sharpe. Under i.i.d. returns $\log\mathrm{GM}_H=E[\log(R_1\cdots R_H)]=H\,E[\log R]$, so $\mathrm{GM}_H=\mathrm{GM}_1^H$ and the GM ranking is horizon-free.

**Stochastic dominance (endnote 4).** Fund A: 16% or 20%; Fund B: 20% or 40% (equal probabilities, $r_f=0$). Sharpe$_A=18/2=9$ > Sharpe$_B=30/10=3$ although B dominates by FSD; GM gives 17.98% vs 29.61%.

**Alpha.** Not designed for fund selection at all: it is a guide for marginal weight changes relative to a benchmark, and even there fails for non-infinitesimal changes (Levy–Roll 2015); it is also benchmark-dependent (Roll 1978).

## Critical assessment
- **What is convincing.** The decomposition is the real contribution: it shows that Sharpe's failure comes entirely from the financing assumption, not from non-normality (0.998 under textbook financing), and pins down crossovers (1.6% spread, ~120% cap) that are easy to compare with an actual client's terms. The EU-based CE metric makes the stakes concrete.
- **Partly by construction.** $\log\mathrm{GM}$ *is* CRRA-1 expected utility at $x=1$, and with a 2x cap and a 350 bp borrowing penalty, $x^*$ is pushed toward the neighbourhood of 1 for many funds, so EU ranking collapses toward a $\mu-\tfrac{\alpha}{2}\sigma^2$-type ranking that GM approximates. Sharpe in contrast answers "which fund is best *if levered freely*" — a question the setup forbids. The result is correct but less surprising than the headline suggests. Note that GM's own wrong-choice rate is not small (18–34% for $\alpha\ge1$); its CE losses are small because its mistakes are near-ties.
- **Trend in $\alpha$.** GM's correlation declines (0.995 → 0.873) and Sharpe's rises (0.173 → 0.586) as $\alpha$ goes from 0.5 to 2.5; the paper does not report $\alpha>2.5$, where the gap narrows further. Very risk-averse, unlevered investors are exactly the case where a variance penalty with $\alpha/2 > 1/2$ matters, and GM implicitly fixes that penalty at $1/2$.
- **Not tested:** a Sharpe ratio computed against the borrowing rate or a kinked CML, or the obvious "compute CE at a default $\alpha$" alternative; no standard errors on the Spearman differences; a single 10-year sample (including 2008) and in-sample distributions with no estimation error — GM relies on the mean, the hardest moment to estimate, so its out-of-sample advantage could be materially smaller. Random 10-fund menus exaggerate dispersion (the author argues this is conservative for his critique of Sharpe).
- **Practical relevance.** For a PM/researcher: for an unlevered or margin-constrained allocator choosing among funds (or strategies) to hold stand-alone, ranking by $\mu-\sigma^2/2$ (or directly by CE under the actual financing terms) is closer to the right objective than Sharpe or factor alpha. For a levered platform that can finance at near the risk-free rate, Sharpe/IR remains the right scalar — the paper's own Panel A/B shows this. Monthly Sharpe for a long-horizon investor is mis-specified regardless.
