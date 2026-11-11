# Stock Price Predictability

**Author:** Wayne E. Ferson (Boston College, Carroll School of Management; Collins Chair in Finance)  
**Publication:** Working draft for *The New Palgrave Dictionary of Economics*, 2nd ed., Palgrave Macmillan (the draft header reads "Durlaf and Arrow, Eds.")  
**Drafts:** first 28 August 2006; this draft 17 October 2006 (file dated 2008)  
**Source file:** `Finance/StockPrediction_Ferson_2008.pdf` (20-page draft)  
**Summary prepared:** 2026-09-25 (Scholar batch_2026-09-25_1)

---

## Scope and framing
This is a short dictionary entry covering developments after Fama (1970). It uses Fama's information sets, covers only weak-form (past prices) and semi-strong-form (public information) predictability, and leaves out strong-form evidence such as insider trading. Two readings of any predictability are set against each other:

1. **Exploitable inefficiency.** Frictions (trading costs, taxes, information costs) or cognitive biases stop arbitrageurs from bidding the pattern away (the Friedman 1953 / Samuelson 1965 logic is the foil). An investor who avoids the friction or bias profits.
2. **Efficient-markets predictability.** $R=E(R\mid\Omega)+u$ with $E(u\mid\Omega)=0$, so only time variation in required expected returns (rates, risk, risk aversion) is forecastable, and there need be no abnormal profit. The natural framework is conditional asset pricing (Ferson 1995).

Predictable second moments (ARCH/GARCH, Engle 2004) and third moments (Harvey–Siddique 2001) are mentioned but not covered.

## Weak form
Organizing regression, with $R_t$ log returns and $r(t,t+H)=\sum_{j=1}^H R_{t+j}$:
$$r(t,t+H)=a_H+\rho_H\,r(t-H,t)+\varepsilon(t,t+H). \tag{1}$$
Variance ratios $\mathrm{Var}\{r(t,t+H)\}/(H\,\mathrm{Var}(R_t))$ (Working 1949; Lo–MacKinlay 1988) are functions of autocorrelations (Cochrane 1988). Kaul (1996) shows most weak-form statistics are differently weighted combinations of autocorrelations at different lags.

- **Daily and intraday.** Dependence here is statistically significant but produced by bid–ask bounce (Roll 1984) and nonsynchronous trading (Fisher 1966; Scholes–Williams 1977). It is neither tradable nor evidence of discount-rate variation.
- **Weekly.** If $E(R\mid\Omega)$ is AR, then realized returns are ARMA with AR and MA coefficients of **opposite sign**: a rise in expected returns raises future means but lowers today's price through discounting. The two effects offset, so raw autocorrelations can be small. Conrad–Kaul (1988, 1989) estimate AR coefficients near 0.5 for weekly portfolio returns, explaining up to 25% of the variance of a small-firm portfolio. Nonsynchronicity still contaminates weekly data (Lo–MacKinlay 1990; Muthuswamy 1988). Boudoukh–Richardson–Whitelaw (1994) find little weekly predictability in index futures, which are free of stale prices.
- **Relative predictability (cross-sectional (1)).** Jegadeesh (1990) finds monthly continuation and Lehmann (1990) weekly reversals. Jegadeesh–Titman (1993) use US data 1927–89, focusing on 1965–89: the top 20% of six-month winners beat losers by about 1% per month over the next six months.
  - Risk explanations mostly fail; a partial exception is downside-risk exposure (Ang–Chen–Xing 2001).
  - Behavioral stories: biased self-attribution (Daniel–Hirshleifer–Subrahmanyam 1998) and the disposition effect (Grinblatt–Han 2003).
  - Lesmond–Schill–Zhou (2004) and Korajczyk–Sadka (2004) conclude that trading costs consume the profits.
- **Long horizon.** Fama–French (1988) find U-shaped autocorrelations across horizons, with mean reversion at 4–5 years. This is compatible with stationary time-varying expected returns or with temporary mispricing. DeBondt–Thaler (1985) find five-year reversals of past winners and losers, which they read as overreaction. The reversals are concentrated:
  - in January (Zarowin 1990; Grinblatt–Moskowitz 2003), consistent with tax-loss selling;
  - in high idiosyncratic-risk stocks (McLean 2006), consistent with limits to arbitrage.
  
  Barberis–Shleifer–Vishny (1998), DHS (1998) and Hong–Stein (1999) aim to explain short-run momentum and long-run reversal jointly. Ferson's verdict: "the jury is still out."

## Semi-strong form
$$r(t,t+H)=\alpha_H+\beta_H'Z_t+v(t,t+H). \tag{2}$$
Three groups of predictors:
- **Valuation ratios:**
  - detrended price (Keim–Stambaugh 1986);
  - D/P (Rozeff 1984; Campbell–Shiller 1988; Fama–French 1989);
  - B/M (Pontiff–Schall 1998; Kothari–Shanken 1997);
  - payout including repurchases and other noncash payouts (Boudoukh et al.; Lei 2006);
  - consumption/wealth, cay (Lettau–Ludvigson 2001).
  
  All give significant $\beta_H$. Rationale: with $P=c/(R-g)$, $c/P=R-g$, so a varying D/P must forecast returns, growth, or both. Campbell–Shiller show the logic holds approximately with time-varying $R,g$ and find that D/P does not forecast dividend growth. Cochrane (2006) turns this around: if D/P does not forecast cash flows, it must forecast returns.
