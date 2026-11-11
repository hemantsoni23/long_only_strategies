# Does Stock Return Predictability Imply Improved Asset Allocation and Performance? Evidence from the U.S. Stock Market (1954–2002)

Puneet Handa and Ashish Tiwari (2006), *Journal of Business* 79(5), 2423–2468, DOI 10.1086/505240. [Supplied PDF](../../Finance/PredictableReturns_HandaTiwari_2006.pdf). Printed journal page numbers are used below; PDF page 2 is journal page 2423. Both mathematical appendices are included in the supplied 47-page file.

## Why this matters

Return predictability can change a portfolio substantially without improving its realized performance. Handa and Tiwari test this distinction by repeatedly estimating forecasts using historical information, choosing among forecasting models, optimizing positions with estimation uncertainty and trading costs, and then recording next-month outcomes. The competing investor also updates estimates but assumes returns are independent and identically distributed. The comparison therefore asks whether conditioning variables improve decisions beyond ongoing learning about unconditional returns.

The result is mixed for dividend yield, the short rate, default spread, and term spread. Predictive allocations can generate large certainty-equivalent gains in some periods, yet lose badly in others. In the single-stock-index experiment, a moderately risk-averse investor gains 38 basis points per month in 1959–1973 and 12 in 1974–1988, then loses 59 in 1989–2002 relative to the unconditional strategy. The full-period difference is −3 basis points. A model-selection procedure that contains the unconditional model is not protected against this deterioration because it selects using past performance, which need not identify the best model in a changing environment.

A different use of information works better: shrinking expected industry returns toward the static CAPM. With strong confidence in zero pricing errors, the reported full-period certainty-equivalent improvement is 45 basis points per month for risk aversion 5 and 51 for risk aversion 10. Allowing alphas, betas, and the market premium to vary with the four predictors does not improve this result consistently. The distinction is between adding flexibility to fit conditional means and imposing restrictions to stabilize cross-sectional expected-return estimates.

The paper's contribution is the combination of sequential portfolio evaluation, parameter uncertainty, model selection based on realized utility, proportional costs, and constrained leverage. It is not a full Bayesian treatment of model uncertainty: the predictor strategy selects one model each month instead of integrating over model probabilities. Its “real-time” claim means use of historical data through the preceding month, not an audited point-in-time vintage database. Several printed formula and inference gaps prevent exact reconstruction from the article alone; those are identified explicitly below.

## Data, information timing, and investment opportunities

The estimation history is January 1954–December 2002. January 1954–December 1958 supplies 60 initial learning observations, and performance is evaluated over January 1959–December 2002, 528 months. Expanding estimation windows begin in January 1954 and end immediately before each decision month. The three evaluation subperiods are 1959–1973 and 1974–1988, each 180 months, and 1989–2002, 168 months. Occasional prose referring to a final subperiod beginning in 1988 is inconsistent with the defined and tabulated 1989 start.

The single risky asset is the CRSP value-weighted NYSE/AMEX/NASDAQ stock index. The three-asset experiment combines CRSP capitalization decile portfolios into large, medium, and small groups by value weighting. The source's decile numbering puts the largest firms in deciles 1–3, medium firms in 4–7, and small firms in 8–10; a modern dataset using the opposite convention must be remapped. Excess returns subtract the one-month Treasury bill return. The CAPM experiments instead use ten industry portfolios from Ken French: chemicals, durables, financials, manufacturing, nondurables, oil, retail, telecommunications, utilities, and a miscellaneous group. Historical industry definitions and constituent handling must match the supplied vintage if exact table replication is intended.

Four predictors are available at the end of the preceding month. Dividend yield is the natural logarithm of trailing twelve-month dividends on the CRSP value-weighted index divided by the current index level. The short-rate predictor is the one-month bill yield minus its backward twelve-month moving average. Default spread is Moody's BAA corporate yield minus AAA yield. Term spread is the ten-year Treasury yield minus the three-month Treasury yield. CRSP supplies the bill data and the Federal Reserve Bulletin supplies spreads. The regressions use all predictors with a one-month lag.

