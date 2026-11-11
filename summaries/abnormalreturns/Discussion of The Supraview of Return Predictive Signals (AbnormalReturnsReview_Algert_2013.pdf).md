# Discussion of “The Supraview of Return Predictive Signals”

**Author:** Peter Algert (Algert Coldiron Investors, San Francisco) | **Year:** 2013 | **Venue:** *Review of Accounting Studies* 18:731–733, DOI 10.1007/s11142-013-9237-8 | **JEL:** G12, G14  
**Discussed paper:** Green, Hand and Zhang (GHZ), “The supraview of return predictive signals”  
**Source file:** `Finance/AbnormalReturnsReview_Algert_2013.pdf` (3-page discussion note; no tables or new empirics of its own)

---

## What the note does

A practitioner's discussion of GHZ's database of published return predictive signals (RPS). Algert singles out three GHZ findings — (i) RPS discovery continues at an undiminished pace, (ii) how a new RPS should be evaluated against known factors, (iii) returns are either "pervasively inefficient" or there are many more priced factors than thought — comments briefly on (i)–(ii), and spends most of the space on the *returns to RPS strategies* and why implementation frictions keep them from being arbitraged away. Its value is a set of concrete cost and leverage anchors from a working quant manager.

## Points, in order

**1. Discovery rate.** GHZ find neither the number of new RPS per year nor their in-sample Sharpe ratios has declined. Algert's analogy: either the ocean has many fish or technology more than compensates for a declining population; he favours the technology explanation. Since most work is on US stocks, he expects further papers from global extension and more signals. He also notes GHZ's data as a rare measurement of the "production function" of academic research.

**2. Evaluating a new RPS (GHZ Section 4).** GHZ argue one need not control for an exhaustive factor set: a signal significant net of the standard three factors is likely to stay significant with many more controls. Highly correlated or a-priori similar signals should still be controlled for, but GHZ's simulations show the probability of remaining significant stays high, particularly for *value-weighted* hedge-portfolio returns. Algert: not a methodological prescription, but a likely useful citation.

**3. Combination returns.** Many RPS have Sharpe ratios high relative to equity indices. Average pairwise correlation of RPS returns is near zero, but average *absolute* correlation is **0.29**, so large subgroups are highly correlated. Combinations would have earned very attractive returns in-sample, and large firms did run multi-RPS strategies from the early 1990s, peaking in 2007–2008 when many quantitative strategies "famously imploded."

**4. Leverage regime.** The old playbook — maximise combined Sharpe, then lever to a return target — exposed the most levered books to liquidity risk and was a primary cause of the 2007 losses. With both supply of and demand for leverage reduced, an RPS that raises Sharpe but lowers mean return is now less attractive.

**5. Costs scale with leverage and with apparent alpha.** Stock-loan fees, trading costs and financing roughly scale with leverage. Loan and trading costs are also highly correlated with the size of the apparent return opportunity: high-spread RPS (which GHZ find have higher Sharpe) load extreme quantiles on high-idiosyncratic-risk stocks, which are expensive to borrow and trade. Hence less practitioner pressure to arbitrage those RPS away.

| Cost item (Algert's rules of thumb) | Magnitude |
|---|---|
| Annual financing + borrow, stocks outside the largest 1,500 in CRSP | 50–100 bp |
| Same, larger stocks | about half that |
| General borrow rate | ~25 bp/yr |
| "Hot stock" borrow | sometimes >20%/yr; a few such names drive portfolio cost up quickly |
| Round-trip trading cost in smaller stocks, simple hedge portfolio | 100–200 bp of return *each time it is rebalanced* |
| Turnover to fully rebalance at 1×1 leverage | 400% of capital |

Trading costs depend on leverage and capital; business models push managers to deploy hundreds of millions per strategy.

**6. Partial decay as equilibrium.** Once an RPS is discovered, managers should not be expected to fully close the return/risk gap, especially in small, illiquid stocks; frictions are consistent with the observed *partial* post-discovery decay. Residual success depends on research quality, cost management, and investors' willingness to bear the risk.

**7. Correlation with other risks.** GHZ report average RPS returns have a low negative correlation with the market; Algert cautions that combined RPS returns may still correlate meaningfully with credit or volatility strategies institutional investors hold.

**8. Organising the zoo.** Practitioners often group signals by correlation with price (positive/negative/zero) — useful for combinations, unlikely to yield a unifying framework. He suggests grouping by theme (valuation, corporate finance, behavioural) and studying within-group relationships.

## Assessment

- **Convincing / useful:** the cost numbers are the substance. The mechanism — paper alpha concentrates in exactly the names that are costly to short and trade — explains why high in-sample Sharpe overstates live Sharpe most where it looks best, and why decay is partial rather than complete. The 0 vs 0.29 (signed vs absolute) correlation point is a direct warning against counting published signals as independent breadth; a risk model for a multi-signal book needs thematic block structure.
- **Fragile:** cost figures are unsourced rules of thumb from one manager circa 2013, not estimates; borrow and trading-cost levels have changed since. The "technology" explanation for undiminished discovery is opinion; the note does not engage the obvious alternative that undiminished discovery with stable in-sample Sharpes reflects data mining / publication bias (later the central theme of Harvey–Liu–Zhu 2016 and replication studies). GHZ's three-factor sufficiency claim is reported uncritically.
- **Practical use:** a checklist for promoting a signal — three-factor screen plus correlated-cousin controls; value-weighted implementation; explicit borrow and impact budget by size bucket; evaluate on capital-efficient mean, not Sharpe alone, when leverage is constrained; check overlay correlation to credit/vol; cluster signals by theme before combining.
