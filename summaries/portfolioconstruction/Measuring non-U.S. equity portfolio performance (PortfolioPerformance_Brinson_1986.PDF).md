# Measuring non-U.S. equity portfolio performance

Gary P. Brinson and Nimrod Fachler, The Journal of Portfolio Management, Spring 1985, pp. 73–76. Source: [PortfolioPerformance_Brinson_1986.PDF](../../Finance/PortfolioPerformance_Brinson_1986.PDF), four scanned pages. The filename says 1986, but the printed pages say Spring 1985. This is the Brinson–Fachler international-equity attribution article, not the later Determinants of Portfolio Performance study.

## Why this matters and what the paper contributes

The paper joins two tasks: selecting a benchmark that actually represents a non-US equity mandate, and decomposing active performance into country allocation, within-country stock selection, and their interaction. The allocation term compares each country's benchmark return with the overall benchmark return. This makes the contribution of an overweight depend on whether the country outperformed the aggregate opportunity set, rather than on whether its absolute return happened to be positive.

The result is an exact single-period accounting decomposition under its stated weight and return conventions. It is not a causal attribution of manager skill, a factor-pricing model, or evidence that a particular active strategy generates alpha. The article provides historical index comparisons and a fully specified three-country numerical illustration, but no new manager-return panel.

## Benchmark coverage and the historical comparison

The authors discuss Capital International Perspective indexes as a commonly used international benchmark family. They value consistent calculation methods, long histories generally reaching back to 1959, industry subdivisions, and availability of local-currency and dollar-adjusted returns. They also warn that coverage varies substantially across countries. At December 31, 1983, included companies represented 59.9% of world capitalization; reported national coverage ranged from 53% for Australia and 55% for Denmark to 81.4% for the Netherlands.

Tables I and II compare twelve CIP national indexes with domestic indexes using monthly local-currency price changes over the five years ending December 31, 1983. These are price-change comparisons, not the net-dividend total-return comparisons of Table III. Regression places CIP return on the left and the selected domestic index on the right, with an intercept.

The Netherlands has reported $R^2=.738$, Switzerland .879, and France .898, showing that benchmark and broader domestic movements are not interchangeable despite considerable common variation. For Japan, CIP annualized price return is 12.44% versus 10.24% for the domestic index, and standard deviations are 10.64% versus 8.80%. The Japanese regression slope is 1.168, compared with 1.076 for Australia, .956 for Italy, 1.072 for Belgium, and 1.052 for Canada. The paper identifies these as significant deviations from one.

Table II's displayed slope $t$ statistics test the coefficient in the regression and should not simply be read as the $t$ statistic for the null slope one. The underlying standard error is needed for that comparison. Intercepts are described as insignificantly different from zero. Exact data vintages, annualization code, and domestic-index constituent histories are not supplied, so reproducing these historical comparisons requires the actual index series.

## Constructing the mandate-consistent non-US index

The correct aggregate benchmark depends on the mandate. A global portfolio can use the World Index, whereas a portfolio excluding US assets should use the corresponding non-US opportunity set. The article argues that the then-used EAFE index omits Canada, South African gold mines, and Mexico, and therefore does not span the entire non-US universe considered by the authors.

Let $P_{US}$ be the US capitalization weight in the World Index, $R_{US}$ its total return, $R_W$ the World Index total return, and $R_X$ the non-US total return. The article derives

$
R_W=P_{US}R_{US}+(1-P_{US})R_X,\qquad
R_X=\frac{R_W-P_{US}R_{US}}{1-P_{US}}.
$

These are single-period arithmetic contribution identities. A numerical reconstruction needs a compatible weighting date and return definition; applying an ending weight to a beginning-weight contribution can fail. The source does not provide a complete multi-period rebalance or index-maintenance algorithm.

Table III uses monthly data and net-yield total returns for periods ending December 1983. Ten-year annualized EAFE and non-US returns are 10.5% and 10.8%, with standard deviations 15.9% and 16.4%. Five-year returns are 9.5% and 10.5%, with standard deviations 14.9% and 15.5%. Three-year returns are 6.5% and 6.4%, with both standard deviations 15.2%. Thus benchmark choice can change measured active performance even when two index labels sound similar. These are historical figures, not assertions about current index membership.

## Exact single-period attribution

For country $x$, let $W_{x,p}$ and $W_{x,i}$ be portfolio and index weights, each summing to one across countries. Let $R_{x,p}$ be the return earned on the portfolio's holdings in that country and $R_{x,i}$ the country-index return. Returns are measured in US dollars. The aggregate index return is $R_i=\sum_xW_{x,i}R_{x,i}$, and the portfolio return is $R_p=\sum_xW_{x,p}R_{x,p}$.

