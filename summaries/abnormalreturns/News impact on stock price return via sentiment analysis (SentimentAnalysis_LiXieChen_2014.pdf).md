# News impact on stock price return via sentiment analysis

Xiaodong Li, Haoran Xie, Li Chen, Jianping Wang, and Xiaotie Deng, *Knowledge-Based Systems* 69 (2014), 14–23. DOI: 10.1016/j.knosys.2014.04.022. Source: [SentimentAnalysis_LiXieChen_2014.pdf](../../Finance/SentimentAnalysis_LiXieChen_2014.pdf), ten pages including all experimental tables.

## Why this matters

Dictionary sentiment can compress a high-dimensional news vocabulary into a small set of economically interpretable features. This paper tests whether that representation improves stock-return classification relative to bag-of-words, concept sentiment, and simple positive/negative polarity rules. Its useful design choices include a chronological training/validation/test split and an explicit examination of how return-label thresholds alter apparent accuracy.

The empirical result is modest and specific. The financial dictionary gives the highest capitalization-weighted stock-classification accuracy in the reported test set, 55.27% versus 53.91% for bag-of-words. This is not an accuracy for predicting the index's own return. More importantly, the news features appear to include same-day articles while the target is the same day's open-to-close return. The source does not establish that all features were available at the open. The experiment therefore does not demonstrate the profitability or even the implementability of an opening-time prediction strategy.

The main contribution is the representation comparison and label-design analysis. Any reproduction should preserve that descriptive experiment while separately testing a correctly timed forecasting variant. The latter is additional work, not something already validated by the paper.

## Universe and data selection

The study focuses on large, actively traded Hang Seng Index stocks. Starting from the fifty constituents referenced as of 2013, the authors remove those added after January 1, 2003, leaving twenty-two stocks. The stated intention is to avoid behavior around index additions. This is not a complete point-in-time constituent reconstruction: starting from a later membership list can omit firms removed before 2013 and introduce survivorship selection.

The final universe is:

| Sector | Symbols |
|---|---|
| Commerce | 0013, 0019, 0066, 0267, 0291, 0293, 0494, 0762, 0941, 1199 |
| Finance | 0005, 0011, 0023, 0388, 2388 |
| Properties | 0001, 0012, 0016, 0101 |
| Utilities | 0002, 0003, 0006 |

All symbols have the suffix .HK. The table is the selected subset, not all historical HSI members. News coverage is uneven. The reported cross-stock correlation between index weight and mean daily news count is 0.7990; capitalization and news count correlate 0.8484. Thus the evaluation puts much more information and index weight on a few large stocks.

English-language news comes from FINET between January 2003 and March 2008. Each article has a release timestamp and associated company symbols. Daily OHLC quotes over the same dates come from Yahoo Finance. The paper does not disclose the complete article corpus, exact record counts by split and stock, handling of repeated wire stories, revisions, corporate-action adjustments, or the policy for trading days with no company news.

Multiple articles about a stock on one date are concatenated into a single document. A document can therefore include information arriving at several times during that trading day. The running example is timestamped 11:19 on March 17, 2008 and already describes ongoing price declines. This is direct evidence that the represented text need not predate the opening price.

## Labels and the time-alignment issue

The target return is the simple open-to-close return

$$
R_{it}=\frac{C_{it}-O_{it}}{O_{it}}.
$$

With a symmetric threshold $h$, labels are positive if $R_{it}\geq h$, negative if $R_{it}\leq-h$, and neutral otherwise. The final choice is $h=0.005$, or fifty basis points. The threshold creates a three-class task; 50% accuracy is not automatically the no-information benchmark.

The authors motivate open-to-close returns as avoiding overnight inventory risk and some nontrading-day complications. Such a choice does not remove all seasonality, nor does it solve information timing. To trade the full open-to-close return, the prediction must be available before execution at the open. Using an article released at 11:19 to label that morning's opening-to-closing return includes a pre-publication part of the target and potentially contemporaneous price information in the text.

No explicit next-day shift, pre-open cutoff, publication-latency rule, or intraday post-news execution price is supplied. The chronological split prevents training on later labeled dates, but it does not fix leakage within each date. The safest interpretation of the reported task is classification of same-day returns associated with daily news, pending a timing audit. It should not be called a causal estimate of news impact.

