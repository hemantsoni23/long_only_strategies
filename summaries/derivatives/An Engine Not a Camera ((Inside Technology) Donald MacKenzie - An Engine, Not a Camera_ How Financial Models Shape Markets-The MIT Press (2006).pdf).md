# An Engine, Not a Camera: How Financial Models Shape Markets — Detailed Quantitative Research Notes

**Donald MacKenzie** · 2006 · MIT Press (Inside Technology series) · Social studies of finance / history of financial economics · Source file: `Finance/(Inside Technology) Donald MacKenzie - An Engine, Not a Camera_ How Financial Models Shape Markets-The MIT Press (2006).pdf` (the Drive text extraction was truncated at the end of chapter 2, about p. 67. Chapters 3–9 are summarised from the author's own chapter-by-chapter overview in chapter 1, and are flagged as such.)

---

## Thesis

The title comes from Friedman (1953): economic theory is "an 'engine' to analyze [the world], not a photographic reproduction of it." MacKenzie uses "engine" in a sense Friedman did not intend. Finance theory was an active force that reshaped the markets it described, not a camera that passively recorded them. The book pursues two linked histories: the rise of financial economics in the US from the 1950s, and the growth of derivatives markets after 1970. It asks how each shaped the other. The core case study (chapters 5–7) is option pricing: Black–Scholes–Merton (BSM), the Chicago options exchanges, and the 1987 crash.

Sources: more than 60 oral-history interviews with theorists and practitioners, Fischer Black's papers at MIT, the trade press, and the econometric literature on option prices. Equations are confined to appendices; the book is deliberately non-mathematical.

## The performativity typology (Fig. 1.1)

The categories are nested, following Callon's claim that economics "performs, shapes and formats the economy, rather than observing how it functions":

| Level | Definition |
|---|---|
| Generic | Some aspect of economics (a theory, model, procedure, data set) is *used* by market participants, regulators, etc. |
| Effective | That use *makes a difference* to economic processes. Establishing this needs a counterfactual, since use may be epiphenomenal (Mirowski–Nik-Khah on the spectrum auctions). |
| Barnesian | That use makes processes *more like* their depiction by the model (after Barry Barnes's self-validating feedback loops). |
| Counterperformativity | That use makes processes *less like* the model. |

Why he avoids the "self-fulfilling prophecy" label:
1. The strong forms are subsets of a broader phenomenon: economics built into market infrastructure.
2. The deepest kind of incorporation is into algorithms, routines and devices, not beliefs. A model embedded in them works even on users who are sceptical of it or have never heard of it.
3. Barnesian performativity is not pathological. An arbitrary formula (say BSM with an algebra error that halves or doubles the price) could not make itself true, because arbitrage and systematic losses would destroy it.

Evidence for Barnesian performativity comes from comparing market conditions (transaction costs, short-sale feasibility) and price patterns before and after a model is widely adopted. This is suggestive, never conclusive.

## Methodological points worth keeping

- **Friedman vs Samuelson on unrealistic assumptions.** Friedman: "to be important ... a hypothesis must be descriptively false in its assumptions." Samuelson: unrealism "is anything but a demerit." Merton Miller: "Of course you don't worry about the assumptions." The field's epistemic culture judges models by their implications, and even those are treated leniently. CAPM implies that everyone holds identical risky portfolios, which was known to be false, yet the model was prized.
- **Testing is theory-laden (Duhem–Quine).**
  - Efficiency tests are joint tests with CAPM as the benchmark.
  - CAPM tests use realised returns as a proxy for expected returns, which already assumes rational expectations.
  - The CRSP data-cleaning filter flagged as a probable misrecording any price that moved more than 10% of the previous price plus $1 and then reversed by a similar amount. The rule rests on the random-walk property it was later used to test.
  - Rubinstein's option tests averaged prices that differed for the same stock price (Polaroid at $37.50 with July/40 calls trading at $3.25, $3.375 and $3.50) and excluded the first and last 1,000 seconds of each trading day as "artificial pricing." Such filtering embeds a view of what "natural" market operation looks like.

## Chapter 2 — Transforming finance (fully read)

Finance in the 1950s was descriptive and institutional; Dewing's two-volume, 1,500-page text contained no mathematics beyond arithmetic. Three strands transformed it:

1. **Modigliani–Miller (1958, 1961).** Capital structure and dividend policy are irrelevant in a "perfect market." The proof is by arbitrage between "perfect substitutes" in the same risk class, and needs no assumptions about risk preferences. Durand's critique was institutional. Regulation T (margin typically ≤50%) prevents the home-made leverage the arbitrage requires, and investors restricted to high-grade assets create a "super premium for safety." Their dispute came down to whether arbitrage is strong enough to overcome institutional frictions, which is the question the whole book keeps returning to. Modigliani (a Keynesian) was more cautious about relaxing assumptions than Miller (a Chicago/Friedman-style economist).
2. **Markowitz → Sharpe (CAPM).**
   - *Origin.* Markowitz applied Williams's expected-value logic to a whole portfolio and saw that maximising expected return alone means holding a single stock. Adding variance made selection a quadratic programme, which he solved with the critical-line algorithm.
   - *Early reception.* Practitioners ignored it. Durand saw "no obvious audience." At Markowitz's defence, Friedman said it "isn't a dissertation on economics."
   - *Computational limits.* 1,000 securities require 499,500 correlations. A 25-security problem was beyond what Markowitz could compute at Yale in 1955–56, and even on an IBM 7090 in the early 1960s the Rand code handled at most 249 securities.
   - *Single-index model.* Markowitz suggested it; Sharpe (1963) made large problems computationally feasible.
   - *CAPM.* Sharpe (1964) asked what prices would be if everyone followed Markowitz. The answer was a linear expected-return/beta relation. He initially "tweaked" the maths to avoid the implication that everyone holds the same risky portfolio, and only later accepted that "if there's only one, it's got to be the market portfolio." Treynor, Lintner and Mossin reached essentially the same model independently. Sharpe's defence, "the proper test of a theory is not the realism of its assumptions but the acceptability of its implications," echoes Friedman (via Alchian).
   - *Tobin's separation theorem* linked portfolio choice to Keynesian liquidity preference.
3. **Random walk → EMH.**
   - *Early forerunners.* Regnault (1863) found empirically that price deviations scale with $\sqrt{t}$ and argued that short-term speculators face certain ruin. Bachelier (1900) used arithmetic Brownian motion to price options; Lévy's verdict was "Too much on finance!"
   - *Mid-century revival.* Working (1934) compared real price series with simulated random ones. Kendall (1953) found negligible serial correlation in weekly UK stock indices, wheat and cotton (the "Demon of Chance").
   - *Economic interpretation.* Samuelson: "If one could be sure that a price will rise, it would have already risen." He switched to geometric Brownian motion (log-normal prices) to respect limited liability. Osborne, working independently, also found log-normality.
   - *Consolidation.* Cootner's 1964 volume of readings, then Fama (1970) with weak, semi-strong and strong forms. Specialists and insiders were the admitted exceptions to strong-form efficiency.

By 1970, MM, CAPM and EMH formed a coherent view. For example, Treynor showed that CAPM implies MM, and CAPM supplied the benchmark for efficiency tests.

## Chapters 3–9 (from the author's overview; not in the extracted text)

- **Ch. 3.** Financial economics became an academic subfield based in business schools. Practitioners were mostly hostile, since EMH implied that much active management was pointless. Beta was sold commercially. **Index funds** (early 1970s) are presented as a *Barnesian* case: indexing made CAPM's "everyone holds the market" prediction less untrue.
- **Ch. 4.** Testing:
  - Roll's critique: the market portfolio is unobservable, so CAPM may not be testable.
  - Anomalies: trading to exploit them seems often to have shrunk or eliminated them (performativity through arbitrage).
  - Mandelbrot's infinite-variance ("wild randomness") model was initially championed by Fama and then rejected, partly because it undermined standard statistics ("consigning centuries of work to the ash pile").
- **Ch. 5.** Option pricing:
  - Black and Scholes derived the formula via CAPM. Thorp's contemporaneous work was aimed at finding arbitrage opportunities, not at a theoretical price.
  - Merton reached the same equation without CAPM, via continuous-time replication, using rigorous stochastic calculus. By the end of the 1970s derivatives pricing had been recast in martingale terms.
  - The replicating-portfolio method, not the formula itself, is the lasting exemplar.
- **Ch. 6.** Chicago (CBOE opened in 1973, the year of the BSM papers):
  - Economics lent legitimacy to derivatives exchanges against the charge that they were gambling. Physical-delivery rules inherited from grain futures cast a long shadow.
  - The fit of BSM to prices was initially approximate and improved rapidly in the 1970s. By Rubinstein's tests, 1976–78 prices fit well "by social-science standards," and index options in the 1980s fit even better.
  - Two mechanisms: market conditions moved toward the model's assumptions, and traders used BSM for **"spreading"** (buying options the model showed as cheap relative to others and selling the expensive ones). This arbitraged away exactly the discrepancies the econometric tests looked for.
  - Verdict: BSM's performativity in this period was Barnesian.
- **Ch. 7.** After 1987 a durable **volatility skew** appeared. BSM remains embedded in market language and technical devices (quoting in implied volatility), but the prices it performs are no longer those of classic BSM. The crash reveals the "historicity" of economics. Portfolio insurance, an application of option theory, raises the possibility of counterperformativity, but MacKenzie concludes its contribution to the crash cannot be determined.
- **Ch. 8.** **LTCM (1998).**
  - The dismissive "blind faith in models" story is wrong. The partners treated models as engines of inquiry, and model details mattered less than supposed.
  - The crisis was social. Imitation of the Meriwether group's success built an unstable, overlapping **"superportfolio"** of arbitrage positions; some firms even adjusted their mortgage-backed-securities models to match what they inferred Meriwether's group was using.
  - The Russian default of 17 Aug 1998 triggered forced sales into illiquid markets, and LTCM became the subject of a self-fulfilling prophecy of failure (R. K. Merton's 1948 bank-run example).
  - Limits to arbitrage are therefore a sociological matter.
- **Ch. 9.** Finance theory's ambivalent attitude to empirical adequacy, a synthesis of how far the theory brought its world into being, behavioural finance, arbitrage as the pivot between orthodox and behavioural finance, and a call for a "politics of market design" analogous to the politics of technology.

## Assessment

- **Strong:** the performativity typology is precise and testable in principle, and the Chicago/"spreading" mechanism is a concrete causal channel, not a slogan. The account of how testing depends on theory (CRSP filters, Rubinstein's exclusions) is directly relevant to anyone doing empirical work. The LTCM chapter's "superportfolio" is one of the clearest early statements of the crowding and common-ownership fragility that quants now model explicitly.
- **Fragile:** the evidence for Barnesian performativity is circumstantial (before/after comparisons with many confounders), which MacKenzie concedes. "Markets learned the correct price slowly" is a rival explanation he addresses only by pointing to the post-1987 break. Nearly all the evidence is US and Chicago-centred, and the story ends in 2006.
- **For a quant PM:**
  - Ask of any widely used model what trading on it does to the patterns it relies on. Anomaly decay after publication is Barnesian-in-reverse, and crowded stat-arb and vol-selling are "superportfolio" risk.
  - Implied volatility is a quoting convention embedded in infrastructure, not a belief in constant $\sigma$.
  - Arbitrage capital is finite and correlated across holders, so stress tests should model forced liquidation by *other* holders of similar positions, not just historical shocks.
  - Treat hedging flows as a feedback channel. Portfolio insurance in 1987 is the canonical case; the modern analogues are dealer gamma, vol-targeting and trend-following.

Related notes: Gatheral (post-smile volatility modelling), Michaud (optimiser-driven crowding), Abergel et al. (limit order books).
