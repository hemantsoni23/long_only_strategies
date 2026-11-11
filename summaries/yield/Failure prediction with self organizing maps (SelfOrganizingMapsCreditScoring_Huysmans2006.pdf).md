# Failure prediction with self organizing maps

Johan Huysmans, Bart Baesens, Jan Vanthienen, and Tony van Gestel. *Expert Systems with Applications* 30 (2006), 479–487. DOI: 10.1016/j.eswa.2005.10.005.

Source: [original PDF](../../Finance/SelfOrganizingMapsCreditScoring_Huysmans2006.pdf). All nine pages, including references, were read. Equation and table numbers below refer to the article; printed page 479 is PDF page 1. The maps, error plots, stacking diagram, weighting experiment, and numerical tables were inspected visually.

## Why this matters

A credit model may separate good and bad accounts while giving analysts little sense of where errors concentrate or which customer groups are poorly understood. A self-organizing map, or SOM, places representative feature vectors on a small grid that can display customer characteristics, class frequencies, and prediction errors together. Its main attraction in this paper is that common visual representation. The basic map does not, by itself, optimize the separation of good and bad borrowers.

Huysmans and coauthors test whether supervised classifiers can improve SOM prediction without discarding the maps. They consider two integrations: specialized classifiers for poorly performing map cells, and a map trained on original inputs augmented by a neural-network score. The former makes small improvements on one data set and larger but still limited improvements on the other. The latter approaches the underlying neural network’s accuracy as that score receives more weight in map formation. The evidence supports the map as an exploratory or diagnostic interface; it does not show a general accuracy advantage over a strong standalone supervised model.

An important qualification is that the preprocessing uses class labels to encode categorical variables through weight of evidence. The SOM weight-update rule is unsupervised, but the entire pipeline is not independent of outcomes. This distinction matters both for interpreting the pictures and for keeping test labels out of training.

## Samples, comparison protocol, and what is undisclosed

The study uses two proprietary consumer-credit data sets from a major Benelux financial institution. Bene1 has 3,123 observations and 27 variables, with an approximately 67:33 good/bad ratio. Bene2 has 7,190 observations and 27 variables, with an approximately 70:30 ratio. Two-thirds of each sample train models and one-third forms a test sample. The authors reuse exactly the training and test sets from the Baesens et al. (2003) benchmark, facilitating comparison on those observations.

Table 1 reports the prior benchmark’s best Bene1 method as an RBF least-squares SVM, with 73.1% accuracy, 83.9% sensitivity, and 52.6% specificity. Bene2’s best method is a multilayer perceptron, with 75.1%, 86.7%, and 48.1%, respectively. Here sensitivity means the fraction of good accounts correctly identified, while specificity means the fraction of bad accounts correctly identified. A reader accustomed to treating default as the positive class must reverse that convention before comparing recall measures.

The article does not disclose application dates, outcome observation windows, delinquency thresholds defining “bad,” loan amounts or products by sample, complete feature names, original case identifiers, missing-value treatment, or the institution. It does not establish that the split is chronological or that customers with multiple applications are confined to one split. Those gaps prevent reconstruction of a prospective lending experiment or evaluation of performance after a regime change.

The same proprietary split controls a useful part of the comparison, but the reported local-neural-network repetitions are not independent resamplings of the borrower population. Their 100 trials primarily address algorithmic variation on the retained sample. No standard deviations, confidence intervals, or paired significance tests accompany the improvements. The paper also does not report an untouched validation set for choosing the cell-accuracy threshold or score weighting.

## Preprocessing defines the geometry

Categorical inputs include loan purpose and residential status. Instead of creating many dummy variables, the paper replaces each category $v$ by

$$
WOE(v)=\log\frac{P(X=v\mid G)}{P(X=v\mid B)}
=\log\frac{n_{Gv}/n_G}{n_{Bv}/n_B}.
$$

This is the meaning of equation (2), despite its compressed probability notation. It is a ratio of class-conditional category frequencies, not simply $\log P(G\mid v)/P(B\mid v)$. Bayes’ rule relates the latter posterior log odds to WOE by adding $\log[P(G)/P(B)]$. Higher WOE therefore denotes a category associated with good borrowers relative to the sample’s base rate.

All variables are then standardized to zero mean and unit variance. This is consequential because Euclidean distances define which neuron wins. Without scaling, a variable expressed in large currency units can dominate a count or a bounded ratio. With scaling, each original coordinate receives comparable marginal variance, although correlated coordinates may still count the same economic information more than once.

