# Medium Term Simulations of The Full Kelly and Fractional Kelly Investment Strategies

Leonard C. MacLean, Edward O. Thorp, Yonggan Zhao, and William T. Ziemba, working paper dated January 18, 2010. Source: [UniversalPortfolios_MacleanThorpZhaoZiemba_2010.pdf](../../Finance/UniversalPortfolios_MacleanThorpZhaoZiemba_2010.pdf). This note covers the supplied 19-page version, including its appendix and all numerical tables and figures. Page references use its printed pagination. It is distinct from the three-author survey *Good and Bad Properties of the Kelly Criterion* cited in its introduction.

## Why this matters

A strategy that maximizes long-run logarithmic growth can be uncomfortable over the actual horizon of an investor. The relevant distinction is between expected terminal currency, expected log wealth, the probability of exceeding a target, and the chance of a severe loss. These quantities need not rank position sizes in the same order. MacLean and coauthors illustrate their divergence by repeating simple favorable gambles and constant-proportion asset allocations over finite horizons.

The contribution is a set of simulation comparisons extending the much smaller experiments of Bicksler–Thorp and Ziemba–Hausch. It is not a new universal-portfolio theorem, a return-prediction model, or an empirical test of profitable market timing. The authors compare full and fractional Kelly, include overbetting in two experiments, and display terminal-wealth distributions and extreme paths rather than reporting only mean returns. One example allows leverage while remaining below its true Kelly exposure; another produces negative wealth. Their different behavior depends on return support and trading conventions, not just on whether an allocation is called leveraged.

The source's central practical lesson is supported by its tables: reducing exposure can greatly narrow terminal dispersion, and aggressive positions can create enormous right tails without improving expected logarithmic growth. Its Gaussian-return experiment, however, does not literally solve the expected-log problem printed in its appendix. That model has a positive probability of nonpositive one-period wealth for every positive risky weight. The note therefore distinguishes the useful finite-horizon sensitivity exercise from an exact claim about Kelly optimality in that specification.

## Common accounting and objective

Write $W_t$ for wealth immediately before decision $t+1$, starting from $W_0=1000$. A constant-fraction strategy rebalances after every realization. If its gross portfolio return is $G_{t+1}(f)$, wealth evolves as

$$
W_{t+1}=W_tG_{t+1}(f),\qquad
W_T=W_0\prod_{t=1}^TG_t(f).
$$

For independent identically distributed positive multipliers with finite log moments,

$$
\mathbb E\log W_T=\log W_0+Tg(f),\qquad
g(f)=\mathbb E\log G(f),
$$

$$
\operatorname{Var}(\log W_T)=T\operatorname{Var}(\log G(f)).
$$

Thus maximizing one-period expected log return also maximizes finite-horizon expected log wealth in this fixed-distribution, fixed-opportunity setting. A finite horizon does not change that particular optimizer. It changes the distribution of realized outcomes and can change the appropriate allocation when the objective is a target probability, a shortfall limit, or another utility function.

Expected terminal money is different:

$$
\mathbb EW_T=W_0[\mathbb EG(f)]^T.
$$

A favorable gamble can have increasing arithmetic expected wealth even after its log-optimal size has been exceeded. Similarly, $\exp(\mathbb E\log W_T)$ is a geometric center, not the arithmetic expectation and not automatically the median of a finite distribution. The paper sometimes uses growth informally across these objects. A replication should label each one explicitly.

The experiments are repeated draws from prescribed laws. There is no training/validation split, rolling forecast window, universe selection, signal lag, asset-entry filter, or portfolio turnover model. The risky allocation is restored each decision date using current wealth. The stochastic laws and sizing fractions are treated as known. The study does not estimate a Kelly fraction anew along each simulated path or propagate parameter-estimation uncertainty.

## Favorable discrete bets: exact specification

The first family uses five possible bets. Before each decision, select a bet with the probabilities in the second column below. Conditional on its type, its outcome is a win with the stated probability. The quoted odds $O$ are net winnings per unit staked: a successful unit stake returns principal plus $O$, while an unsuccessful stake is lost.

