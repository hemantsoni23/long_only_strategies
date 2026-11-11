# Asset Management: A Systematic Approach to Factor Investing — Detailed Quantitative Research Notes

**Title:** Asset Management: A Systematic Approach to Factor Investing  
**Author:** Andrew Ang  
**Year:** 2014  
**Publisher:** Oxford University Press (Financial Management Association Survey and Synthesis Series)  
**ISBN:** 978-0-19-995932-7  
**Structure:** 18 chapters in 3 parts: I Asset Owner (Ch. 1-5); II Factor Risk Premiums (Ch. 6-14); III Delegated Portfolio Management (Ch. 15-18); Afterword, Appendix  
**Source file:** Finance/(Financial Management Association Survey and Synthesis Series) Andrew Ang - Asset Management_ A Systematic Approach to Factor Investing-Oxford University Press (2014).pdf (Drive id `1KPyDbIG_eWFX963c6DLpXqZ3OR0Hjfcv`). The Drive text extraction is truncated after about p. 67 (front matter, Ch. 1, most of Ch. 2), so only those parts were checked against the text; later chapters are summarized at the level of the preface and table of contents, and any figures from them are marked unverified.

---

## Thesis

"The two most important words in investing are *bad times*." Each asset owner has bad times defined by liabilities, income, constraints and beliefs. Factors (growth, inflation, volatility; value, momentum, illiquidity, low risk, etc.) earn premiums because they lose money in the average investor's bad times. An owner who can bear a factor's bad times better than average should harvest it. Asset classes are bundles of factors ("asset allocation is actually factor management"), and delegation adds its own agency bad times. The three parts map to: know your bad times (I); harvest premiums for bearing others' bad times (II); stop managers from loading you with new bad times (III). Ang calls the book opinionated and normative, and gives a reading map: trustees Ch. 1, 14, 16-18; fund managers add Ch. 2-4 and 6-10; individuals Ch. 5 and 12.

---

## Part I — The Asset Owner (verified against text: Ch. 1-2)

### Ch. 1 Asset Owners

Common problems for all owners: meet liabilities, choose risk, oversee intermediaries.

**Sovereign wealth funds.** The Timor-Leste case: GDP per capita under \$900, about 95% of government revenue from oil and gas; Petroleum Fund set up in 2005 held \$11.8bn at end-2012. The payout rule is the estimated sustainable income (ESI) = 3% of *total* petroleum wealth (fund plus NPV of oil still underground) -- closer to theory (Ch. 5) than Norway's 4% of fund value. Actual withdrawals exceeded ESI: 3.8% (2009), 4.8% (2010), 4.3% (2011). Equity allowed at 4% (2010), up to 20% (2012), mirroring Norway (\$685bn at end-2012; 100% bonds, then 40% equity in 1998, 60% in 2007, first real estate with a 5% limit in 2011). SWF motives: precautionary self-insurance (emerging-market reserves average 17% of GDP, Lee 2004; possibly too high) and avoiding Dutch disease. Legitimacy, governance and spending discipline are first-order risks: Russia and Ireland raided funds; Libya, Nauru and Angola are cautionary tales. Transparency is neither necessary nor sufficient (Kuwait, Singapore are opaque but accountable).

**Pensions.** US pension assets exceed 70% of GDP; private pension assets \$6.6tn (2012), and they fell 29% in the 2008 crisis. Non-fixed-income share rose from under 20% (1950s) to over 70%. The DB share of assets fell from about 70% (1984) to 35% (2012); 401(k) active participants rose from 29% to about 90% of DC participants. PBGC insurance is a put for sponsors (premiums would need to rise more than 6x per CBO), encouraging underfunding and risk-taking. Milliman 100 funding ratio 105% (2007), 79% with a record \$327bn deficit (2011). State plans: \$5.7tn liabilities vs under \$2tn assets (Novy-Marx-Rauh), a hole of over \$3tn; Social Security needs an additional \$8.6tn. Public liabilities are understated because they are discounted at expected asset returns although benefits are near risk-free (a Modigliani-Miller violation). LDI (Leibowitz 1986) manages surplus; ABO-based liabilities imply bond-heavy hedging and drove de-risking (top-100 plan equity from 80% in 2005 to under 40% in 2011). Governance pyramid: the least-paid board makes the most important decision (factor risk budget), while the best-paid external managers affect returns least.

