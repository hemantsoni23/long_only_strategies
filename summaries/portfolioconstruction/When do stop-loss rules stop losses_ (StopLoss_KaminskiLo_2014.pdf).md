# When do stop-loss rules stop losses?

**Kathryn M. Kaminski and Andrew W. Lo (2014).** *Journal of Financial Markets* 18, 234–254; available online July 10, 2013. DOI: 10.1016/j.finmar.2013.07.001. Source: [StopLoss_KaminskiLo_2014.pdf](../../Finance/StopLoss_KaminskiLo_2014.pdf). References identify source sections, equations, tables, and figures.

## Why this matters

A stop-loss rule is often judged by the losses it avoided in a memorable decline. The relevant comparison is broader: what returns were given up while out of the market, what asset replaced the original exposure, and what happened after re-entry? This paper treats a stop-loss as an overlay on an existing strategy and decomposes the expected-return change into the frequency of being out and the return difference during those periods.

Its central exact result is simple: an overlay adds arithmetic expected return only when the replacement asset outperforms the original strategy **conditional on being stopped out**. For iid returns with a positive premium over the replacement cash asset, the overlay sacrifices expected return. Predictability or favorable conditional performance of the replacement asset can change that conclusion. The paper then studies AR(1) and regime-switching models and illustrates the framework with equity and Treasury futures.

The framework evaluates a heuristic. It does not derive an optimal policy from investor utility, guarantee a wealth floor, or establish that a positive historical premium survives costs and new market regimes. Several mathematical and empirical details in the source need qualification before replication.

## The policy: cumulative exit, one-period re-entry

Let the underlying strategy have stationary one-period simple returns $r_t$, finite mean $\mu$, and variance $\sigma^2$. The strategy can itself be dynamic. The theoretical replacement asset has constant return $r_f$, with positive unconditional premium $\pi=\mu-r_f>0$.

For a window of $J$ observations, define

$$
R_t(J)=\sum_{j=1}^{J}r_{t-j+1}.
$$

The trigger uses an additive return sum, not compounded wealth and not a trailing high-water-mark drawdown. The source deliberately ignores compounding for the trigger but compounds investment returns when evaluating wealth. Those operations should remain separate.

Let $s_t\in\{0,1\}$ be the fraction allocated to the original strategy during period $t$. With loss magnitude $\gamma\geq0$ and re-entry threshold $\delta$,

$$
s_t=\begin{cases}
0,&s_{t-1}=1\ \text{and}\ R_{t-1}(J)<-\gamma,\\
1,&s_{t-1}=1\ \text{and}\ R_{t-1}(J)\geq-\gamma,\\
1,&s_{t-1}=0\ \text{and}\ r_{t-1}\geq\delta,\\
0,&s_{t-1}=0\ \text{and}\ r_{t-1}<\delta.
\end{cases}
$$

The loss threshold has a minus sign in the original equation; extraction can omit it. The exit condition looks at $J$ prior returns, while re-entry uses only the previous **one-period return of the underlying strategy**, even while the overlay holds the replacement asset. The rule therefore must keep observing the underlying market while out. It is not re-entering on the bond return or on recovery of the entire cumulative loss.

Both decisions are lagged: information through $t-1$ sets exposure earning $r_t$. An implementation needs a starting state and a warm-up policy, neither fully specified for the empirical results. It should evaluate the branches using the previous state once per decision time; applying exit and re-entry sequentially to an already updated state would implement a different rule.

The theoretical combined return is

$$
r^S_t=s_tr_t+(1-s_t)r_f.
$$

A one-way transaction-cost term can be added as $-\kappa|s_t-s_{t-1}|$. The article sets $\kappa=0$ for the remaining analysis. A stop trigger does not guarantee execution at its threshold, and this sampled rule does not continuously monitor intraperiod prices.

## Exact expected-return attribution

Write $p=P(s_t=0)$ and $m_0=E[r_t\mid s_t=0]$. For $p>0$,

$$
\Delta\mu=E[r^S_t]-E[r_t]=p(r_f-m_0),\qquad
\frac{\Delta\mu}{p}=r_f-m_0.
$$

This identity requires no AR model, Gaussian distribution, or optimality claim. The stopping premium $\Delta\mu$ is the unconditional arithmetic return change per observation period. The stopping ratio is the conditional advantage during out-of-market periods. Positive premium requires $m_0<r_f$; a positive unconditional premium of the risky strategy does not preclude this conditional reversal.

