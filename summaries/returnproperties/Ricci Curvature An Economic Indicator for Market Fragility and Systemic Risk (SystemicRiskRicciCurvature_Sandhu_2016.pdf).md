# Ricci Curvature: An Economic Indicator for Market Fragility and Systemic Risk

**Authors:** Romeil S. Sandhu, Tryphon T. Georgiou, Allen R. Tannenbaum. **Publication:** *Science Advances* 2, e1501495, 27 May 2016. **DOI:** 10.1126/sciadv.1501495. **Source:** `Finance/Copulas/SystemicRiskRicciCurvature_Sandhu_2016.pdf`, 11 PDF pages, comprising the ten-page article and a bibliographic page. Page references below refer to the article. The separate supplementary figures listed on page 9 are not embedded in this local PDF; they were not independently inspected.

## Contribution and economic interpretation

The paper proposes Ollivier-Ricci curvature as a descriptor of financial networks. Its empirical object is a sequence of graphs constructed from equity-return correlations. Its methodological contribution is to transfer a geometric measure of how neighboring probability distributions approach or separate from one another into financial network analysis, calculate that measure between both adjacent and nonadjacent stocks, and compare its evolution with entropy, graph distances, and minimum-variance portfolio risk.

The central empirical finding is initially counterintuitive: average curvature rises during crises. Under the authors' terminology, greater curvature indicates greater network robustness. This does not mean that investors' portfolios become safer during crashes. A tightly connected market can be robust as a synchronized network while providing poor diversification. The paper interprets normal market configurations as comparatively fragile and crisis configurations as comparatively robust, because crisis correlations create additional paths and tightly coupled feedback. Preserving this distinction is essential: mechanically interpreting low curvature as high contemporaneous equity risk reverses the principal observed association.

The paper supplies a computationally explicit statistic and retrospective evidence that it tracks important changes in market topology. It does not establish an out-of-sample crash forecasting rule, a causal model of bank defaults, or a calibrated mapping from curvature to portfolio loss probabilities. Although the abstract uses strong language about crises being preceded by changes in robustness, the actual empirical presentation consists mainly of historical plots and annual averages. There is no reported predictive regression, alarm threshold, false-positive rate, or lead-time distribution.

The mathematical motivation combines three ideas: relaxation rates as robustness, entropy as an indicator of robustness, and curvature as related to entropy through optimal transport. These connections motivate the chosen statistic. They should not be read as a complete theorem proving that a particular estimated stock-correlation graph forecasts realized financial fragility. The distinction matters because the probability model underlying relaxation is not estimated from these equity data.

## From returns to a sequence of networks

The historical data come from QuantQuote and cover January 1998 through July 2013. The initial universe consists of stocks comprising the S&P 500 at the time the dataset was obtained. The authors remove stocks lacking observations over the full interval, leaving 388 stocks. This fixed, complete-history universe makes graph size constant and removes missing-data complications, but introduces a material selection issue: it is not the historical S&P 500 membership at each date. Firms that disappeared during the sample are excluded by construction.

For a rolling window of returns, calculate each pairwise correlation $c_{ij}$. To construct a connected backbone, transform correlation into the familiar distance

$$
\widehat d_{ij}=\sqrt{2(1-c_{ij})}.
$$

A minimum spanning tree is then obtained using Prim's algorithm; the reported implementation uses MATLAB 2013a. The tree connects all 388 vertices with 387 edges while minimizing the sum of these transformed distances. Because correlation and transformed distance are monotonically related, the tree favors strong correlation links subject to connectivity.

The authors augment this backbone with every pair whose sample correlation satisfies $c_{ij}\geq 0.85$. They justify the threshold by preceding network studies. The resulting network used in the experiment is **unweighted**, despite the presentation of a more general weighted-graph framework. Thus the correlation magnitude determines which links exist, but does not become the transition probability once the adjacency matrix is formed. For the empirical graph, all retained edges have equal weight before normalizing by node degree.

This two-stage construction has several consequences. The spanning tree prevents disconnected components, so all-pairs graph distances remain finite. Adding high-correlation edges allows crisis-period increases in common movement to change network density rather than merely changing the identity of tree edges. Conversely, strong negative correlations are not added through the positive threshold, even though they can be important for hedging. The topology is deliberately a description of positive comovement, with additional connections forced by the spanning tree.

