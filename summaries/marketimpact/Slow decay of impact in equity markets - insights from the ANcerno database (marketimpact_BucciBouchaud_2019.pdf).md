# Slow decay of impact in equity markets: insights from the ANcerno database

**Authors:** Frédéric Bucci, Michael Benzaquen, Fabrizio Lillo, and Jean-Philippe Bouchaud. **Source version:** January 23, 2019; arXiv:1901.05332v2, with arXiv revision stamp January 22, 2019. **Source file:** `Finance/marketimpact_BucciBouchaud_2019.pdf`, 12 PDF pages. Page references below use the PDF's printed page numbers, which coincide with PDF pages. **Type:** empirical market-microstructure research paper.

## Question and contribution

The paper asks how far, and how slowly, the price displacement associated with an institutional trade reverses after execution finishes. Its central contribution is to separate an easily observed intraday regularity from a claim about permanence. Prices at the end of the execution day are, on average, displaced by approximately two-thirds of the peak displacement reached at completion. That observation does not establish a permanent two-thirds plateau. Extending the measurement horizon and correcting for correlated subsequent institutional orders reveals continued decay.

This distinction addresses a specific prediction of the fair-pricing theory of Farmer, Gerig, Lillo, and Waelbroeck, abbreviated FGLW in the paper. With an appropriate power-law distribution of metaorder sizes, that theory predicts a final price equal to the average execution price, producing permanent impact equal to two-thirds of peak impact. Earlier studies that stopped observing prices shortly after completion appeared compatible with that prediction. Bucci and coauthors show that a restricted observation window can create that appearance even when relaxation is continuing.

The empirical innovation has three connected parts. First, the authors examine intraday relaxation using the amount of market volume traded after completion relative to volume traded during execution. Second, they connect that curve to next-day relaxation. Third, they estimate a daily distributed-lag model to remove the contribution of correlated later trading, producing an approximation to the response to an isolated order-flow impulse. These steps matter because an institutional decision often produces trades on several successive days. An average return following today's buy is then partly a response to tomorrow's correlated buy, rather than evidence that today's impact has remained intact.

The most defensible substantive conclusion is continued relaxation below two-thirds of the execution peak. The existence and size of a genuinely permanent component are less securely identified. A fitted model favors a positive long-run level, but alternative specifications, missing information about traders' signals, and large long-horizon uncertainty prevent a decisive distinction between permanent mechanical impact and information conveyed by trades. The authors themselves emphasize this limitation (pp. 9–11).

## Data, observation unit, and selection

The source is a commercial ANcerno transaction-cost-analysis database covering January 2007 through June 2010, a total of 880 trading days. The selected universe consists of Russell 3000 stocks. After applying a cleaning procedure inherited from Zarinelli and coauthors and used in related work, the sample contains approximately eight million metaorders, representing around 5% of total market volume. Before those filters, the database would represent roughly 10% of market volume. Trading is described as relatively evenly distributed across time and market capitalizations (p. 3).

A metaorder is a series of executions jointly reported by one investor, through one broker, on one stock, in one direction, within one day. Each record has a stock identifier, share quantity $Q$, start time $t_s$, end time $t_e$, and sign $\epsilon\in\{-1,+1\}$. This is an operational definition, not direct observation of a complete investment decision. A portfolio manager may spread one decision across brokers or days. Consequently, separate observed metaorders can remain strongly related, which is precisely the problem addressed by the multiday analysis.

The data do not reveal the execution algorithm, trading motive, or underlying predictive signal. That makes it impossible to classify all trades as informed or uninformed and prevents direct subtraction of the manager's expected alpha. The sample is heterogeneous across anonymous institutions, which improves breadth relative to studies of one manager but makes interpretation of the final residual price change harder. Database coverage also remains partial: the regressions use the observed slice of institutional flow, rather than every market participant's demand.

The paper references, rather than reproduces, the detailed cleaning protocol and the full descriptive distributions of durations, participation rates, and numbers of fills. A replication therefore needs both the licensed raw data and the referenced cleaning implementation. The authors cannot redistribute the purchased data, including aggregates (p. 11). The paper's equations and fitting choices are reproducible in principle; the exact sample cannot be reconstructed from this PDF alone.

## Definitions and normalization

Let $V(t)$ be cumulative market volume in a stock from the beginning of the trading day through time $t$. Let $V_d=V(t_c)$ denote volume at the day's close. The participation rate, volume-time duration, and daily volume fraction are

