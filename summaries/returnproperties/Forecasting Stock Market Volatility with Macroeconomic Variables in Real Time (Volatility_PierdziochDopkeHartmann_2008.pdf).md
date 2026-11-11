# Forecasting Stock Market Volatility with Macroeconomic Variables in Real Time

**Christian Pierdzioch, Jörg Döpke, and Daniel Hartmann.** *Journal of Economics and Business* 60 (2008), 256–276. DOI: 10.1016/j.jeconbus.2007.03.001. Source: [Volatility_PierdziochDopkeHartmann_2008.pdf](../../Finance/Volatility_PierdziochDopkeHartmann_2008.pdf). This note covers the complete 21-page article, including all eight tables and its two figures. No separate appendix is included in the library PDF.

## Why this matters

An apparent macroeconomic volatility predictor may be unavailable when a position must be decided. Industrial-production and output-gap histories are revised, publication delays change, and end-of-sample filters can use future observations. A forecasting result obtained from final data therefore need not describe a feasible historical strategy.

The paper compares real-time and revised-data versions of the *same recursive modeling process*. Its innovation is not a new GARCH estimator. It is a German vintage-data experiment that reselects regressors and re-estimates coefficients through time, then evaluates forecasts using statistical loss, a portfolio-utility calculation, and a synthetic options market. The three criteria help expose differences between numerical forecasting accuracy and economic value.

Its broad finding is that using preliminary macroeconomic data does not systematically degrade performance in this sample. That is a limited empirical conclusion, not permission to ignore release calendars. The paper's own design depends on preserving those calendars. It also forecasts an implied-volatility index in its main experiment, so its results do not automatically establish predictability of future physical return variance. Some economic-evaluation details and printed formulas are insufficiently specified or inconsistent; these limits must be retained in a reconstruction.

## Prediction target, information set, and timing

The principal volatility series is VDAX-NEW, the square root of option-implied DAX30 variances with a constant 30-day maturity. Its construction uses at- and out-of-the-money options and incorporates information across strikes. Daily data are available for January 1992–April 2005; the authors use end-of-month values to avoid overlapping daily observations. Figure 1 covers January 1995–March 2005 and shows the major high-volatility episodes within that period.

Let $v_t$ denote the end-of-month volatility index. The regression target is the next change in log volatility,

$$
y_{t+1}=\log v_{t+1}-\log v_t.
$$

At an origin $t$, each candidate model uses a subset of regressors observable then, always including a constant. With $x_{t,i}$ the regressors of candidate $i$,

$$
y_{t+1}=x_{t,i}'\beta_i+\varepsilon_{t+1,i}.
$$

All fitted observations used to estimate $\beta_i$ must have outcomes already observed at the origin. The model selected at $t$ supplies $\widehat y_{t+1|t}$. A natural level reconstruction is $\widehat v_{t+1|t}=v_t\exp(\widehat y_{t+1|t})$, but the paper does not detail its retransformation convention or lognormal bias adjustment. Since exponentiating a fitted log mean is not generally the conditional mean of the level, that choice can affect level RMSE and downstream variance forecasts.

The article motivates its regression with $dv=\kappa(\bar v-v)v\,dt+\alpha v\,dW$. This is a multiplicative mean-reverting diffusion, described there as a geometric Ornstein–Uhlenbeck process. It writes $dv/v\approx d\log v$ to motivate a predictor in the volatility level. Exact Itô differentiation would instead give

$$
d\log v=\left[\kappa(\bar v-v)-\frac12\alpha^2\right]dt+\alpha\,dW.
$$

With constant $\alpha$, the omitted adjustment changes the intercept, not the suggested dependence on $v$. The regression should therefore be understood as a discrete empirical specification inspired by a diffusion, not an exact discretization of the displayed process.

## Vintage data and predictor construction

The monthly macroeconomic vintages come from the Deutsche Bundesbank's *Saisonbereinigte Wirtschaftszahlen*. The main indicators are month-to-month industrial-production growth excluding construction, month-to-month orders-inflow growth, and annualized consumer-price inflation. An output gap is constructed by recursively applying the one-sided Christiano–Fitzgerald band-pass filter to each vintage of industrial production. Consequently, both revisions to history and endpoint uncertainty can change the gap estimated at a later date.

