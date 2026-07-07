import logging

from api import Api
from db import Database

logger = logging.getLogger(__name__)


def load_genres(api: Api, db: Database) -> list[dict]:
    logger.info("Loading genres...")

    genres = api.get("/obras/v3/generos")
    db.upsert_genres(genres)

    logger.info("Loaded %d genres.", len(genres))
    return genres


def load_movie_genres(api: Api, db: Database, genres: list[dict]) -> set[int]:
    logger.info("Loading movie-genre relationships...")

    movie_ids: set[int] = set()
    movie_genres: list[tuple[int, int]] = []

    for genre in genres:
        movies = api.get(f"/obras/v3/generos/{genre['id']}/filmes")

        for movie in movies:
            movie_ids.add(movie["id"])
            movie_genres.append((movie["id"], genre["id"]))

    db.upsert_movie_genres(movie_genres)

    logger.info(
        "Loaded %d movie-genre relationships for %d movies.",
        len(movie_genres),
        len(movie_ids),
    )

    return movie_ids


def load_movies(api: Api, db: Database, movie_ids: set[int]) -> None:
    logger.info("Loading movies...")

    movies = [api.get(f"/obras/v3/filmes/{movie_id}") for movie_id in movie_ids]

    db.upsert_movies(movies)

    logger.info("Loaded %d movies.", len(movies))


def load_ratings(api: Api, db: Database, movie_ids: set[int]) -> None:
    logger.info("Loading ratings...")

    ratings = []

    for movie_id in movie_ids:
        for rating in api.get(f"/obras/v3/filmes/{movie_id}/avaliacoes"):
            rating["filme_id"] = movie_id
            ratings.append(rating)

    db.upsert_ratings(ratings)

    logger.info("Loaded %d ratings.", len(ratings))


def etl(api: Api, db: Database) -> None:
    logger.info("Starting ETL.")

    genres = load_genres(api, db)
    movie_ids = load_movie_genres(api, db, genres)
    load_movies(api, db, movie_ids)
    load_ratings(api, db, movie_ids)

    logger.info("ETL finished successfully.")
