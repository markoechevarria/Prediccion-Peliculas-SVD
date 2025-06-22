import pandas as pd

ruta = "../datasets/u.item"
ruta_guardar = "../datasets_procesados/movies.csv"

item_cols = [
    "movie_id", "title", "release_date", "video_release_date", "IMDb_URL",
    "unknown", "Action", "Adventure", "Animation", "Children's", "Comedy",
    "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror",
    "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"
]

movies = pd.read_csv(
	ruta,
	sep="|",
	header = None,
	names=item_cols,
	encoding="latin-1"
)

movies_simple = movies[["movie_id", "title"]]

movies_simple.to_csv(ruta_guardar, index=False)