**Endowments and foundations.** Foundations must pay out 5% (else 30% excise tax); endowments spend about 4.2% (2012). Restrictions dominate: Harvard (\$30.7bn) is only 17% unrestricted; NACUBO's \$408bn total has 4% unrestricted true endowment and 23% quasi-endowment (the Princeton-Robertson dispute over restricted funds, about \$900m by 2008). HPY moved first into illiquid alternatives: Yale cut public equity from 60% (1980) to 20% by the mid-1990s and raised hedge funds from 0% (1990) to over 20%. By 2012 over half of US endowment assets were in alternatives ("lemmings"; Goetzmann-Oster arms race). Outcome: returns of −3.0% (2008) and −18.7% (2009), 0.3% (2012); since 2001, 4.6% average vs 5.4% for 60/40, with higher volatility (11.3% vs 10.2%), plus liquidity crises (Harvard).

**Individuals.** 70% of family wealth dissipates within two generations. Wealthy families face infighting, nepotism, concentration and overspending. For everyone else, human capital is the dominant asset, housing is levered and illiquid (a short bond position), and health shocks are uninsurable background risk.

### Ch. 2 Preferences

Motivating case: a short-volatility strategy (Merrill Lynch MLHFEV1 variance-swap index, Apr 1989–Dec 2011) vs the S&P 500:

| | Vol strategy | Equities |
|---|---|---|
| Mean | 9.9% | 9.7% |
| Std dev | 15.2% | 15.1% |
| Skewness | −8.3 | −0.6 |
| Kurtosis | 104.4 | 4.0 |

Correlation 0.51; the strategy lost over 70% from Sep to Dec 2008. Identical first two moments, very different bad times.

