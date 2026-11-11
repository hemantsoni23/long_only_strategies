# An empirical analysis of herd behavior in global stock markets

**Thomas C. Chiang and Dazhi Zheng (2010).** *Journal of Banking & Finance* 34, 1911–1921. DOI: 10.1016/j.jbankfin.2009.12.014. Source: [Crowding_Chiang_2010.pdf](../../Finance/Crowding_Chiang_2010.pdf). References use journal pages or numbered equations and tables.

## Why this matters

A country's stocks can move together because investors follow one another, because they respond to common information, or because their risk exposures change. This paper studies an observable implication associated with herding: cross-sectional return dispersion grows less rapidly, or falls, when aggregate market movements become large. It extends that regression-based approach to 18 markets, adds US-market variables, and examines up/down asymmetry and crisis subsamples.

The contribution is a comparative empirical specification, not direct observation of investor imitation. A negative quadratic coefficient is the paper's operational herding signal. It is evidence consistent with herding under the maintained dispersion model, not a causal identification of irrational behavior, information suppression, or trading interactions.

## Data: industry indices rather than individual trades

The observations are daily Datastream **industry price-index returns**. Each market's return is the equal-weighted mean of its industry returns; the cross section is not a common list of individual stocks, investor holdings, or executed trades. Industry aggregation and the number of industries differ across countries, which affects comparability.

The main data section and table notes start the longest samples on **April 25, 1989**, ending April 24, 2009. The abstract and conclusion instead say May 25, 1988. This date conflict is unresolved; the detailed data section and repeated table notes are the implementation reference.

| Group used in paper | Markets, number of industries | Starting dates |
|---|---|---|
| Advanced | Australia 109; France 138; Germany 125; Hong Kong 91; Japan 145; UK 140; US 155 | April 25, 1989 for all seven |
| Latin American | Argentina 59; Brazil 70; Chile 59; Mexico 67 | July 28, 1993; July 5, 1994; July 5, 1989; June 19, 1991 respectively |
| Asian | China 64; South Korea 88; Indonesia 53; Malaysia 74; Singapore 89; Thailand 63; Taiwan 56 | China August 12, 1996; Indonesia June 16, 1992; Thailand September 3, 1990; Taiwan July 4, 1989; the others April 25, 1989 |

Hong Kong and Japan are geographically Asian and use the Asian timing convention for US variables even though the paper places them in its advanced-market reporting group. The counts $N$ in Table 1 are industry counts, not time-series sample sizes.

For industry $i$ in country $c$,

$$
R_{i,t}=100\{\log P_{i,t}-\log P_{i,t-1}\},\qquad
R_{m,t}=\frac{1}{N}\sum_{i=1}^{N}R_{i,t}.
$$

Returns are expressed in percentage points. Using decimal returns without rescaling the squared-return coefficients would change their numerical values. The source describes missing holiday information as carefully inspected or interpolated, but gives no exact interpolation, stale-price, or trading-calendar rule. It does not supply index identifiers, constituents, historical classification changes, currency conventions, dividend treatment beyond its description as price indices, or a rule for varying $N$ with missing observations.

Mean daily cross-sectional absolute deviation is 0.8486 for the US, 0.8793 for Japan, 1.3538 for Hong Kong, 1.6100 for China, and 1.6987 for Indonesia (Table 1). Some emerging-market series have extreme kurtosis: 152.81 for Brazil and 235.7591 for Chile. These are descriptions of dispersion distributions, not the return kurtosis of a representative stock.

## Dispersion statistics and the maintained test

The paper discusses two measures:

$$
CSSD_t=\sqrt{\frac{1}{N-1}\sum_{i=1}^{N}(R_{i,t}-R_{m,t})^2},\qquad
CSAD_t=\frac{1}{N}\sum_{i=1}^{N}|R_{i,t}-R_{m,t}|.
$$

The reported regressions use CSAD, which is less sensitive to extreme deviations than the squared-deviation measure. The authors report similar CSSD conclusions and weighted-least-squares results as available on request; neither complete robustness output is reproduced in the article.

The baseline equation is

$$
CSAD_t=\gamma_0+\gamma_1R_{m,t}+\gamma_2|R_{m,t}|+\gamma_3R_{m,t}^{2}+\varepsilon_t.
$$

