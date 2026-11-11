# Volatility, Correlation, and Diversification in a Multi-Factor World

Richard Roll. *The Journal of Portfolio Management*, Winter 2013, pp. 11–18. Source: [Diversification_Roll_2013.pdf](../../Finance/Diversification_Roll_2013.pdf), nine PDF pages including the final rights notice. The complete article, two exhibits, appendix, and endnotes were read; mathematical expressions and table entries were checked visually.

## Why this matters

Low correlation between two packaged portfolios need not mean that the second portfolio supplies a new source of diversification to an investor who can already trade and recombine the constituents of the first. Both packages may be driven by exactly the same factors, with different exposure vectors. The investor may be able to construct the second package's factor profile entirely within the first opportunity set. The economically relevant question is then what the second package adds beyond an achievable mimicking portfolio, including residual risk, expected return, costs, and constraints.

Roll's contribution is a compact factor-spanning argument that separates this opportunity-set question from the usual two-index allocation problem. It does not invalidate covariance-based portfolio optimization. If an investor is restricted to two fixed indices, low covariance remains relevant to their combination. The paper asks a broader question by allowing the composition of one index's underlying assets to change. Its conclusions are strongest when factor exposures are known and replicating portfolios are feasible at low cost.

A separate appendix gives an implied-correlation calculation using options on a long asset, a short asset, and a leveraged spread ETF. That calculation is useful as an algebraic diagnostic, with important limitations when actual option-implied volatilities refer to different nonlinear payoffs, horizons, or smiles.

## Factor model and the correlation mechanism

Let asset $i$ follow

$$
R_{i,t}=E_i+\beta_{i,1}f_{1,t}+\beta_{i,2}f_{2,t}+\epsilon_{i,t}.
$$

The factors and residuals have zero means. Expected returns and factor sensitivities are assumed constant in the elementary model. For the diversification calculations, residuals are uncorrelated with the factors and with one another, as stated in endnote 4. The two-factor construction is illustrative; the linear-algebra mechanism extends to more factors.

Consider two diversified indices whose residual variances are negligible. In vector notation, $R_A-E_A=\beta_A^\top f$ and $R_B-E_B=\beta_B^\top f$. Writing the factor covariance matrix as $\Omega$, their correlation is

$$
\rho_{AB}=\frac{\beta_A^\top\Omega\beta_B}
{\sqrt{\beta_A^\top\Omega\beta_A}\sqrt{\beta_B^\top\Omega\beta_B}}.
$$

This explicit form reconstructs the paper's argument. Correlation measures the angle between covariance-scaled loading vectors; it does not count distinct underlying drivers. With positive-definite $\Omega$ and nonzero portfolio variances, the Cauchy–Schwarz equality condition gives $|\rho_{AB}|=1$ precisely when the loading vectors are proportional. Positive proportionality gives correlation +1 and negative proportionality gives −1. A singular factor covariance requires the corresponding statement in the effective factor subspace; raw loading proportionality is then stronger than necessary.

Exhibit 1 assumes equal factor variances and zero factor covariance. The loading relationships are $\beta_{A,1}=k_1\beta_{B,1}$ and $\beta_{A,2}=k_2\beta_{B,2}$, with $k_1,k_2$ ranging from −1 to 1. For arbitrary nonzero reference loadings,

$$
\rho_{AB}=\frac{k_1\beta_{B,1}^2+k_2\beta_{B,2}^2}
{\sqrt{k_1^2\beta_{B,1}^2+k_2^2\beta_{B,2}^2}
\sqrt{\beta_{B,1}^2+\beta_{B,2}^2}}.
$$

For equal reference loading magnitudes, this simplifies to $(k_1+k_2)/\sqrt{2(k_1^2+k_2^2)}$. Equal nonzero $k$ values give perfect signed correlation. Opposite appropriately weighted values give zero correlation. At $k_1=k_2=0$, portfolio A has no random variation and correlation is undefined; this is not a defined zero-correlation case. The exhibit's caption states equal factor variances but does not separately tabulate the reference betas, so the equal-loading simplification is a transparent illustrative normalization rather than an independently documented calibration.