- **Risk aversion.** CRRA $U(W)=W^{1-\gamma}/(1-\gamma)$ is wealth-homogeneous. For a 50/50 lottery over \$1,000 or \$500, willingness to pay maps to $\gamma$: \$750 (γ=0), \$707 (1), \$667 (2), \$632 (3), \$586 (5), \$540 (10). Evidence puts most people at γ between 1 and 10: Jeopardy contestants near risk-neutral (Metrick), Norwegian survey about 4, Kimball-Sahm-Shapiro about 8, P2P lenders about 3.
- **Mean-variance.** $U=E(r_p)-\tfrac{\gamma}{2}\mathrm{var}(r_p)$, justified by Levy-Markowitz's second-order approximation; it does not assume normality. Optimal risky weight $w^*=(E(r)-r_f)/(\gamma\sigma^2)$. The mean-variance certainty equivalent of the vol strategy for γ=3 is 6.45% -- about the same as equities, which shows exactly what mean-variance misses.
- **Revealed risk aversion.** US stocks/bonds 1926-2011 (correlation 11%): γ=2 → 78% equities, γ=7 → 32%; 60/40 implies γ≈2.8. Stock/T-bill CAL: Sharpe 0.53 with $r_f=1\%$ (0.40 using realized T-bills, 0.0766/0.1918; raw Sharpe 0.58); γ=7 → 40% equities, γ=2 → 139%. Market-implied: \$15.6tn equities vs \$1.5tn T-bills (end-2011) gives $w^*=91.2\%$ and, with premium 10.19% and σ 19.15%, γ≈3.0.
- **Beyond mean-variance.** Safety-first (Roy) and quantile utility (Manski, Rostek; VaR-like). Prospect theory $U=\sum_s w(p_s)U(W_s)$ with loss aversion λ (Tversky-Kahneman 1992: 2.25). With reference point $r_f=1\%$, a CRRA investor with γ=1.68 holds 100% in the vol strategy (a mean-variance investor needs γ=3.86 for the same). At λ=2 the weight drops to about 20%, and above about 2.2 to zero. Disappointment aversion (Gul 1991; reference point = certainty equivalent, well-posed and dynamically consistent) exits fully at A=0.45, i.e. about 2x weight on disappointing outcomes. Habit utility makes risk aversion endogenous (rising as wealth nears habit), so habit investors are poor holders of short vol. Catching-up-with-the-Joneses utility defines bad times relative to peers and drives herding (endowments).
- **Non-monetary preferences** (Norway's ethical exclusions) belong in the utility function. Ang's framing is normative: what owners *should* hold (diversify, rebalance, dis-save in retirement, look through labels to factors, distrust agents).

---

## Parts I-III, remaining chapters (not verified: text truncated)

Chapter scope as given by the table of contents and preface:
- **Ch. 3 Mean-Variance Investing** — diversification, frontier sensitivity, with a twist on socially responsible investing and risk parity (volatility-based allocation, treated as a constrained special case of mean-variance).
- **Ch. 4 Investing for the Long Run** — rebalancing as the foundational long-horizon strategy (short-volatility-like, concave payoff), dynamic hedging demands.
- **Ch. 5 Life Cycle** — human capital as an asset whose risk profile sets the financial portfolio; saving and payout rules based on total wealth.
- **Ch. 6-7 Factor Theory / Factors** — CAPM as the first factor model (bad times = low market returns); pricing kernel $E[mR^e]=0$; macro factors (growth, inflation, volatility) and tradeable styles (value-growth, momentum, illiquidity, low volatility), with rational and behavioral explanations.
- **Ch. 8-9 Equities, Bonds** — equity premium; level factor and term and credit premia.
- **Ch. 10 Alpha (and the Low-Risk Anomaly)** — alpha is defined only relative to a benchmark or factor set; flat security market line.
- **Ch. 11-13** — "real" assets (inflation hedging is conditional), taxes as a factor, illiquid assets (in Ch. 1's cross-reference, top endowments' returns came from manager selection rather than illiquidity per se).
- **Ch. 14 Factor Investing** — optimal factor mixes; reference-portfolio approach (CPPIB case).
- **Ch. 15-18** — delegation and agency; mutual funds; hedge funds and private equity are "not asset classes" but contract labels over factor exposures (Ch. 1-2 state this explicitly).

Figures from earlier versions of these notes that could not be checked against the extracted text (treat as unverified): US–Japan equity correlation 35.4% (59% post-2000); sin-stock exclusion raising minimum-variance volatility only from 12.05% to 12.10%; a low-volatility strategy with alpha 3.44%/yr and beta 0.73 vs Russell 1000; BAB about 0.42%/mo; CalPERS returns about 90% spanned by a stock/bond mix; Baa spread 2.09% vs realized excess return 0.86%.

---

## Assessment

- **Strong:** a single organizing principle (marginal utility / bad times) applied consistently from preferences to factor premia to delegation. The Ch. 2 vol-strategy example is the cleanest demonstration of why Sharpe ratios and mean-variance certainty equivalents fail for negatively skewed payoffs. The governance material (SWF legitimacy, PBGC put, public-plan discount rates, endowment herding) is unusually concrete.
- **Weak or dated:** data end about 2012. The endowment-vs-60/40 comparison covers one decade dominated by the crisis. Implied-γ exercises depend heavily on sample moments (1926-2011 equity premium about 10%). Normative prescriptions (e.g. total-wealth payout rules, factor-based benchmarks) are harder to implement than the text suggests.
- **For a quant PM:** (1) evaluate strategies by their bad-times profile and higher moments, not Sharpe alone -- λ≈2 loss aversion eliminates a Sharpe-comparable short-vol allocation; (2) regress "alternatives" on liquid factors before paying for them; (3) risk aversion backed out of a 60/40 policy (γ≈3) is a sensible default for utility-based sizing; (4) the owner's funding and liquidity structure (spending rules, PBGC-style puts, restricted capital) determines which factor premia it can actually harvest.
