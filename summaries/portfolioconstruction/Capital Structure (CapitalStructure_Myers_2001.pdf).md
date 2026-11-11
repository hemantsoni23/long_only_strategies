# Capital Structure

Stewart C. Myers, *Journal of Economic Perspectives* 15(2), Spring 2001, pp. 81-102. [Source PDF](../../Finance/CapitalStructure_Myers_2001.pdf). The supplied 22-page article is image-based apart from its metadata and reproduction notices. Every page, including Table 1, Figure 1, footnotes, and references, was read visually. PDF page $j$ corresponds to printed page $80+j$. This is a research review and methodological argument, not a new panel-data estimation or a complete structural model.

## Why this matters

Myers distinguishes explaining particular financing decisions from explaining a firm's overall debt policy. Taxes clearly affect the design of securities. Information asymmetry clearly affects the reaction to an equity issue. Debt can discipline managers in a mature firm that wastes surplus cash. These findings do not establish one universal model of leverage or show how to calculate an optimal debt ratio for every company.

The review's main contribution is a disciplined comparison of conditional theories and of the statistical tests used to distinguish them. Tradeoff theory balances tax benefits against distress costs. The pecking order links borrowing to accumulated financing deficits when outside investors have less information. Free-cash-flow theory studies debt's control benefits in firms prone to overinvestment. Each can fit observations that another theory also generates. A significant coefficient or apparent adjustment toward a historical average may therefore have little power to identify the economic mechanism.

For a researcher, this is a guide to defining the state variables and counterfactuals before fitting leverage regressions. For a credit or equity investor, it explains why profitable, liquid firms can have little debt, why a debt-funded payout differs from borrowing for investment, and why the same transaction can benefit shareholders while harming existing creditors.

## Scope and the financing facts

The review primarily concerns public nonfinancial corporations with access to U.S. or international capital markets. Those firms can select among many instruments and adjust financing relatively cheaply. The analysis should not be transferred without modification to regulated banks, households, or small firms dependent on one relationship lender.

Myers reports that internally generated cash, including depreciation and retained earnings, finances most aggregate U.S. corporate investment. External funds generally cover less than 20%, with debt accounting for most external financing. Net equity issuance can be negative because repurchases and acquisition-related retirement of shares exceed new issuance.

For U.S. nonfarm nonfinancial corporations in 1999, the reported financing arithmetic is:

| Item | Amount |
|---|---:|
| Aggregate investment | \$944 billion |
| Internal cash flow | \$805 billion |
| External financing | \$139 billion |
| Net additional borrowing | \$283 billion |
| Net equity issuance | −\$144 billion |

Thus internal financing is about 85.3% of investment, and \$283 billion minus \$144 billion reconciles to the external requirement. These are sector aggregates from the Federal Reserve Flow of Funds, not the financing mix of a representative firm. Small, risky, rapidly growing firms can rely heavily on stock issues even when aggregate net issuance is negative.

Industry and balance-sheet definitions matter. Oil, utilities, chemicals, transport, telecommunications, forest products, and property development are cited as relatively debt-intensive. Pharmaceuticals and prominent growth firms often have little net debt. Myers reports approximately \$25 billion in Ford cash and marketable securities against \$10 billion debt in 2000, and \$24 billion in Microsoft cash and marketable securities with no long-term debt at midyear 2000. These examples describe net lender positions under the stated measures, not an assertion that every liability or business segment is debt-free. Exxon repurchased \$29 billion of stock from the mid-1980s through its 1999 Mobil merger.

Table 1, drawn from Rajan and Zingales, illustrates the sensitivity of country comparisons to accounting. It reports median debt divided by debt plus equity for publicly traded companies in 1991:

| Country | Book | Adjusted book | Market | Adjusted market |
|---|---:|---:|---:|---:|
| Canada | 39% | 37% | 35% | 32% |
| France | 48% | 34% | 41% | 28% |
| Germany | 38% | 18% | 23% | 15% |
| Italy | 47% | 39% | 46% | 36% |
| Japan | 53% | 37% | 29% | 17% |
| United Kingdom | 28% | 16% | 19% | 11% |
| United States | 37% | 33% | 28% | 23% |

Accounting adjustments change the rankings substantially. German pension obligations and reserves receive particular attention: gross pension liabilities and treatment of reserves can differ from U.S. reporting. After adjustment, the United States lies within the group rather than being an obvious low-leverage outlier. The review does not supply the company list or detailed adjustment code from the underlying study.

Debt-to-capital $D/(D+E)$, debt-to-equity $D/E$, and net-debt measures are different objects. Book values describe accounting financing; market values are needed in the weighted-average cost-of-capital identity. A replication must preserve which measure each hypothesis and table uses rather than relabel every ratio as leverage.