| Net odds $O$ | Probability of selecting type | Conditional win probability $p$ | Kelly stake $k$ |
|---:|---:|---:|---:|
| 1 | 0.10 | 0.570 | 0.140 |
| 2 | 0.30 | 0.380 | 0.070 |
| 3 | 0.30 | 0.285 | $0.14/3$ |
| 4 | 0.20 | 0.228 | 0.035 |
| 5 | 0.10 | 0.190 | 0.028 |

Every bet has expected gross payoff $p(O+1)=1.14$ on staked capital, or a 14% edge. Differentiating $p\log(1+kO)+(1-p)\log(1-k)$ gives

$$
k=\frac{p(O+1)-1}{O}=\frac{0.14}{O}.
$$

At Kelly fraction $f$, stake $fk$ of current total wealth; hold the remainder as non-interest-bearing cash. The multiplier is $1+fkO$ on a win and $1-fk$ on a loss. Fractions above one are overbetting relative to Kelly, but they do not necessarily require borrowing. Even $f=1.75$ has maximum stake $1.75(0.14)=0.245$ in this experiment, well below total wealth.

The source rounds the odds-three Kelly fraction to 0.047, then uses that rounded number in its later stake table. Exact $0.14/3$ and rounded 0.047 define slightly different simulations. A reconstruction should run one declared convention and retain it across all fractions. The analytical calculations below use the exact fraction, while reported tables remain the source's numbers.

Conditional win draws and type selections need to be independent across dates to implement the intended repeated-gamble model. For comparing strategies, common draws across fractions make paired differences more interpretable. The source's discussion of identical worst scenarios suggests some shared scenario use, but does not give the seed, generator, or complete pairing protocol. A new implementation should record those choices rather than claim bit-for-bit replication.

## Seven hundred decisions: heavy tails and loss frequencies

Section 2 repeats the bet mixture for 700 decisions on 2,000 paths, extending the earlier Ziemba–Hausch simulation. It compares $f=1,0.75,0.5,0.25,0.125$. Table 2, p. 3, gives the following terminal-wealth statistics, all in the same currency units as initial wealth 1000:

| Fraction | Maximum | Mean | Minimum | Standard deviation |
|---:|---:|---:|---:|---:|
| 1 | 318,854,673 | 524,195 | 4 | 8,033,178 |
| 0.75 | 4,370,619 | 70,991 | 56 | 242,313 |
| 0.50 | 1,117,424 | 19,005 | 111 | 41,289 |
| 0.25 | 27,067 | 4,339 | 513 | 2,951 |
| 0.125 | 6,330 | 2,072 | 587 | 650 |

The counts exceeding initial wealth are 1,752, 1,855, 1,930, 1,957, and 1,978 respectively. Their complementary loss frequencies are 12.4%, 7.25%, 3.5%, 2.15%, and 1.1%. The counts above 10,000 are 1,175, 1,185, 912, 104, and zero. For that particular tenfold target, three-quarter Kelly slightly exceeds full Kelly in the simulation, despite a far lower arithmetic sample mean. At the much higher threshold of one million, counts are 111, 17, 1, zero, and zero.

Full Kelly's reported skewness is 35 and kurtosis 1,299, compared with 1 and 2 for one-eighth Kelly. The text refers to excess kurtosis, although the tables shorten the label to kurtosis and do not specify a sample-estimator convention. These figures convey extreme tail concentration; their exact numerical reproduction needs the moment convention as well as the simulation draws.

The largest full-Kelly observation alone contributes about 159,427 to its sample mean, or 30.4% of the reported mean. Using the table's sample standard deviation, the usual estimated Monte Carlo standard error of that mean is approximately 179,627. This is a diagnostic calculated here, not an uncertainty interval supplied by the authors. With such a heavy finite-horizon tail, a normal approximation for that mean is itself questionable. Calling 524,195 a typical outcome would be misleading.

The discrete model permits a useful analytical check independent of Monte Carlo. The average Kelly stake across types is $\sum q_Ok_O=0.0588$, so

$$
\mathbb EW_{700}=1000(1+0.008232f)^{700}.
$$

With exact fractions this gives approximately 310,695, 74,330, 17,731, 4,217, and 2,054 in the order above. Differences from reported sample means are not automatically coding errors: heavy-tail sampling variation and stake rounding both matter. For full Kelly the exact expected log increment is approximately 0.00403735, giving a geometric center $1000\exp(700g)\approx16,880$, dramatically below arithmetic expected wealth.