A reproducible pipeline must estimate category frequencies and scaling parameters using the training sample only, then freeze them for validation and test cases. The paper does not explicitly state the estimation boundary. It also gives no smoothing for $n_{Gv}=0$ or $n_{Bv}=0$, no treatment of unseen categories, and no rule for missing values. Raw WOE can diverge in sparse categories. Adding pseudocounts or pooling rare levels would be sensible implementation choices, but their values would be additions to the reported method.

Because WOE uses $G/B$ labels, the resulting feature geometry already reflects historical credit performance. A map that separates risks after this transformation is not evidence that purely label-free customer attributes spontaneously divide into the same groups. Conversely, this supervised preprocessing can be useful if its estimation is correctly confined to training data.

## The SOM update and its interpretation

Associate each grid neuron $c$ with a vector $w_c\in\mathbb R^{27}$ and a fixed grid position $r_c$. For a standardized observation $x$, choose the best matching unit

$$
b(x)=\arg\min_c\|x-w_c\|_2^2.
$$

Equation (1) updates the winning neuron and its neighbors:

$$
w_c^{\rm new}=w_c+\eta(t)\Lambda_{b(x),c}(t)(x-w_c).
$$

The learning rate $\eta(t)$ decreases with training time. The neighborhood function decreases with distance on the grid and typically has Gaussian form,

$$
\Lambda_{b,c}(t)=\exp\left[-\frac{\|r_b-r_c\|^2}{2\sigma_t^2}\right],
$$

with decreasing radius $\sigma_t$. This Gaussian formula makes the stated family explicit; the source does not provide the actual schedule or its numerical parameters. Initialization, presentation order, number of epochs, convergence tolerance, and random seeds are likewise missing. Analyses use the SOM Toolbox for MATLAB.

The update moves neighboring grid units toward similar input examples, encouraging nearby grid cells to represent similar feature vectors. The source describes SOMs as topology preserving, but that is an algorithmic tendency rather than a guarantee that every neighborhood in 27 dimensions survives compression to two dimensions. Grid location is also arbitrary up to rotations or rearrangements induced by initialization. An “upper” high-risk region in one map is not a fixed economic coordinate system transferable to another fitted map.

The exploratory example uses a 4-by-6 grid, also described as 6-by-4 elsewhere: 24 neurons. A U-matrix visualizes distances between adjacent prototypes. In Figure 1, small distances are dark and large ones light. Distinct dark regions separated by bright boundaries would suggest clusters. The authors find no strong separation in Bene1. This is a visual description, not a formal statistical test that all possible customer clusters are absent.

Figures 2–3 show good/bad training and test hits for each neuron. The upper-left training neuron receives 122 goods and 97 bads, 219 observations altogether. Its observed good fraction is $122/219=55.71\%$, rounded to about 55% in the text. Mixed cells show why a geometric partition can be a poor classification partition. The class bars in Figure 3 have different scales, a detail that matters when comparing their visual heights.

A component plane displays one coordinate of $w_c$ across the map. Figure 4 shows that newer clients lie primarily in the region containing more bad borrowers. The paper also compares loan purpose, age, loan amount, and loan duration. Such pictures reveal co-location of attributes and model scores. They do not estimate conditional causal effects or show what would happen if one changed an applicant’s age, tenure, or loan request while holding other features fixed.

For larger maps, the study creates 400 neurons, clusters them with Ward’s hierarchical method, and initializes k-means from the resulting centroids. Figure 5 assumes five clusters. Labels are assigned by visually comparing cluster shapes with component planes; the authors do not use the statistical salient-dimension labeling procedure they discuss from earlier work. New-car and real-estate purposes occupy the high-WOE area in the loan-purpose plane; unspecified purpose and secondhand cars tend to appear elsewhere. There is no reported selection criterion showing that five clusters are optimal.

## Turning prototypes into credit predictions

The first classifier gives each neuron the label of the closest training observation. A new case inherits the label of its best matching unit. This nearest-training-observation labeling can be unstable: one nearby case can determine the label of a cell receiving many cases from the other class. Bene1 obtains only 57.5% accuracy, 22.3% bad recall, and 76.1% good recall. Bene2 obtains 66.1%, 14.5%, and 88.3%.