Data releases referring to Germany as a whole begin in January 1994. The forecasting sample January 1995–March 2005 comprises 123 calendar-month vintages. Historical observations are added to permit initial estimation. The source says these histories go back to November 1991, but also calls January 1991–December 1994 the training period. Alongside the stated January 1992 start of VDAX-NEW, these descriptions do not fully identify the effective first regression observation. An exact replication requires the actual aligned data matrices, rather than assuming all listed series start in January 1991.

Release delays are explicitly respected. Industrial production normally arrives with a two-month lag, but no new production releases were issued from February through June 1995 during a conceptual revision. The statistical office later issued two observations per month from June through August to restore the normal delay. The real-time investor always uses the latest publicly released observation; if no new observation appears, the latest available value from the latest available vintage fills the gap. This is a carry-forward rule for available information, not interpolation using a future release.

The additional seven predictors are: the first difference of the three-month Treasury-bill rate (Datastream BDI60C...); the long government-bond yield (BDI61...) minus that bill rate; a January dummy; the DAX30 index (DAXINDZ) minus its backward-looking four-month moving average; the analogous eight-month moving-average difference; the IFO business-climate indicator (WGIFOMXLE); and the current VDAX-NEW level. The moving averages correspond approximately to 100 and 200 trading days. The source does not provide more detailed scaling or normalization for those price-minus-average variables.

Four predictor universes are evaluated. Three combine one activity measure—production, orders, or the output gap—with inflation and the seven other predictors, giving nine candidates. The fourth combines all four macroeconomic series with the seven others, giving eleven. Every subset includes an intercept. This yields $2^9=512$ or $2^{11}=2048$ distinct variable subsets at an origin, not a million subsets from eleven variables alone. The paper's statement that more than one million models are estimated should be read in the context of repeated searches over dates and experimental configurations; it does not supply a complete run-count calculation.

The revised-data experiment uses later-revised histories in place of the real-time macroeconomic information. The exact final-vintage date, band-pass cutoffs, initialization of the filter, original release calendar, and vintage panels are not supplied in this PDF. Deterministic linear and quadratic trends are mentioned as alternative gap filters, with qualitatively similar results, but their results are not tabulated.

## Recursive estimation and model selection

At every month, estimate all candidate subset regressions by OLS using the expanding historical sample, compute the selection score, retain the best model, issue a one-step forecast, and repeat after the next observation arrives. The selection criteria are adjusted $R^2$ (ACD), Akaike information criterion (AIC), and direction of change (DCC). ACD and DCC are maximized; AIC is minimized.

For implementation, with $n$ observations and $k$ regression coefficients including the intercept, conventional forms are $1-(RSS/(n-k))/(TSS/(n-1))$ for adjusted $R^2$ and $n\log(RSS/n)+2k$ for Gaussian AIC up to constants common to models. DCC is the proportion of in-sample changes whose fitted sign matches the observed sign. The source describes DCC once as predicting “changes of returns,” although its dependent variable here is the change in log volatility. Ties and zero-change classifications are not specified. These score formulas clarify a standard implementation but do not replace missing source-code conventions.

The exercise measures performance of a repeated model-selection procedure, rather than the performance of a single specification selected with hindsight. Selection must therefore be rerun separately for each origin and each vintage treatment. Fixing the full-sample winner and backfilling its fitted forecasts would change the experiment. So would using revised industrial production to construct a nominally real-time output gap.

AIC tends to select parsimonious specifications. Table 2 shows that VDAX-NEW itself enters almost always, while the output gap is the activity measure most frequently retained. In the all-macro universe under AIC, the gap is selected 78.69% of the time with revised data and 77.05% with real-time data. VDAX inclusion is 98.36% and 97.54%; industrial-production inclusion is 14.75% and 9.02%; orders inclusion is 4.10% and 2.46%. Thus comparable overall performance does not require identical variable selection, and the forecasting system is dominated by persistent volatility information rather than by every macroeconomic release.

## Statistical evaluation and results

The paper reports level-volatility RMSE and the ratio

$$
U=\frac{RMSE_{\mathrm{real\ time}}}{RMSE_{\mathrm{revised}}}.
$$

Values below one favor real-time inputs. Given the index target and the size of the reported errors, the RMSE values should be treated in the reported volatility-index units, not as monthly decimal return variances. The publication does not fully spell out the transformation between its log-change regression and the evaluated level forecast.

