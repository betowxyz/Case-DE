from klaviai.api import API
from klaviai.db import Database
from klaviai.etl import etl
from klaviai.settings import settings


def main() -> None:
    api = API(
        base_url=settings.api.base_url,
        username=settings.api.username,
        password=settings.api.password,
    )

    db = Database(
        host=settings.database.host,
        port=settings.database.port,
        database=settings.database.database,
        user=settings.database.user,
        password=settings.database.password,
    )

    try:
        etl(api, db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
