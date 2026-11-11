# Stock Return Predictability and Model Uncertainty

**Doron Avramov.** Working-paper revision dated April 17, 2001; first draft April 14, 1999. Source: [AssetPrediction_Avramov_2001.pdf](../../Finance/AssetPrediction_Avramov_2001.pdf). This note follows the supplied 43-page version, including its mathematical appendix, data description, references, and eight tables. Printed pages 1–41 correspond to PDF pages 3–43. Numerical results are those reported in this version; corrections derived below are explicitly distinguished from them.

## Why this matters

Predictive regressions leave an allocator with two different uncertainties: coefficients are estimated imprecisely, and the researcher does not know which predictors belong in the regression. Selecting one specification and integrating over its coefficient posterior handles only the first. Avramov assigns probabilities to every subset of fourteen candidate variables, averages their predictive distributions, and carries the resulting mixture into a portfolio decision. The paper is useful because it connects predictor selection, forecasting diagnostics, forecast-risk decomposition, and investment utility within one framework.

The empirical conclusions are more qualified than the abstract's positive description. Model averaging produces modest monthly mean-squared-error improvements over a historical-mean forecast, while several conventional model-selection rules perform worse. The relevant allocation exercise is a model-based buy-and-hold decision evaluated at December 1998 conditions; it is not a realized, cost-adjusted trading backtest. Several printed formulas and one universal forecasting claim also conflict with the appendix or tables. Reimplementing the statistical architecture is feasible, but reproducing the numerical results exactly requires resolving those discrepancies and recovering conventions not specified in the source.

The novel contribution is the combination of a skeptical empirical-Bayes prior, an explicit prior mass on no predictability, model-averaged coefficient uncertainty, and a multivariate predictive distribution for long-horizon allocation. The paper also shows that the evidence for a particular predictor can weaken substantially after accounting for disagreement across specifications. Strong posterior odds that *some* predictor matters do not imply strong evidence for each variable in the full regression.

## Forecasting universe and data

The main sample contains 549 months, April 1953–December 1998. Risky investments are the six Fama–French portfolios formed by intersecting two size groups, small and big, with three book-to-market groups, low, medium, and high: SL, SM, SH, BL, BM, and BH. The forecasting response is the continuously compounded portfolio return minus the continuously compounded Treasury-bill return. Quarterly observations provide a second experiment; the source does not fully specify every aggregation and alignment convention needed to rebuild them from monthly files.

Each candidate regression uses an intercept and a subset of fourteen variables observed with one lag:

| Variable | Construction in the source |
|---|---|
| Div | Dividend yield on the value-weighted NYSE index |
| BM | Book-to-market for Standard & Poor's Industrials |
| EY | Latest twelve-month earnings divided by the contemporaneous S&P Composite index |
| WML | Winners-minus-losers one-year momentum portfolio return |
| Def | Moody's Baa-minus-Aaa annualized corporate yield spread |
| Tbill | Monthly rate corresponding to a three-month Treasury bill |
| RET | CRSP value-weighted index excess return, including dividends |
| DEF | Long-term corporate-bond return minus long-term government-bond return |
| TERM | Long-term government-bond monthly return minus the one-month bill rate |
| Jan | January indicator |
| Inf | Monthly inflation |
| SMB | Size-factor return |
| HML | Value-factor return |
| Term | Ten-year-minus-one-year Treasury yield spread |

Capitalization is economically important: TERM is a realized bond-return premium, whereas Term is a yield spread; DEF and Def likewise differ. The main text calls the latter term-spread instruments Treasuries, while some table descriptions call both “bills.” The natural intended object is the specified ten-year/one-year yield difference, not a ten-year bill. Units also differ across predictors: return series are generally decimals, while some yield spreads and inflation are reported on percentage scales. The descriptive table gives RET mean .0063 and standard deviation .0423, Def mean .9476, and inflation mean .3330. One common rescaling across all columns would therefore be incorrect.

Sources are CRSP for dividend yield, bills, and the market premium; Standard & Poor's *Security Price Index Record* for book-to-market; Citibase for the default yield spread; Ibbotson for bond-return premiums; Kenneth French for the six portfolios, SMB, and HML; Mark Carhart for WML; Robert Shiller for earnings and inflation; and the Federal Reserve for Treasury yields. The source provides neither frozen input files nor a complete vintage calendar. Publication lags must be distinguished from the mechanical one-period lag when attempting a historical real-time reconstruction.