The one-month bill return and the detrended yield predictor are not automatically in the same annualization units. Table 1 reports bill-return standard deviation 0.0021 but detrended-yield standard deviation 0.0113. A replication must reconcile source series units rather than mechanically treating both as monthly decimal returns. The article does not fully document yield conversion conventions, publication timing, or revisions. Its prior estimates use 1946–1953 data, which are separate from both the expanding estimation history and the 1954–1958 learning window.

Table 1 reports mean monthly market excess return 0.55% and standard deviation 4.38%; small-, medium-, and large-cap mean excess returns are 0.77%, 0.70%, and 0.53%. Log dividend yield has mean −3.4913, standard deviation 0.4019, and first-order autocorrelation 0.9893. Default and term spreads also have high persistence, 0.9711 and 0.9444. This persistence is relevant to predictive-regression inference and to the long blocks used in the bootstrap.

## Portfolio objective, trading costs, and leverage

Both investors use a one-period mean–variance objective with risk aversion $\lambda\in\{2,5,10\}$. Let $\mu_t$ and $\Sigma_t$ denote the posterior predictive mean and covariance of excess risky returns, $w_t$ their weights, and $r_{f,t}$ the known bill return. Expected total return and variance are

$$
E_t[r_{p,t}]=r_{f,t}+w_t'\mu_t,
\qquad
\operatorname{Var}_t(r_{p,t})=w_t'\Sigma_t w_t.
$$

The intended proportional-cost optimization is

$$
\max_{w_t}\left\{
 w_t'\mu_t-\frac{\lambda}{2}w_t'\Sigma_t w_t
 -\kappa\sum_i|w_{i,t}-w_{i,t-1}|
\right\},
\qquad \sum_i|w_{i,t}|\le2,
$$

with $\kappa=0.0025$, or 25 basis points per one-way trade and 50 basis points for a complete round trip. Cash trades are free, the residual cash weight is $1-\sum_iw_{i,t}$, and borrowing is allowed at the risk-free rate. The gross exposure constraint permits individual short positions and total absolute risky exposure up to 200%; it is not a 200% long-only constraint or separate 200% limits on each asset. For one risky asset it reduces to $-2\le w_t\le2$.

The absolute values in the cost term above are a **derived correction to match the source's stated proportional trading costs**. Printed equation (4), page 2430, contains $\kappa(w_{i,t}-w_{i,t-1})$ without absolute values, although it does use absolute values in the exposure constraint. Read literally, sales receive a cost rebate, and a round trip has zero net cost. That contradicts the accompanying 50-basis-point round-trip description. The paper does not reveal whether this is merely a typesetting omission in the equation or a feature of the implementation.

The notation also measures turnover relative to the previous selected weight, without explicitly adjusting that weight for intervening returns. Actual turnover should generally be measured from the pretrade, drifted holdings. The article does not specify that accounting detail or whether initial positions and final liquidation receive costs. These choices matter for exact reproduction. At a fixed convention the intended problem is a convex quadratic program after introducing auxiliary variables for turnover and absolute exposure. The covariance is predictive rather than a plug-in residual covariance, so uncertainty about estimated means can reduce exposure.

This is myopic optimization. It does not solve a dynamic consumption problem, include intertemporal hedging demand, or treat future transaction costs as a continuation-value term. The authors call $\lambda$ relative risk aversion, but the implemented criterion is the stated mean–variance functional; it should not be substituted for exact CRRA expected utility without changing the experiment.

## Bayesian predictive regression and a source formula gap

For each predictor subset, write the observed excess return vector as

$$
R=Xb+\varepsilon,
\qquad \varepsilon\mid h\sim N(0,h^{-1}I_T),
$$

where $h$ is precision and $X$ includes an intercept. The unconditional model uses only that intercept. The article specifies a normal–gamma prior

$$
s_0^2h\sim\chi^2_{\nu_0},
\qquad b\mid h\sim N(b_0,h^{-1}H_0^{-1}),
\qquad \nu_0=15.
$$