Figures 1 and 2 plot paths selected for the highest and lowest final wealth. They show late accumulation in the best runs and large early losses in the worst ones. Selection on terminal extremes is intentional and useful for illustrating risk, but it does not show a median path or the distribution of maximum drawdown. The figures supply neither a pathwise floor guarantee nor a drawdown confidence bound.

All tested stakes are below one, so wealth remains strictly positive in every finite sequence under the discrete law. Observed minima above 500 for the two smallest fractions do not mean those strategies mathematically guarantee retention of half the original wealth. An arbitrarily long losing sequence can still reduce a fixed positive-fraction portfolio substantially.

## Forty decisions and overbetting

Section 3.1 reduces the horizon to 40 decisions and uses 3,000 paths. It compares fractions 1.75, 1.50, 1.25, 1.00, 0.75, 0.50, and 0.25. Table 3 lists actual stake fractions for each bet; for example the even-money stake ranges from 0.245 to 0.035, and the odds-five stake from 0.049 to 0.007. Table 4, p. 6, reports:

| Fraction | Mean terminal wealth | Minimum | Maximum | Standard deviation |
|---:|---:|---:|---:|---:|
| 1.75 | 1,738.11 | 42.77 | 50,364.73 | 2,360.73 |
| 1.50 | 1,625.63 | 80.79 | 25,093.12 | 1,851.10 |
| 1.25 | 1,527.20 | 83.55 | 21,730.90 | 1,296.72 |
| 1.00 | 1,386.80 | 193.07 | 8,256.97 | 849.73 |
| 0.75 | 1,279.32 | 281.25 | 6,632.08 | 587.16 |
| 0.50 | 1,172.74 | 456.29 | 3,044.34 | 359.94 |
| 0.25 | 1,085.07 | 664.31 | 1,854.53 | 160.76 |

The table's count above 1000 for fraction 1.50 is printed as 11,606, impossible in 3,000 paths. It is a source error; no corrected count can be recovered with certainty from the supplied material. The other columns report 1,556, 1,762, 1,836, 1,899, 1,938, and 2,055 in their respective positions. In particular, full Kelly finishes above initial capital on 61.2% of paths, while quarter Kelly does so on 68.5%. Greater odds of a modest profit can coexist with lower expected log wealth and much lower mean money.

Figures 3–5 display extreme paths, inverse cumulative distributions of log wealth, normal-probability plots, and mean/standard-deviation comparisons. Mean log wealth peaks near full Kelly; beyond it, mean log wealth declines while log-wealth dispersion rises. Arithmetic sample mean still increases with the fraction, as the table shows. This is the clearest demonstration of the difference between overbetting and merely taking more expected dollar risk.

The quantile curves cross. Consequently, the simulations do not establish first-order stochastic dominance of one fraction over all others. Approximate linearity in normal-probability plots is evidence that log wealth is roughly normal over this horizon. It is not exact lognormality: log wealth is a sum of finitely many discrete increments. The central limit approximation can describe its center better than its extreme tails, precisely where ruin and large targets become most relevant.

## Uniform-return asset: leverage below full Kelly

Section 3.2 replaces the bets with one risky asset whose gross annual return is uniform on $[0.75,1.50]$. Its arithmetic net mean is 12.5%. Cash earns zero and may be borrowed at the same zero rate. For risky wealth proportion $\lambda$, net risky return $R\sim U(-0.25,0.50)$ gives

$$
G(\lambda)=1+\lambda R.
$$

The simulation uses 40 annual decisions, 3,000 paths, and $\lambda=0.4,0.8,1.2,1.6,2.0,2.4$. Rebalancing maintains those proportions of current wealth. Weights above one borrow cash; at 2.4, the risky position is 240% of net wealth and cash is −140%.

Appendix 5.1 derives the exact expected-log optimum for uniform net returns $R\sim U(a,b)$ and cash net rate $r$. On the positive-payoff domain, its first-order condition is

$$
\frac1{b-a}\int_a^b\frac{R-r}{1+r+x(R-r)}\,dR=0.
$$

For a nonzero root this reduces to

