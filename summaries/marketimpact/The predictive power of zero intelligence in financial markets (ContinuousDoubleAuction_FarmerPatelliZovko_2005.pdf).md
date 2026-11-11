# The predictive power of zero intelligence in financial markets

J. Doyne Farmer, Paolo Patelli, and Ilija I. Zovko. *Proceedings of the National Academy of Sciences* 102(6), 2005, pp. 2254-2259. DOI: 10.1073/pnas.0409157102.

Source: [ContinuousDoubleAuction_FarmerPatelliZovko_2005.pdf](../../Finance/ContinuousDoubleAuction_FarmerPatelliZovko_2005.pdf). All six supplied pages, including references, were read. The article refers to online Supporting Text, additional tables, and Figures 5-11 that are not contained in this PDF. This note distinguishes what is available in the supplied article from those missing replication details. Journal page 2254 is PDF page 1.

## Why this matters

A limit-order book transforms order flow into spreads, depth, and volatility even before a model explains why investors choose that flow. Farmer, Patelli, and Zovko test whether a deliberately minimal model of this transformation can explain cross-sectional differences between real stocks. Their finding is striking: simple rate-based scaling laws explain 96% of the cross-sectional variation in average log spreads and 76% of the corresponding variation in log price-diffusion rates across eleven London stocks. Rescaling individual market orders and their immediate price effects by the same flow variables nearly collapses the different stocks' impact curves.

These are conditional structural relationships, not forecasts of tomorrow's returns or volatility. The inputs are measured order-flow characteristics from the same sample whose average market properties are being explained. The model does not forecast those inputs. Its practical attraction is a compact liquidity benchmark; its scientific attraction is a null hypothesis for separating mechanical effects of market design from explanations requiring sophisticated strategic behavior.

The paper's novelty is empirical testing of scaling laws derived earlier from a stochastic continuous double-auction model, together with the flow-based normalization of market impact. It does not originate all the underlying auction theory. It cites Daniels et al. (2003) and Smith et al. (2003) for construction, simulations, and mean-field analysis, emphasizing that the model and its predictions preceded this data examination. Nor does the paper claim that financial traders literally choose orders at random. It asks which aggregate quantities can be modeled usefully that way.

## Market state, order types, and stochastic primitives

The model uses the continuous double auction, in which buy and sell limit orders wait in two queues and incoming marketable interest consumes the opposite queue. Let $a(t)$ and $b(t)$ be the best ask and best bid in the modeled log-price coordinate, with $a(t)>b(t)$. The spread is $s(t)=a(t)-b(t)$, and the midpoint is $m(t)=[a(t)+b(t)]/2$. New limit orders can improve the quotes; market orders and cancellations can remove the best quote and expose the next occupied price.

The article classifies an order by its economic effect. A noncrossing order that adds standing liquidity is a limit order; an order that crosses the best opposite price and executes immediately is a market order. A real exchange order can be split into an immediately executing part and a residual resting part. This decomposition matters when estimating the model from a feed with many native order types: labeling every exchange “limit order” as a liquidity addition would misclassify marketable limits.

The independent Poisson primitives are:

| Symbol | Meaning | Units |
|---|---|---|
| $\mu$ | Market-order share flow | Shares per unit time |
| $\alpha$ | Limit-order placement density, with equal buy and sell densities | Shares per unit log-price per unit time |
| $\delta$ | Cancellation hazard of a resting order | Inverse time |
| $\sigma$ | Fixed number of shares per order in the model | Shares |

Buy limit orders are placed uniformly on $(-\infty,a(t))$, and sell limit orders uniformly on $(b(t),\infty)$. Thus an incoming order may improve its own best price inside the spread but cannot cross the current opposite best. Buying and selling are balanced in rate. Limit and market orders have constant size, cancellations occur independently at constant hazard, and all driving processes are independent except for the dependence of admissible placement regions on current quotes.

There is no utility function, inventory target, information signal, optimization condition, or fundamental-value process. An agent's minimal “intelligence” consists of respecting the current opposite quote. The book itself contains the relevant endogenous state. A new buy inside the spread changes the bid and therefore immediately changes the admissible lower boundary for future sell placement. This moving boundary is the feedback mechanism making a simple Poisson specification nontrivial.

