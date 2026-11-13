# Recommendation Engines Group Project

IE University, Recommendation Engines course.

We play data scientists at a large company that currently shows products to customers at random. We build a recommender system that works for every customer (including new ones) and show the CEO how much value it adds compared with random display.

## Team and ownership

| Notebook | Owner |
|---|---|
| notebooks/01_data_and_baselines.ipynb | (name) |
| notebooks/02_collaborative_filtering.ipynb | (name) |
| notebooks/03_content_based.ipynb | (name) |
| notebooks/04_hybrid_context_bandits.ipynb | (name) |

## Folder structure

- notebooks/ has one notebook per person or section
- src/ has shared Python functions (data loading, metrics) used by all notebooks
- data/ is where each person puts the dataset locally (it is never uploaded to GitHub)

## Setup

1. Clone the repository in PyCharm (File > New > Project from Version Control).
2. Download the dataset and put the files in the data/ folder. (Dataset and download link to be added once the group decides.)
3. If you use the Kaggle API, put your own kaggle.json in the project root. It is in .gitignore so it is never uploaded.

## Rules

- Pull before you start working (Git > Pull).
- Only edit your own notebook. Shared code goes in src/.
- Clear large outputs before committing (Clear All Outputs).
- Never commit data files or kaggle.json.
- Write short clear commit messages, for example "add TF-IDF content-based model".
