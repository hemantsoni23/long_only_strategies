# Expectations of Returns and Expected Returns

Robin Greenwood and Andrei Shleifer, *The Review of Financial Studies* 27(3), 2014, pp. 714–746. DOI: 10.1093/rfs/hht082. Source: [InvestorExpectations_GreenwoodShleifer_2014.pdf](../../Finance/InvestorExpectations_GreenwoodShleifer_2014.pdf). All thirty-three supplied pages, including Appendix Table A.1, were read; the rotated regression tables were inspected visually. The authors' [March 2014 Internet Appendix](https://shleifer.scholars.harvard.edu/sites/g/files/omnuum10626/files/shleifer/files/expectations_internet_appendix_updated.pdf) was also inspected through its eight-page text extraction. It supplies raw survey series, excluding licensed Investors Intelligence data, but does not contain the detailed index algorithm and bias-adjustment results promised in the article. Its table layout could not be rendered in this inspection.

## Why this matters

An investor's stated forecast of future returns and an econometrician's conditional expected return are different empirical objects. This paper assembles six survey measures and asks whether their movements agree with model-based expected-return proxies. The answer is largely no. Respondents become more optimistic after strong market returns and at high valuations, whereas dividend yields and several consumption-based proxies usually imply lower subsequent returns in those states. Survey expectations also tend to predict realized returns with a negative sign.

The contribution is the joint evidence, not a new equilibrium model or an optimized sentiment strategy. The surveys cover individuals, corporate CFOs, newsletter writers, wealthy investors, and consumers; their common movements make it harder to dismiss the entire pattern as one poorly worded question. Mutual-fund flows move with reported optimism, connecting statements to aggregate investment behavior. Equity issuance offers suggestive evidence about participants accommodating that demand.

For implementation, the paper suggests maintaining separate variables for subjective beliefs, econometric return forecasts, and required compensation for risk. Calling all three “expected returns” can conceal a substantive disagreement. It also creates a test for asset-pricing models: matching prices and realized return predictability is insufficient if the model identifies its representative investor with people whose reported beliefs move in the opposite direction.

The results do not establish a profitable timing rule after costs. Most regressions are descriptive, use heterogeneous samples, and are estimated over the available historical period. The composite expected-return forecast and survey rescalings are not presented as an expanding-window trading experiment. A prospective strategy would need a separate real-time information set and validation design.

## The six survey series

The maximum span is January 1963–December 2011, determined by Investors Intelligence. Most surveys begin much later. Do not construct a balanced panel starting in 1963 by silently filling nonexistent observations.

| Series | Population and question | Construction and usable observations |
|---|---|---|
| Gallup | Individual investors; optimism about market performance over the next twelve months | Percentage optimistic or very optimistic minus percentage pessimistic or very pessimistic; October 1996–December 2011, 135 observations, with gaps |
| Graham–Harvey | More than 200 corporate CFO responses per quarter; expected S&P 500 return over the next year | Mean numerical expected return; October 2000–December 2011, 42 quarterly observations |
| AAII | Association members; bullish, neutral, or bearish over the next six months | Bullish minus bearish, averaged from weekly observations into months; July 1987–December 2011, 294 observations |
| Investors Intelligence, abbreviated II | Editors classify more than 120 investment newsletters | Bullish minus bearish, averaged within month; 588 monthly observations from 1963–2011 |
| Shiller | Individual-investor confidence survey, drawn from wealthy investors | Percentage expecting a market increase over the next year; 132 observations, irregular initially and monthly after July 2001 |
| Michigan | Consumer survey respondents | Mean annualized expected stock return over the next two to three years; 22 irregular observations, 2000–2005 |

The horizons are intentionally not homogeneous. AAII is six-month directional sentiment; Michigan is a multi-year annualized forecast; the principal Gallup and CFO questions concern one year. The authors compare their cyclical behavior, not perfectly matched one-year probability distributions. A reproduction should retain these distinctions in metadata.