## Modigliani-Miller as the benchmark

Figure 1 represents a market-value balance sheet: assets in place and growth opportunities have total value $V$, financed by debt $D$ and equity $E$, with $V=D+E$. In perfect capital markets, holding the left-hand-side investment opportunities fixed, changing how cash flows are divided among securities does not change $V$.

The benchmark removes taxes, transaction frictions, and financing-induced changes to investment and incentives. Myers's footnote also emphasizes market completeness or replicability: the risk characteristics of a new security must be reproducible using other claims or trading strategies. Frictionless trade alone is not a sufficient description of every condition behind irrelevance.

Let $r_A$ be the expected return on the firm's assets or equivalently its aggregate outstanding securities, and let $r_D,r_E$ be expected required returns on debt and equity. Then

$$
r_A=r_D\frac DV+r_E\frac EV,
\qquad
r_E=r_A+(r_A-r_D)\frac DE.
$$

Under the benchmark, $r_A$ is fixed by business risk. Replacing equity with apparently cheaper debt increases the risk borne by remaining equity and therefore its required return. The identity does not say $r_D$ stays fixed as leverage becomes risky. Treating it as a linear regression in $D/E$ with a constant debt cost at every debt level would add an assumption the general statement does not require.

The after-tax corporate version is

$$
\mathrm{WACC}=r_D(1-T_C)\frac DV+r_E\frac EV.
$$

Here $T_C$ is the relevant marginal corporate tax rate. The source presents this as a discount rate for after-tax project cash flows when the investment does not alter business risk, under the financing assumptions implicit in the calculation. It is not a universal rate for projects with different risk or arbitrary future leverage policies.

Financial innovation does not simply refute the benchmark. Investors can demand specialized claims, but corporations and intermediaries can often supply and imitate them cheaply. Any initial premium may shrink as supply expands. Myers stresses this supply response: persistent large value gains from merely changing the packaging of unchanged cash flows would invite imitation. The benchmark consequently directs research toward specific costs, information differences, or agency effects that impede the replication argument.

## Corporate and investor taxes

A fixed perpetual debt issue with usable tax deductions every year gives the familiar tax-shield calculation. If debt is $D$, interest is $r_DD$, the tax saving is $T_Cr_DD$, and the saving is discounted at $r_D$, then

$$
PV(\mathrm{tax\ shield})=T_CD.
$$

The assumptions are doing the work: fixed permanent debt, a constant applicable tax rate, sufficient taxable income, and a tax-shield risk matching the discount rate. Myers's historical illustration uses \$1 million debt and a 35% corporate tax rate, producing a \$350,000 present-value gain. The statutory rate is from the article's setting in 2001.

The review calls such calculations remote upper bounds in many applications. A firm can have losses, deductions can be unusable or deferred, debt capacity changes with future profitability, and debt may be repaid. The tax shield is then state-dependent and risky. Personal taxation can offset part of its corporate benefit because investors may pay more on interest than on equity income or deferred capital gains.

For each dollar of pretax operating income, a simple integrated-tax comparison is

$$
\text{debt investor receipt}=1-T_D,
\qquad
\text{equity investor receipt}=(1-T_C)(1-T_E).
$$

This is a compact reconstruction of the article's examples, with $T_D$ the effective personal rate on interest and $T_E$ the effective personal rate on equity income. Cancellation requires equality of these two receipts. It does not follow just from interest being deductible at the corporate level.

The first example uses corporate tax of 35%, personal interest tax near 40%, and effective capital-gains tax near 8%. On \$100,000 of operating income, corporate tax is \$35,000 and the equity investor's deferred tax is approximately \$5,000. Replacing the equity income with interest adds about \$40,000 in personal interest tax while removing that roughly \$5,000 equity tax, offsetting the corporate saving. Using exactly 8% gives \$5,200 rather than \$5,000, so the cancellation is approximate at the source's rounded rates, not a numerical identity requiring correction.

The second example uses Graham's estimates: interest taxation near 30% and effective equity taxation near 12%. The extra personal tax is about \$30,000 minus \$8,000, leaving approximately \$13,000 of the \$35,000 corporate saving. Exact arithmetic at the rounded rates gives \$12,800. Myers notes uncertainty about the identity and tax rates of marginal investors; the figures are illustrative evidence that personal taxes reduce, but may not eliminate, the debt advantage.

