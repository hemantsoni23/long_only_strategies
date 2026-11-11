# Crash Sensitivity and the Cross Section of Expected Stock Returns
**Authors:** Fousseni Chabi-Yo, Stefan Ruenzi, Florian Weigert
**Year:** 2018
**Journal/Venue:** Journal of Financial and Quantitative Analysis, Vol. 53, No. 3, pp. 1059-1100
**Source file:** Finance/AbnormalReturnsMomentum_ChabiyoRuenziWeigert_2018.pdf

## Question

Is crash sensitivity, defined as asymptotic lower-tail dependence (LTD) between a stock and the market, priced in the cross section, and is it distinct from beta, downside beta (Ang-Chen-Xing 2006), coskewness, cokurtosis and the Kelly-Jiang (2014) tail beta? Answer: yes; strong-LTD stocks earn about 0.36%/month more than weak-LTD stocks (value weighted), and weak-LTD stocks act as insurance on crash days.

## Measure

For stock return $X_1$ and market return $X_2$ (market excludes stock $i$ to avoid mechanical dependence):

$$
\text{LTD}=\lim_{q\to0^+}\Pr\!\left(X_1<F_{X_1}^{-1}(q)\mid X_2<F_{X_2}^{-1}(q)\right),\qquad
\text{UTD}=\lim_{q\to1^-}\Pr\!\left(X_1>F_{X_1}^{-1}(q)\mid X_2>F_{X_2}^{-1}(q)\right).
$$

Estimation, each stock-month, on the previous 12 months of daily returns (at least 100 observations):

1. Margins: rescaled empirical CDFs $\hat F(x)=\frac{1}{n+1}\sum_k \mathbf 1\{r_k\le x\}$.
2. Copula: all $4\times4\times4=64$ convex mixtures
$$C(u_1,u_2;\Theta)=w_1C^{LTD}(\theta_1)+w_2C^{NTD}(\theta_2)+(1-w_1-w_2)C^{UTD}(\theta_3),$$
with $C^{LTD}\in$ {Clayton, rotated Gumbel, rotated Joe, rotated Galambos}, $C^{NTD}\in$ {Gauss, Frank, FGM, Plackett}, $C^{UTD}\in$ {Gumbel, Joe, Galambos, rotated Clayton}; five parameters each, fitted by canonical maximum likelihood.
3. Model selection: minimize the integrated Anderson-Darling distance to the Deheuvels empirical copula. No mixture dominates; the most frequent (Clayton-Gauss-Galambos) is chosen only about 6% of the time.
4. Tail coefficients from closed forms: $\text{LTD}^*=w_1^*\,\lambda_L(\theta_1^*)$, $\text{UTD}^*=(1-w_1^*-w_2^*)\,\lambda_U(\theta_3^*)$.

The argument for the copula route: nonparametric tail estimators use only a handful of tail points and are imprecise; conditional-quantile downside betas at the 5% cutoff use about 12 daily observations per year. The authors attribute Van Oordt and Zhou's (2016) null tail-beta result to this noise.

## Data and descriptive facts

- CRSP common stocks (share codes 10/11), NYSE/AMEX/NASDAQ, 1963-2012. Bottom 1% of market cap dropped. 2.61m firm-months, 1,904-6,778 firms per month.
- Mean (median) LTD is 0.100 (0.069), with an interquartile range of about 0.15. Mean UTD is 0.065, below LTD in most years (33 of 49), consistent with correlations rising in down markets.
- Correlations with LTD: downside beta 0.38, beta 0.34, UTD 0.15, Kelly-Jiang tail beta 0.07. LTD is positively correlated with cokurtosis and negatively with coskewness. High-LTD stocks are larger, more liquid, higher beta, lower B/M.
- Aggregate LTD has no trend (the ADF test rejects a unit root). It spikes in 1987 and 2007-2011, with correlation 0.32 with market volatility.
- Persistence is moderate: a Fama-MacBeth AR coefficient of 0.208 (t = 11.46) year on year; the extreme quintiles are retained with probability 31.6% (Q5) and 26.6% (Q1), against 20% if random. Cross-sectional drivers are beta, size, tail beta and distress (+), and coskewness and idiosyncratic volatility (-).
- The hedge is realized: weak-LTD stocks outperform strong-LTD stocks on the crash days of 19 Oct 1987, 27 Oct 1997, 14 Apr 2000 and 15 Oct 2008 (Internet Appendix).