$$
\eta=\frac{Q}{V(t_e)-V(t_s)},\qquad
D=\frac{V(t_e)-V(t_s)}{V_d},\qquad
\phi=\frac{Q}{V_d}=\eta D.
$$

The denominator in participation rate is volume traded by the entire market during the execution window, while the daily fraction uses the whole day's volume. These variables must not be interchanged. Two orders of equal daily fraction can differ greatly in urgency: one may consume a high fraction of a short interval, another a low fraction of a long interval. The relaxation measurement later controls for elapsed market activity relative to execution activity.

Prices are expressed as normalized log prices,

$$
s(t)=\frac{\log S(t)}{\sigma_d},\qquad
\sigma_d=\frac{S_{\mathrm{High}}-S_{\mathrm{Low}}}{S_{\mathrm{Open}}}.
$$

The daily high-low-open estimator is explicitly described as noisy. It is used for cross-stock scale normalization, not claimed to be an exact latent-volatility estimate. Because the same normalization is used across the relevant comparisons, the impact curves are in units of estimated daily volatility. Using another volatility estimator or using information available only before execution would be a different empirical design and should be reported as such.

Start-to-end impact is the conditional signed mean price change,

$$
I_{SE}(\phi)=\mathbb E\left[\epsilon\{s(t_e)-s(t_s)\}\mid\phi\right].
$$

The analogous start-to-close impact $I_{SC}$ substitutes the same day's closing price for $s(t_e)$. Start-to-next-day-close impact $I_{SC2}$ uses the next day's close. Multiplication by trade sign puts buys and sells on a common axis: movement in the direction of the order is positive. These are conditional average price responses, rather than execution-cost measurements based on every fill price.

For estimation, observations are sorted into equally populated bins of daily fraction and conditional averages are computed within bins. Error bars in the initial impact analysis are standard errors (p. 4). The ratio of conditional means is the relevant object when comparing curves. It is not the mean of individual-order ratios, which would behave poorly when individual price changes are close to zero or have the opposite sign.

## Intraday evidence and the apparent two-thirds plateau

The start-to-end curve is approximately square root in daily fraction for the intermediate range $10^{-3}\lesssim\phi\lesssim10^{-1}$. At smaller fractions it is closer to linear. Thus the data do not justify imposing a square-root curve on every order size. In the reported intermediate range, the usual descriptive relation is $I\propto\sqrt{\phi}$, with volatility normalization already incorporated in the plotted measure (pp. 4–5).

The start-to-close curve lies below the start-to-end curve, demonstrating average reversal after completion. Across daily-fraction bins, the mean ratio is approximately $0.66\pm0.04$. Taken alone, this is compatible with the FGLW two-thirds prediction. The more informative feature is that the ratio rises with order size. Larger orders tend to finish later because they take longer to execute, leaving less time for reversal before the close. Small orders have a longer post-execution window, so their close-of-day impact has more opportunity to decay.

To test this explanation, the authors define execution-window and post-execution market volumes,

$$
V_{SE}=V(t_e)-V(t_s),\qquad
V_{EC}=V(t_c)-V(t_e),\qquad
z=\frac{V_{EC}}{V_{SE}}.
$$

They plot relative remaining impact against $z$. The ratio continues to decline as relative post-trade volume increases. This change of horizontal axis is central: clock time measured from completion is not enough when orders themselves have different durations and when trading intensity varies across the day.

The curve is well described by a propagator-model scaling function,

$$
I_{\mathrm{prop}}(z)=(1+z)^{1-\beta}-z^{1-\beta},\qquad\beta=0.22.
$$

This function starts at one and decays. At large $z$, a first-order expansion gives approximately $(1-\beta)z^{-\beta}$, so a slowly declining curve can appear nearly flat over a short interval. The exponent $\beta$ is the decay exponent of the underlying propagator $G(t)\sim t^{-\beta}$. It is not the square-root exponent of impact as a function of trade quantity.

When the plot is restricted to $z\in[0,2]$, the declining trajectory visually resembles relaxation toward two-thirds. Expanding the axis reveals continuing decay to lower levels. The paper therefore does more than offer a different point estimate: it demonstrates how the observation window and scaling choice can produce a misleading structural interpretation. An empirical plateau requires evidence that the curve has stabilized over a relevant range, not merely that it crosses a theoretically attractive value.

The study also says similar conclusions obtain with elapsed calendar-time duration scaled by execution duration, although those results are not plotted. The displayed volume-time analysis is the stronger documented basis for the claim. The authors interpret the small overnight contribution to decay as evidence that relaxation follows trading activity more closely than the mere passage of calendar time (pp. 3 and 6).