Miller's equilibrium account adds a supply mechanism. Increasing corporate debt brings investors in higher tax brackets into the marginal debt-holding position. The pretax debt yield must compensate them, eventually offsetting the corporate tax benefit. Evidence that low-tax firms prefer equity is consistent with this account as well as with a positive net debt tax shield. That empirical relation alone does not identify the tax shield's contribution to firm value.

## Tradeoff theory and the profitability problem

Tradeoff theory chooses borrowing so that the marginal value of additional tax shields equals the marginal increase in expected distress costs. A notation-level reconstruction is

$$
\max_D\;V_U+PV[\mathrm{tax\ shields}(D)]-PV[\mathrm{distress\ costs}(D)].
$$

The review gives the economic ingredients, not a functional-form model or estimated optimizer. Distress costs include more than bankruptcy lawyers and administrative fees: possible default can distort operating and investment decisions before any filing occurs.

Safe tangible assets support more debt because losses in distress may be smaller and collateral more dependable. Risky intangible assets and valuable future growth opportunities can support less. Those predictions are plausible, but they are not unique signatures of a tax-distress optimum.

The more difficult fact is that profitable firms within an industry tend to borrow less. A simple tradeoff model might predict the opposite: profitable firms have more income to shield and can service debt with lower distress risk. Myers cites firms that maintain superior credit standing and little debt for years despite apparently valuable unused deductions. Graham's analysis suggested that approximately half the sample paid the full statutory rate, that the average firm could double interest payments while expecting doubled tax shields, and that more borrowing could add about 7.5% to firm value on average. These are cited estimates, not a new valuation calculated in the review.

Cross-country evidence on profitability is not completely uniform. The review cites Wald's strong profitability relation, while a footnote notes that Rajan and Zingales did not find significant correlations for France, Germany, Italy, and Britain. A substantive note should preserve that qualification rather than turn an often observed sign into an exceptionless law.

Tax-sensitive tactics are easier to document. The article describes preferred securities whose intercorporate dividends faced an effective tax rate of $0.30\times0.35=10.5\%$, finance leases that shift deductions to better positioned taxpayers, and trust structures issuing tax-deductible preferred securities. By the end of 1997, the latter example involved 285 issues totaling \$27 billion after initial success in 1993. These are historical arrangements, not current issuance instructions.

MacKie-Mason's probit evidence that low-marginal-tax firms choose equity, and Graham's evidence linking long-term borrowing changes to marginal tax rates, show taxes influencing decisions. Fama and French's failure to identify tax-shield value in their statistical search illustrates the harder valuation question. The review's criticism is methodological: a pattern compatible with two different theories cannot establish one simply because its coefficient has the predicted sign.

## The pecking order: information rather than a debt target

The Myers-Majluf setting contains assets in place and a growth opportunity requiring outside funding. Managers know more than investors about their value and act for existing shareholders. An equity issue may fund a positive-NPV project, but if the new shares sell too cheaply it can transfer sufficient value to new investors that existing shareholders prefer to forgo the project.

Investors recognize the selection: firms more willing to issue tend to have less favorable private valuations. An issue announcement can therefore lower the price even though the funds finance a productive project. The average issuer sells at a fair price conditional on the information revealed by issuance; this is not the same as saying every manager's private valuation equals the issue price. Some firms hold back because the terms are unattractive relative to their private information.

The cited announcement-price decrease is about 3% of pre-issue market capitalization. Its denominator is not the dollar amount raised. Myers explicitly distinguishes the price revision from underwriting costs: it is an informational revaluation, not a fee paid to an intermediary. A refused issue can nevertheless impose an economic opportunity cost by preventing a worthwhile investment.

Debt is less sensitive to uncertain firm value because it has a prior claim. Investment-grade debt, with limited default exposure, should convey much less adverse information than equity. In the stylized limit where firms can issue debt cheaply and safely, optimistic managers choose debt, making an equity attempt an unfavorable signal. Equity becomes relevant when debt is already costly, including when additional borrowing raises substantial distress risk.

The resulting ordering is internal finance first, then the safest available external claim, moving from safer to riskier debt and possibly hybrids, with equity last. Dividends are assumed sticky. A shortfall of internal funds after investment and dividends is met by borrowing; a surplus pays debt down. Borrowing is an accumulated consequence of financing needs rather than movement toward a target debt ratio.

Use a consistent positive-deficit convention:

$$
\mathrm{DEF}_{it}=I_{it}+\mathrm{DIV}_{it}-\mathrm{CF}_{it},
\qquad \Delta D_{it}\approx\mathrm{DEF}_{it},
$$

