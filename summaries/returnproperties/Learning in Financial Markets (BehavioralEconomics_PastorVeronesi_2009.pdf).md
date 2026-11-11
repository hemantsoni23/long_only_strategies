# Learning in Financial Markets

**Authors:** Lubos Pastor and Pietro Veronesi. **Publication:** *Annual Review of Financial Economics* 1 (2009), 361–381. **DOI:** 10.1146/annurev.financial.050808.114428. **Source:** [BehavioralEconomics_PastorVeronesi_2009.pdf](../../Finance/BehavioralEconomics_PastorVeronesi_2009.pdf).

This is a research review, organized around Bayesian learning as a mechanism connecting financial decisions and observed asset prices. It does not introduce a single estimated model or a new unified empirical dataset. Its contribution is to show how uncertainty about otherwise conventional model parameters changes valuation, return dynamics, portfolio choice, and investment behavior. The appendix derives a simple valuation and volatility example. Page references below use printed pages 361–381; PDF pages 22–24 are journal contents and advertising, not additional research results.

## Why this matters

A researcher can mistakenly attribute an apparent anomaly to irrationality by giving model investors information that actual investors did not possess. A fixed but unknown expected return is not equivalent to a known expected return: estimates move with observations, the predictive distribution differs from a distribution evaluated at estimated parameters, and an optimal investor anticipates future learning. Similarly, a high realized return can signal either high future profitability or a decline in the discount rate. The sign of the investment response depends on which latent quantity is being learned.

The review therefore offers a way to build and diagnose models, rather than an implementable trading signal. Specify the hidden state, observations, prior, information available at each date, and economic decision rule; derive the posterior before interpreting prices or allocations. The authors emphasize parsimonious rational explanations but do not establish that learning uniquely explains every reviewed phenomenon. They explicitly call for predictions that discriminate learning from competing mechanisms and for quantitative calibration or structural estimation (p. 376).

## The common statistical model

The starting point is a fixed unknown parameter $\theta$, with normal prior mean $\theta_0$ and variance $q_0$. Independent observations satisfy

$$
s_t=\theta+\varepsilon_t,\qquad \varepsilon_t\sim N(0,\sigma^2).
$$

Here $\sigma^2$ is known observation noise; it is distinct from uncertainty $q_t$ about the parameter. Equations (1)–(2), p. 362, imply

$$
q_T=\left(q_0^{-1}+T\sigma^{-2}\right)^{-1},\qquad
\widehat\theta_T=q_T\left(q_0^{-1}\theta_0+\sigma^{-2}\sum_{t=1}^T s_t\right).
$$

For sequential implementation, initialize $(\widehat\theta_0,q_0)=(\theta_0,q_0)$ and update

$$
K_t=\frac{q_{t-1}}{q_{t-1}+\sigma^2},\qquad
\widehat\theta_t=\widehat\theta_{t-1}+K_t(s_t-\widehat\theta_{t-1}),\qquad
q_t=(1-K_t)q_{t-1}.
$$

This is the review’s equation (3), with $K_t$ replacing its multiplier $m_t$. A large surprise changes beliefs most when prior uncertainty is high relative to observation noise. Under these assumptions, uncertainty declines deterministically: its path depends on observation count, not realized surprises. That property becomes a substantive limitation when the model is used to explain recurring volatility episodes.

In continuous time, observations follow $ds_t=\theta\,dt+\sigma\,dW_t$. The exact Gaussian filter is

$$
d\widehat\theta_t=\frac{q_t}{\sigma^2}(ds_t-\widehat\theta_t\,dt),\qquad
q_t=(q_0^{-1}+t/\sigma^2)^{-1}.
$$

The innovation $ds_t-\widehat\theta_tdt$ is the unanticipated signal. Both the clock and variance units must match: replacing annual observations by monthly observations without changing the noise variance changes the model. These formulas assume independent normal noise and an invariant latent parameter; regime changes, correlated signals, and unknown noise variance require a different filter.

## Valuation: convexity, uncertainty, and an integrability qualification

With a fixed discount rate $r$ and known constant dividend-growth rate $g<r$, the continuous-time model is

