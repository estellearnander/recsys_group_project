# Recommendation Engines Group Project

IE University, Recommendation Engines course.

We play data scientists at a large company that currently shows products to customers at random. We build a recommender system that works for every customer (including new ones) and show the CEO how much value it adds compared with random display.

## Team and ownership

| Notebook | Owner |
|---|---|
| notebooks/00_build_dataset.ipynb | Estelle |
| notebooks/01_preprocessing.ipynb | Estelle |
| notebooks/02_eda.ipynb | Estelle |
| notebooks/03_recommenders.ipynb Part 1 (evaluation setup) and Part 2 (non-personalized) | Estelle |
| notebooks/03_recommenders.ipynb Parts 3 to 8 | (to be split at the meeting) |

## Folder structure

- notebooks/ has the four project notebooks (00 build dataset, 01 preprocessing, 02 EDA, 03 recommenders)
- notebooks/03_recommenders.ipynb is the main notebook with everything after the EDA. Part 1 is the shared evaluation setup.
- drafts/ is where each person develops their part (one draft notebook per person)
- data/ is where each person puts the dataset locally (it is never uploaded to GitHub)

## Setup

1. Clone the repository in PyCharm (File > New > Project from Version Control).
2. The cleaned dataset is already in `data/processed` after you pull. It is built from the raw MyAnimeList files by `notebooks/00_build_dataset.ipynb` and `notebooks/01_preprocessing.ipynb`, which only need to be rerun if the cleaning changes.
3. Install the packages (Python 3.12). recmetrics must be installed without its dependencies, because it pins old versions of pandas and seaborn (see Part 1 of notebooks/03_recommenders.ipynb).
   `pip install pandas pyarrow matplotlib pycountry scikit-surprise rexmex "seaborn>=0.13" "plotly>=5" funcsigs six`
   `pip install --no-deps recmetrics`
4. To work on your part, copy notebooks/03_recommenders.ipynb to drafts/yourname_part.ipynb, run Part 1 and add your part below it. When it is finished, one person pastes it into notebooks/03_recommenders.ipynb. Only that person edits the main notebook, so Git never has to merge two versions of it.
5. If you use the Kaggle API, put your own kaggle.json in the project root. It is in .gitignore so it is never uploaded.

## Rules

- Pull before you start working (Git > Pull).
- Only edit your own draft notebook. Use the split, relevance threshold and metric functions from Part 1 of 03_recommenders.
- Clear large outputs before committing (Clear All Outputs).
- Never commit data files or kaggle.json. The only exception is `data/processed`, the cleaned dataset everyone uses.
- Write short clear commit messages, for example "add TF-IDF content-based model".