A simple reconstruction makes the distinction concrete. Let independent unit-variance factors drive $R_A=f_1+f_2$ and $R_B=f_1-f_2$. Both returns are explained completely by the same two factors, but their covariance is zero and their correlation is zero. A 50/50 combination has return $f_1$ and variance 1 versus variance 2 for either original index. That reduction is real for a fixed-index investor. Roll's further observation is that an investor who can already create arbitrary combinations of the relevant factor exposures within A may obtain the same result without adding B. Thus “common factors” does not mean “no benefit from combining fixed portfolios”; it means the incremental benefit must be evaluated relative to the feasible span already available.

The economic examples use different sensitivities to growth, inflation, confidence, and energy. Saudi and Hong Kong stocks may share confidence shocks while responding oppositely to energy shocks. Their low correlation can therefore coexist with integration into a common factor system. These examples are mechanisms, not fitted empirical models in this article.

## Matching a candidate portfolio's risk profile

Suppose the investor can form a portfolio $A^*$ from assets already available in class A with the same factor loadings as index B:

$$
R_{A^*,t}=E_{A^*}+\beta_B^\top f_t+\epsilon_{A^*,t},\qquad
R_{B,t}=E_B+\beta_B^\top f_t+\epsilon_{B,t}.
$$

Let residual variances be $s_A^2$ and $s_B^2$, with zero residual covariance. A portfolio with weight $w$ in B and $1-w$ in $A^*$ has variance

$$
V(w)=\beta_B^\top\Omega\beta_B+(1-w)^2s_A^2+w^2s_B^2.
$$

Differentiating yields the source's central weight formula, printed p. 13:

$$
w^*=\frac{s_A^2}{s_A^2+s_B^2},\qquad
V(w^*)=\beta_B^\top\Omega\beta_B+
\frac{s_A^2s_B^2}{s_A^2+s_B^2}.
$$

These expressions hold when the denominator is positive. If $s_A^2=0$ and $s_B^2>0$, the variance-minimizing allocation to B is zero. If both residual variances vanish, every combination has the same factor risk; the weight expression is undefined as $0/0$, but there is no residual-risk benefit to optimize. If both are positive, the reduction relative to $A^*$ is $s_A^4/(s_A^2+s_B^2)$. The residual variances, rather than the correlation of the original indices A and B, determine this incremental risk reduction.

The restriction on residual covariance is consequential. As a diagnostic extension, if $\operatorname{Cov}(\epsilon_{A^*},\epsilon_B)=c$, then the unconstrained optimum becomes

$$
w^*=\frac{s_A^2-c}{s_A^2+s_B^2-2c}.
$$

A long-only allocation would clip that value to $[0,1]$ when the denominator is positive. This correlated-residual formula is derived here to expose the source assumption; it is not a separate result reported in the paper. Factor models with omitted sector risks or correlated residuals can otherwise overstate the gain from averaging residuals.

The same argument applies to adding a single security. If an existing portfolio can exactly mimic its factor exposure with less idiosyncratic risk, the security does not improve the attainable risk profile merely because its correlation with the current index is low. A higher expected return can still make the security desirable. The paper explicitly separates this return motive from diversification. The word “dominates” must therefore be read conditionally: matching systematic exposure and lowering residual variance establish risk dominance, but full mean–variance dominance also depends on relative expected returns.

## Feasibility is part of the proposition

Factor matching is an assumption about tradable opportunities, not a consequence of two indices having high factor-model $R^2$. To make it operational, let $B_A$ be the matrix of factor loadings of available A assets and $x$ their holdings. One must solve $B_A^\top x=\beta_B$ subject to the portfolio's financing and trading restrictions. Full investment may require $\mathbf1^\top x=1$, or a cash position may absorb the difference. Shorting, derivatives, and cheap leverage can expand the feasible loading set. Long-only limits, concentration limits, illiquidity, or missing factor directions can prevent the required match.

