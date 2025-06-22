import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../datasets_procesados/ratings.csv")

plt.figure(figsize=(6,4))
df['rating'].value_counts().sort_index().plot(kind='bar', color="#4caf50")
plt.title("Distribución Ratings Reales")
plt.xlabel("Rating")
plt.ylabel("Cantidad")
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()