Earlier work's restricted version sets $\gamma_1=0$. Adding the signed return allows a different linear response in positive and negative markets. Writing $x=|R_m|$, the two conditional curves are

$$
f_+(x)=\gamma_0+(\gamma_2+\gamma_1)x+\gamma_3x^2,\qquad
f_-(x)=\gamma_0+(\gamma_2-\gamma_1)x+\gamma_3x^2.
$$

Thus $\gamma_2\pm\gamma_1$ describe the linear components with respect to *return magnitude*. The full slopes also include $2\gamma_3x$. The source's asymmetry ratio $(\gamma_2+\gamma_1)/(\gamma_2-\gamma_1)$ concerns those linear components; it is not a constant ratio of full marginal responses at every market move.

The empirical criterion is a significantly negative $\gamma_3$. Its mechanism is concavity: unusually large aggregate moves produce less dispersion than a linear extrapolation would predict. A negative quadratic term does **not** mean dispersion declines at every observed return magnitude. Actual decline requires a sufficiently large $x$ relative to the relevant linear coefficient. Nor should the polynomial be extrapolated until it predicts negative dispersion, which is impossible by construction.

The authors motivate the null with rational asset-pricing models and contrast it with investors clustering around consensus under stress. That economic interpretation relies on the adequacy of the null. Common-factor shocks, nonlinear fundamentals, changing industry composition, and volatility dynamics could also change the dispersion-return relation. The specification does not observe private information, prove that it was suppressed, or distinguish rational from irrational imitation.

The regressions use Newey–West heteroskedasticity/autocorrelation-consistent inference. The article does not state the bandwidth, finite-sample correction, or exact software convention. Significance markers denote 10%, 5%, and 1%. Reported $R^2$ values are adjusted $R^2$. There is no reported multiple-testing adjustment across countries, specifications, and crisis comparisons.

## Baseline results: Table 2

The following coefficients are for the unrestricted equation including the signed return term; $t$-statistics are in parentheses.

| Market | Quadratic coefficient $\gamma_3$ | Market | Quadratic coefficient $\gamma_3$ |
|---|---:|---|---:|
| Australia | −0.0124 (−3.51) | China | −0.0064 (−3.43) |
| France | −0.0209 (−5.44) | South Korea | −0.0208 (−9.27) |
| Germany | −0.0258 (−9.97) | Taiwan | −0.0613 (−19.32) |
| Hong Kong | −0.0023 (−1.46) | Indonesia | −0.0251 (−8.43) |
| Japan | −0.0086 (−3.79) | Malaysia | −0.0103 (−12.47) |
| UK | −0.0180 (−4.67) | Singapore | −0.0131 (−6.26) |
| US | −0.0015 (−0.78) | Thailand | −0.0297 (−11.55) |
| Argentina | +0.0097 (+3.35) | Brazil | +0.0431 (+14.10) |
| Chile | +0.0935 (+24.09) | Mexico | +0.0285 (+7.17) |

The US coefficient is not significant. All four Latin American coefficients are positive, contrary to the domestic concavity criterion. Most advanced markets and all seven countries in the paper's Asian group have significant negative coefficients. Hong Kong is a specification-sensitive exception: its restricted coefficient is −0.0053 with $t=-3.45$, but adding the signed return reduces it to the insignificant value above.

The baseline US regression has intercept 0.6366, signed-return coefficient 0.0140, absolute-return coefficient 0.2992, and adjusted $R^2=0.35$. Positive and negative linear components are therefore 0.3132 and 0.2852, even though the quadratic term supplies no significant evidence of domestic herding. This illustrates why asymmetry and herding are separate questions.

These cross-country tests do not establish that every investor in a country herds, or that absence of significant concavity proves fully rational decision making. They describe an aggregate industry-return relationship over unequal historical samples.

## Adding US dispersion and market shocks

Equation 4 augments the domestic regression:

$$
CSAD_{c,t}=\gamma_0+\gamma_1R_{c,t}+\gamma_2|R_{c,t}|+\gamma_3R_{c,t}^{2}+\gamma_4CSAD_{US,t^*}+\gamma_5R_{US,t^*}^{2}+\varepsilon_{c,t}.
$$

