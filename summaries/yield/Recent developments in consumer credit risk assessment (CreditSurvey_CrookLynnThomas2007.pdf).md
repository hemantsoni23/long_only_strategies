# Recent developments in consumer credit risk assessment

**Jonathan N. Crook, David B. Edelman, and Lyn C. Thomas (2007).** *European Journal of Operational Research*, article in press, DOI 10.1016/j.ejor.2006.09.100. Source: [CreditSurvey_CrookLynnThomas2007.pdf](../../Finance/CreditSurvey_CrookLynnThomas2007.pdf). This local version has 19 pages, including references, and placeholder volume/page fields; it was received in July 2006 and accepted in September 2006. The filename does not contain the complete author list. This note covers the entire source, including its historical Basel 2 discussion, and distinguishes the survey's reports from algebraic clarifications needed to implement them.

## Why this matters

Consumer-credit modeling is a sequence of decisions over an account's life, not just a binary classification contest. Application scoring screens a new borrower; behavioral scoring uses subsequent repayment and usage; profit scoring chooses terms and cutoffs; portfolio models translate individual risks into capital. A model can rank borrowers well while misestimating default probabilities, and a low-default borrower need not be the most profitable customer. These distinctions determine what data, losses, and validation statistics an implementation needs.

The survey's contribution is to connect classifier research with reject inference, account dynamics, profitability, and the emerging capital framework. It introduces no new universal classifier and conducts no unified empirical benchmark. Its table aggregates results from different published studies, and its numerical regulatory discussion describes the framework at the time of writing. Neither those adoption claims nor those historical rules are presented here as current regulatory guidance.

Its practical warning is that small laboratory improvements in classification may be overwhelmed by population drift, selection into the observed sample, changing outcome definitions, and a mismatch between the fitting objective and the business decision. The tentative preference for support vector machines in the conclusion must be read in that context.

## Outcomes, information, and the basic scorecard

Let $Y_i=1$ denote a bad outcome—default over a specified observation horizon—and let $g_i=P(Y_i=0\mid x_i)$ denote the probability of being good. The horizon is commonly one year in the survey; possible default definitions include three missed scheduled payments or three consecutive missed payments. Those definitions are not interchangeable. Every implementation must fix the product, observation window, arrears rule, treatment of cures, and censoring before fitting a score.

The source has a consequential wording slip across PDF pages 2–3: it describes a good as a borrower who defaulted. Its surrounding equations and classification discussion consistently treat good as the desirable repayment class. The convention above resolves that slip explicitly.

For logistic regression, define $\eta_i=\beta_0+\beta'x_i$. Then

$$
\log\frac{g_i}{1-g_i}=\eta_i,\qquad
 g_i=\frac{e^{\eta_i}}{1+e^{\eta_i}},\qquad
 PD_i=1-g_i.
$$

The probability expression printed immediately after source equation (1) omits the intercept; it is valid only if the intercept has been absorbed into the regressor vector. With independent labeled observations, a reproducible fit maximizes

$$
\ell(\beta)=\sum_i\{(1-Y_i)\log g_i+Y_i\log(1-g_i)\}.
$$

This explicit likelihood is a reconstruction of the stated maximum-likelihood procedure. Dependence between accounts or repeated observations requires a declared modeling and inference treatment. A higher good score means a safer applicant, so acceptance is $s_i\ge c$ for a suitable monotone score $s_i$.

The survey describes coarse classification: combine raw variable values into bins with similar outcome proportions, including a separate missing-value category when appropriate. The bin can enter a model as dummy variables or through an evidence transformation. Its example is the log good-to-bad proportion within a bin. The frequently used alternative $\log[P(\text{bin}\mid G)/P(\text{bin}\mid B)]$ differs from within-bin posterior log odds by the population prior log odds. With a free intercept, a fixed additive difference can be absorbed; mixing conventions without tracking the reference population can break probability calibration. Empty cells require a disclosed smoothing rule, which this survey does not specify.

All outcome-dependent binning, variable selection, and transformations belong inside the training process. Validation observations must not influence them. The source advocates training and holdout samples but does not provide a single dataset, split, feature dictionary, or fitted coefficient vector from which a reader could reproduce one complete scorecard.

A ranking can be enough to choose a predetermined acceptance fraction. It is not enough to choose a profit-optimal cutoff or calculate expected loss without calibrated probabilities or independent outcome-rate estimates. Monotone score transformations preserve rank-based discrimination while changing the interpretation of the score as a probability.