The second rule labels a neuron by the majority of training observations projected onto it. For a fixed map and unweighted zero-one loss, this maximizes in-sample accuracy among constant labels assigned to that cell. It guarantees weakly better training accuracy than another fixed cell label, not strictly better test accuracy. Empty cells and tied class counts need conventions that are not specified in the article.

The cell fraction can also be retained as a score,

$$
\widehat p_B(c)=\frac{n_{Bc}}{n_{Bc}+n_{Gc}}.
$$

Classifying a cell as bad when $\widehat p_B(c)>1/2$ reproduces majority voting. With false-accept cost $C_B$ for a bad borrower labeled good and false-reject cost $C_G$ for a good borrower labeled bad, expected losses are $C_Bp_B$ for “good” and $C_G(1-p_B)$ for “bad.” The latter is preferred when

$$
p_B>\frac{C_G}{C_B+C_G}.
$$

Thus $C_B=2C_G$ gives the paper’s one-third threshold. This is a loss-sensitive classification rule, not a fitted estimate of actual lending profits. No monetary cost inputs are supplied. Lowering the bad threshold raises bad recall and lowers good recall; a claim of better economics additionally requires realistic costs and calibrated probabilities.

Majority voting gives Bene1 accuracy 71.0%, bad recall 44.6%, and good recall 84.9%. Its AUC is .734. Bene2 gives 69.7%, 0.6%, and 99.34%, with AUC .6248. In Bene2 all but one cell receive a good label. Its nominal accuracy is therefore close to the approximately 70% always-good baseline, despite identifying almost none of the bad cases at that threshold. Reporting only 69.7% would conceal the operational failure.

Figures 8–9 locate errors. Fifty-three bad test observations fall on the upper-left Bene1 neuron and are misclassified because it has a good label. Absolute error count should be interpreted together with cell occupancy and error proportion. A frequently visited cell with modest error can contribute more total mistakes than a rare cell with poor accuracy. The figures distinguish those two quantities, a practical advantage of the SOM display.

These are test-data diagnostics. The discussion notes that reversing cells with test accuracy below one-half would improve that particular test score. Doing so would convert the test sample into training information. The paper’s subsequent local models are explicitly based on training-cell accuracy, but the diagnostic suggestion itself is not a valid procedure for obtaining an untouched-test performance estimate.

## Separate maps for the two classes

A third approach trains a good-only map and a bad-only map. For a new $x$, compute the nearest prototype distance to each map and select the class whose map is closer. This uses labels in allocating training observations. It differs from a single map with post-training labels and does not automatically incorporate class priors or misclassification costs.

With 24 neurons in each map, Bene1 accuracy/bad recall/good recall are 66.4/79.7/59.4%, and Bene2 gives 64.5/73.6/60.6%. Bad detection rises sharply relative to majority voting, while many more good cases are rejected. Increasing the good map to 8-by-6, or 48 neurons, while retaining a 24-neuron bad map gives 68.1/66.6/68.9% for Bene1 and 68.5/59.2/72.4% for Bene2.

This illustrates a geometric operating-point effect. Giving a class more prototypes can make its nearest distances smaller over more of feature space and therefore expand its prediction region. Map-size asymmetry is not a transparent substitute for a probability threshold: it changes representation capacity and classification at once. The source does not systematically optimize map size or show that a particular allocation corresponds to an economic loss ratio.

## Local supervised refinement

Section 7.1 retains ordinary map labels for cells with high training accuracy and trains an independent feedforward network for each low-accuracy cell. The network uses only training cases projected onto that cell. This makes the SOM a gate selecting either a simple constant label or a local nonlinear model.

For Bene1, the training-accuracy threshold is 58%, chosen by trial and error. Three cells receive local models: the first two in the top row and the third in the third row. Several hidden-layer sizes are tested, with one hidden unit performing best. Averaged over 100 trials, test accuracy rises from 71.0% to 71.3%. Bad recall rises from 44.6% to 52.6%, while good recall falls from 84.9% to 81.5%. The 0.3-point accuracy gain is small, but the change in error composition is more substantial.

For Bene2, a 65% threshold triggers nine local classifiers. Average test accuracy rises from 69.7% to 71.9%; bad recall increases to 26.8% and good recall declines to 91.1%. The method therefore recovers some bad-account detection from a map that nearly always predicted good, but remains below the 75.1% standalone MLP accuracy from the benchmark.