Gallup's early monthly samples exceed 700 respondents, and participants change across surveys. Its longest interruption is described as November 2009–February 2011, with resumption in March 2011. The supplied appendix data include a February 2011 entry, illustrating why the actual date series must be checked rather than inferred from prose. II was monthly in 1963, then biweekly until June 1969, then weekly. Newsletter membership changes, and new letters are observed for several months before inclusion. Only four editors classified newsletters over the period, which the authors regard as supporting consistency.

The paper contains date inconsistencies. Its text and Appendix A.1 place the Shiller series mostly from April 1999, while Table 1 labels it 1996–2011; the external raw series includes an earlier isolated observation. Michigan begins in September or November 2000 depending on the description, and Table 1 Panel B mistakenly labels its span 1996–2011. Preserve the supplied observation dates and report the resulting sample rather than manufacturing continuity from any one label.

## Qualitative balances, rescaling, and the common index

For Gallup, AAII, and II, the principal balance statistic is

$$
B_t=100\bigl(\Pr_t[\text{bullish}]-\Pr_t[\text{bearish}]\bigr),
$$

when probabilities are stored as fractions. If input shares are already percentage points, subtract them without another factor of 100. Neutral responses contribute through the denominator but receive zero signed weight. Shiller's statistic is the percentage expecting an increase, not a bullish-minus-bearish balance.

Gallup also asked for numerical expected returns over September 1998–approximately April/May 2003, providing 51 observations. Fourteen observations over 1998–2000 ask for minimum acceptable portfolio returns. The qualitative and numerical expectations series correlate 0.84 in levels and 0.65 in monthly changes. Minimum acceptable returns average 1.74 percentage points below reported expectations over their common period and correlate 0.87 with them. The authors use these patterns to argue that respondents distinguish, but relate, expected and required returns.

For selected regressions, fit a linear projection of the Gallup numerical return expectation onto each qualitative survey over overlapping dates, then apply its intercept and slope to that survey's full history. In notation,

$$
g_t^{\mathrm{num}}=a_j+b_jB_{j,t}+e_{j,t},
\qquad \widehat E_{j,t}^{*}=\widehat a_j+\widehat b_jB_{j,t}.
$$

Graham–Harvey and Michigan already report annual percentage returns and do not require this conceptual rescaling. Transforming a predictor by a nonzero affine map changes the regression coefficient and intercept but not fitted values, $R^2$, or the absolute slope $t$ statistic. It does affect whether a slope of one has the intended economic interpretation, so percentage versus decimal units must be harmonized separately.

For Gallup, the rescaled history ranges from 3.94% to 14.27%, with the trough around February 2009 and the peak January 2000. A zero bullish-minus-bearish balance corresponds to approximately 8.5% expected annual return. Table 1 reports a mean of 10.49% and standard deviation of 2.27 percentage points for the rescaled Gallup series. It reports 5.95% and 1.62 points for CFOs, 10.23% and 1.28 for AAII, and 10.18% and 2.09 for II. These are different sample periods, not a cross-sectional ranking of optimism at identical dates.

Table 1's raw Gallup row is problematic: it gives a minimum of 20 and maximum of 68, whereas the defined balance and plotted series include negative values. That row therefore cannot be used as a reliable numerical check of the balance statistic without consulting underlying data. Other obvious table-label problems include an impossible autocorrelation entry of 294 for the rescaled index. These issues do not reverse the plotted findings, but they matter for exact reproduction.

The authors check an alternative Carlson–Parkin transformation of categorical responses. It correlates 0.99 with the simple Gallup balance, 0.997 with AAII, and 0.83 with II. The lower II correlation is attributed to dates with almost no neutral responses, which make the distribution-based transformation unstable. The main results retain the simpler balances. No assumption that survey forecasts are correct on average is imposed to determine their scale.

To create an expectations index, the authors extract the first principal component of Gallup, AAII, and II over their 135 overlapping monthly observations. It explains 74% of variance. Including CFOs yields 71% in a different sample, so the two percentages do not measure an incremental loss of explanatory quality on the same observations. Missing Gallup dates are filled by carrying forward past values. For the pre-Gallup period, the common component is projected on AAII and II and fitted values provide the earlier index. Finally, the history is standardized to mean zero and variance one.

