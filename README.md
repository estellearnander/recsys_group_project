# Recommendation Engines Group Project

IE University, Recommendation Engines course.

We play data scientists at a large company that currently shows products to customers at random. We build a recommender system that works for every customer (including new ones) and show the CEO how much value it adds compared with random display.

## Team and ownership

| Notebook | Owner |
|---|---|
| notebooks/00_build_dataset.ipynb | Estelle |
| notebooks/01_preprocessing.ipynb | Estelle |
| notebooks/02_eda.ipynb | Estelle |
| notebooks/03_collaborative_filtering.ipynb | (name) |
| notebooks/04_content_based.ipynb | (name) |
| notebooks/05_hybrid_context_bandits.ipynb | (name) |

## Folder structure

- notebooks/ has one notebook per person or section
- src/ has shared Python functions (data loading, metrics) used by all notebooks
- data/ is where each person puts the dataset locally (it is never uploaded to GitHub)

## Setup

1. Clone the repository in PyCharm (File > New > Project from Version Control).
2. The cleaned dataset is already in `data/processed` after you pull. It is built from the raw MyAnimeList files by `notebooks/00_build_dataset.ipynb` and `notebooks/01_preprocessing.ipynb`, which only need to be rerun if the cleaning changes.
3. If you use the Kaggle API, put your own kaggle.json in the project root. It is in .gitignore so it is never uploaded.

## Rules

- Pull before you start working (Git > Pull).
- Only edit your own notebook. Shared code goes in src/.
- Clear large outputs before committing (Clear All Outputs).
- Never commit data files or kaggle.json. The only exception is `data/processed`, the cleaned dataset everyone uses.
- Write short clear commit messages, for example "add TF-IDF content-based model".
