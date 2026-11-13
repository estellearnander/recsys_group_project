"""Build the combined anime dataset used by the whole group.

Sources (all in data/raw):
- 2018 MyAnimeList dataset (Kaggle: azathoth42/myanimelist)
    users_cleaned.csv       users with gender, location and birth date
    animelists_cleaned.csv  one row per user and anime (score, status, timestamps)
    anime_cleaned.csv       anime metadata
- 2020 MyAnimeList dataset (GitHub: Hernan4444/MyAnimeList-Database)
    anime_with_synopsis.csv synopsis text, joined on the anime id

Output (in data/processed):
- users.parquet         one row per user (no usernames, only user_id)
- anime.parquet         one row per anime, metadata plus synopsis
- interactions/         one row per user and anime, with user attributes and
                        basic anime info already joined (split into parts)

Usage:
    from src.data import build_all, load_interactions, load_anime, load_users
    build_all()   # run once, takes a few minutes
"""

import os
import pandas as pd

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
INTERACTIONS_DIR = os.path.join(PROCESSED_DIR, "interactions")

# Ages outside this range are treated as fake birth dates
MIN_AGE = 5
MAX_AGE = 90

CHUNK_SIZE = 2_000_000


def build_users():
    """Clean the users table and save it. Returns the cleaned dataframe."""
    users = pd.read_csv(
        os.path.join(RAW_DIR, "users_cleaned.csv"),
        usecols=["username", "user_id", "gender", "location", "birth_date", "join_date"],
    )

    users["birth_date"] = pd.to_datetime(users["birth_date"], errors="coerce")
    users["join_date"] = pd.to_datetime(users["join_date"], errors="coerce")

    # Location is free text typed by the user, the last part is usually the country
    users["location"] = users["location"].astype(str).str.strip()
    users["country"] = users["location"].str.split(",").str[-1].str.strip()

    os.makedirs(PROCESSED_DIR, exist_ok=True)
    # Usernames are not saved, only the numeric user_id
    users.drop(columns=["username"]).to_parquet(
        os.path.join(PROCESSED_DIR, "users.parquet"), index=False
    )
    return users


def build_anime():
    """Join the 2018 anime metadata with the 2020 synopsis and save it."""
    anime = pd.read_csv(
        os.path.join(RAW_DIR, "anime_cleaned.csv"),
        usecols=[
            "anime_id", "title", "title_english", "type", "source", "episodes",
            "rating", "score", "scored_by", "members", "popularity", "premiered",
            "studio", "genre", "duration_min", "aired_from_year",
        ],
    )

    synopsis = pd.read_csv(
        os.path.join(RAW_DIR, "anime_with_synopsis.csv"),
        usecols=["MAL_ID", "sypnopsis"],
    )
    synopsis = synopsis.rename(columns={"MAL_ID": "anime_id", "sypnopsis": "synopsis"})

    # Left join so no 2018 anime is lost, anime without a match get an empty synopsis
    anime = anime.merge(synopsis, on="anime_id", how="left")

    os.makedirs(PROCESSED_DIR, exist_ok=True)
    anime.to_parquet(os.path.join(PROCESSED_DIR, "anime.parquet"), index=False)
    return anime


def build_interactions(users, anime, max_chunks=None):
    """Read the big animelists file in chunks, clean it, join user attributes and
    basic anime info, and save each chunk as a parquet part.

    Parts that already exist are skipped, so this can be stopped and restarted.
    """
    os.makedirs(INTERACTIONS_DIR, exist_ok=True)

    user_cols = users[["username", "user_id", "gender", "country", "birth_date"]]
    anime_cols = anime[["anime_id", "title", "genre", "type"]]

    reader = pd.read_csv(
        os.path.join(RAW_DIR, "animelists_cleaned.csv"),
        usecols=[
            "username", "anime_id", "my_watched_episodes", "my_start_date",
            "my_finish_date", "my_score", "my_status", "my_last_updated",
        ],
        chunksize=CHUNK_SIZE,
    )

    done = 0
    for i, chunk in enumerate(reader):
        part_path = os.path.join(INTERACTIONS_DIR, f"part_{i:03d}.parquet")
        if os.path.exists(part_path):
            continue

        chunk = chunk.rename(columns={
            "my_watched_episodes": "watched_episodes",
            "my_start_date": "start_date",
            "my_finish_date": "finish_date",
            "my_score": "score",
            "my_status": "status",
            "my_last_updated": "last_updated",
        })

        # 0000-00-00 and other invalid dates become NaT
        for col in ["start_date", "finish_date", "last_updated"]:
            chunk[col] = pd.to_datetime(chunk[col], errors="coerce")

        chunk = chunk.merge(user_cols, on="username", how="inner")
        chunk = chunk.merge(anime_cols, on="anime_id", how="left")

        # Age of the user when the entry was last updated
        age = (chunk["last_updated"] - chunk["birth_date"]).dt.days / 365.25
        chunk["age"] = age.where((age >= MIN_AGE) & (age <= MAX_AGE)).round()

        chunk = chunk.drop(columns=["username", "birth_date"])
        chunk.to_parquet(part_path, index=False)

        done += 1
        if max_chunks is not None and done >= max_chunks:
            return False  # not finished yet
    return True


def build_all():
    users = build_users()
    anime = build_anime()
    build_interactions(users, anime)


def load_users():
    return pd.read_parquet(os.path.join(PROCESSED_DIR, "users.parquet"))


def load_anime():
    return pd.read_parquet(os.path.join(PROCESSED_DIR, "anime.parquet"))


def load_interactions(columns=None):
    return pd.read_parquet(INTERACTIONS_DIR, columns=columns)