Figure 5 dates the index July 1987–December 2011; some surrounding text says 1988–1995 for the backcast period and Table 1 labels the index 1986–2011. The loadings, precise centering/standardization conventions before PCA, backcast regression coefficients, and all calendar choices are not reproduced in the supplied article or the located data appendix. Carrying forward a missing survey avoids using its next observation, but full-sample PCA estimation and backcasting are still ex post transformations. They are not automatically free of lookahead when used as trading signals.

## Cross-survey coherence and investment behavior

Table 2 uses each pair's available overlap. The article calls these “partial correlations,” but its caption describes pairwise correlations on overlapping observations, not correlations after controlling for other regressors. Gallup correlates 0.77 with CFO expectations, 0.64 with AAII, 0.60 with II, 0.39 with Shiller, and 0.61 with Michigan. The average survey correlation is approximately 0.43. CFOs and Shiller correlate 0.66; AAII and II correlate 0.55.

Not every pair is positive. Michigan and CFOs have a small negative estimate, while Michigan and Shiller have correlation $-0.55$. The Michigan–Shiller overlap has only seventeen observations, and the article attributes its negative relationship largely to the first three. The correct conclusion is broad common movement with meaningful small-sample exceptions, rather than unanimity among all investor groups.

Mutual-fund flows come from the Investment Company Institute. Monthly net dollar flows into equity-oriented funds are divided by aggregate U.S. equity capitalization from CRSP. This denominator is the equity market, not assets held in the surveyed funds. The flow history is January 1984–December 2011, 336 months. Its correlation with Gallup is 0.69, with CFOs 0.71, with AAII 0.42, with II 0.20, and with the expectations index 0.45. Michigan's estimate is 0.40 with reported $p=0.068$.

These positive relationships support behavioral relevance, but do not connect a particular respondent's forecast to that respondent's purchases. Common responses to market returns can produce correlations among surveys and aggregate flows. No instrument, randomized survey framing, or individual portfolio panel identifies a causal effect of stated beliefs on demand in this paper.

## Estimating extrapolation

The principal time-series specification is equation (2):

$$
E_t=a+bR_{t-12,t}+c\log(P_t/D_t)+d'Z_t+u_t.
$$

$R_{t-12,t}$ is the past twelve-month raw market return, and the valuation variable is the log price–dividend ratio. Controls $Z_t$ include earnings growth, unemployment, and the risk-free rate in the displayed table. The text also describes experiments with dividend growth, GDP, industrial production, consumption, and consumption growth. Many controls lose explanatory power after past returns and valuation are included.

Table 3 reports Newey–West statistics using twelve-month lags. For irregularly observed surveys, the paper follows a procedure that treats the retained observations as equally spaced. This differs from inserting calendar-month zero residuals or linearly interpolating survey values. The description leaves some ambiguity about the conversion of the twelve-month bandwidth for quarterly CFO data; reproducing that convention requires code or a clearly stated reconstruction. Survey collection itself occurs over a period before the reported date, adding timing uncertainty.

For Gallup, past returns alone have coefficient 91.227 and $t=8.811$, with $R^2=0.611$ over 135 observations. Adding log $P/D$ gives coefficients 89.155 on past returns and 25.995 on valuation, with $t=13.052$ and 4.107 respectively and $R^2=0.689$. Return inputs are decimal returns while Gallup is in balance points, so a ten-percentage-point increase in the past return corresponds to approximately 8.92 balance points holding valuation constant.

The paper's own 20% price-increase illustration reports a 20.5-point Gallup increase and approximately 1.80 percentage points of rescaled expected return. That combined numerical example is not transparently reconciled with both printed coefficients and an explicit dividend assumption. It should be recorded as a reported illustration rather than used to infer an undocumented conversion factor. Changing price generally moves both past returns and $P/D$; an implementation must specify which regressors are held fixed.

The average $R^2$ across the main specifications is about 0.33. Results are weaker for some surveys than for Gallup. Shiller's past-return-only regression has $R^2=0.002$, whereas including valuation raises it to 0.317. This is one reason to preserve separate survey results rather than present a single pooled extrapolation coefficient as universal.

To estimate memory decay, equation (3) uses nonlinear least squares:

