# Empirical option pricing: a retrospection

David S. Bates. *Journal of Econometrics* 116 (2003), 387–404. DOI: 10.1016/S0304-4076(03)00113-1.

Source: [OptionPricing_Bates_2003.pdf](../../Finance/OptionPricing_Bates_2003.pdf). References below use journal page numbers; PDF page 1 is journal page 387. All 18 pages, including the references and the reported regressions, were inspected.

## Why this matters

Bates asks what counts as an empirical test of an option-pricing model. The central answer is broader than fitting today's option surface. A useful structural model must connect the underlying's historical behavior, the cross-section of option prices, the evolution of the option surface, and the joint dynamics that determine hedge performance. A flexible formula can describe the cross-section while failing those connections.

This paper is a critical retrospective and research agenda, not a new calibrated model or a large original trading experiment. Its contribution is to organize empirical evidence around consistency restrictions and to explain why apparently successful option-model estimation can be weak evidence for the economics of the model. It also develops a particularly useful interpretation of the wedge between implied and realized volatility: that wedge can constrain the form of volatility and jump risk premia, rather than merely supply another regression showing that implied volatility is biased.

For a quantitative researcher, the practical objective is to design tests that can distinguish a pricing interpolation device from a model of financial risks. Parameters estimated from options alone often represent risk-neutral beliefs. Historical data identify a different probability law. Risk premia connect them. A model that leaves this connection unrestricted may fit both datasets but say little about why option holders earn the returns they do.

## The three objects that a structural model must distinguish

Let $P$ be the physical probability law, $Q$ a risk-neutral law, $S_t$ the underlying price, and $Y_t$ a vector of latent state variables such as variance or jump intensity. For a European call,

$$
C_t=E_t^Q\left[e^{-\int_t^T r_u\,du}(S_T-K)^+\right].
$$

Equivalently, under $P$, $C_t=E_t^P[m_{t,T}(S_T-K)^+]$ for a valid stochastic discount factor $m$. These are valuation representations, not empirical evidence that one particular discount factor or state law is correct. A structural model must specify the dynamics of $(S,Y)$ under $P$, the change to $Q$, and the parameters governing the price of each unspanned risk.

In Bates's generic notation, an option-pricing function can be written $c(S_t,Y_t,T;\theta,\lambda)$, where $\theta$ captures process parameters and $\lambda$ the relevant risk-premium parameters. The distinction between a state and a parameter matters. The current variance can change daily while its mean-reversion parameters remain fixed. Reestimating all parameters every day lets a model absorb failures into moving parameters and weakens its interpretation as a stable stochastic system.

Affine models are attractive because characteristic functions and conditional transforms are tractable, facilitating pricing and likelihood-based restrictions. Their convenience is not a license to regard the physical and risk-neutral processes as interchangeable. Changing measure often changes variance drift or jump intensities while preserving enough functional structure for closed-form transforms. The empirical issue is whether one set of parameters and premia can account for both sets of observations.

Incomplete-market models add a further distinction. Specifying the physical variance or jump process does not by itself determine the option price: compensation for risks that cannot be replicated with the underlying must also be specified. Conversely, today's option prices identify aspects of the risk-neutral distribution without necessarily identifying the physical distribution or investor preferences separately.

## Black–Scholes supplies several different tests

Section 1 uses Black–Scholes as a compact example of the multiplicity of model implications. The assumptions imply more than lognormal terminal returns. A constant-volatility diffusion constrains the underlying's time series; the same constant volatility should price all strikes and maturities; implied volatility should not wander through time; and implied volatility should be compatible with subsequently realized variation. A term structure of implied volatility also implies forecasts about the subsequent evolution of shorter-maturity implied volatility.

Joint underlying–option behavior is another test. A call and the underlying should move in the same direction for a small price change, and a put in the opposite direction, holding the other model inputs fixed. Independent option-price movements reveal omitted states or market frictions. Bates cites evidence from 1994 S&P 500 options in which these simple directional restrictions are violated in roughly 7–17% of observations. That statistic comes from cited work, not an independently cleaned dataset in this article. It illustrates why looking only at a smooth surface on one date misses important dynamics.

Finally, replication imposes an almost degenerate instantaneous relationship. Ignoring deterministic financing terms at the leading diffusion scale,

$$
\frac{dC_t}{C_t}=\frac{S_tC_S}{C_t}\frac{dS_t}{S_t}+O(dt).
$$

The coefficient is the option elasticity. Under the model, option and stock diffusion shocks have only one source, so delta hedging should eliminate that instantaneous risk. Empirical hedge residuals therefore test a stronger restriction than small pricing errors. Stochastic volatility, jumps, changing implied distributions, asynchronous quotes, and trading costs can each break the idealized hedge relation, but they are economically different failures.