The source assumes a fully invested equity portfolio and no separate active currency strategy. Its equations (3)–(5) define

$
A_x=(W_{x,p}-W_{x,i})(R_{x,i}-R_i),
$

$
S_x=W_{x,i}(R_{x,p}-R_{x,i}),\qquad
I_x=(W_{x,p}-W_{x,i})(R_{x,p}-R_{x,i}).
$

$A_x$ is country or market selection, $S_x$ within-country stock selection at the benchmark weight, and $I_x$ their cross product. An overweight in an above-average country contributes positively, as does an underweight in a below-average country. A benchmark-weight country or a country returning exactly $R_i$ has zero allocation contribution.

Using the benchmark weight for stock selection isolates the return difference from the manager's country-weight decision. This does not make estimated decisions statistically independent; it separates accounting components. A manager's large selection contribution in a major market can exceed that from a much larger percentage outperformance in a small market. The authors therefore suggest examining the unweighted country return differential as a time series when assessing within-market selection ability.

Expanding and collecting terms gives equation (7):

$
A_x+S_x+I_x
=W_{x,p}(R_{x,p}-R_i)-W_{x,i}(R_{x,i}-R_i).
$

Summing countries and using equal total weights yields

$
\sum_x(A_x+S_x+I_x)=R_p-R_i.
$

The per-country combined contribution is not simply $W_{x,p}R_{x,p}-W_{x,i}R_{x,i}$: the difference is $-(W_{x,p}-W_{x,i})R_i$. Those recentering terms cancel only in the total. This distinction prevents an implementation from demanding the wrong bucket-level reconciliation while the aggregate identity is correct.

## Reproducing the worked example

The portfolio holds Japan, the UK, and Germany. Portfolio weights are .55, .30, and .15; index weights are .45, .35, and .20. Portfolio country returns are 6%, -2%, and 4%; index country returns are 4%, 4%, and 6%. Thus

$
R_p=.55(.06)+.30(-.02)+.15(.04)=.033,\qquad
R_i=.45(.04)+.35(.04)+.20(.06)=.044.
$

The active result is -1.1 percentage points, or -110 basis points. The attribution is:

| Country | Allocation, bp | Selection, bp | Interaction, bp | Combined, bp |
|---|---:|---:|---:|---:|
| Japan | -4 | +90 | +20 | +106 |
| UK | +2 | -210 | +30 | -178 |
| Germany | -8 | -40 | +10 | -38 |
| Total | -10 | -160 | +60 | -110 |

For Japan, allocation is $.10(.04-.044)=-.0004$, stock selection $.45(.06-.04)=.009$, and interaction $.10(.06-.04)=.002$. These reconcile exactly to 106 basis points. For the UK, the underweight in a below-benchmark-return country gives positive allocation, but poor stock selection overwhelms it. The interaction is positive because the manager underweights a country in which its selected holdings underperform that country's index.

The scan's explanatory total-return line uses a German return of 6 in one multiplication even though the input table says 4. The reported 3.3% portfolio total and -40-basis-point German selection component are consistent with 4%, not 6%. The equations above explicitly repair this arithmetic transcription inconsistency using the coherent input table and attribution table; they do not change the economic example.

## Extensions and limits

Cash can add a market-timing component that measures the effect of not being fully invested in each equity market. The paper says the necessary equity returns, cash returns, and cash proportions are normally available from accounting records, but does not derive a full extended system. One should not silently treat a cash balance as a stock-selection return or assume that the fully invested identity remains unchanged with unequal total weights.

An active currency strategy requires local-currency analysis plus a currency-selection term and additional interactions. The authors explicitly place the exact currency-factor specification beyond the scope of the paper. Therefore the dollar-return decomposition above includes currency effects inside country returns and does not independently identify currency-management skill. A separate currency attribution algorithm would be an extension, not a reproduction of equations given here.

Other unreported implementation choices include intra-period cash-flow treatment, beginning versus average weights in a practical accounting system, negative weights, countries absent from one side of the comparison, and linking single-period contributions across time. The exact algebra assumes well-defined group returns and matched total weights. Geometrically compounding bucket contributions is not supplied as a multi-period linking method.

## Practical takeaway

The paper provides a reproducible three-component arithmetic attribution once weights and country returns are known, and shows why the benchmark must match the investment opportunity set. Its contribution is precise performance accounting rather than a claim of causal skill or profitable strategy. The most important implementation checks are currency consistency, matched weight totals, the recentered allocation formula, and reconciliation of summed contributions to the observed active return.