Advance the return window by one trading day and repeat the construction. The paper reports approximately 4,000 time-varying graphs. Main curvature figures use window lengths $T=22$ and $T=132$ trading days. The former approximates one month and the latter six months. Longer windows smooth the statistic but also blend pre-crisis, crisis, and recovery observations. The graph at a date is therefore a function of the full preceding estimation window, not a direct observation of a latent instantaneous financial network.

The source does not fully specify whether adjusted prices, simple returns, or log returns were used, nor does it state a treatment of every corporate-action or exchange-calendar issue. A faithful replication should record these choices rather than invent them. It should also retain the original static-universe experiment separately from a historically investable-universe robustness exercise. Changing both the universe and graph convention simultaneously makes disagreement with the published figures hard to diagnose.

## The curvature statistic and its computation

Let $G=(V,E)$ be the graph and let $d(i,j)$ be the shortest **hop** distance: the number of edges in the shortest path. This is different from the correlation distance used to construct the spanning tree. Confusing the two changes the optimal-transport problem and consequently the entire curvature series.

In the general weighted construction, edge weight $w_{ij}$ gives a one-step transition distribution from vertex $i$:

$$
s_i=\sum_j w_{ij},\qquad \mu_i(j)=\frac{w_{ij}}{s_i}.
$$

For the empirical unweighted graph, $\mu_i$ is uniform over the neighbors of $i$. A stock with degree ten places probability $0.1$ on each neighbor. The paper does not introduce a separate idleness probability at the starting node, an option used in other graph-curvature conventions. Adding such a probability would define a different statistic.

For distinct vertices $i$ and $j$, the Ollivier-Ricci curvature is equation (4):

$$
\kappa(i,j)=1-\frac{W_1(\mu_i,\mu_j)}{d(i,j)}.
$$

Here $W_1$ is the Wasserstein distance of order one computed using graph-hop distances as transportation costs. The statistic compares the separation between two nodes with the minimal cost of transporting the probability distribution on one node's neighborhood to that on the other's neighborhood. If neighborhoods overlap or are closely linked, their distributions can be matched cheaply, giving relatively high curvature. If neighborhoods lie in separated branches, the transport cost can exceed the distance between centers, giving negative curvature.

This offers more information than an edge's original correlation. Two pairs with the same pairwise correlation can occupy very different positions in the graph: one pair can have many common neighbors and redundant connecting paths, while the other connects two otherwise separated regions. Curvature depends on the surrounding topology through both transition probabilities and transport distances. The claimed financial value comes from this dependence on the network surrounding the pair.

Equation (12) states a finite linear program. With transport variables $\pi_{ab}$, solve

$$
W_1(\mu_i,\mu_j)=\min_{\pi\geq0}\sum_{a,b\in V}d(a,b)\pi_{ab}
$$

subject to

$$
\sum_b\pi_{ab}=\mu_i(a),\qquad \sum_a\pi_{ab}=\mu_j(b).
$$

The marginal constraints ensure that the mass leaving each location equals the source distribution and that the mass received equals the destination distribution. The mass is probability mass, not equity capital or counterparty exposure. The result therefore measures a geometric property of an inferred graph; it is not an optimization of actual trades or bailout transfers.

Only neighbors of $i$ and $j$ have positive marginal mass, so a computational implementation can restrict the transport matrix to these supports. The graph distance matrix must still reflect paths through the complete graph. Distances can be computed once per daily network and reused across pairwise transport programs. Independent pairwise calculations can run in parallel. The authors emphasize this linear-programming structure as computationally tractable, although they provide no comprehensive timing benchmark against alternative network indicators.

For 388 stocks there are $388\times387/2=75{,}078$ distinct unordered pairs. This explains the approximately 75,000 pairs reported in the paper. Curvature is calculated for direct and indirect relationships, not solely the graph's existing edges. An implementation that averages only adjacent-edge curvature would therefore not reproduce their market-wide measure. The article reports average curvature across pairwise relationships; diagonal self-curvature requires a separate convention because the displayed formula has a zero denominator at $i=j$.

## Robustness, entropy, and the scope of the theoretical argument