The distinction between occupation and transitions is important. $p$ is the **fraction of periods out**, not the frequency of new stop events. It does not by itself determine turnover or mean spell length. In particular, the source's interpretation of $1/p$ as expected stop duration is not generally correct. For a stationary binary Markov policy with exit probability $a$ and re-entry probability $b$, occupation is $a/(a+b)$ while expected out-spell length is $1/b$. Many combinations of $a,b$ yield the same occupation and different durations.

For the same reason, expected net premium is $p(r_f-m_0)-\kappa E|s_t-s_{t-1}|$, not a function of $p$ alone. The text's numerical policy-comparison narrative around 1%, 2%, 25%, and 10% should not be used as a valid derivation of total-return or duration rankings. The stated algebraic stopping ratio is useful without that interpretation.

If the replacement is a risky bond strategy with return $b_t$, the exact extension is

$$
\Delta\mu=pE[b_t-r_t\mid s_t=0].
$$

The empirical application is of this type. It can benefit from favorable conditional bond returns, not merely from avoiding equity losses. A constant risk-free replacement and long-duration Treasury futures are economically different policies.

## Variance and Sharpe: exact decomposition and a printed error

Let $m_1=E[r_t\mid s_t=1]$ and $v_j=\operatorname{Var}(r_t\mid s_t=j)$. For a constant replacement return,

$$
\operatorname{Var}(r_t)=(1-p)v_1+pv_0+p(1-p)(m_1-m_0)^2,
$$

$$
\operatorname{Var}(r^S_t)=(1-p)v_1+p(1-p)(m_1-r_f)^2.
$$

Consequently,

$$
\Delta\sigma^2=-pv_0+p(1-p)\{(m_1-r_f)^2-(m_1-m_0)^2\}.
$$

This follows directly from total variance. The removal of within-out-state risky variance tends to reduce volatility, but the changed between-state means can offset it. Switching to cash does not universally reduce unconditional variance under arbitrary conditional means.

The printed equation 10 instead uses $(r_f-m_0)^2$ as the first squared term in the bracket. In the general decomposition it should involve the in-state mean $m_1$ as above. Its other term, $\{(\mu-m_0)/(1-p)\}^2$, equals $(m_1-m_0)^2$. Thus the printed general formula is not consistent with its own preceding total-variance identity. The special iid result below remains correct because $m_0=m_1=\mu$ there.

The article defines $\Delta\sigma=\sqrt{\operatorname{Var}(r^S)}-\sigma$ and a Sharpe difference $(E[r^S]-r_f)/\sigma_S-(\mu-r_f)/\sigma$. It also acknowledges that these one-period summaries do not fully characterize a dynamic investor's welfare or path-dependent risk. In empirical portfolios with a risky replacement, its conditional variance also contributes, so the constant-cash decomposition cannot simply be reused unchanged.

## Iid returns: a loss of expected premium

Under $r_t=\mu+\epsilon_t$ with iid innovations independent of the past, the lagged policy has no information about today's return. Hence $m_0=m_1=\mu$, and Proposition 1 gives

$$
\Delta\mu=-p\pi,\qquad
\Delta\sigma^2=-p\sigma^2+p(1-p)\pi^2.
$$

For $p>0$, volatility falls when $(1-p)\pi^2<\sigma^2$. A positive risky-asset premium makes expected-return improvement impossible under these assumptions unless the rule never exits. This is an arithmetic-mean statement with a constant replacement asset. It does not prove that every investor with drawdown constraints, nonstandard preferences, or different return dynamics should reject a stop.

A broad interpretation that iid stopping adds “no benefit” overlooks possible changes to risk, utility, or constraints. The paper's explicit success criterion is a positive stopping premium, which is narrower than all possible economic objectives.

## AR(1): the exact identity and the qualified approximation

The alternative process is

$$
r_t=\mu+\rho(r_{t-1}-\mu)+\epsilon_t,\qquad |\rho|<1,
$$

with iid zero-mean innovations and stationary variance $\sigma^2=\sigma_\epsilon^2/(1-\rho^2)$. Since the policy is determined by the past, the innovation has zero conditional expectation. Therefore the exact stopping ratio is

$$
\frac{\Delta\mu}{p}=-\pi-\rho\{E[r_{t-1}\mid s_t=0]-\mu\}.
$$

Positive serial dependence can help when the rule identifies states with sufficiently low last returns; negative dependence can make exiting before a rebound costly. But the full stopped-state distribution depends on both exit and re-entry history, not just the unconditional lag-one correlation.