$$
x(b-a)=(1+r)\log\frac{1+r+x(b-r)}{1+r+x(a-r)}.
$$

For the experiment, solve $[(1+0.5x)/(1-0.25x)]^{1/x}=e^{0.75}$ to obtain $x^*\approx2.8655$. This is exact for the stated uniform law up to numerical root precision. The six tested risky weights therefore correspond to fractions approximately 0.140, 0.279, 0.419, 0.558, 0.698, and 0.838 of full Kelly. None overbets, even though four borrow cash.

Table 6, p. 10, reports:

| Risky weight | Mean wealth | Minimum | Maximum | Count above 10,000 |
|---:|---:|---:|---:|---:|
| 0.4 | 7,045.27 | 728.45 | 34,435.74 | 529 |
| 0.8 | 45,675.75 | 425.57 | 743,361.14 | 2,524 |
| 1.2 | 275,262.93 | 197.43 | 11,155,417.33 | 2,808 |
| 1.6 | 1,538,429.88 | 70.97 | 124,068,469.50 | 2,851 |
| 2.0 | 7,877,534.72 | 18.91 | 1,070,576,212 | 2,847 |
| 2.4 | 36,387,516.18 | 3.46 | 7,399,787,898 | 2,803 |

The counts above initial wealth are 2,998, 2,997, 2,995, 2,991, 2,980, and 2,965. Larger exposure increases both expected log growth and dispersion throughout this below-Kelly grid, as Figure 8 shows. Yet the chance of exceeding the particular 10,000 target peaks in the middle of the grid, while the count above one million rises from zero at the first two weights to 1,407 at the largest. The preferred weight remains objective-dependent.

All path multipliers are positive because $1-0.25\lambda>0$ for every tested $\lambda<4$. Even the full Kelly allocation has minimum one-period multiplier about 0.283625. This support restriction, rather than a general statement that fractional Kelly cannot go bankrupt, explains positivity here. A leverage ratio by itself does not determine admissibility; it must be compared with the worst possible asset return and financing terms.

Figures 6–7 show extreme paths and terminal log-wealth distributions. As in the discrete example, approximate normality of summed log returns is a finite-horizon approximation, and extreme plotted paths are selected realizations. There is no spread between borrowing and lending rates, margin liquidation, collateral haircut, or financing availability constraint.

## Gaussian equity calibration and the Kelly qualification

Section 3.3 uses historical U.S. equity and Treasury-bill moments quoted from Siegel for 1926–2001: annual equity net mean 0.102, standard deviation 0.203, and bill net return 0.039 treated as deterministic. It does not replay the historical annual observations. Appendix 5.2 explicitly assumes Gaussian net risky returns and simulates 40 annual decisions on 3,000 paths.

For the same risky weights $\lambda=0.4,0.8,1.2,1.6,2,2.4$, the portfolio multiplier is

$$
G(\lambda)=1.039+\lambda(R-0.039),\qquad R\sim N(0.102,0.203^2).
$$

The source calls $x^*=1.5288$ the Kelly risky proportion and labels those weights approximately 0.26, 0.52, 0.78, 1.05, 1.31, and 1.57 Kelly. Two distinctions are necessary before using that normalization.

First, the appendix prints $x=(\mu_R-r)/\sigma_R$, but the numerical answer is $(0.102-0.039)/0.203^2\approx1.5288$. The denominator must be variance to match the number and the familiar diffusion expression. The body also prints the associated cash weight as −0.5228; one minus 1.5288 is −0.5288. These are directly derived consistency corrections.

Second, replacing the denominator does not repair the literal discrete optimization. A Gaussian arithmetic return has unbounded negative support. For every $\lambda>0$,

$$
\Pr(G(\lambda)\le0)
=\Phi\left(\frac{0.039-1.039/\lambda-0.102}{0.203}\right)>0.
$$

Real-valued expected $\log G$ is therefore not defined on that portfolio. With bankruptcy assigned log utility minus infinity, it is not a finite-log admissible strategy. The Merton proportion is exact in a continuously rebalanced diffusion model with its corresponding drift and variance rates; it is not an exact solution of an annual arithmetic-Gaussian log problem. One can use it as an exposure benchmark or approximation, but must say which model has changed.