The authors define robustness using a large-deviation relaxation rate. Suppose $q_\delta(t)$ is the probability that a specified observable remains more than $\delta$ away from its original mean at time $t$ after a perturbation. Their equation (1) is

$$
R=\lim_{t\to\infty}-\frac1t\log q_\delta(t).
$$

A larger rate means the deviation probability decays faster; this is called greater robustness. Fragility changes are assigned the opposite sign, $\Delta F=-\Delta R$. This is a reasonable dynamical definition once an observable, perturbation mechanism, and stochastic evolution are fixed. In the empirical exercise, however, these ingredients are not specified and estimated for stock markets. $R$ is motivational rather than a directly measured outcome.

The paper invokes an entropy-robustness relation, summarized as $\Delta S_e\Delta F\leq0$, and a curvature-entropy relation, summarized as $\Delta S_e\Delta\mathrm{Ric}\geq0$. Combining them motivates a negative relationship between curvature and fragility. These sign expressions should not be mistaken for regression estimates. Nor does pairwise positive association automatically supply a universal transitive statistical relation without additional assumptions.

The transport geometry motivation uses concavity of an entropy functional along Wasserstein-2 geodesics and its relation to lower bounds on Ricci curvature. In a standard sign convention, relative entropy is displacement convex and its negative is displacement concave. The paper's equations (5) and (6) express the concave form. The chosen empirical statistic, however, is an Ollivier curvature defined using Wasserstein-1 transport between graph random-walk measures. The article draws conceptual connections among these frameworks; it does not prove that every smooth-space or Wasserstein-2 characterization carries over without qualification to the daily finite graphs and averaging operation used here.

For the empirical entropy comparison, equation (13) defines a Markov-chain entropy rate. With transition matrix $P=(p_{ij})$ and stationary distribution $\pi$, it is

$$
S_e=\sum_i\pi_i H_i,\qquad H_i=-\sum_j p_{ij}\log p_{ij}.
$$

For a connected undirected unweighted graph, $p_{ij}=1/k_i$ over the $k_i$ neighbors and $\pi_i=k_i/\sum_jk_j$. Thus $H_i=\log k_i$, and the global entropy rate is a degree-weighted average of log degree. This algebraic specialization is an explanatory derivation from their definition. It helps interpret why adding many edges during crisis periods raises entropy. Entropy and curvature can co-move partly because both react to graph density, even though curvature also incorporates graph distances and neighborhood overlap.

The paper argues that curvature preserves pair-level information lost when entropy is contracted to a node or global scalar. That is a defensible distinction between the unaggregated objects. Once curvature is itself averaged over all pairs, some of that location-specific information is also lost. For an institutional risk application, the full curvature matrix or selected pair measures would need to be retained and linked to observable exposures.

## Empirical design and numerical evidence

Figures 3 through 5 compare average curvature, entropy, mean shortest path, and graph diameter across the historical sample. The same main phenomenon appears with 22-day and 132-day estimation windows: crises create denser, more tightly connected correlation graphs, curvature and entropy increase, and path lengths and diameter decrease. Longer windows produce smoother trajectories.

Table 1 provides annual averages using a 22-day window and the 0.85 correlation threshold. Selected values illustrate the scale. In 1998, average curvature is $-0.297$, entropy is $0.941$, mean shortest path is $12.412$, and diameter is $31.361$. In 2000 the respective values are $-0.285$, $0.909$, $14.910$, and $38.210$. By 2008 they are $-0.068$, $2.159$, $7.186$, and $21.044$. In 2011 curvature reaches $0.023$, entropy $2.688$, mean path $6.208$, and diameter $17.770$.

These numbers show that the empirical curvature average is often negative; movement toward zero can still represent a substantial increase. A user should therefore not define crisis solely by positive curvature. They also show that 2011 exhibits stronger changes in some graph statistics than 2008. The measure is a descriptor of the chosen correlation topology, not a one-dimensional ranking of the eventual macroeconomic severity of historical crises.

The interpretation is that herd-like behavior adds links and alternative paths. In graph terms, redundancy makes the structure resilient to some local perturbations and reduces neighborhood separation. In investment terms, the same common movement reduces opportunities to offset exposures. These statements concern different outcomes, so the apparent contradiction between robust networks and risky portfolios is resolved by specifying the meaning of robustness.

