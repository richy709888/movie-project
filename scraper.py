import requests
import sqlite3

API_KEY = "PUT_YOUR_REAL_KEY_HERE"

url = "http://www.omdbapi.com/"
params = {
    "t": "The Godfather",
    "y": "1972",
    "apikey": API_KEY
}

response = requests.get(url, params=params)
data = response.json()

movie = {
    "title": data["Title"],
    "year": int(data["Year"]),
    "rating": float(data["imdbRating"]) if data["imdbRating"] != "N/A" else None,
    "poster_url": data["Poster"]
}

conn = sqlite3.connect("movies.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS api_movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    year INTEGER,
    rating REAL,
    poster_url TEXT
)
""")

cur.execute("""
INSERT INTO api_movies (title, year, rating, poster_url)
VALUES (?, ?, ?, ?)
""", (
    movie["title"],
    movie["year"],
    movie["rating"],
    movie["poster_url"]
))

conn.commit()
conn.close()

print("Saved:", movie["title"])
