from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import pandas as pd
from surprise import dump, Dataset, Reader, SVD
import json

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

ratings_df_original = pd.read_csv("dataset_model_script/datasets/datasets_procesados/ratings.csv")

modelo_entrenado = "dataset_model_script/model/svd_model"
ruta_movies = "dataset_model_script/datasets/datasets_procesados/movies.csv"
ruta_json = "dataset_model_script/model/metricas.json"

model = dump.load(modelo_entrenado)[1]
movies = pd.read_csv(ruta_movies)
movies_ids = movies['movie_id'].astype(str).tolist()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app_web"), name="static")

@app.get("/")
def root():
    return FileResponse("app_web/index.html")

class RatingPelicula(BaseModel):
    movie_id: str
    rating: float

class UsuarioRatingPelicula(BaseModel):
    user_id: str
    ratings: List[RatingPelicula]
    top_n: int = 10

@app.post("/recomendaciones/")
def recomendaciones_personalizada(data: UsuarioRatingPelicula):
    rating_usuario_df = pd.DataFrame([{
        "user_id": data.user_id,
        "movie_id": r.movie_id,
        "rating": r.rating
    } for r in data.ratings])

    df_combinado = pd.concat([ratings_df_original, rating_usuario_df], ignore_index=True)

    reader = Reader(rating_scale=(1, 5))
    data_temp = Dataset.load_from_df(df_combinado[["user_id", "movie_id", "rating"]], reader)
    trainset_temp = data_temp.build_full_trainset()

    model_temp = SVD()
    model_temp.fit(trainset_temp)

    rated_ids = set(rating_usuario_df["movie_id"].astype(str))
    peliculas_no_vistas = [mid for mid in movies_ids if mid not in rated_ids]

    predicciones = [
        (mid, model_temp.predict(data.user_id, int(mid)).est)
        for mid in peliculas_no_vistas
    ]

    top_predicciones = sorted(predicciones, key=lambda x: x[1], reverse=True)[:data.top_n]

    resultados = []
    for movie_id, score in top_predicciones:
        row = movies[movies["movie_id"].astype(str) == movie_id]
        if not row.empty:
            resultados.append({
                "movie_id": movie_id,
                "title": row.iloc[0]["title"],
                "predicted_score": round(score, 3)
            })

    return {
        "user_id": data.user_id,
        "recomendaciones": resultados
    }

@app.get("/metricas/")
def obtener_metricas_modelo():
    try:
        with open(ruta_json, "r") as f:
            metricas = json.load(f)
        return {"success": True, "metricas": metricas}
    except Exception as e:
        return {"success": False, "error": str(e)}
    
@app.get("/")
def serve_root():
    return FileResponse("../app_web/index.html")