## Connecting the next day to the same-day trajectory

For the next-day analysis, the post-execution volume window is extended through the next day's close. The paper writes $V_{EC2}=V_{EC}+V_d$ in its shorthand, adding a day's market volume and excluding the overnight from active trading time. A replication must align that additional volume with the intended next trading day and apply a consistent convention across stocks.

The raw next-day impact cannot simply be appended to the intraday curve because next-day institutional order flow is positively correlated with today's flow. The authors use an adjustment factor

$$
\zeta=\frac{1}{1+C(1)}\approx0.80,
$$

where $C(1)$ is the one-day autocorrelation of signed square-root volume imbalance, introduced more formally in the daily analysis. After multiplication by $\zeta$, the next-day relative-impact observations lie near the continuation of the intraday propagator curve with the same exponent $\beta=0.22$ (Figure 2, p. 6).

A complementary conditional regression relates next-day-close impact to same-day-close impact. The reported line is $I_{SC2}=0.83I_{SC}$. That suggests the next day's remaining response is around four-fifths of the same-day-close response. This regression and the $0.80$ correlation adjustment answer related but different questions: the first describes the relation between observed impact measures; the second adjusts the plotted continuation for predictable later flow. They should not be treated as independent estimates of a universal mechanical decay constant.

Because next-day impact is approximately proportional to same-day-close impact, the paper argues that impact measured at the next close can retain the same approximate square-root dependence on trade size. Size concavity and temporal permanence are separate properties. Observing a concave curve at a later endpoint does not show that its level will stop decreasing after that endpoint.

## Multiday deconvolution model

At longer horizons, two problems grow. Ordinary market fluctuations add noise roughly proportional to $\sigma_d\sqrt{\tau}$ at lag $\tau$ days. Meanwhile, persistent trading in the original direction adds new impact. Without correcting for that persistence, the average price response can rise even while the effect of any isolated trade is decaying.

The daily analysis first aggregates observed metaorders by stock and trading day. For a stock with $N$ observed metaorders on day $\tau$,

$$
\Phi(\tau)=\sum_{i=1}^{N}\epsilon_i\phi_i.
$$

Define a signed square-root transform $x^{\bullet1/2}=\operatorname{sign}(x)\sqrt{|x|}$. The aggregate impact specification is $I=Y\sigma_d\Phi^{\bullet1/2}$, where $Y$ is a scale constant. Crucially, the transform is applied after netting signed daily volume. Summing square roots of individual orders would encode a different co-impact model and would not reproduce this study.

The transformed flow has multiday persistence. The fitted autocorrelation is

$$
g(\tau)=a\tau^{-\gamma}e^{-b\tau},\qquad
a=0.24\pm0.04,\quad b=0.038\pm0.002,\quad\gamma=0.56.
$$

The power-law exponent is fixed using the propagator restriction $\gamma=1-2\beta$ with $\beta=0.22$. The exponential cutoff corresponds to a time scale of about $1/b\simeq26$ trading days. The exponent is therefore partly a theory-based constraint, rather than an unrestricted estimate independent of the intraday model (Figure 3, p. 7).

Let $r(\tau)$ be the stock's close-to-close daily return and $r_M(\tau)$ the Russell 3000 return. The authors estimate stock market beta using a window from $\tau-20$ to $\tau+20$. They also remove a market-related component from the flow signal:

$$
\widetilde\Phi^{\bullet1/2}(\tau)=\Phi^{\bullet1/2}(\tau)-\beta_{\mathrm{CAPM}}(\tau)\left\langle\Phi^{\bullet1/2}(\tau)\right\rangle_{\mathrm{stocks}}.
$$

The centered flow enters the pooled least-squares regression

$$
r(\tau)=\beta_{\mathrm{CAPM}}(\tau)r_M(\tau)+\sum_{\ell=0}^{H}g_\ell\sigma_d\widetilde\Phi^{\bullet1/2}(\tau-\ell)+\xi(\tau),\qquad H=50.
$$

Here $g_\ell$ denotes the regression's daily return coefficient; this note uses a distinct lower-case symbol to avoid confusing it with the cumulative impact kernel. The original paper uses closely related typographic versions of $G$. The inferred level response is

$$
\mathcal G(\tau)=\sum_{\ell=0}^{\tau}g_\ell.
$$