$$
\frac{dD_t}{D_t}=g\,dt+\sigma\,dW_t,\qquad
P_t=E_t\left[\int_t^\infty e^{-r(u-t)}D_u\,du\right]
=\frac{D_t}{r-g}.
$$

In this continuous-time expression $D_t$ is the current dividend flow. Conditional on $g$, expected future dividends are $D_te^{g(u-t)}$; integration gives the Gordon denominator. The diffusion affects realized dividends but not their conditional mean growth.

For an uncertain fixed $g$ with posterior density $f_t$, the appendix, equation (15), derives

$$
\frac{P_t}{D_t}=\int_{-\infty}^{r}\frac{f_t(g)}{r-g}\,dg.
$$

When the integral is finite and the distribution is nondegenerate, convexity gives

$$
E_t\left[\frac{1}{r-g}\right]>\frac{1}{r-E_t[g]}.
$$

Thus substituting the estimated mean growth into a nonlinear pricing formula understates the price in this fixed-discount-rate example. More uncertainty raises price under a mean-preserving spread, with expectations well defined. A larger variance alone does not order arbitrary distributions in convex order. Nor is this a general equilibrium theorem saying all forms of uncertainty increase valuations: the discount rate can also respond.

**Mathematical qualification to the source.** The stated condition $g<r$ almost surely is insufficient for a finite price. In particular, the appendix uses a normal distribution truncated at $r$. Such a density has a positive left limit at $r$, so its price integral diverges logarithmically. Writing $h=r-g$, the problematic part is proportional to $\int_0^\epsilon dh/h$. A normal tail with very small density near the boundary still has this problem. Consequently, the finite volatility example based on that literal infinite-horizon specification cannot be reproduced without an additional restriction.

A sufficient repair is support bounded by $r-\epsilon$ for some fixed $\epsilon>0$; another is a density vanishing sufficiently quickly at $r$. A finite dividend horizon also removes the singularity, replacing $1/(r-g)$ by $[1-e^{-(r-g)H}]/(r-g)$, whose limit at $g=r$ is $H$. These are qualifications and possible repairs derived in this note, not restrictions stated in the review. They should be declared explicitly before numerical integration; a quadrature routine that stops just short of the singularity can return a misleading finite answer.

The economically broader application concerns uncertainty about average profitability and market-to-book value, including firms paying no dividends. The review reports that median market-to-book falls from 2.25 for one-year-old firms to 1.25 for ten-year-old firms in the evidence of Pastor and Veronesi (2003). The predicted negative age relation is stronger among younger and non-dividend-paying firms. Market-to-book rises with the level and volatility of profitability and falls with expected return. These are reported cross-sectional findings, not coefficients estimated anew in this review; the underlying sample construction, regression controls, and standard errors are not reproduced here.

## Volatility and technological booms

Learning creates two responses to a dividend innovation: the current dividend changes, and the estimate of future growth changes. Define $F(\widehat g,q)=\log(P/D)$ for a well-defined valuation function. If one approximates the growth filter by the Gaussian filter above and posterior variance has no diffusion term, Ito’s formula gives the diffusion component

$$
\frac{dP_t}{P_t}\bigg|_{\mathrm{diffusion}}
\simeq \sigma\left[1+F_{\widehat g}(\widehat g_t,q_t)\frac{q_t}{\sigma^2}\right]d\widetilde W_t.
$$

Therefore equation (8), p. 366, expresses return volatility approximately as dividend-growth volatility multiplied by $1+F_{\widehat g}q_t/\sigma^2$. The price reaction is amplified when growth expectations respond strongly to news and price is sensitive to those expectations. This is an instantaneous diffusion calculation; drift terms and Ito corrections are omitted only because they do not determine instantaneous volatility. The source labels the filtering step an approximation because Gaussian posterior updating is not exact for its truncated-normal distribution.

The review’s numerical illustration uses dividend volatility 5% per year, discount rate 10%, posterior mean growth 3%, and growth uncertainty with standard deviation 2%, and reports approximately 20% return volatility. That is the authors’ reported fourfold amplification, not a verified numerical output of the literal truncated-normal specification. The integrability issue above prevents treating it as an exact replication target without a stated boundary treatment. The more general mechanism does not require endorsing that particular numerical implementation.

