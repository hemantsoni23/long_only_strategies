# Comparing Asset Pricing Models
**Authors:** Francisco Barillas, Jay Shanken
**Year:** 2018
**Journal/Venue:** Journal of Finance
**Source file:** Finance/AbnormalReturnsReview_BarillasShanken_2018a.pdf (accepted-manuscript version)

## Question

GRS-type tests say whether a single model is rejected on a chosen set of test assets; large-sample models are "rejected" routinely, and a high p-value may reflect imprecise alphas rather than adequacy. The paper asks how to compare many nested and nonnested traded-factor models *simultaneously* and assign each a posterior probability, in the spirit of "it takes a model to beat a model."

## Contributions

1. A closed-form Bayesian version of the GRS test (posterior probability of $\alpha=0$ as a function of the GRS statistic), with an economically calibrated prior on alpha and an extension to *approximate* nulls.
2. A model-comparison procedure over all subsets of a candidate set of traded factors, exploiting "test-asset irrelevance" (Barillas-Shanken 2017, "Which alpha?").
3. An extension to *categorical factors* (alternative versions of the same construct), and one in which the market is not forced into every model.
4. Empirics on 10 factors, 1972-2015: the top model is $\{Mkt, SMB, ROE, IA, HML^m, UMD\}$; FF5 and HXZ-q are dominated.

## Setup and the Bayesian test

Time-series regression for $N$ test assets on $K$ traded factors over $T$ months:
$$r_t = \alpha + \beta f_t + \varepsilon_t,\qquad \varepsilon_t \sim N(0,\Sigma)\ \text{i.i.d. given } f.$$
GRS: $F = \tfrac{T-N-K}{NT}W$, with
$$W = T\,\frac{\hat\alpha'\hat\Sigma^{-1}\hat\alpha}{1+Sh^2(f)} ,\qquad \hat\alpha'\hat\Sigma^{-1}\hat\alpha = Sh^2(f,r) - Sh^2(f),$$
i.e. the test asks whether adding the assets raises the maximum squared Sharpe ratio.

**Prior.** Diffuse (Jeffreys) prior on $\beta,\Sigma$; under the alternative $\alpha\mid\beta,\Sigma \sim N(0, k\Sigma)$. Proportionality to $\Sigma$ follows Pastor-Stambaugh / MacKinlay and APT bounds (Dybvig; Grinblatt-Titman): large alphas only where residual risk is large, so implausibly large Sharpe ratios get little mass. Since $\alpha'\Sigma^{-1}\alpha/k \sim \chi^2_N$, the prior expected increment to $Sh^2$ is $kN$, so $k$ is set from a target $Sh_{\max}$:
$$k = \frac{Sh_{\max}^2 - Sh^2(f)}{N}.$$
Example: CAPM test, $Sh_{\max} = 2\times 0.115$, $N=10$ gives $k = (2^2-1)(0.115^2)/10 \approx 0.004$.

A diffuse prior on alpha is not available: $k\to\infty$ implies infinite expected Sharpe ratio and, via Bartlett's (Lindley's) paradox, pushes the Bayes factor toward the null. The authors also criticize the training-sample priors of Avramov-Chao (2006) as potentially implying implausibly wide alpha dispersion.

**Proposition 1.** Marginal likelihoods are closed form; the Bayes factor for $H_0$ vs $H_1$ is
$$BF = \left(\frac{|S|}{|S_R|}\right)^{T/2}\Big/ Q,$$
with $S, S_R$ the unrestricted/restricted OLS residual cross-product matrices and $Q\in(0,1)$ an explicit function of $W$, $k$ and $Sh^2(f)$. For an approximate null with prior scale $k_0<k$, $BF = Q_{k_0}/Q_k$. $BF$ is decreasing in $W$. The formula coincides with Shanken's (1987b) Bayes factor computed by conditioning only on the F-statistic, so that shortcut loses no information under these priors.

## Relative vs absolute tests; test-asset irrelevance

Let model $M = \{Mkt, f\}$, excluded factors $f^*$, and $M^a$ the all-factor model. **Result** (Barillas-Shanken 2017): $M$ holds iff $f^*$ has zero alpha on $(Mkt,f)$ *and* $r$ has zero alpha on all factors. The test-asset restriction is common to every model, so it cancels.

**Proposition 2** (nested): $BF_M^{abs} = BF_{M\,vs\,M^a} \times BF_{M^a}^{abs}$, i.e. relative support can be backed out of absolute tests and is unaffected by the test assets.