These tests have unequal diagnostic power. Failure of a constant implied-volatility surface is easy to establish, whereas explaining the dynamic premium on a variance exposure is harder. A model can cure one failure and retain another. The paper's organizing principle is to keep the full collection of implications visible when evaluating a proposed extension.

## What common model extensions fix and what they leave unresolved

Local-volatility models make instantaneous volatility a deterministic function of the underlying and time. Given an adequate arbitrage-free surface, they can fit a cross-section of European prices closely. Their appeal is retaining a one-factor diffusion and the associated replication logic. But flexibility across strike does not create the independent volatility shocks seen in the option surface. A function fitted at one date can predict the wrong movement of the smile as the underlying moves. Continual recalibration can restore fit while abandoning the original dynamics.

There is also a stationarity issue. A local-volatility function written in the absolute asset-price level can behave oddly as the price drifts far from its calibration range. Calendar-time dependence and moving calibration parameters may be necessary to track the data. These can be useful engineering choices, but they alter the claim that a fixed economic process has been empirically validated.

Independent, identically distributed return jumps add skewness and kurtosis and can improve short-dated out-of-the-money pricing. However, their nonnormal contribution tends to average out with horizon, and a constant jump process does not explain persistent changes in the overall volatility level. Pure jump corrections therefore address distributional tails without automatically explaining the surface's time-series behavior.

Stochastic-volatility models introduce a separate state and can generate persistent volatility and leverage-related asymmetry. They are more natural candidates for explaining both volatility forecasts and option dynamics. The problem reviewed by Bates is quantitative: volatility-of-volatility values consistent with the underlying time series often do not generate the pronounced risk-neutral equity-index smirk. Parameters that price options well can imply variance movements that are implausible under the observed physical history unless a substantial risk premium is added.

Combining stochastic volatility and jumps improves flexibility. State-dependent jump intensities, jumps in variance itself, multiple factors, and nonaffine variance dynamics each address particular shortcomings. Yet a better price fit does not guarantee a proportionate improvement in hedging. Bates highlights the empirical distinction, including evidence associated with Bakshi and coauthors, that adding jumps may improve pricing more than hedge performance. The extra component must be tested against the dynamic data it is intended to explain.

The retrospective discusses work using long underlying histories, including a 37-year Dow Jones sample in research by Chernov and coauthors. Those cited studies compare richer dynamics, rather than constitute Bates's own common-sample benchmark. Sample periods, return measurement, and estimation criteria differ across the literature. The article does not provide enough inputs to reconstruct every cited comparison as a single controlled experiment.

## Why option-only calibration can look more decisive than it is

A broad cross-section of option prices contains many observations about one date's risk-neutral distribution. It does not contain an equal number of independent observations of the latent process through time. If a model has several latent states, a small set of liquid options can nearly invert the pricing relation to recover those states. Additional strikes then mostly test the cross-sectional shape conditional on those inferred values.

A joint estimation criterion can be dominated by the number and apparent precision of option quotes. Bid–ask measurement noise may be small while systematic model errors remain much larger. Bates notes that model residuals can be roughly one to four times measurement-error estimates. Treating every quote as an independent, correctly specified measurement can create impressively small standard errors without ensuring that the model's physical dynamics are right.

For example, suppose $K$ latent factors are recovered from $K$ option prices at each date. Conditional on a trial parameter vector, one solves

$$
\widehat Y_t(\theta,\lambda)=c^{-1}(C_{t,1},\ldots,C_{t,K};S_t,\theta,\lambda).
$$

The inferred path can then be checked against its specified transition law and used to price held-out strikes or maturities. This separation makes restrictions easier to diagnose: some data identify states; others test the pricing function; still others test their evolution. The inversion must exist and be sufficiently well conditioned, and parameter uncertainty in the recovered states must be acknowledged. A perfect inversion of the chosen quotes is not an out-of-sample success.

Alternatively, all quotes can enter a measurement-error or likelihood model. Then the cross-sectional covariance of errors, serial dependence, bid–ask effects, and the relative weight of the underlying time series become important. A misspecified error model can make a large option panel overwhelm a shorter but economically decisive underlying-return record. The paper argues for interpreting estimated precision in the context of these restrictions, rather than accepting small reported parameter errors at face value.

Daily recalibration creates another ambiguity. If a model is reestimated from yesterday's surface and predicts today's prices well, persistent implied-volatility patterns may do most of the work. One-day prediction is useful operationally but is not a demanding test of a stable structural model. A lagged surface can be a strong benchmark without explaining why it has its shape. Longer horizons, fixed-parameter exercises, and joint hedge tests help separate persistence from model content.