For perspective, under the literal independent Gaussian law, the probability of at least one nonpositive multiplier over 40 years is approximately 0.0095% at weight 1.2, 0.895% at 1.6, 7.90% at 2.0, and 25.36% at 2.4. These are calculations from the supplied law, not source-reported Monte Carlo frequencies. They are distinct from ending below initial wealth and from ending with negative wealth after allowing the process to continue through insolvency.

## Reported equity-simulation outcomes

Table 8, p. 14, reports the following raw terminal wealth:

| Risky weight | Mean | Minimum | Standard deviation | Count above initial 1000 |
|---:|---:|---:|---:|---:|
| 0.4 | 12,110.34 | 2,367.92 | 6,147.30 | 3,000 |
| 0.8 | 30,937.03 | 701.28 | 35,980.17 | 2,996 |
| 1.2 | 76,573.69 | −4,969.78 | 174,683.09 | 2,954 |
| 1.6 | 182,645.07 | −133,456.35 | 815,091.13 | 2,779 |
| 2.0 | 416,382.80 | −6,862,762.81 | 3,634,459.82 | 2,409 |
| 2.4 | 895,952.14 | −102,513,723.8 | 15,004,915.61 | 1,875 |

The arithmetic sample mean increases throughout, but the frequency below initial wealth rises to 37.5% at the largest weight. Counts above 10,000 are 1,698, 2,276, 2,273, 2,112, 1,794, and 1,375. Counts above one million are zero, zero, 9, 116, 216, and 270. More leverage can improve the upper tail while reducing the chance of exceeding a moderate target.

The source explicitly says its large negative outcomes assume short selling remains permissible through the horizon. This means Table 8 continues a signed wealth recursion after insolvency. A real limited-liability fund, margin account, or institution with a stop-out rule would have a different terminal distribution. Once wealth changes sign, maintaining positions proportional to signed net wealth also reverses the signs of the asset and financing positions. These outcomes cannot be interpreted as feasible ordinary Kelly wealth without additional contractual assumptions.

Figure 9 terminates the displayed worst paths when wealth vanishes, while Table 8 retains negative terminal values. Figure 10 incorporates losses with the transformation

$$
\operatorname{sign}(W_T)\log|W_T|.
$$

Although its axis is labeled log wealth, this is not the logarithm of wealth or the log-growth objective. It depends on the currency scale in a different way on positive and negative observations and is not even globally monotone around zero. Figure 11's corresponding mean/dispersion plot is a descriptive transformed-data comparison, not a validation of expected-log optimality. The negative tail is economically important, but changing its graphical transformation cannot restore admissibility.

## What a faithful reconstruction can establish

The supplied laws, horizons, starting wealth, fraction grids, and recurrence equations are sufficient to reproduce the qualitative experiment and independently compute many population quantities. Exact table matching is blocked by missing seeds, unspecified random-number coupling, stake rounding, moment-estimator conventions, and the inconsistent count in Table 4. No source code or standard-error table accompanies the supplied version.

A reconstruction should generate the underlying outcomes once per path, apply all fractions to the same draws, and save both terminal wealth and the complete path. For the first two families, accumulate logs separately from wealth to avoid numerical overflow and verify positive multipliers. Compare sample means against the analytical product of mean multipliers; compare average log wealth against the sum of one-period expected logs. Report threshold counts with binomial uncertainty and paired comparisons where common draws are used. These checks assess the model without pretending to reproduce an unavailable random seed.

For the Gaussian case, record the first nonpositive multiplier and separate the source's signed continuation from a clearly specified bankruptcy-absorbing or margin-liquidation variant. Such variants are new experiments, not corrections that preserve Table 8. Truncating the return law also changes the distribution and its log-optimal weight. A continuous diffusion simulation requires its own sampling and rebalancing assumptions; plugging the Merton fraction into annual Gaussian multipliers is not that simulation.

There is no evidence here about transaction costs, predictive signals, real-time parameter learning, or realized performance after estimating expected returns. The paper illustrates a sizing problem conditional on favorable opportunities already being known. Its strongest transferable result is the need to choose the objective and admissible wealth process before interpreting a Kelly fraction. Finite-horizon target probabilities, tail losses, and expected log wealth answer different questions, and the numerical examples make those differences large enough to matter.
