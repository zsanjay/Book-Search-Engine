import numpy as np
import pandas as pd
import psycopg2
import re

def to_snake_case(col):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', col).lower()

df = pd.read_csv('books.csv')

columns = [to_snake_case(col) for col in df.columns]

conn_string = "host='localhost' dbname='library' user='admin' password='admin123' port='5432'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor();

# Remove 'author' column for books table
books_columns = [col for col in columns if col != 'author']

replacements = {
    'book_id' : 'int',
    'title' : 'varchar(255)',
    'series' : 'varchar(255)',
    'rating' : 'float',
    'description' : 'text',
    'language' : 'varchar(50)',
    'isbn' : 'varchar(20)',
    'genres' : 'text',
    'characters' : 'text',
    'book_format' : 'varchar(50)',
    'edition' : 'varchar(100)',
    'pages' : 'int',
    'publisher' : 'varchar(255)',
    'publish_date' : 'date',
    'first_publish_date' : 'date',
    'awards' : 'text',
    'num_ratings' : 'int',
    'ratings_by_stars' : 'text',
    'liked_percent' : 'float',
    'setting' : 'text',
    'cover_img' : 'text',
    'bbe_score' : 'float',
    'bbe_votes' : 'int',
    'price' : 'float'
}

# Convert 'publishDate' and 'firstPublishDate' columns to YYYY-MM-DD
for col in ['publishDate', 'firstPublishDate']:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors='coerce').dt.date

# Insert books data
for _, row in df.iterrows():
     placeholders = ', '.join(['%s'] * len(books_columns))
     cols = ', '.join(books_columns)
     sql = f"INSERT INTO books ({cols}) VALUES ({placeholders})"
     row_values = [None if pd.isna(row[col]) else row[col] for col in df.columns if col not in ['author']]
     book_id_value = row_values[0]
     if "-" in str(book_id_value):
         bookId = str(book_id_value).split("-")[0]
     else:
         bookId = str(book_id_value).split(".")[0]
     row_values[0] = int(bookId)
     cursor.execute(sql, tuple(row_values))

# Insert authors data
if 'author' in df.columns:
    authors = df['author'].dropna().unique()
    for index, author in enumerate(authors):
        author = author[:255]
        cursor.execute("INSERT INTO authors (author_id, name) VALUES (%s, %s) ON CONFLICT DO NOTHING", (index + 1, author))

conn.commit()
cursor.close()
conn.close()