A genuinely prospective variant could restrict features to pre-open news and retain the same-day target, shift daily features to a subsequent session, or use post-publication intraday returns. Each changes the experiment and must be evaluated separately. The source does not report results for those variants.

## Text representation and dictionaries

After removing stop words, a document-term matrix $N$ contains word frequencies. Rows are stock-day aggregated documents; columns are retained terms. A sentiment dictionary matrix $D$ associates terms with sentiment categories. Aligning common vocabulary columns/rows gives

$$
S=ND.
$$

This is vocabulary-matched matrix multiplication, described as an “inner-multiply” operation. Terms absent from a dictionary contribute no sentiment feature. The output dimension depends on the dictionary rather than the full vocabulary size.

The Harvard IV-4 dictionary has over ten thousand entries and 182 dimensions, grouped into fifteen broad types such as positive/negative, activity and strength, institutional language, motivation, cognitive orientation, and personal pronouns. The financial dictionary is the 2012 Loughran–McDonald version, using six categories: negative, positive, uncertainty, litigious, strong modal, and weak modal. Table 4 lists respective category counts 2,349, 354, 291, 871, 19, and 27. Entries can belong to multiple categories, so these numbers need not sum to a unique-word vocabulary count.

The article describes term-frequency multiplication, but its worked example raises a reproducibility inconsistency. “Attractive” occurs three times in the term-frequency table, while its positive contribution in the sentiment table is one. That matches a binary-presence interpretation more closely than a raw frequency sum. The exact handling of repeated terms should therefore be checked against code. It is not enough to state $ND$ without declaring whether $N$ contains counts, normalized counts, or binary occurrence indicators.

Further preprocessing choices are incompletely specified: case folding, stemming/lemmatization, phrase handling, dictionary inflections, the actual stop-word list, negation treatment, document-length normalization, feature scaling, and whether the vocabulary is fitted only on training data. The printed example retains terms such as “not” and “but,” making a guessed generic stop-word list especially unsafe. The dictionary is also a later resource relative to the 2003–2008 sample, which is acceptable for a retrospective representation study but differs from a historical information-vintage backtest.

## Six compared approaches and model tuning

HVD and LMD use the corresponding sentiment feature vectors. SN uses SenticNet 3.0-beta. BoW uses the vocabulary representation. These models feed a support vector machine with a radial-basis kernel. The article does not provide a fully operational account of the SenticNet feature construction or a complete vocabulary/feature-selection specification for BoW.

The SVM grid has kernel parameter $\gamma\in\{10^{-4},10^{-3},10^{-2},10^{-1},1,10,100,1000,10000\}$ and penalty $C\in\{1,3,5,7,9,11,13,15,17,19\}$, yielding ninety combinations. A conventional RBF is $K(x,x')=\exp[-\gamma\|x-x'\|^2]$; that expression makes the kernel parameter's role explicit. The library, multiclass decomposition, class weights, feature standardization, tie-breaking, and selected pair for each stock/model are not reported.

PO is a rule based on positive and negative sentiment frequencies. The paper first gives normalized polarity $(f_+-f_-)/(f_++f_-)$. Its implemented three-way rule instead compares relative differences $(f_+-f_-)/f_-$ and $(f_--f_+)/f_+$ with a threshold. APO reverses the positive and negative decisions. These are hand-coded rules, not trained SVM classifiers. Zero denominators and the relationship between the polarity threshold and the return-label threshold are not fully explained. A literal implementation must resolve them explicitly rather than silently divide by zero.

The training sample is January 2003–December 2005, validation January–December 2006, and the independent test January 2007–March 2008. Hyperparameters are chosen using training/validation and carried into the test. This is preferable to randomly shuffling temporally dependent data. The authors also say they tried several date splits and found negligible changes, but do not tabulate those results or establish that every design choice was fixed without test-set feedback.

## Why threshold choice can manufacture accuracy

The authors analyze a no-information classifier drawing labels from the true class probabilities. Its expected accuracy is

$$
A_{\rm random}=p_-^2+p_0^2+p_+^2.
$$

Under a symmetric return distribution with $p_-=p_+=p$, this becomes $6p^2-4p+1$, minimized at balanced probabilities $p=1/3$. As the neutral threshold grows, neutral labels dominate and apparent accuracy rises even without predictive information. At a threshold near zero, the task approaches a two-class problem with chance accuracy near one half.

