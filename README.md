# The Broker's Paradox 🎭

**Testing Burt's Structural Holes Theory on 168,000 Twitch Streamers**

A graduate data-mining project testing a classic 30-year-old theory of social capital against modern creator-economy data. The finding: Ronald Burt's *structural holes* theory partly survives — but **language is a wall the theory does not cross**.

> 👉 **Start here: [`main_notebook.ipynb`](main_notebook.ipynb)** — the curated story of the project.
> 🎥 **2-minute pitch video:** [youtu.be/U0zgOHqXI7Q](https://youtu.be/U0zgOHqXI7Q)

---

## Overview

For three decades, Ronald Burt's *structural holes* theory has argued that people who bridge disconnected groups enjoy a success premium — faster promotions, higher pay, better ideas. The theory has been validated across managers, scientists, investment bankers, and TQM teams. It has **never been rigorously tested on a creator platform**.

We test it on the SNAP Twitch Gamers dataset — **168,114 streamers** linked by **6.8 million mutual-follow ties**, with Twitch Affiliate status (the platform's monetization gate, ~49% prevalence) as a clean binary success outcome. The analytical sample is **165,009 streamers** (mega-hubs with degree > 500 are excluded for computational tractability).

We operationalize "bridge" three ways — ego-network brokerage (Burt's classical constraint), cross-community bridging via Louvain, and cross-language bridging — and find them nearly uncorrelated (pairwise Spearman 0.07–0.26). Controlling for degree, account age, and language-majority status:

| Bridge type | Odds Ratio (per 1-SD) | 95% CI | Verdict |
|---|---|---|---|
| **Ego-network brokerage** (Burt 1992) | **1.320** | [1.293, 1.348] | 🟢 **Pays** (p < 0.001) |
| Structural community bridging (Louvain) | 1.014 | [1.001, 1.028] | ⚪ Flat on average (hides subgroup heterogeneity) |
| **Cross-language bridging** | **0.933** | [0.919, 0.946] | 🔴 **Hurts** (p < 0.001) |

**McFadden pseudo-R² = 0.094.** A likelihood-ratio test confirms the bridge measures add joint explanatory power beyond controls (χ² = 920.92 on 3 df, p ≈ 0).

### Additional findings that sharpen the picture

- **English/non-English asymmetry (formally confirmed by interaction test).** `pc_language × is_english` OR = **0.733** (p < 0.001). Disaggregated: non-English speakers who bridge *toward* English are rewarded (OR = 1.23); English speakers who bridge *outward* are penalized (OR = 0.91). The penalty is a majority-language phenomenon.
- **Affiliate-vs-views inversion.** An OLS on `log_views` (R² = 0.35) reveals that brokerage *hurts* total views (coef = −0.19), while cross-language bridging *helps* total views (coef = +0.23). **Affiliate and views reward opposite network structures** — depth within a community vs. reach across them. "Creator success" is not a single thing.
- **Structural heterogeneity of `pc_louvain`.** Flat at the aggregate but strongly positive for English speakers and large streamers (OR ≈ 1.03–1.15) and strongly negative for non-English speakers and small streamers (OR ≈ 0.80–0.96). The aggregate null masks two opposing subgroup effects.
- **Bridge burnout — null result honestly reported.** Burt's (2004) specific brokerage-cost prediction on churn is **not supported** (brokerage OR = 1.024 on `dead_account`, p = 0.14). Two ancillary findings: structural community bridging predicts higher churn (OR = 1.25); cross-language bridging predicts *lower* churn (OR = 0.71). These are interesting but are not confirmations of Burt's theoretical mechanism.

### Robustness

- **Node2vec robustness:** a fourth, partition-free bridge measure (participation coefficient over node2vec embedding clusters) leaves the main regression coefficients virtually unchanged. The finding is not an artifact of Louvain specifically.
- **VIFs all < 2.3** — no multicollinearity.
- **Calibration Brier score = 0.219** (vs. 0.25 uninformative baseline); predicted probabilities track observed rates across deciles.
- **Propensity-score matching ATT = −8.6pp** for the composite broker label (reflects net effect across the three opposing measures).

### Honest limitation on predictive power

Adding the three bridge measures to the controls-only model lifts 5-fold CV AUC only modestly — **0.698 → 0.701**. The bridge measures are **statistically and theoretically significant, but predictively secondary**. This is consistent with a theory-test scope (effect identification, not prediction), and we report it transparently rather than overclaim.

---

## Research question

> **On Twitch, do streamers who bridge disconnected communities enjoy a success premium — as Burt's classic social-capital theory predicts — after controlling for reach and tenure? And does the answer depend on what kind of bridge we mean?**

**Answer:** Yes, at the ego-network scale (Burt replicates). No, at linguistic boundaries (the theory inverts). Subgroup-dependent in between.

---

## Project video

🎥 **[The Broker's Paradox — 2-minute pitch](https://youtu.be/U0zgOHqXI7Q)**

A 2-minute narrated slide deck introducing the motivation, method, and headline finding. Built for investors / recruiters / anyone curious who doesn't want to read a notebook.

---

## Repo structure

```
.
├── README.md                       ← this file
├── main_notebook.ipynb             ← 👉 THE MAIN DELIVERABLE — start here (50 cells)
├── requirements.txt                ← pip freeze from the Colab session
├── SUBMISSION_CHECKLIST.md         ← step-by-step submission guide
├── .gitignore
│
├── checkpoints/                    ← semester-progression artifacts (graded earlier)
│   ├── checkpoint_1.ipynb          ← three candidate datasets (explored, then narrowed)
│   └── checkpoint_2.ipynb          ← three candidate RQs (narrowed to one per guidance)
│
├── src/                            ← reusable helper modules
│   ├── __init__.py
│   └── graph_metrics.py            ← participation_coefficient, fit_logit_with_inference, compute_vif
│
├── scripts/
│   └── download_data.py            ← fetches SNAP Twitch Gamers (~15MB) into .data/
│
├── data/                           ← raw data lives here locally (gitignored)
├── cache/                          ← gitignored; expensive computations are cached here
└── assets/
    └── figures/                    ← PNGs rendered by the notebook
```

---

## Data

**Dataset:** [SNAP Twitch Gamers](https://snap.stanford.edu/data/twitch-social-networks.html) (Rozemberczki & Sarkar, 2021)

- 168,114 nodes (Twitch streamers, snapshot ca. Spring 2018)
- 6,797,557 edges (mutual-follow ties, undirected; graph is a single connected component)
- Node attributes: `views`, `language`, `created_at`, `updated_at`, `life_time`, `affiliate`, `dead_account`, `mature`

The dataset is **not committed** to the repo (≈15 MB zipped). Download it with:

```bash
python scripts/download_data.py
```

Or run the notebook — it fetches + extracts on first run.

**Preprocessing highlights** (all in `main_notebook.ipynb`):
- Degree computed from edge counts; log-transformed to tame the long tail
- Account age derived from `created_at` against the snapshot date (Oct 2018)
- `life_time` dropped from regression controls due to collinearity with `account_age_days`
- Burt's constraint computed only for nodes with degree ≤ 500 (~98.2% of the sample); mega-hubs flagged and excluded
- Both NetworkX and igraph graph objects built — NetworkX for flexibility, igraph for C-speed centrality

---

## How to reproduce

**Built in Google Colab (default runtime, 12 GB RAM, no GPU required).** Full pipeline:

1. **Clone the repo:**
   ```bash
   git clone https://github.com/sandsinghal/brokers-premium.git
   cd brokers-premium
   ```

2. **Open `main_notebook.ipynb` in Colab** (or local Jupyter).

3. **Run all cells.** The notebook:
   - Installs dependencies (first cell — restart runtime after)
   - Downloads the dataset (~15 MB) if not already present
   - Computes all graph metrics and caches them under `cache/`
   - Produces all figures under `assets/figures/`
   - Writes a final results JSON to `cache/final_results.json`

**Runtime:**
- First run from scratch: ~20–25 minutes
  - Louvain: ~9 min
  - Burt's constraint: ~9 min
  - Node2vec: ~7 min
  - Other: ~1 min
- Subsequent runs with caches: ~30 seconds

**Memory note:** Node2vec is the heaviest step. We use a memory-safe implementation (dim=32, walk_len=10, num_walks=5, streaming walks + gensim Word2Vec, MiniBatchKMeans clustering) that stays under ~8 GB peak RAM. If it still OOMs on a lower-memory machine, the notebook gracefully skips the node2vec robustness check — the main findings do not depend on it.

---

## Key dependencies

Built with (Python 3.12, Colab Apr 2026):

| Package | Version |
|---|---|
| Python | 3.12 (Colab default) |
| numpy | < 2.0 (pinned — pandas compatibility) |
| pandas | ≥ 2.0 |
| scipy | ≥ 1.11 |
| scikit-learn | ≥ 1.4 |
| networkx | ≥ 3.2 |
| igraph | ≥ 0.11 |
| python-louvain | ≥ 0.16 |
| gensim | ≥ 4.3 (for node2vec) |
| matplotlib | ≥ 3.8 |
| pyarrow | ≥ 15.0 (for parquet caching) |

Full list in [`requirements.txt`](requirements.txt).

---

## Results visualized

### The main finding

![Main finding — forest plot](assets/figures/fig_forest_bridge_premium.png)

Three operationalizations of "bridge" predict Affiliate status in three directions:

- **Ego-network brokerage pays** (Burt's theory replicates at the local scale)
- **Structural community bridging is flat on average** (but masks strong subgroup heterogeneity — see below)
- **Cross-language bridging is penalized** (audience fragmentation breaks the theory at cultural boundaries)

### Where the premium lives

![Heterogeneity across subgroups](assets/figures/fig_heterogeneity.png)

The cross-language penalty is entirely a majority-language (English-speaker) phenomenon; minority-language streamers bridging to English are rewarded. Formally confirmed via the interaction test (`pc_language × is_english` OR = 0.733, p < 0.001).

---

## Limitations and future work

- **Cross-sectional snapshot (2018)** — our findings are correlational, not causal. A longitudinal panel would support within-streamer fixed effects, dramatically strengthening identification.
- **Degree cap on Burt's constraint** excludes ~1.8% mega-hubs — conservative for our scientific question but limits generalizability to elite streamers.
- **One platform, one year.** Whether the cross-language penalty holds in 2025 or on YouTube/TikTok is an open question.
- **Modest predictive gain.** The bridge measures add ~0.003 AUC points — strong effect identification, weaker prediction. Honest about scope: this is a theory-test, not a predictive engineering project.
- **Future directions:** longitudinal panel with fixed effects; instrumental-variable designs using exogenous network churn; direct audience-overlap measurement to test the fragmentation mechanism; cross-platform replication; field experiment in partnership with Twitch.

---

## Author

**Shivam Singhal** — CSCE 676 (Data Mining), Spring 2026, Texas A&M University
GitHub: [@sandsinghal](https://github.com/sandsinghal)

---

## References

- **Burt, R. S. (1992).** *Structural Holes: The Social Structure of Competition.* Harvard University Press.
- **Burt, R. S. (2004).** Structural holes and good ideas. *American Journal of Sociology*, 110(2), 349–399.
- **Guimerà, R., & Amaral, L. A. N. (2005).** Functional cartography of complex metabolic networks. *Nature*, 433(7028), 895–900.
- **Blondel, V. D., Guillaume, J. L., Lambiotte, R., & Lefebvre, E. (2008).** Fast unfolding of communities in large networks. *Journal of Statistical Mechanics*, 2008(10), P10008.
- **Grover, A., & Leskovec, J. (2016).** node2vec: Scalable feature learning for networks. *KDD '16*.
- **Rozemberczki, B., & Sarkar, R. (2021).** Twitch Gamers: A Dataset for Evaluating Proximity Preserving and Structural Role-based Node Embeddings. *arXiv:2101.03091*.
- **Rosenbaum, P. R., & Rubin, D. B. (1983).** The central role of the propensity score in observational studies for causal effects. *Biometrika*, 70(1), 41–55.

---

*Social capital, it turns out, is not cultureless.*