A reproducible implementation extension is to minimize $x^\top D_Ax$ subject to factor matching and the actual constraints, where $D_A$ is residual covariance. This selects the lowest-residual-risk mimic rather than an arbitrary matching portfolio. The article motivates engineering such a portfolio but does not specify this optimization, estimate $D_A$, or run it on a named dataset. Reporting the optimization as an implemented source backtest would therefore be incorrect.

The distinction matters for the article's emphasis on $R^2$. High explanatory power for a common factor system suggests that residual diversification is limited once matching is possible. It does not prove that the investor's accessible holdings span the candidate loading vector. A strong factor fit with inaccurate estimated loadings can also generate a poor realized hedge. A replication should inspect loading rank, numerical conditioning, tracking error, and constraint feasibility, rather than substitute an $R^2$ threshold for a spanning test.

## What should count as a factor?

Roll interprets the relevant factors as high-frequency changes in market perceptions of pervasive economic conditions. Official macroeconomic releases arrive too slowly to explain all rapid asset-price movements directly. Perceptions can involve rational revisions to growth, inflation, real rates, and energy, as well as shifts in confidence, liquidity, or risk appetite. This framing does not uniquely identify a factor model.

The paper compares four proxy strategies. Statistical principal components or factor analysis can recover common variation, but require sufficient stability of the system being estimated. Prespecified macroeconomic variables have a clearer economic interpretation but low observation frequency and require innovations rather than levels. Characteristics such as size, value, and momentum can provide empirical return proxies without necessarily corresponding to primitive economic risks. Finally, heterogeneous liquid portfolios can span the relevant factors without naming them individually.

The last method receives particular attention. The article cites earlier evidence that replacing ten global principal components with ten broad country indices produced similar measures of market integration. That is a result from the cited study, not a newly re-estimated robustness exercise in the current paper. Tradable ETF proxies are attractive because they are observable frequently and can span different asset classes. Yet many equity ETFs are too similar to each other to provide much independent variation. Changes in index composition and derivative-based exposures also complicate the stability of their loadings.

## ETF illustration and a reconstructable volatility measure

Exhibit 2 reports 25 prominent equity ETFs against the S&P 500, using monthly observations from each ETF's inception through March 2010. Sample lengths differ, ranging from 27 months to 205 months. Consequently, even the benchmark's reported volatility differs across rows. The table gives correlation, regression beta, its $t$ statistic, ETF and benchmark annualized volatilities, and an EDM measure: the maximum percentage volatility reduction from combining the ETF and the S&P 500 without shorting either.

Selected exact reported values are:

| ETF | Months | Correlation | Beta | ETF vol. | Index vol. | EDM |
|---|---:|---:|---:|---:|---:|---:|
| IYY | 116 | 0.9933 | 1.034 | 16.50% | 15.85% | 0.000% |
| IVV | 117 | 0.9979 | 0.989 | 15.67% | 15.80% | 0.852% |
| DDM | 45 | 0.9779 | 1.836 | 34.23% | 18.23% | 0.000% |
| SSO | 45 | 0.9963 | 2.018 | 36.93% | 18.23% | 0.000% |
| XLG | 58 | 0.9781 | 0.884 | 14.78% | 16.37% | 9.670% |
| SPY | 205 | 0.9969 | 0.991 | 14.90% | 14.99% | 0.628% |
| VIG | 47 | 0.9754 | 0.810 | 14.86% | 17.90% | 16.997% |

Volatilities are standard deviations, not variances. All 25 displayed correlations exceed 0.97. The examples support the limited heterogeneity of these equity ETF packages; they do not constitute an out-of-sample test of a multi-asset factor-spanning strategy.