There are no statistical significance estimates for the displayed associations, no controls for average correlation or density, and no out-of-sample comparison with simple volatility or correlation indicators. As a result, the empirical evidence establishes resemblance and contemporaneous association. It does not establish that solving thousands of transport problems produces incremental predictive information beyond inexpensive summary statistics. A direct test would regress future risk outcomes on curvature alongside density, average correlation, and volatility, using strictly lagged inputs and held-out periods; that is a proposed extension, not a reported result.

## Minimum-variance portfolios and diversification

The portfolio illustration uses fully invested long-only global minimum-variance portfolios. For an estimated covariance matrix $\Sigma_t$, solve

$$
\min_w w^\top\Sigma_t w
\quad\text{subject to}\quad
\mathbf1^\top w=1,\quad w_i\geq0.
$$

No expected-return forecast is required. The discussion initially introduces the more general Markowitz problem, but the actual application focuses on minimum variance. The long-only constraint is consequential: it avoids relying on large offsetting short positions and makes the result a study of diversification among positive holdings.

Let $B_t$ contain pairwise curvature estimates. Equation (7) defines a portfolio projection

$$
W^{K}_{\mathrm{port},t}=w_t^\top B_t w_t.
$$

The authors emphasize that $B_t$ need not be positive definite. It is therefore not a covariance matrix, a squared distance matrix with a guaranteed interpretation, or automatically a valid substitute in a convex minimum-risk program. In this experiment the portfolio is optimized using covariance, then its existing weights are applied to curvature. There is no optimization that chooses weights by minimizing curvature.

The text states that portfolio weights and the matching correlation network use a 132-day sliding window. Figure 6's caption instead prints 122 days. This discrepancy is visible in the source and should be recorded in a replication rather than silently harmonized. The sensible primary reproduction uses 132 days, consistent with the body and other long-window analyses, while a 122-day sensitivity calculation can diagnose the caption issue. The diagonal convention for $B_t$ also needs documentation because the formula for distinct nodes does not determine it.

Figure 6 shows that the portfolio curvature projection rises around periods when the minimum attainable variance rises. The paper interprets this as diversification melting away in crises. It does not provide an out-of-sample performance table, turnover, transaction costs, concentration statistics, or a trading rule based on the indicator. The covariance estimate is evaluated within the same rolling setting, so the plotted minimum risk should not be read as demonstrated realized risk of a tradable strategy.

## Heavy tails and a mathematical qualification

Page 7 compares Gaussian and Laplace differential entropy at a common variance to motivate the relationship between fat tails and fragility. The displayed Gaussian formula uses $\varphi^2$ while the prose calls $\varphi$ the variance; the Laplace formula uses $\sqrt{\varphi/2}$. These conventions are inconsistent. Written with an unambiguous common variance $v$, the correct expressions are

$$
h_G=\tfrac12\log(2\pi e v),\qquad h_L=1+\log\bigl(\sqrt{2v}\bigr).
$$

Their difference is $\tfrac12\log(\pi/e)$, a positive constant. Both grow at the same rate with respect to $\log v$. Thus the statement that Laplace entropy increases more slowly with variance than Gaussian entropy does not follow under a consistent common-variance parameterization. The valid comparison is that Gaussian entropy is larger at equal variance. This correction follows from the standard density formulas and should not be represented as a finding established by the paper.

Furthermore, lower differential entropy by itself does not establish slower dynamical recovery without a specified process. Two marginal distributions do not determine the transition dynamics governing perturbations. The heavy-tail discussion is best treated as suggestive motivation; it is not a calibrated derivation of crash probability from curvature.

## Reproduction priorities and practical conclusions

A reproduction should first recover the published descriptive series: fixed 388-stock universe, the two return windows, the correlation-distance MST, extra links above 0.85, unweighted adjacency, hop distances, non-lazy neighbor transition measures, all distinct-pair transport distances, and equal-pair average curvature. Save intermediate edge counts, degree distributions, distance matrices, and solver residuals. These expose whether a discrepancy comes from data preparation, graph construction, or transport optimization.

