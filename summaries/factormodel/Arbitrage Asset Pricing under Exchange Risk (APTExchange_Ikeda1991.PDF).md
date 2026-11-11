# Arbitrage Asset Pricing under Exchange Risk

Shinsuke Ikeda, The Journal of Finance 46(1), March 1991, pp. 447–455. Source: [APTExchange_Ikeda1991.PDF](../../Finance/APTExchange_Ikeda1991.PDF), ten PDF pages including archive cover. The source is a theoretical international APT paper, not an estimated factor model or a currency strategy backtest.

## Why this matters and what is new

The paper changes a deceptively important assumption: common factors explain risky-asset returns in each asset's local currency, rather than assuming at the outset that all returns converted into one numeraire share a common factor model. Under this specification, eliminating local factor exposures does not necessarily eliminate currency risk. Ikeda constructs a locally financed asset–bond portfolio that cancels the direct exchange-rate component, and derives a linear pricing relation for the adjusted expected returns. A further implication links asset–currency covariances to differences between currency-specific local-factor prices.

This distinction matters when an international equity model describes local operating or market risk well but does not span exchange-rate fluctuations. A good local factor model cannot simply be relabeled as a complete model of a foreign investor's return. The result also clarifies what currency hedging means in this argument: it cancels direct denomination exposure using local borrowing and lending, rather than minimizing the total covariance of the resulting position with exchange rates.

## Economy, notation, and factor assumptions

There are $N$ countries, initially with one risky asset and one locally riskless national bond in each country. Both securities are denominated in local currency, and perfect international capital markets allow free trading, lending, and borrowing. $N$ is sufficiently large for the APT diversification argument. The one-asset-per-country device is expositional; the paper later discusses multiple assets per country.

Use $r_i$ for the random local-currency return on asset $i$, $\mu_i=E[r_i]$, $p_i$ for its country's locally riskless bond return, and $b_i$ for its $K$ local-factor loadings. Equation (1) is

$
r_i=\mu_i+\sum_{k=1}^K b_{ik}f_k+\epsilon_i.
$

The common factors have zero means. Residuals have zero means, bounded variances, and $E[\epsilon_i\mid f_k]=0$ for each factor. Residuals may be correlated across assets. Bounded individual variances alone are not a general guarantee that arbitrary correlated residuals diversify. The argument uses the paper's additional large-market diversification condition for the chosen portfolio, stated in equation (7); one should not interpret the result as a finite-market theorem requiring no control on aggregate residual risk.

Let $s_i^j$ be the appreciation rate of currency $i$ measured in currency $j$:

$
s_i^j=\bar s_i^j+\delta_i^j,\qquad E[\delta_i^j]=0.
$

For $i=j$, all three currency quantities are zero. Crucially, $\delta_i^j$ is not assumed to follow the same $K$-factor structure as local risky returns. This is the departure from the numeraire-currency formulation discussed in Section II.

The paper uses short-interval returns under conditions permitting Itô calculus. Multiplying local asset price by the exchange rate gives, in the source's return-rate notation,

$
r_i^j=r_i+s_i^j+\operatorname{Cov}(r_i,s_i^j),\qquad
\mu_i^j=\mu_i+\bar s_i^j+\operatorname{Cov}(r_i,s_i^j).
$

These correspond to equations (3) and (5). The covariance term comes from the product's quadratic covariation. This is not a license to replace the exact finite-period gross-return conversion $(1+R_i)(1+S_i^j)$ by the displayed short-interval relation in a monthly implementation. Sampling horizon and return conventions must be reconciled explicitly.

## Why the usual factor-neutral portfolio is insufficient

Write $B$ for the $N\times K$ matrix of local loadings. Choose risky-asset positions $w$ satisfying

$
B^\top w=0,\qquad w^\top\epsilon=0
$

under the paper's diversified-portfolio treatment. The first condition cancels common-factor risk; the second represents eliminated residual risk. Viewed in currency $j$, the portfolio return is nevertheless

$
w^\top r^j=w^\top\mu^j+w^\top\delta^j.
$

This is equation (8). The residual currency component can survive because exposure differs with nationality and need not lie in the span of $B$. Merely setting local betas to zero therefore does not create a riskless international portfolio. One could recover the conventional argument by imposing a factor structure that spans both local returns and currency fluctuations, but that is an extra economic and statistical assumption.

## The financing construction and the theorem

For each risky holding $w_i$, take the opposite position $-w_i$ in country $i$'s national bond. The full $2N$-asset portfolio has weights $(w,-w)$, making it zero cost. Since the local bond return is deterministic, its foreign-currency return is