## Measuring discrimination and making a decision

The source's confusion matrix uses the first subscript for predicted class and the second for observed class. Thus $n_{GB}$ counts bads accepted as good, and $n_{BG}$ counts goods rejected as bad. With $n_G=n_{GG}+n_{BG}$ and $n_B=n_{GB}+n_{BB}$,

$$
\text{reject-good rate}=\frac{n_{BG}}{n_G},\qquad
\text{accept-bad rate}=\frac{n_{GB}}{n_B}.
$$

These class-conditional error rates have different denominators from the bad fraction among accepted loans, $n_{GB}/(n_{GG}+n_{GB})$. Overall error is $(n_{BG}+n_{GB})/(n_G+n_B)$; simply adding the two conditional rates gives a different, implicitly balanced criterion. Changing class proportions can change overall accuracy even when each conditional error rate remains unchanged.

The ROC curve plots bads correctly rejected, $n_{BB}/n_B$, against goods incorrectly rejected, $n_{BG}/n_G$, as the cutoff varies. With high scores denoting good borrowers, the corresponding area has the rank interpretation

$$
AUC=P(s_G>s_B)+\tfrac12P(s_G=s_B),\qquad Gini=2AUC-1.
$$

The Kolmogorov–Smirnov separation is $\sup_s|F_G(s)-F_B(s)|$. Both AUC/Gini and KS summarize discrimination, not calibration or profit. Crossing ROC curves can favor different models in different operating regions. A global area advantage may be irrelevant near the lender's feasible acceptance and bad-rate constraints. The source's verbal description of how its error areas move with the cutoff is inconsistent with its correctly oriented figures; using the explicit confusion-matrix definitions avoids that ambiguity.

Let $L>0$ be the gain from accepting a good and $D>0$ the loss from accepting a bad, before costs omitted from this simple model. Expected incremental profit from acceptance is

$$
L g(x)-D[1-g(x)].
$$

If rejection has zero incremental payoff, acceptance is profitable when $g(x)/(1-g(x))\ge D/L$, equivalently $g(x)\ge D/(D+L)$. The threshold changes with funding, acquisition, servicing, recovery, capital, and borrower-specific exposure. The survey's cost-sensitive comparison cannot be replaced by maximizing unweighted accuracy unless the associated costs and class balance justify it.

## Behavioral scoring and account dynamics

Behavioral scoring adds repayment history, utilization, balances, and activity to application information. It can support credit-limit increases, repricing, additional loans, or collections. A predictive model fitted under the old credit-limit policy does not automatically identify outcomes under a new policy: changing exposure or price can change both borrower behavior and repayment risk. The survey flags this policy-dependence problem without supplying a causal identification strategy.

For a monthly Markov model, let $X_t$ be the account state and $P_t(i,j)=P(X_{t+1}=j\mid X_t=i)$. With row-vector state probabilities $\pi_t$,

$$
\pi_{t+h}=\pi_tP_tP_{t+1}\cdots P_{t+h-1}.
$$

This propagation requires the chosen first-order conditional structure, not stationarity. Under stationarity the product becomes $P^h$. Delinquency, activity, and balance can jointly define a state; paid-off and written-off states are often absorbing. Structural zeros matter: in an ordinary monthly arrears system, an up-to-date account cannot become several monthly payments behind in one step without a separate event or accounting rule.

For order $k$, use the history state $(X_{t-k+1},\ldots,X_t)$ and transition by shifting the history and appending one new state. This gives a first-order representation on an enlarged state space, with many impossible transitions. It does not by itself make a time-varying process stationary. State explosion and sparse cells can make a formally richer model difficult to estimate.

The studies summarized report that at least 90% of up-to-date credit-card or personal-loan accounts remain up to date in the next month. Published tests also reject simple first-order and stationary specifications in some datasets; one cited account-state definition rejects orders one through three. These findings are product- and state-definition-specific, not universal transition probabilities.

The mover–stayer model introduces a latent permanent-stayer fraction for each initial state. Write $S=\operatorname{diag}(s_1,\ldots,s_m)$ and let $M$ be the movers' stationary transition matrix. Then

$$
P(0,h)=S+(I-S)M^h.
$$