for the simplified regime where debt is the marginal external source. This notation omits other working-capital and financing adjustments that an empirical implementation must define. Printed p. 93 describes internally generated cash less investment and dividends, the opposite sign, but immediately calls the quantity a deficit financed by borrowing. The positive-deficit convention above follows the funding identity and the continuation on p. 94. This is an explicitly derived sign clarification, verified visually, rather than an unnoticed change in the source's words.

More profitable firms can then borrow less because they have greater internal resources, without any claim that their optimal target is lower. The argument requires assumptions about payouts, financing capacity, and managerial objectives. Flexible repurchases can absorb cash-flow fluctuations and weaken the simple debt-as-residual prediction; Myers explicitly notes this development in footnote 11.

## Statistical power: fitting one theory to data generated by another

The review contrasts two schematic empirical specifications. A target-adjustment regression uses a debt ratio $d_{it}$ and a target $d^*_{it}$:

$$
\Delta d_{it}=\lambda(d^*_{it}-d_{i,t-1})+\varepsilon_{it}.
$$

A simplified pecking-order regression instead relates net borrowing to the financing deficit:

$$
\Delta D_{it}=a+b\,\mathrm{DEF}_{it}+u_{it},
$$

with $a=0,b=1$ in the strict debt-residual version. These equations reconstruct the models described in the review; it does not provide the complete original estimation specification. Debt level and debt ratio must not be conflated, and the target is unobserved. Using a firm's full-sample average debt ratio as its target is an in-sample explanatory convention, not a real-time forecasting variable.

Shyam-Sunder and Myers tested 157 firms over 1971-1989. Both model classes appeared statistically successful on actual observations. They then generated financing histories under one model and fitted the competing model. A target-adjustment model fitted pecking-order-generated debt histories about as well as actual debt histories. Thus its apparent success was not discriminating evidence for a target.

The mechanism is that lumpy investment and business-cycle variation in internal cash can generate runs of deficits followed by surpluses, producing upward and downward debt movements that resemble reversion toward a target over the observed sample. This need not imply a theorem that arbitrary stationary deficits make debt levels stationary. A cumulated stationary deficit can still be nonstationary; the reported result concerns the empirical simulation and its financing patterns.

The reverse experiment was more discriminating: when histories were generated by gradual target adjustment, the pecking-order test failed. On that sample and those alternatives, the authors interpreted the asymmetry as evidence that the pecking-order test had useful power. It does not establish universal dominance of the pecking order across firms or later periods.

Myers extends the lesson to cross-sectional proxies. Variables intended to represent tax benefits, collateral, distress, or opportunities can correlate with financing deficits or managerial preferences. Plausible, significant coefficients can arise under the wrong structural interpretation. A credible test needs alternatives that reproduce the observational pattern and a demonstration that the chosen statistic separates them.

Exact replication of the cited experiment requires the 157-firm selection, accounting definitions, missing-data handling, target construction, simulated histories, initial debt, regression scaling, and inference procedure. This review reports neither those data nor coefficient estimates or standard errors. It supports reconstructing the identification logic, not claiming a reproduced empirical result.

## What the pecking order leaves unexplained

The information model assumes management cares about existing shareholders' wealth. It does not derive that objective from compensation, control rights, or an explicit employment contract. Alternative incentive models can produce similar financing choices. Consequently, observing an ordering of claims need not identify one specific informational story.

The review also asks why securities are not designed to avoid the information problem. If today's private information becomes public within a year, a firm could issue a claim repaid with shares worth a fixed \$1,000 at that future date. The share quantity is $N=1000/P_1$, where $P_1$ is the future stock price, rather than a fixed conversion ratio. The manager need not signal a view about today's share valuation by committing to that future conversion.

This deferred-equity example challenges the breadth of the theory rather than supplying a ready financing product. It assumes the relevant information resolves, the settlement price is meaningful, sufficient shares can be delivered, and the claim's other risks are addressed. Myers notes related preferred instruments but asks why the exact proposed form is not more prevalent. He does not solve its contracting, dilution, default, or market-design problems.

## Debt-equity conflicts and the cost of distress

When default is possible, shareholder actions can transfer value from creditors without raising the value of the underlying business. Myers distinguishes four channels. Risk shifting increases upside for residual equity while creditors absorb more downside. Additional borrowing followed by a payout can dilute the protection of old debt. Debt overhang discourages new equity-funded investment because part of the gain accrues to existing creditors. Delaying disclosure or reorganization can extend the effective maturity and risk of creditors' claims.

The underinvestment mechanism can be written without pretending the review supplies a calibrated model. Let a project cost $I$ and add gross value $G>I$ to the firm's claims. If existing creditors capture an increase $\Delta B$ in value, equity's net benefit from financing the project is $G-\Delta B-I$. Shareholders can reject a positive-NPV project when

