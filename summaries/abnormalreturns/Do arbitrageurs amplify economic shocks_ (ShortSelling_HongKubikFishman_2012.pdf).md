# Do arbitrageurs amplify economic shocks?

**Harrison Hong, Jeffrey D. Kubik, and Tal Fishman (2012).** *Journal of Financial Economics* 103, 454–470. DOI: 10.1016/j.jfineco.2011.10.007. Source: [original PDF](../../Finance/ShortSelling_HongKubikFishman_2012.pdf). This note covers all 17 PDF pages, including the theoretical appendix; page references below are printed journal pages. The separate robustness web appendix mentioned in Section 4.8 is not contained in this source and its unreported estimates are not reconstructed here.

## Why this matters

A trader can correctly identify an overpriced security and nevertheless be forced to cover after favorable news. Covering adds demand precisely when the fundamental value has increased. The resulting price response can exceed the fundamental response, leaving an opportunity for a newly funded trader to short after the original trader has realized a loss. This distinction between the profitability of an idea and the survivability of a position is the paper's central contribution.

The authors turn that mechanism into three jointly testable predictions: heavily shorted stocks should react more strongly to earnings surprises; their turnover should react more strongly to the magnitude of those surprises; and good-news announcements should be followed by relatively worse returns when the stock was heavily shorted. The last prediction distinguishes temporary amplification from a simple explanation in which short interest identifies stocks whose earnings announcements reveal more information.

This is primarily an event-study and mechanism paper. It does not deliver an optimized short portfolio, an execution model, or a borrow-cost-adjusted trading strategy. Its practical relevance is to event risk and funding resilience: a favorable reassessment of a company's value need not make an existing short position safe to hold, even if the remaining overvaluation becomes larger. The empirical design also illustrates why response slopes and interactions can be more informative than comparing average returns of highly and lightly shorted stocks.

## The constrained-arbitrage model

Section 2, pp. 457–458, considers one stock with unit net supply and three dates, $t=0,1,2$. At date 2 the stock pays $v$, which is either $\underline v$ or $\overline v$ with equal probability. At date 1 everyone learns the realization. Thus uncertainty about the eventual cash payment disappears before liquidation. Let $\mu=E_0[v]=(\underline v+\overline v)/2$ and let $p_t$ be the stock price.

There are optimistic noise traders and risk-neutral arbitrageurs. Initial noise-trader sentiment is $S>0$; after the announcement it is $S(v)$; by date 2 it disappears. The specified demands, measured in shares, are

$$
Q_0^N=\frac{\mu+S}{p_0},\qquad Q_1^N=\frac{v+S(v)}{p_1}.
$$

These are demand schedules rather than utility-derived optimal demands. Optimistic investors commit a dollar amount equal to their perceived value. Arbitrageurs partially offset them by selling short. In the main-text simplification all initial arbitrage capital $F_0$ is put at risk, with $F_0<S$, giving $Q_0^S=-F_0/p_0$. At date 1 they again use available capital, so $Q_1^S=-F_1/p_1$, provided $F_1(v)\le S(v)$. These inequalities keep the analysis in the region where arbitrage capital cannot eliminate overpricing.

The crucial feedback rule is equation (5):

$$
F_1(v)=F_0+aF_0\left(1-\frac{p_1(v)}{p_0}\right),\qquad a>1.
$$

A price increase generates a short loss and reduces deployable resources; a price decline increases resources. The coefficient $a$ summarizes the sensitivity of capital to position performance. Margin constraints, internal risk limits, performance-driven redemptions, and related mechanisms can all motivate such feedback, but the paper does not separately identify them or derive $a$ from an explicit financing contract. The symmetric capital response is an assumption with empirical consequences: successful shorts receive additional capacity, rather than merely retaining their original capacity.

Market clearing, $Q_t^N+Q_t^S=1$, gives equations (7)–(8):

$$
p_0=\mu+S-F_0,
\qquad
p_1(v)=\frac{v+S(v)-F_0(1+a)}{1-aF_0/p_0},
\qquad p_2=v.
$$

