# Structural model of revolving consumer credit risk

Alex Kordichev, John Powel [the title page spells the surname this way; its affiliation note says Powell], and David Tripe. Draft dated 27 September 2005, Massey University. The supplied manuscript has 13 pages and no journal or DOI designation. Source: [original PDF](../../Finance/RevolvingCredit_Kordichev2005.pdf). These notes cover the complete manuscript, including references; page numbers below refer to the PDF's numbered pages.

## Why this matters

A credit card lender observes transactions much more frequently than it observes a borrower's income, employment, household composition, or other debts. The paper asks whether spending and repayment histories can support a structural model of revolving credit risk that produces probability of default, exposure, and loss measures. The intended mechanism is affordability: default develops when required payments exceed what the consumer can or will allocate to this account. Personal shocks act through spending, repayment size, and payment timing. This is useful for stress testing because a scenario can be translated into changes in those quantities rather than only into a change in a generic credit score.

The contribution is a proposed balance-process framework with a contractual delinquency rule and numerical sensitivity illustrations. It is not an estimated causal model, an empirically validated forecasting system, or a calibrated option-pricing model. The option analogy on pp. 2–3 motivates the setup: the lender effectively allows future expenses to be put onto the facility, subject to the limit, while the borrower pays to retain access. The authors explicitly do not value the default option itself. Their operational default boundary is a sequence of missed minimum payments, not a firm's market-valued assets crossing debt principal.

This distinction matters to a quant researcher. A corporate structural model can be driven by continuously marked assets and an inferred asset volatility. Here the relevant state is a transaction ledger, and the cash available to repay is only indirectly observed. Moving from a score to a simulated balance path makes the timing and amount of default endogenous to the account contract. It does not by itself establish that observed payments identify repayment capacity, because the borrower also chooses which liabilities to service and whether to preserve cash.

The paper's Basel II discussion is historical motivation. It treats three consecutive monthly delinquencies as the default event and a one-year horizon as the prediction horizon. These are the paper's conventions, not a statement of the currently applicable regulatory treatment of every revolving product.

## State, contract, and stochastic inputs

The principal state variable is $CCB_t$, outstanding credit card balance. Let $L$ be the contractual credit limit, $CCE_t$ spending charged to the account during time step $t$, and $CCR_t$ the amount of a repayment when a payment event occurs. The event process is described as Poisson with intensity $\lambda=1/T_p$, where $T_p$ is the mean interval between payments. The paper uses $T$ for that interval; these notes use $T_p$ to avoid confusion with the annual forecasting horizon.

The balance recursion printed as equation (2) is

$$
CCB_t=CCB_{t-1}+CCE_t-CCR_tY(\lambda),\qquad CCB_t\in[0,L+\mathrm{Penalties}].
$$

The displayed notation suppresses the time increment of the Poisson process. A literal simulation should use an increment $\Delta N_t=N_t-N_{t-1}$, not repeatedly subtract the cumulative count $N_t$. If multiple events can occur during a step, each needs a repayment amount; multiplying a single draw by the count is an additional specification. These implementation details are not resolved in the manuscript.

Spending is described as a lognormal random variable based on preliminary observation of a small, unspecified number of accounts. A purchase is generally limited by unused credit, $L-CCB_{t-1}$. The source writes lognormal parameters as $(\log\mu_{CCE},\sigma_{CCE})$ but later uses the untruncated lognormal expectation $\exp(\mu_{CCE}+\sigma_{CCE}^2/2)$. Those statements use incompatible meanings for $\mu_{CCE}$ unless the notation is reinterpreted. A clean implementation should distinguish the log-location $m$ from the arithmetic mean $\bar c=\exp(m+s^2/2)$.

The paper also does not specify whether spending beyond the available line is rejected, clipped to the headroom, or resampled from a truncated distribution. These choices differ. Clipping creates a point mass at the headroom, rejection creates a mass at zero, and conditional truncation redistributes probability across permitted spending. Near the credit limit, where the default mechanism is most sensitive, they do not produce the same exposure path.

Required minimum payments depend on a statement balance, not on the balance after the payment is made. Let $DD$ be the payment due date, $PP$ the payment period, typically 30 days, and $k$ the minimum fraction of the statement balance. Equation (1), visually checked on p. 5, is

$$
MMR_{DD}=k\,CCB_{DD-PP}+\max(CCB_{DD-PP}-L,0)+\mathrm{Penalties}(\mathrm{fee},\mathrm{interest}).
$$

