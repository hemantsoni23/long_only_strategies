# The Profitability of Technical Analysis: A Review
**Authors:** Cheol-Ho Park, Scott H. Irwin
**Year:** 2004
**Journal/Venue:** AgMAS Project Research Report 2004-04, University of Illinois at Urbana-Champaign (October 2004)
**Source file:** Finance/AbnormalReturnsTechnicalAnalysis_IrwinPark_2004.pdf (the Drive text extraction truncates inside the final summary section; the conclusions below rely on the abstract and the per-category syntheses)

## Question and scope

What does the accumulated survey, theoretical and empirical evidence say about whether technical trading rules earn *economic* profits, i.e. risk-adjusted returns net of transaction costs (Jensen's 1978 definition of efficiency relative to an information set $\Omega_t$ = past prices)? The report covers 42 "early" empirical studies (Donchian 1960 through 1987) and 92 "modern" studies (Lukac, Brorsen and Irwin 1988 through Sapp 2004), plus practitioner surveys and theory. Roughly half of all empirical studies since 1960 appeared in 1995-2004.

Headline tally (modern studies only): **58 positive, 24 negative, 10 mixed.** The authors immediately qualify it: most studies suffer from data snooping, ex post selection of rules or search technologies, and weak treatment of risk and costs. Modern studies indicate profits "consistently" in a variety of speculative markets **at least until the early 1990s**.

## Surveys and theory (brief)

- Practitioner surveys (Smidt 1965; Group of Thirty 1985; Brorsen-Irwin 1987; Taylor-Allen 1992; Menkhoff 1997; Lui-Mole 1998; Cheung-Chinn 2001; Oberlechner 2001): technical analysis is widely used in futures and FX; about 30-40% of practitioners regard it as important for horizons up to about 6 months. The authors found **no survey evidence for stock-market traders**.
- Theory. Martingale / random-walk models rule out TA profits: with $E[P_{t+1}\mid\Omega_t]=P_t$ (or the sub-martingale version $\ge P_t$), no rule based on $\Omega_t$ beats buy-and-hold in expectation. Models that allow profits: noisy rational expectations (Grossman-Stiglitz; Hellwig; Brown-Jennings 1989 and Grundy-McNichols 1989, where past prices help infer others' private signals; Blume-Easley-O'Hara 1994 on volume), feedback/noise-trader models, herding (Froot-Scharfstein-Stein 1992), disequilibrium adjustment (Beja-Goldman 1980), and chaos/agent-based models. Neftci (1991) shows that dual moving averages are among the few TA rules whose signals are Markov times, i.e. they use no future information. Many chart patterns ("head-and-shoulders", "triangles") are not.

## Early studies (pre-1988)

- **Fama-Blume (1966)**, 30 DJIA stocks 1956-62, 24 filters (0.5%-50%): after commissions only 4 of 30 stocks show positive average filter returns, and filters lose to buy-and-hold for all but 2 stocks even before commissions. The one exception: the 0.5% filter on long positions earned 12.5% net of a 0.1% clearing fee against 9.86% for buy-and-hold, which Fama-Blume dismiss as unimplementable. The paper's own criticism: averaging across filters and stocks can hide rules that work for some assets (Sweeney 1988).
- **Stevenson-Bear (1970)**, July corn and soybeans 1957-68: stop-loss and filter/stop-loss combinations beat buy-and-hold net of costs.
- **Sweeney (1986)**, FX: a CAPM-based risk-adjusted $X$-statistic; small filters (0.5%, 1%) significant on \$/DM 1975-80, with 1.6%-3.7% annual excess returns after 0.125% round-trip costs. Across 10 currencies, filters significantly beat buy-and-hold in 22 of 70 cases in the first subperiod and 21 in the second. Sweeney notes that time-varying risk premia could reconcile this with efficiency.
- **Verdict:** little evidence in stocks; sizable net profits in futures and FX.
- **Weaknesses:** one or two rule families tested exhaustively (snooping; Jensen-Benington 1970's "table of random numbers"); risk rarely adjusted (only 3 studies); significance tested in only 4 studies, using t-tests on returns that are skewed and leptokurtic (Lukac-Brorsen 1990); optimize-then-test-out-of-sample in only 3 studies (Taylor's "dubious optimization" critique); no consensus benchmark.

## Modern studies (1988-2004): seven methodological groups

| Group | Representative study | Key result |
|---|---|---|
| Standard (optimize, OOS, costs, risk, t-tests) | Lukac-Brorsen-Irwin 1988: 12 systems, 12 futures markets, 1975-84; parameters re-optimized each year on the prior 3 years | 7 of 12 systems have significant gross returns. 4 systems (close channel, directional parabolic, MII channel, dual MA) earn significant net portfolio returns of 1.89%-2.78% per month on margin-based capital (about 3.8%-5.6% simple annual) and have significant CAPM alpha |
| Model-based bootstrap | Brock-Lakonishok-LeBaron 1992: DJIA 1897-1986, 26 VMA/FMA/TRB rules, nulls RW, AR(1), GARCH-M, EGARCH, 500 replications | VMA buy days +0.042% per day vs sell days -0.025% (unconditional 0.017%); none of the nulls reproduces the spread (GARCH-M gives 0.018% vs 0.067% observed). Sell periods are *more* volatile (1.34% vs 0.89%), so risk does not explain it. No costs, no OOS |
| Genetic programming | Allen-Karjalainen 1999: S&P 500 1928-95, rolling 5-year train / 2-year select windows | At 0.25% one-way cost, excess returns negative in 9 of 10 test periods. Some timing ability: in-market days have higher mean and lower volatility |
| Reality Check | Sullivan-Timmermann-White 1999: DJIA 1897-1996, about 8,000 rules | In sample, best rule (5-day MA) earns 17.2% per year, RC p = 0.00 (63 trades per year, breakeven cost 0.27%). OOS 1987-96: 2.8% per year, p = 0.32. S&P futures 1984-96: nominal p = 0.04, snooping-adjusted p = 0.90 |
| Chart patterns | Chang-Osler 1999: head-and-shoulders on 6 currencies 1973-94 | About 13% (DM) and 19% (yen) per year, Sharpe 1.00 and 1.47, betas about 0. But simple MA and momentum rules dominate, and adding H&S raises risk more than return |
| Nonlinear | Gencay 1998a: feedforward net on DJIA 1963-88 | 7%-35% annual net returns, 57%-61% correct sign |
| Other | Neely 1997: filters and MAs on 4 currencies 1974-97 | Positive net returns in 38 of 40 cases; DM mean 4.4% per year; MA Sharpe about 0.6 vs 0.3 for the S&P 500. Neely himself flags data mining |

Cross-cutting results worth keeping:

- **FX is the strongest case, and it decays.** Standard studies find 2%-10% per year net in currency futures from the late 1970s to the early 1990s. Qi-Wu (2002) still reject after White's Reality Check for 5 of 7 currencies (7.2%-12.2% excess, 1973-98). But Olson (2004) shows MA-crossover risk-adjusted profits on an 18-currency portfolio falling from more than 3% (late 1970s/early 1980s) to about 0 by the late 1990s. Neely-Weller (2001) find GP rules earn 1.7%-8.3% per year in 1981-92 but roughly zero in 1993-98 except the yen. Whether central-bank intervention drives the profits is disputed: LeBaron 1999 and Sapp 2004 say yes; Neely 2002 and Saacke 2002 say no. Sosvilla-Rivero et al. (2002) find nearest-neighbour FX profits turn negative once US intervention days are dropped.
- **Equities: emerging markets yes, developed markets no.** Bootstrap studies find net profits in emerging-market indices (e.g. Ratner-Leal 1999: Mexico, Taiwan, Thailand, Philippines). In developed markets, profits are negligible after costs or disappear over time. Bessembinder-Chan (1998), using the BLL rules on dividend-adjusted DJIA 1926-91, find a 4.4% per year buy-sell differential (breakeven one-way cost 0.39%). With a one-day lag this falls to 3.2%. For 1976-91 the breakeven cost is 0.22%, against estimated actual costs of 0.24%-0.26%. Ready (2002) argues BLL's best rule would not have been chosen by a trader in 1962, so its success is snooping. Mills (1997) finds FT30 MA profits in 1935-74 vanish in 1975-94.
- **Futures:** mixed. Lukac-Brorsen (1990) extend to 30 markets and 23 systems: 7 systems are significant at 10% net, but most profits come from 1979-80. Kidd-Brorsen (2004) link the 1990s decline in managed-futures returns to lower volatility and more of the large moves happening while markets are closed.
- **Risk-based explanations:** Kho (1996) and Sapp (2004) explain FX rule returns with a conditional CAPM and time-varying premia.

## Critique of the stronger methods (the paper's most useful contribution)

- **BLL-type bootstrap:** tests only a surviving, popular rule set. This means survivorship bias (Merton's coin-flip parable), and it reports gross returns only.
- **Genetic programming:** avoids ex post parameter choice. But applying a search technology that did not exist in the sample period is itself look-ahead (Cooper-Gulen 2003; Timmermann-Granger 2004). GP rules are "fit" rather than "best" solutions, so studies average over 10-100 of them. The evolved rules are more complex than anything practitioners use.
- **White's Reality Check:**
  1. The p-value is biased toward zero if the tested universe is a subset of the true universe. The STW DJIA best technical rule for 1987-96 has p = 0.341, but after adding calendar rules (17,298 rules) the best rule has p = 0.98.
  2. Costs are not built into the selection criterion. Qi-Wu show that selecting on net returns picks lower-turnover rules.
  3. The best rule differs across periods, so snooping-adjusted p-values do not carry over to another sample.
  4. Least-favourable-configuration nulls lose power when poor rules are included (Hansen 2003, 2004; SPA test). This bites in TA because parameter grids inevitably include many bad rules.
- **Snooping taxonomy (following Cooper-Gulen 2003, Denton 1985):** Snooping can happen at several levels: ex post in-sample rule choice; search over rule families, markets, in-sample and OOS windows, performance criteria and cost assumptions; and *collective* snooping, where many researchers each make one "ad hoc" choice on the same data. The collective form is the most dangerous because no single author sees it.

## Assessment

- **Convincing:** Across methods, trend-following rules (MA crossovers, channel breakouts) earned net, low-beta profits in currencies and some futures through roughly the early 1990s. These results survived several independent procedures: optimize-then-OOS, bootstrap nulls, GP and Reality Check. The joint pattern is more informative than the 58/24/10 count: profits concentrate in less-arbitraged markets and earlier periods, and they decay once the rules become widely known and computing cheap.
- **Fragile:** Developed-equity evidence rarely survives realistic costs or out-of-sample tests. Break-even costs of about 0.2%-0.4% one-way are the relevant yardstick. Most positive modern studies still lack either OOS tests or snooping control. Reported magnitudes often use margin-based capital, so returns must be converted before comparing across studies. Risk adjustment is mostly CAPM-beta, which is weak for FX and futures.
- **Limitations of the review:** It is a vote count plus narrative, with no meta-analytic weighting by design quality or effect size. The literature ends in 2004.
- **For a quant PM/researcher:** Treat this as (i) a reference prior that TA edges in liquid markets decay after the early 1990s; (ii) a checklist: pre-specified universe, costs inside the selection criterion, rolling OOS, SPA/StepM-type multiple-testing correction over the *full* searched universe, and subperiod stability; and (iii) motivation to model TA returns as time-series momentum or trend premia with explicit crisis and volatility conditioning, rather than as rule-specific anomalies.