The denominator exposes the amplification. Define $k=(1-aF_0/p_0)^{-1}$. Within the economically admissible constrained region, $k>1$. Holding initial conditions fixed,

$$
\frac{dp_1}{dv}=k\{1+S'(v)\}.
$$

The initial short ratio is $F_0/p_0$ because net shares outstanding are normalized to one. A larger initial short position increases the strength of the capital-price feedback. A simulator must nevertheless check positive prices, nonnegative remaining capital, the residual-overpricing restrictions, and a positive denominator. One cannot extrapolate this branch through its singularity or assume it describes arbitrageurs with unlimited capital. The paper does not provide a universally admissible numerical parameter grid.

The earnings-response coefficient is a finite response from the initial expectation, not simply the local derivative:

$$
\beta(v)=\frac{(p_1-p_0)/p_0}{(v-\mu)/p_0}
=\frac{p_1-p_0}{v-\mu}.
$$

Normalizing both the price change and the earnings innovation by the same previous price makes the cancellation explicit. In empirical work earnings per share are only a proxy for the fundamental innovation in this stylized one-payment economy.

## Endogenous initial exposure and the limits of the propositions

The appendix, pp. 468–470, permits arbitrageurs to commit $D_0\le F_0$ initially and leave the remainder in cash with zero net return. This allows a trader to reserve capacity for a better opportunity after the announcement. Initial price becomes $p_0=\mu+S-D_0$, and the feedback rule uses the initial amount exposed to the short:

$$
F_1(v)=F_0+aD_0\left(1-\frac{p_1(v)}{p_0}\right),
\qquad
p_1(v)=\frac{v+S(v)-F_0-aD_0}{1-aD_0/p_0}.
$$

At date 1 the remaining opportunity is certain in the model, so available resources are deployed against overpricing.

The paper writes the terminal-wealth objective as

$$
\max_{0\le D_0\le F_0}\frac12F_1(\underline v)
\left(2-\frac{\underline v}{p_1(\underline v)}\right)
+\frac12F_1(\overline v)
\left(2-\frac{\overline v}{p_1(\overline v)}\right).
$$

The factor $2-v/p_1$ includes both capital and the gain from a fully funded short. Equation (17) states the corresponding marginal optimality condition as the probability-weighted sum of $(1-p_1(v)/p_0)(2-v/p_1(v))$. A positive marginal value leads to the upper boundary $D_0=F_0$; an interior solution requires equality to zero. The condition is part of an equilibrium in which prices and capital must also satisfy the clearing equations. For implementation, it should not be read as an unconstrained instruction to differentiate a monopolist's price impact: the arbitrageurs are price takers, and equilibrium prices are determined consistently afterward.

The appendix rewrites the response coefficient as

$$
\beta(v)=k\left[1+\frac{S(v)-S-(F_0-D_0)}{v-\mu}\right],
\qquad k=(1-aD_0/p_0)^{-1}.
$$

This shows why cash retention matters. The conclusion that more shorting means greater amplification is local to insufficient-capital economies; it is not a global monotonicity theorem covering the transition to complete arbitrage. The proof compares more and less shorted assets with uniformly shifted sentiment levels so that $S(v)-S$ remains fixed. For small capital, $D_0=F_0$ and increasing initial exposure raises $k$. With enough capital prices approach fundamentals and the response coefficient returns to one. The appendix therefore invokes a threshold below which its comparison holds without supplying an empirically estimated threshold.

Proposition 2 connects news to trading. Good news raises price and reduces capital, lowering the post-event short ratio $F_1/p_1$; bad news can increase it. Because there are only two investor types, turnover in the model equals the absolute change in the short position. In real markets total share turnover includes numerous other motives, making that equality an identification assumption that cannot be carried literally into the data.

Proposition 3 predicts increased attractiveness of shorting after favorable news under increasing sentiment. Its proof uses $dp_1/dv=k(1+S'(v))>1$. A mathematical qualification is necessary when translating that argument into percentage returns: increasing the dollar gap $p_1-v$ does not alone establish that the ratio $p_1/v$ rises. The latter requires $vp_1'(v)>p_1(v)$. The appendix's stated equivalence between the ratio argument and a slope above one is therefore stronger than generally follows without further normalization or restrictions. The observed post-event return reversal is an empirical finding; this note does not treat the brief proof as a general theorem for arbitrary sentiment schedules.

## Data construction and event timing

Section 3 describes quarterly observations of NYSE, Amex, and Nasdaq stocks from 1994 through 2007. The main regressions contain 119,785 observations. A record is dropped if short interest, earnings, or analyst forecast information is missing, or if the announcement falls outside 30–90 calendar days after the fiscal period ends. The resulting sample is consequently an analyst-covered, data-complete subset of listed firms.

Monthly short positions come from Bloomberg and Nasdaq and refer to positions closed on the first business day on or after the fifteenth. Short interest is divided by CRSP shares outstanding on that date. Each quarter, `HISR` identifies the top 33% of the short-ratio distribution in the eligible sample; the other two thirds form the comparison group. The overall mean short ratio is 3.44%, its standard deviation is 4.80%, and the high-short group's mean is 7.46%. The source describes the monthly convention but does not provide an entirely explicit date-join rule for matching the announcement to the last observable short-interest release. A replication must document that rule and avoid using a position observation or publication available only after the event.

I/B/E/S summary files provide actual initial, unadjusted earnings and the consensus forecast from the last month before the announcement. Unexpected earnings are actual minus forecast, divided by a prior stock price. `UEHIGH` is the top quarterly tercile of this surprise. For the turnover tests, `ABSUEHIGH` is the top tercile of its absolute value. For asymmetric tests, `UELOW` is the bottom tercile of signed surprise. These are discrete group comparisons; their coefficients are not slopes per one dollar of earnings news. The paper explicitly specifies a price lag of 21 days for the P/E control but is less explicit about the exact prior-price date used in the surprise denominator.

Daily returns, trading volume, market capitalization, and shares outstanding come from CRSP. Benchmark-adjusted returns use 18 portfolios formed from two size groups, three book-to-market groups, and three momentum groups, with Fama–French-style breakpoints. Equation (10) is an arithmetic cumulative abnormal return:

$$
CAR_i[t_0,t_1]=\sum_{j=t_0}^{t_1}(R_{ij}-R^{bench}_{ij}).
$$

The announcement is trading day zero. `CAR` uses days $[-1,+1]$; `POSTCAR` uses $[+2,+126]$. For firms disappearing before day 126, the authors use available returns and the delisting return. This is not a compounded buy-and-hold abnormal return. The exact momentum formation window, benchmark weighting, and complete portfolio-reconstitution conventions are not fully restated in the article; reproducing its cited benchmark methodology requires those additional choices.

Share turnover is daily volume divided by shares outstanding, averaged over $[-1,+1]$. Nasdaq volume is divided by 2 before February 1, 2001; by 1.8 from that date through December 2001; and by 1.6 during 2002–2003. From 2004 it is unadjusted. `ABNTURN` subtracts the firm's average announcement-window turnover over the whole sample. This full-sample demeaning is appropriate to reproducing the retrospective event study but is not a real-time trading feature. Table 1 gives abnormal-turnover standard deviation 1.40 percentage points, event-CAR standard deviation 8.22 points, and POSTCAR standard deviation 31.41 points.

Annual accounting controls come from CRSP/Compustat: book equity item 60, convertible securities item 39, EPS item 57, and fiscal-year-end price item 199. P/E uses price 21 days before the release over previous annual EPS. Daily CRSP returns supply previous-month volatility. Analyst disagreement follows the dispersion construction cited to Diether, Malloy, and Scherbina. The article does not provide code or a complete point-in-time accounting-vintage protocol, so the published variable list alone is insufficient to guarantee an identical historical database join.

## Estimation architecture

For the main return test, estimate

$$
CAR_{iq}=\alpha+b_1UEHIGH_{iq}+b_2HISR_{iq}
+b_3UEHIGH_{iq}HISR_{iq}+X_{iq}'\gamma+\varepsilon_{iq}.
$$

Controls include 25 quarterly size-category indicators, 25 positive-P/E categories plus a negative-earnings indicator, 25 analyst-disagreement categories, a positive-convertible-debt indicator, 25 previous-volatility categories, two-digit SIC industry indicators, exchange indicators, and quarter effects. This flexible discretization matters: replacing it with linear controls changes the estimated specification.

The paper then interacts the main firm characteristics with `UEHIGH`, allowing other characteristics to affect the news-response slope. Industry, exchange, and quarter indicators are excluded from this additional interaction block. Further specifications use stock fixed effects and industry-by-quarter effects. Standard errors are clustered by stock. They account for serial dependence within a firm, but the reported design does not separately cluster contemporaneous dependence across firms or the overlapping six-month post-event windows.

There is a source inconsistency worth preserving for a reproducer. The prose describes columns 7–9 as replacing stock fixed effects with industry-by-quarter effects; the printed tables label stock effects “Yes” in those columns as well. Both constructions should be kept distinct in replication records until author code resolves the difference. Reporting either interpretation as unambiguous would conceal a material specification uncertainty.

For turnover, replace the dependent variable with `ABNTURN` and the surprise indicator with `ABSUEHIGH`. For post-event performance, replace the dependent variable with `POSTCAR` while retaining signed `UEHIGH`. The central coefficient $b_3$ is always a difference in response across short-interest groups, conditional on the specified controls. A negative level effect of `HISR` is conceptually different from this interaction.

## Main empirical results

Table 2's simple interaction specification estimates a 3.27-percentage-point event-CAR effect of high surprise for lower-short-interest stocks and an additional 0.55 points for heavily shorted stocks. The interaction standard error is 0.12, giving a $t$ statistic near 4.6. Thus the estimated conditional high-surprise contrast is 3.82 points in the high-short group, approximately 17% larger than 3.27. These are regression contrasts relative to non-high-surprise observations, not unconditional mean announcement returns.

Adding characteristic-by-news interactions reduces the incremental response to 0.33 points, standard error 0.13. With stock fixed effects the simpler interaction is 0.79, standard error 0.13; with the additional interaction controls it is 0.56, standard error 0.14. The final industry-quarter specifications report 0.53 and 0.30, each with standard error 0.13. The amplification pattern survives flexible controls, although the magnitude changes materially with specification.

Table 3 produces the turnover counterpart. Without stock fixed effects, high absolute surprise adds 0.104 percentage points of turnover for the low-short group and another 0.075 points for the high-short group, standard error 0.023. The resulting 0.179-point response is about 72% greater. With stock effects, the corresponding coefficients are 0.090 and 0.111, with interaction standard error 0.026; the relative increase is about 123%. Fully interacted specifications give incremental responses of 0.087 and 0.112. These findings support additional event trading but do not directly observe which transactions close shorts.

Table 4 examines subsequent returns. The baseline low-short high-news contrast is +1.57 percentage points; the high-short interaction is −2.67, standard error 0.50. Their sum is −1.10, with reported test $p=0.01$. With stock effects, the coefficients are +0.82 and −2.06, producing −1.24 points. With industry-quarter controls, they are +1.65 and −2.52, producing −0.87 points, reported $p=0.04$. Adding characteristic-news interactions reduces the incremental negative effect to −1.90, −1.25, and −1.80 across the respective specifications.

The sum of the high-news main effect and interaction is the high-news contrast within the high-short group. It is not, by itself, the total expected post-event return of that group because intercepts, fixed effects, the high-short level effect, and controls also contribute. Nor is its negative value a demonstrated net short-trading profit after borrowing and execution costs. This distinction is important when using the reported 110-basis-point figure.

## Good-news versus bad-news asymmetry

Table 5 introduces both top- and bottom-tercile surprise indicators and their interactions with `HISR`, using the middle tercile as the surprise reference group. With stock effects, the event-CAR interactions are +0.46 for high surprise, standard error 0.14, and −0.55 for low surprise, standard error 0.14. Their absolute magnitudes are similar. The turnover interactions are +0.078 and +0.090, with standard errors 0.038 and 0.043. Both large positive and large negative news therefore bring extra activity in heavily shorted names.

The post-event interactions differ: −2.21 points after high surprise, standard error 0.57, versus −0.23 after low surprise, standard error 0.55. The latter is imprecise and close to zero. The authors reject equality of the relevant signed magnitudes at $p=0.05$. This combination fits the proposed funding asymmetry in outcomes: losing shorts must cover after good news, whereas winning shorts can maintain or expand exposure after bad news.

The joint evidence is harder to explain with a pure information-resolution account than the announcement coefficient alone. Nevertheless, earnings surprises, short interest, and investor beliefs are not randomly assigned. Analyst disagreement and fixed effects only partially address omitted information. A sufficiently rich alternative involving time-varying beliefs or correlated trading could still generate some of these patterns.

## The two supporting comparisons

The first comparison exploits historically looser short-sale restrictions on Nasdaq than on NYSE/Amex before decimalization. The sample is restricted to the top and bottom terciles of short interest and surprise within quarter and exchange, and regressions add Nasdaq indicators and all relevant lower-order terms around the triple interaction. There are 27,066 observations. The narrative places this exercise before 2001 within the 1994-start main sample, while Table 6 labels its period 1993–2000; this discrepancy remains unresolved in the supplied article.

The Nasdaq triple interaction is +1.40 points for event CAR, standard error 0.43, and −4.93 points for POSTCAR, standard error 1.90. Its turnover counterpart is only +0.012, standard error 0.052. Thus the return evidence supports the mechanism, but the turnover comparison is essentially uninformative. An unreported preliminary regression finds Nasdaq listing raises the probability of high short interest by 7.9 percentage points, with $t\approx6.6$. Exchange listing is not randomized, so this is a regulatory comparison with remaining exchange-composition confounding, not a clean isolated treatment.

The second comparison concerns the growth of shorting in smaller stocks after 2001. Figure 1 shows small-stock short ratios rising steeply toward approximately 9% in 2007 while large-stock ratios remain around 2–3%. The text defines small firms using the bottom five NYSE size deciles and large firms using deciles eight through ten, excluding the intermediate group. Table 7 instead describes small firms as below the fortieth percentile and large firms above the seventieth. The large-firm conventions are compatible; the small-firm convention requires clarification.

Separate regressions for 24,781 small-stock and 17,274 large-stock observations interact high surprise, high short interest, and an after-2001 indicator. Event-CAR triple interactions are +0.38 for small firms and −0.48 for large firms, both with standard error 0.48. POSTCAR estimates are −0.33 and +0.61 with standard errors 2.11 and 1.75. Turnover estimates are +0.109 and +0.139, with standard errors 0.082 and 0.095; their relative ordering does not support the proposed small-stock channel. These estimates are weak and should be characterized as suggestive patterns, rather than strong confirmation of hedge-fund-driven amplification.

## Reproduction priorities and practical limits

A faithful reconstruction starts with the event panel and its timing, not a trading backtest. Preserve initial I/B/E/S earnings, construct the quarterly eligible population before percentile cutoffs, join genuinely pre-event short-interest information, implement the Nasdaq volume adjustments, and keep arithmetic benchmark-adjusted return windows distinct from compounded returns. Then reproduce the baseline, interaction-rich, firm-effects, and industry-quarter variants separately and report their sample counts. The main 119,785-observation target and the descriptive moments provide useful diagnostics of incorrect database joins.

The model and evidence leave several inputs open. There is no estimated $a$, no fitted sentiment schedule, no borrowing-fee series, no direct observation of daily short covering, and no complete point-in-time release-lag specification. The paper mentions calibration ranges of 10–30% extra response using an approximately 8% short ratio, but the detailed calculation is available only on request. It would be inappropriate to turn that range into a uniquely calibrated structural model.

For an implementation extension, directly identified cover trades, actual borrow availability, recall risk, event-time spreads, and financing constraints would be needed to decide whether post-news shorts are executable. Such an extension should also test common-date dependence and overlapping-window inference. These are proposed improvements, not reported robustness results. The source itself establishes a historical conditional pattern consistent with constrained arbitrage: existing sophisticated positions can contribute to temporary price amplification even while their holders are trying to trade against initial overvaluation.