It sets $b_0$ from OLS over 1946–1953 and describes $s_0^2$ as an average historical variance estimate. The printed prior specification then sets $H_0=s_0^2(\nu_0-2)$, which is a scalar even when $b$ has multiple elements. An identity-matrix convention or a fully specified precision matrix is needed, and the article does not give predictor-specific prior scaling. Moreover, under the displayed chi-square convention $E[h^{-1}]=s_0^2/(\nu_0-2)$, so setting $s_0^2$ itself equal to the desired prior mean variance would require a different scale normalization. These are reproduction ambiguities, not evidence about which internal parametrization the authors used.

For a dimensionally conformable prior precision, the posterior coefficient calculations are

$$
H_T=H_0+X'X,
\qquad b_T=H_T^{-1}(H_0b_0+X'R).
$$

The scale required by the stated normal–gamma likelihood is, by completing the square,

$$
s_T^2=s_0^2+(R-X\widehat b)'(R-X\widehat b)
 +(\widehat b-b_T)'X'X(\widehat b-b_T)
 +(b_0-b_T)'H_0(b_0-b_T).
$$

Then $s_T^2h\mid R\sim\chi^2_{\nu_0+T}$, and the one-step moments at known design vector $x_*$ are

$$
E[r_*\mid R]=x_*'b_T,
\qquad
\operatorname{Var}(r_*\mid R)
=\frac{s_T^2}{\nu_0+T-2}
\left(1+x_*'H_T^{-1}x_*\right).
$$

These last expressions are a standard derivation under the displayed prior, not a claim that the printed article states them correctly. Its equation (9) defines $Q$ using only the last two coefficient-discrepancy terms, omitting the residual sum of squares $(R-X\widehat b)'(R-X\widehat b)$. Equation (8) then uses $s_0^2+Q$ as the updated scale. This cannot generally be the posterior precision distribution under equation (6), because residual variation must enter. Equation (10)'s Student distribution also leaves the scale convention implicit; the scale matrix and the covariance differ by degrees-of-freedom factors. Visual inspection confirms these are printed features rather than extraction errors.

The three-risky-asset version needs a joint predictive covariance. The authors omit its derivation as similar in spirit to the scalar case, so the article alone does not uniquely specify its covariance prior. A matrix-normal/inverse-Wishart implementation is a reasonable extension, but would be a declared implementation choice, not a recovered author setting. A robustness variant jointly models returns and predictors as a first-order VAR; the full prior and estimation details for that variant are likewise not tabulated.

## Sequential model choice and performance measurement

There are $2^4=16$ predictor subsets, including the intercept-only model. At every month the active investor compares the historically realized utility of the allocation path associated with each model and chooses the best-performing model to forecast and allocate for the next month. Parameters are re-estimated using only historical observations. The base model-selection performance window expands; alternatives use 60, 36, or 12 months. The estimation window and the window used to rank models are conceptually separate, even when both expand.

A reconstructable implementation must maintain sixteen model-specific shadow portfolios, calculate their prior-month net returns, update historical mean–variance scores, select the winning model using only scores available before trading, and apply its predictive moments to the live portfolio's optimization. The source does not resolve tie-breaking, how the first model is chosen before sufficient realized shadow performance exists, or whether switching costs use the live holdings or a candidate's hypothetical prior holdings during evaluation. Those details can change performance when selected models imply widely different positions.

The main realized performance measure is

$$
\mathrm{CER}=\bar r_p-\frac{\lambda}{2}s_p^2,
\qquad
\Delta\mathrm{CER}=\mathrm{CER}_{\mathrm{predictive}}-\mathrm{CER}_{\mathrm{iid}},
$$

using realized returns net of costs and a monthly variance. The tables express CER differences in basis points per month. They are not annualized fees and are not differences between arithmetic mean returns alone. A riskier strategy can have a positive mean-return difference and a negative CER difference.

The “adjusted Sharpe ratio” is Graham–Harvey's volatility-matched return difference, not a dimensionless Sharpe ratio. The unconditional portfolio is combined with bills and levered or unlevered to match the predictive portfolio's realized volatility; the difference in average returns is reported. With constant risk-free return it has the form $\bar r_M-r_f-(s_M/s_I)(\bar r_I-r_f)$. Actual variable-rate handling should follow the underlying monthly series. The source appropriately treats CER as primary because it corresponds to the allocation criterion.

Inference uses 1,000 stationary-bootstrap replications, a geometric block length with mean 60 months, and sequential re-estimation and allocation through each 528-month resample. The restart probability is therefore $q=1/60$. Recomputing allocations is essential: resampling only the final realized portfolio returns would not reproduce the stated learning experiment.

However, the article describes counting resampled differences that exceed the original difference, while also interpreting the result as a test under no predictability. It does not explicitly describe null centering, restricted-model generation, joint resampling of returns with predictors, or two-sided treatment of negative differences. An ordinary bootstrap from the observed joint process preserves its predictive relationships and is not automatically a no-predictability null. The numerical values below are consequently **the authors' reported bootstrap p-values**, not independently verified null probabilities or posterior probabilities that one investor will outperform.

The paper also applies a sign test to nine combinations of three subperiods and three risk aversions. Six positive differences yield a one-sided binomial p-value of 0.2539. Its footnote explicitly assumes nine independent draws. Results for different risk aversions on the same returns are dependent, so that independence assumption is a material limitation rather than a harmless simplification.

## Predictor-based allocation results

Table 3, pages 2442–2443, reports the following CER differentials in basis points per month. Each vector follows risk aversions 2, 5, and 10.

| Evaluation period | One stock index | Three size portfolios |
|---|---:|---:|
| 1959–1973 | 28, 38, 17 | 26, 42, 22 |
| 1974–1988 | 136, 12, −7 | 157, −13, −21 |
| 1989–2002 | −56, −59, 1 | −72, −20, −2 |
| 1959–2002 | 37, −3, 4 | 38, 3, 0 |

For the full one-index sample the reported CER p-values are 0.574, 0.922, and 0.744; the corresponding three-portfolio values are 0.480, 0.896, and 1.000. Thus the large full-sample low-risk-aversion economic gain is not accompanied by a small reported p-value. The headline average gain of approximately 37 basis points in the first two subperiods masks the fact that much of the second-period gain is concentrated at risk aversion 2.

Figure 1, page 2445, illustrates the mechanism for risk aversion 5. The predictive portfolio repeatedly changes from heavily short to heavily long, reaching approximately −160% to −200% and +160% to +200% during the volatile middle period. The unconditional investor is much more stable, initially around 120%–200% equity and subsequently near 80%. Such swings raise costs and expose the predictive strategy to forecast error; posterior parameter uncertainty alone does not suppress them.

Full-sample fitted regressions do show predictive relationships. In Table 2 the detrended bill-yield slope is −0.689 with Newey–West $t=-4.30$ in the univariate regression and −0.706 with $t=-3.11$ in the full model. Its univariate adjusted $R^2$ is 2.99%; the four-predictor adjusted $R^2$ is 3.62%. Dividend yield is significant in several combinations; default spread is not conventionally significant over the full sample. The table caption says 1954–2002 whereas the preceding prose describes 1959–2002, an unresolved sample-label inconsistency. These in-sample statistics do not repair the out-of-sample allocation instability.

Table 5 explains why availability of the unconditional model is insufficient. For risk aversion 5 it is selected only 3.60% of months overall and never in either of the last two subperiods under expanding model selection. The most frequently used model is the short-rate-only model B in the middle and final periods, but the best fixed model ex post in the final period is term-spread-only model D. Continuing with model B yields a final-period monthly CER of 3.75 basis points, versus 52.21 for the unconditional model and 62.45 for model D. Those are hindsight comparisons, not feasible oracle selections.

Shortening the ranking window shifts the losses rather than consistently removing them. For 60-, 36-, and 12-month windows, risk-aversion-5 CER differentials across the three subperiods are respectively $(36,0,-32)$, $(63,-21,-22)$, and $(44,-57,5)$ basis points. Full-period differences are 2, 7, and −3. Selecting the best window after seeing these paths would add a further layer of data selection.

The market-timing experiment switches entirely between stocks and bills according to the forecast sign. Table 4 reports overall accuracy 53.89%, 58.33%, and 40.48% across the subperiods, or 51.14% overall. The full-sample conditional hit rates are 52.15% in up markets and 49.78% in down markets. Always predicting an up market would achieve 57.39% unconditional accuracy in this sample, so the coin-toss benchmark alone is weak. Accuracy also ignores the magnitudes of missed gains and losses.

The accompanying prose gives conflicting counts: it says the strategy holds bills in 57 of 225 down months and 63 of 303 up months. Those counts imply only 25.33% correct down predictions and 79.21% correct up predictions, inconsistent with Table 4's 49.78% and 52.15%. They may refer to a different unreported policy, but the source does not establish that. This note uses the table for reported timing accuracy and flags the counts rather than combining them.

## Static CAPM shrinkage and conditional-factor extensions

The static approach follows Pástor and Stambaugh. For nonbenchmark industry excess returns $r_1$ and market excess return $r_2$,

$$
r_{1,t}=\alpha+B r_{2,t}+u_t,
\qquad u_t\sim N(0,S).
$$

The prior centers $\alpha$ at zero, with $\alpha\mid S\sim N(0,\sigma_\alpha^2 S/s^2)$. The annualized prior pricing-error standard deviation is set to approximately 0%, 2%, or infinity, representing strong, intermediate, or negligible confidence in the CAPM. The numerical approximations to zero and infinity and the annual-to-monthly conversion are not supplied. They must be fixed explicitly for a reproduction.

Appendix A expresses shrinkage using $Y=ZA+U$, $Z=[\mathbf1,r_2]$, and $A=[\alpha,B]'$. Define $D=\operatorname{diag}(s^2/\sigma_\alpha^2,0)$ and $F=D+Z'Z$. The posterior coefficient mean is $\widetilde A=F^{-1}Z'Y$. With an inverse-Wishart residual prior and $\nu=15$, the posterior mean residual covariance is

$$
\widetilde S=
\frac{H+T\widehat S+\widehat A'Q\widehat A}
{T+\nu-m-k-1},
\qquad Q=Z'(I-ZF^{-1}Z')Z,
$$

where $m$ is the number of nonbenchmark assets and $k=1$ the benchmark count. The article gives the role of the prior scale $H$ but does not fully calibrate its matrix entries. Factor mean and covariance uncertainty must also be integrated. If $e$ is the posterior mean market premium and $V_f$ its predictive variance, the nonbenchmark predictive mean is $\widetilde\alpha+\widetilde B e$; predictive covariance includes residual covariance, factor risk, uncertainty in betas interacting with factor risk, and covariance of estimated conditional means. Appendix A equation (A8) supplies these terms explicitly, so using only $\widetilde B V_f\widetilde B'+\widetilde S$ would understate uncertainty.

Table 6's full-period CER differences are:

| Annual prior alpha uncertainty | $\lambda=2$ | $\lambda=5$ | $\lambda=10$ |
|---|---:|---:|---:|
| Approximately 0% | −10 (0.777) | 45 (0.016) | 51 (0.034) |
| 2% | 4 (0.645) | 23 (0.136) | 41 (0.130) |
| Approximately infinite | −11 (0.269) | 18 (0.202) | 36 (0.152) |

Entries are monthly basis points with reported p-values in parentheses. Strong confidence is beneficial at moderate and high risk aversion, but the favorable result is not universal across investors or periods. Under near-zero alpha uncertainty, the first-period gains at risk aversions 5 and 10 are 89 and 125 basis points, whereas the middle-period low-risk-aversion difference is −56. None of the full-sample adjusted volatility-matched return differences has a small conventional p-value. Shrinkage can improve the relevant utility measure without demonstrating a higher conventional Sharpe ratio.

The conditional extension specifies

$$
r_{t+1}=\alpha_0+\alpha_1z_t+(\beta_0+\beta_1z_t)f_{t+1}+v_{t+1},
\qquad f_{t+1}=a_f+A_fz_t+v_{f,t+1},
$$

and a first-order VAR for the four-dimensional predictor vector $z_t$. Stock regressions include $[1,z_t',f_{t+1},f_{t+1}z_t']$, ten columns. Priors are noninformative; alphas are either unrestricted or fixed to zero. Appendix B takes residual asset covariance to be diagonal and adds a common market-risk component. This assumption itself changes the covariance estimator and should not be confused with unrestricted industry residual dependence.

For implementation, let $x=[1,z']'$, $g(f)=[x',f,fz']'$, $\Omega_i=(G_i'G_i)^{-1}$, and $L=\partial g/\partial f$. With forecast market mean $m_f$, variance $V_f$, and $\bar g=g(m_f)$, the Appendix B parameter-risk adjustment can be written compactly as $d_i=\bar g'\Omega_i\bar g+\operatorname{tr}(\Omega_iLV_fL')$. Then the covariance has the form $\operatorname{diag}\{\widetilde\omega_i(1+d_i)\}+\beta(z)V_f\beta(z)'$. This is an algebraic restatement of its partitioned equations, not a new estimated result. The printed dimensions for the regression coefficient matrix and an undefined $K$ in equation (B6) require correction to the actual ten-column, one-factor design; restricted-alpha cases must also reduce the coefficient count appropriately.

Table 7 shows that extra flexibility can be expensive. Full-period unrestricted-alpha CER differences are 23, −5, and −113 basis points at risk aversions 2, 5, and 10. In 1974–1988 the risk-aversion-10 difference is −234 basis points with reported p-value 0.043. Restricted-alpha full-period differences are −31, 7, and −2. Figure 3 shows aggressive 120%–200% equity exposure for much of the middle period, when realized returns were volatile. Adding conditional parameters is not simply an improvement on static CAPM shrinkage.

## Robustness, interpretation, and missing replication inputs

The reported VAR robustness gives full-period single-index CER gains of 11, 12, and 4 basis points across the three risk aversions. Prohibiting short sales gives 4, 17, and 9. Eliminating costs gives 45, −6, and 7, so the moderate-risk-aversion failure is not solely a trading-cost artifact. Priors based on 1926–1953 and different prior sample sizes retain qualitative instability. Detailed robustness tables are said to be available on request and are not contained in this PDF; their precise allocations and uncertainty cannot be reconstructed from the brief numerical examples.

A new implementation should first settle the normal–gamma scale and missing residual term, transaction-cost absolute values, drifted holdings, and multivariate prior. It should then preserve separate model-specific estimation and evaluation histories, report actual gross and net holdings, and specify bootstrap null generation and predictor resampling. Without these choices, numerical disagreement with the tables would be difficult to diagnose. None of the derived formula repairs in this note establishes that the authors' code made the printed errors.

The evidence supports a narrower conclusion than “predictors are valuable because they are frequently selected.” Selection from fifteen predictive alternatives and one unconditional alternative can favor predictive models even without stable economic gains. The useful finding is that sequential selection and posterior uncertainty do not guarantee stable allocation benefits, while theoretical shrinkage restrictions can help particular investors in this historical sample. The study ends in 2002, uses stylized financing and costs, and does not supply a modern executable strategy, a causal account of regime change, or proof that all forms of conditional forecasting lack value.

## Bibliographic and source pointers

The complete supplied article was read, including Appendix A on static CAPM predictive moments and Appendix B on conditional factor moments, pages 2462–2465. Important equations, portfolio tables, and allocation figures were inspected visually. Design and Bayesian inputs are on pages 2429–2437; predictive and allocation evidence on pages 2438–2449; static and conditional CAPM results on pages 2450–2460. The discussion above distinguishes reported estimates, unresolved printed specifications, and explicitly derived repairs.

The article builds on Kandel and Stambaugh (1996) for the allocation consequences of predictability, Pesaran and Timmermann (1995) for recursive model selection, Pástor and Stambaugh (2000) for asset-pricing-based shrinkage, and Politis and Romano (1994) for the stationary bootstrap. Those references define the intellectual components; all numerical results here are from the supplied Handa–Tiwari article.
