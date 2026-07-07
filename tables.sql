CREATE TABLE genre (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT
);

CREATE TABLE movie (
    id INTEGER PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    synopsis TEXT,
    director VARCHAR(255),
    cast TEXT,
    production_company VARCHAR(255)
);

CREATE TABLE movie_genre (
    movie_id INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,
    PRIMARY KEY (movie_id, genre_id),
    CONSTRAINT fk_movie FOREIGN KEY (movie_id) REFERENCES movie(id) ON DELETE CASCADE,
    CONSTRAINT fk_genre FOREIGN KEY (genre_id) REFERENCES genre(id) ON DELETE CASCADE
);

CREATE TABLE review (
    id INTEGER PRIMARY KEY,
    movie_id INTEGER NOT NULL,
    rate NUMERIC(3, 2) NOT NULL,
    note TEXT,
    CONSTRAINT fk_review_movie FOREIGN KEY (movie_id) REFERENCES movie(id) ON DELETE CASCADE
);