The experiment does not establish statistical significance of either gain. Trial-and-error threshold selection lacks a disclosed separate validation procedure, and the paper does not give local sample sizes, network objectives, optimization settings, or trial dispersion. The fact that the simplest one-hidden-unit model works best is consistent with limited within-cell data, but is not a demonstrated explanation.

The authors suggest requesting extra information only for applicants assigned to ambiguous cells. That is an interesting use of the map as a triage mechanism. No new information is actually collected in the experiment, and no acquisition cost or measured improvement is supplied. A future implementation would need to value the additional measurement against the expected reduction in classification loss.

## A supervised score as an extra map coordinate

Section 7.2 trains a global two-hidden-unit MLP first. Its average accuracy is 72.5% for Bene1 and 75.1% for Bene2. The original training vectors are augmented with the MLP output $s(x)$, and the SOM is trained in the resulting feature space. Although Figure 10 depicts several base learners, the experiment uses one.

The best-matching-unit calculation uses the weighted squared distance

$$
d_c^2(x)=\sum_{j=1}^{27}(x_j-w_{cj})^2
+\lambda\{s(x)-w_{c,s}\}^2.
$$

The 27 original weights equal one, and the MLP-coordinate weight $\lambda$ varies from 1 to 100. Equation (3) labels the sum as a norm, but it is a squared-distance expression; omitting the square root does not change the winning neuron. The usual prototype update remains unchanged. The modification acts through winner selection.

For a large $\lambda$, neurons are selected mainly to match the MLP score. This explains why the map’s predictions tend to resemble the supervised model more closely as $\lambda$ increases. It does not imply that the map learns independent additional credit information. It may mostly organize or discretize an existing forecast.

Figure 11 shows majority-vote performance above nearest-observation labeling across the displayed range, with irregular changes as the weight varies. At large weights, Bene2 majority-vote accuracy is visually around 74%, approaching but not clearly surpassing the 75.1% MLP benchmark; Bene1 majority-vote accuracy fluctuates near its low-70% baseline. The figure gives no numerical table for every weight, no error bars, and no uniquely selected optimum. Exact improvement percentages should not be manufactured from the curves.

The paper says that the MLP is trained using the available training observations and that its output augments the SOM’s training inputs. It does not describe out-of-fold generation of that score. In-sample base-model outputs can be more optimistic than predictions on unseen applicants, causing a mismatch for the second-stage map. Cross-fitted base predictions would address that issue, but would be a modified experiment. The MLP-output scaling relative to the standardized original features is also not fully documented; $\lambda$ has meaning only together with those scales.

The score component plane resembles the tenure and age planes more than loan amount or duration. The authors interpret that as greater relevance of tenure and age. It is evidence about spatial agreement within the learned map, not a conditional feature-importance measure. Correlated covariates, WOE transformations, and the trained score all influence the same geometry.

## Evidence boundary and replication requirements

The complete numerical summary in Table 2 uses accuracy/bad recall/good recall, in that order:

| Method | Bene1 | Bene2 |
|---|---|---|
| Nearest training observation | 57.5 / 22.3 / 76.1 | 66.1 / 14.5 / 88.3 |
| Majority vote | 71.0 / 44.6 / 84.9 | 69.7 / 0.6 / 99.34 |
| Two equal maps | 66.4 / 79.7 / 59.4 | 64.5 / 73.6 / 60.6 |
| Unequal maps | 68.1 / 66.6 / 68.9 | 68.5 / 59.2 / 72.4 |
| Local neural refinement | 71.3 / 52.6 / 81.5 | 71.9 / 26.8 / 91.1 |

A replication needs the original split and raw categories, a training-only WOE dictionary and standardization, specified SOM topology and training schedules, all node-label rules, local-network settings, and score-weight selection rules. To make a stronger operational claim, it also needs borrower-level uncertainty estimates, a later cohort, probability calibration, rejection/approval costs, and an audit of repeated borrowers. These are missing inputs or proposed validation improvements, not hidden details recoverable from the plotted maps.

No realized cash-flow, capital, default-loss, or collection-cost experiment is provided. The study does not prove that visual interpretability yields better lending decisions, nor that the map accurately explains every input’s effect on a neural score. What it does supply is a useful way to display mixed-risk neighborhoods and concentrated errors while retaining a common representation across several classification schemes. The most defensible role is diagnostic and exploratory, with any predictive benefit evaluated against the standalone supervised model and the actual cost of each type of mistake.