This summation is essential. The regression predicts daily return increments; permanent displacement is the cumulative response to one initial flow shock. Negative lag coefficients can produce a decaying cumulative level even when contemporaneous impact is positive. Reading the raw coefficients as the level of remaining impact would invert the economic interpretation.

The model pools stocks and uses 50 days of lags. The centered beta window contains future returns relative to the date being analyzed, so this is an ex post attribution exercise, not a deployable real-time forecasting rule. That is appropriate for the paper's measurement purpose, but it must be changed and revalidated before using the model in a live trading decision.

Uncertainty is assessed using 200 bootstrap samples drawn using all 1,500 stocks, with the regression rerun for each sample. The figures display bootstrap uncertainty and accumulated regression errors. The PDF does not fully specify every resampling and covariance convention, so faithful software reproduction would need additional implementation detail. Cross-stock dependence, serial dependence, and the conditioning of the many correlated flow regressors deserve attention when interpreting the resulting intervals.

## Long-horizon fit and its uncertainty

The normalized cumulative response is fitted with an explicitly ad hoc modification of the propagator curve,

$$
I_m(\tau)=I_\infty+(1-I_\infty)I_{\mathrm{prop}}(\tau)e^{-b\tau}.
$$

Fixing $b=0.038$ from flow autocorrelation and retaining $\beta=0.22$ yields an asymptotic normalized level near $I_\infty=0.42$. Figure 3 reports a fit error of about $0.01$, but this is conditional fitting uncertainty and is much smaller than the broader uncertainty visible in the estimated response. Letting $b$ vary produces $b=0.03\pm0.01$ and $I_\infty=0.39\pm0.05$. These two variants favor a positive residual level relative to the same-day-close response (pp. 8–9).

A more revealing sensitivity check removes the exponential cutoff by setting $b=0$ and estimates the power-law exponent instead. The result is $\beta=0.15\pm0.04$ and $I_\infty=0.0\pm0.19$. Thus the same noisy long-horizon data can be compatible with decay toward zero under another parametric form. A fitted nonzero plateau is not established independently of the shape restriction.

The normalization also requires care. In the daily model, $\mathcal G(0)$ corresponds to first-day impact, not execution-completion peak impact. A long-run value near one-half of the first-day-close level translates to roughly one-third of peak impact when combined with the earlier two-thirds ratio. The source's page 9 contains an arithmetic typo, writing $2/3\times1/2\approx1/2$; the product is $1/3$, consistent with the introduction. Using the one-parameter estimate literally would give about $0.66\times0.42\approx0.28$ of peak impact. These conversions are approximate because the pooled daily regression and intraday order-level estimators are not identical measurement objects.

Market-capitalization splits yield fitted residual levels around $0.44$ for large caps, $0.61$ for mid caps, and $0.35$ for small caps. Their flow-autocorrelation shapes are similar, and the plateau estimates fall within the broad uncertainty band of the pooled curve (Figure 4, p. 9). The evidence does not justify a precise monotonic capitalization ranking of permanent impact.

Adding lagged market-adjusted returns as rough proxies for mean-reversion or momentum information increases the fitted plateau to about $0.54$ when $b$ remains fixed. The authors expected information controls to lower the residual level, so this opposite movement illustrates noise and imperfect identification. These return lags cannot replace knowledge of the manager's true signal.

## Raw response versus isolated impact

The paper also computes the cumulative covariance-like response between subsequent market-adjusted returns and current centered signed square-root flow. Unlike the distributed-lag inversion, that response does not remove correlated future trades. Its plotted normalized value increases over time (Figure 3 inset; discussion on p. 10).

This result is economically important because the same dataset can seem to show either growing impact or decaying impact depending on the estimand. The raw response answers what typically happens after the observed flow event, including the continuation of institutional trading. The deconvolved kernel asks what the fitted linear model attributes to an isolated flow impulse, holding the other observed flow shocks separate. Neither is automatically a causal effect: the second still relies on the adequacy of the regressors and the noise assumptions. But confusing the first with the second systematically overstates persistence when flow signs are autocorrelated.

A practical implementation should retain both diagnostics. If the raw response rises while the cumulative regression kernel falls, that is expected when continuation flow is strong. If both are presented under the single label “permanent impact,” readers cannot distinguish execution persistence, alpha, and market reaction. The paper's methodological contribution is to make that separation explicit even though the final decomposition remains incomplete.

## Economic interpretation and trade-size argument