The EDM definition can be implemented from two variances and their covariance. With weight $x$ in the ETF and $1-x$ in the index, let $v_E$, $v_I$, and $c$ be their variances and covariance. Then

$$
x^*=\operatorname{clip}_{[0,1]}
\left(\frac{v_I-c}{v_E+v_I-2c}\right),\qquad
\mathrm{EDM}=100\left(1-\frac{\sqrt{x^{*2}v_E+(1-x^*)^2v_I+2x^*(1-x^*)c}}{\sqrt{v_I}}\right).
$$

This derivation implements endnote 6. The zero-denominator case corresponds to identical random return components and needs separate handling. Using rounded published inputs may not reproduce all EDM values exactly. The article does not disclose the underlying monthly series, all return adjustments, the ETF selection rule, or confidence intervals. It does not provide a trading rule for replacing factor proxies over time or a cost-adjusted performance comparison.

## Appendix: implied correlation from a spread ETF

Let a spread ETF hold signed weights $w_L$ and $w_S$ in two underlying assets, with $w_S<0$. Assume financing does not add volatility. For its daily return,

$$
R_E=w_LR_L+w_SR_S,
$$

and the variance identity is

$$
\sigma_E^2=w_L^2\sigma_L^2+w_S^2\sigma_S^2+
2w_Lw_S\rho\sigma_L\sigma_S.
$$

If the three volatilities are available on a consistent basis, invert it:

$$
\rho=\frac{\sigma_E^2-w_L^2\sigma_L^2-w_S^2\sigma_S^2}
{2w_Lw_S\sigma_L\sigma_S}.
$$

The source proposes obtaining them from simultaneous option prices on the two constituents and the ETF. In its example, $w_L=2$, $w_S=-2$, and annualized volatilities are 20%, 15%, and 35%. The result is

$$
\rho=\frac{0.2^2+0.15^2}{2(0.2)(0.15)}
-\frac{0.35^2}{8(0.2)(0.15)}=0.53125.
$$

The mathematical feasibility bound $|\rho|\leq1$ implies

$$
\left||w_L|\sigma_L-|w_S|\sigma_S\right|
\leq\sigma_E\leq |w_L|\sigma_L+|w_S|\sigma_S.
$$

The example therefore requires ETF volatility between 10% and 70%. Holding constituent volatilities fixed, a higher correlation lowers spread volatility because the cross term has a negative coefficient. If one's correlation view is lower than the quoted implied value, the corresponding spread variance should be higher, making a long-volatility position on the spread the natural direction under the model.

The variance algebra is exact for linear returns with fixed weights over the measurement interval. Its interpretation through three vanilla option-implied volatilities is more conditional. Implied volatility is a model-dependent transformation of option prices, not automatically a common-horizon variance under one measure. Different strikes, maturities, volatility smiles, jumps, dynamic ETF rebalancing, and financing can break the direct identification. The source describes out-of-bound values as pure arbitrage; in practice that conclusion requires a consistent joint pricing model and executable hedging instruments, not merely plugging three unrelated Black–Scholes implied volatilities into the identity. Likewise, a subjective disagreement about correlation indicates a risky relative-value view, not a guaranteed trading profit. These are qualifications to the appendix's economic interpretation, not changes to its arithmetic.

## Scope of the result

The paper's theoretical claim is about incremental attainable risk profiles after allowing factor-matching trades. Its empirical ETF table illustrates redundant packaged exposures, while the appendix offers a related market-implied diagnostic. Neither component estimates a comprehensive investment policy or establishes its realized net performance.

For research use, the strongest takeaway is to compare a proposed investment with the best feasible substitute already in the opportunity set. Record systematic exposure differences, residual tracking risk, expected return differences, and the cost of creating the substitute. Correlation between current packages is an input to that analysis, but cannot alone establish whether a new package adds a tradable risk direction. When matching is infeasible, costly, or unstable, the package may remain valuable even if its returns are explained by the same statistical factors.