$$
E_t=a+b\sum_{j=0}^{K}w_j(\lambda)R_{t-j}+u_t,
\qquad w_j(\lambda)=\frac{\lambda^j}{\sum_{i=0}^{K}\lambda^i}.
$$

Returns here are quarterly. For $0<\lambda<1$, older returns receive less weight, and $w_j/w_0=\lambda^j$. A larger $\lambda$ means slower decay and relatively more weight on distant returns. Table 4's caption reverses this direction by saying higher $\lambda$ puts more weight on recent data. The equation, not that sentence, should govern implementation. The truncation horizon $K$, optimizer, starting values, and parameter bounds are not fully specified in the article.

Estimated $\lambda$ values are 0.770 for Gallup, 0.457 for CFOs, 0.392 for AAII, 0.493 for II, 0.334 for Shiller, 0.918 for Michigan, and 0.542 for the index. The average is about 0.56, implying a four-quarter-old return receives about $0.56^4=0.098$ times the most recent quarter's weight. The index fit has $R^2=0.415$, Gallup 0.675, and Shiller only 0.015. Shiller's estimated decay parameter has a very low reported $t$ statistic, 0.384. The separate flow regression gives $\lambda=0.65$. These descriptive estimates should not be interpreted as a universally identified psychological discount factor.

## Comparing surveys with model-based expected returns

Four proxies are used: log dividend yield, negative surplus consumption, the consumption–wealth ratio $cay$, and a composite fitted return. Log dividend yield is constructed from CRSP value-weighted returns; surplus consumption follows Campbell–Cochrane with code from Cochrane; $cay$ is obtained from Lettau. These external inputs are identified but their historical vintages and complete construction code are not included in the local PDF.

The surplus-consumption sign matters. Higher surplus consumption corresponds to lower risk aversion in the habit model, so the comparison uses its negative when orienting the variable as a high-expected-return measure. The composite fits next-year excess returns on log dividend yield, Treasury-bill yield, the BAA-minus-AAA yield spread, and the ten-year government-minus-three-month Treasury term spread. Fitted values are the composite ER series; this is an in-sample conditional projection, not a documented real-time forecast.

Table 5's pairwise correlations use only dates on which both measures are observed, with no interpolation. Gallup's correlations are $-0.328$ with log dividend yield, $-0.481$ with negative surplus consumption, 0.025 with $cay$, and $-0.572$ with the composite. CFO correlations are $-0.443$, $-0.529$, 0.139, and $-0.443$ respectively. Thus the general sign disagreement is strong for dividend yield and habit-related variation, but not uniform for every proxy.

The $cay$ results are especially mixed: Shiller has a positive 0.366 correlation, II has $-0.185$, and several surveys are effectively uncorrelated. II also has a positive 0.125 correlation with the composite ER, unlike the other survey measures. These exceptions narrow the claim. The paper challenges the identification of observed survey beliefs with model-implied representative-agent expectations; it does not prove every expected-return model is negatively correlated with every investor's belief.

Under an idealized null with identical horizons, units, information sets, and noiseless measurement, subjective rational expectations and the true conditional expected return coincide. A regression of one on the other would have zero intercept, unit slope, and $R^2=1$. Real survey measurement error and imperfect ER proxies weaken this exact benchmark. Classical independent noise tends to attenuate correlations toward zero, which motivates the authors' emphasis on negative signs, but nonclassical measurement errors or heterogeneous investor groups complicate the rejection of broader rational models.

## Return forecasting design and results

Equation (5) estimates

$$
R^x_{t,t+h}=a+bX_t+u_{t+h},\qquad h\in\{12,36\}\text{ months}.
$$

The dependent variable is the future cumulative CRSP value-weighted market return net of the compounded risk-free return. Table 1 describes the forward variables as excess log returns, while the forecasting discussion uses cumulative-return language. Exact simple-versus-log compounding is therefore an implementation detail to verify rather than silently resolve. Samples are constrained to the 1963–2011 window and shorten with survey availability and forward-return availability. Overlapping horizons are handled with Newey–West lag length $h$.