$
p_i^j=p_i+\bar s_i^j+\delta_i^j.
$

The direct currency innovation in the risky asset is canceled by the opposite national-bond position. Combined with the factor-neutral and residual-diversified risky leg, the resulting return is deterministic:

$
w^\top(r^j-p^j)=w^\top(\mu^j-p-\bar s^j).
$

This is equation (12). No arbitrage requires it to vanish for every admissible $w$ in the null space of $B^\top$. Linear algebra then requires the adjusted expected-return vector to lie in the column space of $B$:

$
\mu^j-p-\bar s^j=B\lambda^j,\qquad j=1,\ldots,N.
$

This is the main theorem, equation (14). There is a $K$-vector of local-factor prices $\lambda^j$ for each measuring currency. Unlike a raw common-currency APT plane, the left side subtracts both local financing rates and expected currency appreciation. In equivalent local-return form, equation (15) is

$
\mu_i-p_i+\operatorname{Cov}(r_i,s_i^j)=b_i^\top\lambda^j.
$

The theorem is a no-arbitrage restriction under the factor and diversification premises. It is not a utility-based derivation of numerical prices of risk, and the paper supplies no estimation procedure for those prices.

The national-bond hedge removes the explicit exchange-rate innovation, but local asset returns may themselves covary with the exchange rate. The source expressly notes that the construction is not a minimum-variance currency hedge. Calling the resulting individual asset–bond position unconditionally independent of currencies would erase the covariance term that is central to the result. Only the full diversified, factor-neutral arbitrage portfolio is riskless under the stated construction.

## Asset–currency covariance restriction

Subtract equation (15) evaluated in currencies $j$ and $\ell$. The currency conversion identities imply that the corresponding difference in asset–currency covariances equals covariance with the appreciation of currency $\ell$ in currency $j$. Thus equation (16) states

$
\operatorname{Cov}(r_i,s_\ell^j)=b_i^\top(\lambda^j-\lambda^\ell).
$

Across assets, this covariance vector lies in the same local-loading span. Differences in prices of local factor risk across measuring currencies account for differences in hedged expected returns, and the covariance term reconciles those representations. This is a restriction on the joint moments conditional on the model; covariances do not become free causal policy variables simply because the theorem expresses them algebraically.

The source counts $N^2$ pricing restrictions: they can be viewed as determining $N$ local expected returns and $N(N-1)$ asset–currency covariances given the relevant rates, currency expectations, and factor prices. Identification in an empirical sample would still require factor normalization, full-rank loadings where needed, and consistent currency quotations. The paper does not provide an identified empirical design or confidence intervals for these objects.

## Relation to Solnik's formulation

Section II adds the assumption

$
\delta_i^j=\sum_k c_{ik}^j f_k+u_i^j.
$

Then common-currency risky returns have composite loadings $b_{ik}^j=b_{ik}+c_{ik}^j$ and composite residual $\epsilon_i+u_i^j$. If those residuals also meet the needed diversification conditions, conventional APT applies in numeraire currency $j$:

$
\mu^j-p_j\mathbf 1=B^j\pi^j.
$

This is equation (19). The loadings now measure total local-plus-currency factor risk, and $\pi^j$ prices that composite risk. Ikeda's theorem instead retains local loadings and explicitly adjusts financing and expected currency appreciation. The two statements answer different model specifications rather than contradict each other.

With many assets per nationality, the paper says that similar reasoning can use local zero-beta portfolios when a locally riskless bond is unavailable. Assets sharing one currency can also exhibit the standard APT relation within that nationality. These extensions are discussed qualitatively rather than developed as a fully separate theorem and proof.

## Reproduction scope and limits

A theoretical reconstruction requires the local factor equation, currency quotation convention, short-interval product rule, the null-space portfolio, opposite local-bond financing, and the row-space argument. Those steps recover the central theorem and covariance corollary without estimating an unreported dataset. An empirical test would additionally need a universe, factor definitions, sample frequency, financing instruments, currency series, residual-diversification diagnostics, and a treatment of estimation error and trading constraints; none is supplied here.

Perfect borrowing and lending, no trading frictions, and the asymptotic treatment are substantial boundaries. A finite collection of correlated residuals, borrowing restrictions, basis costs, or horizon mismatches can leave risk in a purported arbitrage. The paper's practical contribution is to expose the denomination and financing assumptions behind international factor pricing, not to certify a costless implementable trading profit.