A uniform placement density over an infinite half-line has infinite total arrivals but finite arrivals in every bounded price interval. The paper explicitly defends this local-intensity construction. It is not a probability density normalized to one over an infinite interval. Numerical implementations must still truncate or otherwise handle distant orders; the main article does not specify the simulator's finite boundaries or burn-in.

## Two scaling laws and what they do and do not prove

Define the dimensionless ratio

$$
\epsilon=\frac{\sigma\delta}{\mu}.
$$

It compares the flow scale associated with canceling an order to the market-order removal flow and also captures order discreteness. Equation 1 predicts the mean spread as

$$
\widehat s=\frac{\mu}{\alpha}f(\epsilon),
\qquad f(\epsilon)\approx 0.28+1.86\epsilon^{3/4}.
$$

The ratio $\mu/\alpha$ supplies the required price dimension. More market removal tends to widen the book; more limit addition tends to fill it. Cancellation and order size affect the dimensionless correction. The function $f$ is obtained from the prior model analysis; dimensional analysis alone determines neither its intercept nor its exponent. The expression is an approximation rather than an exact theorem for every $\epsilon$.

The dependence on typical order size is particularly useful. Two markets with identical gross share arrival rates can differ if one receives many small orders and the other fewer large ones. Orders are discrete parcels of liquidity, so share flow alone need not determine the spread. This is a more specific statement than the usual empirical observation that high market-order intensity accompanies low liquidity.

Equation 2 predicts a short-term diffusion rate

$$
\widehat D=k\mu^{5/2}\delta^{1/2}\sigma^{-1/2}\alpha^{-2},
$$

where $k$ is a constant. The diffusion convention is $V(t)=Dt$ for a random walk's variance, so $D$ has units of log-price squared per unit time; it is not volatility itself. The predicted volatility over a horizon would require the square root of a variance and a justified diffusion horizon. Substituting the primitive units verifies that the right side has the correct dimension.

The diffusion formula was found numerically in the preceding theoretical work. The authors explicitly state that it had not been analytically derived. Dimensional analysis helped identify the plausible functional form but did not prove the exponents. The law predicts greater volatility with market orders and cancellations, lower volatility with more limit placements, and an inverse square-root dependence on order size holding the other primitives fixed. The latter dependence is less intuitive than the liquidity-removal effects and should be treated as a testable model prediction rather than a universal causal law.

The article's claim of one free parameter concerns the empirical mapping, especially the window used to estimate local order placement and cancellation. Measured $\mu$, $\alpha$, $\delta$, and $\sigma$ are not separately fitted regression coefficients; they are inputs. At the same time, Equation 2 includes a multiplicative constant $k$, and the six-page article does not give its numerical calibration. Reconstructing an absolute diffusion forecast from this PDF alone therefore requires information beyond merely reading the displayed powers. It would overstate reproducibility to call the entire empirical exercise parameter-free.

## Sample and construction of the observables

The data are the electronic open limit-order book of the London Stock Exchange, representing about half the total trading volume in the market considered. The period is 1 August 1998 through 30 April 2000: 21 months and 434 trading days. There are eleven stocks and approximately six million events. Every stock contributes more than 300,000 events overall and at least 80 on every included day. An event is an order placement or cancellation. Opening-auction orders are removed because the model concerns continuous trading.

Figure 4 identifies the stock codes AZN, BARC, CW., GLXO, LLOY, ORA, PRU, RTR, SB., SHEL, and VOD. The main text does not provide a separate selection table, survival rules, corporate-action treatment, detailed trading-hour filters, or the method for reconstructing partially filled orders. These belong among the missing inputs for exact replication, rather than among assumptions that can safely be guessed.

For each stock, the empirical test measures average flow parameters, inserts them into the theoretical formula, and compares the resulting predicted average spread or diffusion rate with its measured counterpart over the same full period. Market share flow $\mu$ can be estimated as market-order shares divided by elapsed time, or by averaging daily estimates; the authors state that the results are similar. Measuring order size is described as straightforward, but the article does not spell out how a variable-size empirical distribution is reduced to the model's single fixed-size parameter.