The source's equation (3) has this matrix structure, but calls $S$ a row vector in the prose; a diagonal matrix is required for dimensional consistency. The mixture need not satisfy $P(0,h)=P(0,1)^h$, because type is persistent rather than redrawn each month. The cited studies report 44–72% of accounts remaining in one state over their observed histories; finite-window nonmovement is evidence supporting a stayer component, not proof that an account will never move. Further segmentation distinguishes modest, intermediate, and frequent movers. To use such a model for net-present-value optimization requires transition probabilities conditional on the proposed credit line and APR, cash flows, and discounting, none of which is numerically supplied here.

## Classifier families and their assumptions

Fisher's linear discriminant maximizes the squared difference in projected means divided by within-class variance:

$$
J(w)=\frac{[w'(\bar x_G-\bar x_B)]^2}{w'Sw},\qquad
w\propto S^{-1}(\bar x_G-\bar x_B).
$$

The direction follows from a Rayleigh-quotient argument when $S$ is positive definite; Gaussianity is not needed merely to maximize that criterion. Gaussian class distributions with common covariance $\Omega$ are additional assumptions that yield a Bayes cost-sensitive linear boundary. Under those assumptions, accept if $x'w\ge c$, where

$$
w=\Omega^{-1}(\mu_G-\mu_B),\qquad
c=\tfrac12(\mu_G'\Omega^{-1}\mu_G-\mu_B'\Omega^{-1}\mu_B)
+\log\frac{D\pi_B}{L\pi_G}.
$$

Here $\pi_G,\pi_B$ are population class priors. The fitted direction alone does not specify this economically meaningful cutoff. Unequal class covariance matrices generally yield a quadratic boundary. A linear-probability regression can still rank observations but may predict outside $[0,1]$, preventing a direct PD interpretation.

Mathematical-programming scorecards choose weights and slack variables to separate good from bad applications. The source gives a sum-of-slacks objective, with goods above a cutoff and bads below it. The unnormalized formulation admits scaling degeneracy; its discussion proposes normalization and warns about dependence on linear transformations of the inputs. An implementer must state the normalization, strict-inequality replacement, and treatment of an intercept. A binary misclassification formulation instead minimizes $L\sum_{i\in G}m_i+D\sum_{i\in B}m_i$, where $m_i$ indicates an error. It can have multiple optima with very different holdout behavior and, in the cited implementations, is computationally demanding.

Neural networks compose affine maps and nonlinear activations and fit weights through backpropagation. The survey emphasizes interpretability: rule extraction can prune and simplify a fitted network or train an interpretable surrogate to mimic it. Such mimicry needs both a fidelity check and an outcome-performance check. The paper's comments on giving rejection reasons describe its historical setting; this note does not infer current legal obligations from them.

Trees recursively split applicants into more homogeneous nodes and then prune. Their entropy criterion is

$$
H(p)=-p\log_2p-(1-p)\log_2(1-p),
$$

with $0\log0=0$. Split selection should compare the parent impurity with the child-size-weighted impurities. A tree also needs minimum node sizes, pruning or stopping rules, and terminal probability or class assignments. Fuzzy rules allow graded membership; nearest-neighbor methods use local comparisons. Genetic algorithms are optimization procedures for rules, feature subsets, trees, or networks, rather than one unique classifier.

Support vector machines combine margin maximization with a penalty for violations. A precise conventional reconstruction of the survey's description is

$$
\min_{w,b,\xi\ge0}\;\tfrac12\|w\|^2+C\sum_i\xi_i,
\qquad y_i[w'\varphi(x_i)+b]\ge1-\xi_i,
$$

where $y_i=+1$ for good and $-1$ for bad. Its score can be evaluated explicitly as $f(x)=\sum_i\alpha_i y_iK(x_i,x)+b$ even if no convenient finite-dimensional primal feature map is available. Thus the source's statement that a kernel cannot yield an explicit scorecard should be understood as an interpretability difficulty, not an inability to calculate predictions. Kernel, penalty, feature scaling, and tuning protocol are necessary inputs not fixed by this survey. An SVM margin is not automatically a calibrated default probability.

## What the comparison table actually shows

Table 2 reports percentages correctly classified, not cost-weighted profit or universally comparable error rates. Selected rows, checked against the visual table, are:

| Study | Reported percentages correctly classified | Scope |
|---|---|---|
| Srinivisan and Kim (1987), spelling as cited | Linear/LDA 87.5; logistic 89.3; tree 93.2; mathematical programming 86.1 | One row's comparison only |
| West (2000) | Linear/LDA 79.3; logistic 81.8; tree 77.0; neural net 82.6; nearest neighbor 76.7 | Average across two datasets |
| Lee et al. (2002) | Linear/LDA 71.4; logistic 73.5; neural net 73.7; hybrid LDA–network 77.0 | Hybrid is separately parenthesized in the source |
| Baesens (2003) | Linear/LDA 79.3; logistic 79.3; tree 77.0; mathematical programming 79.0; neural net 79.4; nearest neighbor 78.2; SVM 79.7 | Average across eight datasets |
| Ong et al. (2005) | Linear/LDA 80.8; tree 78.4; neural net 81.7; genetic programming 82.8 | Average across two datasets |

In the Baesens row, SVM exceeds logistic regression by 0.4 percentage points. That is not a 0.4% reduction in default losses, nor proof of statistical superiority. The table lacks uniform sample sizes, standard errors, common cutoffs, and costs. Henley's much lower reported accuracies, around 43%, are explicitly associated with a different default proportion. Comparing that row with an 80% row would confuse population composition with model quality.

The source stresses that many studies lack inferential tests and choose cutoffs differently. It also discusses population drift, omitted predictors, changing definitions of default, and differing optimization and evaluation objectives. A neural network containing a logistic model as a special case need not outperform it out of sample after estimation error and tuning. The survey's SVM conclusion is a tentative reading of the available studies, not a theorem or a fresh out-of-time replication.

## Reject inference: identification before correction

Let $A=1$ indicate that an applicant is accepted and an outcome is observed. In practice observation can also require taking up the offer and remaining observable, so a more complete selection indicator may combine several events. The paper focuses on acceptance. With a common covariate set $X$, the probability identity is

$$
P(Y=1\mid X)=
P(Y=1\mid X,A=1)P(A=1\mid X)
+P(Y=1\mid X,A=0)P(A=0\mid X).
$$

The source's equation (9) mixes covariate sets $X_1$ and $X_2$ in these terms. That expression is not a general conditional-probability identity without additional compatibility assumptions. Conditioning every term on the same information makes the necessary claim explicit.

If $Y\perp A\mid X$, then $P(Y=1\mid X,A=1)=P(Y=1\mid X)$ where observations are available. This is the relevant missing-at-random condition. It is conditional independence, not an assertion that acceptance is unrelated to default unconditionally. Including all acceptance-rule inputs can support the condition when selection depends only on those observed inputs. It does not establish it if unrecorded judgment, offer take-up, or omitted variables still select on repayment risk.

There are two separate requirements: conditional ignorability and support. If a deterministic legacy policy rejects every applicant in a region, no labeled accepted cases exist there. Even with ignorability, prediction in that region requires model extrapolation or new information. Including the old score does not create overlap. Nor does the absence of a marginal covariate-distribution assumption make logistic regression, a network, or an SVM automatically unbiased in finite samples. Model specification, estimation, regularization, and outcome measurement still matter.

Augmentation estimates the acceptance propensity $e(X)=P(A=1\mid X)$ from all applicants and weights each accepted case by $1/e(X)$. A weighted outcome likelihood or weighted performance estimate can then target the applicant population under conditional ignorability, correctly estimated propensities, and positivity. Very small propensities produce unstable weights. Trimming them changes the target or adds bias and must be disclosed; it is not specified in the survey.

Under missing-not-at-random selection, imputing rejected outcomes with the accepted-sample model does not identify the missing risk. EM and multiple imputation depend on their assumed missingness and outcome models. The bivariate-probit selection approach models acceptance and default jointly with correlated latent errors. The survey notes restrictive bivariate-normal assumptions and problems when the historical accept rule is perfectly predicted. Any exclusion variable or other identifying restriction must be stated; the paper supplies no dataset-level specification establishing it.

The cited empirical studies find relatively small model-parameter bias in their nearly all-applicant samples, while apparent validation performance can be seriously overstated when the holdout contains only historical accepts. Bias grows as the old policy becomes more selective in the described experiments. Augmentation sometimes worsens performance relative to accepted-only logistic regression. These findings do not establish that rejects can always be ignored; they show that a proposed correction must solve an identifiable problem and be evaluated on an appropriate target population.

## Profit scoring and a corrected strategy curve

Let $\pi_G,\pi_B$ be applicant class fractions and $F_G(s),F_B(s)$ the conditional score distributions. Accept scores at least $s$, and ignore tie handling for continuous scores. Define

$$
a(s)=\pi_G[1-F_G(s)]+\pi_B[1-F_B(s)],
\qquad b(s)=\pi_B[1-F_B(s)].
$$

Here $a(s)$ is the acceptance fraction of all applicants, while $b(s)$ is the fraction of all applicants who are both bad and accepted. The bad rate among accepts is $b(s)/a(s)$ when $a(s)>0$. The survey's Figure 5 and associated formulas blur these two bad-rate denominators. Its perfect-classifier curve, zero until acceptance reaches $.95$ and then rising with slope one, corresponds to $b=\max(0,a-.95)$ when 95% of applicants are good. The conditional accepted bad rate would instead be $\max(0,a-.95)/a$.

For constant per-account gain and loss, expected profit per applicant and expected default loss are

$$
\Pi(s)=L\pi_G[1-F_G(s)]-D\pi_B[1-F_B(s)],
\qquad EL(s)=D\,b(s).
$$

Lowering the cutoff initially can increase profit, but eventually the added loss from worse applicants can outweigh added revenue. The efficiency frontier contains cutoffs giving the lowest expected loss for a required profit, or the greatest profit for a loss constraint. These are economic tradeoffs, not a covariance-based portfolio frontier.

The gain/loss odds condition derived earlier gives the marginal profit-maximizing cutoff. The source reports extensions with funding, operating, and regulatory-capital costs; within the cited risk-neutral model, the added capital requirement raises the cutoff and reduces lending. That conclusion is conditional on the model, rather than a universal equilibrium result across competing lenders.

Loan design adds the probability that the customer accepts the offer. Interest rate and amount affect take-up, borrower utility, risk, and lender profit. The surveyed model trades off expected profit and market share and has limitations: no explicit rival offers, no learning, and difficult-to-observe individual utility functions. The source's instruction to minimize expected profit in that discussion conflicts with the stated maximization objective. No quantitative optimum can be calculated from this survey because the response and profit functions are absent.

## Historical one-factor capital model

The historical capital formula in source equation (10) is a fraction of exposure:

$$
k=LGD\left\{\Phi\left[
\frac{\Phi^{-1}(PD)+\sqrt R\,\Phi^{-1}(.999)}{\sqrt{1-R}}
\right]-PD\right\}.
$$

$PD$ is a probability over the prescribed horizon, $LGD$ is the fraction of exposure lost upon default, and $R$ is a latent asset correlation. Multiplication by exposure at default gives a currency amount in this simplified representation. All probability and loss-fraction inputs use decimal units. The subtraction $PD\times LGD$ is expected loss; the remaining term represents stress loss above that expectation. The expression inside $\Phi$ is not itself a probability that an uncertain PD lies between two values.

A reconstruction clarifies the assumptions. Let latent asset value be $Z_i=\sqrt R\,F+\sqrt{1-R}\,\epsilon_i$, with independent standard-normal factor and idiosyncratic shocks, and default if $Z_i<\Phi^{-1}(PD)$. Conditional default probability at $F=f$ is

$$
p(f)=\Phi\left[\frac{\Phi^{-1}(PD)-\sqrt R f}{\sqrt{1-R}}\right].
$$

In a sufficiently granular homogeneous pool, conditioning on the adverse factor quantile $f=-\Phi^{-1}(.999)$ gives the displayed stress loss. Finite concentration, heterogeneous exposures, dependence beyond the common factor, and uncertain recoveries require additional treatment. The survey questions the behavioral plausibility of importing a corporate asset-threshold story into unsecured household default; it describes reputation-based alternatives without establishing one as empirically definitive.

The paper gives $R=.15$ for mortgages, $.04$ for qualifying revolving exposures, and for other retail exposures

$$
R(PD)=.03 A(PD)+.16[1-A(PD)],\qquad
A(PD)=\frac{1-e^{-35PD}}{1-e^{-35}}.
$$

This function decreases from $.16$ to $.03$ as $PD$ increases from zero to one. The negative derivative is $-.13(35)e^{-35PD}/(1-e^{-35})$. Source page 16 says a negative correlation–PD relationship is opposite to equation (11), but the equation itself is also decreasing. The quoted Brazilian estimate of 2.28% is below its 3% lower bound; it does not establish that one correlation is suitable for all consumer products. Asset correlation also differs from correlation between binary default indicators.

Risk grouping and behavioral scoring can provide the ordinal structure for capital pools, but a capital calculation requires calibrated PDs, LGDs, and EADs. The survey describes multi-year information intended to cover a business cycle. It does not supply a bank portfolio, loan-level defaults, recoveries, utilization at default, or an implemented pool calibration. Its historical percentages and implementation expectations should not be used as a present-day compliance specification.

## Low-default portfolios and calibration tests

Zero observed defaults do not imply zero risk. Under independent identical Bernoulli defaults with $N$ exposures and probability $p$, $P(D=0)=(1-p)^N$. A one-sided confidence upper bound at confidence $\gamma$ solves $(1-p_U)^N=1-\gamma$, giving

$$
p_U=1-(1-\gamma)^{1/N}.
$$

The printed zero-default formula on PDF page 16 omits the reciprocal in the exponent. The displayed bound above follows directly from its preceding zero-default probability and decreases appropriately with sample size. For example, $N=800$ and $\gamma=.999$ would give about $.860\%$; this is an illustrative reconstruction, not a reported sample size in the survey.

For ordered grade probabilities $p_1\le p_2\le p_3$, pooling counts $n_1+n_2+n_3$ yields the cited most-prudent construction for the safest grade when all three are assigned its probability; the next grade uses the corresponding remaining pool. The survey's prose says decreasing risk, but its inequalities imply increasing risk with the index. It reports independent-default upper estimates of $.86\%$ and $.98\%$ for the first two grades. With correlated latent returns, its cited estimates rise to $5.3\%$, $5.8\%$, and $9.8\%$. The necessary sample counts, correlation parameters, and complete numerical procedure are not provided here, so those values cannot be independently regenerated from this article alone.

For few defaults, the appropriate binomial likelihood over grades is, up to constants,

$$
\mathcal L(p_A,p_B)=p_A^{d_A}(1-p_A)^{n_A-d_A}
 p_B^{d_B}(1-p_B)^{n_B-d_B}.
$$

Here $d_j$ is the default count and $n_j$ the number of exposures. The source's equation (12) prints $1-d_j$ rather than $n_j-d_j$ while describing multiple exposures; that is not the count likelihood. Impose the desired weak ordering, such as $p_A\ge p_B$, when estimating ordered grade risks. A strict inequality can make a boundary optimum unattainable. A maximum-likelihood estimate and a conservative upper confidence limit answer different questions and should not be interchanged.

Calibration tests compare forecast PDs with realized default frequencies. The survey reviews pool-level binomial tests, portfolio-level chi-square tests, a normal approximation using time-series forecast errors, and a multi-category traffic-light test. It reports difficulties with power, short histories, dependence, and size distortions. Its language about tests being conservative is sometimes inconsistent with its statement that they reject too often; those are opposite notions in the usual test-size terminology. A replication must define the null, rejection direction, nominal size, and actual rejection probability explicitly.

For intuition, if equal-PD default indicators have pairwise correlation $r_D$, then

$$
\operatorname{Var}(\bar Y)=\frac{p(1-p)}{N}[1+(N-1)r_D].
$$

This derived identity explains why an independent-binomial reference can badly understate uncertainty. It does not identify a complete tail distribution or convert an asset correlation directly into $r_D$. Multiple grade tests create multiplicity as well; a joint test still needs a correct covariance model. The paper's historical conclusion is that reliable calibration validation remained a substantial research problem, not that a particular omnibus test solved it.

## What a reproducible study would need

A study implementing this survey should retain all applicants, historical decision inputs, acceptance and take-up indicators, observation dates, subsequent repayments, and the precise outcome definition. It should document product terms and policy changes, avoid post-application leakage, and separate training, model selection, calibration, and final evaluation. Time-based holdouts are a useful design choice for measuring drift, but are not a protocol supplied by this source.

Report both rank discrimination and the quantities used in the decision: acceptance fraction, bad fraction among accepts, class-conditional error rates, calibrated PD, expected loss, and realized or estimated profit. Give the monetary cost model and uncertainty intervals, not just accuracy. For reject inference, state the missingness assumption and overlap diagnostics. For dynamic policies, specify how transitions and cash flows change with the action. For capital, keep latent dependence, default-event dependence, pool-level probabilities, and exposure units separate.

Reproducing the published studies in Table 2 would require their original datasets, preprocessing, splits, class proportions, cutoff choices, hyperparameters, and fitted models. Reproducing the profit and capital examples would require additional functions and numerical inputs from the cited primary studies. The present source does not supply them. The value of this survey is its map of connected modeling problems and the warning that a better classifier alone does not solve selection, calibration, policy response, or profitability.