| Predictor universe and selection | Revised RMSE | Real-time RMSE | Ratio from the printed RMSE values |
|---|---:|---:|---:|
| Production, ACD | 5.8922 | 5.9163 | 1.0041 |
| Production, AIC | 5.7650 | 5.7772 | 1.0021 |
| Orders, AIC | 5.7650 | 5.7569 | 0.9986 |
| Gap, AIC | 5.8258 | 5.7890 | 0.9937 |
| Gap, DCC | 6.0835 | 5.6657 | 0.9313 |
| All macro, ACD | 5.9508 | 6.0135 | 1.0105 |
| All macro, AIC | 5.8134 | 5.8257 | 1.0021 |
| All macro, DCC | 5.9952 | 5.6987 | 0.9505 |

Table 3 prints 1.1054 for the all-macro ACD ratio, which is inconsistent with $6.0135/5.9508\approx1.0105$. The corrected arithmetic is given above, with the source values preserved. Several tiny ratio differences elsewhere reflect rounding. The economically larger reductions under DCC are about 6.9% for gap-only activity information and 5.0% for all macro series.

For unconditional predictive accuracy, the authors regress the squared-error loss differential on a constant and report its robust $t$ statistic as a Diebold–Mariano test. The conditional-predictive-ability exercise uses a lagged-loss test function in the Giacomini–White framework. Robust standard-error bandwidths and the exact test-function vector are not fully given. The expanding-window implementation is supplemented by an unreported rolling-window check, important because the asymptotic justification of forecast-comparison procedures can depend on the estimation scheme.

Only two of twelve Diebold–Mariano comparisons are weakly significant at 10%: production/AIC has a statistic of 1.73 and orders/AIC 1.82. Neither is significant at 5%. Only one Giacomini–White result is significant at 5%: gap/DCC, with a statistic of 5.65. The table mostly reports positive statistics, so one should use the paired RMSEs rather than infer the direction of every effect from those signs. There is no multiplicity adjustment reported across the twelve comparisons. Failure to reject equality also does not establish a tight equivalence bound.

## How different are first-release and revised data?

Table 1 shows that the similar forecast outcomes are not simply due to negligible revisions. The noise-to-signal ratio is the standard deviation of revisions divided by the standard deviation of final-release data. Final-versus-first-release ratios are 1.01 for production, 0.88 for orders, 0.81 for inflation, and 0.90 for the output gap. Thus revision variability is often comparable to the variability of the final series.

For production, the final revision has mean 0.14, standard deviation 1.15, minimum −3.61, and maximum 3.37 in the source's growth-rate units. Orders have mean −0.01, standard deviation 1.85, and range −6.87 to 8.95. Gap revisions have mean 0.13, standard deviation 1.04, and range −3.26 to 3.01. F-tests reject equal first/final-release variances for production and the gap at 1%, and orders at 5%. Means are described as not significantly different from zero. Large revisions without a systematic mean bias can still matter for a particular investor; the result concerns their effect on this forecasting procedure's average outcomes.

## Portfolio-utility evaluation

The utility exercise considers one-period mean–variance wealth utility,

$$
U_{t+1}=E_tW_{t+1}-\frac{\gamma}{2}\operatorname{Var}_t(W_{t+1}),
\qquad
W_{t+1}=W_t[(1-f_t)R_{F,t+1}+f_tR_{t+1}].
$$

The source defines $\delta=\gamma W_t/(1-\gamma W_t)$ and obtains

$$
f_t=\frac{1+\delta}{\delta}\frac{\mu_{t+1}-R_{F,t+1}}{\widehat h_{t+1}},
$$

where $\mu_{t+1}$ is an assumed-known conditional expected gross stock return and $\widehat h$ is forecast variance. There are no stated leverage or short-sale bounds. Let $d_t=((1+\delta)/\delta)(\mu_{t+1}-R_{F,t+1})^2$. Substituting the selected weight into expected utility gives

$$
E_tU_{t+1}=W_t\left[R_{F,t+1}+d_t\left(\frac1{\widehat h_{t+1}}-\frac{h_{t+1}}{2\widehat h_{t+1}^2}\right)\right].
$$

This makes underprediction costly: it produces excessive risky exposure. The evaluation replaces latent $h_{t+1}$ by the realized squared log price change and averages over forecasts while holding $W_t$ fixed. A raw squared return estimates a conditional second moment, not a centered variance exactly when the conditional mean is nonzero. The distinction is usually small at short horizons but should not be described as an identity without that qualification.

The paper reports $\delta=1$ and $10$. It compares models using an annualized wealth-sacrifice ratio,

$$
WSR_m=120000\left(1-\frac{\overline U_m}{\overline U_{\mathrm{best}}}\right)
$$