The difficult mapping is the uniform placement and cancellation assumption. Real order placement is concentrated near best prices rather than spatially uniform. The authors introduce a price window enclosing approximately 60% of limit orders measured away from the midpoint, assume uniform placement inside it and zero outside it, and estimate $\alpha$ from shares placed within that window divided by its width and elapsed time. Daily estimates are then averaged for each stock. They estimate $\delta$ as the reciprocal of the mean lifetime of canceled orders within the same window.

Two different uses of “window” should be kept apart. The fraction 0.6 selects a share of placements, while the resulting price width has log-price units. The article uses $W$ in explaining both the window and its chosen 60% specification. For implementation, one should store the percentile choice and the actual daily price width as separate quantities. Changing the width changes parameter estimates and particularly the level of the spread prediction.

The cancellation estimate is conditional on observed canceled orders in that window. The main text does not discuss censoring at sample boundaries or distinguish cancellation hazard estimation from inverse completed lifetime under execution as a competing risk. Those details can matter materially when moving from a model with exponential cancellation to real order histories.

The spread is measured after each event with equal event weight, excluding the opening auction. Thus it is not a time-weighted quoted spread and not a volume-weighted effective spread. The authors average in levels first and then take the logarithm of each stock's average. They explicitly do not average logs of individual-event spreads. The distinction changes both the estimand and the interpretation of a log-linear fit.

There is a typographical inconsistency in the article: page 2256 describes the spread as the average of $\log b(t)-\log a(t)$, although the earlier definition has ask minus bid and the subsequent logarithm requires a positive spread. The positive-spread model and plots indicate the intended economic variable. A replication must resolve this sign using the original implementation; this note flags the inconsistency rather than treating the negative expression as an implementable positive spread.

## Empirical accuracy and the limited number of independent comparisons

For spread, the authors estimate

$$
\log \overline s_i=A\log\widehat s_i+B,
$$

where each observation is one stock's full-period average. The model benchmark is $A=1$ and $B=0$. The estimates are $A=0.99\pm0.10$ and $B=0.06\pm0.29$, with $R^2=0.96$. The fit strongly rejects a zero slope and does not reject a unit slope. The intercept is somewhat arbitrary because the placement window affects the prediction's scale, so the slope and dispersion around the relation are more informative than a naive test of the intercept alone.

The analogous diffusion regression gives $A=1.33\pm0.25$ and $B=2.43\pm1.75$, with $R^2=0.76$. A zero slope is rejected; a unit slope is not rejected at 95% confidence, although the point estimate suggests actual diffusion grows faster across stocks than the model prediction. Figure 3 also visually shows a level departure from the diagonal. “Explains 76%” should therefore not be restated as unbiased prediction or accurate calibration for every stock.

The millions of events do not make this a regression with millions of independent cross-sectional observations. The plotted regression has eleven points. Long memory within order-flow series and cross-stock dependence inflate uncertainty relative to independent sampling. The article says its errors account for these difficulties but delegates the detailed estimation procedure to Supporting Text. The displayed $\pm$ quantities are reported here as in the source; without the supplement one cannot fully reconstruct their computation or resampling scheme.

The authors say 60% was chosen a priori and also happens to be near the best-fitting choice, while changing the window does not substantially change goodness of fit. Numerical sensitivity grids are absent from the supplied PDF. The result supports a robust approximate scaling relationship, but the exact range of robustness is not documented here.

## Instantaneous impact and dimensional collapse

The market-impact observable is an immediate quote response to a single market order, not the execution cost of a multi-hour institutional parent order. If an incoming order of size $\omega$ removes all standing quantity at the best price, the midpoint changes to reflect the next available quote. The article defines

$$
\phi(\omega)=E[\Delta p\mid\omega],
$$

where $\Delta p$ is the logarithmic midpoint change between the instant before and the instant after that order, before another event occurs. The curve includes orders that move prices and orders that do not. It is distinct from the price walk needed to fill a large hypothetical sweep through a frozen book.