The empirical motivation is an approximately 17% annual postwar market-return volatility versus 5% dividend-growth volatility. At the firm level, the cited median monthly return volatility declines from 14% for one-year-old stocks to 11% for ten-year-old stocks. The monthly firm figures must not be confused with annual aggregate figures. The review provides these descriptive magnitudes without a replication panel or inference table.

Constant-parameter Gaussian learning cannot by itself generate repeated uncertainty shocks: $q_t$ decreases with time. Hidden regime changes can. An observation inconsistent with the current regime raises the probability of a shift, makes older data less informative, and can raise posterior uncertainty. Persistent beliefs about regimes then generate persistent volatility. In Veronesi’s setting, bad dividend news in good times raises both uncertainty and the equilibrium discount rate, amplifying the price decline. This mechanism differs from merely increasing the fixed noise variance in the elementary filter.

For the late-1990s Nasdaq, the reviewed calibration infers growth uncertainty from peak valuation in March 2000 and checks whether that uncertainty is compatible with observed volatility. Starting from those peak-matching beliefs, the subsequent profitability deterioration in 2000–2001 produces downward revisions and a substantial price decline. Matching the starting valuation is a calibration condition, not independent validation or an advance prediction of the peak.

The technological-adoption model adds an endogenous transition from idiosyncratic to systematic risk. Productivity news first raises expected cash flows; if adoption spreads, exposure to the technology becomes economy-wide and required returns rise. The cash-flow effect dominates early and the discount-rate effect later. Conditioning on technologies that eventually achieve widespread adoption selects unusually favorable early news. The resulting boom-and-decline pattern is visible in hindsight, rather than a predictable bubble path available to investors ex ante.

The review cites railroad evidence for 1830–1861 and Internet evidence for 1992–2005. Nasdaq’s market beta roughly doubled between 1997 and 2002, and railroad betas increased sharply in the 1850s. These beta changes help distinguish the model from explanations based solely on enthusiasm, but do not exclude every behavioral or risk-based alternative. Exact beta windows, constituent histories, and adoption parameters require the cited original study.

## Expected returns: distinguish perceived opportunities from hindsight

A low growth estimate relative to the unknown true growth rate depresses current price. Subsequent positive learning surprises then raise realized returns. An econometrician can observe low price-to-dividend ratios followed by high returns even when investors could not know that their growth estimate was too pessimistic at the time. Learning thus separates the investors’ perceived return distribution from the empirical distribution conditional on the true parameter.

This is not a claim that all predictability is untradeable. Risk-driven time variation in required returns can be observable to investors. The review treats that case separately. An implementable test must use the investor’s historical information set and beliefs, rather than classify dates using a full-sample estimate of the true growth rate.

There is also no universal sign for the equity-premium effect of learning. With power utility and elasticity of intertemporal substitution below one, bad growth news can raise desired saving and stock demand, cushioning the price fall and reducing covariance with consumption growth. Other preferences, elasticity above one, or distinct consumption and dividend processes can reverse the sign. Unknown consumption volatility can thicken predictive tails. Ambiguity aversion adds a separate worst-case or model-penalty decision rule; it is not equivalent to Bayesian uncertainty about a parameter within one accepted model.

Two cross-sectional examples show why the economic mapping matters. In Johnson’s levered-firm model, greater idiosyncratic uncertainty raises equity’s option value and reduces its exposure to priced risk, lowering expected equity return. The dispersion-return relation should therefore be stronger for more levered firms. In structural credit models, imperfect observation of asset value makes proximity to default uncertain and can generate non-negligible short-maturity credit spreads. Neither mechanism follows from a generic instruction to raise every risk premium when uncertainty increases.

## Filtering conditional mean returns

Equations (9)–(10), pp. 369–370, separate realized returns from latent expected returns:

$$
r_{t+1}=\mu_t+u_{t+1},\qquad
\mu_{t+1}=(1-b)\bar\mu+b\mu_t+w_{t+1}.
$$

Jointly Gaussian innovations may have covariance $c=\operatorname{Cov}(u_{t+1},w_{t+1})<0$: a positive innovation to required future return can depress today’s price. The optimal estimate uses a Kalman filter, not an ordinary moving average of returns.