The paper writes this as $-\pi+\rho\sigma+\eta(\gamma,\delta,J)$ and argues that $\eta\geq0$ for positive $\rho$ and “reasonable” parameters, obtaining the proposed sufficient condition $\rho\geq\pi/\sigma$. The right-hand Sharpe ratio must be measured at the **same frequency** as $\rho$. Comparing a daily autocorrelation with an annual Sharpe is dimensionally inappropriate. Ordinary square-root-of-time Sharpe annualization is itself not exact under serial dependence, as the paper notes.

This bound should not be treated as a general proved guarantee for every stated AR(1). Appendix A.2 takes a special limit with sufficiently large $J$ and $\delta=-\infty$, invokes approximately negligible dependence at lag $J$, and uses a truncated-expectation inequality bounded by $\mu-\sigma$ without establishing distributional conditions sufficient for it. The phrase “reasonable parameters” is not operationally defined, and the appendix's equivalence between being out and a fresh threshold crossing does not fully represent arbitrary spell histories. The main text itself calls the result a first-order approximation. A reproduction should retain the exact conditional-mean identity and estimate/simulate its conditional expectation for the chosen rule, rather than assert the stated lower bound universally.

## Two-state regime switching

Let $I_t=1$ indicate a high-mean state and $I_t=0$ a low-mean state. Conditional returns have state means $\mu_1>\mu_2$ and variances $\sigma_1^2,\sigma_2^2$, with Gaussian iid innovations within the stipulated state process. A time-homogeneous Markov matrix has rows $(p_{11},1-p_{11})$ and $(1-p_{22},p_{22})$.

For $p_j=P(s_t=0,I_t=j)$, with low state indexed consistently, the article's exact attribution is the weighted sum of state return differences. Equivalently, letting $q=P(I_t=0\mid s_t=0)$,

$$
\frac{\Delta\mu}{p}=(1-q)(r_f-\mu_1)+q(r_f-\mu_2).
$$

This uses the model's conditional independence of the return innovation from the policy once the current state is fixed. If $\mu_1>r_f>\mu_2$, nonnegative premium requires

$$
q\geq\frac{\mu_1-r_f}{\mu_1-\mu_2}.
$$

If even the low-state expected return exceeds cash, no stopped-state classification accuracy can produce positive expected premium. If $r_f=\mu_2$, only perfect concentration in the low state can attain zero premium; strictly positive improvement remains impossible. With regime-dependent replacement means $r_{f1},r_{f2}$, substitute those means in the corresponding terms.

The quantity $q$ is the fraction of stopped periods falling in the low state, not overall classification accuracy or the fraction of all low-state periods captured. The formula does not itself solve for $q$ as a function of thresholds and transition probabilities. Numerical simulation or a joint state-policy calculation is still needed. The overlay does not observe the hidden state directly.

## Empirical data and strategy grid

Section 5 uses daily futures prices from **January 5, 1993–November 7, 2011**. Equity exposure is an IMM S&P futures basket; replacement exposure is CBT ten-year Treasury-note futures. Prices are described as a weighted basket of near maturities rolled to avoid maturity jumps. Exact contracts, weighting schedule, roll dates, splice method, collateral yield, financing, margin treatment, and return denominator are not provided. Those omissions prevent unique reconstruction of the daily tradable return series.

The reported stock/bond return correlation is −17.29%. Table 1 annualizes with 250 days per year:

| Statistic | S&P futures | Ten-year Treasury futures |
|---|---:|---:|
| Mean | 7.295% | 1.181% |
| Standard deviation | 19.499% | 6.331% |
| Lag-one autocorrelation | −0.06 | +0.02 |
| Skewness | +0.12 | −0.09 |
| Kurtosis | 14.24 | 6.11 |
| Minimum daily return | −9.88% | −2.43% |
| Maximum daily return | +14.12% | +3.61% |
| Reported annualized Sharpe | 0.37 | 0.19 |
| Reported maximum drawdown | 26.62% | 5.25% |

The negative signs in the original table matter. In particular, the text says the equity contract has net **positive** autocorrelation, but Table 1 prints **−0.06**. Rolling 75- and 150-day autocorrelations in Figures 1–2 vary in sign, which supports time variation but does not resolve that full-sample sign contradiction. No confidence intervals are shown for the rolling curves. The reported Sharpe values numerically resemble mean divided by standard deviation; the precise cash/collateral convention is absent.