**Proposition 3** (general): with independent priors across the blocks,
$$ML(M) = ML_U(f\mid Mkt)\times ML_R(f^*\mid Mkt,f)\times ML_R(r\mid Mkt,f,f^*),$$
and the last term is identical across models. Posterior probabilities are $P(M_j\mid D) = ML_j P(M_j)/\sum_\ell ML_\ell P(M_\ell)$ with uniform model priors. Two features distinguish this from Avramov-Chao and from "highest Sharpe ratio wins":
- excluded factors enter as left-hand-side assets, so all models are conditioned on the same data;
- the *unrestricted* term rewards a model only if its included factors actually raise the Sharpe ratio relative to the prior; redundant factors are penalized, so parsimony is built in.

Implementation details: $k$ is chosen so that the six-factor $Sh_{\max}$ is a multiple of $Sh(Mkt)$, with each added factor contributing an equal expected increment to $Sh^2$ (so $Sh_{\max}$ increases concavely); the count of nuisance parameters is $K(K+1)/2-1$ for every model, which justifies using the same improper-prior constants (a more elaborate permutation-based variant in the Internet Appendix gives nearly identical probabilities). An extension randomizes the "anchor" factor so that Mkt need not be included.

**Warm-up (FF3, 1972-2015):** $\{Mkt,HML\}$ 60%, FF3 39%, CAPM and $\{Mkt,SMB\}$ share 1%. HML alpha on Mkt is 5.50%/yr ($t=3.69$); SMB alphas are small ($t\approx1$).

## Categorical factors

Several factors are versions of the same idea. Models may contain at most one version per category: size (SMB, ME), value (HML, $HML^m$), profitability (RMW, ROE), investment (CMA, IA). Each "version" $w$ of the full factor set gets equal prior weight; models within $w$ uniform. The alternative versions $w^*$ are priced as an extra restricted block, $ML(M\mid w) = ML_U(f\mid Mkt)\,ML_R(f^*\mid Mkt,f)\,ML_R(w^*\mid Mkt,f,f^*)$, and (Proposition C1) $P(M\mid F) = E_{w\mid F}[P(M\mid w,F)]$ with $P(w\mid F)\propto E_{M\mid w}[ML(M\mid w)]$. This splits a categorical model's prior mass evenly among its versions rather than letting near-duplicates crowd out parsimonious models. Illustration with SMB/ME (correlation 0.98): $\{Mkt,HML\}$ 55.6%, $\{Mkt,HML,Size\}$ 43.4%.

## Main empirical results (10 factors, Jan 1972 - Dec 2015)

Factors: Mkt, SMB (FF5 version), HML, RMW, CMA, UMD, ME, IA, ROE (HXZ), $HML^m$ (Asness-Frazzini, book-to-market with the latest monthly price). ROE uses the most recent quarterly earnings over one-quarter-lagged book equity; FF's RMW uses annual $t-1$ data. 162 models (32 categorical models). $Sh(Mkt)=0.113$ monthly; the top model's in-sample Sharpe ratio is 0.51 (4.5x market). Baseline prior: six-factor $Sh_{\max}=1.5\,Sh(Mkt)$ ("risk-based tilt").

**Top individual models** (posterior %, by prior multiple 1.25 / 1.5 / 2 / 3):

| Model | 1.25 | 1.5 | 2 | 3 |
|---|---|---|---|---|
| Mkt SMB ROE IA HMLm UMD | 24.8 | 38.5 | 46.8 | 50.0 |
| Mkt SMB ROE CMA HMLm UMD | 10.5 | 14.8 | 16.3 | 16.2 |
| Mkt ME ROE IA HMLm UMD | 11.0 | 13.7 | 13.4 | 12.2 |
| Mkt ROE IA HMLm UMD | 17.5 | 13.7 | 9.3 | 8.0 |

The top model has ranked first since 2000. All top seven models contain ROE, $HML^m$ and UMD. Cumulative factor probabilities: ROE and $HML^m$ near 1, UMD about 97%.

**Categorical models:** {Mkt Size Prof Inv Val Mom} 72.8% at baseline (53.0 to 82.4% across priors); the version without size is second (20%). Within-category shares: $HML^m$ 99.5%, ROE 99.4%, SMB 73.5%, IA 72.0%. Even in the categorical FF5 model, the $HML^m$ share is 84% and ROE 99.9%: timeliness, not the category list, is what separates FF5 from the winners.

**Direct tests** (50/50 prior on two models): top six-factor model vs HXZ-q: 96.1%; vs FF5: above 99%, even dropping SMB from the six-factor model.