For clarity, the following recursion is derived from those two equations for known parameters. Let $a_t=E[\mu_t\mid\mathcal F_t]$, $Q_t=\operatorname{Var}(\mu_t\mid\mathcal F_t)$, and innovation variances $v_u,v_w$. After observing $r_{t+1}$,

$$
a_{t+1}=(1-b)\bar\mu+ba_t+
\frac{bQ_t+c}{Q_t+v_u}(r_{t+1}-a_t),
$$

$$
Q_{t+1}=b^2Q_t+v_w-\frac{(bQ_t+c)^2}{Q_t+v_u}.
$$

This follows by conditioning the joint normal pair $(\mu_{t+1},r_{t+1})$: their conditional covariance is $bQ_t+c$. Innovations are assumed independent of previous information, and their covariance matrix must be positive semidefinite. The gain can be negative when $c<-bQ_t$, so a high recent return can reduce the forecast of the next return. The review also explains positive weights on more distant returns through information about the unconditional mean. Reproducing that richer weighting requires specifying uncertainty about $\bar\mu$; the displayed known-parameter scalar recursion does not silently estimate it.

If instead expected return is $\mu_t=\alpha+\beta(x_t-\bar x)$ with unknown $\beta$, learning about the slope depends on the predictor’s position. A positive return surprise raises the slope estimate when $x_t>\bar x$ and lowers it when $x_t<\bar x$. If predictors are imperfect proxies for the latent expected return, filtering also uses past returns and potentially dividends. The review does not supply a universal predictor list, initialization, fitted transition parameters, or out-of-sample validation schedule.

## Horizon risk and portfolio choice

Parameter uncertainty creates dependence in predictive returns even if returns are independent conditional on the parameter. For a constant unknown mean $\mu$, known innovation variance $\sigma^2$, and the sum of $k$ future returns,

$$
\operatorname{Var}_t\left(\sum_{j=1}^{k}r_{t+j}\right)
=k\sigma^2+k^2\operatorname{Var}_t(\mu).
$$

The first term is expected conditional variance; the second is variance of the conditional mean $k\mu$. Per-period predictive variance is $\sigma^2+k\operatorname{Var}_t(\mu)$, which grows with horizon. This result concerns additive returns under the stipulated model, not the variance of compounded terminal wealth. With time-varying means, mean reversion and uncertainty compete; the review’s discussion of higher long-horizon risk is not a theorem for every predictive process.

For known constant excess-return mean and volatility, the unconstrained myopic risky share is $\pi_{\mathrm{myopic}}=\mu/(\gamma\sigma^2)$, where $\gamma$ is relative risk aversion. The review uses annual inputs $\mu=7\%$ and $\sigma=16\%$: risky shares are approximately 273%, 91%, and 55% for $\gamma=1,3,5$. The first is leveraged; these are model allocations without borrowing or position limits, not feasible holdings imposed on every household.

With learning, the posterior mean is a state variable. Write $V(W,\widehat\mu,t)$ for the dynamic value function; the review denotes its wealth derivative by $U_W$. Equation (13), p. 371, gives the hedging component

$$
\pi_{\mathrm{hedge}}=
-\rho_{\widehat\mu,r}\frac{\sigma_{\widehat\mu}}{\sigma}
\frac{V_{W\widehat\mu}}{W V_{WW}}.
$$

The leading minus sign is essential. In the discussed power-utility setting with $\gamma>1$, $V_{WW}<0$ and $V_{W\widehat\mu}<0$. Learning a constant mean produces positive correlation between return news and mean revisions, making this hedging demand negative. A short position relative to the myopic allocation pays off when disappointing returns also reduce expected future opportunities and increase marginal utility. Solving the allocation still requires the dynamic value function, investment horizon, and boundary conditions; substituting the posterior mean into the myopic rule omits this hedge.

The review reports a Brennan (1998) example with mean estimate 8.5%, prior mean uncertainty 4.5%, return volatility 14%, risk aversion four, and a twenty-year horizon: learning reduces the allocation to 56%, compared with a reported 102% myopic allocation. There is a numerical inconsistency in the review: its displayed myopic formula and quoted inputs yield $0.085/[4(0.14)^2]\simeq108.4\%$, not 102%. The note preserves the reported comparison but does not present it as exactly reproduced; the original calibration must resolve the discrepancy.

