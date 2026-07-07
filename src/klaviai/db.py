import psycopg2
from psycopg2.extras import execute_values


class Database:

    def __init__(self, host: str, database: str, user: str, password: str):
        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
        )

        self.cursor = self.conn.cursor()

    def upsert_genres(self, genres):

        rows = [(g["id"], g["name"], g.get("description")) for g in genres]

        execute_values(
            self.cursor,
            """
            INSERT INTO genre(id,name,description)
            VALUES %s
            ON CONFLICT(id)
            DO UPDATE SET
                name=EXCLUDED.name,
                description=EXCLUDED.description
            """,
            rows,
        )

        self.conn.commit()

    def upsert_movie_genres(self, rows):

        execute_values(
            self.cursor,
            """
            INSERT INTO movie_genre(
                movie_id,
                genre_id
            )
            VALUES %s
            ON CONFLICT DO NOTHING
            """,
            rows,
        )

        self.conn.commit()

    def upsert_movies(self, movies):

        rows = [
            (
                m["id"],
                m["title"],
                m.get("synopsis"),
                m.get("diretor"),
                m.get("actors"),
                m.get("production_company"),
            )
            for m in movies
        ]

        execute_values(
            self.cursor,
            """
            INSERT INTO movie(
                id,
                title,
                sinopse,
                diretor,
                elenco,
                produtora
            )
            VALUES %s
            ON CONFLICT(id)
            DO UPDATE SET
                title=EXCLUDED.title,
                sinopse=EXCLUDED.sinopse,
                diretor=EXCLUDED.diretor,
                elenco=EXCLUDED.elenco,
                produtora=EXCLUDED.produtora
            """,
            rows,
        )

        self.conn.commit()

    def upsert_ratings(self, ratings):

        rows = [(r["id"], r["movie_id"], r["rate"], r.get("note")) for r in ratings]

        execute_values(
            self.cursor,
            """
            INSERT INTO avaliacao(
                id,
                movie_id,
                rate,
                note
            )
            VALUES %s
            ON CONFLICT(id)
            DO UPDATE SET
                rate=EXCLUDED.rate,
                note=EXCLUDED.note
            """,
            rows,
        )

        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
