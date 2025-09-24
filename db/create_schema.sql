-- We are using POSTGRESQL 17.6 
-- CSV header is below
-- bookId,	title,	series,	author,	rating,	description,	language,  	isbn,	genres,	characters,	bookFormat,	edition,	pages,	publisher,	publishDate,	firstPublishDate, awards,	numRatings,	ratingsByStars,	likedPercent,	setting,	coverImg,	bbeScore,	bbeVotes,	price

-- create the books table
CREATE TABLE IF NOT EXISTS books (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    series VARCHAR(255),
    rating FLOAT,
    description TEXT,
    language VARCHAR(50),
    isbn VARCHAR(20),
    genres TEXT,
    characters TEXT,
    book_format VARCHAR(50),
    edition VARCHAR(100),
    pages INT,
    publisher VARCHAR(255),
    publish_date DATE,
    first_publish_date DATE,
    awards TEXT,
    num_ratings INT,
    ratings_by_stars TEXT,
    liked_percent FLOAT,
    setting TEXT,
    cover_img TEXT,
    bbe_score FLOAT,
    bbe_votes INT,
    price FLOAT
);

-- create author table
CREATE TABLE IF NOT EXISTS authors (
    author_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- create book_author junction table
CREATE TABLE IF NOT EXISTS book_author (
    book_id INT REFERENCES books(book_id) ON DELETE CASCADE,
    author_id INT REFERENCES authors(author_id) ON DELETE CASCADE,
    PRIMARY KEY (book_id, author_id)
);