## Main results

**Univariate VW quintile sorts (Table 3).** Mean LTD runs from 0.00 (Q1) to 0.27 (Q5).

| | Excess return | CAPM α | Carhart α | FF5 α |
|---|---|---|---|---|
| Q1 weak | 0.296% | -0.129% | -0.108% | -0.323% |
| Q5 strong | 0.656% | +0.172% | +0.129% | +0.211% |
| Q5-Q1 | 0.360% (t=3.68) | 0.302% (3.15) | 0.237% (2.35) | 0.534% (5.58) |

- Alphas are monotone in LTD. UTD sorts give -0.134%/month (t = -1.26), which is insignificant; the paper then focuses on LTD.
- Conditioning: the spread is 0.794%/month in up-market months and -0.244% (insignificant) in down-market months. That is the expected pattern for a crash-risk premium. It is similar in high and low volatility regimes and in CFNAI regimes (somewhat larger when CFNAI < 0).
- Screens: the spread survives excluding stocks below the NYSE 10% size or liquidity breakpoints and stocks priced under $5 (about 0.34-0.35%).
- Horizon: the cumulative 2- and 3-month spreads are significant; the 6-month spread is not, except for the FF5 alpha. This matches LTD's limited persistence.

**Factor spanning of the 5-1 portfolio (Table 4).** Alphas of 0.22-0.46%/month survive adding Pastor-Stambaugh or Sadka liquidity, FMAX, orthogonalized sentiment, BAB, the Kelly-Jiang tail factor, short and long reversal, or the Hou-Xue-Zhang q-factors. The loadings matter for implementation:
- positive on market (about 0.1) and on UMD (about 0.21-0.24, t ≈ 10);
- negative on SMB, HML, BAB and INVEST;
- positive on TAIL_RISK (0.356).

**Dependent double sorts (Table 5, VW).** Average Q5-Q1 LTD spread within quintiles of:

| Control | Spread (t) |
|---|---|
| Beta | 0.404% (3.62) |
| Downside beta | 0.415% (3.31) |
| Coskewness | 0.253% (1.89) |
| Cokurtosis | 0.492% (4.02) |
| Tail beta | 0.351% (2.75) |

Coskewness is the control that absorbs the most. Only 10% significance remains there, and in the most negative coskewness quintile the spread is insignificant.

**Alternative downside betas (Table 8).** The spread holds within quintiles of every alternative downside beta, at 0.40-0.55%/month with all t > 2.8:
- betas conditional on the market below its 10/5/2/1% quantiles;
- the Hogan-Warren, Estrada and Harlow-Rao asymmetric-response betas.

The correlation of LTD with quantile-conditional downside betas falls from 0.42 (Ang et al. definition) to 0.24, 0.13, 0.04 and 0.00 as the cutoff tightens. The authors read this as noise in tail betas, not as evidence that LTD and extreme downside beta are different objects.

**Fama-MacBeth (Table 6).**
- Univariate LTD coefficient: 0.0123. LTD stays significant with t-statistics of 4.85 and 4.21 in the rich specifications (beta, UTD, size, B/M, coskewness, illiquidity, past return, idiosyncratic volatility, cokurtosis, MAX, tail beta) and above 3 in all columns, including when beta is split into $\beta^-,\beta^+$ and for 2- and 3-month-ahead returns.
- UTD is negative and significant in the regressions but much smaller.
- A one-SD increase in LTD adds about 2.60% per year. That is fourth largest, after past return and B/M (6.12% each) and ILLIQ (4.78%). It is larger than coskewness (-2.11%), cokurtosis (+2.42%) and tail beta (+1.62%). Tail beta loses significance once LTD is included, except at the 3-month horizon.