## The loss function is part of the experimental design

Different fitting criteria answer different questions. Minimizing dollar pricing errors gives greater weight to expensive options. Percentage price errors can be extreme for low-priced, deep-out-of-the-money options. Implied-volatility errors express misspecification in a common volatility unit but implicitly reweight price errors by vega. Normalizing option prices by the underlying can aid comparisons across price levels, yet does not remove every source of heteroskedasticity.

The same issue applies when comparing models out of sample. Estimating one model by dollar error and judging it by percentage error, while giving a competitor another objective, mixes model differences with loss-function differences. The choice must reflect the intended use: valuation, a particular hedge, risk-neutral-density inference, or forecasting. A score suitable for liquid at-the-money trading need not be suitable for far-tail insurance valuation.

A reproducible study built from the paper's recommendations should therefore state quote filters, synchronization rules, loss weights, the parameter-update schedule, the set of options used to infer states, and the held-out contracts. It should also say whether hedges are evaluated at theoretical prices, midpoints, or executable quotes. These details are not supplied as one algorithm in the retrospective; they are necessary operational choices inferred from its critique.

For a structural model, validation should include how the inferred state behaves under $P$, how observed options behave under $Q$, and whether their joint evolution is consistent with the specified change of measure. A lower average pricing error is evidence about the selected loss, not a blanket ranking of all economic uses of the model.

## The original implied-versus-realized volatility illustration

The most concrete numerical exercise appears on journal page 398, equations (2)–(3). Bates uses 30-day at-the-money S&P 500 futures options observed at noon from January 1988 through November 1998. Realized variation is measured from noon futures-price observations during the option life. The monthly observations are described as essentially nonoverlapping. The regressions use heteroskedasticity-consistent standard errors, but the exact estimator, final observation count, quote-cleaning rules, and data vendor are not fully specified in the article.

Define annualized realized variance over a $T$-day horizon by

$$
RV_t=\frac{365}{T}\sum_{j:\ t<t_j\leq t+T}(\log F_{t_j}-\log F_{t_{j-1}})^2.
$$

Here $T$ is the calendar-day option horizon and the sum uses the available consecutive noon observations within it. Let $IV_t$ be the option's annualized implied volatility. The reported variance regression is

$$
RV_t=0.0027+0.681\,IV_t^2+\varepsilon_t,
\qquad R^2=0.33,
$$

with standard errors 0.0033 on the intercept and 0.161 on the slope. In volatility units, the second regression is

$$
\sqrt{RV_t}=0.0160+0.756\,IV_t+u_t,
\qquad R^2=0.45,
$$

with standard errors 0.0142 and 0.102. On average, implied volatility exceeds realized volatility by about two volatility percentage points in this sample.

These are different regressions. Taking a square root after averaging variance is not the same operation as averaging realized volatility, and the slopes need not coincide. The intercept in the variance regression is in annualized variance units; the volatility regression's 0.0160 is 1.60 annualized volatility percentage points. The $R^2$ values should not be read as equal measures of forecast quality on an identical dependent-variable scale.

The slopes below one are consistent with a state-dependent wedge between risk-neutral and physical expected variation. They do not, alone, identify that wedge. Measurement error in implied volatility, realized-variance noise, finite samples, omitted nonlinearities, or a misspecified physical state process can affect the regression. The paper's contribution is to ask whether particular risk-premium mechanisms can produce the observed slope pattern, not to prove that the regression is a unique estimator of investor risk aversion.

To reproduce this exercise, collect noon futures and contemporaneous 30-day at-the-money option prices, reconstruct the implied-volatility convention, form horizon-matched realized variance with the 365-day annualization, select the monthly observations, and fit both regressions with documented robust covariance estimation. Missing noon quotes, interpolation to exactly 30 days, holidays, futures rolls, and the definition of at-the-money require explicit choices not fully recoverable from this short description. A new implementation should disclose those choices and avoid claiming an exact replication solely because its slope is below one.

## What the slope says about risk premia

In an affine setting, expected future variation may be approximately affine in a current state:

$$
E_t^P[RV]=a+bY_t,\qquad E_t^Q[RV]=a^*+b^*Y_t.
$$

If implied variance is a sufficiently close proxy for the second quantity and realization noise is conditionally mean zero, eliminating $Y_t$ yields a regression slope $b/b^*$. A slope below one requires the risk-neutral exposure to the state to exceed the physical exposure. This simple algebra clarifies which proposed explanations change an intercept and which change a slope.