The second term makes an overlimit amount immediately repayable; penalties and interest are also required in full. The text gives 3% as an example for $k$, while the numerical figure captions use 2%. One should use the latter for reproducing those figures. The manuscript does not give a complete fee-accrual ledger: the annual versus monthly interpretation of the 12% interest parameter, ordering of interest and spending, treatment of interest-free purchases, and payment allocation rules are missing.

Actual repayments are assumed to reflect the maximum amount a consumer can afford or chooses to pay. The argument is that repaying debt preserves access and reduces interest. This combines ability and willingness into one marked arrival process. A normal distribution for repayment size is entertained in a footnote; the simulations do not report a fitted repayment-size distribution or its variance. Since normal draws can be negative and can exceed the balance, a production model would need bounds or another positive distribution. Such a change would be an implementation extension, not a documented feature of the source.

## Delinquency and default mechanics

Equation (3) sums payments within the period:

$$
R_{DD}=\sum_{t=DD-PP}^{DD}CCR_t\Delta N_t,
\qquad D_{DD}=\mathbf 1\{R_{DD}<MMR_{DD}\}.
$$

Care is required at adjacent period boundaries so that a payment on the statement or due date is counted only once. Equation (4) declares default when $D_{DD}=D_{DD+PP}=D_{DD+2PP}=1$. Thus the model has a memory variable: the length of the current run of delinquent periods. Balance alone is not a sufficient state for simulation or a Markov representation. A useful state includes balance, the current statement's required payment, accrued payments toward it, next due date, and the consecutive-delinquency count.

For a one-month approximation, the authors assume that there is only a single possible repayment. If $P_1$ is the probability that it occurs and $P_2$ the probability that it is sufficient, equation (5) gives

$$
P_{AD}=1-P_1P_2.
$$

This factorization requires the event probability and the sufficient-payment probability to be combined conditionally or independently in the appropriate way. The paper does not define which Poisson probability is intended. The probability of at least one payment in a 30-day interval is $1-e^{-30\lambda}$; the probability of exactly one is $30\lambda e^{-30\lambda}$. At the figure value $\lambda=1/30$ per day these are about 0.6321 and 0.3679, respectively. Confusing them materially changes delinquency. Restricting the monthly model to at most one payment is also different from the unrestricted compound-Poisson balance process.

A visible formula issue occurs in footnote 3 on p. 6. It identifies $P(CCR>MMR)$ with $\Phi((MMR-\mu_{CCR})/\sigma_{CCR})$. With $\Phi$ the standard normal CDF, this is the lower-tail probability. The derived upper-tail expression is

$$
P_2=1-\Phi\!\left(\frac{MMR-\mu_{CCR}}{\sigma_{CCR}}\right)
=\Phi\!\left(\frac{\mu_{CCR}-MMR}{\sigma_{CCR}}\right).
$$

This is a mathematical diagnostic of the supplied PDF, not an official erratum. It also reveals why the sign matters: increasing affordable payments must increase the chance of satisfying the minimum, all else equal.

One cannot obtain annual default probability by cubing an unconditional monthly delinquency probability. Cubing would describe one specified triple under independent, identically distributed monthly events. The annual event is a run of three at any eligible point, with overlapping triples, evolving balances, and state-dependent required payments. Even in an independent constant-probability toy model, a recursion over run lengths zero, one, and two is needed. In this paper the balance dependence makes path simulation the natural proposed solution.

## Exposure and the meaning of loss

Equation (6) calls the following an expected amount of account delinquency:

$$
AoD_{DD}=CCB_{DD-PP}+\exp\!\left(\mu_{CCE}+\frac12\sigma_{CCE}^2\right).
$$

This expression is an opening balance plus an expected spending amount. It does not subtract repayments, condition on delinquency, impose the available-credit cap, or specify whether the lognormal variable represents total monthly spending. Consequently it should not be treated as a general conditional-exposure formula. It is an illustrative approximation whose notation and timing must be fixed before use.

On p. 7 the paper assumes exposure at default equals the personal credit limit, $EAD=L$, because the borrower may draw to the limit within a month; penalties are assumed written off and excluded. On p. 8 it says the credit card balance at default is treated as LGD under zero recovery. These are not interchangeable quantities. A balance is a currency amount; LGD in the usual decomposition is a fraction of exposure. If $EAD=L$, a compatible loss fraction would be $CCB_\tau/L$ after removing written-off penalties, under the assumed zero-recovery convention. If $EAD=CCB_\tau$, zero recovery implies an LGD fraction of one. The manuscript does not explicitly resolve the convention, although its figures plot LGD on a dimensionless scale around 0.8.