The concluding model illustrates why a positive residual response need not be a universal mechanical property. Suppose peak impact is $I(Q)=Y\sigma_d\sqrt{Q/V_d}$ and is entirely transient for an uninformed order. Integrating the square-root trajectory gives average impact cost per share equal to two-thirds of peak impact. An investor expecting a price improvement $\Delta$ chooses size by maximizing

$$
\Delta Q-\frac23 QI(Q).
$$

Since total impact cost scales as $Q^{3/2}$, its marginal derivative is $I(Q)$. The first-order condition is $I(Q^*)=\Delta$. In this stylized setting, the informed investor trades until the induced price reaches the correctly predicted value. A truly informed trade need not subsequently reverse; an uninformed trade should reverse if its effect is fully transient. The argument depends on the square-root cost specification, a known price forecast, and no additional risk or execution constraints. It is a conceptual explanation, not an estimated optimal-trading policy for the ANcerno investors.

For a mixture of investors, the apparent asymptotic response can be written

$$
I_\infty(Q)=f(Q)I(Q)+[1-f(Q)]I_R(Q),
$$

where $f(Q)$ is the fraction of truly informed metaorders of size $Q$ and $I_R(Q)$ is permanent reactional impact. This decomposition shows why a square-root-shaped residual does not settle whether uninformed mechanical permanent impact is linear in quantity. The observed curve mixes information with market reaction, and the mixture weight may itself depend on size.

The paper does not establish that $I_R(Q)$ is zero, linear, or square root. It explains why resolving that question would require a large sample of reliably informationless trades and accurate long-horizon response measurements. Neither requirement is satisfied here. Consequently, the empirical rejection of a universal two-thirds plateau should not be turned into a claim that every trade has a known one-third permanent component.

## Reproduction priorities and takeaways

A reproduction should preserve the order of operations: identify investor-broker-stock-direction-day metaorders; apply the documented source filters; join intraday midprices, market volumes, and daily price ranges; compute sign-adjusted normalized impact; compare identical order sets at execution end and at the close; then scale post-completion time by execution-window market volume. It should document bin boundaries and observation counts, because equal-count bins and equal-width bins answer differently weighted questions.

For the daily stage, net signed volume before the square-root transformation, compute the cross-sectional flow adjustment, estimate the specified beta windows, and pool the distributed-lag regression with 50 lags. Sum return coefficients to obtain a price-level kernel. Reproduce both bootstrap and regression-based uncertainty, and evaluate the alternative plateau fits rather than reporting only the preferred curve. The original licensed sample, cleaning details delegated to earlier papers, and unspecified implementation conventions are the principal barriers to exact replication.

For execution research, the paper recommends treating permanence as a horizon-dependent hypothesis. Same-day cost attribution, next-day opportunity-cost analysis, and multiweek investment attribution require different controls. The approximate two-thirds ratio is useful as a sample-level description at the end of the first day, but using it as a fixed terminal boundary condition can prematurely stop modeled relaxation. The strongest result is a slow, continuing decay whose estimation requires explicit correction for persistent order flow; the remaining permanent component is substantially less certain than a single fitted plateau suggests.

## What the fitted kernel does and does not identify

The distributed-lag approach is best understood as an attribution model conditional on a particular observed flow proxy. Its useful comparison is not between two fully specified structural economies; it is between a response contaminated by predictable continuation trades and a response after those trades are separately represented in a regression. This makes the correction necessary without making it sufficient for causal identification. An omitted common signal can cause both today's flow and future returns. An omitted investor can also trade alongside the observed institution. Either mechanism can leave a positive cumulative response after observed-flow persistence has been removed.

The nonlinear transformation introduces a further restriction. The square root of net daily imbalance compresses large imbalances and assumes that observed buys and sells offset before impact is determined. This is a reasonable empirical specification supported by the authors' related co-impact work, but it discards the precise sequence of buying and selling within the day. A morning buy followed by an afternoon sell can have little net daily flow despite a meaningful intraday price path. The daily kernel is therefore an aggregate object and should not be inserted unchanged into a child-order execution simulator.

Similarly, pooling produces an average relation across institutions, stocks, and a sample that includes the financial crisis. The size of the dataset greatly reduces some sampling noise, but it does not by itself establish parameter stability outside 2007–2010. The capitalization subsamples provide one documented robustness check; they do not cover execution-algorithm differences, motive differences, or later changes in market structure. A modern calibration would need to reassess the input transformation, decay shape, and horizon while preserving the paper's main diagnostic: compare the uncorrected response with an estimated response that accounts for continuing flow.