For stochastic volatility, a risk-neutral process that mean reverts more slowly keeps a high current variance elevated longer under $Q$ than under $P$. The option-implied forecast therefore responds more strongly to the state. This can create the observed slope below one. But if calibration drives the risk-neutral variance process into locally explosive behavior, it can imply implausibly strong increases in variance at longer maturities. A premium that fixes one regression must be checked against the volatility term structure.

For jumps, a constant premium on a constant jump intensity can add a roughly constant amount to risk-neutral expected variation. That changes the intercept but cannot by itself explain a state-dependent slope wedge. State-dependent jump intensity or a state-dependent price of jump risk is needed for that mechanism to affect the slope in the same manner. Thus the regression can reject an overly simple premium story even when it cannot separately identify all the richer alternatives.

Another discrepancy concerns crash frequencies inferred from options. Bates discusses risk-neutral crash arrival rates of roughly 0.5–5 per year in some calibrations, dramatically larger than the experience of a relatively short historical sample with few crashes. This is not a literal forecast that crashes should occur at the risk-neutral rate. It may reflect a high price for tail insurance, a rare-event or peso-problem interpretation of the sample, or model misspecification. The physical frequency and pricing weight must not be conflated.

Option-implied variance is also not always exactly expected realized variance under $Q$. The mapping depends on the option set, payoff approximation, jumps, and the definition of implied volatility. The affine elimination argument is a useful approximation for interpreting the reported regressions; it should not be promoted to an exact identity for every Black–Scholes implied volatility extracted from one option.

## From statistical fit to an economic explanation

No-arbitrage language can hide an unresolved economic question. Given sufficiently flexible pricing-kernel choices, a wedge between physical and risk-neutral distributions can be accommodated. The more demanding question is why investors pay that premium, who supplies the insurance, and what constraints determine the compensation.

Bates emphasizes market structure. Institutional investors may be large buyers of crash or volatility insurance, while a smaller set of intermediaries supplies it under capital and risk-management constraints. Delta hedging handles small underlying moves in a diffusion approximation. It does not eliminate jump losses or independent changes in the volatility state. Buying other options to neutralize gamma or vega reallocates aggregate risk among participants; it does not make the system's net demand for insurance disappear.

The analogy with catastrophe insurance makes this concrete. The paper cites premiums reaching about nine times expected losses in that setting. Such a multiple cannot be interpreted from actuarial expected loss alone; capital, tail exposure, and intermediary constraints matter. The analogy is suggestive rather than an estimated structural explanation of equity-option premia. It motivates models that account for who is willing and able to warehouse risks.

Worst-case superhedging gives another perspective, but can generate bounds too wide to explain traded prices. Treating every admissible adverse path as decisive resembles extreme aversion to model uncertainty. A useful economic model must balance robustness against finite compensation, capital availability, and actual investor preferences. The paper does not prescribe a universal utility function or transaction-cost calibration that resolves this tradeoff.

Learning is another neglected element. A model may presume investors observe the current variance state and know all structural parameters, while the econometrician struggles to infer both. If investors themselves learn, belief revisions become an additional source of option-price variation. Treating latent-state estimates as perfect knowledge can miss this channel. Learning can also alter how a crash updates perceived tail frequencies, making a fixed risk-premium interpretation incomplete.

## A research design implied by the retrospective

The most useful way to operationalize Bates's critique is to declare the model's independent restrictions before fitting it. Specify which features belong to the physical process, which can change under the pricing measure, and which risk premia are constant or state dependent. Identify the observations used to estimate parameters, the prices used to infer current states, and the observations reserved for tests.

Then evaluate several distinct outputs: the underlying transition distribution and tail behavior; option pricing errors by strike and maturity under a common loss; state and implied-surface persistence; implied-versus-realized variation over matched horizons; and hedge residuals conditional on market moves and volatility changes. If parameters must be recalibrated frequently, report their instability as a result rather than treating it as an invisible operational step.

Uncertainty should reflect both finite historical samples and the dependence among quotes from one date. A dense cross-section is not a substitute for many independent crises. The risk-neutral tails may be well constrained over traded strikes while physical tail probabilities remain weakly identified. Empirical conclusions should state which side of that distinction the evidence supports.

This article does not provide a complete dataset, source code, standardized train/test split, optimization settings, or an all-model horse race. Its lasting result is a framework for assessing such work: cross-sectional fit, historical plausibility, dynamic consistency, and economic risk compensation are separate achievements. A model becomes more credible when the same specification survives all four, with its failures made visible rather than absorbed by perpetual recalibration.