This is a useful diagnostic, but the actual data need not be Gaussian or symmetric. The relevant baseline should use the empirical class frequencies in each declared evaluation sample. A deterministic majority-class predictor has accuracy $\max(p_-,p_0,p_+)$, often larger than the random-prior baseline. The paper does not supply those class proportions or a majority-class comparison alongside its headline table.

The final fifty-basis-point label threshold is justified by an asserted thirty-basis-point Hong Kong trading-cost level and a desire to avoid a mostly-neutral task. This is the historical paper's design convention, not a verified current market-cost estimate. No actual net trading simulation deducts thirty basis points, and a class label outside the threshold does not itself guarantee a profitable fill or a position-size rule.

## Actual held-out results and their size

At the stock level, Table 12 reports that LMD beats BoW for twelve of twenty-two stocks and loses for ten. HVD beats BoW for only eight and loses for fourteen. Thus the article's broad conclusion that both sentiment approaches outperform BoW at every level is stronger than the stock-by-stock test evidence. In validation the corresponding wins are fourteen versus eight for LMD and twelve versus ten for HVD. The difference between a tuned validation result and a held-out result matters.

The two simple polarity rules usually perform worse, but not uniformly. In the test set, PO is best in the capitalization-weighted commerce comparison, at 0.3892. A statement that polarity never produces useful predictions is not established by its lower aggregate accuracy, especially without class-balanced baselines or statistical tests.

The reported “index-level” statistic is a weighted average of individual-stock accuracies,

$$
A_{\rm index}=\sum_i\omega_iA_i.
$$

It does not classify the sign of an index return and does not aggregate stock signals into a traded index portfolio. The sector statistic uses the analogous weighted average. Exact historical weight dates, normalization within the selected twenty-two-stock subset, and reconstitution rules are not disclosed.

| Model | Validation weighted stock accuracy | Test weighted stock accuracy |
|---|---:|---:|
| HVD | 0.5892 | 0.5460 |
| LMD | 0.5976 | 0.5527 |
| BoW | 0.5858 | 0.5391 |
| SN | 0.5876 | 0.5445 |
| PO | 0.2230 | 0.2789 |
| APO | 0.2172 | 0.2665 |

The LMD test gain over BoW is 0.0136, or 1.36 percentage points, not 13.6 points. HVD's gain in this weighted statistic is 0.69 points despite losing more stock-level comparisons. Concentration in highly weighted stocks can explain that pattern. For HSBC, test accuracies are 0.6968 for LMD and 0.6767 for BoW; some other stocks have much lower accuracies. Without class proportions, those high values cannot be interpreted as equally strong directional information.

Test-sector LMD/BoW accuracies are commerce 0.3763/0.3776, finance 0.6509/0.6318, properties 0.4030/0.3956, and utilities 0.4001/0.3868. LMD is best among all six in finance, properties, and utilities; commerce is the exception. There are no confidence intervals, paired forecast tests, or dependence-adjusted significance results demonstrating that the small aggregate differences are statistically distinguishable. Stocks share news and market shocks, so twenty-two win/loss observations are not independent replications.

## Reproduction plan and missing inputs

A faithful descriptive reproduction needs the FINET corpus with original timestamps and stock tags, the exact selected price histories, the twenty-two-stock universe, and the two dictionary versions. Construct stock-day documents, declare count versus binary features, match dictionary vocabulary, and reproduce the three-way open-to-close labels. Preserve the chronological split and ninety-point SVM grid. Record each stock/model's selected hyperparameters and compare predictions on identical stock-day instances.

An availability audit must then establish when every feature would have been known relative to its target return. Separate same-day association from a prospective strategy. Fit preprocessing only on training data where appropriate, publish the empirical class distributions, and compare against majority-class and prior-random baselines. Paired inference should account for common dates and stocks rather than treating individual predictions as independent.

The paper omits the corpus, complete sample counts, timestamp cutoff, feature-scaling details, selected hyperparameters, weight histories, and code. No execution, position construction, short availability, turnover, realized P&L, or transaction-cost result is supplied. The thirty-basis-point discussion is a label choice, not a validation of net profitability.

The supported takeaway is that a compact financial-dictionary representation gives a small improvement in the reported weighted classification experiment. Whether that improvement survives a strictly prospective news cutoff, a point-in-time universe, stronger imbalance baselines, dependence-aware testing, and actual trading costs remains unanswered. Those gaps are central to using the paper as a quantitative research design rather than accepting its prediction language at face value.