**Value and momentum redundancy.** Alphas of each top-model factor on the other five: $HML^m$ 5.59%/yr ($t=5.10$), UMD 6.44% ($t=4.05$), SMB 4.7% ($t=3.0$). Standard HML on {Mkt SMB ROE IA UMD} has alpha 0.95% ($t=0.81$), reproducing the HXZ/FF finding that HML is redundant. The mechanism is correlation with momentum: $\rho(HML^m,UMD)=-0.65$ vs $-0.17$ for HML, so hedging momentum raises $HML^m$'s alpha. Bayesian redundancy probability for $HML^m$ falls quickly to zero as the prior multiple rises; getting even a 25% Sharpe increase over the five-factor 0.42 would require $\sigma_\alpha\approx7.5\%$/yr. UMD is non-redundant when $HML^m$ is present, but on {Mkt SMB IA ROE} the posterior probability of UMD redundancy is always above 50% (above 80% near multiple 1.2; classical p-value above 0.35). So "momentum is redundant" (HXZ) and "value is redundant" (FF5, HXZ) are artifacts of using stale-price HML.

As the prior multiple rises, the SMB alpha becomes more consistent with the alternative, so the size-inclusive model gains probability at the expense of the size-free one.

## Out-of-sample checks

Full-sample Sharpe ratios: top three models about 0.48; HXZ 0.38 (best benchmark). Selection over the first $T/2$ or $2T/3$ of the data, evaluated on the remainder: with in-sample tangency weights re-estimated in the performance period, estimation-period Sharpe ratios of the top three are about 0.8 but fall OOS to about 0.37 for the second-ranked model and FF5, with HXZ and the other top models close behind ($T/2$); with $2T/3$, FF5 0.37 vs top model 0.31 (difference insignificant, p = 0.39). With estimation-period weights applied out of sample (implementable), all ratios are below 0.30 and the top models, HXZ and FF5 are roughly tied. The authors conclude that high-probability models perform well out of sample, but so do HXZ and FF5; in-sample selection bias in Sharpe ratios is acknowledged.

## Absolute tests of the top model

- 25 size/momentum portfolios: mean $|\alpha|=1.65\%$/yr, GRS 3.32 ($p\approx1.9\times10^{-7}$); Bayesian null probability essentially zero for multiples up to 2.
- 25 book-to-market/investment portfolios: mean $|\alpha|=2.57\%$, GRS 3.21 ($p\approx4.5\times10^{-7}$; lower GRS despite larger alphas because residual variance is higher). The null probability rebounds for large multiples and tends to 1 as the multiple goes to infinity (Bartlett's paradox), underscoring that the prior scale must be chosen deliberately.
- Approximate null with $\sigma_{\alpha_0}=1\%$/yr (expected |deviation| about 0.8%, about 6% higher Sharpe than the exact null): no zero-probability region; even odds at a multiple of about 1.6; 95% posterior confidence that the approximate model is false only for multiples roughly 1.15-1.45.

## Assessment

- **Convincing:** the test-asset irrelevance argument is clean and practically important: for traded factors, model comparison is entirely about spanning among the candidate factors, so disputes over which test portfolios to use are beside the point for *relative* ranking. The closed-form Bayes factor makes the method cheap to run over hundreds of models. The $HML^m$/UMD correlation explanation for the redundancy reversals is a concrete, checkable mechanism.
- **Fragile or limited:**
  - Results depend on the candidate universe (10 factors); probabilities are relative to that menu, and the menu itself was chosen after these factors were published (the authors flag data mining, citing Harvey-Liu-Zhu).
  - The prior scale matters: rankings are fairly stable, but probabilities move a lot (top model 25% to 50%), and absolute tests are sensitive through Bartlett's paradox.
  - The model assumes i.i.d. normal returns with constant parameters; irrelevance holds under elliptical distributions, but time-varying betas and heteroskedasticity are not handled.
  - Uniform model priors plus the categorical structure are modeling choices; the Mkt anchor is conditioned on throughout.
  - In-sample Sharpe ratios near 0.5/month are gross of costs; $HML^m$, ROE and UMD have high turnover, and the OOS evidence does not separate the winners from FF5/HXZ.
- **Practical relevance for a quant PM:** a principled, cheap way to decide which factors in a risk/alpha model are redundant given the others, answering the question "what does factor X add to the tangency portfolio?" with a calibrated prior on Sharpe improvement. It also suggests including timely value (monthly-price B/M) together with momentum, and quarterly ROE, when building a parsimonious pricing benchmark. The sibling paper [Barillas-Shanken 2017, "Which alpha?"] supplies the irrelevance result; Barillas-Kan-Robotti-Shanken give the classical Sharpe-ratio comparison counterpart.