Valuation ratios are highly persistent: first-order autocorrelations are .9828 for Div, .9889 for BM, and .9929 for EY. RET and TERM have autocorrelations .0655 and .0662. This contrast matters for finite-sample predictive-regression behavior and long-horizon dynamics. The January indicator is deterministic, although the predictor list describes one lag generically. Its exact calendar alignment and treatment in the subsequent stochastic state model need to be specified rather than inferred silently.

## Model space and skeptical prior

Let $r_t$ be the $N\times1$ vector of excess log returns. Model $j$ retains $m_j$ predictors $z_{j,t-1}$, and $x_{j,t-1}=(1,z_{j,t-1}')'$. With $k_j=m_j+1$ coefficients per equation,

$$
r_t'=x_{j,t-1}'B_j+\epsilon_{j,t}',\qquad
\epsilon_{j,t}\sim N(0,\Sigma_j).
$$

The empty subset is an intercept-only, iid-return model. Fourteen possible predictors imply $2^{14}=16,384$ specifications. Models differ in predictor membership; they do not include arbitrary nonlinearities, structural breaks, heteroskedastic innovations, or predictors outside this chosen set. Averaging protects against selecting the wrong member of that finite set, not against all forms of model misspecification.

Write $X_j$ for the $T\times k_j$ design and $R$ for the $T\times N$ return matrix. The hypothetical prior sample matches the actual sample's means and covariance matrices but has zero predictive slopes. Its coefficient center is $B_{j,0}=(\bar r,0)'$, its return residual sum of squares is $S_{j,0}=T_{j,0}\widehat V_r$, and its design precision is

$$
K_{j,0}=X_{j,0}'X_{j,0}=
\frac{T_{j,0}}{T}X_j'X_j.
$$

Equations (6)–(7) can therefore be written as a matrix-normal/inverse-Wishart prior:

$$
\operatorname{vec}(B_j)\mid\Sigma_j
\sim N\!\left(\operatorname{vec}(B_{j,0}),\Sigma_j\otimes K_{j,0}^{-1}\right),
\qquad
\Sigma_j\sim IW(S_{j,0},\nu_{j,0}),
\quad\nu_{j,0}=T_{j,0}-k_j.
$$

Here vec uses column stacking, consistently with the displayed Kronecker covariance. The original prose's description of its stacking convention is awkward; choosing and documenting one consistent convention prevents dimension errors. The inverse-Wishart density is proportional to $|\Sigma|^{-(\nu+N+1)/2}\exp[-\operatorname{tr}(S\Sigma^{-1})/2]$.

The construction is empirical Bayes: some “prior” inputs are estimated from the same sample subsequently used in the likelihood. The default strength is described as fifty hypothetical observations per parameter, with twenty-five and one hundred considered as alternatives. Prior sample size grows with model dimension. The source does not provide code or an unambiguous all-cases parameter-count convention for the multivariate exercises; an implementation must state how its per-parameter rule maps into $T_{j,0}$ and ensure proper inverse-Wishart degrees of freedom. It should recompute empirical-Bayes inputs inside each training window for an out-of-sample exercise.

Prior odds of any predictability versus no predictability equal one. Thus the iid model receives probability one-half, while each of the other 16,383 models receives $1/[2(16,383)]$. This is substantially different from assigning equal probabilities to all 16,384 specifications, which would put almost no prior mass on the iid benchmark. Posterior probabilities are

$$
p_j=P(M_j\mid D)=
\frac{p(D\mid M_j)P(M_j)}{\sum_\ell p(D\mid M_\ell)P(M_\ell)}.
$$

Compute these using log marginal likelihoods and a log-sum-exp normalization. Equal posterior weights, minimum-AIC selection, and equal prior model probabilities are three distinct procedures.

## Conjugate updating and a consequential normalization discrepancy

The appendix gives sufficient statistics for conjugate updating. A convenient dimensionally consistent implementation is

$$
K_{j,n}=K_{j,0}+X_j'X_j,
\qquad
B_{j,n}=K_{j,n}^{-1}(K_{j,0}B_{j,0}+X_j'R),
$$

$$
S_{j,n}=S_{j,0}+R'R+B_{j,0}'K_{j,0}B_{j,0}
-B_{j,n}'K_{j,n}B_{j,n},
\qquad \nu_{j,n}=\nu_{j,0}+T.
$$

Then $B_j\mid\Sigma_j,D$ is matrix normal with center $B_{j,n}$ and row covariance $K_{j,n}^{-1}$, while $\Sigma_j\mid D\sim IW(S_{j,n},\nu_{j,n})$. Use Cholesky solves and log determinants rather than explicit inverses in actual numerical code.

For these normalized prior and likelihood distributions, direct integration yields the following marginal likelihood:

$$
p(D\mid M_j)=\pi^{-TN/2}
\left(\frac{|K_{j,0}|}{|K_{j,n}|}\right)^{N/2}
\frac{|S_{j,0}|^{\nu_{j,0}/2}}{|S_{j,n}|^{\nu_{j,n}/2}}
\frac{\Gamma_N(\nu_{j,n}/2)}{\Gamma_N(\nu_{j,0}/2)}.
$$

This equation is a derived normalized reconstruction, not a transcription of the source's equation (10). Because $K_{j,n}/K_{j,0}$ is a scalar multiple of the identity in design coordinates, its log complexity term is

$$
-\frac{Nk_j}{2}\log\frac{T+T_{j,0}}{T_{j,0}}.
$$

The visually checked equation (10), printed p. 5, instead has $-Nk_j^2/2$ multiplying that logarithm. Appendix equations (A.5) and (A.8) likewise raise the determinant of the *full vector covariance* to $-k_j/2$, whereas a multivariate normal density requires exponent $-1/2$. These printed expressions do not normalize as the stated Gaussian densities when $k_j>1$. The extra factor changes relative model weights; it is not a common constant that cancels in Bayes factors. The supplied document does not reveal whether its computations used these printed formulas or correctly normalized code. Consequently, reproducing the tables and implementing the mathematically specified Bayesian model are separate validation targets.

Posterior inclusion probability for predictor $q$ is $\sum_jp_j1\{q\in M_j\}$. To average coefficients, embed each model in the common fourteen-predictor space and set excluded slopes to zero. If $\bar B=\sum_jp_jB_{j,n}$, total coefficient covariance is the posterior-weighted sum of within-model covariance plus covariance of the model-specific centers about $\bar B$. This second term is the source of the reduction in posterior t-ratios.

There is a second printed issue: equation (15) uses a scalar-regression within-model variance denominator $T_j^*-4$, irrespective of predictor count. With the stated inverse-Wishart convention and $N=1$, the coefficient covariance is

$$
\operatorname{Var}(B_j\mid D)
=\frac{S_{j,n}}{T_j^*-m_j-3}K_{j,n}^{-1},
\qquad T_j^*=T+T_{j,0},
$$

provided the moment exists. The printed denominator agrees when $m_j=1$ but not generally. The note retains the published numerical t-ratios as reported outcomes and does not claim they have been recomputed under this correction. Finally, a posterior mean divided by its posterior standard deviation is a descriptive Bayesian ratio; it is not automatically a classical Student t test after model averaging.

## What the posterior evidence actually says

The six reported posterior odds for predictability versus iid returns are 550, 10,886, 1,040,000, 74, 121, and 1,249 for SL, SM, SH, BL, BM, and BH respectively (printed p. 12). Predictability appears strongest for small value and weakest for big growth. These are conditional on the chosen predictors, empirical-Bayes prior, model probabilities, and implementation; they are not posterior odds for an unrestricted economic proposition about markets.

Table 2 shows relatively sparse highest-probability specifications, containing at most two predictors. RET inclusion probabilities for the three small portfolios are .48, .40, and .49, compared with .05, .03, and .02 for the big portfolios. Jan inclusion probability is 1.00 for SH and .92 for BH. TERM receives .54 for SM and BM, while inflation receives .69 for BL. Dividend yield and book-to-market are less prominent than their ubiquity in the forecasting literature might suggest. HML inclusion probabilities are only .02–.05 across the six portfolios.

Table 3 illustrates the distinction between predictor uncertainty and coefficient uncertainty. For SH, the RET ratio falls from 2.22 when model uncertainty is ignored to .89 when it is included. For SM, TERM falls from 2.37 to .97. The SH January effect remains strong, declining from 4.69 to 4.48, consistent with its near-certain inclusion. A large posterior odds ratio for the predictive model class can coexist with many individual ratios below two because different models explain the evidence with different variables.

The quarterly exercise replaces Jan with Lettau–Ludvigson's trend deviation in wealth, TDW, constructed from log consumption, asset wealth, and labor income. The paper emphasizes two implementation issues: release occurs after quarter-end, so a quarter-$t$ observation is usable for returns at or after $t+2$; and full-sample cointegrating coefficients embed future information. The cited wealth and labor-income coefficients, .3054 and .5891, sum to .8945 rather than one, despite the motivating expression $c_t-wa_t-(1-w)y_t$.

With full-sample TDW and seventeen prior observations per parameter, its average inclusion probability is about .31, compared with .34 for TERM. In the alternative 122-observation recursive-TDW exercise, TDW probabilities fall to .10–.18, and none of the highest-probability models retains it. TERM probabilities are .25–.38 and it enters four highest-probability models. The remaining quarterly results use full-sample TDW, a limitation that must accompany any investment interpretation; the recursive-TDW experiment is not the input to every subsequent table.

## Out-of-sample forecasting experiment

Because the model space is large, the forecast comparison uses one response, the CRSP value-weighted market excess return. The initial estimation sample is the first third of the available observations. Rolling estimation keeps that window length constant; recursive estimation grows the sample from its original start; fixed estimation fits once and subsequently updates the conditioning values without refitting parameters. Exact endpoint treatment and resulting forecast counts are not tabulated. The full monthly sample has 549 observations, so one third is 183 before any additional loss from alignment; the source should be consulted alongside the actual input file before treating this as a definitive usable-row count.

Competitors are the all-predictor regression, iid model, and single models chosen by adjusted $R^2$, AIC, SIC, FIC, and PIC. The last two criteria and exact selection conventions are referred to Bossaerts–Hillion rather than fully defined here. There is no separate hyperparameter-validation period: prior strengths 25, 50, and 100 are reported as sensitivity scenarios. Forecast diagnostics are mean error, a regression of errors on forecasts, first-order error autocorrelation, and MSE; inference follows West–McCracken's scheme-dependent regression tests. Failure to reject a zero error moment is evidence of compatibility, not proof the population moment is zero.

| Monthly scheme | iid MSE | BMA MSE: prior 50 | BMA MSE: prior 100 | BMA MSE: prior 25 |
|---|---:|---:|---:|---:|
| Rolling | .2155 | .2137 | .2141 | .2139 |
| Recursive | .2155 | .2133 | .2133 | .2143 |
| Fixed | .2162 | .2118 | .2133 | .2113 |

These are Table 6's MSE units, described as “in percent.” Since the underlying returns are decimals, the magnitude is consistent with a scaling of squared decimal returns by 100, not with squared percentage-point returns. Scale-invariant relative improvement is safer: at prior strength 50, $1-MSE_{BMA}/MSE_{iid}$ is approximately .84%, 1.02%, and 2.04% for rolling, recursive, and fixed estimation, respectively. These are derived forecast-loss reductions, not portfolio returns.

Conventional model selection performs worse than iid. Rolling MSEs range from .2298 to .2339 among the five selected models; recursive MSEs range from .2189 to .2260. The fixed all-predictor model has MSE .5111 versus .2162 for iid. Its fixed-sample mean error is −.0458 with t-statistic −9.1930, and its error-autocorrelation slope is .5828 with t-statistic 8.7574. BMA sharply reduces this instability.

Nevertheless, fixed BMA fails the forecast-efficiency diagnostic: its error-on-forecast slope is about −.495, with t-statistics from −3.9771 to −4.0433. A forecast can improve MSE while remaining systematically overresponsive. Nor is the prose claim that BMA beats iid for every quarterly prior and scheme literally true in the table. Quarterly recursive MSE for the weakest prior is .7930, exceeding iid's .7781; the corresponding strengths 17 and approximately 33/34 give .7757 and .7678. The text and tables alternate between 33 and 34 for this prior strength. Both discrepancies should remain visible in a replication specification.

## From regressions to a predictive distribution

For allocation, each retained predictor follows a first-order VAR jointly with returns:

$$
r_{t+1}=b_j+C_jz_{j,t}+\epsilon_{j,t+1},\qquad
z_{j,t+1}=a_j+A_j'z_{j,t}+\eta_{j,t+1},
$$

$$
\begin{pmatrix}\epsilon_{j,t+1}\\\eta_{j,t+1}\end{pmatrix}
\sim N\!\left(0,
\begin{pmatrix}\Sigma_j&\Lambda_j\\\Lambda_j'&\Theta_j\end{pmatrix}\right).
$$

The posterior for the joint coefficient matrix and innovation covariance is constructed from another hypothetical sample, Appendix B. It matches predictor means and lag-one cross moments, centers return-predictor innovation covariance at zero, and uses an approximate predictor residual covariance that becomes exact when the first and last predictor observations coincide. Equations (B.2)–(B.3) give inverse-Wishart degrees of freedom $T_{j,0}-(N+m_j)-1$ and $T+T_{j,0}-(N+m_j)-1$ for this joint system. These are the source's stated joint-system prior choices; they should not be silently replaced by the return-regression degrees of freedom.

Model weights still come from the regressions that condition on predictors as fixed. The author deliberately avoids comparing likelihoods whose dependent-variable vectors change with the included predictor set. Thus the procedure combines fixed-design model weights with model-specific stochastic predictor dynamics; it is not the posterior from one fully specified common joint probability model for every candidate predictor.

For $K$ months, define cumulative excess log return $R_{T+K}=\sum_{h=1}^Kr_{T+h}$. Conditional on a model and its parameters, it is Gaussian. A numerically convenient finite-sum equivalent of equations (20)–(22) is

$$
\lambda_j=Kb_j+C_j\sum_{h=0}^{K-1}
\left[(A_j')^hz_{j,T}+\sum_{q=0}^{h-1}(A_j')^qa_j\right].
$$

Let $D_{j,k}=C_j\sum_{q=0}^{k-2}(A_j')^q$, with the empty sum zero. Then

$$
\Upsilon_j=K\Sigma_j+\sum_{k=1}^K
\left(D_{j,k}\Theta_jD_{j,k}'+\Lambda_jD_{j,k}'+D_{j,k}\Lambda_j'\right).
$$

Finite sums avoid the source's explicit inverse of $A_j'-I$, which fails at a unit eigenvalue even though a finite-horizon conditional distribution remains well defined. No undocumented stationarity rejection should be introduced when replicating posterior simulation. Conversely, the source does not describe whether explosive VAR draws were excluded; this matters for long-horizon Monte Carlo stability. The deterministic January indicator also requires a known calendar path rather than an ordinary Gaussian VAR innovation.

The algorithm samples a model with probability $p_j$, samples its covariance and coefficients from their posterior, then draws cumulative returns directly from $N(\lambda_j,\Upsilon_j)$. Direct terminal-return simulation avoids simulating every predictor path. Averaging these draws integrates both model and parameter uncertainty. The resulting unconditional predictive distribution is a mixture, generally nonnormal even though each conditional component is normal.

## Risk decomposition and portfolio problem

The law of total variance gives three components:

$$
\operatorname{Var}(R_{T+K}\mid D)=\sum_jp_j
\left[E(\Upsilon_j\mid D,M_j)+\operatorname{Var}(\lambda_j\mid D,M_j)
+(\mu_j-\bar\mu)(\mu_j-\bar\mu)'\right],
$$

where $\mu_j=E(\lambda_j\mid D,M_j)$ and $\bar\mu=\sum_jp_j\mu_j$. The terms are innovation risk, parameter risk, and disagreement between model means. They are covariance matrices; portfolio risk must retain their off-diagonal elements rather than average only marginal variance shares.

At December 1998 predictor values, the average one-month shares at prior strength 50 are reported as 93.8% innovation risk, 2.7% estimation risk, and 3.5% model risk. Quarterly counterparts are 84.5%, 6.0%, and 9.5%. These are conditional calculations at one state, not universal percentages. The SH monthly row actually has parameter risk .04 versus model risk .02, so “model risk is larger” describes an average, not every portfolio. Disagreement is amplified when current valuation ratios are far from their historical centers. The paper reports December 1998 BM .1178 versus mean .5078 and standard deviation .1790; TDW .5716 versus mean .6052 and standard deviation .0111.

A buy-and-hold investor chooses risky weights $w$ and cash weight $1-\mathbf1'w$. With constant monthly log bill rate $r_f$, terminal wealth from initial wealth one is

$$
W_{T+K}(w)=(1-\mathbf1'w)e^{Kr_f}
+\sum_{i=1}^Nw_i e^{Kr_f+R_{i,T+K}}.
$$

The objective is $E[W^{1-\gamma}/(1-\gamma)]$ under the model-averaged predictive distribution. The economically stated prohibition on shorting and margin requires $w_i\ge0$ and $\mathbf1'w\le1$. Merely constraining every risky weight to $[0,1]$, or imposing only nonnegativity as the optimization display says, does not prevent borrowing when multiple assets are present. The simplex constraint is the explicit reconstruction of the source's stated no-margin requirement.

The paper uses 400,000 independent predictive draws, relative risk aversion seven, and horizons one, two, four, six, eight, and ten years. A constrained optimizer maximizes sample-average utility. No solver, convergence tolerances, random seed, Monte Carlo standard errors, or treatment of extreme draws is provided. Weights are chosen once; there is no intertemporal rebalancing or learning policy. Transaction costs, taxes, cash-flow liabilities, and liquidity constraints beyond no shorting/no borrowing are not included.

The economic comparison evaluates the optimal BMA weights and each selected-model allocation under the *same BMA predictive distribution*. For horizon $H=K/12$ years, the annual certainty-equivalent gross factor is

$$
CE(w)=\left\{(1-\gamma)E[U(W_{T+K}(w))]\right\}^{1/[H(1-\gamma)]}.
$$

The loss is $CE(w^*)-CE(w_j)$; subtracting one to express net rates would leave the difference unchanged. It is a subjective expected-utility cost under the chosen mixture, not an independently realized performance advantage.

Table 8 at prior strength 50 assigns 36% to SH, 31% to BH, and 33% to cash at one year; at ten years the allocation is 27%, 35%, and 38%. Other equity portfolios receive zero. The all-predictor allocation loses 4.37 percentage points of annual certainty-equivalent rate at one year and 1.75 at ten years relative to BMA. At predictor sample means, corresponding losses are .15 and .24 percentage points. The source's claim that longer horizons necessarily make model-risk contributions vanish is conditional on convergence of model-specific expected-return paths; it is not a general property of arbitrary posterior VAR draws.

The absence of a rising equity share contrasts with familiar dividend-yield timing examples. Covariance between return innovations and predictor innovations determines whether future investment opportunities hedge current losses. Here posterior weight favors RET and TERM, whose positive innovation covariances can raise long-horizon risk, rather than persistent valuation signals that provide stronger mean reversion. This is a mechanism within the estimated system, not evidence that age or investment horizon never matters for households.

## Replication boundary and source trail

A defensible reconstruction should preserve the model prior, distinction between return and yield spreads, training-window empirical-Bayes inputs, quarterly publication lags, and joint return covariance. It should separately report results using the printed versus normalized marginal likelihood if investigating the source discrepancy. It also needs a stated parameter-count rule for prior strength, precise quarterly aggregation, calendar treatment, benchmark selection criteria, and numerical optimization controls. The paper's aggregate portfolio data reduce individual-stock implementation problems, but they do not supply a live-investable history or net trading-cost estimate.

The principal source pointers are equations (1)–(15) for regression/model averaging; (16)–(25) and Appendix B–D for predictive simulation and variance decomposition; (26)–(29) for utility and certainty equivalents; Appendix E for data; Tables 2–5 for predictor evidence; Table 6 for out-of-sample diagnostics; and Tables 7–8 for state-dependent risk and allocation. The most relevant methodological references in the supplied bibliography are Kandel and Stambaugh (1996), Barberis (2000), Bossaerts and Hillion (1999), West and McCracken (1998), Leamer (1978), and Zellner (1971). Their full methods are not reproduced in the supplied paper, so missing implementation conventions should remain explicit.
