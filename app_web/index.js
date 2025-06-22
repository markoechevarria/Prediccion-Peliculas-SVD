const API_BASE = "";
let selected = new Map();

async function cargarPeliculas() {

    selected = new Map();

    const response = await fetch("/static/dataset_movies/movies.csv");
    const text = await response.text();
    const rows = text.trim().split('\n').slice(1);

    const agrupado = {};

    for (const row of rows) {
        const [movie_id, title] = row.split(',');
        const letra = title.trim().charAt(0).toUpperCase();

        if (!agrupado[letra]) agrupado[letra] = [];
        agrupado[letra].push({ movie_id, title });
    }

    const contenedor = document.getElementById("agrupado-por-letra");
    for (const letra of Object.keys(agrupado).sort()) {
        const toggle = document.createElement("div");
        toggle.className = "year-toggle";
        toggle.innerText = `📁 ${letra}`;
        contenedor.appendChild(toggle);

        const lista = document.createElement("div");
        lista.className = "movie-list";

        agrupado[letra].forEach(pelicula => {
            const item = document.createElement("div");
            item.className = "movie-item";
            item.dataset.id = pelicula.movie_id;

            const titulo = document.createElement("div");
            titulo.className = "movie-title";
            titulo.innerText = pelicula.title;

            const rating = document.createElement("select");
            [1, 2, 3, 4, 5].forEach(val => {
                const option = document.createElement("option");
                option.value = val;
                option.text = val;
                rating.appendChild(option);
            });


            const ratingDiv = document.createElement("div");
            ratingDiv.className = "movie-rating";
            ratingDiv.appendChild(rating);

            item.appendChild(titulo);
            item.appendChild(ratingDiv);

            rating.addEventListener("click", e => e.stopPropagation());

            item.addEventListener("click", () => {
                if (selected.has(pelicula.movie_id)) {
                    selected.delete(pelicula.movie_id);
                    item.classList.remove("selected");
                } else if (selected.size < 5) {
                    selected.set(pelicula.movie_id, rating);
                    item.classList.add("selected");
                } else {
                    alert("Solo puedes seleccionar 5 películas.");
                }
            });

            lista.appendChild(item);
        });

        toggle.addEventListener("click", () => {
            lista.style.display = lista.style.display === "block" ? "none" : "block";
        });

        contenedor.appendChild(lista);
    }
}

async function enviarRatings() {
  console.log("Enviando ratings:");
    if (selected.size !== 5) {
        alert("Selecciona exactamente 5 películas.");
        return;
    }

    const ratings = Array.from(selected.entries()).map(([movie_id, input]) => ({
        movie_id,
        rating: parseFloat(input.value) || 3
    }));

    const response = await fetch(`${API_BASE}/recomendaciones/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            user_id: "usuario_temp",
            ratings,
            top_n: 5
        })
    });

    const data = await response.json();
    mostrarRecomendaciones(data.recomendaciones);

    const metricas = await fetch(`${API_BASE}/metricas/`).then(r => r.json());
    mostrarMetricas(metricas);
}

function mostrarRecomendaciones(lista) {
  const contenedor = document.getElementById("recomendaciones");
  contenedor.innerHTML = "<h2> Tus recomendaciones:</h2>";
  lista.forEach(peli => {
    contenedor.innerHTML += `
      <div class="card">
        <div>
          <strong>🎬 ${peli.title}</strong><br>
          <span style="font-size: 14px; color: #9be49b;">
            📈 Predicción: ${peli.predicted_score.toFixed(2)} / 5.00
          </span>
        </div>
      </div>
    `;
  });
}

function mostrarMetricas(metricas) {
  const div = document.getElementById("metricas");
  if (metricas.success) {
    div.innerHTML = `
      <h2>📊 Precisión del Modelo</h2>
      <p>RMSE: <strong>${metricas.metricas.rmse.toFixed(4)}</strong> &nbsp;|&nbsp; MAE: <strong>${metricas.metricas.mae.toFixed(4)}</strong></p>
      <div style="max-width: 700px; margin: auto; font-size: 15px; color: #ccc;">
        <p>Este sistema utiliza un <strong>modelo de recomendación basado en SVD (Singular Value Decomposition)</strong>, que predice tus gustos analizando patrones de calificación entre miles de usuarios. El modelo estima qué tan probable es que te guste una película que aún no has visto, comparando tus calificaciones con las de otros usuarios similares.</p>
        <p><strong>RMSE (Root Mean Square Error)</strong> y <strong>MAE (Mean Absolute Error)</strong> son métricas que indican qué tan cerca están las predicciones del modelo respecto a las calificaciones reales. Mientras más bajos sean estos valores, mejor es la calidad de las predicciones.</p>
        <ul>
          <li><strong>RMSE</strong> penaliza más los errores grandes.</li>
          <li><strong>MAE</strong> es un promedio directo de los errores absolutos.</li>
        </ul>
      </div>
    `;
  } else {
    div.innerHTML = `<p>Error al obtener métricas: ${metricas.error}</p>`;
  }
}


cargarPeliculas();