This ambiguity is economically material. A model with low conditional balance but high default probability can have the same expected loss as one with high balance and low default probability. Reporting a normalized balance as LGD while independently multiplying by an inconsistent EAD can double-count or mis-scale loss. A reproduction should report the distribution of $CCB_\tau$, the normalization used for each displayed curve, and the actual expected currency loss separately.

The paper includes a further contractual device in the simulations: consumers with a balance at least 30% below their credit limit may draw cash to cover minimum payments when approaching 90 days past due. The option is described as expensive and exercised only then. Its fee, cash-advance amount, effect on available credit, and exact timing are unspecified. It can prevent default without an external inflow of cash, so it can strongly influence the relationship between payment arrivals and observed annual PD. Ignoring it is not necessarily a harmless simplification.

## Numerical illustrations: what was actually run and reported

The paper supplies simulated trajectories and comparative-static graphs, not a dataset-based estimation exercise. Figure 1 on p. 7 displays three balances for approximately 361 days. Account 1 defaults after no repayment event occurs over 90 days; account 2 defaults despite some repayments because they are too small; account 3 survives. This separates payment timing from payment adequacy. No initial balances, complete random paths, simulation seed, or number of replications are supplied.

Figures 2–4 use a limit of \$5,000, minimum payment fraction 2%, and a penalty parameter pair of \$25 and 12%. Figure 2 varies expected monthly expenses from zero to roughly \$6,000 while holding repayment size at \$200 and $\lambda=1/30$. Its reported directional result is that greater expected spending, generated by changing either lognormal location or dispersion, raises PD and the plotted LGD measure. The paper argues that the limit prevents PD from approaching one in the same fashion as under unlimited indebtedness. It gives no numeric table or sampling uncertainty, and the caption does not state the exact grid or lognormal parameter combinations.

Figure 3 varies expected repayment size, displaying a horizontal range up to \$2,000 with curves drawn to around \$1,500. The caption states $CCE=\$60$ per month, $\lambda=1/30$, $L=\$5,000$, $k=2\%$, and penalties of \$25 and 12%. The visually inspected PD curve begins near one for negligible repayment, falls sharply over the first few hundred dollars, and is close to zero beyond that. The LGD curve remains near 0.8 across much of the range. Those are approximate graphical readings; no exact point estimates or Monte Carlo confidence intervals are available.

Figure 4 varies daily payment intensity from zero to around 0.067, with spending again labelled \$60 per month and repayment size \$100. PD declines from around one toward zero as intensity increases. The plotted LGD measure remains near 0.8 with simulation variation. The textual sentence interpreting an increase of $\lambda$ as a shock to the ability to maintain stable payments is imprecise: under the given definition, an increase means more frequent payments. The graph and surrounding argument support the beneficial direction, not a worsening of repayment regularity.

The caption's \$60 per month may appear surprisingly low relative to the spending ranges in Figure 2, but it is what the supplied PDF says. It should not be silently converted to a daily amount to make a recreated graph look similar. The missing expenditure convention, starting balance, repayment distribution, and cash-advance rule leave too many degrees of freedom to infer the simulation from appearance alone.

There are no reported AUCs, calibration errors, likelihood values, realized default comparisons, economic-return comparisons, or standard errors. No benchmark scorecard, logistic model, Merton adaptation, or alternative payment process is actually tested. The numeric parameters define illustrations, not estimated population facts. The small preliminary account sample mentioned for lognormal spending has no count, date range, country, observation window, or eligibility criteria.

## Reimplementation plan and required decisions

A faithful research implementation should retain the distinction between reported equations and the choices needed to complete them. First, define daily time steps, statement and due dates, and a forecast horizon of 365 days or twelve exact contractual periods. The source uses both annual language and 30-day cycles, so the endpoint must be stated. Initialize outstanding balance and all delinquency-memory variables from the account ledger. A starting account already one or two periods behind has a different default probability from a current account with the same balance.

