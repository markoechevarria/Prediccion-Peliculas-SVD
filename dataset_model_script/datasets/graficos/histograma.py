from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("../datasets_procesados/ratings.csv")
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(df[['user_id', 'movie_id', 'rating']], reader)
trainset, testset = train_test_split(data, test_size=0.2)

model = SVD()
model.fit(trainset)
predictions = model.test(testset)

errors = [pred.r_ui - pred.est for pred in predictions]

plt.figure(figsize=(7,4))
plt.hist(errors, bins=30, color="#ff9900f4", edgecolor="black")
plt.title("Histograma errores de prediccion (rating real vs prediccion)") 
plt.xlabel("Error")
plt.ylabel("Frecuencia")
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()