Table 2 reports an EM-estimated two-state Hamilton model with annualized means +22.3% and −39.0%, volatilities 10.3% and 33.0%, and a single probability value 0.72. State labels differ from the theoretical high/low numbering. A full two-state Markov model requires two transition probabilities or an equivalent complete parameterization; the meaning of the lone $p$ is not explained sufficiently to reproduce the fitted dynamics. The table therefore supports a qualitative high-return/calm versus low-return/volatile contrast, not an exact reproducible transition model.

The experiment varies decision/re-entry observation frequency and exit window. In daily units, the text lists:

| Decision period | Exit-window / one-period re-entry pairs |
|---|---|
| Daily, 1 day | (3,1), (5,1), (10,1) |
| Weekly, 5 days | (15,5), (25,5), (50,5) |
| Monthly, 20 days | (60,20), (100,20), (200,20) |
| Quarterly, 60 days | (180,60), (300,60), (600,60) |

Figures 3–5 additionally show (360,120), (600,120), and (1200,120), extending to a 120-day decision period not fully developed in the text's grid description. Here “monthly” means 20 trading days, not calendar month-end rebalancing.

The plots use exit levels −1.5, −1.2, −1.0, −0.8, and −0.5 standard deviations relative to the relevant mean, and a re-entry level of **zero** standard deviations. The text also describes varying re-entry levels from 0.5 to 1 standard deviation, but does not display the full corresponding output. It does not clearly specify whether means and standard deviations are full-sample, rolling, or expanding, nor the exact scaling for multi-period thresholds. The theoretical $-\gamma$ convention and standardized empirical threshold convention should be mapped explicitly in code rather than equated by label alone.

## Findings and limits of the backtest

The figures show strongly negative stopping premiums for very short horizons, with monthly/quarterly configurations often better. In Figure 3, the earliest daily rules have premiums around −6% to −7% in plotted return units, while some medium/long configurations peak around +2% to +2.5%. These are approximate readings, not a numerical result table. Very long configurations are not uniformly better: some premiums return below zero at the 1200/120 endpoint.

Figure 4 shows Sharpe improvements for many medium/long configurations, but losses for short ones and mixed very-long results. Figure 5 shows volatility reductions across the displayed grid, often around 3–6 percentage points if interpreted on the annualized decimal-return scale. The introduction highlights one calibration with about a 1.5-percentage-point return gain, a 5-point volatility reduction, and a Sharpe improvement described as up to 20%. It does not identify that calibration sufficiently to reconstruct it from a complete result table; the plot's $\Delta SR$ is an arithmetic difference, so it should not automatically be read as a percentage relative change.

The outcome is conditional on the chosen historical equity/bond relationship and the replacement asset. Some gains can reflect Treasury strength after equity losses. They are not evidence that an equivalent cash stop would earn the same premium. Nor does lower volatility establish a hard drawdown bound: signals are delayed and losses can occur before exit or after re-entry.

No confidence intervals on stopping premiums, bootstrap accounting for overlapping windows, formal multiple-testing correction, held-out parameter selection, or out-of-sample period is reported. Examining a broad threshold grid is informative sensitivity analysis, but does not eliminate data-selection bias. Frequencies, long windows, thresholds, and the 1993–2011 equity/bond sample all affect the result. Costs are explicitly zero, and the frequency of switching is not tabulated; a net premium cannot be inferred from time spent in bonds.

The behavioral mechanisms discussed—loss aversion, the disposition effect, ambiguity aversion, and flight to safety—are possible interpretations rather than separately identified causal findings. The authors themselves acknowledge that nonlinear stock/bond dynamics could explain the evidence without resolving the efficiency-versus-behavioral debate.

## What can be implemented faithfully

The binary policy, lag structure, additive trigger, and expected-return attribution are precise enough to implement once numerical thresholds, execution conventions, and returns are supplied. An implementation can verify the premium by comparing both the full return difference and the stopped-state conditional difference. It can separately record occupation, exit/re-entry counts, spell durations, and switching costs; these quantities should not be substituted for one another.

The iid formulas and regime-conditioned attribution are exact under their assumptions. The general variance expression needs the correction shown above, and the AR lower-bound discussion should remain qualified. Reproducing the empirical figures requires the undisclosed continuous-futures construction, threshold estimation windows, decision-date alignment, starting/warm-up policy, and complete result data.

The paper's strongest durable conclusion is an attribution criterion: the question is whether the rule selects periods when the underlying strategy performs worse than the chosen alternative. It offers a clear way to measure that claim, while its published backtest provides suggestive gross evidence rather than an independently validated optimal stop-loss policy.