The transport solver should satisfy both marginal constraints to numerical tolerance. Symmetry provides a simple diagnostic because the graph, cost metric, and pair definition are undirected. Nodes with degree one are legitimate and must retain their single-neighbor probability distribution. Disconnected graphs should not occur after the MST step; if they do, an implementation or data problem has been introduced. Replacing the all-pairs calculation with only threshold edges is another easily missed change to the experiment.

The main economic limitation is the difference between a correlation network and a balance-sheet network. Equity correlations do not reveal contractual debt directions, seniority, collateral, or the amount of losses propagated after default. The authors explicitly identify directed networks and specific banking applications as future work. Suggestions involving Ricci flow, emergency lending, market-neutral portfolios, and Ornstein-Uhlenbeck mean reversion are research directions rather than tested policy or investment prescriptions.

For a quantitative investor, the useful deliverable is a geometrically informed measure of the organization of comovement, especially the relation between local neighborhoods and indirect paths. The strongest supported takeaway is that crisis periods substantially reorganize correlation topology in ways detectable by curvature and consistent with entropy and shrinking graph distances. Before treating curvature as a standalone signal, one needs evidence of stability to universe choice and graph threshold, incremental information beyond simpler correlation measures, and predictive value under strict information timing. Those tests would determine whether the geometric construction adds an economically useful measurement layer or mainly repackages the well-known concentration of correlations during stress.

## Algebraic checks that clarify what curvature measures

Two small graph calculations help make the transport construction reproducible. They are explanatory checks, not additional empirical results from the authors. In a complete graph with $n$ vertices and no self-loops, every pair of distinct nodes has hop distance one. Each node's transition measure is uniform over the other $n-1$ vertices. For nodes $i$ and $j$, the two measures agree on all $n-2$ other vertices. The only unmatched mass is $1/(n-1)$ at $j$ in the first measure and the same amount at $i$ in the second. Transporting that mass one hop gives

$$
W_1(\mu_i,\mu_j)=\frac1{n-1},\qquad
\kappa(i,j)=1-\frac1{n-1}.
$$

Thus complete graphs become highly positively curved as their size increases. The example shows why heavy addition of common-correlation links can raise curvature without any reduction in economic losses. In the limiting topology, all nodes look almost interchangeable to a one-step random walk. An investor holding many such stocks can still possess very little independent diversification.

At the other extreme, consider an isolated two-node graph. Each node's random walk moves with probability one to the other node. The two transition distributions remain one hop apart, so curvature is zero, despite perfect connectivity between the two vertices. This calculation also reveals that graph size and the no-self-loop convention matter. Introducing an idleness probability changes both transition measures and can change curvature even though the visible edges stay the same. These examples are useful unit checks for a transport implementation before applying it to noisy financial correlations.

For a weighted graph, multiplying every edge incident to the whole graph by a common positive constant leaves transition probabilities unchanged. If the cost metric also remains the hop metric, curvature is unchanged. It therefore does not measure the absolute dollar scale of financial exposure. A banking application that doubles every institution's leverage while holding proportional connections fixed could have identical curvature under this construction, even though economic default risk rises sharply. Encoding exposure magnitudes or capital buffers would require additional state variables or a different metric.

A final computational implication concerns the number of linear programs. About 75,000 pair calculations across roughly 4,000 daily graphs imply approximately 300 million transport problems per window specification. This is an order-of-magnitude calculation from the reported design, not a published runtime. Neighborhood support restriction, reuse of shortest-path distances, and parallel execution are therefore operationally important. Claiming that the method is tractable does not mean it is cheaper than entropy, which is especially simple on the unweighted graph. Its economic justification must come from the extra pair-level structure that the optimal transport calculation reveals.

These algebraic properties identify precisely what can be learned from the statistic: relative neighborhood geometry under a chosen graph representation. They also specify what must be supplied separately: exposure scale, loss functions, temporal dynamics, and an empirical link to the risk outcome of interest. Keeping those ingredients distinct makes the authors' geometric proposal usable without giving it stronger economic content than the experiment supports.

The threshold of 0.85 is another important sensitivity parameter. Because links enter discretely, small sample-correlation changes near the cutoff can alter several shortest paths and neighborhood distributions at once. A stable risk indicator should therefore be checked across nearby thresholds and estimation windows. The article demonstrates two window lengths but does not present a systematic threshold-selection or threshold-robustness study.