For the twelve-month regression, the printed Gallup slope is $-1.985$, with $t=-1.370$, $R^2=0.057$, and 132 observations. Its $p$ value against a unit-slope null is 0.040. The expectations index has slope $-1.617$, $t=-1.530$, $R^2=0.039$, and 285 observations. II has slope $-1.534$, $t=-2.323$, and 579 observations. These numbers distinguish rejecting a correctly scaled forecast slope of one from establishing a slope significantly below zero; the former can occur without the latter.

The printed CFO coefficient is $-0.021$, with $t=-0.670$, and Michigan's is $-0.081$, with $t=-3.964$. Their numerical magnitudes are consistent with predictors stored in percentage points, whereas the starred qualitative series appear on a decimal-return scale. A coefficient of one is not invariant to that hundredfold unit change. The table reports unit-slope tests, but a fresh replication must reconcile raw units before relying on every reported null test. This note does not claim to have recomputed them from the original regression dataset.

At thirty-six months, Gallup's slope is $-7.485$, $t=-4.864$, $R^2=0.235$, and $N=124$; II gives $-5.319$, $t=-3.206$, $R^2=0.110$, and $N=555$; the index gives $-5.713$, $t=-2.678$, $R^2=0.094$, and $N=261$. Michigan is excluded because there are too few observations to construct the same HAC standard errors. These are horizon-specific projections, not annualized trading alphas.

Dividend yield and consumption-based measures generally forecast returns positively. At twelve months, log dividend yield's slope is 0.072 with $t=1.424$, negative surplus consumption's is 0.958 with $t=4.147$, and $cay$ has 3.095 with $t=3.031$. Bivariate regressions show partial overlap between survey information and ER proxies. At thirty-six months, Gallup remains negative when paired with dividend yield, with slope $-6.205$ and $t=-3.306$; the index/dividend-yield specification gives index slope $-3.189$ and $t=-2.048$.

The article reports that a Stambaugh bias adjustment in an Internet Appendix changes most coefficients little. That particular table is not in the located eight-page data supplement, so the claim is source-reported rather than independently checked here. HAC corrections address serial covariance, not model-selection bias, unstable predictors, limited effective long-horizon observations, or the prospective availability of revised macroeconomic data.

## Who accommodates optimism, and how to reproduce the study

The final empirical exercise regresses monthly IPO counts and equity issuance on contemporaneous surveys or fund flows. IPO counts come from the referenced issuance series; dollar IPO and follow-on offerings come from SDC over January 1972–December 2011 and are divided by CRSP aggregate market capitalization. Although Table 7 calls the latter “net issuance,” the described construction aggregates offerings and does not explicitly subtract repurchases. A replication should not silently substitute a repurchase-adjusted measure.

Gallup and IPO counts correlate about 0.60. The count regression slope is 0.514 IPOs per Gallup balance point, with $t=4.360$, $N=131$, and $R^2=0.362$. Thus ten additional balance points correspond to approximately 5.14 additional IPOs in that descriptive regression. The index slope is 6.142 with $t=2.457$. Evidence for dollar issuance is weaker and uneven; the authors themselves describe it as tentative. These contemporaneous associations do not identify firms as the complete or uniquely rational counterparty to extrapolators.

To reconstruct the work, retain raw dated survey observations first, build each balance and numerical series in its native units, and reproduce overlap counts and pairwise correlations before estimating economic relationships. Keep interpolation out of the pairwise tests; apply carry-forward only where the index construction calls for it. Fit and document the rescaling and PCA conventions, then build the market, valuation, consumption, flow, and issuance variables with explicit vintages. Reconcile Table 1's inconsistent labels and Table 6's units before comparing regression coefficients. Finally estimate the linear and nonlinear expectation equations, the separate forward-horizon regressions with their overlap corrections, and the issuance regressions.

The paper provides a useful empirical architecture but not a complete execution package. Licensed II data, market and issuance datasets, missing transformation coefficients, and unresolved timing conventions prevent exact reproduction from the PDF alone. Its strongest transferable finding is the empirical separation of popular optimism from valuation-implied expected returns, supported across several types of survey and behavior. Turning that separation into a live allocation method is additional research requiring genuinely out-of-sample tests and transaction-cost analysis.