$$
0<G-I<\Delta B.
$$

This is a derived accounting illustration of the mechanism, not an estimate. Future growth opportunities are especially vulnerable because they depend on decisions not yet made and are weak collateral. A promise to undertake every future positive-NPV project is generally not an enforceable complete contract.

Covenants restricting new borrowing, payouts, and other behavior can reduce these conflicts, often with acceleration rights on violation. The cited Asquith-Wizman evidence reports an average 5.2% loss in bond market value on LBO announcements for bonds lacking covenant protection. Bonds with strong covenants could instead gain. RJR Nabisco's existing debt reportedly lost more than 10% when its management proposed an LBO. Those observations show why changes in equity value alone are insufficient for evaluating financing actions.

The magnitude of lost investment is an empirical question. Myers's footnote cites Parrino and Weisbach's numerical experiments as finding few cases with large underinvestment losses at high debt ratios. The review therefore supplies both a mechanism and a warning against assuming its quantitative importance. The cost of distress can include ex ante distortions as well as ex post workout costs, but neither component is calibrated universally here.

## Managerial agency and free cash flow

Complete alignment between management and investors is implausible. Managers can value pay, job security, perks, and investments that entrench their particular skills. Monitoring is costly, and compensation cannot depend perfectly on effort or decisions that outsiders cannot observe or verify. Corporate outcomes also contain much variation unrelated to managerial contribution.

Jensen's free-cash-flow theory addresses firms whose operations generate more funds than worthwhile investment requires. A large mandatory payout financed with debt can force asset sales, cancel wasteful projects, and sharpen managerial incentives. Myers interprets many 1980s leveraged buyouts and later leveraged restructurings as responses to this problem, while acknowledging tax, financing-price, creditor-transfer, and other stakeholder explanations.

The theory is conditional in two senses. It is most relevant to mature, cash-rich firms inclined to overinvest. It also often describes consequences of externally imposed leverage rather than management's voluntary choice. Hostile takeover pressure may be necessary precisely because the managers who would lose discretion do not want the value-maximizing restructuring. The source cites Sealed Air as an important voluntary case, not a universal pattern.

Myers does not claim most public firms overinvest or that ordinary debt issues generally raise equity prices through discipline. Capital expenditure announcements are often good news, and the cited Shyam-Sunder study finds no significant stock-price effect for debt-issue announcements even for junk debt. Debt's control value can be large in a particular restructuring without being the dominant driver of capital structure throughout a heterogeneous panel.

This also connects managerial preferences to the tradeoff puzzle. Management may resist debt levels that exploit more tax benefits because the associated personal risk or loss of flexibility is unattractive. But asserting that managers are conservative does not by itself supply a testable economic model; their objectives and constraints need to be specified.

## Implications for research design and implementation

The three theories differ in their main state variable and decision margin:

| Theory | Main mechanism | Critical conditional distinction | Main implementation gap in this review |
|---|---|---|---|
| Tax-distress tradeoff | Marginal tax value versus expected distress cost | Tax capacity, asset risk, collateral, and investment opportunities | No estimated objective or firm-specific optimum |
| Pecking order | Security issuance under asymmetric information | Internal cash, sticky payouts, financing deficit, and remaining debt capacity | No complete data definitions or endogenous managerial objective |
| Free cash flow | Debt commits surplus resources and shifts control | High cash generation with weak opportunities and weak internal discipline | No universal prediction of voluntary leverage choice |

An applied model should separate book from market financing measures, gross from net debt, outstanding stocks from new financing flows, and promised yield from expected debt return. It should define which information was observable at each decision date. A full-sample average target or ex post estimate of profitable opportunities cannot silently become a real-time predictor.

The review offers no asset-selection rule, portfolio construction, realized strategy return, transaction-cost estimate, or capital-structure-arbitrage implementation. Its historical announcement results and country ratios are evidence used to compare explanations. They are not prospective excess returns available from buying a balance-sheet characteristic.

The conclusion points toward organizational objectives. Insiders invest time, specialized human capital, and personal risk in the firm and expect future benefits, including wages above outside alternatives, shares, options, and private benefits. A broader theory might model the joint investment of human and financial capital and the terms on which outsiders finance insiders who retain some control. Myers explicitly presents this as unfinished research, not a completed fourth model with an optimal debt solution.

The practical research lesson is to test the mechanism in the setting where it should operate and to measure the test's ability to reject plausible alternatives. Financing choices can reveal taxes, private information, and control conflicts, but a successful reduced-form fit does not identify which objective the organization is pursuing.