**Time-varying crash fear (Table 7).** In the 5 years after one of the 10 worst market days (1987, 1997, 1998, 2000, 2008, 2011), the LTD coefficient is 0.0241 (t = 3.65), against 0.0132 (t = 4.52) in other years. This fits Chen-Joslin-Tran (2012) disaster-premium dynamics and Gennaioli-Shleifer-Vishny (2015) crash-memory arguments.

**Robustness (Table 9 and Internet Appendix).**

| Variant | LTD coefficient (t) |
|---|---|
| Fixed mixture, among the most-selected | 0.0112-0.0129 (t ≈ 2.9-3.7) |
| Fixed mixture, least-selected rotated-Gumbel types | 0.0091-0.0111 (t = 1.75-2.45) |
| Two-copula mixture | 0.0089 (1.80) |
| Log-likelihood selection | 0.0131 (4.02) |
| 24-month window | 0.0110 (3.21) |
| 36-month window | 0.0106 (2.31) |

- FF49 industries as test assets: 5-1 spread 0.333%/month (t = 2.41), FF5 alpha 0.352%.
- The effect has the right sign in every 10-year subperiod and in 1927-1963. It is significant in 3 of 6 subperiods for sorts and 5 of 6 for regressions.
- Also robust to industry and DGTW adjustments, no winsorization, and pooled OLS with clustered standard errors.
- Filtering returns with ARCH, GARCH or EGARCH before estimating LTD changes little.
- Equal-weighted results are stronger, about 4.8% per year against 4.3% VW.

## Theory (Appendix A)

The model has a representative agent with $u'>0,u''<0,u'''>0,u''''<0$. The SDF is spanned via Carr-Madan into the market return plus option payoffs, and expected excess returns decompose into beta plus integrals of tail co-moment risks such as $\delta^{dd}_i[k]=\mathrm{cov}((k-R_i)^+,(k-R_M)^+)/\mathrm{var}((k-R_M)^+)$, with prices $\lambda^{dd}>0$, $\lambda^{uu}<0$. The limiting co-moments $\delta^{dd}_i[0]$ and $\delta^{uu}_i[k_{max}]$ are increasing linear functions of LTD and UTD, so $\partial E[R_i]/\partial\text{LTD}>0$ and $\partial E[R_i]/\partial\text{UTD}<0$. Prudence ($u'''>0$) makes the lower-tail weight large, which is why UTD should matter less. Under quadratic utility everything collapses to the CAPM. This is a sufficiency argument and yields no quantitative premium.

## Assessment

- **Convincing:**
  - The measure is ex ante (rolling 12 months, predicting month t+1).
  - The spread survives a long list of co-moment and factor controls.
  - The sign pattern fits a risk premium: the spread is earned in up markets, negative in down months, and weak-LTD stocks pay off on crash days.
  - The premium is larger after crashes.
  - The downside-beta comparison is careful.
- **Fragile or open:**
  - The raw spread is modest: 0.36%/month with a Carhart alpha t of 2.35, and coskewness sorts cut it to t ≈ 1.9.
  - The FF5 alpha is larger than the raw spread because the portfolio is short HML/SMB/INVEST exposure. The alpha therefore depends on the benchmark.
  - LTD is identified from 250 daily points through the parametric mixture: the tail coefficient is an extrapolation implied by $w_1$ and $\theta_1$, and model choice among 64 mixtures adds estimation noise. The paper reports no standard errors for individual LTD estimates.
  - The short leg is small, low-beta stocks. Rebalancing is monthly and no transaction costs are modeled (the authors flag this).
  - There is a sizable positive momentum loading.
  - The sample ends in 2012, and some subperiods are insignificant in sorts.
- **For a quant PM:**
  - LTD is a cheap-to-state but expensive-to-compute characteristic (64 five-parameter MLEs per stock-month). A single fixed mixture such as Clayton-Gauss-Galambos retains most of the signal.
  - It is best seen as a crash-insurance axis that is weakly related to Kelly-Jiang tail beta, useful as a risk descriptor or for conditioning, for example to scale exposure after crashes. It is not a standalone alpha: the premium is small and turns negative precisely in drawdowns.
  - Related: the same authors' LTD-momentum work, [[Momentum and Crash Sensitivity (2018)]].