Discrete-time Bayesian portfolio analysis instead often integrates parameter uncertainty into the predictive distribution:

$$
p(R_{t+k}\mid\mathcal F_t)=\int p(R_{t+k}\mid\theta,\mathcal F_t)
p(\theta\mid\mathcal F_t)\,d\theta.
$$

Expected utility is evaluated under this mixture. Drawing one parameter vector for each simulated future path preserves dependence from shared uncertain parameters; independently redrawing a supposedly fixed mean each period would remove the $k^2$ uncertainty term. This implementation implication follows from the model. A one-period predictive optimization does not automatically reproduce a dynamic learning hedge, because future decisions and the value of information must also enter the optimization.

## Learning about skill and endogenous selection

The mutual-fund example combines unknown manager ability, decreasing returns to scale, and competitive capital provision. Strong performance raises estimated skill and attracts money. Inflows continue until capacity costs remove the expected abnormal return available to investors. Consequently, performance-sensitive flows coexist with weak future net-performance persistence. Younger funds have shorter histories and higher uncertainty, so the same new evidence moves beliefs and flows more. Anticipated strategy changes after poor performance can make bad past returns less informative than good returns and produce a convex flow-performance relation.

Related manager-replacement models predict outflows and higher risk before replacement, followed by inflows and lower risk afterward. This is an account of endogenous capital and personnel decisions, not a rule to buy every recently successful fund. It requires a capacity function and a model of what investors observe, neither of which is numerically specified in this review.

Individual investors may accept expected short-run trading losses to learn about their ability. Success raises posterior ability and subsequent trade size; poor results reduce trading or induce exit. Better average performance among active survivors can arise from selection. Learning about fixed ability must be separated from learning by doing, where experience changes ability itself. The review describes empirical support without supplying trader-level sample filters or a calibrated trading-cost schedule.

Learning alone also does not defeat the no-trade logic of common-prior, purely informational settings. Volume models add heterogeneous information together with hedging needs, or different priors or interpretations. In the reviewed asymmetric-information model, hedging trades tend to be associated with return reversals, whereas speculative trades are associated with continuation. Inferring this mechanism from volume requires distinguishing motives rather than treating every trade as information acquisition.

IPO timing provides a particularly specific selection prediction. A firm goes public when expected profitability crosses a threshold. Reaching that threshold requires positive profitability surprises, so realized profitability at the IPO exceeds expected profitability and subsequently tends to decline. The decline is larger with noisier profitability signals and lower prior uncertainty: either condition reduces the Bayesian gain, requiring a more extreme realized signal to move the posterior across the threshold. Earnings-announcement price reactions help distinguish signal volatility from parameter uncertainty; weak reactions predict larger post-IPO profitability declines in the cited evidence.

For venture capital, investing generates both cash returns and information useful for later investments, creating an exploration-versus-exploitation decision. Asymmetric learning can also sustain performance persistence. Incumbent limited partners learn more about a general partner than outsiders; their refusal to reinvest would be a negative signal. This gives incumbents bargaining power and allows high net returns in subsequent funds, unlike the public mutual-fund setting where competitive inflows dissipate investor surplus. The reviewed predictions include higher incumbent returns in follow-on funds and persistent investor composition.

## What can and cannot be replicated from this review

The elementary normal filter, conditional-mean state-space example, additive horizon-variance decomposition, and myopic allocation arithmetic are reconstructible from the equations and declared assumptions. The appendix’s valuation calculation is reconstructible only after checking integrability; its quoted truncated-normal volatility example needs an additional restriction. The dynamic hedge has a precise form, but the review does not provide the full control problem and numerical solver for each cited application.

For empirical applications, the review reports selected magnitudes and mechanisms, not raw data, complete estimation code, sampling exclusions, standard-error procedures, trading implementation, or robustness tables. A replication must return to the original study for those inputs. It should retain point-in-time information, separate calibration targets from validation outcomes, and compare competing mechanisms on predictions beyond the fact used to motivate the model. The authors’ most useful standard is that an attractive learning explanation must deliver both discriminating predictions and effects of the right economic magnitude.