- **Calendar effects:** January, turn of the month, holidays, Mondays, time of day, sunlight, geomagnetic storms (reviews: Haugen–Lakonishok 1988; Schwert 2003).
- **Other variables:**
  - The short T-bill yield forecasts with a negative sign (Fama–Schwert 1977, read as expected inflation). Ferson (1989) argues this implies interest-rate-driven time variation in systematic risk.
  - Default spreads (Keim–Stambaugh 1986), Treasury spreads (Campbell 1987), conditional volatility (Merton 1980). Fama–French (1989) tie the 1980s predictors to the business cycle.
  - Later candidates: equity share of new issues and dividend initiations (Baker–Wurgler), investment plans (Lamont 2000), average idiosyncratic volatility (Polk–Thompson–Vuolteenaho 2004), corporate cash (Greenwood 2004), share issuance (Pontiff–Woodgate 2006), presidential party (Santa-Clara–Valkanov 2003).

**$R^2$ and economic size.** $R^2$ is about 10–15% or less at monthly to annual horizons and up to 40% or more at 4–5 years. Expected returns are more persistent than returns, so predictable variance accumulates faster with horizon. Small $R^2$ can still matter because equity is a long-duration asset. Ferson's example: $P/E=15$ and payout $k=0.6$ give $c/P=4\%$, and with $g=3\%$, $R=7\%$. A one-point shock to $R$ moves value by about 20%: $(R-g)$ goes from 4% to 5%, so price falls by exactly 20%. He notes this overstates the effect, since a shock to $R$ usually also moves expected cash flows. Portfolio-choice studies (Kandel–Stambaugh 1996; Campbell–Viceira 2002; Fleming–Kirby–Ostdiek 2001) find economically large effects from low-$R^2$ predictability.

## Methodology
Ferson argues that the literature's main contribution may be methodological. The key problems are:
- **Data mining and selection bias.** A search that accounts for the number of tries (White 2000) differs from naive mining. With 100 independent candidate variables, about 5 will be "significant" at 5% by chance. "There probably have been at least as many regressions run using [CRSP] as there are numbers in the database." Only significant results get published.
- **Out-of-sample evidence is mixed.**
  - For: Fama–French 1989; Pesaran–Timmermann 1995; international evidence (Harvey 1991; Solnik 1993; Ferson–Harvey 1993, 1999).
  - Against: Goyal–Welch 2003, 2004; Simin 2006.
  - A true predictor can still lose to the historical mean out of sample (Campbell–Thompson 2005; Hjalmarsson 2006).
- **Other issues:** finite-sample bias, unreliable standard errors, spurious regression (Granger), regime shifts, and in particular their interactions. Ferson–Sarkissian–Simin (2003) study data mining combined with spurious regression. Little work had been done on these interactions.

## Ferson's perspective
- **Skeptic's case.**
  - The efficient-markets logic.
  - Weak-form effects retreat into subsamples once sliced. Momentum is concentrated by industry, stronger in larger stocks and stocks above \$5, absent before 1940, stronger after 1968 and in expansions. Reversals are concentrated in small, low-priced and high idiosyncratic-risk stocks, in January, and in earlier samples.
  - "For each approach to slicing and dicing the data there is a clever story."
  - Some direct semi-strong predictability has weakened in recent samples, either because it was never there or because it was traded away.
- **Believer's case.**
  - Persistent time-varying expected returns imply predictability, and recession/expansion patterns are intuitive.
  - Conditional models with time-varying premia largely explain lagged-variable predictability (Ferson–Harvey 1991; Ferson–Korajczyk 1995; Avramov–Chordia 2006).
  - Momentum held out of sample (Jegadeesh–Titman 2001, 1990–98) and outside the US.
  - Semi-strong predictors work across countries, periods, bonds, futures and macro growth rates.
  - Ferson–Heuson–Su (2005) find no recent weakening. They regress stocks on firm-specific predictors and use the average covariance of fitted values, which approximates the variance of a large portfolio's expected return. These predictors are also less mined.
  - Campbell–Thompson (2005) find step-ahead support in recent data.
- **Conclusion:** weak-form evidence is "more fragile and less compelling" than semi-strong evidence. Conditional asset pricing with time-varying expected returns, risk and volatility is one of the field's most significant developments of the past two decades, including for performance evaluation.

## Assessment
- As a map of the pre-2006 literature it is balanced and accurate. Its most useful content for a researcher is the methodological warning list and the Conrad–Kaul point that raw autocorrelations understate persistent expected-return variation.
- It gives almost no magnitudes beyond a handful of classic figures and does not adjudicate the econometric disputes. Stambaugh-type bias with persistent predictors and overlapping-observation inference are covered only by reference (Boudoukh–Richardson 1994).
- The distinction that matters in practice is between predictability absorbed by time-varying risk premia and residual predictability. The first is beta to be harvested in allocation or timing. Only the second is a candidate for alpha, and it is exactly where naive mining and costs (momentum) bite.
- Post-2006 developments are out of scope: Welch–Goyal 2008, Campbell–Thompson restrictions, forecast combination and machine-learning predictors, momentum crashes.