The model explains qualitative concavity through book depletion. Near-best limit orders are removed more quickly than distant orders, leaving an average stored-order density that rises away from the midpoint. As cumulative quantity penetrates deeper into that increasing density, incremental price movement per additional share falls. Nevertheless, the theoretical model predicts greater variation of impact with $\epsilon$ than the data exhibit. The article acknowledges this quantitative failure instead of claiming a complete fit to impact shape.

Its more successful result is a rescaling. For each order on day $t$, define

$$
\Delta p^*=\Delta p\frac{\alpha_t}{\mu_t},
\qquad
\omega^*=\omega\frac{\delta_t}{\mu_t}.
$$

Both variables are dimensionless. The price scale is $\mu_t/\alpha_t$ and the quantity scale $\mu_t/\delta_t$. The transformation uses daily flow estimates before pooling observations into impact bins. Merely rescaling the final stock-average curve by a full-sample average need not reproduce the same result.

Figure 4 compares this normalization with an ordinary plot using British-pound order value against log-price movement. Ordinary units yield visibly different stock curves. Dimensionless units produce a near collapse: corresponding bins differ across stocks by about 8% on average, approximately the reported sampling-error scale. The authors cannot reliably establish that the remaining differences are statistically significant because of long memory and cross-stock dependence, and they explicitly qualify those tests.

On a double-logarithmic scale the common curve is approximately proportional to $\omega^{0.25}$. This empirical exponent is not the now-common claim of square-root parent-order impact. It applies to their immediate, single-event average and their sample. Nor is the collapse evidence that an arbitrary order can be executed at a quarter-power cost independent of order splitting, participation, information, or other traders' reactions. Those mechanisms are not modeled or tested.

## Interpretation for quantitative work

The paper makes a useful causal distinction. Rational-choice explanations may say volatile conditions cause investors to prefer the execution certainty of market orders. This model produces a positive association in the opposite mechanical direction: more market orders deplete standing liquidity and raise volatility. Both mechanisms can operate simultaneously. A positive regression between market-order share and volatility does not identify the strategic explanation by itself.

The strongest application is as a baseline relating local liquidity supply, liquidity removal, and book outcomes. Deviations from its predictions can motivate investigation of strategic placement, hidden liquidity, correlated order flow, inventory effects, or market design. They are not direct proof of misconduct or exploitable mispricing. The article suggests regulation or market-maker monitoring as possible uses, but supplies no intervention study establishing how agents would adapt to fees or incentives.

The simplicity is also the main limitation. Real orders have variable sizes, clustered arrivals, signed persistence, price-dependent cancellations, strategic placement, and cross-market routing. Uniform independent flow suppresses all of these. The model can permit profitable trading opportunities because it contains no equilibrium discipline forcing efficient prices, although the authors describe unpublished simulation evidence that such profits are finite and risky. Its explanatory success for average spread does not validate it as a realistic simulator of every execution path.

For exact replication, the supplied article is sufficient to reconstruct the conceptual model, scaling formulas, broad sample, regression target, and impact normalization. It is insufficient for the stock-level parameter table, diffusion estimator and horizon, full uncertainty calculation, precise window construction, event cleaning, and simulator constants. The missing supporting material is therefore a real boundary to the note. The defensible result is that a parsimonious mechanical model organizes important cross-sectional facts remarkably well in this historical sample, not that it delivers an independently validated trading strategy.

## Bibliographic and source map

Farmer, J. Doyne, Paolo Patelli, and Ilija I. Zovko. 2005. “The predictive power of zero intelligence in financial markets.” *PNAS* 102(6): 2254-2259. Model and Eq. 1-2: pp. 2254-2255, PDF pp. 1-2. Sample, parameter measurement, and spread regression: p. 2256, PDF p. 3. Diffusion and immediate impact: p. 2257, PDF p. 4, Figures 3-4. Dimensionless normalization and interpretation: pp. 2258-2259, PDF pp. 5-6. Background theory cited by the article: Daniels, Farmer, Iori, and Smith (2003), *Physical Review Letters* 90, 108102; Smith, Farmer, Gillemot, and Krishnamurthy (2003), *Quantitative Finance* 3, 481-514.
