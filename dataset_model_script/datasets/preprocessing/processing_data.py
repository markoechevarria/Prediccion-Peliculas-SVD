import pandas as pd

ruta = "../datasets/u.data"
ruta_guardar_csv = "../datasets_procesados/ratings.csv"

ratings = pd.read_csv(
	ruta,
	sep="\t",
	header = None,
	names=["user_id", "movie_id", "rating", "timestamp"]
)

ratings.to_csv(ruta_guardar_csv, index=False)