in annual basis points. This is its fee-equivalent transformation of average one-period utilities, not a compound portfolio return or an observed management fee. The numerical conditional-mean inputs, wealth normalization, conversion from VDAX units to monthly variance, and any positivity safeguards for variance are not fully disclosed. These gaps prevent an exact independent reproduction of Tables 5–7 from the article alone.

The central utility result is conditional on the selector. With AIC, real-time inputs beat their revised counterparts in all four universes. At $\delta=1$, production average utilities are 114.61 versus 113.64; orders 114.43 versus 113.65; gap 116.05 versus 113.65; and all macro 117.03 versus 113.33. With ACD the ordering reverses in all four. A useful qualification to the prose claim favoring AIC is that real-time gap/DCC reaches 117.08, above gap/AIC's 116.05. Table 6 correctly makes DCC the within-gap real-time winner. The selection criterion and activity measure jointly determine economic performance.

Table 7's revised-to-real-time AIC wealth-sacrifice ratios at $\delta=1$ are 1015.62, 817.97, 2481.70, and 3793.90 annual basis points. These are large model-dependent fee equivalents. Without the missing utility calibration, they should not be translated into deployable investment gains. They mainly show that statistical and utility rankings need not coincide.

## Synthetic option experiment

Two traders value one-month DAX30 straddles on an underlying normalized to one euro. One uses real-time forecasts and the other revised-data forecasts. Each straddle consists of a European call and put with strike at the forward price. The trader with the higher volatility forecast buys; the other sells. Trade price is the average of their valuations. If forecasts are identical, the convention makes both traders short a straddle, so aggregate reported profits need not sum to zero.

For an at-forward option with normalized spot one, a consistent Black–Scholes expression is $C=P=2\Phi(\frac12\sqrt{\widehat h M})-1$ and straddle price $4\Phi(\frac12\sqrt{\widehat h M})-2$, provided $\widehat h$ and maturity $M$ use matching time units and the forward/discount conventions are handled consistently. The article uses this expression in Eq. (9). If $\widehat h$ is already a monthly variance, $M$ must be in months; if annualized, it must be in years. The precise convention is not provided.

The source's closing sentence in Section 2.2.3 calls $\exp(R_{F,t+1}-1)$ the realized stock-market return used for settlement, although $R_F$ is the riskless return elsewhere. Literal use of that expression would settle the underlying at its forward and would not implement the intended realized-DAX experiment. A reproducible economic implementation must settle using actual DAX terminal value and payoff $|S_{t+1}-K_t|$, subtracting the appropriately financed purchase price. That is the logical correction, not proof of what the authors' unpublished code did.

Table 8 reports cumulative profit, its stated standard deviation, and their ratio. These are synthetic valuation contests without bid–ask spreads, margin constraints, transaction costs, or observed option quotes. They should not be labeled a live options backtest or conventional annualized Sharpe ratios. For production/AIC, revised and real-time profits are 0.45 and 0.30; for orders/AIC, 0.45 and 0.44. For gap/DCC the contrast is much larger: 0.92 versus −0.58. All-macro/DCC gives 0.87 versus −0.42. Conversely production/ACD gives 0.13 versus 0.25, favoring real-time inputs. The outcomes do not support a universal ordering, even though some configurations differ substantially.

## Replication boundaries and conclusions

The reported robustness checks replace VDAX-NEW with GARCH(1,1) volatility, add one lag beyond the actual macroeconomic release delay, use quarterly GDP growth instead of monthly production growth, and use alternative gap detrending. The article says conclusions are qualitatively unchanged but does not publish those tables or all their estimation settings. They are reported robustness claims, not independently inspectable numerical replications in the supplied PDF.

The experiment is strongest as evidence about the relative effect of data vintage within one recursive procedure. It is weaker as proof of absolute macroeconomic forecasting value: the headline tables principally compare real-time against revised predictors, not their economic gains against a fully documented simple no-macro benchmark. The implied-volatility target, short 1995–2005 evaluation period, many subset searches, incomplete economic calibration, and source presentation errors narrow what can be claimed.

An implementation based on this paper should preserve vintage-specific histories, release delays, recursive gap estimation, repeated model selection, and separate forecast-evaluation objectives. It should also expose retransformation, variance-unit conversion, and settlement conventions as explicit inputs. Those details are where an apparently faithful reproduction can otherwise become an infeasible hindsight exercise. The source supports the proposition that large macro-data revisions need not materially harm average volatility forecasting in this setting; it does not establish that revisions are harmless in all markets or that the illustrated utility and option profits survive trading costs.
