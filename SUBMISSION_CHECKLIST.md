# SUBMISSION CHECKLIST — The Broker's Paradox

Due **April 27, 2026**. Submit: **public GitHub repo URL**.

Everything below is already built in this folder. Your job is to push it to GitHub and verify public access. Follow the steps in order.

---

## Step 1 — Create the GitHub repo

Go to https://github.com/new and create a **public** repo:

- **Name:** `brokers-premium` (or whatever you prefer — just update README link at the end)
- **Description:** `Testing Burt's structural holes theory on 168K Twitch streamers | CSCE 676 Spring 2026`
- **Visibility:** **Public** ✅
- **Initialize:** leave all boxes unchecked (no README, no .gitignore, no license — we have all this)

## Step 2 — Push this directory as the repo's contents

From inside the repo folder (`brokers_premium_repo/`):

```bash
cd brokers_premium_repo

git init
git add .
git commit -m "Final deliverable: The Broker's Paradox"
git branch -M main
git remote add origin https://github.com/sandsinghal/brokers-premium.git
git push -u origin main
```

If prompted for credentials, use a personal access token (GitHub → Settings → Developer settings → Personal access tokens).

## Step 3 — Regenerate requirements.txt from your actual Colab session (IMPORTANT)

The current `requirements.txt` is the intended minimal set. The professor asked for the *actual* frozen environment. Run this in a cell at the bottom of your Colab notebook:

```python
!pip freeze > requirements.txt
from google.colab import files
files.download('requirements.txt')
```

Then replace the `requirements.txt` at the repo root with the downloaded one:

```bash
# Move your downloaded file into the repo
mv ~/Downloads/requirements.txt requirements.txt
git add requirements.txt
git commit -m "Update requirements.txt from actual Colab environment"
git push
```

Also grab your Python version from Colab for the README:

```python
!python --version
```

## Step 4 — Run the main notebook end-to-end ONE more time

This ensures all cells have outputs committed, which makes the repo browsable from GitHub without running anything.

1. Open `main_notebook.ipynb` in Colab
2. `Runtime` → `Run all`
3. Wait for completion (~45 min first time with node2vec; ~30s with caches)
4. File → Download → `.ipynb`
5. Replace the local file:
   ```bash
   mv ~/Downloads/main_notebook.ipynb main_notebook.ipynb
   git add main_notebook.ipynb
   git commit -m "Final notebook with all cell outputs"
   git push
   ```

## Step 5 — Verify the repo is genuinely public

Open an **incognito / private browser window** and navigate to:

```
https://github.com/sandsinghal/brokers-premium
```

You should see the README rendered with the forest plot image. If you see "404 Not Found" or a login wall, the repo is not actually public — go back to Settings → General → scroll to Danger Zone → Change visibility.

## Step 6 — Submit on Canvas

Copy the URL: `https://github.com/sandsinghal/brokers-premium`

Paste into the Canvas submission for the Final Deliverable.

---

## What's in the repo

```
brokers-premium/
├── README.md                       ← full project description with figures
├── main_notebook.ipynb             ← the main deliverable (38+ cells, narrated)
├── requirements.txt                ← pip freeze from Colab (UPDATE THIS — see Step 3)
├── .gitignore
│
├── checkpoints/                    ← semester progression
│   ├── checkpoint_1.ipynb
│   └── checkpoint_2.ipynb
│
├── src/                            ← reusable helpers
│   ├── __init__.py
│   └── graph_metrics.py
│
├── scripts/
│   └── download_data.py
│
└── assets/figures/                 ← rendered figures (forest, heterogeneity, etc.)
    ├── fig_forest_bridge_premium.png
    ├── fig_heterogeneity.png
    ├── fig_dataset_overview.png
    └── fig_three_bridges.png
```

---

## Last-minute polish (optional but recommended)

- [ ] Verify YouTube video is set to **Unlisted** (not Private) — graders need access without requesting it
- [ ] Add a short paragraph to the top of the README if there's any unique context you want recruiters to see (you mentioned this repo may be useful for job apps)
- [ ] Check that `assets/figures/fig_forest_bridge_premium.png` renders correctly in the README preview on GitHub
- [ ] If any cell in the notebook shows an error output, re-run that specific cell and recommit

---

## If something breaks

- **Notebook won't render on GitHub:** GitHub's renderer can choke on very large notebook outputs. If you see "file too large," strip the outputs: `jupyter nbconvert --clear-output main_notebook.ipynb`, re-run, commit, then re-push.
- **`pip freeze` returns hundreds of Colab-internal packages:** that's normal. Commit it anyway — the professor said to freeze the full environment.
- **node2vec section failed in your run:** that's fine. The notebook handles it gracefully and the main findings don't depend on it. Just leave the output as-is.

Good luck.
