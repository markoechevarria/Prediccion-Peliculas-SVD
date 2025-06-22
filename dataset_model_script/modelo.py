from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split, cross_validate
from surprise import accuracy
from surprise.dump import dump
import pandas as pd
import json

ruta_ratings = "datasets/datasets_procesados/ratings.csv"
ruta_modelo = "model/svd_model"
ruta_metricas = "model/metricas.json"

ratings_df = pd.read_csv(ruta_ratings)

reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(ratings_df[["user_id", "movie_id", "rating"]], reader)

trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

model = SVD()
model.fit(trainset)

prediccion = model.test(testset)
rmse = accuracy.rmse(prediccion)

resultado = cross_validate(model, data, measures=["RMSE", "MAE"], cv=5, verbose=True)
rmse_promedio = resultado["test_rmse"].mean()
mae_promedio = resultado["test_mae"].mean()

dump(ruta_modelo, algo=model)

with open(ruta_metricas, "w") as f:
    json.dump({"rmse": rmse_promedio, "mae": mae_promedio}, f)