Next, specify a spending distribution with an unambiguous arithmetic mean and log-scale variance, and specify how headroom constrains attempted spending. Generate daily payment arrivals using $\Delta N_t\sim\mathrm{Poisson}(\lambda\Delta t)$ if retaining the source's event process. Generate nonnegative payment marks conditional on arrivals and cap actual repayment at the amount owed if credit balances are excluded. Post spending, fees, interest, and payments in a documented order. At each due date compare accrued payments with the minimum established at the appropriate statement date; update the consecutive-delinquency state and record the first time it reaches three.

For the optional cash-advance rescue mechanism, explicitly code the eligibility boundary $CCB\le0.7L$, the timing relative to the default test, the amount advanced, and its costs. This step cannot be reproduced exactly from the paper. Run both with and without the device and label the latter as a diagnostic variant. Otherwise apparently improved performance of the payment process could merely be a consequence of accounting for an internally financed payment as a cure.

For $M$ independent simulated annual paths, estimate

$$
\widehat{PD}=\frac1M\sum_{m=1}^{M}\mathbf1\{\tau_m\le H\},
\qquad
\widehat{EL}=\frac1M\sum_{m=1}^{M}\mathbf1\{\tau_m\le H\}\,\mathrm{Loss}_m.
$$

Estimate conditional default exposure using only defaulting paths; distinguish its Monte Carlo standard error from the standard error of unconditional loss. Near zero PD, conditional LGD estimates may have almost no effective observations even with a large total simulation count. This helps explain why a smooth-looking PD curve is not enough evidence that a loss curve is reliable. The paper does not disclose $M$, so these statistical calculations are proposed replication controls rather than reported methodology.

The balance recursion also lends itself to deterministic checks. With zero spending, zero fees, and positive payments, outstanding balance should not grow. With zero payment intensity and a positive required payment, default should occur at the third eligible due date unless a rescue rule intervenes. Raising the limit alters both accessible borrowing and rescue eligibility; monotonicity of PD in $L$ therefore cannot simply be assumed. Increasing repayment size should not worsen the pure affordability model, but negative normal draws or incorrectly signed tail probabilities can reverse that direction in faulty implementations.

The intended calibration workflow is to estimate payment frequency and amount distributions from transactional histories, estimate spending distributions over the same information window, and periodically reassign borrowers to pools with similar parameters and contracts. The manuscript suggests monthly or quarterly review. It does not prescribe a rolling estimation-window length, minimum number of payments, shrinkage across borrowers, treatment of seasonality, or censoring after limit changes. Each is essential for a usable empirical design. In particular, observed spending near a limit is censored demand, and payments posted after collection interventions are not draws from an unchanged voluntary-payment process.

For predictive validation, parameters must be fixed using information available at the forecasting date. Evaluate default over the following year, account for closure and refinancing, and compare simulated probabilities with realized default frequencies and established behavioral models. Pool reallocation and stress parameter changes should be assessed separately. These are necessary extensions to turn the proposal into a tested risk model, not empirical procedures completed in the paper.

## Interpretation and limitations

The model offers a transparent channel for household stress: fuel costs can raise expected spending, benefit changes can alter repayment capacity, and unstable income can affect payment timing or dispersion. Yet a parameter scenario is not an identified causal effect. The mapping from a macroeconomic shock to $CCE$, $CCR$, and $\lambda$ is external to the model and may involve joint changes. Modeling those inputs independently could miss the same shock both raising spending and reducing payments.

The assumption that payment amount reveals maximum affordable repayment is especially strong for transactors, households with several cards, borrowers making strategic minimum payments, and those saving cash for essential expenses. A structural interpretation would need a household budget or an explicit payment-allocation model. Without it, transaction parameters are behavioral summaries whose response to a new limit or price policy may differ from their historical association with risk.

There is no portfolio dependence model. Pooling borrowers with similar parameters makes marginal simulations more efficient but does not generate systematic co-default risk, downturn recoveries, or capital tail risk. Likewise the paper's zero-recovery simplification does not model collections, legal costs, time to recovery, debt sale proceeds, or discounting. The option terminology therefore should not be mistaken for an arbitrage-pricing or comprehensive capital framework.

The lasting research idea is to make revolving-credit default an outcome of payment-flow dynamics and contractual rules. The supplied draft is most useful as a model specification to critique and extend. Its observed results are qualitative simulation responses; the repayment-tail sign, spending parameterization, EAD/LGD terminology, missing simulation inputs, and unestimated stress mappings must be resolved before numerical outputs can be interpreted as risk estimates for an actual book.
