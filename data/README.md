# Data

Raw data is not committed to this repository.

To download the SNAP Twitch Gamers dataset (~15 MB zipped):

```bash
python scripts/download_data.py
```

The data will be placed in `.data/` at the repo root (gitignored).

Or simply run `main_notebook.ipynb` — it auto-downloads on first run.

## Dataset details

- **Source:** https://snap.stanford.edu/data/twitch-social-networks.html
- **Citation:** Rozemberczki, B., & Sarkar, R. (2021). Twitch Gamers: A Dataset for Evaluating Proximity Preserving and Structural Role-based Node Embeddings. *arXiv:2101.03091*.
- **Files after extraction:**
  - `large_twitch_edges.csv` — 6,797,557 undirected mutual-follow edges
  - `large_twitch_features.csv` — 168,114 nodes with attributes (views, language, affiliate, mature, etc.)