For Asian markets, including Hong Kong and Japan, $t^*=t-1$ to account for the US trading day's timing. Other non-US markets use same-date US variables. This is a historical regression convention: same-date US closing data may not be available at another market's decision time, so it is not automatically a tradable forecast.

A positive $\gamma_4$ indicates co-movement in dispersion. The paper interprets a negative $\gamma_5$ as herding around US market conditions conditional on the other regressors. The two coefficients should not be conflated: a positive dispersion coefficient does not itself establish a herding mechanism.

Table 3 finds positive, statistically significant US-dispersion coefficients in all 17 non-US equations, ranging from 0.0779 for Chile to 0.5319 for the UK. Adjusted explanatory power often rises: France from 0.38 to 0.54, Germany from 0.45 to 0.60, and the UK from 0.38 to 0.60. This demonstrates predictive association conditional on the regressors, not a causal direction of information transmission.

Selected contrasts are particularly informative:

| Market | Domestic quadratic, $t$ | US quadratic, $t$ | US dispersion coefficient |
|---|---|---|---:|
| Hong Kong | +0.0006, +0.11 | −0.0130, −2.65 | 0.4445 |
| China | −0.0056, −1.10 | −0.0068, −2.00 | 0.2610 |
| Brazil | +0.0737, +3.23 | −0.0379, −3.94 | 0.3351 |
| Chile | +0.0975, +2.74 | −0.0154, −2.94 | 0.0779 |
| Mexico | +0.0349, +1.25 | −0.0088, −2.28 | 0.3158 |
| Argentina | +0.0109, +1.10 | −0.0001, −0.04 | 0.2155 |

For Hong Kong and China, domestic concavity is not significant after US controls, while the US squared-return term is negative and significant. Brazil, Chile, and Mexico also meet the foreign-term criterion without meeting the domestic one. Argentina does not. Australia has a *positive* US quadratic coefficient, 0.0039, significant only at 10%; Singapore's is positive but insignificant. Thus the prose's statement that all US quadratic coefficients except Australia's are negative is too broad.

A footnote reports a Hong Kong regression with Chinese market variables: the relevant Chinese herding coefficient is −0.0099 with an absolute $t$-statistic of 3.52; the reverse direction is not significant. The article does not give the full equation estimates. A joint test of the two US variables reportedly rejects their joint absence at 1%, but numerical test statistics are available only on request.

## Up-market and down-market curvature

With $D_t=1$ when the local market return is negative and zero otherwise, equation 5 is

$$
CSAD_t=\gamma_0+\gamma_1(1-D_t)R_{m,t}+\gamma_2D_tR_{m,t}+\gamma_3(1-D_t)R_{m,t}^{2}+\gamma_4D_tR_{m,t}^{2}+\gamma_5CSAD_{US,t^*}+\gamma_6R_{US,t^*}^{2}+\varepsilon_t.
$$

This changes both the linear and quadratic terms by market direction, while retaining a common intercept and common US coefficients. The equality test is $H_0:\gamma_3=\gamma_4$. It asks whether curvature differs, rather than whether one coefficient is significant and the other is not. Those are distinct tests.

Table 4 reports stronger up-market concavity for Hong Kong (−0.0143 versus +0.0035; equality $p=0.0021$), Japan (−0.0164 versus −0.0024; displayed $p=0.0000$), South Korea (−0.0266 versus −0.0154; $p=0.0365$), Indonesia (−0.0351 versus −0.0179; $p=0.0513$), and Malaysia (−0.0125 versus −0.0065; $p=0.0188$). Indonesia's difference meets 10% but not 5% significance.

China's up coefficient is −0.0098 and significant, while its down coefficient −0.0031 is not; nevertheless the equality test gives $p=0.2848$. It is therefore incorrect to infer a statistically established asymmetry in China merely from the two separate significance labels. Taiwan also has no significant curvature difference ($p=0.5596$). The US has neither significant up nor down concavity and no significant difference ($p=0.6372$).

Argentina has an equality-test $p=0.0271$, but its up coefficient is positive and its down coefficient insignificant. Asymmetry alone does not mean herding under this model. The paper's broader conclusion about more pronounced Asian asymmetry should be read with these country-specific qualifications.

## Crisis design and results

Equation 6 adds dispersion and squared-return variables for the crisis-origin market to the domestic and US variables. If the origin is the domestic country or the US, duplicate regressors are omitted. The crisis windows are fixed historical episodes:

| Episode | Origin | Estimation window |
|---|---|---|
| Asian crisis | Thailand | July 1, 1997–December 31, 1998 |
| Mexican crisis | Mexico | December 22, 1994–December 31, 1995 |
| Argentine crisis | Argentina | January 1–December 31, 1999 |
| Credit crisis | US | March 1, 2008–March 31, 2009 |

The article's “Argentine crisis” is its 1999 window; it should not silently be replaced by a different Argentine crisis date. The Russian crisis is omitted, with the authors citing missing industry data and proximity to the Argentine episode.

For each origin the domestic quadratic coefficient is negative: Thailand −0.0392 ($t=-1.90$, only 10% significance), Mexico −0.0497 ($t=-2.06$), Argentina −0.0397 ($t=-2.56$), and the US −0.0074 ($t=-1.99$). These are in-sample crisis estimates, not forecasts of crisis onset.

The cross-border terms differ by episode. During the Mexican crisis Argentina's coefficient on Mexican squared returns is −0.0350 ($t=-2.99$), and its coefficient on Mexican dispersion is +0.2654 ($t=3.60$). During the Argentine episode Brazil's coefficient on Argentine squared returns is −0.0517 ($t=-2.81$), with dispersion coefficient +0.1950 ($t=2.68$). During the Asian crisis Singapore's Thai squared-return coefficient is −0.0062 ($t=-2.92$), while its own quadratic term is +0.0018 and insignificant. Thus foreign and domestic concavity can tell different stories within the same episode.

The authors compare crisis curvature with a tranquil sample of equal length selected before or after the crisis, depending on what they consider appropriate. Exact tranquil dates are not listed, preventing exact reproduction of those comparisons. For Mexico's own crisis, crisis minus tranquil curvature is −0.0679 with equality-test $p=0.0048$; for Argentina's own episode it is −0.0444, $p=0.0042$. The US comparison during the Mexican crisis gives −0.2114, $p=0.0033$; during the Argentine episode it gives −0.1271, $p=0.0580$.

There is a material table-label problem in the 2008–2009 comparison. Table 5A4 assigns −0.0152 to Hong Kong, −0.0115 to Japan, −0.0079 to the UK, −0.0284 to Argentina, −0.0185 to Brazil, −0.0226 to Chile, +0.0457 to Mexico, and +0.0001 to China. Table 5B4 assigns those same crisis coefficients to differently ordered country labels: for example −0.0152 appears under UK and +0.0457 under Hong Kong. This is visible in the original PDF, not merely a text-extraction error. The associated country-specific crisis/tranquil claims cannot be reconciled reliably without the original code or corrected table. The note therefore does not silently remap them.

For the US, whose row is consistent, credit-crisis curvature −0.0074 compares with tranquil +0.0040, a difference −0.0114 with $p=0.0022$. During that episode, positive dispersion co-movement is widespread, while evidence from US squared returns is much less uniform. This distinguishes general global co-movement from the narrower herding criterion.

## Reproduction limits and practical reading

A reproducible implementation should construct country-specific equal-weighted industry means and CSAD from the exact underlying series; preserve percentage-point units; specify holiday and missing-data rules; align US information by actual trading time; and fit the nested baseline, foreign-control, directional, and crisis equations with a disclosed HAC convention. It should preserve the article's crisis dates and disclose exact matched tranquil windows. None of these steps requires estimating individual-stock betas.

The article leaves essential inputs unavailable: index identifiers and membership, interpolation policy, return adjustments, exact observation counts after alignment, Newey–West bandwidth, matched tranquil dates, complete robustness results, and a correction to the inconsistent crisis-country labels. These gaps limit coefficient-level replication even though the main equations are explicit.

The finding is best used as a warning that domestic dispersion models can change materially when foreign conditions and market direction are included. It supports examining cross-border concentration and the stability of diversification during stress. It does not establish that a particular observed market move was caused by imitation, identify an exploitable anomaly after costs, or supply a calibrated portfolio-allocation rule. The causal claims about contagion in the article are stronger than the observational regressions alone can support.
